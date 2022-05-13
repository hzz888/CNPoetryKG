import requests
import json
import xlrd
import xlwt


def getInfo(url, headers):
    res = requests.get(url, headers=headers)
    return res.json()


class ownThink:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def getForm(self):
        jsonData = getInfo(self.url, self.headers)
        if jsonData['message'] == 'success':
            return jsonData['data']
