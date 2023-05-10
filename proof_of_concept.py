import speech_recognition as sr
import easygopigo3 as go
import time
import random
import serial
import serial.tools.list_ports
import time
import sys
import select


ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.name, port.description)

def callback(recognizer_instance, AudioData):
    global myRobot, ser, autonomy, timer
    try:
        a = recognizer_instance.recognize_google(AudioData)
        print(a)
        split = a.split(" ")
        for i in range(len(split)):    
            try:
                split[i] = int(split[i])
                idx = split.index(split[i])
            except:
                pass 
        #print(split)
        autonomy = 0
        if ("go" or "drive") in split:
            if "forward" in split:
                for i in split:
                    if (isinstance(i,(int,float))):
                        print(f"Driving forward {i}cm")
                        sendToDisplay(ser, f"Forward {i} cm")
                        myRobot.drive_cm(i)
                        break
                else:
                    myRobot.forward()
                    print("Driving forward")
                    sendToDisplay(ser, "Driving forward")
            elif "backward" in split:
                for i in split:
                    if (isinstance(i,(int,float))):
                        print(f"Drive backward {i}cm")
                        sendToDisplay(ser, f"Backward {i} cm")
                        myRobot.drive_cm(-i)
                        break
                else:
                    sendToDisplay(ser, "Driving backward")
                    myRobot.backward()
        elif "turn" in split:
            if "left" in split:
                print("Turning left")
                sendToDisplay(ser, 'Turning left')
                myRobot.steer(25,-25)
            elif "right" in split:
                print("Turning right")
                sendToDisplay(ser, "Turning right")
                myRobot.steer(-25,25)
            elif "degrees" in split:
                if (isinstance(i,(int,float))):
                    myRobot.turn_degrees(i)
                    print(f"Turning {i} degrees")
                    sendToDisplay(ser, f"Turning {i} dgrs")
        elif ("stop" or "STOP") in split:
            sendToDisplay(ser, 'Stopped')
            myRobot.steer(0, 0)
        timer = time.time()
        return
    except:
        #sendToDisplay(ser, 'Can''nt hear')
        pass
        
                
def sendToDisplay(ser, msg):
    ser.write(msg.encode('utf-8'))
    # time.sleep(2)

def main():
    global ser, myRobot, timer, autonomy
    ser = serial.Serial(port='/dev/ttyACM1',baudrate = 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
    timer = time.time()
    autonomy = 1
    myRobot = go.EasyGoPiGo3()
    r = sr.Recognizer()
    #sr.Microphone.list_microphone_names()
    mic = sr.Microphone(device_index=2) #the device index is important, you can get it with sr.Microphone.list_microphone_names()
    listener = r.listen_in_background(mic, callback,phrase_time_limit = 5)
    myRobot.set_speed(300)
    while True:
        if abs(timer - time.time())>=5:
            autonomy = 1
        if autonomy == 1:
            var = random.randint(1,2)
            sendToDisplay(ser, "Autonomous mode")
            if var == 1:
                myRobot.drive_cm(random.randint(-10,10),blocking = False)
                autonomy = 0
                timer = time.time()
            elif var == 2:
                myRobot.turn_degrees(random.randint(-90,90),blocking = False)
                autonomy = 0
                timer = time.time()
        else:
            pass
            #key = [go ,drive,backward, forward,turn,number =5, meter = 1, cente]
            #go > 0
            #    forwa
            #        myroboy.(numer)
        #If audio is STOP! myRobot.stop()
        #if audio is drive forwards, backwards, myRobot.forwards()/myRobot.backwards()
        #IF audio says drive X cm forwards/backwards, myRobot.forwards()/backwards().drive_cm(n)
        #if audio says turn X degrees, myRobot.turn_degrees(n)
        
        
if __name__ == '__main__':
    main()
