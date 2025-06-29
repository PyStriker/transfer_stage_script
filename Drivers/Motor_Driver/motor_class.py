import os
from Drivers.Interfaces.Motor_Interface import MotorDriverInterface
from ctypes import *
import sys, command_server

file_path = os.path.dirname(__file__)
try:
    dll_dir = os.path.join(file_path, "DLL_Files")
    dll_folders = os.listdir(dll_dir)
    dll_folder = [
        folder for folder in dll_folders if folder.startswith("TangoDLL_64bit_V")
    ][0]
except:
    raise ValueError("No Tango DLL found, Check the DLL_Files folder")

dll_path = os.path.join(dll_dir, dll_folder, "Tango_DLL.dll")


class MotorDriver(MotorDriverInterface):
    """
    controls the HQ transfer stage motors
    """

    def __init__(self, dll_path=dll_path):

        self.pipe = command_server.PipeClient()
        self.pipe.connect()

        """ calibrate everything to defaults """

    

    def get_pos(self):
        """
        Returns the Current Position
        """
        # query actual position (4 axes) (unit depends on GetDimensions)
        x = command_server.get_first_double(self.pipe.send_command('GETPOSX'))
        y = command_server.get_first_double(self.pipe.send_command('GETPOSY'))

        return (x, y)

    def abs_move(self, x, y, silent: bool = True, wait_for_finish: bool = True):
        """
        moves to an absolute position, checks for max_y and max_y\n
        """
        moveX = c_double(x)
        moveY = c_double(y)
        wait_for_finish = c_bool(wait_for_finish)

        error = self.pipe.send_command(f'SETPOSX{moveX}')
        if error > 0:
            print("Error: abs_move " + str(error))
            sys.exit()
        error = self.pipe.send_command(f'SETPOSY{moveY}')
        if error > 0:
            print("Error: abs_move " + str(error))
            sys.exit()
        else:
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
        x = command_server.get_first_double(self.pipe.send_command('GETPOSX')) + move_dx
        y = command_server.get_first_double(self.pipe.send_command('GETPOSY')) + move_dy

        error = self.pipe.send_command(f'SETPOSX{x}')
        if error > 0:
            print("Error: rel_move " + str(error))
            sys.exit()
        error = self.pipe.send_command(f'SETPOSY{y}')
        if error > 0:
            print("Error: rel_move " + str(error))
            sys.exit()
        else:
            if not silent:
                print(f"Moved by {dx}, {dy} (Rel)")
            return True
