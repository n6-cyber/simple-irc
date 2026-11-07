'''This is a simple IRC Chat Server, well more like its a chat / messaging client/server built in python,
used between 2 known users. It's not much of an IRC chat, more like E2E chat, but its def not 
as secure as any commercial or even opensource p2p / e2e chat app. So like it's just a lil project of mine 
I'm just playing around learning how things communicate over networks.
- made by n_6, as a side project lwk.'''

import socket
from ipaddress import ip_address, IPv4Address, IPv6Address
import sys
import builtins
import selectors

try:
    
    host = input("Please set server ip: ")
    port = int(input("Please set a server port: "))
    
    host_type = type(ip_address(host))

    # usernames moved up for easier reach tbh
    connections = []
    usernames = []

    sel = selectors.DefaultSelector()
    
    # checks host type against known ip addr types
    if host_type == IPv4Address:
        server = socket.create_server((host, port), family = socket.AF_INET, backlog = 2)
        print("Server is up!!")
    else:
        server = socket.create_server((host, port), family = socket.AF_INET6, backlog = 2)
        print("Server is up!!")
    
    print(f"\nWaiting to connect...")

    # removed username code temp, working on a function instead
    while True:
        pass
        
    
except OSError as e:
    print(f"Could not create server {e}")
    sys.exit(1)
except KeyboardInterrupt as e:
    print("\nKeyboard Interrupt detected, shutting down server")
    sys.exit()
except ValueError as e:
    print(f"The above IP does not seem to be a valid IPv4 or IPv6, IP address please try again.")
    sys.exit(1)
except builtins.ConnectionRefusedError:
    print(f"Connection Refused, it maybe down, or doesn't exist")
    sys.exit(1)
