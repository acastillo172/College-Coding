#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# importing systemlink
import ubinascii, ujson, urequests, utime

# Write your program here
brick.sound.beep()

Key = '....'

def SL_setup():
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = urequests.get(urlValue,headers=headers).text
          data = ujson.loads(value)
          print(data)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result


Put_SL('Launch','STRING','0')

# Port assignments for sensor and motor
ultSens = UltrasonicSensor(Port.S1)
launchMotor = Motor(Port.A)

# main loop
while True:
    
    # get launch signal from system link
    if Get_SL('Launch') == 'true':
        dist = ultSens.distance()

        # use the equation found from data collection
        motorSpeed = (1.1071*dist) + 53.445

        # launch the ball
        launchMotor.run_angle(motorSpeed, -360)

        # put the calculated parameters back into system link
        Put_SL('Distance (mm)','STRING',str(dist))
        Put_SL('Angular Velocity','STRING',str(motorSpeed))

        

