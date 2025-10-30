import argparse, os, json
import RPi.GPIO as GPIO 
import random, sys, time, requests
from periphery import SPI
from functools import reduce
from math import log,ceil
import hashlib

sys.path.insert(1, '/home/pi/SandGrain/SandGrainSuite_DeviceAPI/')

s_initialcwfilename = 'initialcw.json'

import CyberRock_Cloud as cloud
import CyberRock_Token as token
import SandGrain_Credentials as credentials

s_FirmwareLevelTwoFile = 'FirmwareLevel2.py'

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
    
    print("------------------------FW1--------------------------------")

    print("Executing Level 1 Firmware functions")

    print("Verifying Level 2 Firmware")

    #Read Initial CW0
    
    with open(s_initialcwfilename, 'r') as openfile:
        # Reading from json file
        initialcwdata = json.load(openfile)
        
    initialcw = initialcwdata['CW0']
    
    print("Initial CW value: ",initialcw)

    #Compute hash of next level firmware

    FW2hash = compute_file_hash(s_FirmwareLevelTwoFile)

    print("Calculated FW2 hash value: ",FW2hash)

    #XOR both hex stings to get CW
    
    cw = "".join(["%x" % (int(x, 16) ^ int(y, 16)) for (x, y) in zip(initialcw[: len(FW2hash)], FW2hash)])

    rw1 = token.do_host_auth(intToList(int(cw,16)))

    nextchainvalue = rw1 + rw1

    print("Intermediate RW1 value: ",rw1)
    print("Starting Level 2 Firmware\n")

    os.system("python " + s_FirmwareLevelTwoFile + " " + nextchainvalue + " " + initialcw + " " + " " + FW2hash)

    
main()    
