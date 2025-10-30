import argparse, os, json
import RPi.GPIO as GPIO 
import random, sys, time, requests
from periphery import SPI
from functools import reduce
from math import log,ceil
import hashlib

sys.path.insert(1, '/home/pi/SandGrain/SandGrainSuite_DeviceAPI/')

s_attestationfilename = 'attestationvalue.json'
s_manifestfilename = 'manifest.json'

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

def compute_file_hash(file_path, algorithm='sha256'):
    """Compute the hash of a file using the specified algorithm."""
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as file:
        # Read the file in chunks of 8192 bytes
        while chunk := file.read(8192):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()
     
def main():

    GPIO.setwarnings(False)
    gpio_setup()

    with open(s_attestationfilename, 'r') as openfile:
        # Reading from json file
        jsonfiledata = json.load(openfile)

    #Read attestation data set             
    tid = jsonfiledata["TID"]
    initialcw = jsonfiledata["initialcw"]   
    FW2hash = jsonfiledata["FW2hash"]
    FW3hash = jsonfiledata["FW3hash"]
    attestationvalue = jsonfiledata["attestationvalue"]    

# Check Manifest file

    with open(s_manifestfilename, 'r') as openfile:
        # Reading from json file
        manifestfiledata = json.load(openfile)

    manifestok = True
    print("\nSecure Boot: checking file manifest\n")

    if (FW2hash == manifestfiledata["FW2hash"]):
        print("Secure Boot: Firmware level 2 file hash correct")
    else:
        manifestok = False
        print("Secure Boot: Firmware level 2 file hash incorrect!")
        
    if (FW3hash == manifestfiledata["FW3hash"]):
        print("Secure Boot: Firmware level 3 file hash correct")
    else:
        manifestok = False
        print("Secure Boot: Firmware level 3 file hash incorrect!")

    if manifestok:

    # Login to CyberRock
        iotaccesstoken, iotid = cloud.do_device_login(credentials.cloudflaretokens, credentials.iotusername, credentials.iotpassword)

    # Retrieve first level result
        print("\nSecure Boot: retrieving first level result\n")
        cw1 = "".join(["%x" % (int(x, 16) ^ int(y, 16)) for (x, y) in zip(initialcw[: len(FW2hash)], FW2hash)])

        transactionid = cloud.do_device_requestHRWtransactionid(credentials.cloudflaretokens, iotaccesstoken, tid, cw1)

        RWtransactionID = cloud.do_device_requestHRW(credentials.cloudflaretokens, iotaccesstoken, tid, cw1, transactionid)

        result, rw1 = cloud.do_device_requestHRWstatus(credentials.cloudflaretokens, iotaccesstoken, RWtransactionID)

        rw1l = rw1 + rw1
        
    # Check second level result
        print("\nSecure Boot: checking last (second) level result\n")
        cw2 = "".join(["%x" % (int(x, 16) ^ int(y, 16)) for (x, y) in zip(rw1l[: len(FW3hash)], FW3hash)])

        result = cloud.do_device_priorityhostauth(credentials.cloudflaretokens, iotaccesstoken, tid, cw2, attestationvalue)

        if (result == "AUTH_OK"):
            print("\nSecure Boot attestation value authenticated")
        else:
            print("\nSecure Boot failed!")
    else:
        print("\nSecure Boot failed!")
    
main()    
