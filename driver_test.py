import json
import os
import shutil
import sys
import time
import cv2

import Utils.conversion_functions as conversion
import Utils.etc_functions as etc
import Utils.raster_functions as raster
import Utils.stitcher_functions as stitcher
import Utils.upload_functions as uploader
from Drivers import CameraDriver, MicroscopeDriver, MotorDriver
from Drivers import PipeClient
from GMM.Model.GMMDetector import Detector
from GUI import ParameterPicker

buffer = 0
#establish pipeclient
client = PipeClient()

#connect to transfer stage
while not client.connect():
    print("Connecting...\n")
    time.sleep(.5)
    buffer += 1
    if buffer > 15:
        print("connection unsuccessful\n")
        sys.exit()
print("Connection successful")    

client.send_command(f"SETPOSZ{int(-2)}")
client.send_command(f"SETPOSZ{int(-7)}")
