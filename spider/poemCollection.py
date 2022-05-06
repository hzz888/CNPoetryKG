import requests
from lxml import etree
import xlwt


poemList = []

counter = 0

url = "https://www.xungushici.com/shiji/8"
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
response = requests.get(url=url, headers=headers)
html = response.content.decode('utf-8')
firstTree = etree.HTML(html)
li = firstTree.xpath('//a[@target="_blank"]')[0:-6]

for entity in li:
    poem = {}

    poemLink = entity.xpath('./@href')[0]
    fullLink = "https://www.xungushici.com" + poemLink

    secondResponse = requests.get(url=fullLink, headers=headers)
    secondHtml = secondResponse.content.decode('utf-8')
    secondTree = etree.HTML(secondHtml)

    tags = secondTree.xpath('//a[@class="badge badge-secondary"]/text()')
    if not tags:
        continue
    else:
        tagStr = ",".join(tags)

    title = secondTree.xpath('//h3[@class="card-title"]/text()')[0]

    dynasty = secondTree.xpath('/html/body/div/div/div[1]/div[1]/div/p/a[1]/text()')[0]

    if (
            len(secondTree.xpath('/html/body/div[1]/div/div[1]/div[1]/div/p/span/text()')) == 0):

        author = secondTree.xpath(
            '/html/body/div[1]/div/div[1]/div[1]/div/p/a[2]/text()'
        )[0]

    else:
        author = secondTree.xpath(
            '/html/body/div[1]/div/div[1]/div[1]/div/p/span/text()'
        )[0]

    if len(secondTree.xpath('//div[@class="card-body"]/p[@class="mb-0"]/text()')) != 0:
        authorIntro = secondTree.xpath('//div[@class="card-body"]/p[@class="mb-0"]/text()')[0]

    elif len(secondTree.xpath('//div[@class="card-body d-flex"]/p/text()')) != 0:
        authorIntro = secondTree.xpath('//div[@class="card-body d-flex"]/p/text()')[0]

    else:
        authorIntro = "无简介"

    poemBody = ""
    if (
            len(
                secondTree.xpath(
                    '/html/body/div[1]/div/div[1]/div[1]/div/div[1]/p/text()'
                )
            )
            == 0
    ):
        artical = secondTree.xpath(
            '/html/body/div[1]/div/div[1]/div[1]/div/div[1]/text()'
        )
        for artiEntity in artical:
            poemBody += artiEntity.replace("\r", "").replace("\t", "").replace("\n", "")  # 去除特殊符号
    else:
        artical = secondTree.xpath(
            '/html/body/div[1]/div/div[1]/div[1]/div/div[1]/p/text()'
        )
        for artiEntity in artical:
            poemBody += (artiEntity.replace("\r", "").replace("\t", "").replace("\n", ""))

    # !获取译文
    trans = ""
    path = '/html/body/div[1]/div/div[1]/div[2]/div[2]/p/text()'
    if not secondTree.xpath(path):
        trans = "无"
    else:
        translist = secondTree.xpath(path)
        for tranEntity in translist:
            trans += (tranEntity + "\n")

    # 获取鉴赏
    appre = ""
    path = '/html/body/div[1]/div/div[1]/div[3]/div[2]/p/text()'
    if not secondTree.xpath(path):
        appre = "无"
    else:
        apprelist = secondTree.xpath(path)
        for appreEntity in apprelist:
            appre += (appreEntity + "\n")

    # 获取创作背景
    background = secondTree.xpath(
        '/html/body/div[1]/div/div[1]/div[4]/div[2]/p/text()'
    )
    bg = ""
    if background:
        for bgEntity in background:
            bg += (bgEntity + "\n")
    else:
        bg = "无"

    poem['title'] = title
    poem['dynasty'] = dynasty
    poem['author'] = author
    poem['authorIntro'] = authorIntro
    poem['body'] = poemBody
    poem['translation'] = trans
    poem['appreciation'] = appre
    poem['background'] = bg
    poem['tags'] = tagStr

    poemList.append(poem)

    counter += 1
    print("第" + str(counter) + "首")

poemData = xlwt.Workbook()
# 调用对象的add_sheet方法
poemSheet = poemData.add_sheet('poemSheet', cell_overwrite_ok=True)
# 创建表头
poemSheet.write(0, 0, "title")
poemSheet.write(0, 1, 'dynasty')
poemSheet.write(0, 2, 'author')
poemSheet.write(0, 3, 'authorIntro')
poemSheet.write(0, 4, 'body')
poemSheet.write(0, 5, 'translation')
poemSheet.write(0, 6, 'appreciation')
poemSheet.write(0, 7, 'background')
poemSheet.write(0, 8, 'tags')

for i in range(0, len(poemList)):
    poemSheet.write(i + 1, 0, poemList[i]['title'])
    poemSheet.write(i + 1, 1, poemList[i]['dynasty'])
    poemSheet.write(i + 1, 2, poemList[i]['author'])
    poemSheet.write(i + 1, 3, poemList[i]['authorIntro'])
    poemSheet.write(i + 1, 4, poemList[i]['body'])
    poemSheet.write(i + 1, 5, poemList[i]['translation'])
    poemSheet.write(i + 1, 6, poemList[i]['appreciation'])
    poemSheet.write(i + 1, 7, poemList[i]['background'])
    poemSheet.write(i + 1, 8, poemList[i]['tags'])

poemData.save("../data/19shou.xls")

print("已爬取完成" + str(counter) + "首诗词")
