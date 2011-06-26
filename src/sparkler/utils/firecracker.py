#!/usr/bin/python

#-----------------------------------------------------------
# X10 Firecracker CM17A Interface
#
# Copyright (c) 2010 Collin J. Delker
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
#-----------------------------------------------------------
#
# NOTES:
#   This software requires the pySerial python module:
#   http://pyserial.sourceforge.net/
#
#   Commands can be sent from the command line or from
#   python scripts by calling send_command().
#
#   X10 Firecracker CM17A protocol specificaiton:
#   ftp://ftp.x10.com/pub/manuals/cm17a_protocol.txt
#
#-----------------------------------------------------------

import serial
import time
import sys

#-----------------------------------------------------------
# Firecracker spec requires at least 0.5ms between bits
#-----------------------------------------------------------
DELAY_BIT = 0.001 # Seconds between bits
DELAY_FIN = 1     # Seconds to wait before disabling after transmit

#-----------------------------------------------------------
# House and unit code table
#-----------------------------------------------------------
HOUSE_LIST = [
   0x6000, # a
   0x7000, # b
   0x4000, # c
   0x5000, # d
   0x8000, # e
   0x9000, # f
   0xA000, # g
   0xB000, # h
   0xE000, # i
   0xF000, # j
   0xC000, # k
   0xD000, # l
   0x0000, # m
   0x1000, # n
   0x2000, # o
   0x3000  # p
   ]

UNIT_LIST = [
  0x0000, # 1
  0x0010, # 2
  0x0008, # 3
  0x0018, # 4
  0x0040, # 5
  0x0050, # 6
  0x0048, # 7
  0x0058, # 8
  0x0400, # 9
  0x0410, # 10
  0x0408, # 11
  0x0400, # 12
  0x0440, # 13
  0x0450, # 14
  0x0448, # 15
  0x0458  # 16
  ]
MAX_UNIT = 16
    
#-----------------------------------------------------------
# Command Code Masks
#-----------------------------------------------------------
CMD_ON   = 0x0000
CMD_OFF  = 0x0020
CMD_BRT  = 0x0088
CMD_DIM  = 0x0098

#-----------------------------------------------------------
# Data header and footer
#-----------------------------------------------------------
DATA_HDR = 0xD5AA
DATA_FTR = 0xAD

#-----------------------------------------------------------
# Put firecracker in standby
#-----------------------------------------------------------
def set_standby(s):
    s.setDTR(True)
    s.setRTS(True)
    
#-----------------------------------------------------------
# Turn firecracker "off"
#-----------------------------------------------------------
def set_off(s):
    s.setDTR(False)
    s.setRTS(False)

#-----------------------------------------------------------
# Send data to firecracker
#-----------------------------------------------------------
def send_data(s, data, bytes):
    mask = 1 << (bytes - 1)
    
    set_standby(s)
    time.sleep(DELAY_BIT)    

    for i in range(bytes):
        bit = data & mask        
        if bit == mask:
            s.setDTR(False)
        elif bit == 0:
            s.setRTS(False)

        time.sleep(DELAY_BIT)
        set_standby(s)
        
        # Then stay in standby at least 0.5ms before next bit
        time.sleep(DELAY_BIT)

        # Move to next bit in sequence
        data = data << 1
    
#-----------------------------------------------------------
# Generate the command word
#-----------------------------------------------------------
def build_command(house, unit, action):
    cmd = 0x00000000    
    house_int = ord(house.upper()) - ord('A')

    #-------------------------------------------------------
    # Add in the house code
    #-------------------------------------------------------
    if house_int >= 0 and house_int <= ord('P') - ord('A'):
        cmd = cmd | HOUSE_LIST[ house_int ]
    else:
        print "Invalid house code ", house, house_int
        return
        
    #-------------------------------------------------------
    # Add in the unit code. Ignore if bright or dim command,
    # which just applies to last unit.
    #-------------------------------------------------------
    if unit > 0 and unit < MAX_UNIT:
        if action.upper() != 'BRT' and action.upper() != 'DIM':
            cmd = cmd | UNIT_LIST[ unit - 1 ]
    else:
        print "Invalid Unit Code", unit
        return

    #-------------------------------------------------------
    # Add the action code
    #-------------------------------------------------------
    if action.upper() == 'ON':
        cmd = cmd | CMD_ON
    elif action.upper() == 'OFF':
        cmd = cmd | CMD_OFF
    elif action.upper() == 'BRT':
        cmd = cmd | CMD_BRT
    elif action.upper() == 'DIM':
        cmd = cmd | CMD_DIM
    else:
        print "Invalid Action Code", action
        return
    
    return cmd

#-----------------------------------------------------------
# Send Command to Firecracker
#   portname: Serial port to send to
#   house:    house code, character 'a' to 'p'
#   unit:     unit code, integer 1 to 16
#   action:   string 'ON', 'OFF', 'BRT' or 'DIM'
#-----------------------------------------------------------
def send_command( portname, house, unit, action ):
    cmd = build_command( house, unit, action )
    if cmd != None:
        try:
            s = serial.Serial(portname)
            send_data( s, DATA_HDR, 16 ) # Send data header
            send_data( s, cmd, 16 )      # Send data
            send_data( s, DATA_FTR, 8 )  # Send footer
            time.sleep( DELAY_FIN )      # Wait for firecracker to finish transmitting
            set_off(s)                   # Shut off the firecracker
            s.close()
            return True

        except serial.SerialException:
            print 'ERROR opening serial port', portname
            return False
            
#-----------------------------------------------------------
# Main Program Entry
#-----------------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) < 4:
        print "USAGE:  python firecracker.py house unit action [port]"
        print "   house  = [a,p]"
        print "   unit   = [0,16]"
        print "   action = (ON, OFF, BRT, DIM)"
        print "   port   = serial port (e.g. COM1 or /dev/tty.usbserial)"
        quit()
        
    house = sys.argv[1]
    unit = int(sys.argv[2])
    action = sys.argv[3]

    try:
        portname = sys.argv[4]
    except:
        #-------------------------------------------------------
        # REPLACE portname with the default serial port your
        # firecracker is connected to. In Windows, this could
        # be "COM1" etc. On Mac/Unix, this will be 
        # '/dev/tty.something'. With my usb-to-serial adapter,
        # it shows up as '/dev/tty.usbserial'. To find available
        # ports, type 'ls /dev/tty.*' at the terminal prompt.
        #-------------------------------------------------------
        portname = '/dev/tty.usbserial'

    send_command( portname, house, unit, action )
    