import random, sys, time
import spidev
import RPi.GPIO as GPIO 
from periphery import SPI
from functools import reduce
from math import log,ceil

i_f = 10_000_000 #10MHz

fp_out = None

API_CS1 = 22 # GPIO22,  

l_command_ident = [0x01, 0x00, 0x00, 0x00]
l_command_bist  = [0xff, 0x00, 0x00, 0x00] #pv-2024-03-13: 0x80 for SGA
l_command_cr    = [0x03, 0x00, 0x08, 0x00]
l_command_cr_ek = [0x07, 0x00, 0x08, 0x00]
l_command_hcr    = [0x05, 0x00, 0x08, 0x00]
l_command_hcr_ek = [0x06, 0x00, 0x08, 0x00]

API_I_IDENT_PART1_START  =  5
API_I_IDENT_PART1_LENGTH = 16
API_I_IDENT_PART2_START  = 21 # API_I_IDENT_PART1_START + API_I_IDENT_PART1_LENGTH
API_I_IDENT_PART2_LENGTH = 16

API_I_IDENT_START        =  5
API_I_IDENT_LENGTH       = 32

API_I_CHAL_START         = 38 # API_I_IDENT_START       + API_I_IDENT_LENGTH        + 1
API_I_CHAL_LENGTH        = 32                                                       
                                                                                    
API_I_CHAL_PART1_START   = 38 # API_I_IDENT_START       + API_I_IDENT_LENGTH        + 1
API_I_CHAL_PART1_LENGTH  = 16                                                       
API_I_CHAL_PART2_START   = 54 # API_I_CHAL_PART1_START  + API_I_CHAL_PART1_LENGTH   
API_I_CHAL_PART2_LENGTH  = 16                                                       
                                                                                    
API_I_RESP_START         = 71 # API_I_CHAL_START        + API_I_CHAL_LENGTH         + 1
API_I_RESP_LENGTH        = 16                                                       
API_I_EK_START           = 87 # API_I_RESP_START        + API_I_RESP_LENGTH         
API_I_EK_LENGTH          = 16                                                       
                                                                                    
API_I_RWL_PART1_START    = 38 # API_I_IDENT_START       + API_I_IDENT_LENGTH        + 1
API_I_RWL_PART1_LENGTH   = 16
API_I_RWL_PART2_START    = 54 # API_I_RWL_PART1_START   + API_I_RWL_PART1_LENGTH
API_I_RWL_PART2_LENGTH   = 16

API_I_BIST               = 71

def gpio_setup():
    GPIO.setup(API_CS1, GPIO.OUT)   
    GPIO.output(API_CS1, GPIO.HIGH)

#spi
def spi_open():
    spi = spidev.SpiDev(0, 0) # bus, device
    spi.max_speed_hz = i_f 
    return spi
    
def spi_close(spi): spi.close()

def do_spi_transfer_l(l):
    GPIO.output(API_CS1, GPIO.LOW)
    
    spi = spi_open()
    l_r = spi.xfer(l) #xfer2
    spi_close(spi)
    
    GPIO.output(API_CS1, GPIO.HIGH)
    return l_r

#helper routines
def do_print_l(s, l, end = ''): 
    print(s, ' '.join('%02x' % e for e in l), end)
    s_out = s
    s_out = s_out + ' '.join('%02x' % e for e in l)
    s_out = s_out + '\n'

def list_invert(l): return [(~e)&0xFF for e in l]    
    
#assemble
def assemble_bist_l()         : return l_command_bist +[0]*68
def assemble_id_l()           : return l_command_ident + [0] + [0]*32
def assemble_cw_l(l_challenge): return l_command_cr    + [0] + l_challenge + [0] + [0]*49 # CR 65-16
def assemble_ek_l(l_challenge): return l_command_cr_ek + [0] + l_challenge + [0] + [0]*65 # CR_EK 65
def assemble_hcw_l(l_challenge): return l_command_hcr    + [0] + l_challenge + [0] + [0]*49 # CR 65-16
def assemble_hek_l(l_challenge): return l_command_hcr_ek + [0] + l_challenge + [0] + [0]*65 # CR_EK 65

# disassemble
def disassemble_l_bist(l_r):
    l_pcc_s       = l_r[API_I_IDENT_PART1_START : API_I_IDENT_PART1_START  + API_I_IDENT_PART1_LENGTH]                
    l_id_s        = l_r[API_I_IDENT_PART2_START : API_I_IDENT_PART2_START  + API_I_IDENT_PART2_LENGTH]                
    l_rw_s        = l_r[API_I_RWL_PART1_START : API_I_RWL_PART1_START  + API_I_RWL_PART1_LENGTH]                
    l_ek_s        = l_r[API_I_RWL_PART2_START : API_I_RWL_PART2_START  + API_I_RWL_PART2_LENGTH]                
    i_pass        = l_r[API_I_BIST]      
    b_pass = 1 if i_pass == 0x50 else 0
    return b_pass, l_pcc_s, l_id_s, l_rw_s, l_ek_s
    
