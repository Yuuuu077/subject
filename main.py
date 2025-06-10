from machine import Pin, Timer
import time
import sensors
import display
import alerts
import network
import weather

# Wi-Fi 設定（請改成你的實體板子可連的熱點）
SSID = 'Galaxy S20 5G'
PASSWORD = 'c8763333'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("正在連線到 WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print("✅ WiFi 已連線:", wlan.ifconfig())
    
connect_wifi()

# ========== 全域變數 ==========
current_page = 0
num_pages = 3
force_update = True  # 預設一開始會更新一次

# ========== 初始化 ==========
button_a = Pin(5, Pin.IN, Pin.PULL_UP)   # A: 切換畫面
button_b = Pin(36, Pin.IN)               # B: 強制更新
debounce_timer_a = Timer(1)
debounce_timer_b = Timer(2)

# ========== 資料更新定時器 ==========
def auto_update(timer):
    data = sensors.read_all()
    alerts.check(data)
    display.show_page(current_page, data)


timer = Timer(0)
timer.init(period=1000, mode=Timer.PERIODIC, callback=auto_update)

# ========== 按鈕處理 ==========
def handle_button_a(timer):
    global current_page, force_update
    if not button_a.value():
        current_page = (current_page + 1) % num_pages
        force_update = True  # 切換頁面後重新更新顯示
        print("頁面切換至：", current_page)

def handle_button_b(timer):
    global force_update
    global weather_data
    if not button_b.value():
        force_update = True
        print("更新天氣中...")
        display.refresh_weather()
        print("強制更新資料")

def irq_handler_a(pin):
    debounce_timer_a.init(mode=Timer.ONE_SHOT, period=50, callback=handle_button_a)

def irq_handler_b(pin):
    debounce_timer_b.init(mode=Timer.ONE_SHOT, period=50, callback=handle_button_b)

# 綁定中斷 IRQ
button_a.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler_a)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler_b)

# ========== 主迴圈 ==========
while True:
    time.sleep(0.1)  # 主迴圈閒置，不阻塞 IRQ 或 Timer                                                                                                                                                                                                                                                                           