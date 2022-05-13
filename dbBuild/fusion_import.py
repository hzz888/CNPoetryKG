import xlrd
from py2neo import *
import re

graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
matcher = NodeMatcher(graph)
dataFile = xlrd.open_workbook('../data/final.xls')
sheet = dataFile.sheet_by_index(0)

pattern = re.compile(r'[^\u4e00-\u9fa5]')

for i in range(1, sheet.nrows):
    row = sheet.row_values(i)

    poemName = row[0]
    poemForm = re.sub(pattern, '', row[13])
    poemOrigin = re.sub(pattern, '', row[14])

    titleNode = matcher.match("标题", name=poemName).first()

    formNode = Node('文学体裁', name=poemForm)
    formNode.__primarylabel__ = '文学体裁'
    formNode.__primarykey__ = 'name'

    oriNode = Node('作品出处', name=poemOrigin)
    oriNode.__primarylabel__ = '作品出处'
    oriNode.__primarykey__ = 'name'

    if poemForm != '无此属性' and poemForm != '该图谱中无此数据':
        graph.merge(formNode)
        title_form = Relationship(titleNode, '文学体裁', formNode)
        graph.create(title_form)
    else:
        pass

    if poemOrigin != '无此属性' and poemOrigin != '该图谱中无此数据':
        graph.merge(oriNode)
        title_ori = Relationship(titleNode, '作品出处', oriNode)
        graph.create(title_ori)
    else:
        pass

    print('第' + str(i) + '行导入完成')
