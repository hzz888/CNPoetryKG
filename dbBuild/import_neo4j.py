import xlrd
from py2neo import *

graph = Graph("bolt://localhost:7687", auth=("neo4j", "6886089"))

data = xlrd.open_workbook('../data/final.xls')
table = data.sheets()[0]

for i in range(1, table.nrows):  # 第一行为表头，从第二行开始读取
    row = table.row_values(i)

    title = row[0].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    dynasty = row[1].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    author = row[2].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    authorIntro = row[3].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    body = row[4].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    translation = row[5].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    appreciation = row[6].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    background = row[7].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    tagStr = row[8].replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    tagList = tagStr.split(',')
    happyFactor = str(row[9]).replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    angryFactor = str(row[10]).replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    dislikeFactor = str(row[11]).replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")
    sadFactor = str(row[12]).replace(" ", "").replace("\r", "").replace("\t", "").replace("\n", "")

    # 创建节点
    titleNode = Node("标题", name=title)
    titleNode.__primarylabel__ = "标题"
    titleNode.__primarykey__ = "name"
    graph.create(titleNode)

    dynastyNode = Node("朝代", name=dynasty)
    dynastyNode.__primarylabel__ = "朝代"
    dynastyNode.__primarykey__ = "name"
    graph.merge(dynastyNode)

    authorNode = Node("作者", name=author)
    authorNode.__primarylabel__ = "作者"
    authorNode.__primarykey__ = "name"
    graph.merge(authorNode)

    title_author = Relationship(titleNode, "诗词作者", authorNode)
    graph.create(title_author)

    title_dynasty = Relationship(titleNode, "朝代", dynastyNode)
    graph.create(title_dynasty)

    if author != '佚名':
        author_dynasty = Relationship(authorNode, "作者朝代", dynastyNode)
        graph.merge(author_dynasty)
    else:
        pass

    authorIntroNode = Node("作者简介", name=authorIntro)
    authorIntroNode.__primarylabel__ = "作者简介"
    authorIntroNode.__primarykey__ = "name"
    if authorIntro != '无简介':
        graph.merge(authorIntroNode)
        author_authorIntro = Relationship(authorNode, "作者简介", authorIntroNode)
        graph.merge(author_authorIntro)
    else:
        pass

    bodyNode = Node("诗词内容", name=body)
    bodyNode.__primarylabel__ = "诗词内容"
    bodyNode.__primarykey__ = "name"
    graph.create(bodyNode)

    title_body = Relationship(titleNode, "诗词内容", bodyNode)
    graph.create(title_body)

    translationNode = Node("译文", name=translation)
    translationNode.__primarylabel__ = "译文"
    translationNode.__primarykey__ = "name"

    if translation != '无':
        graph.create(translationNode)
        body_translation = Relationship(bodyNode, "译文", translationNode)
        graph.create(body_translation)
    else:
        pass

    appreciationNode = Node("赏析", name=appreciation)
    appreciationNode.__primarylabel__ = "赏析"
    appreciationNode.__primarykey__ = "name"

    if appreciation != '无':
        graph.create(appreciationNode)
        body_appreciation = Relationship(bodyNode, "赏析", appreciationNode)
        graph.create(body_appreciation)
    else:
        pass

    backgroundNode = Node("创作背景", name=background)
    backgroundNode.__primarylabel__ = "创作背景"
    backgroundNode.__primarykey__ = "name"

    if background != '无':
        graph.create(backgroundNode)
        title_background = Relationship(titleNode, "创作背景", backgroundNode)
        graph.create(title_background)
    else:
        pass

    for tag in tagList:
        tagNode = Node("分类", name=tag)
        tagNode.__primarylabel__ = "分类"
        tagNode.__primarykey__ = "name"
        graph.merge(tagNode)
        title_tag = Relationship(titleNode, "诗词分类", tagNode)
        graph.create(title_tag)

    happyFacNode = Node("喜悦因子", name=happyFactor)
    happyFacNode.__primarylabel__ = "喜悦因子"
    happyFacNode.__primarykey__ = "name"
    if happyFactor != "0":
        graph.create(happyFacNode)
        body_happyFac = Relationship(bodyNode, "喜悦因子为", happyFacNode)
        graph.create(body_happyFac)
    else:
        pass

    angryFacNode = Node("愤怒因子", name=angryFactor)
    angryFacNode.__primarylabel__ = "愤怒因子"
    angryFacNode.__primarykey__ = "name"
    if angryFactor != "0":
        graph.create(angryFacNode)
        body_angryFac = Relationship(bodyNode, "愤怒因子为", angryFacNode)
        graph.create(body_angryFac)
    else:
        pass

    dislikeFacNode = Node("厌恶因子", name=dislikeFactor)
    dislikeFacNode.__primarylabel__ = "厌恶因子"
    dislikeFacNode.__primarykey__ = "name"
    if dislikeFactor != "0":
        graph.create(dislikeFacNode)
        body_dislikeFac = Relationship(bodyNode, "厌恶因子为", dislikeFacNode)
        graph.create(body_dislikeFac)
    else:
        pass

    sadFacNode = Node("悲伤因子", name=sadFactor)
    sadFacNode.__primarylabel__ = "悲伤因子"
    sadFacNode.__primarykey__ = "name"
    if sadFactor != "0":
        graph.create(sadFacNode)
        body_sadFac = Relationship(bodyNode, "悲伤因子为", sadFacNode)
        graph.create(body_sadFac)
    else:
        pass
    print("第" + str(i) + "行导入完成")

print("导入完成")
