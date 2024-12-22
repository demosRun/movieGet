from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
import json
import time
import requests
from ume import ume, umeSeatMapInfo, umeGetOrder
from ruiziyou import ruiziyou
from flask_cors import CORS

CORS(app)




def serachCinemaName(name):
    # 打开并读取影院数据
    with open('./UME/cinema.json', 'r', encoding='utf-8') as file:
        cinema = json.load(file)  # 使用 json.load() 解析 JSON 文件
        cinema = cinema['data']
        for cityData in cinema:
            for item in cityData['cinemaList']:
                if (item['cinemaName'] == name):
                    print(item)
                    return {"cinemaName": item["cinemaName"], "cinemaCode": item["cinemaCode"], "cinemaLinkId": item["cinemaLinkId"], "type": "ume"}
    with open('./UME/ruiziyou.json', 'r', encoding='utf-8') as file:
        cinema = json.load(file)
        cinema = cinema['data']
        for cityData in cinema:
            for item in cityData['list']:
                if (item['name'] == name):
                    print(item)
                    return {"cinemaName": item["name"], "cinemaCode": item["mcode"], "type": "ruiziyou"}
    return None
    



@app.route("/")
def index():
    return 'ok'


@app.route("/order", methods=['POST'])
def check():
    body = json.loads(request.get_data())
    print(body)
    # 查找影院名称
    CinemaData = serachCinemaName(body["cinemaName"])
    if (CinemaData != None):
        if (CinemaData['type'] == 'ume'):
            return ume(CinemaData, body)
        if (CinemaData['type'] == 'ruiziyou'):
            return ruiziyou(CinemaData, body)
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
        return umeSeatMapInfo(CinemaData, body)
    else:
        print("影院信息不存在!")
        return json.dumps({"err": 1, "msg":"影院信息不存在!"})

@app.route("/getOrder", methods=['POST'])
def getOrder():
    body = json.loads(request.get_data())
    if (body["type"] == "UME"):
        return umeGetOrder(body)
    return {"err": 1, "msg": "类型不存在"}

if __name__ == '__main__':
    app.run(debug=True, port=8100)