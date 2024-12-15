from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
import json
import time
import requests
from flask_cors import CORS

CORS(app)


Certificate = "25787994743237024f5aad0a0"

def serachCinemaName(name):
    # 打开并读取影院数据
    with open('./UME/cinema.json', 'r', encoding='utf-8') as file:
        cinema = json.load(file)  # 使用 json.load() 解析 JSON 文件
        cinema = cinema['data']
        for cityData in cinema:
            for item in cityData['cinemaList']:
                if (item['cinemaName'] == name):
                    return {"cinemaName": item["cinemaName"], "cinemaCode": item["cinemaCode"], "cinemaLinkId": item["cinemaLinkId"]}
        return None
    
def findFilmInfoToApp(cinemaData, filmName):
    url = "https://oc.yuekeyun.com/api/storeServer/cinCinemaFilmInfoService/findFilmInfoToApp"

    payload = 'params={"cinemaCode":"%s","channelCode":"QD0000001","sysSourceCode":"YZ001","cinemaLinkId":"%s"}' % (cinemaData["cinemaCode"], cinemaData["cinemaLinkId"])
    headers = {
    'Host': 'oc.yuekeyun.com',
    'content-type': 'application/x-www-form-urlencoded',
    'tenantCode': 'cinema_umedy',
    'Certificate': Certificate,
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003632) NetType/WIFI Language/zh_CN'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    # print(data["data"][1])
    for item in data["data"][1]['fimlList']:
        print(item['filmName'], filmName)
        if (filmName == item['filmName']):
            return {"filmName": item["filmName"], "filmUniqueId": item["filmUniqueId"], "showDate": item["showDate"]}
    return None

def findScheduleInfoToApp(cinemaData, FilmData, date, Time):
    url = "https://oc.yuekeyun.com/api/storeServer/cinScheduleInfoService/findScheduleInfoToApp"

    payload = 'params={"cinemaCode":"%s","filmUniqueId":"%s","showDate":"%s","channelCode":"QD0000001","sysSourceCode":"YZ001","cinemaLinkId":"%s"}' % (cinemaData["cinemaCode"], FilmData['filmUniqueId'], date, cinemaData["cinemaLinkId"])
    headers = {
    'Host': 'oc.yuekeyun.com',
    'content-type': 'application/x-www-form-urlencoded',
    'tenantCode': 'cinema_umedy',
    'Certificate': Certificate,
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003632) NetType/WIFI Language/zh_CN'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    for item in data["data"]:
        print(date + " " + Time + ":00", item['showDateTime'])
        if (date + " " + Time + ":00" == item['showDateTime']):
            return item
    return None

def findSeatMapInfo(cinemaData, FilmData, ScheduleData, CoordList):
    returnList = []
    url = "https://oc.yuekeyun.com/api/storeServer/cinSyncService/findSeatMapInfo"

    payload = 'params={"cinemaCode":"%s","cinemaLinkId":"%s","scheduleId":"%s","scheduleKey":"%s","channelCode":"QD0000001","sysSourceCode":"YZ001"}' % (cinemaData["cinemaCode"], cinemaData["cinemaLinkId"], ScheduleData['scheduleId'], ScheduleData['scheduleKey'])
    
    headers = {
    'Host': 'oc.yuekeyun.com',
    'content-type': 'application/x-www-form-urlencoded',
    'tenantCode': 'cinema_umedy',
    'Certificate': Certificate,
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003632) NetType/WIFI Language/zh_CN'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    if (CoordList and len(CoordList) > 0):
        for Coord in CoordList:
            for item in data["data"]["seatList"]:
                if (item['rowId'] == Coord['row'] and item['columnId'] == Coord['col']):
                    returnList.append(item)
        return returnList
    else:
        return data["data"]["seatList"]

