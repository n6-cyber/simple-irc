'''This is a simple IRC kinda chat thing. I have a github so check that out, which i assume u already are
but basically this is to help me learn a bit about network application communication, like messaging apps,
chat apps etc. This is the simple IRC client script. anyways
- made by n_6, as a side project lwk.'''

import socket
import sys
import builtins
import threading  

try:
    
    host = input("Please input the ip of the server you are connecting to: ")
    port = int(input("Please input the port of the server you are trying to connect to: "))
    
    threads = []
 
    connect = socket.create_connection((host, port))
    print(f"Connected to server on: {host}:{port}")
    
    user = input("\nPlease create a user name: ")
    bytes_user = user.encode(encoding="ascii", errors="xmlcharrefreplace") 
    connect.sendall(bytes_user)
    back = connect.recv(1024)
    returned = back.decode(encoding="ascii", errors="xmlcharrefreplace")

    if returned == "GOOD":
        print("All good, username accepted!")
    else:
        print("Sorry try a different one!")
        while returned != "GOOD":
            user = input("Please create a username: ")

    print("Server is connected you can chat now!")

    def listener(connect):
        connect.recv(16384)

    thread_1 = threading.Thread(target=listener, args=(connect, ))
    threads.append(thread_1)
    thread_1.start()

    while True:
        chat = input(f"{user}: ")
        chat_bytes = chat.encode(encoding="ascii", errors="xmlcharrefreplace")
        connect.sendall(chat_bytes)
        

except OSError as e:
    print(f"An error has occured, shutting down server: {e}")
    sys.exit(1)

except KeyboardInterrupt:
    print("\nShutting down/Quitting Client")
    sys.exit(0)

except ValueError as e:
    print(f"Maybe you misspelled something, {e}")
    sys.exit(1)
