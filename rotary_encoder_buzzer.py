import RPi.GPIO as GPIO
import time

RoAPin = 11  # pin11 -> Connected to CLK
RoBPin = 12  # pin12 -> Connected to DT
RoSPin = 13  # pin13 -> Connected to SW
BuzzerPin = 15  # Example pin for buzzer, you can change it as per your setup
globalCounter = 0
flag = 0
Last_RoB_Status = 0  # two var. for pin B’s value
Current_RoB_Status = 0

def setup():
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(RoAPin, GPIO.IN)  # input mode
    GPIO.setup(RoBPin, GPIO.IN)
    GPIO.setup(RoSPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Bottom pin
    GPIO.setup(BuzzerPin, GPIO.OUT)  # Buzzer pin set as output
    rotaryClear()

def rotaryDeal():
    global flag, Last_RoB_Status, Current_RoB_Status, globalCounter
    Last_RoB_Status = GPIO.input(RoBPin)  # Read in data from DT
    while not GPIO.input(RoAPin):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1
    if flag == 1:
        flag = 0
        if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
            globalCounter += 1
            print('globalCounter = %d' % globalCounter)
            # Turn on buzzer to make the "z" sound
            GPIO.output(BuzzerPin, GPIO.HIGH)
            time.sleep(0.1)  # Buzz for a short duration
            GPIO.output(BuzzerPin, GPIO.LOW)
        if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
            globalCounter -= 1
            print('globalCounter = %d' % globalCounter)
            # Turn on buzzer to make the "z" sound
            GPIO.output(BuzzerPin, GPIO.HIGH)
            time.sleep(0.1)  # Buzz for a short duration
            GPIO.output(BuzzerPin, GPIO.LOW)

def clear(ev=None):
    global globalCounter
    globalCounter = 0
    print('globalCounter = %d' % globalCounter)
    time.sleep(1)

def rotaryClear():
    GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear)

def loop():
    while True:
        rotaryDeal()

def destroy():
    GPIO.cleanup()  # Release resource

setup()

try:
    loop()
except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program will be executed.
    destroy()
