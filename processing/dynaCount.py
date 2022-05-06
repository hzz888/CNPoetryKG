import xlrd
import xlwt
from collections import Counter

data = xlrd.open_workbook('../data/final.xls')
table = data.sheets()[0]
dynastyList = []
for i in range(1, table.nrows):
    row = table.row_values(i)
    dynasty = row[1]
    dynastyList.append(dynasty)
    print("第" + str(i) + "行处理完成")
dynastyCount = Counter(dynastyList).most_common(len(dynastyList))
dynastyFile = xlwt.Workbook()
sheet = dynastyFile.add_sheet('dynasties')
for i in range(0, len(dynastyCount)):
    sheet.write(i, 0, dynastyCount[i][0])
    sheet.write(i, 1, dynastyCount[i][1])
dynastyFile.save('../data/dynasty.xls')
print("处理完成")
