#import Drivers.Camera_Driver as Camera
import Drivers.Microscope_Driver as Microscope
import Drivers.Motor_Driver as Motor
from Drivers import PipeClient as Server
import time, sys

buffer = 0
#establish pipeclient
client = Server.PipeClient()

#connect to transfer stage
while not client.connect():
    print("Connecting...\n")
    time.sleep(.5)
    buffer += 1
    if buffer > 15:
        print("connection unsuccessful\n")
        sys.exit()
print("Connection successful")    

"""
microscope driver test
"""
#initialization
micro = Microscope(client)
#


"""
motor driver test
"""
#initialization
motor = Motor(client)

#Get position
pos = motor.get_pos()
print(pos)

#absolute move
    # 2,2
motor.abs_move(2,2)
    # 0,0
motor.abs_move(0,0)

#relative move
    # 2,2
motor.rel_move(2,2)
    # -2,-2
motor.rel_move(-2,-2)
"""
camera driver test
"""