import xlrd
import xlwt
import re
from collections import Counter

data = xlrd.open_workbook('../data/final.xls')
table = data.sheets()[0]
wordList = []

xuci = '当｜使｜从｜入｜至｜闻｜成｜然｜能｜里｜外｜在｜十｜余｜前｜后｜作｜出｜矣｜公｜吾｜欲｜处｜将｜百｜千｜万｜曰｜如｜有｜时｜相｜我｜君｜而｜何｜乎｜乃｜其｜且｜若｜所｜为｜焉｜以｜因｜于｜与｜也｜则｜者｜之｜不｜子｜自｜得｜一｜来｜去｜无｜可｜是｜故｜已｜此｜的｜上｜中｜兮｜三｜四｜下｜'

for i in range(1, table.nrows):
    row = table.row_values(i)
    poemBody = row[4]
    poemWords = re.findall(r'[\u4e00-\u9fa5]', poemBody)
    for word in poemWords:
        if word not in xuci:
            wordList.append(word)
        else:
            continue
    print("第" + str(i) + "首处理完成")

topWords = Counter(wordList).most_common(300)

topWordsFile = xlwt.Workbook()
sheet = topWordsFile.add_sheet('singleCount')
for i in range(0, len(topWords)):
    sheet.write(i, 0, topWords[i][0])
    sheet.write(i, 1, topWords[i][1])
topWordsFile.save('../data/topWords.xls')
print("处理完成")
