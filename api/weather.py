# 初期
import logging
# 追加
import requests
from bs4 import BeautifulSoup
import datetime
import calendar
from api import weathertoJson

def gwr(region_code):
    logging.info('---------- Get Weather Forcast ----------')

    # URLセット
    region_url = "https://www.jma.go.jp/jp/week/" + region_code + ".html"
    req_main = requests.get(region_url)

    # HTMLデータ取得
    soup = BeautifulSoup(req_main.text, 'lxml')

    ###############
    # 結果用変数
    ###############
    # DATE = list()  # 日付結果リスト
    WEATHER = list()  # 天気結果リスト
    # WEATHERSTR = list()  # 天気文字列結果リスト
    RAIN = list()  # 雨フラグリスト
    MAXTEMP = list()  # 最高気温リスト
    MINTEMP = list()  # 最低気温リスト
    JSONLIST = list()  # JSON用リスト
    # OUTPUT_JSON = {"forcast": ""}

    # 天気部分抜き出し・雨フラグ作成
    bs_weather = soup.find_all("td", class_="for")

    # 最高気温
    bs_maxtemp = soup.find_all("font", class_="maxtemp")
    # 最低気温
    bs_mintemp = soup.find_all("font", class_="mintemp")
    # 天気文字列
    bs_weatherstr = soup.find_all("td",class_="for")[0:7:]
    # print(bs_weatherstr)
    # 日付
    bs_date = soup.find("caption")
    # メインループ
    # タイミングにより６日目までしか表示されないので6でループを強制的に止める
    for i in range(6):
        # print(i)

        # 日付
        # DATE.append(bs_date[i].contents[0])
        # print(bs_date[i].contents[0])

        # 天気
        WEATHER.append(bs_weather[i].contents[0])
        weatherlist = ["みぞれ", "雪", "ふぶき", "ひょう", "あられ"]
        # 雨フラグデータ作成
        rain_flg = ""
        # print(bs_weather[i].contents[0])
        # リストの中から"晴"の文字を検索して、-1なら見つからなかった場合
        if bs_weather[i].contents[0].find("晴") != -1:
            rain_flg = rain_flg+"1"
        else:
            rain_flg = rain_flg+"0"
        # リストの中から"曇り"の文字を検索して、-1なら見つからなかった場合
        if bs_weather[i].contents[0].find("曇") != -1:
            rain_flg = rain_flg+"1"
        else:
            rain_flg = rain_flg+"0"
        # リストの中から"雨"の文字を検索して、-1なら見つからなかった場合
        if bs_weather[i].contents[0].find("雨") != -1:
            rain_flg = rain_flg+"1"
        else:
            # 異常気象の場合も雨と同じステータスにするように変更
            for weather in weatherlist:
                if bs_weather[i].contents[0].find(weather) != -1:
                    rain_flg = rain_flg+"1"
                    break
            if len(rain_flg) == 2:
                rain_flg = rain_flg+"0"
        # print(rain_flg)

        RAIN.append(rain_flg)

        # リストの中から"雨"の文字を検索して、-1なら見つからなかった場合
        # if bs_weather[i].contents[0].find("雨") != -1:
        # RAIN.append("1")
        # else:
        # RAIN.append("0")

        # 最高気温
        MAXTEMP.append(bs_maxtemp[i].contents[0])

        # 最低気温
        MINTEMP.append(bs_mintemp[i].contents[0])

        # 日付
        strdate = bs_date.contents[0].split("日")[0] # ○月○○
        datelist = strdate.split("月") # [○,○○]
        thismonth = int(datelist[0])
        thisyear = datetime.datetime.today().year
        for j in range(len(datelist)):
            if j == 1:
                datelist[j] = str(int(datelist[j]) + i + 1)
                if int(datelist[j]) > calendar.monthrange(thisyear,int(datelist[0]))[1]:
                    datelist[j] = str((int(datelist[j]))%calendar.monthrange(thisyear,thismonth)[1])
                    datelist[0] = str(int(datelist[0]) + 1)
                    if datelist[0]=="13":
                        datelist[0] = "01"
                    if len(datelist[0]) < 2:
                        datelist[0] = "0" + datelist[0]
            if len(datelist[j]) < 2:
                datelist[j] = "0" + datelist[j]
        respdate = datelist[0] + "/" + datelist[1]

        # 天気文字列
        weatherstr = bs_weatherstr[i].img.get("title")

        # JSON 生成
        data_json = {
            "date": respdate,
            # "wather": WEATHER[i],
            "weather": weatherstr,
            "rain": RAIN[i],
            "maxtemp": bs_maxtemp[i].contents[0],
            "mintemp": bs_mintemp[i].contents[0]
        }
        JSONLIST.append(data_json)
        # weatherdataディレクトリに天気データを格納
        weathertoJson.createWeatherJsonFile(JSONLIST,region_code)
    return str(JSONLIST)

# デバッグ用：app.py実行時に呼ばれる
# gwr("346")