import argparse, os, json
import RPi.GPIO as GPIO 
import random, sys, time, requests
from periphery import SPI
from functools import reduce
from math import log,ceil
import hashlib

sys.path.insert(1, '/home/pi/SandGrain/SandGrainSuite_DeviceAPI/')

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

    parser = argparse.ArgumentParser()
    parser.add_argument("chainvalue", help="Secure Boot chaining value")
    parser.add_argument("initialcw", help="initial CW value") 
    parser.add_argument("FW2hash", help="FW2 hash value")
    args = parser.parse_args()    
    s_chainvalue =  args.chainvalue
    s_initialcw = args.initialcw
    s_FW2hash =  args.FW2hash
    
    GPIO.setwarnings(False)
    gpio_setup()
    
    print("------------------------FW2--------------------------------")
    print("Chaining value received: ",s_chainvalue)
    print("Initial CW value received: ",s_initialcw)
    print("FW2Hash value received: ",s_FW2hash)

    print("Executing Level 2 Firmware functions\n")

    print("Verifying Level 3 Firmware\n")

    #Compute hash of next level firmware

    FW3hash = compute_file_hash(s_FirmwareLevelThreeFile)
    
    print("Calculated FW3 hash value: ",FW3hash)
        
    #XOR both hex stings to get CW
    
    cw = "".join(["%x" % (int(x, 16) ^ int(y, 16)) for (x, y) in zip(s_chainvalue[: len(FW3hash)], FW3hash)])

    rw = token.do_host_auth(intToList(int(cw,16)))

    attestationvalue = rw

    print("Intermediate RW2 value: ",rw)
    print("Starting Level 3 Firmware\n")
    
    os.system("python " + s_FirmwareLevelThreeFile + " " + attestationvalue + " " + s_initialcw + " " + s_FW2hash + " " + FW3hash)

main()
