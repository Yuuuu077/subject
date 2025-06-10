from ssd1306 import SSD1306_I2C
from machine import I2C, Pin
from character import get_character_bitmap
import weather  # 引入 weather 模組

# 初始化 OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)

# 中文字體繪圖
def draw_chinese(oled, x, y, char):
    data = get_character_bitmap(char)
    if data is None:
        oled.text("?", x, y)
        return
    for row in range(16):
        byte1 = data[row * 2]
        byte2 = data[row * 2 + 1]
        for bit in range(8):
            if byte1 & (0x80 >> bit):
                oled.pixel(x + bit, y + row, 1)
            if byte2 & (0x80 >> bit):
                oled.pixel(x + 8 + bit, y + row, 1)

def draw_chinese_text(oled, x, y, text):
    for i, ch in enumerate(text):
        draw_chinese(oled, x + i * 16, y, ch)

def draw_bar(oled, x, y, width, height):
    for dx in range(width):
        for dy in range(height):
            oled.pixel(x + dx, y + dy, 1)

# 第三頁天氣資料快取（初始為 None）
weather_data = None

def refresh_weather():
    global weather_data, last_weather_time
    import time
    try:
        weather_data = weather.get_weather()
        last_weather_time = time.time()
        print("✅ 已強制更新天氣資料")
    except Exception as e:
        print("❌ 強制更新天氣資料失敗：", e)

def show_page(page, data):
    global weather_data
    oled.fill(0)

    if page == 0:
        draw_chinese_text(oled, 0, 0, "即時感測儀表板")
        oled.text("Temp: {} C".format(data['temp']), 0, 20)
        oled.text("Humi: {} %".format(data['humi']), 0, 30)
        oled.text("Light: {}".format(data['light']), 0, 40)
        oled.text("Setting: {}%".format(data['pot']//40, 0, 50)

    elif page == 1:
        draw_chinese_text(oled, 0, 0, "圖形模式")
        draw_bar(oled, 0, 20, int(data['temp']), 8)
        draw_chinese_text(oled, 95, 20, "溫度")
        draw_bar(oled, 0, 40, int(data['light'] / 40), 8)
        draw_chinese_text(oled, 95, 40, "光度")

    elif page == 2:
        try:
            if weather_data is None:
                print("更新天氣中...")
                weather_data = weather.get_weather()
            draw_chinese_text(oled, 0, 0, weather_data["location"])
            draw_chinese_text(oled, 0, 16, "天氣")
            oled.text(": " , 32, 20)
            draw_chinese_text(oled, 0, 32, weather_data["weather"])
            oled.text(": " + weather_data["rain"], 48, 52)
            draw_chinese_text(oled, 0, 48, "降雨率")
        except:
            oled.text("天氣讀取失敗", 0, 0)

    oled.show()