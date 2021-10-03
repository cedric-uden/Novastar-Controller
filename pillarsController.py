import socket
import sys
import binascii
import time
import os
from enum import Enum


def fade_in():

    global step_counter

    for i in range (0, step_counter - 1):
        line = all_left_panel_values[i][:-1]
        sock.sendall(bytearray.fromhex(line))
        line = all_right_panel_values[i][:-1]
        sock.sendall(bytearray.fromhex(line))
        time.sleep(fade_interval)


def fade_out():

    global step_counter

    for i in range (step_counter - 2, -1, -1):
        line = all_left_panel_values[i][:-1]
        sock.sendall(bytearray.fromhex(line))
        line = all_right_panel_values[i][:-1]
        sock.sendall(bytearray.fromhex(line))
        time.sleep(fade_interval)


def setCurrentFilePath():
    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    os.chdir(dir_name)

def setRunOptionOrError():
    try:
        return sys.argv[1]
    except:
        print("No Run Option defined. Please use run 'off' or 'on'.")

def connectToSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the ip
    server_address = ('192.168.0.78', 5200)
    # Connect to socket
    sock.connect(server_address)
    return sock


setCurrentFilePath()
TARGET_FADE_TIME = 2
runOption = setRunOptionOrError()

sock = connectToSocket()

class PowerOptionOn():
    def fade_action(self):
        fade_in()

class PowerOptionOff():
    def fade_action(self):
        fade_out()

class PowerOptions(Enum):
    OFF = PowerOptionOff
    ON = PowerOptionOn

    def fade_action(self):
        self.value.fade_action(self)


def main():
    try:
        PowerOptions[runOption].fade_action()
    finally:
        sock.close()



def readfileAndReturnContent(file):
    with open(file) as f:
        return f.readlines()

def determineFadeInterval():
    CommandOverheadDelayCompensator = 0.7
    return (TARGET_FADE_TIME / step_counter) * CommandOverheadDelayCompensator        

all_left_panel_values = readfileAndReturnContent("fader/left-pillar-fade-values.csv")
all_right_panel_values = readfileAndReturnContent("fader/right-pillar-fade-values.csv")

step_counter = len(all_left_panel_values)
fade_interval = determineFadeInterval()


# call the main function
main()
