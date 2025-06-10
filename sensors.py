from machine import ADC, Pin
import dht

# 接腳設定
light_sensor = ADC(Pin(39))
light_sensor.atten(ADC.ATTN_11DB)

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

dht_sensor = dht.DHT11(Pin(15))

def read_all():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humi = dht_sensor.humidity()
    except OSError:
        temp = -1
        humi = -1

    return {
        'temp': temp,
        'humi': humi,
        'light': light_sensor.read(),
        'pot': pot.read()
    }