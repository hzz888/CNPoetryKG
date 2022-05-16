import xlrd
from py2neo import *

dataFile = xlrd.open_workbook('../data/final.xls')
sheet = dataFile.sheet_by_index(0)

graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
matcher = NodeMatcher(graph)

for i in range(1, sheet.nrows):
    row = sheet.row_values(i)
    poemName = row[0].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    authorName = row[2].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    authorLoca = row[15]
    poemLoca = row[16]

    titleNode = matcher.match('标题', name=poemName).first()
    authorNode = matcher.match('作者', name=authorName).first()

    if authorLoca:
        for e in authorLoca.split(','):
            authorLocaNode = Node('地点', name=e)
            authorLocaNode.__primarylabel__ = '地点'
            authorLocaNode.__primarykey__ = 'name'
            graph.merge(authorLocaNode)

            authorLocationRelation = Relationship(authorNode, '诗人相关地点', authorLocaNode)
            graph.merge(authorLocationRelation)
    else:
        pass

    if poemLoca:
        for r in poemLoca.split(','):
            poemLocaNode = Node('地点', name=r)
            poemLocaNode.__primarylabel__ = '地点'
            poemLocaNode.__primarykey__ = 'name'
            graph.merge(poemLocaNode)

            poemLocationRelation = Relationship(titleNode, '本诗相关地点', poemLocaNode)
            graph.create(poemLocationRelation)
    else:
        pass
    print('第{}行导入完成'.format(i))
print('导入完成')
