import speech_recognition as sr
import easygopigo3 as go
import time
import random
import time
import sys
import select
import serial
import serial.tools.list_ports
import json

MIN_DISTANCE = 30
SPEED = 75
display_msg = "Starting robot"
autonomy = 0
device = "/dev/"
ports = serial.tools.list_ports.comports()

robot = go.EasyGoPiGo3()
robot.set_speed(SPEED)

for port in ports:
    if "board" in port.description.lower():
        device += port.name
        
pico = serial.Serial(device, 115200, timeout = 1)

def sendToDisplay(msg):
    global display_msg
    if display_msg != msg:
        display_msg = msg
        pico.write(msg.encode('utf-8'))
    time.sleep(0.2)
    pico.read_all()

def get_distances():
    line = pico.readline().decode('utf-8')
    pico.read_all()
    while line == '':
        line = pico.readline().decode('utf-8')
    #print(line)
    if(line[0]!= '{'):
        if(line[0]!= '"'):
            line = '{"' + line
        else:
            line = '{' + line
    try:
        data = json.loads(line.strip())
    except:
        return -1
    #print(data)
    return data

def turn(dr, dl):
    if dr > MIN_DISTANCE and dl > MIN_DISTANCE:
        if dr > dl:
            robot.spin_right()
            sendToDisplay('Turning right')
        else:
            robot.spin_left()
            sendToDisplay('Turning left')
    elif dr > MIN_DISTANCE:
        robot.spin_right()
        sendToDisplay('Turning right')
    elif dl > MIN_DISTANCE:
        robot.spin_left()
        sendToDisplay('Turning left')
    else:
        robot.steer(0, 0)
        sendToDisplay('Stopped')

def autonomous():
    global autonomy
    distances = get_distances()
    #print(distances)
    while distances == -1:
        distances = get_distances()
    #print("debug")
    df = int(distances['front'])
    if df > MIN_DISTANCE:
        robot.forward()
    else:
        dr = int(distances['right'])
        dl = int(distances['left'])
        if(autonomy == 1):
            turn(dr, dl)
    #time.sleep(0.0002)