def createMovieTicketsOrder(cinemaData, FilmData, ScheduleData, SeatDataList, showDate):
    seatInfoList = []
    for SeatData in SeatDataList:
        seatInfoList.append({"seatCode": SeatData['seatCode'],"buyerRemark":""})
    url = "https://oc.yuekeyun.com/api/storeServer/storeTkOrderHeaderService/createMovieTicketsOrder"

    payload = 'params={"orderType":"ticket_order","scheduleId":"%s","scheduleKey":"%s","filmUniqueId":"%s","showDate":"%s","ticketDetail":%s,"showDateTime":"%s","channelCode":"QD0000001","sysSourceCode":"YZ001","cinemaCode":"%s","cinemaLinkId":"%s"}' % (ScheduleData['scheduleId'], ScheduleData['scheduleKey'], FilmData['filmUniqueId'], showDate, json.dumps(seatInfoList), ScheduleData['showDateTime'], cinemaData["cinemaCode"], cinemaData["cinemaLinkId"])
    print(payload)
    headers = {
    'Host': 'oc.yuekeyun.com',
    'content-type': 'application/x-www-form-urlencoded',
    'tenantCode': 'cinema_umedy',
    'Certificate': Certificate,
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003632) NetType/WIFI Language/zh_CN'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # {"msg":"锁座成功！","data":{"orderPriceInfo":{"scheduleInfo":{"filmCode":"001105972024","marketPrice":"9000","dimensional":"2D","hallType":"N","dimensionCode":"1","language":"国语","scheduleSpecialProperties":"","showDate":"2024-12-16","sysSourceCode":"YZ001","cinemaLinkId":"15936","duration":"105","firstShowFlag":"N","hallCode":"0000000000000002","localFilmVersion":"2D","modifyPriceFlag":"Y","cinemaName":"UME影城（长沙砂之船店）","stopSellingTime":"2024-12-16 21:00:00","starsShowFlag":"N","scheduleId":"1000000837845609","ticketLowestPrice":"3000","areaSettlePriceMin":"5000","ticketStandardPrice":"9000","saleStatus":"Y","showDateTime":"2024-12-16 21:00:00","scheduleInfoId":1443654,"filmUniqueId":"001105972024","scheduleKey":"9B8B037ADA6F73B59E45DCA55F7B727F","cinemaCode":"43013211","filmName":"孤星计划","hallName":"2号厅 王源孤星计划","detailsDescription":"","ticketMemberPrice":"3000"},"seatInfoList":[{"yCoord":"6","columnId":"1","rowName":"6","type":"N","rowId":"6","areaId":"7474","xCoord":"6","areaName":"优选区","seatCode":"000000045774-6-6","damaged":"N","areaSettlePrice":5000,"areaMemberPrice":[{"areaPrice":0,"relationCardPlan":"10001256","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000},{"areaPrice":0,"relationCardPlan":"10001508","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000},{"areaPrice":0,"relationCardPlan":"10002884","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000},{"areaPrice":0,"relationCardPlan":"10003576","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000},{"areaPrice":0,"relationCardPlan":"10004020","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000}],"seatStandardCode":"00000000000457740601","columnName":"1","status":"1"},{"yCoord":"6","columnId":"2","rowName":"6","type":"N","rowId":"6","areaId":"7474","xCoord":"7","areaName":"优选区","seatCode":"000000045774-6-7","damaged":"N","areaSettlePrice":5000,"areaMemberPrice":[{"areaPrice":0,"relationCardPlan":"10001256","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000},{"areaPrice":0,"relationCardPlan":"10001508","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000},{"areaPrice":0,"relationCardPlan":"10002884","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000},{"areaPrice":0,"relationCardPlan":"10003576","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000},{"areaPrice":0,"relationCardPlan":"10004020","price":3000,"cardType":"GOLDEN_CARD","settlePrice":3000}],"seatStandardCode":"00000000000457740602","columnName":"2","status":"1"}]},"orderInfo":{"cinemaCode":"43013211","cinemaLinkId":"15936","cinemaName":"UME影城（长沙砂之船店）","createdBy":407327,"creationDate":"2024-12-13 21:23:16","deleteFlag":0,"duration":"105","filmCode":"001105972024","filmName":"孤星计划","filmUniqueId":"001105972024","filmVersion":"2D","hallCode":"0000000000000002","hallName":"2号厅 王源孤星计划","lastUpdateDate":"2024-12-13 21:23:16","lastUpdateLogin":407327,"lastUpdatedBy":407327,"lockOrderId":"2691015936213885107","memberCode":"HY000407805","memberId":407327,"memberMobile":"15577502294","memberName":"微信用户","movieLanguage":"国语","operatorUserId":407327,"orderCode":"LD24121300322100072","orderHeaderId":1913587,"orderStatus":"loke_success","orderType":"ticket_order","payStatus":"non-payment","scheduleId":"1000000837845609","scheduleKey":"9B8B037ADA6F73B59E45DCA55F7B727F","screeningCode":"1000000837845609","seatInfo":"6排-1座,6排-2座","showDate":"2024-12-16","showDateTime":"2024-12-16 21:00:00","sourceChannel":"QD0000001","sysSourceCode":"YZ001","versionNum":0,"yzAccountId":"1003694002335709"}},"count":1,"status":"S"}
    return json.loads(response.text)

