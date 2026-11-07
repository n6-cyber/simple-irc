'''This is a simple IRC kinda chat thing. I have a github so check that out, which i assume u already are
but basically this is to help me learn a bit about network application communication, like messaging apps,
chat apps etc. This is the simple IRC client script. anyways
- made by n_6, as a side project lwk.'''

import socket
import sys
import builtins
import selectors  

try:
    
    host = input("Please input the ip of the server you are connecting to: ")
    port = int(input("Please input the port of the server you are trying to connect to: "))
    
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

    sel = selectors.DefaultSelector()
    
    socket.setdefaulttimeout(15)
    connect = socket.create_connection((host, port))
    print(f"Connected to server on: {host}:{port}")
    
    user = input("\nPlease create a user name: ").strip()
    while not user:
        user = input("Please create a username: ").strip()
        
    bytes_user = user.encode(encoding="ascii", errors="xmlcharrefreplace")
    connect.sendall(bytes_user)
    back = connect.recv(1024)
    returned = back.decode(encoding="ascii", errors="xmlcharrefreplace")

    if returned == "GOOD":
        print("All good, username accepted!")
    else:
        print("Sorry try a different one!")
        while returned != "GOOD":
            user = input("Please create a username: ").strip()
            while not user:
                user = input("Please create a username: ").strip()
            bytes_user = user.encode(encoding="ascii", errors="xmlcharrefreplace")
            connect.sendall(bytes_user)
            back = connect.recv(1024)
            returned = back.decode(encoding="ascii", errors="xmlcharrefreplace")

    print("Server is connected you can chat now!")

    # listens to msg from server, listener function
    def listener(connect, mask):
        msg = connect.recv(16384)
        msg = msg.decode(encoding="ascii", errors="xmlcharrefreplace")
        if msg:
            print(f"\r\033[K{msg}")
        else:
            print("\nDisconnected from server")
            sel.unregister(connect)
            connect.close()
            sys.exit()
    
    # sends msgs to server, writer function
    def writer(stdin, mask):
        chat = stdin.readline()
        if chat:

            chat = chat.strip()
            
            if chat:
                chat_bytes = chat.encode(encoding="ascii", errors="xmlcharrefreplace")
                connect.sendall(chat_bytes)
        else:
            print("\nExiting Client")
            sys.exit()

    connect.setblocking(False)
    sel.register(connect, selectors.EVENT_READ, listener)
    sel.register(sys.stdin, selectors.EVENT_READ, writer)
    
    print(f"{user}: ", end="", flush=True)

    while True:
        events = sel.select()
        for log, mask in events:
            callback = log.data
            callback(log.fileobj, mask)
            print(f"{user}: ", end="", flush=True)

except OSError as e:
    print(f"An error has occured, shutting down server: {e}")
    sys.exit(1)

except KeyboardInterrupt:
    print("\nShutting down/Quitting Client")
    sys.exit(0)

except ValueError as e:
    print(f"Maybe you misspelled something, {e}")
    sys.exit(1)
