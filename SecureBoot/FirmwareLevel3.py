import argparse, os, json
import RPi.GPIO as GPIO 
import random, sys, time, requests
from periphery import SPI
from functools import reduce
from math import log,ceil
import hashlib

sys.path.insert(1, '/home/pi/SandGrain/SandGrainSuite_DeviceAPI/')

s_jsondatafile = 'attestationvalue.json'
s_initialcwfilename = 'initialcw.json'

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
    parser.add_argument("attestationvalue", help="Secure Boot attestation value")
    parser.add_argument("initialcw", help="initial CW value")    
    parser.add_argument("FW2hash", help="FW2 hash value")
    parser.add_argument("FW3hash", help="FW3 hash value")
    args = parser.parse_args()    
    s_attestationvalue =  args.attestationvalue
    s_initialcw = args.initialcw
    s_FW2hash =  args.FW2hash
    s_FW3hash =  args.FW3hash
    
    GPIO.setwarnings(False)
    gpio_setup()

    print("------------------------FW3--------------------------------")

    print("Received attestation value: ", s_attestationvalue)
    print("Initial CW value received: ",s_initialcw)
    print("FW2Hash value received: ",s_FW2hash)
    print("FW3Hash value received: ",s_FW3hash)
        
    print("Saving Attestation value\n")
    
    tid = token.get_tid()    
    
    data = {
        "TID": tid,
        "initialcw": s_initialcw,    
        "FW2hash": s_FW2hash,
        "FW3hash": s_FW3hash,
        "attestationvalue": s_attestationvalue
    }
    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Writing
    with open(s_jsondatafile, "w") as outfile:
        outfile.write(json_object)

    print(json.dumps(data, indent=4))    
    print('\n')  

    print("Generate/retrieve new initial CW value\n")

#Create new initial CW locally
    hash_func = hashlib.new('sha256') 
    hash_func.update(str(data).encode('utf-8'))
    newinitialcw = hash_func.hexdigest()

    cw0data = { "CW0": newinitialcw }
    
    # Serializing json
    cw0json_object = json.dumps(cw0data, indent=4)

    # Writing
    with open(s_initialcwfilename, "w") as outfile:
        outfile.write(cw0json_object)

    print(json.dumps(cw0data, indent=4))    
    print('\n')  

    print("Executing Level 3 Firmware functions\n")

main()