# 获取活动信息
def getOptimalCombination(cinemaData, FilmData, ScheduleData, SeatDataList, orderInfo):
    url = "https://oc.yuekeyun.com/api/storeServer/optimalCombinatService/getOptimalCombination"
    seatInfoList = []
    for SeatData in SeatDataList:
        seatInfoList.append({"seatCode": SeatData['seatCode'],"buyerRemark":""})
    payload = 'params={"orderCode":"%s","cinemaCode":"%s","cinemaLinkId":"%s","sysSourceCode":"YZ001","orderHeaderId":%s,"timestamp":%s,"productInfo":null,"orderType":"ticket_order","scheduleId":"%s","scheduleKey":"%s","filmUniqueId":"%s","showDate":"%s","ticketDetail":%s,"showDateTime":"%s","channelCode":"QD0000001","lockFlag":"2691015936213885117"}' % (orderInfo["orderCode"], cinemaData["cinemaCode"], cinemaData["cinemaLinkId"], orderInfo["orderHeaderId"], int(time.time() * 1000), orderInfo["scheduleId"], orderInfo["scheduleKey"], orderInfo["scheduleKey"], orderInfo["showDate"], json.dumps(seatInfoList), orderInfo["showDateTime"])
    # print(payload)
    headers = {
    'Host': 'oc.yuekeyun.com',
    'content-type': 'application/x-www-form-urlencoded',
    'tenantCode': 'cinema_umedy',
    'Certificate': Certificate,
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003632) NetType/WIFI Language/zh_CN'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    # {"msg":"操作成功","data":{"mainPushCard":{},"ticketOptimalComb":{"cards":[{"actionExpression":"","cardAmount":"10000","cardInstanceId":1807576,"cardNo":"20004132572X","cardRuleId":"10001256","cardRuleName":"UME尊享卡","cardStatus":"ENABLED","cardStatusName":"正常","cardType":"DEPOSIT","cardTypeName":"储值卡","cashReplenish":"Y","cinemaCode":"43013211","cinemaName":"UME影城（长沙砂之船店）","companyId":1,"discountAmount":2000,"expireDate":"2026-12-12","fontColor":"#ffffff","memberId":407327,"orderNum":"KS000004","originalAmount":5500,"resultAmount":3500,"seatResltCardJson":{"seatResltAmountCardJson":{"000000045776-7-3":3500},"seatResltDiscountAmountCardJson":{"000000045776-7-3":2000.00}},"sellAfterPicture":"https://static.oc.yuekeyun.com/cinema_umedy/img/225358e3c7104b138f9bcabfd86c9ba5.png"}],"coupons":[],"activities":[]}},"count":1,"status":"S"}
    return json.loads(response.text)

def commitMovieTicketsOrder(cinemaData, FilmData, ScheduleData, SeatDataList, orderInfo, combinationData):
    url = "https://oc.yuekeyun.com/api/storeServer/storeTkOrderHeaderService/commitMovieTicketsOrder"
    seatInfoList = []
    for SeatData in SeatDataList:
        seatInfoList.append({"seatCode": SeatData['seatCode'],"buyerRemark":""})
    payload = 'params={"orderType":"ticket_order","cinemaCode":"%s","cinemaLinkId":"%s","sysSourceCode":"YZ001","timestamp":%s,"ticket":{"orderHeaderId":"%s","activityId":null,"coupon":[],"totalPrice":31},"product":null,"mainPushCard":null,"cardId":"%s","ticketMobile":"15577502294","inviteCode":"","fulfillPlace":"影院柜台","fulfillTime":"","fulfillType":"","channelCode":"QD0000001"}' % (cinemaData["cinemaCode"], cinemaData["cinemaLinkId"], int(time.time() * 1000), orderInfo["orderHeaderId"], combinationData["data"]["ticketOptimalComb"]["cards"][0]['cardNo'])
    print('------------------------')
    print(payload)
    print('------------------------')
    headers = {
    'Host': 'oc.yuekeyun.com',
    'content-type': 'application/x-www-form-urlencoded',
    'tenantCode': 'cinema_umedy',
    'Certificate': Certificate,
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003632) NetType/WIFI Language/zh_CN'
    }
    # {"msg":"获取成功！","data":{"filmCode":"001105972024","orderType":"ticket_order","lastUpdateDate":"2024-12-13 22:24:36","versionNum":0,"lastUpdateLogin":407327,"showDate":"2024-12-17","deleteFlag":0,"ticketAmount":30,"screeningCode":"1000000837446229","discounts":"member_card","subsidiesAmount":0,"cinemaName":"UME影城（长沙砂之船店）","scheduleId":"1000000837446229","filmVersion":"2D","memberId":407327,"memberCode":"HY000407805","lastUpdatedBy":407327,"yzAccountId":"1003694002335709","showDateTime":"2024-12-17 19:00:00","creationDate":"2024-12-13 22:20:58","movieLanguage":"国语","scheduleKey":"B154070D354B6C9561CCD4449CB26B38","filmName":"孤星计划","payOrderCode":"LP241213001985","memberMobile":"15577502294","preferentialAmount":20.00,"sourceChannel":"QD0000001","preferentialVirtualAmt":0,"memberName":"微信用户","orderStatus":"paying","paymentAmount":31.00,"sysSourceCode":"YZ001","cinemaLinkId":"15936","duration":"105","hallCode":"0000000000000002","orderTotalAmount":51.00,"seatInfo":"6排-1座","timestamp":"1734099671827","orderHeaderId":1913704,"ticketMobile":"15577502294","receivableVirtualAmt":0,"paymentList":[{"memberCardList":[{"cardAmount":10000,"cardInstanceId":1807576,"cardNo":"20004132572X","cardRuleName":"UME尊享卡","cardStatus":"ENABLED","cardStatusName":"正常","cardType":"DEPOSIT","cardTypeName":"储值卡","cinemaCode":"43013211"}],"paymentMethodCode":"Z0006","paymentMethodName":"会员卡","paymentWayId":2,"sequence":2}],"operatorUserId":407327,"filmUniqueId":"001105972024","lockOrderId":"2691015936213879933","createdBy":407327,"cinemaCode":"43013211","orgPaymentAmount":51.00,"orderCode":"LD24121300343800072","hallName":"2号厅 王源孤星计划","payStatus":"non-payment"},"count":1,"status":"S"}
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)

