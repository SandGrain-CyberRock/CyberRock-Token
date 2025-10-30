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

    #Create same data set as used in creation
    data = {
        "name": filedata["name"],
        "TID": filedata["TID"],
        "date": filedata["date"]
    }
    
    tid = filedata["TID"]
    claimed_hrw = filedata["HRW"]
    
    hash_func = hashlib.new('sha256') 
    hash_func.update(str(data).encode('utf-8'))
    hcw = hash_func.hexdigest()

    iotaccesstoken, iotid = cloud.do_device_login(credentials.cloudflaretokens, credentials.iotusername, credentials.iotpassword)

    transactionid = cloud.do_device_requestHRWtransactionid(credentials.cloudflaretokens, iotaccesstoken, tid, hcw)

    HRWtransactionID = cloud.do_device_requestHRW(credentials.cloudflaretokens, iotaccesstoken, tid, hcw, transactionid)

    result, hrw = cloud.do_device_requestHRWstatus(credentials.cloudflaretokens, iotaccesstoken, HRWtransactionID)

    if (hrw == claimed_hrw):
        print("Sensor Data authenticated")
    else:
        print("Sensor Data not authentic!")

    print('\n')   
    
main()    
