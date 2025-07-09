import win32com.client, Drivers.PipeClient as PipeClient, time, sys
from Drivers.Interfaces.Microscope_Interface import MicroscopeDriverInterface


class MicroscopeDriver(MicroscopeDriverInterface):
    """
    an easy way to control the microscope
    """

    def __init__(self, cli: PipeClient.PipeClient):
        self.cli = cli
        
        self.set_default_values()

    def set_default_values(self):
        """Sets the Default values\n
        Lamp Volatge: 6.4V\n
        Aperture: 2.3\n <<< cant adjust aperture
        Auto focuses objective
        """
        self.lamp_on()
        self.set_lamp_voltage(6.4)
        self.set_mag(1)
        buf = 0
        """
        #self.cli.send_command("SETPOSF1.1")
        
        while(abs(PipeClient.get_first_double(self.cli.send_command("GETPOSF1.1")) - 1.1) > 0.1):
            time.sleep(1)
            buf += 1
            if buf > 20:
                print("focus error")
                break
        """
        self.cli.send_command("AUTFOC")
        f1 = 1
        f2 = 2
        f3 = 3
        while not (f1 == f2 and f2 == f3):
            f1 = PipeClient.get_first_double(self.cli.send_command("GETPOSF1.1"))
            time.sleep(1)
            f2 = PipeClient.get_first_double(self.cli.send_command("GETPOSF1.1"))
            time.sleep(1)
            f3 = PipeClient.get_first_double(self.cli.send_command("GETPOSF1.1"))
            time.sleep(1)
            buf += 1
            if buf > 20:
                print("focus error")
                break

    def get_microscope_object(self):
        return PipeClient.get_first_double(self.cli.send_command('GETOBJ'))

    def set_z_height(self, height):
        """
        Sets the Height in µm\n
        Only works if the AF is not on\n
        Has small protection by only setting height between 3500 and 6500 µm
            Need to add saftey checks to make sure things don't run into each other
        """
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

    def get_z_height(self):
        height = PipeClient.get_first_double(self.cli.send_command('GETZ'))
        return height

    def lamp_on(self):
        self.cli.send_command('LEDON')

    def lamp_off(self):
        self.pipe.send_command('LEDOFF')

    def rotate_nosepiece_forward(self):
        r = PipeClient.get_first_double(self.cli.send_command('GETPOSR'))
        new_r = r + 0.0
        self.cli.send_command(f"SETPOSR{new_r}")
        """ by how much should it rotate"""

    def rotate_nosepiece_backward(self):
        r = PipeClient.get_first_double(self.cli.send_command('GETPOSR'))
        new_r = r - 0.0
        self.cli.send_command(f"SETPOSR{new_r}")
        """ by how much should it rotate"""

    def set_lamp_voltage(self, voltage: float):
        self.cli.send_command(f'LEDPERCENT{voltage}')

    def set_mag(self, mag_idx: int):
        """
        Swaps the Position of the Nosepiece\n
        Automatically sets the Height\n
        1 : 2.5x 5500µm\n
        2 : 5x 4300µm\n
        3 : 20x 3930µm\n
        4 : 50x 3900µm\n
        5 : 100x 3900µm\n
        """
        if 0 < mag_idx < 6:
            self.cli.send_command(f'SETOBJ{mag_idx}')
        else:
            print(f"Wrong Mag Idx, you gave {mag_idx}, needs to be 1 to 5")

    def set_lamp_aperture_stop(self, aperture_stop: float):
        print("")
        """ no  aperture setting """

    def get_af_status(self):
        """
        Currently Bugged\n
        Return Codes:\n
        AfStatusUnknown     : -1\n
        AfStatusJustFocus   : 1\n
        AfStatusUnderFocus  : 2\n
        AfStatusOverFocus   : 3\n
        AfStatusOutOfRange  : 9
        """
        return 1; """ still need to find a way to figure out if a certain command is being performed """

    def is_af_searching(self):
        return -1; """ same as above ^^^ """

    def get_properties(self):
        """
        Returns the current properties of the microscope\n
        dict keys:
        'nosepiece' : positon of the nosepiece
        'aperture'  : current ApertureStop of the EpiLamp
        'voltage'   : current Voltage of the EpiLamp in Volts
        """
        val_dict = {"nosepiece" : 0, "aperture" : 0, "light" : 0}
        # height = self.micro.ZDrive.Value()
        #   File "C:\Users\Transfersystem User\.conda\envs\micro\lib\site-packages\win32com\client\dynamic.py", line 197, in __call__
        #     return self._get_good_object_(self._oleobj_.Invoke(*allArgs),self._olerepr_.defaultDispatchName,None)
        # pywintypes.com_error: (-2147352567, 'Exception occurred.', (0, 'Nikon.LvMic.ZDrive.1', '', None, 0, -2147352567), None)
        val_dict["nosepiece"] = str(PipeClient.get_first_double(self.cli.send_command('GETPOSR')))
        val_dict["aperture"] = "unknown"; """ no aperture on microscope """
        self.cli.send_command("LEDPERCENT50")
        val_dict["light"] = "50%" #PipeClient.get_first_double(self.cli.send_command('GETLED')); """ no get voltage command, GETLED is placeholder"""
        return val_dict

