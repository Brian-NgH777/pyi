#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import platform
import sys
from pathlib import Path
import requests
from datetime import datetime

oper = platform.system()
apiKey= "01fzm8bzzjpghaezax4df49yxy01fzm8cc0nqy899hpqrn38z6vdrosbtg7px9ty"

def getVendor(mac):
    vendor = {}
    url = "https://api.maclookup.app/v2/macs/%s?apiKey=%s"%(mac,apiKey)
    r = requests.get(url)
    if r.status_code == 200:
        vendor = r.json()
    return vendor


def scanMac():
    data = list()
    arp = subprocess.check_output(["arp", "-a"]).splitlines()
    for x in arp:
        oj = {}
        item = x.decode('utf-8')
        arr = item.split()
        oj["ip"] = arr[1].replace("(", "").replace(")", "")
        oj["mac"] = arr[3]
        oj["vendor"] = getVendor(arr[3])
        data.append(oj)

    # df= "'%s':%s" %(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),data)
    # log_text = '{}\n'.format(df)
    # pathFile = Path.cwd().joinpath('data-storage.log')
    # out_file = open(pathFile, "a") 
    # out_file.write(log_text)
    # out_file.close()

    return data

def scanWin():
    data = list()
    arp = subprocess.check_output(["arp", "-a"]).splitlines()
    for x in range(len(arp)):
        oj = {}
        if x == 0 or x == 1 or x == 2:
            continue
        item = arp[x].decode('utf-8')
        arr = item.split()
        oj["ip"] = arr[0]
        oj["mac"] = arr[1]
        oj["vendor"] = getVendor(arr[1])
        data.append(oj)

    # df= "'%s':%s" %(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),data)
    # log_text = '{}\n'.format(df)
    # pathFile = Path.cwd().joinpath('data-storage.log')
    # out_file = open(pathFile, "a") 
    # out_file.write(log_text)
    # out_file.close()
    return data

def scanLinux():
    data = list()
    arp = subprocess.check_output(["arp", "-a"]).splitlines()
    for x in range(len(arp)):
        oj = {}
        item = arp[x].decode('utf-8')
        arr = item.split()
        oj["ip"] = arr[1].replace("(", "").replace(")", "")
        oj["mac"] = arr[3]
        oj["vendor"] = getVendor(arr[3])
        data.append(oj)

    # df= "'%s':%s" %(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),data)
    # log_text = '{}\n'.format(df)
    # pathFile = Path.cwd().joinpath('data-storage.log')
    # out_file = open(pathFile, "a") 
    # out_file.write(log_text)
    # out_file.close()

    return data

if (oper == "Windows"):
    print(scanWin())
else :
    print(scanMac())
sys.stdout.flush()