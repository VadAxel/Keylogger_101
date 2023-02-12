# Keylogger_101

kelogger_101

Requirements:

python 3, sys, subprocess

Functions:

* on_tryck : actions if key is pressed
* on_slapp : actions if key is released
* write_file : write to file with options
* run_ncat : uses ncat for reverse shell

Notes:

* Replace os.system('ncat <command>') with your corresponding IP & Port
* Variables need weird names to not get detected
* Use base64 or similar when exec

Future features:

* Auto exec (.exe)

