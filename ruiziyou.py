import time
import requests
import json

def ruiziyou(CinemaData, body):

    url = "https://gzxe.ruiziyou.com/wx/appLet/GetSchedul"

    payload = {}
    headers = {
    'Host': 'gzxe.ruiziyou.com',
    'rid': '4623',
    'appid': 'wx7add15304f004bcb',
    'signature': '8dda5a0c7918ce6dc7078e43df8a7532',
    'content-type': 'application/json',
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'time': str(int(time.time())),
    'openid': 'oc0Cg6-eTYvMEDZu3mERlfO8sgNI',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003635) NetType/WIFI Language/zh_CN'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text