def saveMemberOrderPayAmount(cinemaData, FilmData, ScheduleData, SeatDataList, orderInfo, combinationData):
    url = "https://oc.yuekeyun.com/api/storeServer/storeTkOrderHeaderService/saveMemberOrderPayAmount"
    payload = 'params={"paymentWay":"Z0006","orderHeaderId":"%s","cardNo":"%s","isMultiplePay":"","channelCode":"QD0000001","sysSourceCode":"YZ001","cinemaCode":"%s","cinemaLinkId":"%s"}' % (orderInfo["orderHeaderId"], combinationData["data"]["ticketOptimalComb"]["cards"][0]['cardNo'], cinemaData["cinemaCode"], cinemaData["cinemaLinkId"])
    headers = {
    'Host': 'oc.yuekeyun.com',
    'content-type': 'application/x-www-form-urlencoded',
    'tenantCode': 'cinema_umedy',
    'Certificate': Certificate,
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003632) NetType/WIFI Language/zh_CN'
    }
    # {"msg":"获取成功！","data":{"filmCode":"001105972024","orderType":"ticket_order","lastUpdateDate":"2024-12-13 22:24:36","versionNum":0,"lastUpdateLogin":407327,"showDate":"2024-12-17","deleteFlag":0,"ticketAmount":30,"screeningCode":"1000000837446229","discounts":"member_card","subsidiesAmount":0,"cinemaName":"UME影城（长沙砂之船店）","scheduleId":"1000000837446229","filmVersion":"2D","memberId":407327,"memberCode":"HY000407805","lastUpdatedBy":407327,"yzAccountId":"1003694002335709","showDateTime":"2024-12-17 19:00:00","creationDate":"2024-12-13 22:20:58","movieLanguage":"国语","scheduleKey":"B154070D354B6C9561CCD4449CB26B38","filmName":"孤星计划","payOrderCode":"LP241213001985","memberMobile":"15577502294","preferentialAmount":20.00,"sourceChannel":"QD0000001","preferentialVirtualAmt":0,"memberName":"微信用户","orderStatus":"paying","paymentAmount":31.00,"sysSourceCode":"YZ001","cinemaLinkId":"15936","duration":"105","hallCode":"0000000000000002","orderTotalAmount":51.00,"seatInfo":"6排-1座","timestamp":"1734099671827","orderHeaderId":1913704,"ticketMobile":"15577502294","receivableVirtualAmt":0,"paymentList":[{"memberCardList":[{"cardAmount":10000,"cardInstanceId":1807576,"cardNo":"20004132572X","cardRuleName":"UME尊享卡","cardStatus":"ENABLED","cardStatusName":"正常","cardType":"DEPOSIT","cardTypeName":"储值卡","cinemaCode":"43013211"}],"paymentMethodCode":"Z0006","paymentMethodName":"会员卡","paymentWayId":2,"sequence":2}],"operatorUserId":407327,"filmUniqueId":"001105972024","lockOrderId":"2691015936213879933","createdBy":407327,"cinemaCode":"43013211","orgPaymentAmount":51.00,"orderCode":"LD24121300343800072","hallName":"2号厅 王源孤星计划","payStatus":"non-payment"},"count":1,"status":"S"}
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


