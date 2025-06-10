from machine import Pin, PWM
import time

# 初始化腳位
led_r = Pin(16, Pin.OUT)
led_y = Pin(12, Pin.OUT)
led_g = Pin(13, Pin.OUT)
buzzer = PWM(Pin(14))  # 用 PWM 控制

def beep(freq=1000, duration=1000):
    buzzer.freq(freq)
    buzzer.duty(10)
    time.sleep_ms(duration)
    buzzer.duty(0)

def check(data):
    led_r.off()
    led_y.off()
    led_g.off()
    buzzer.duty(0)

    temp = data['temp']
    light = data['light']
    humi = data['humi']

    if temp > 30 or  humi > data['pot']//40:
        led_r.on()
        beep(1000, 150)  # 發出一聲
    elif temp > 28 or light < 500 or data['pot']//40 >= humi >= 70:
        led_y.on()
    else:
        led_g.on()
    
    