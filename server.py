'''This is a simple IRC Chat Server, well more like its a chat / messaging client/server built in python,
used between 2 known users. It's not much of an IRC chat, more like E2E chat, but its def not 
as secure as any commercial or even opensource p2p / e2e chat app. So like it's just a lil project of mine 
I'm just playing around learning how things communicate over networks.
- made by n_6, as a side project lwk.'''

import socket
import ipaddress
import sys

host = input("Please set server ip: ")
port = int(input("Please set a server port: "))

server = socket.create_server((host, port), family = socket.AF_INET)

try:
    server.listen()

except socket.error as e:
    print(f"Bind failed: {e}")
    sys.exit()
