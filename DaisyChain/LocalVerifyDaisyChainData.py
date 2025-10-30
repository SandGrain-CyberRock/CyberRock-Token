import argparse, os, json
import RPi.GPIO as GPIO 
import random, sys, time, requests
from periphery import SPI
from functools import reduce
from math import log,ceil
import hashlib

sys.path.insert(1, '/home/pi/SandGrain/SandGrainSuite_DeviceAPI/')

import CyberRock_Cloud as cloud
import CyberRock_Token as token
import SandGrain_Credentials as credentials

def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    token.gpio_setup()

def listToInt(lst):
    """Convert a byte list into a number"""
    return reduce(lambda x,y:(x<<8)+y,lst)

def intToList(number):
    """Converts an integer of any length into an integer list"""
    L1 = log(number,256)
    L2 = ceil(L1)
    if L1 == L2:
        L2 += 1
    return [(number&(0xff<<8*i))>>8*i for i in reversed(range(L2))] 
 
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename (without extension)")
    args = parser.parse_args()    
    s_datafile =  args.filename + ".json"

    GPIO.setwarnings(False)
    gpio_setup()

    with open(s_datafile, 'r') as openfile:
 
        # Reading from json file
        filedata = json.load(openfile)
    
    tid = filedata["TID"]
    hcw1 = filedata["HCW1"]
    data1 = filedata["data1"]
    data2 = filedata["data2"]
    claimed_hrw3 = filedata["HRW3"]
    
    iotaccesstoken, iotid = cloud.do_device_login(credentials.cloudflaretokens, credentials.iotusername, credentials.iotpassword)

# get HRW1
    transactionid = cloud.do_device_requestHRWtransactionid(credentials.cloudflaretokens, iotaccesstoken, tid, hcw1)
    HRW1transactionID = cloud.do_device_requestHRW(credentials.cloudflaretokens, iotaccesstoken, tid, hcw1, transactionid)
    result, hrw1 = cloud.do_device_requestHRWstatus(credentials.cloudflaretokens, iotaccesstoken, HRW1transactionID)

# get HRW2
    hcw2 = hrw1 + data1
    transactionid = cloud.do_device_requestHRWtransactionid(credentials.cloudflaretokens, iotaccesstoken, tid, hcw2)
    HRW2transactionID = cloud.do_device_requestHRW(credentials.cloudflaretokens, iotaccesstoken, tid, hcw2, transactionid)
    result, hrw2 = cloud.do_device_requestHRWstatus(credentials.cloudflaretokens, iotaccesstoken, HRW2transactionID)

# get HRW3
    hcw3 = hrw2 + data2
    transactionid = cloud.do_device_requestHRWtransactionid(credentials.cloudflaretokens, iotaccesstoken, tid, hcw3)
    HRW3transactionID = cloud.do_device_requestHRW(credentials.cloudflaretokens, iotaccesstoken, tid, hcw3, transactionid)
    result, hrw3 = cloud.do_device_requestHRWstatus(credentials.cloudflaretokens, iotaccesstoken, HRW3transactionID)


    if (hrw3 == claimed_hrw3):
        print("Daisy Chain authenticated")
    else:
        print("Daisy Chain not authentic!")

    print('\n')   
    
main()    
