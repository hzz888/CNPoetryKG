import xlrd
import xlwt
from collections import Counter

data = xlrd.open_workbook('../data/final.xls')
table = data.sheets()[0]
authorList = []
for i in range(1, table.nrows):
    row = table.row_values(i)
    author = row[2]
    authorList.append(author)
    print("第" + str(i) + "行处理完成")
authorCount = Counter(authorList).most_common(50)
authorFile = xlwt.Workbook()
sheet = authorFile.add_sheet('authors')
for i in range(0, len(authorCount)):
    sheet.write(i, 0, authorCount[i][0])
    sheet.write(i, 1, authorCount[i][1])
authorFile.save('../data/author.xls')
print("处理完成")
