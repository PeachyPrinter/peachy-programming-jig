#!/usr/bin/python
import subprocess
import serial
import usb
import csv
import datetime
#from usbid.usbinfo import USBINFO


class PeachyProgrammer():
    PEACHY_VENDORID=5840
    PEACHY_PRODUCTID=2803
    ST_VENDORID=1155
    PROGRAMMER_PRODUCTID=14152
    BOOTLOADER_PRODUCTID=57105

    def __init__(self):
        self.version=1.0
        print "Starting Peachy Programmer"
        self.usbs={
                'programmer_usb':False,
                'bootloader_usb':False,
                'arduino_usb':False,
                'peachy_usb':False}
        self.programmingState={
                'drips':False,
                'coil':False,
                'laser':False,
                'rebooted':False,
                'programmed':False,
                'error':'Success'}
        self.fid=open('PeachyProgramLog.csv','a')
        self.csv=csv.writer(self.fid)

    def openocdProgram(self):
        self.checkForUsbIds()
        if self.usbs['programmer_usb']==False:
            print "No programmer detected, check jig setup"
            self.programmingState['programmed']=False
            self.programmingState['error']='No Programmer Detected'
            return -1
        openocd_program='openocd -f stlink.cfg -c "program main.elf verify reset exit"'
        program_return = subprocess.call(openocd_program, shell=True)
        if program_return:
            print "Programming failed, check jig setup (power to Peachy board?)"
            self.programmingState['programmed']=False
            self.programmingState['error']='Programming Failed'
            return -1
        self.programmingState['programmed']=True
        return 0

    def checkForUsbIds(self):
        busses = usb.busses()
        self.usbs['programmer_usb']=False
        self.usbs['bootloader_usb']=False
        self.usbs['peachy_usb']=False
        for bus in busses:
            devices = bus.devices
            for dev in devices:
                if (dev.idVendor==self.PEACHY_VENDORID)&(dev.idProduct==self.PEACHY_PRODUCTID):
                    self.usbs['peachy_usb']=True
                elif (dev.idVendor==self.ST_VENDORID)&(dev.idProduct==self.BOOTLOADER_PRODUCTID):
                    self.usbs['bootloader_usb']=True
                elif (dev.idVendor==self.ST_VENDORID)&(dev.idProduct==self.PROGRAMMER_PRODUCTID):
                    self.usbs['programmer_usb']=True
        return

    def arduinoConnect(self):
        if self.usbs['arduino_usb']==False:
            pass
        return 0

    def logLine(self):
        date=datetime.datetime.now() 
        programmed=self.programmingState['programmed']
        laser=self.programmingState['laser']
        coil=self.programmingState['coil']
        drips=self.programmingState['drips']
        error=self.programmingState['error']
        line=[date,self.version,programmed,laser,coil,drips,error]
        self.csv.writerow(line)


    def fullTest(self):
        self.arduinoConnect()
        self.openocdProgram()
        self.logLine()



if __name__=="__main__":
    Prog=PeachyProgrammer()
    Prog.openocdProgram()
    Prog.logLine()