def saveMemberTriggerPassiveLabel(cinemaData, FilmData, ScheduleData, SeatDataList, orderInfo, combinationData):
    url = "https://oc.yuekeyun.com/api/storeServer/cuxLabelsMemService/saveMemberTriggerPassiveLabel"
    payload = 'params={"eventTracking":"1","keepLoading":true,"channelCode":"QD0000001","sysSourceCode":"YZ001","cinemaCode":"%s","cinemaLinkId":"%s"}' % (cinemaData["cinemaCode"], cinemaData["cinemaLinkId"])
    headers = {
    'Host': 'oc.yuekeyun.com',
    'content-type': 'application/x-www-form-urlencoded',
    'tenantCode': 'cinema_umedy',
    'Certificate': Certificate,
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x18003632) NetType/WIFI Language/zh_CN'
    }
    # {"msg":"操作成功","count":0,"status":"S"}
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


@app.route("/")
def index():
    return 'ok'


@app.route("/order", methods=['POST'])
def check():
    body = json.loads(request.get_data())
    # 查找影院名称
    print(body)
    CinemaData = serachCinemaName(body["cinemaName"])
    if (CinemaData != None):
        print(CinemaData)
        FilmData = findFilmInfoToApp(CinemaData, body["filmName"])
        if (FilmData != None):
            ScheduleData = findScheduleInfoToApp(CinemaData, FilmData, body["showDate"], body["showTime"])
            if (ScheduleData != None):
                SeatDataList = findSeatMapInfo(CinemaData, FilmData, ScheduleData, body["seats"])
                if (len(SeatDataList) > 0):
                    orderData = createMovieTicketsOrder(CinemaData, FilmData, ScheduleData, SeatDataList, body["showDate"])
                    print("订单详情:")
                    print(orderData)
                    if (orderData['status'] == 'E'):
                        return json.dumps({"err": 1, "data":orderData})

                    orderInfo = orderData["data"]['orderInfo']
                    # 优惠券信息
                    combinationData = getOptimalCombination(CinemaData, FilmData, ScheduleData, SeatDataList, orderInfo)
                    print('优惠券信息:')
                    print(combinationData)
                    # # 保存下单
                    # saveMemberTriggerPassiveLabel(CinemaData, FilmData, ScheduleData, SeatDataList, orderInfo, combinationData)
                    # 正式下单
                    ticketsOrderData = commitMovieTicketsOrder(CinemaData, FilmData, ScheduleData, SeatDataList, orderInfo, combinationData)
                    print('正式下单详情:')
                    print(ticketsOrderData)
                    return saveMemberOrderPayAmount(CinemaData, FilmData, ScheduleData, SeatDataList, orderInfo, combinationData)
                else:
                    print("座位信息不存在!")
                    return json.dumps({"err": 1, "msg":"座位信息不存在!"})
            else:
                print("时间信息不存在!")
                return json.dumps({"err": 1, "msg":"时间信息不存在!"})
        else:
            print("电影信息不存在!")
            return json.dumps({"err": 1, "msg":"电影信息不存在!"})
    else:
        print("影院信息不存在!")
        return json.dumps({"err": 1, "msg":"影院信息不存在!"})

@app.route("/seatMapInfo", methods=['POST'])
def seatMapInfo():
    body = json.loads(request.get_data())
    # 查找影院名称
    print(body)
    CinemaData = serachCinemaName(body["cinemaName"])
    if (CinemaData != None):
        print(CinemaData)
        FilmData = findFilmInfoToApp(CinemaData, body["filmName"])
        if (FilmData != None):
            ScheduleData = findScheduleInfoToApp(CinemaData, FilmData, body["showDate"], body["showTime"])
            if (ScheduleData != None):
                return findSeatMapInfo(CinemaData, FilmData, ScheduleData, [])
            else:
                print("时间信息不存在!")
                return json.dumps({"err": 1, "msg":"时间信息不存在!"})
        else:
            print("电影信息不存在!")
            return json.dumps({"err": 1, "msg":"电影信息不存在!"})
    else:
        print("影院信息不存在!")
        return json.dumps({"err": 1, "msg":"影院信息不存在!"})

if __name__ == '__main__':
    app.run(debug=True, port=8084)