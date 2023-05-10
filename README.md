**Project name:** g17: Voice-controlled robot

**Students in project:**

1. Uros Petrovic

2. Olga Puksberg

3. Matis Tõnisson

**[Link to Trello board](https://trello.com/b/K10ugQ4e/subtasks-for-the-project)** 

**Overview:**

Our project task is to implement a voice-controlled robot that is able to understand several basic commands. If the robot is not recieving commands it will drive around autonomously.
The languages the robot will understand is English and if possible Estonian as well. The voice will be sensed using a microphone module, and using the sound level other sound could
be filtered out. The plan is to have around 7 commands, depending on the complexity more could be added. The automonous portion will be controlled using ultrasonic distance sensors
on each side of the robot. Depending on the workload and complexity of the beforementioned tasks the option to use a LCD display and a simple buzzer could be added
to visualize the robot state and have the robot communicate back. The main problems that could happen is whether or not all modules will be available due to the robot(GoPiGo2 has less modules than 3).

**Instructions on running the robot:**

1. Connect the LCD to the Pico

2. Connect the Pico

3. Connect the Pico to the GoPiGo3 

4. Put the code in proof_of_concept_pico.py to the main.py of the Pico

5. Connect to the GoPiGo3

6. Rename the pins used in the main.py of the Pico with the ones the LCD is connected to

7. Rename the serial port witch the Pico is using to communicate with the PI in the proof_of_concept.py script 

8. Run the command: "python3 proof_of_concept.py" in the terminal

**Components:**

| Item (available in the Labs)   | Need from instructors   | Currently have   
|-----------------------------   |----------------------   |---------------
| Ultrasonic distance sensor   	 | x0                      | x4
| Raspberry Pi Pico              | x2 (only 1 allowed)      | x1
| GoPiGo3/GoPiGo2                | x0                      | x1 (GoPiGo3)
| 16x2 char LCD display          | x0                      | x1
| Sound level sensor             | x0                      | x2 (high and low level)
| Microphone module              | x2 (unavailable)         | x0
| Small passive buzzer module    | x0                      | x1
| Breadboard                     | x0                      | x1
| Wires                          | MF x14                  | x20
| 3S LiPo Battery + level sensor | x0                      | x1 (recieved 8.11)
| Power cable for Pico           | x0                      | x1
| USB camera with built in mic   | x0                      | x1
| SD card                        | x0                      | x1