# WeatherAPIから呼ばれる、Jsonファイルを作成するAPI
# 翌日から6日分のデータが格納される
# (正確には、午前0時から午前11時までに実行された場合は当日から6日分)
# 保存されるjsonの型
# [
#   {
#     "date": "03/20",
#     "weather": "晴れ後曇り",
#     "rain": "110",
#     "maxtemp": "22",
#     "mintemp": "9"
#   },
#   {
#     "date": "03/21",
#     ...
#     "date": "03/25",
#     ...
#   }
# ]
import json

def createWeatherJsonFile(weather,region):
    filePath = 'weatherdata/' + region + '.json'
    with open(filePath, mode='w') as f:
        json.dump(weather,f,indent=2, ensure_ascii=False)