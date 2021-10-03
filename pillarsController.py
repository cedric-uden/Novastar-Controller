import socket
import sys
import binascii

try:
    index = sys.argv[1]
except:
    print("que passa")

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set the ip
server_address = ('192.168.0.78', 5200)
# Connect to socket
sock.connect(server_address)

# The XX byte codes the brightness value (0-255) in HEX and T codes left pillar (4) and right pillar (5). 
# The other byte changes are not known to us ...
#                                  T                    XX
left_panel_off =   "55aa00c5fe000104ffff0100010000020100002059"
right_panel_off =  "55aa00c6fe000105ffff0100010000020100002259"

left_20_percent =  "55aa00dcfe000104ffff0100010000020100366d59"
right_20_percent = "55aa00ddfe000105ffff0100010000020100366f59"

left_30_percent =  "55aa0081fe000104ffff01000100000201004c2859"
right_30_percent = "55aa0082fe000105ffff01000100000201004c2a59"


try:
    
    # Send data
    if index == "off":
        sock.sendall(bytearray.fromhex(left_panel_off))
        sock.sendall(bytearray.fromhex(right_panel_off))

    elif index == "on":
        sock.sendall(bytearray.fromhex(left_30_percent))
        sock.sendall(bytearray.fromhex(right_30_percent))

    elif index == "test":
        sock.sendall(bytearray.fromhex(testing_hex))

finally:
    # Close socket
    sock.close()
