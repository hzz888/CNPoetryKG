import json
import time
from hanlp_restful import HanLPClient
import xlrd
import xlwt

HanLP = HanLPClient('https://www.hanlp.com/api', auth='MTA5MEBiYnMuaGFubHAuY29tOkVFVHJOWUdaV09PeGFpdzc=', language='zh')

poemData = xlrd.open_workbook('../data/final.xls')
table = poemData.sheets()[0]

locaList = []

for i in range(1, table.nrows):
    row = table.row_values(i)
    poemBody = row[4]
    translation = row[5]
    appreciation = row[6]
    background = row[7]
    poemInfo = poemBody + translation + appreciation + background
    sentences = poemInfo.split('。')
    locas = []
    for sentence in sentences:
        pos_response = str(HanLP(sentence, tasks='pos/pku'))
        pos_result = json.loads(pos_response)
        time.sleep(1.25)
        if 'ns' in pos_result['pos/pku']:
            location = pos_result['tok/fine'][pos_result['pos/pku'].index('ns')]
            locas.append(location)
        else:
            pass
    locas = list(set(locas))
    locaList.append(locas)
    print('已完成第' + str(i) + '首诗的地点信息提取')

locaFile = xlwt.Workbook()
locaSheet = locaFile.add_sheet('sheet1')
locaSheet.write(0, 0, '相关地点')
j = 0
for i in range(1, len(locaList)):
    locaSheet.write(i, 0, ','.join(locaList[j]))
    j += 1

locaFile.save('../data/location.xls')
print('地点信息补全完成')
