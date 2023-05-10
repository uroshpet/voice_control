# code for ultrasonic sensors and LCD display adopted from lab02, lab03, lab08

import utime
from machine import Pin, PWM
import sys
import select
import json
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

signal_off = 0
signal_on = 0
msg_time = 0

echo_front = Pin(3, Pin.IN)
trig_front = Pin(4, Pin.OUT)
echo_back = Pin(7, Pin.IN)
trig_back = Pin(8, Pin.OUT)
echo_right = Pin(11, Pin.IN)
trig_right = Pin(12, Pin.OUT)
echo_left = Pin(14, Pin.IN)
trig_left = Pin(15, Pin.OUT)
buzzer = PWM(Pin(19, Pin.OUT))
i2c = busio.I2C(board.GP27, board.GP26)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, 16, 2)

def buzz():
    buzzer.duty_u16(2500)
    buzzer.freq(750)
    utime.sleep_ms(750)
    buzzer.duty_u16(0)
    
def get_distance(sensor):
    global signal_off, signal_on
    if sensor == 'front':
        trigger = trig_front
        echo = echo_front
    elif sensor == 'back':
        trigger = trig_back
        echo = echo_back
    elif sensor == 'right':
        trigger = trig_right
        echo = echo_right
    else:
        trigger = trig_left
        echo = echo_left
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(60)
    trigger.low()
    while echo.value() == 0:
        signal_off = utime.ticks_us()
    while echo.value() == 1:
        signal_on = utime.ticks_us()
    duration_us = signal_on - signal_off
    distance = str(int(duration_us * 0.34 / 20))
    return distance

while True:
    msg = ''
    while (data_in := select.select([sys.stdin], [], [], 0)[0]):
        #if len(select.select([sys.stdin], [], [], 0)) > 1:
        #    break
        msg += sys.stdin.read(1)
        lcd.clear()
        print("Adding")
    if msg != '':
        msg_time = utime.time()
        print("Recieved message")
        if 'buzz' in msg.lower():
            lcd.message = msg[4:]
            buzz()
        else:
            lcd.message = msg
    if utime.time() - msg_time >= 60:
        #print()
        lcd.clear()
    readings = {}
    readings['front'] = get_distance('front')
    readings['right'] = get_distance('right')
    readings['left'] = get_distance('left')
    readings['back'] = get_distance('back')
    print(json.dumps(readings))
    utime.sleep(0.25)