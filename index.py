import time
import requests

url = "https://oc.yuekeyun.com/api/storeServer/storeTkOrderHeaderService/commitMovieTicketsOrder"
orderHeaderId = 1925096
payload = "params=%7B%22orderType%22%3A%22ticket_order%22%2C%22cinemaCode%22%3A%2243013211%22%2C%22cinemaLinkId%22%3A%2215936%22%2C%22sysSourceCode%22%3A%22YZ001%22%2C%22timestamp%22%3A" + str(int(time.time() * 1000))+"%2C%22ticket%22%3A%7B%22orderHeaderId%22%3A%22" + str(orderHeaderId) +"%22%2C%22activityId%22%3Anull%2C%22coupon%22%3A%5B%5D%2C%22totalPrice%22%3A31%7D%2C%22product%22%3Anull%2C%22mainPushCard%22%3Anull%2C%22cardId%22%3A%2220004132572X%22%2C%22ticketMobile%22%3A%2215577502294%22%2C%22inviteCode%22%3A%22%22%2C%22fulfillPlace%22%3A%22%E5%BD%B1%E9%99%A2%E6%9F%9C%E5%8F%B0%22%2C%22fulfillTime%22%3A%22%22%2C%22fulfillType%22%3A%22%22%2C%22channelCode%22%3A%22QD0000001%22%7D"
print(payload)
headers = {
  'Host': 'oc.yuekeyun.com',
  'content-type': 'application/x-www-form-urlencoded',
  'tenantCode': 'cinema_umedy',
  'Certificate': '25787994743237024f5aad0a0',
  'Accept-Encoding': 'gzip,compress,br,deflate',
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003634) NetType/WIFI Language/zh_CN',
  'Referer': 'https://servicewechat.com/wx285d5df3fd5c19e6/55/page-frame.html'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
