import numpy as np

np.random.seed(0) # set same seed for all processes
import pandas as pd

import os
from tqdm import tqdm

from collections import defaultdict
import transformers
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup

import torch
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler
import torch.distributed as dist
import torch.multiprocessing as mp
import torch.nn as nn
import torch.optim as optim
from torch.nn.parallel import DistributedDataParallel as DDP

from _thread import start_new_thread
from functools import wraps # wraps装饰器
import traceback

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import copy
import time

root = './'


class SentimentClassifier(nn.Module):

    def __init__(self, hidden_dim, n_layers, n_classes):
        super().__init__()
        # BERT 层
        self.bert = BertModel.from_pretrained(pretrained_model_name_or_path=".")
        # LSTM 层
        self.lstm = nn.LSTM(
            input_size=self.bert.config.hidden_size, # 将bilstm的输入尺寸设置为bert的词嵌入长度
            hidden_size=hidden_dim, # bilstm词嵌入长度设为自身隐藏状态大小
            num_layers=n_layers,
            batch_first=True,
            bidirectional=True # bilstm是双向的
        )

        self.drop = nn.Dropout(p=0.5) # 防止过拟合
        self.out = nn.Sequential(
            nn.Linear(hidden_dim * 2 * n_layers, hidden_dim),  # 线性层
            nn.Linear(hidden_dim, hidden_dim),
            nn.ELU(),
            nn.Linear(hidden_dim, n_classes)
        )

    def forward(self, encoded_input):
        output = self.bert(**encoded_input)
        # print(output.last_hidden_state.shape)
        embedded = output.last_hidden_state

        self.lstm.flatten_parameters()  # 重置参数数据指针
        # for warning below
        # UserWarning: RNN module weights are not part of single contiguous chunk of memory. 
        # This means they need to be compacted at every call, possibly greatly increasing memory usage. 
        # To compact weights again call flatten_parameters(). 
        # text -> [batch_size, sequence_length]
        # embedded = self.embedding(text) # Create embedding of the input text  text -> [batch_size, sequence_length, emb_dim]
        # Handle padding to ignore padding during training of the RNN

        # disable the pack_padded_sequence function for the ability to handle empty token list
        # packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, text_lengths.cpu(), batch_first=True, enforce_sorted=False)
        output, (hidden, cell) = self.lstm(embedded)  # hidden -> [num_direction*num_layers, batch_size, emb_dim]

        # hidden -> [batch_size, emb_dim*num_direction*num_layers] 
        hidden = hidden.permute(1, 0, 2).reshape(output.shape[0],
                                                 -1)  # Concatenate the forward and backward hidden state of each layer

        output = self.out(hidden)  # [batch_size, n_classes]

        return output


