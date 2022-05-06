import xlrd
from jiayan import PMIEntropyLexiconConstructor

data = xlrd.open_workbook('../data/final.xls')
table = data.sheets()[0]
poemGroup = ""
for i in range(1, table.nrows):
    row = table.row_values(i)
    body = row[4]
    poemGroup += body
with open('../data/poemGroup.txt', 'w') as f:
    f.write(poemGroup)
constrctor = PMIEntropyLexiconConstructor()
lexicon = constrctor.construct_lexicon('../data/poemGroup.txt')
constrctor.save(lexicon, '../data/vocaLib.csv')