def callback(recognizer_instance, AudioData):
    global robot, pico, autonomy, timer
    if autonomy == 0:
        sendToDisplay("Processing")
    try:
        a = recognizer_instance.recognize_google(AudioData, language = "en")
    except:
        sendToDisplay("Can't hear")
        return
    #print(a)
    split = a.split(" ")
    for i in range(len(split)):    
        try:
            split[i] = int(split[i])
            idx = split.index(split[i])
        except:
            pass 
    #print(split)
    #autonomy = 0
    if "go" in split or "drive" in split:
        autonomy = 0
        distances = get_distances()
        while distances == -1:
            distances = get_distances()
        if "forward" in split:
            for i in split:
                if (isinstance(i,(int,float))):
                    #print(f"Driving forward {i}cm")
                    if (int(distances['front']) < i):
                        sendToDisplay("BuzzToo close!")
                    else:
                        sendToDisplay(f"Forward {i} cm")
                        robot.drive_cm(i)
                        autonomy = 0
                    timer = time.time()
                    break
            else:
                try:
                    robot.drive_cm(int(distances['front']) - MIN_DISTANCE)
                except:
                    robot.drive_cm(MIN_DISTANCE)
                #robot.forward()
                autonomy = 0
                #print("Driving forward")
                sendToDisplay("Driving forward")
        elif "backward" in split or "back" in split or "backwards" in split:
            for i in split:
                if (isinstance(i,(int,float))):
                    #print(f"Drive backward {i}cm")
                    if int(distances['back']) < i:
                        sendToDisplay("BuzzToo close!")
                    else:
                        sendToDisplay(f"Backward {i} cm")
                        robot.drive_cm(-i)
                        autonomy = 0
                    break
            else:
                try:
                    robot.drive_cm(-(int(distances['back']) - MIN_DISTANCE))
                except:
                    robot.drive_cm(-MIN_DISTANCE)
                #robot.backward()
                autonomy = 0
                sendToDisplay("Driving backward")
        elif ("right" in split) or ("write" in split):
            for i in split:
                if isinstance(i, (int, float)):
                    print(distances)
                    if int(distances['right']) < i:
                        sendToDisplay("BuzzToo Close!")
                        break
                    else:
                        sendToDisplay(f"Right {i} cm")
                        robot.turn_degrees(90)
                        robot.drive_cm(i)
                        autonomy = 0
                        break            
            robot.turn_degrees(90)
            try:
                robot.drive_cm(int(distances['right']) - MIN_DISTANCE)
            except:
                robot.drive_cm(MIN_DISTANCE)
            autonomy = 0
            sendToDisplay("Driving right")
        elif "left" in split:
            for i in split:
                if isinstance(i, (int, float)):
                    if int(distances['left']) < i:
                        sendToDisplay("BuzzToo Close!")
                        break
                    else:
                        sendToDisplay(f"Left {i} cm")
                        robot.turn_degrees(-90)
                        robot.drive_cm(i)
                        autonomy = 0
                        break
            robot.turn_degrees(-90)
            try:
                robot.drive_cm(int(distances['left']) - MIN_DISTANCE)
            except:
                robot.drive_cm(MIN_DISTANCE)
            autonomy = 0
            sendToDisplay("Driving left")
    elif "turn" in split:
        autonomy = 0
        if "left" in split:
            #print("Turning left")
            sendToDisplay('Turning left')
            robot.steer(-25,25)
        elif "right" in split or "write" in split:
            #print("Turning right")
            sendToDisplay("Turning right")
            robot.steer(25, -25)
        elif "degrees" in split or '°' in a or "degree" in split:
            for i in split:
                #print(i)
                if (isinstance(i,(int,float))):
                    robot.turn_degrees(i)
                    #print(f"Turning {i} degrees")
                    sendToDisplay(f"Turning {i} dgrs")
                elif "°" in i:
                    #print("found")
                    #print(i[:-1])
                    robot.turn_degrees(int(i[:-1]))
                    #print(f"Turning {i} degrees")
                    sendToDisplay(f"Turning {int(i[:-1])}")
                    
            
    elif "stop" in split or "STOP" in split or "terminate" in split:
        autonomy = 0
        sendToDisplay('Stopped')
        robot.steer(0, 0)
    elif "autonomy" in split or "economy" in split:
        if ("on") in split or autonomy == 0:
            sendToDisplay("Autonomy ON")
            autonomy = 1
        elif ("off") in split or autonomy == 1:
            sendToDisplay("Autonomy OFF")
            robot.steer(0,0)
            autonomy = 2
    timer = time.time()
    return

def main():
    global pico, robot, timer, autonomy
    timer = time.time()
    autonomy = 0
    robot = go.EasyGoPiGo3()
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.dynamic_energy_threshold = True
    sr.Microphone.list_microphone_names()
    mic = sr.Microphone(device_index=2) #the device index is important, you can get it with sr.Microphone.list_microphone_names()
    listener = r.listen_in_background(mic, callback,phrase_time_limit = 5)
    
    while True:
        if autonomy == 1:
            autonomous()
        if autonomy == 2:
            sendToDisplay("Autonomy off!")
            robot.steer(0,0)
            autonomy = 0
        if autonomy == 10:
            sendToDisplay('')
            time.sleep(1)
        #print(autonomy)
        #time.sleep(0.0002) display[4:]
        #if(display[:2] =="Buzz"):
            #buzz
            #lc.
            #key = [go ,drive,backward, forward,turn,number =5, meter = 1, cente]
            #go > 0
            #    forwa
            #        myroboy.(numer)
        #If audio is STOP! robot.stop()
        #if audio is drive forwards, backwards, robot.forwards()/robot.backwards()
        #IF audio says drive X cm forwards/backwards, robot.forwards()/backwards().drive_cm(n)
        #if audio says turn X degrees, robot.turn_degrees(n)
        
        
if __name__ == '__main__':
    main()