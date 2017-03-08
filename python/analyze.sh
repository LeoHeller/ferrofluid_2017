#!/bin/bash
# set capability for this executable:
# sudo setcap cap_sys_rawio+ep $0
# sudo chmod g+w /dev/mem
/usr/bin/python3 /home/pi/py/analyze_rpio.py

