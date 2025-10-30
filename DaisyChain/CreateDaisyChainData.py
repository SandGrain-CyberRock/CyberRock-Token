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

    # Data to be written
    # Three levels of data in this example
    curr = time.time()
    curr_time = time.strftime("%a %d %b %Y %H %M %S", time.gmtime(curr))

    hash_func = hashlib.new('sha256') 
    hash_func.update(str(curr_time).encode('utf-8'))
    data1 = hash_func.hexdigest()[0:32]
    hash_func.update(str(curr_time).encode('utf-8'))
    data2 = hash_func.hexdigest()[0:32]
    hash_func.update(str(curr_time).encode('utf-8'))
    hcw1 = hash_func.hexdigest()

    GPIO.setwarnings(False)
    gpio_setup()

    tid = token.get_tid()

    data = {
        "name": s_datafile,
        "TID": tid,
        "HCW1": hcw1,
        "data1": data1,
        "data2": data2
        }

    hrw1 = token.do_host_auth(intToList(int(hcw1,16)))

    hcw2 = hrw1 + data1
    hrw2 = token.do_host_auth(intToList(int(hcw2,16)))

    hcw3 = hrw2 + data2
    hrw3 = token.do_host_auth(intToList(int(hcw3,16)))

    data["HRW3"] = hrw3

    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Writing
    with open(s_datafile, "w") as outfile:
        outfile.write(json_object)

    print(json.dumps(data, indent=4))    
    print('\n')   
    
main()    
