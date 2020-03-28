#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import math

# importing systemlink
import ubinascii, ujson, urequests, utime

# Write your program here
brick.sound.beep()

Key = '....'

# Functions for System Link
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
     
# Port assignmnets for sensor and motor
ultSens = UltrasonicSensor(Port.S1)
launchMotor = Motor(Port.A)

Put_SL('Launch','STRING','0')

# Defining unchanging variables
g = -9.81
y1 = 0.155
y2 = 0.096
theta = 45
r = 0.158
circ = 2*math.pi*r

#main loop
while True:
     dist = ultSens.distance()
     dist2 = (dist-10) * 0.001

     # calculating the value inside the square root for the equation
     x = (g*(dist2*dist2))/(2*math.cos(theta)*math.cos(theta)*(y2-y1-dist2))
     
     # geeting the sitance value from system link
     if Get_SL('Launch') == 'true':

          # finding velocity
          vel = math.sqrt(x)

          # converting to rotation speed (deg/s)
          motorSpeed = (vel/circ)*360
          motorSpeed2 = motorSpeed/2
          print(motorSpeed2)

          # launching the ball
          launchMotor.run_angle(motorSpeed2, -360)
          
          # placing the values claculated back into system link
          Put_SL('Distance (mm)','STRING',str(dist))
          Put_SL('Angular Velocity','STRING',str(motorSpeed2))


