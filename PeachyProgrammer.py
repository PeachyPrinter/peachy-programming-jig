#!/usr/bin/python
import subprocess
import serial
import usb
#from usbid.usbinfo import USBINFO


class PeachyProgrammer():
    PEACHY_VENDORID=5840
    PEACHY_PRODUCTID=2803
    ST_VENDORID=1155
    PROGRAMMER_PRODUCTID=14152
    BOOTLOADER_PRODUCTID=57105

    def __init__(self):
        print "Starting Peachy Programmer"
        self.usbs={
                'programmer_usb':False,
                'bootloader_usb':False,
                'arduino_usb':False,
                'peachy_usb':False}
        self.programmingState={
                'programmed':False}

    def openocdProgram(self):
        self.checkForUsbIds()
        if self.usbs['programmer_usb']==False:
            print "No programmer found"
            return
        openocd_program='openocd -f stlink.cfg -c "program main.elf verify reset exit"'
        program_return = subprocess.call(openocd_program, shell=True)
        if program_return:
            print "Programming Failed"
            self.programmingState['programmed']=False
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


    def start(self):
        self.arduinoConnect()
        self.openocdProgram()

class ProgramLogger(self):
    def __init__(self):
        pass


    def arduinoConnect(self):
        print "Connecting to Arduino Monitor"
        self.usbs['arduino_usb']=False
        return 0


if __name__=="__main__":
    Prog=PeachyProgrammer()
    Prog.openocdProgram()
