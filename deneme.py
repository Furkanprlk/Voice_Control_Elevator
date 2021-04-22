import time
import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)

#23 DS SER
#24 STCP RCLK
#25 SHCP SRCLK
katRCLK = 24
katSER = 23
katSRCLK = 25

totalIC = 3
totalICPins= totalIC*8

#katData = [totalICPins]
katData = [0] * totalICPins

def setup():
    IO.setup(katRCLK, IO.OUT)
    IO.setup(katSER, IO.OUT)
    IO.setup(katSRCLK, IO.OUT)
    
def loop():
    for i in range(totalICPins):
        katData[i] = 0;
        katUpdateData()
        time.sleep(.3)
        katClear()
        
def katUpdateData():
    IO.output(katRCLK, IO.LOW)
    for i in range(totalICPins,0,-1):
        
        IO.output(katSRCLK, IO.LOW)
        if(katData[i-1]==1):
            IO.output(katSER, IO.HIGH)
        else:
            IO.output(katSER, IO.LOW)
        IO.output(katSRCLK, IO.HIGH)
    IO.output(katRCLK, IO.HIGH)
    
def katClear():
    for i in range(totalICPins):
        katData[i] = 1;
    katUpdateData()
    
setup()
while 1:
    loop()