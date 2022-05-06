import xlrd
import xlwt
from collections import Counter

data = xlrd.open_workbook('../data/final.xls')
table = data.sheets()[0]
tagList = []
for i in range(1, table.nrows):
    row = table.row_values(i)
    tagStr = row[8]
    subTagList = tagStr.split(',')
    for tag in subTagList:
        tagList.append(tag)
    print("第" + str(i) + "行处理完成")
tagCount = Counter(tagList).most_common(200)
tagFile = xlwt.Workbook()
sheet = tagFile.add_sheet('tags')
for i in range(0, len(tagCount)):
    sheet.write(i, 0, tagCount[i][0])
    sheet.write(i, 1, tagCount[i][1])
tagFile.save('../data/tags.xls')
print("处理完成")
