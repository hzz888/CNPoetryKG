import requests
from lxml import etree
import xlwt
import random
from bs4 import BeautifulSoup

UAList = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50",
    "Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50",
    "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;",
    "Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)",
    "Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)",
    "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
    "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
    "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
    "Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11",
    "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
    "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11"
]

poemList = []

counter = 0

# waitTime = random.randint(0, 3)

for i in range(1, 63544):

    ua = random.choice(UAList)
    headers = {
        'user-agent': ua
    }

    url = 'https://www.xungushici.com/shicis/p-' + str(i)

    response = requests.get(url=url, headers=headers)
    listContent = response.content.decode('utf-8')

    soup = BeautifulSoup(listContent, 'html.parser')

    wrapper = soup.find('div', class_='col col-sm-12 col-lg-9')
    li = wrapper.find_all('div', class_="card mt-3")
    print('第' + str(i) + '页')

    for entity in li:

        # 每首诗词是一个字典
        poem = {}

        # 获取一页所有诗
        href = entity.find('h4', class_='card-title').a['href']
        whole_href = 'https://www.xungushici.com' + href

        tagSection = entity.find_all('a', class_='badge badge-secondary')

        if not tagSection:
            continue
        else:
            # 爬取诗词详细页
            getPoem = requests.get(url=whole_href, headers=headers).text
            tree = etree.HTML(getPoem)

            # title
            poemTitle = tree.xpath('//h3[@class="card-title"]/text()')[0]

            # dynasty
            poemDynasty = tree.xpath('/html/body/div[1]/div/div[1]/div[1]/div/p/a/text()')[0]

            # author name in p or a
            if (
                    len(tree.xpath('/html/body/div[1]/div/div[1]/div[1]/div/p/span/text()')) == 0):

                author = tree.xpath(
                    '/html/body/div[1]/div/div[1]/div[1]/div/p/a[2]/text()'
                )[0]

            else:
                author = tree.xpath(
                    '/html/body/div[1]/div/div[1]/div[1]/div/p/span/text()'
                )[0]

            # author introduction
            if len(tree.xpath('//div[@class="card-body"]/p[@class="mb-0"]/text()')) != 0:
                authorIntro = tree.xpath('//div[@class="card-body"]/p[@class="mb-0"]/text()')[0]

            elif len(tree.xpath('//div[@class="card-body d-flex"]/p/text()')) != 0:
                authorIntro = tree.xpath('//div[@class="card-body d-flex"]/p/text()')[0]

            else:
                authorIntro = "无简介"

            # poem  wrapped by p or divided by br
            poemBody = ""

            if (
                    len(
                        tree.xpath(
                            '/html/body/div[1]/div/div[1]/div[1]/div/div[1]/p/text()'
                        )
                    )
                    == 0
            ):
                artical = tree.xpath(
                    '/html/body/div[1]/div/div[1]/div[1]/div/div[1]/text()'
                )
                for artiEntity in artical:
                    poemBody += artiEntity.replace("\r", "").replace("\t", "").replace("\n", "")  # 去除特殊符号
            else:
                artical = tree.xpath(
                    '/html/body/div[1]/div/div[1]/div[1]/div/div[1]/p/text()'
                )
                for artiEntity in artical:
                    poemBody += (artiEntity.replace("\r", "").replace("\t", "").replace("\n", ""))

            # translations
            trans = ""
            path = '/html/body/div[1]/div/div[1]/div[2]/div[2]/p/text()'
            if not tree.xpath(path):
                trans = "无"
            else:
                translist = tree.xpath(path)
                for tranEntity in translist:
                    trans += (tranEntity + "\n")

            # appreciations
            appre = ""
            path = '/html/body/div[1]/div/div[1]/div[3]/div[2]/p/text()'
            if not tree.xpath(path):
                appre = "无"
            else:
                apprelist = tree.xpath(path)
                for appreEntity in apprelist:
                    appre += (appreEntity + "\n")

            # backgrounds
            background = tree.xpath(
                '/html/body/div[1]/div/div[1]/div[4]/div[2]/p/text()'
            )
            bg = ""
            if background:
                for bgEntity in background:
                    bg += (bgEntity + "\n")
            else:
                bg = "无"

            # tags
            tags = tree.xpath(
                '//a[contains(@class,"badge") and contains(@class,"badge-secondary")]/text()'
            )
            tagStr = ",".join(tags)

            # build dictionary
            poem['title'] = poemTitle
            poem['dynasty'] = poemDynasty
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
            # time.sleep(waitTime)

poemData = xlwt.Workbook()
poemSheet = poemData.add_sheet('poemSheet', cell_overwrite_ok=True)
# create sheet title
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

poemData.save("../data/poem.xls")

print("已爬取完成" + str(counter) + "首诗词")