class TMPDataset(Dataset):
    def __init__(self, df):
        self.df = df
        self.X = df['text'].values
        self.y = df['label'].values

    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def thread_wrapped_func(func):
    """
    Wraps a process entry point to make it work with OpenMP.
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        queue = mp.Queue()

        def _queue_result():
            exception, trace, res = None, None, None
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                exception = e
                trace = traceback.format_exc()
            queue.put((res, exception, trace))

        start_new_thread(_queue_result, ())
        result, exception, trace = queue.get()
        if exception is None:
            return result
        else:
            assert isinstance(exception, Exception)
            raise exception.__class__(trace)

    return decorated_function


def setup(rank, world_size):
    # os.environ['MASTER_ADDR'] = 'localhost'
    # os.environ['MASTER_PORT'] = '123456'
    dist_init_method = 'tcp://{master_ip}:{master_port}'.format(
        master_ip='127.0.0.1', master_port='12345')

    # initialize the process group to do distributed training
    dist.init_process_group(backend="nccl", init_method=dist_init_method,
                            rank=rank, world_size=world_size)


def cleanup():
    dist.destroy_process_group()


def run_(rank, world_size, data):
    print(f"Running process on rank {rank}.")
    setup(rank, world_size)

    # create model and move it to GPU with id rank
    model = SentimentClassifier(hidden_dim=256, n_layers=2, n_classes=4).to(rank)
    if rank == 0:
        print(model)
        total_params = sum(p.numel() for p in model.parameters() if p.requires_grad) # 查看模型参数数量
        print(f"model total params {total_params}")
    # ddp model
    ddp_model = DDP(model, device_ids=[rank], output_device=rank, find_unused_parameters=True)

    loss_fn = nn.CrossEntropyLoss()

    EPOCHS = 10 # 训练轮数
    tokenizer = BertTokenizer.from_pretrained(pretrained_model_name_or_path=".")  # bert-base-chinese
    optimizer = AdamW(ddp_model.parameters(), lr=5e-5, correct_bias=False, no_deprecation_warning=True)

    # Split train_nid and create dataloader
    train_dataset = TMPDataset(data['data_train'])
    # shuffle data
    sampler = DistributedSampler(train_dataset)
    train_dataloader = DataLoader(
        train_dataset, shuffle=False, drop_last=True,
        sampler=sampler, x_size=data['bs']
    )

    total_steps = len(train_dataloader) * EPOCHS
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=total_steps // 5,
        num_training_steps=total_steps
    )

    # val and test dataloader in rank 0 
    if rank == 0:
        test_dataset = TMPDataset(data['data_test'])
        test_dataloader = DataLoader(
            test_dataset, shuffle=False, drop_last=False,
            batch_size=data['bs']
        )

    for epoch in range(data['n_epoch']):
        sampler.set_epoch(epoch)
        time_start = time.time()
        for batch_idx, (X, y) in enumerate(tqdm(train_dataloader)):
            y = y.to(rank)
            ddp_model.train()
            optimizer.zero_grad()

            encoded_input = tokenizer(list(X), padding=True, truncation=True, return_tensors="pt", max_length=256)
            encoded_input = {k: v.to(rank) for k, v in encoded_input.items()}
            output = ddp_model(encoded_input)
            loss = loss_fn(output, y)
            loss.backward()
            optimizer.step()
            scheduler.step()
        # wait for other rank
        torch.distributed.barrier()
        time_end = time.time()

        # validation master node(rank==0) after each epoch
        if rank == 0:
            print(f'Epoch {epoch:2} Train Time(s): {time_end - time_start:4.2f}', end=' ')
            ddp_model.eval()
            with torch.no_grad():
                y_pred_val = []
                y_true_val = []
                for batch_idx, (X, y) in enumerate(tqdm(test_dataloader)):
                    y = y.to(rank)
                    encoded_input = tokenizer(
                        list(X), padding=True, truncation=True,
                        return_tensors="pt", max_length=256
                    )
                    encoded_input = {k: v.to(rank) for k, v in encoded_input.items()}
                    output = ddp_model(encoded_input)
                    y_pred_val.append(output)
                    y_true_val.append(y)

                y_pred_val = torch.cat(y_pred_val, axis=0)
                y_true_val = torch.cat(y_true_val, axis=0)
                # compute metrics
                y_true_val = y_true_val.cpu().numpy()
                y_pred_val = y_pred_val.cpu().numpy()
                y_pred_val = y_pred_val.argmax(axis=1)

                val_acc = (y_pred_val == y_true_val).sum() / y_true_val.shape[0]
                # log val
                print(
                    f'Val Time(s): {time.time() - time_end:4.2f} | ' +  # {[argument_index_or_keyword]:[width][.precision][type]}
                    f'Val ACC: {val_acc:.4f}'
                )
                torch.save(ddp_model.module.state_dict(), f'./{epoch}_{val_acc:.4f}.pt')
        print('barrier')
        # wait other ranks
        

    cleanup()


def main_():
    '''
    '''
    moods = {0: '喜悦', 1: '愤怒', 2: '厌恶', 3: '低落'}
    data = pd.read_csv(f"{root}/simplifyweibo_4_moods.csv")
    data = data.rename(columns={'review': 'text'})
    data = data.sample(frac=0.05)
    data_train, data_test = train_test_split(data, random_state=0, test_size=0.4)
    
    data = dict()
    data['data_train'] = data_train
    data['data_test'] = data_test
    data['bs'] = 32 # set batch size to 32
    data['n_epoch'] = 10

    world_size = 8  # distributed training
    procs = []
    for rank in range(world_size):
        p = mp.Process(target=thread_wrapped_func(run_),
                       args=(rank, world_size, data))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()


if __name__ == "__main__":
    main_()
