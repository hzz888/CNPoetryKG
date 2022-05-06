import xlrd
import xlwt
import re
from collections import Counter

data = xlrd.open_workbook('../data/final.xls')
table = data.sheets()[0]
seasonList = []
seasons = ['春', '夏', '秋', '冬']

for i in range(1, table.nrows):
    row = table.row_values(i)
    poemBody = row[4]
    poemWords = re.findall(r'[\u4e00-\u9fa5]', poemBody)
    for word in poemWords:
        if word in seasons:
            seasonList.append(word)
        else:
            continue
    print("第" + str(i) + "首处理完成")

seasonCount = Counter(seasonList).most_common(4)

seasonFile = xlwt.Workbook()
sheet = seasonFile.add_sheet('seasons')
for i in range(0, len(seasonCount)):
    sheet.write(i, 0, seasonCount[i][0])
    sheet.write(i, 1, seasonCount[i][1])
seasonFile.save('../data/seasons.xls')
print("处理完成")
