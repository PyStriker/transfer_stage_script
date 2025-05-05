import time
import sys
#dependancy pywin32
import win32pipe, win32file, pywintypes
import re
import math

def Send(data):
    try:
        handle = win32file.CreateFile(
        r'\\.\pipe\HQ_server',
        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
        0,
        None,
        win32file.OPEN_EXISTING,
        0,
        None
        )
        res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)

        input_data = str.encode(data + '\n')
        # Send instruction data to c# server
        while True:
            win32file.WriteFile(handle, input_data)

            # Receive data from Python client
            result, resp = win32file.ReadFile(handle, 64*1024)
            win32file.CloseHandle(handle)
            msg = resp.decode("utf-8")
            print(f"message: {msg}")

            return msg

    except pywintypes.error as e:
        if e.args[0] == 2:
            print("no pipe, trying again in a sec")
            time.sleep(1)
        elif e.args[0] == 109:
            print("broken pipe, bye bye")
            return ""


def get_first_double(my_string):
    print(my_string)
    if (my_string is None):
        return 0;
    numeric_const_pattern = '[-+]? (?: (?: \\d* \\. \\d+ ) | (?: \\d+ \\.? ) )(?: [Ee] [+-]? \\d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)
    if any(char.isdigit() for char in my_string) == False:
        return 0
    var = rx.findall(my_string)[0]
    return float(var)

class bounds:
    def __init__(bound, xmin, ymin, xmax, ymax):
        bound.xmin = xmin
        bound.xmax = xmax
        bound.ymin = ymin
        bound.ymax = ymax
        

#rotates the chip sp it is paralelle with the coordinate system and returns xmax and ymax
def align_chip(bounds):
    #calculates xmax
    xmax = math.sqrt(math.pow(bounds[1][0]-bounds[0][0],2)+math.pow(bounds[1][1]-bounds[0][1],2))
    #calculates ymax
    ymax = math.sqrt(math.pow(bounds[2][0]-bounds[0][0],2)+math.pow(bounds[2][1]-bounds[0][1],2))
    aligned_bounds = bounds(xmax, ymax)
    #rotates base based on bounds
    #____________________________

    return aligned_bounds

# zeros the platform on the top right corner
def zero_platform(x0,y0):
    #sets origin to x0, y0
    return 0
#main script

#chip bounds [top left, top right, bottom left]
ex_bounds = bounds(0, 0, 100, 100)

#gets current position and prints the result

#
image_folder = "C:\\Users\\Transferstage\\Transfer_Stage_Script\\transfer_stage_script\\exfoliation_images\\" 
image_name = "flake_1"
command = "" 
isconnected = False
iscalibrated = False

#stage position, #objects 5x: 2, 10x, 3, etc.
x = 0
y = 0
#objective base field of view
fov = 3.0
#object magnification
mag = 5
#buffer for image range
buffer = 0
retcode = ""


while command != "1":
    command = input("1. quit\n2. calibrate")
    if command == "test":
        
        #Send("AUTFOC\n")

        #takes picture and saves it to image_folder
        print(get_first_double(Send("GETPOSX")))
        x = 0
        image_name = "(" + str(x) + ", " + str(y) + ")"
        location = "PIC:" + image_folder + image_name + "\n"
        time.sleep(5)
        Send(location)
        #updates x position:
        x += fov/mag
        command = "SETPOSX" + str(float(x)) + "\n"
        print(command)
        retcode = Send("SETPOSX5.0\n")
        print(retcode)
        if "Unknown" in retcode:
            print("failure")
            #break
        #sets pos to new coordinates based on input
        x = input("input x:")
        y = input("input y:")
        Send('SETPOSX' + str(x) + "\n")
        Send('SETPOSY' + str(y) + "\n")

    if command == "2": #prepares stage for exfoliation
        #checks connects to stage
        if Send('GETPOSX\n') == "":
            print("Transfer stage not connected\n")
            break
        else:
            isconnected = True
        #set stage height, position, Objective height, focus, vacume power, stage rotation and transfer arm rotation to defaults
        #breaks if any of these fail
        Send("SETPOSX0")
        Send("SETPOSY0")
        #Send("AUTFOC\n")
        
        iscalibrated = True
        #input coordinates of the corners of the exfoliation

    if command == "3": #
        if isconnected == False:
            print("Transfer stage is not connected\n")
            break
        if iscalibrated == False:
            print("Transfer stage is not calibrated\n")
            break
        
        #set objective to 5x
        #Send("SETOBJ2")
        x = ex_bounds.xmin
        y = ex_bounds.ymin
        #mag = get_first_double(Send('GETMAG\n'))
        #print(mag + "\n")
        while y <= ex_bounds.ymax + buffer:
            #captures image and stores it
            image_name = "(" + str(x) + ", " + str(y) + ")"
            location = "PIC:" + image_folder + image_name + "\n"
            Send(location)
            #updates x position:
            x += fov/mag
            retcode = Send("SETPOSX" + str(x) + "\n")
            if retcode == "Unknown command":
                break
            if x >= ex_bounds.xmax + buffer:
                x = ex_bounds.xmin
                y += fov/mag
                retcode = Send("SETPOSY" + str(y) + "\n")
                if retcode == "Unknown command":
                    break
            while get_first_double(Send("GETPOSX")) != float(x) or get_first_double(Send("GETPOSY")) != float(y):
                time.sleep(.5)
        
        
        
        

        