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
    #parser.add_argument("downloadfilename", help="download data filename")
    parser.add_argument("jsonfilename", help="JSON filename (without extension)")
    args = parser.parse_args()    
    #s_downloaddatafile =  args.downloadfilename
    s_jsondatafile =  args.jsonfilename + ".json"

    GPIO.setwarnings(False)
    gpio_setup()

    tid_l = token.get_tid()

    with open(s_jsondatafile, 'r') as openfile:
        # Reading from json file
        jsonfiledata = json.load(openfile)
    
    s_downloaddatafile = jsonfiledata["downloadname"]
    filehash = compute_file_hash(s_downloaddatafile)
    
    #Create same data set as used in creation        
    data = {
        "downloadname": jsonfiledata["downloadname"],
        "filehash": filehash,
        "JSONname": jsonfiledata["JSONname"],
        "TID": jsonfiledata["TID"],
        "date": jsonfiledata["date"]
    }
    
    hrw = jsonfiledata["HRW"]
    
    hash_func = hashlib.new('sha256') 
    hash_func.update(str(data).encode('utf-8'))
    hcw = hash_func.hexdigest()

    hrw_l = token.do_host_auth(intToList(int(hcw,16)))
    
    securedownloadresult = True
    
    if (jsonfiledata["downloadname"] == s_downloaddatafile):
        print("Downloaded Filename matches")
    else:
        print("Downloaded Filename does not match!")
        securedownloadresult = False
    
    if (jsonfiledata["JSONname"] == s_jsondatafile):
        print("JSON Filename matches")
    else:
        print("JSON Filename does not match!")
        securedownloadresult = False
        
    if (jsonfiledata["TID"] == tid_l):
        print("TID matches")
    else:
        print("TID does not match!")
        securedownloadresult = False

    if (jsonfiledata["filehash"] == filehash):
        print("File hash matches")
    else:
        print("File hash does not match!")
        securedownloadresult = False

    if (hrw == hrw_l):
        print("Authentication tag matches")
    else:
        print("Authentication tag does not match!")
        securedownloadresult = False
        
    if securedownloadresult == True:
        print("Secure download successful")   
    else:
        print("Secure download failed!")   
    
main()    
