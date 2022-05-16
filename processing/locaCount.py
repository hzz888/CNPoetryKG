import xlrd
from collections import Counter
import xlwt

dataFile = xlrd.open_workbook('../data/locations.xls')
dataSheet = dataFile.sheet_by_index(0)
temList = []
for i in range(1, dataSheet.nrows):
    row = dataSheet.row_values(i)
    loca1 = row[0]
    loca2 = row[1]
    locaList = loca1.split(',') + loca2.split(',')
    for loca in locaList:
        temList.append(loca)

locaCounter = Counter(temList).most_common(51)
locaCountFile = xlwt.Workbook()
sheet = locaCountFile.add_sheet('sheet1')
sheet.write(0, 0, 'name')
sheet.write(0, 1, 'value')
for i in range(len(locaCounter)):
    sheet.write(i+1, 0, locaCounter[i][0])
    sheet.write(i+1, 1, locaCounter[i][1])
locaCountFile.save('../data/locaCount.xls')
print('Done!')
