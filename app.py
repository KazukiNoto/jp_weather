from flask import Flask, jsonify,request
from flasgger import Swagger
from api import weather
import json
# import requests

app = Flask(__name__)
swagger = Swagger(app)

# http://127.0.0.1:5000をルートとして、("")の中でアクセスポイント指定
# @app.route("hoge")などで指定すると、http://127.0.0.1:5000/hogeでの動作を記述できる。
@app.route("/")
def hello():
    # ここがSwaggerの仕様を書いている所
    """デフォルトのサーバ動作確認用
    ---
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: 動作している
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    return jsonify({"return":"OK"})

@app.route("/area_weather",methods=["POST"])
def areaWeather():
    # ここがSwaggerの仕様を書いている所
    """地域別の天気予報取得
    ---
    parameters:
      - name: area
        in: path
        type: string
        enum: ["319", '320', '321']
        required: true
        default: 319
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    try:
        print(request.json)
        # print(request.form[])
        # createdata = datacreate.ret(request.json)
        return jsonify({"return":"OK"})
    except Exception as e:
        return str(e)


# 週間天気情報を気象庁から取得するAPI
# POST,Bodyは無しでOK
# /weatherdataに取得したデータが格納される
@app.route("/weather", methods=["POST"])
def getWeatherReport():
    try:
        region = 301
        while region < 357:
            weather.gwr(str(region))
            region = region + 1
        return "compleate"
    except Exception as e:
        return str(e)

# /getWeather
# 受け取ったregionの天気情報を返す。
# body: json
# {
#   "region":"319"
# }
#
# response: str
# [{"date": "03/28","weather": "曇り後雨","rain": "011","maxtemp": "19","mintemp": "11"},...}]
@app.route("/getWeather", methods=["POST"])
def gweather():
    try:
        print(request.json)
        region = request.json["region"]
        filePath = 'weatherdata/' + region + '.json'
        with open(filePath) as f:
            weatherlist = json.load(f)
        return json.dumps(weatherlist, ensure_ascii=False)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    # webサーバー立ち上げ
    app.run()