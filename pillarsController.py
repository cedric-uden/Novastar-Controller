import socket
import sys
import binascii
import time
import os


# set cwnd to the files directory
abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
os.chdir(dir_name)


try:
    index = sys.argv[1]
except:
    print("que passa")



##### SET THE TARGET FADE TIME
FADE_TIME = 2
##### SET THE TARGET FADE TIME


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set the ip
server_address = ('192.168.0.78', 5200)
# Connect to socket
sock.connect(server_address)


def main():
    try:
        if index == "off":
            fade_out()
        elif index == "on":
            fade_in()
        elif index == "test":
            sock.sendall(bytearray.fromhex(testing_hex))
    finally:
        sock.close()



# read a file and  return the content
def readfile(file):
    with open(file) as f:
        return f.readlines()
    f.close



# read the files
all_left_panel_values = readfile("fader/left-pillar-fade-values.csv")
all_right_panel_values = readfile("fader/right-pillar-fade-values.csv")

# set the counter of available steps to fade to and determine the fade interval
step_counter = len(all_left_panel_values)
# remove 30 percent to compensate other overhead delay
fade_interval = (FADE_TIME / step_counter) * 0.7


# copy pasta simple array access loops for both tables

def fade_in():
    for i in range (0, step_counter - 1):
        line = all_left_panel_values[i][:-1]
        sock.sendall(bytearray.fromhex(line))
        line = all_right_panel_values[i][:-1]
        sock.sendall(bytearray.fromhex(line))
        time.sleep(fade_interval)


def fade_out():
    for i in range (step_counter - 2, -1, -1):
        line = all_left_panel_values[i][:-1]
        sock.sendall(bytearray.fromhex(line))
        line = all_right_panel_values[i][:-1]
        sock.sendall(bytearray.fromhex(line))
        time.sleep(fade_interval)


# call the main function
main()
