import argparse, os, json
import RPi.GPIO as GPIO 
import random, sys, time, requests
from periphery import SPI
from functools import reduce
from math import log,ceil
import hashlib

sys.path.insert(1, '/home/pi/SandGrain/SandGrainSuite_DeviceAPI/')

s_manifestfilename = 'manifest.json'

s_FirmwareLevelTwoFile = 'FirmwareLevel2.py'
s_FirmwareLevelThreeFile = 'FirmwareLevel3.py'

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

    FW2hash = compute_file_hash(s_FirmwareLevelTwoFile)
    FW3hash = compute_file_hash(s_FirmwareLevelThreeFile)

    data = {
        "FW2hash": FW2hash,
        "FW3hash": FW3hash,
    }
    
    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Writing
    with open(s_manifestfilename, "w") as outfile:
        outfile.write(json_object)

    print(json.dumps(data, indent=4))    
    print('\n')   
    
main()    
