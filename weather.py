import urequests

API_KEY = "CWA-C5712E9C-642D-4EBE-B688-C592A4C8302C"  # ⚠️ 記得填入你註冊的金鑰
LOCATION = "花蓮縣"         # 可換成任意地區

URL = (
    "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    "?Authorization=" + API_KEY +
    "&locationName=" + LOCATION
)

def get_weather():
    try:
        res = urequests.get(URL)
        data = res.json()
        info = data["records"]["location"][0]["weatherElement"]
        weather = info[0]["time"][0]["parameter"]["parameterName"]
        rain = info[1]["time"][0]["parameter"]["parameterName"]
        print("天氣資料擷取成功：")
        print("地區：", LOCATION)
        print("天氣狀況：", weather)
        print("降雨機率：", rain + "%")
        return {
            "location": LOCATION,
            "weather": weather,
            "rain": rain + "%"
        }
    except Exception as e:
        print("❌ 天氣資料擷取失敗：", e)
        return {
            "location": LOCATION,
            "weather": "讀取失敗",
            "rain": "--"
        }