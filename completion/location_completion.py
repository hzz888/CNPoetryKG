from hanlp_restful import HanLPClient
import xlrd

HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')  # auth不填则匿名，zh中文，mul多语种
poemData = xlrd.open_workbook('../data/final.xls')
table = poemData.sheets()[0]
for i in range(1, table.nrows):
    row = table.row_values(i)
    poemBody = row[4]
    translation = row[5]
    appreciation = row[6]
    background = row[7]
    poemInfo = poemBody + translation + appreciation + background
    sentences = poemInfo.split('。')
    for sentence in sentences:
        pass
