import os, time
from Drivers.Interfaces.Motor_Interface import MotorDriverInterface
from ctypes import *
import sys, Drivers.PipeClient as PipeClient

class MotorDriver(MotorDriverInterface):
    """
    controls the HQ transfer stage motors
    """

    def __init__(self, cli: PipeClient.PipeClient):

        self.cli = cli

        self.abs_move(0,0)
        def_z = 2151.587 #for 90nm
        self.set_z_height(def_z)

        """ calibrate everything to defaults """

    
    def set_z_height(self, height):
        """
        Sets the Height in µm\n
        Only works if the AF is not on\n
        Has small protection by only setting height between 3500 and 6500 µm
            Need to add saftey checks to make sure things don't run into each other
        """
        if -7000 <= height <= 3000:
                self.cli.send_command(f'SETPOSZ{height/1000}')
                while(abs(PipeClient.get_first_double(self.cli.send_command("GETZ")) - height/1000) > 0.01):
                    time.sleep(1)
                    buf += 1
                    if buf > 60:
                        print("error")
                        sys.exit()
        else:
            print("hieght out of range\n")
            return
        
    def get_pos(self):
        """
        Returns the Current Position
        """
        # query actual position (4 axes) (unit depends on GetDimensions)
        x = PipeClient.get_first_double(self.cli.send_command('GETPOSX'))
        y = PipeClient.get_first_double(self.cli.send_command('GETPOSY'))

        return (x, y)

    def abs_move(self, x, y, silent: bool = True, wait_for_finish: bool = True):
        """
        moves to an absolute position, checks for max_y and max_y\n
        """
        moveX = x
        moveY = y
        wait_for_finish = c_bool(wait_for_finish)
        buf = 0

        self.cli.send_command(f'SETPOSX{moveX}')
        while(abs(PipeClient.get_first_double(self.cli.send_command("GETPOSX")) - float(moveX)) > 0.01):
            time.sleep(1)
            buf += 1
            if buf > 60:
                print("error")
                sys.exit()
       
        self.cli.send_command(f'SETPOSY{moveY}')
        while(abs(PipeClient.get_first_double(self.cli.send_command("GETPOSY")) - float(moveY)) > 0.01):
            time.sleep(1)
            buf += 1
            if buf > 60:
                print("error")
                sys.exit()
        
        if not silent:
            print(f"Moved to {x}, {y} (Absolut)")

    def rel_move(self, dx, dy, silent: bool = True):
        """
        moves relative to the Current position, checks for max_x and max_y\n
        returns False if the move was unsuccesful\n
        return True if successful
        """

        move_dx = c_double(dx)
        move_dy = c_double(dy)
        x = PipeClient.get_first_double(self.cli.send_command('GETPOSX')) + move_dx
        y = PipeClient.get_first_double(self.cli.send_command('GETPOSY')) + move_dy
        buf = 0

        self.cli.send_command(f'SETPOSX{x}')
        while(abs(PipeClient.get_first_double(self.cli.send_command("GETPOSX")) - x) > 0.01):
            time.sleep(1)
            buf += 1
            if buf > 60:
                print("error")
                sys.exit()
        
        self.cli.send_command(f'SETPOSY{y}')
        while(abs(PipeClient.get_first_double(self.cli.send_command("GETPOSY")) - y) > 0.01):
            time.sleep(1)
            buf += 1
            if buf > 60:
                print("error")
                sys.exit()
       
        if not silent:
            print(f"Moved by {dx}, {dy} (Rel)")
        return True
    
    def set_z_height(self, height):
        """
        Sets the Height in µm\n
        Only works if the AF is not on\n
        Has small protection by only setting height between 3500 and 6500 µm
            Need to add saftey checks to make sure things don't run into each other
        """
        buf = 0
        if -7000 <= height <= 3000:
                self.cli.send_command(f'SETZ{height/1000}')
                while(abs(PipeClient.get_first_double(self.cli.send_command("GETZ")) - height/1000) > 0.01):
                    time.sleep(1)
                    buf += 1
                    if buf > 60:
                        print("error")
                        sys.exit()
        else:
            print("hieght out of range\n")
            return