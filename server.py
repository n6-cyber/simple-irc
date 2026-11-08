'''This is a simple IRC Chat Server, well more like its a chat / messaging client/server built in python,
used between 2 known users. It's not much of an IRC chat, more like E2E chat, but its def not 
as secure as any commercial or even opensource p2p / e2e chat app. So like it's just a lil project of mine 
I'm just playing around learning how things communicate over networks.
- made by n_6, as a side project lwk.'''

import socket
from ipaddress import ip_address, IPv4Address, IPv6Address
import sys
import selectors
import mimetypes
import hashlib
import datetime
from collections import deque

try:
    
    # colors
    RESET = "\033[0m"
    BOLD = "\033[1m"

    RED = "\033[31m"
    YELLOW = "\033[33m"
    ORANGE = "\033[38;5;208m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    PINK = "\033[38;5;213m"
    GREY = "\033[90m"
    BLACK = "\033[30m"
    WHITE = "\033[37m"

    host = input(f"{GREEN}Please set server ip:{RESET} ")
    port = int(input(f"{GREEN}Please set a server port:{RESET} "))
    
    host_type = type(ip_address(host))
    
    history = deque(maxlen=50)

    clients = {}

    sel = selectors.DefaultSelector()
    # checks host type against known ip addr types
    if host_type == IPv4Address:
        server = socket.create_server((host, port), family = socket.AF_INET)
        print(f"{GREEN}Server is up!!")
    else:
        server = socket.create_server((host, port), family = socket.AF_INET6)
        print(f"{GREEN}Server is up!!")

    # accept username/general accept function
    def accept(sock, mask):
        # appends new connection
        conn, addr = sock.accept()
        print(f"{GREEN}A Client has connected")
        
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, check_username)
    
    # check username function
    def check_username(conn, mask):
        try:
            username_bytes = conn.recv(1024)

        except OSError:
            print(f"{RED}A Client Disconnected")
            drop_client(conn)
            return
        
        if not username_bytes:
            drop_client(conn)
            return

        username = username_bytes.decode(encoding="ascii", errors="xmlcharrefreplace")

        if username in clients.values():
            print(username)
            try:
                conn.sendall(b"TAKEN\n")
            except OSError:
                print(f"{ORANGE}The client may have disconnected")
                drop_client(conn)
            return

        clients[conn] = username
        try:
            conn.sendall(b"GOOD\n")
            for line in history:
                conn.sendall(line)

        except OSError:
            print(f"{ORANGE}The client may have disconnected")
            drop_client(conn)
            return

        sel.modify(conn, selectors.EVENT_READ, read_msg)
    
    # drop client helper function
    def drop_client(conn):
        try:
            sel.unregister(conn)
        except ValueError:
            print(f"{RED}This connection may have been dropped already")
        except KeyError:
            print(f"{RED}This connection may have been dropped already")
        
        dropping_user = clients.get(conn)
        if dropping_user:
            dropping_bytes = dropping_user.encode(encoding="ascii", errors="xmlcharrefreplace")

            try:
                for client in list(clients):
                    if client != conn:
                        client.sendall(b"User: " + dropping_bytes + b" disconnected\n")
            except OSError:
                print(f"{RED}Dropping Reciever, Someone Disconnected?")
                
                try:
                    sel.unregister(client)
                except ValueError:
                    print(f"{RED}This connection may have been dropped already")
                except KeyError:
                    print(f"{RED}This connection may have been dropped already")
                conn.close()
                clients.pop(client, None)

    
        else:
            print(f"{ORANGE}User may not have entered user name")
            conn.close()
            clients.pop(conn, None)
        conn.close()
        clients.pop(conn, None)

    # read / distibute client msgs
    def read_msg(conn, mask):
        try:
            msg = conn.recv(16384)
            if msg:
                user = clients.get(conn)
                user = user.encode(encoding="ascii", errors="xmlcharrefreplace")
                
                time = datetime.datetime.now().strftime("%H:%M")
                time = time.encode(encoding="ascii", errors="xmlcharrefreplace")
                msg = user + b"[" + time + b"]" + b": " + msg
                history.append(msg + b"\n")

                for client in list(clients):
                    if client != conn:
                        try:
                            client.sendall(msg + b"\n")
                        except OSError:
                            print(f"{RED}Dropping Reciever, Someone Disconnected")
                            drop_client(client)
            
            else:
                print(f"{RED}A Client has Disconnected")
                drop_client(conn)
                return

        except OSError:
            print(f"{RED}A Client has Disconnected")
            drop_client(conn)
        
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, accept)

    print(f"{YELLOW}\nWaiting to connect...")

    while True:
        events = sel.select()
        for log, mask in events:
            callback = log.data
            callback(log.fileobj, mask)

   
# bunch of error handling (idk why im leaving comments anymore)
except OSError as e:
    print(f"{RED}Could not create server {e}")
    sys.exit(1)
except KeyboardInterrupt:
    print(f"\n{ORANGE}Keyboard Interrupt detected, shutting down server")
    sys.exit()
except ValueError as e:
    print(f"{RED}Maybe you inputted the wrong value: {e}")
    sys.exit(1)
