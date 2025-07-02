import time
import sys
import win32pipe, win32file, pywintypes
import re

# Record start time
start_time = time.time()
# Counter for None/empty responses
none_count = 0

class PipeClient:
    def __init__(self, pipe_name=r'\\.\pipe\HQ_server'):
        self.pipe_name = pipe_name
        self.handle = None
        self.connected = False

    def connect(self):
        """Establish connection to the named pipe"""
        try:
            self.handle = win32file.CreateFile(
                self.pipe_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            res = win32pipe.SetNamedPipeHandleState(self.handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            self.connected = True
            print("Connected to pipe server")
            return True
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("No pipe found, waiting for server...")
                time.sleep(1)
            else:
                print(f"Connection error: {e}")
            return False

    def send_command(self, command):
        """Send a command and receive response"""
        if not self.connected:
            if not self.connect():
                return None

        try:
            # Send the command
            print(f"Sending command: {command}")
            input_data = str.encode(command + '\n')
            win32file.WriteFile(self.handle, input_data)

            # Read the response
            result, resp = win32file.ReadFile(self.handle, 64*1024)
            msg = resp.decode("utf-8")
            print(f"Received: {msg.strip()}")

            return msg
        except pywintypes.error as e:
            print(f"Error during communication: {e}")
            self.disconnect()
            self.connect()  # Try to reconnect
            return None

    def disconnect(self):
        """Close the connection"""
        if self.handle:
            win32file.CloseHandle(self.handle)
            self.handle = None
            self.connected = False
            print("Disconnected from pipe server")

def get_first_double(my_string):
    if my_string is None:
        global none_count
        none_count += 1
        return 0

    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)
    # Check if there are any matches
    matches = rx.findall(my_string)
    if not matches:
        # No numeric values found
        none_count += 1
        return 0
    var = matches[0]
    return float(var)