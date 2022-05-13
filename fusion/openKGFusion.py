import time
import requests
import json
import xlrd
import xlwt

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}


def getInfo(url):
    res = requests.get(url, headers=headers)
    return json.loads(res.text)


class generalKG:
    def __init__(self, url):
        self.headers = headers
        self.url = url


class ownThink(generalKG):
    def __init__(self):
        super().__init__('https://api.ownthink.com/kg/eav?entity=')

    def getForm(self, entityname):
        url = self.url + entityname + '&attribute=文学体裁'
        # time.sleep(1)
        formData = getInfo(url)
        if formData['message'] == 'success':
            if len(formData['data']) != 0:
                return str(formData['data']['value'][0])
            else:
                return '无此属性'
        else:
            return '该图谱中无此数据'

    def getOrigin(self, entityname):
        url = self.url + entityname + '&attribute=作品出处'
        time.sleep(1)
        oriData = getInfo(url)
        if oriData['message'] == 'success':
            if len(oriData['data']) != 0:
                return str(oriData['data']['value'][0])
            else:
                return '无此属性'
        else:
            return '该图谱中无此数据'


if __name__ == '__main__':

    otkg = ownThink()
    formList = []
    originList = []

    dataFile = xlrd.open_workbook('../data/final.xls', formatting_info=True)
    sheet = dataFile.sheet_by_index(0)
    newFile = xlwt.Workbook()
    newSheet = newFile.add_sheet('sheet1')

    for i in range(1, sheet.nrows):
        row = sheet.row_values(i)
        poemName = str(row[0])
        form = otkg.getForm(entityname=poemName)
        origin = otkg.getOrigin(entityname=poemName)
        print(poemName, form, origin)
        formList.append(form)
        originList.append(origin)

    newSheet.write(0, 0, '文学体裁')
    newSheet.write(0, 1, '作品出处')

    i, j = 1, 1
    for formItem in formList:
        newSheet.write(i, 0, formItem)
        i += 1
    for originItem in originList:
        newSheet.write(j, 1, originItem)
        j += 1

    newFile.save('../data/ownthink.xls')