def disassemble_l_id(l_r):
    l_pcc       = l_r[API_I_IDENT_PART1_START : API_I_IDENT_PART1_START  + API_I_IDENT_PART1_LENGTH]                
    l_id        = l_r[API_I_IDENT_PART2_START : API_I_IDENT_PART2_START  + API_I_IDENT_PART2_LENGTH]                
    return l_pcc, l_id
  
def disassemble_l_rw(l_r):
    l_pcc       = l_r[API_I_IDENT_PART1_START : API_I_IDENT_PART1_START  + API_I_IDENT_PART1_LENGTH]                
    l_id        = l_r[API_I_IDENT_PART2_START : API_I_IDENT_PART2_START  + API_I_IDENT_PART2_LENGTH]                
    l_rw        = l_r[API_I_RESP_START        : API_I_RESP_START         + API_I_RESP_LENGTH       ]          
    return l_pcc, l_id, l_rw

def disassemble_l_ek(l_r):
    l_pcc       = l_r[API_I_IDENT_PART1_START : API_I_IDENT_PART1_START  + API_I_IDENT_PART1_LENGTH]                
    l_id        = l_r[API_I_IDENT_PART2_START : API_I_IDENT_PART2_START  + API_I_IDENT_PART2_LENGTH]                
    l_ek        = l_r[API_I_EK_START          : API_I_EK_START           + API_I_EK_LENGTH         ]          
    return l_pcc, l_id, l_ek

def disassemble_l_rwek(l_r):
    l_pcc       = l_r[API_I_IDENT_PART1_START : API_I_IDENT_PART1_START  + API_I_IDENT_PART1_LENGTH]                
    l_id        = l_r[API_I_IDENT_PART2_START : API_I_IDENT_PART2_START  + API_I_IDENT_PART2_LENGTH]                
    l_rw        = l_r[API_I_RESP_START        : API_I_RESP_START         + API_I_RESP_LENGTH       ]  
    l_ek        = l_r[API_I_EK_START          : API_I_EK_START           + API_I_EK_LENGTH         ]                  
    return l_pcc, l_id, l_rw, l_ek

# do bist
def do_bist():
    l_r = do_spi_transfer_l(assemble_bist_l())    
    b_pass, l_pcc_s, l_id_s, l_rw_s, l_ek_s = disassemble_l_bist(l_r)    
    
    #do_print_l_fp(l_pcc_s)
    #do_print_l_fp(l_id_s)
    #do_print_l_fp(l_rw_s)
    #do_print_l_fp(l_ek_s)
    
    return b_pass, l_pcc_s, l_id_s, l_rw_s, l_ek_s

# get TID only
def get_tid():
    l_r = do_spi_transfer_l(assemble_id_l())
    l_pcc, l_id = disassemble_l_id(l_r)
    l_tid = l_pcc + l_id
    s_pcc = ''.join('%02x' % e for e in l_pcc)
    s_id = ''.join('%02x' % e for e in l_id)
    s_tid = s_pcc + s_id
    return s_tid

#get RW only
def do_token_auth(cw_l):
    l_r = do_spi_transfer_l(assemble_cw_l(cw_l))    
    l_pcc, l_id, l_rw = disassemble_l_rw(l_r)
    s_rw = ''.join('%02x' % e for e in l_rw)
    return s_rw

def do_host_auth(hcw_l):
    l_r = do_spi_transfer_l(assemble_hcw_l(hcw_l))
    l_pcc, l_id, l_hrw = disassemble_l_rw(l_r)
    s_hrw = ''.join('%02x' % e for e in l_hrw)
    return s_hrw

#get RW and EK
def do_token_auth_ek(cw_l):
    l_r = do_spi_transfer_l(assemble_ek_l(cw_l))    
    l_pcc, l_id, l_rw, l_ek = disassemble_l_rwek(l_r)        
    s_rw = ''.join('%02x' % e for e in l_rw)
    s_ek = ''.join('%02x' % e for e in l_ek)
    return s_rw, s_ek

def do_host_auth_ek(hcw_l):
    l_r = do_spi_transfer_l(assemble_hek_l(hcw_l))
    l_pcc, l_id, l_hrw, l_ek = disassemble_l_rwek(l_r)
    s_hrw = ''.join('%02x' % e for e in l_hrw)
    s_ek = ''.join('%02x' % e for e in l_ek)
    return s_hrw, s_ek
