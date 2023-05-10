from machine import Pin
import utime
import os
import sys
import select
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

lcd_columns = 16
lcd_rows = 2

scl_pin = board.GP27
sda_pin = board.GP26

i2c = busio.I2C(scl_pin, sda_pin)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

while True:
    res = select.select([sys.stdin], [], [], 0)
    data = ""
    while res[0]:
        data = data + sys.stdin.read(1)
        res = select.select([sys.stdin], [], [], 0)
        lcd.clear()
    if data != '':
        lcd.message = data
#    print(data, end = '')
#    time.sleep(1)
#    if data == 'hello':
#        reply = 'reply'
#        sys.stdout.buffer.write(reply)
#        utime.sleep(2)
#        break


sys.stdout.buffer.write('123\n')
utime.sleep(1)
# 
# 
# 
# # while True:
# #     r = os.read(0, 32)
# #     r = sys.stdin.readline()
# #     r = sys.stdin.buffer.read(20)
# #     print(r)
# 
# led = Pin(25, Pin.OUT)
# 
# echo_pin = 3
# trig_pin = 4
# 
# echo = Pin(echo_pin, Pin.IN)
# trigger = Pin(trig_pin, Pin.OUT)
# 
# delay_us = 10
# signal_off = 0
# signal_on = 0
# def get_distance_in_cm():
#     global signal_off, signal_on
#     trigger.low()
#     utime.sleep_us(2)
#     trigger.high()
#     utime.sleep(delay_us)
#     trigger.low()
#     while echo.value() == 0:
#         signal_off = utime.ticks_us()
#     while echo.value() == 1:
#         signal_on = utime.ticks_us()
#     duration_us = signal_on - signal_off
#     distance = duration_us * 0.34 / 2
#     distance /= 10
#     print(distance)
# #     return distance
# 
# def on():
#     print("LED on")
#     led.value(1)
# 
# def off():
#     print("LED off")
#     led.value(0)
