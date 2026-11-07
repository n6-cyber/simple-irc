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
    
    clients = {}

    sel = selectors.DefaultSelector()

    # checks host type against known ip addr types
    if host_type == IPv4Address:
        server = socket.create_server((host, port), family = socket.AF_INET, backlog = 2)
        print("Server is up!!")
    else:
        server = socket.create_server((host, port), family = socket.AF_INET6, backlog = 2)
        print("Server is up!!") 
    
    # accept username/general accept function
    def accept(sock, mask):
        # appends new connection
        conn, addr = sock.accept()
        print("A Client has connected")

        # recieves usernames
        username = conn.recv(1024)
        username = username.decode(encoding="ascii", errors="xmlcharrefreplace")

        if username not in clients.values():
            clients[conn] = username
            conn.sendall(b"GOOD")

            conn.setblocking(False)
            sel.register(conn, selectors.EVENT_READ, read_msg)
        else:
            print(username)
            conn.sendall(b"TAKEN")

    def read_msg(conn, mask):
        msg = conn.recv(16384)
        if msg:

            user = clients.get(conn)
            user = user.encode(encoding="ascii", errors="xmlcharrefreplace")

            for client in clients.keys():
                if client != conn:
                    client.sendall(user + msg)

        else:
            print("A client has disconnected")
            sel.unregister(conn)
            conn.close()
            clients.pop(conn, None)

    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, accept)

    print(f"\nWaiting to connect...")

    while True:
        events = sel.select()
        for log, mask in events:
            callback = log.data
            callback(log.fileobj, mask)

   
# bunch of error handling (idk why im leaving comments anymore)
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
