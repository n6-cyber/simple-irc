'''This is a simple IRC kinda chat thing. I have a github so check that out, which i assume u already are
but basically this is to help me learn a bit about network application communication, like messaging apps,
chat apps etc. This is the simple IRC client script. anyways
- made by n_6, as a side project lwk.'''

import socket
import sys
import builtins
import selectors
import re
import datetime

try:

    color_enabled = input("Would you prefer colours on or off(on/off): ").strip().lower() or "yes"
    while color_enabled not in ("on", "enable", "enabled", "y", "yes", "true", "off", "n", "no", "false", "disabled", "disable"):
        color_enabled = input("Invalid Choice, input 'on' or 'off': ").strip().lower()
    
    host = input("Please input the ip of the server you are connecting to [default: 127.0.0.1]: ") or "127.0.0.1"
    port = int(input("Please input the port of the server you are trying to connect to [default: 6667]: ") or "6667")
   
    # color declarations / check for color on or off + color map for later uses.
    if color_enabled in ("on", "enable", "enabled", "y", "yes", "true"):
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

        color = input(f"""Set a color you want to use for your username, ({RED}Red{RESET}, {YELLOW}Yellow{RESET}, {ORANGE}Orange{RESET}, {GREEN}Green{RESET}, {BLUE}Blue{RESET}, {PURPLE}Purple{RESET}, {PINK}Pink{RESET}, {GREY}Grey{RESET}, {BLACK}Black{RESET}, or {WHITE}White{RESET}): """).strip().lower() or f"{WHITE}"

        color_map = {
            "red": RED, "yellow": YELLOW, "orange": ORANGE, "green": GREEN, "blue": BLUE,
            "purple": PURPLE, "pink": PINK, "grey": GREY, "black": BLACK, "white": WHITE,
        }

        while color not in color_map:
            color = input(f"""Please choose a color listed: ({RED}Red{RESET}, {YELLOW}Yellow{RESET}, {ORANGE}Orange{RESET}, {GREEN}Green{RESET}, {BLUE}Blue{RESET}, {PURPLE}Purple{RESET}, {PINK}Pink{RESET}, {GREY}Grey{RESET}, {BLACK}Black{RESET}, or {WHITE}White{RESET}): """).strip().lower()
        color = color_map[color]
    
    else:
        color = ""
        RESET = "\033[0m"
        BOLD = "\033[1m"

        RED = ""
        YELLOW = ""
        ORANGE =""
        GREEN = ""
        BLUE = ""
        PURPLE = ""
        PINK = ""
        GREY = ""
        BLACK = ""
        WHITE = ""
        
        # added color map here to stop errors from inline_color() functions inner function
        color_map = {
            "red": "", "yellow": "", "orange": "", "green": "", "blue": "",
            "purple": "", "pink": "", "grey": "", "black": "", "white": "",
        }
                    
    sel = selectors.DefaultSelector()

    connect = socket.create_connection((host, port))
    print(f"{GREEN}Connected to server on:{RESET} {BLUE}{host}{RESET}:{RED}{port}{RESET}")

    # recvs one line stops reading after first \n
    def recv_line(conn):
        buffer = bytearray()
        while True:
            byte = conn.recv(1)
            if not byte:
                break
            buffer.extend(byte)
            if byte == b"\n":
                break
        return buffer.decode(encoding="ascii", errors="xmlcharrefreplace").strip()

    # get username and color
    user = input(f"\n{GREEN}Please create a user name: ").strip()
    while not user:
        user = input(f"{GREEN}Please create a username: ").strip()
    if color:
        user = f"{color}{user}{RESET}"
    else:
        user = user

    bytes_user = user.encode(encoding="ascii", errors="xmlcharrefreplace")
    connect.sendall(bytes_user)
    
    returned = recv_line(connect)
    
    # checks returned status code
    if returned == "GOOD":
        print(f"{GREEN}All good, username accepted!")
    else:
        print(f"{RED}Sorry try a different one!")
        while returned != "GOOD":
            user = input(f"{GREEN}Please create a username: ").strip()
            while not user:
                user = input(f"{GREEN}Please create a username: ").strip()
            if color:
                user = f"{color}{user}{RESET}"
            else:
                user = user

            bytes_user = user.encode(encoding="ascii", errors="xmlcharrefreplace")
            connect.sendall(bytes_user)
            returned = recv_line(connect)

    print(f"{ORANGE}Server is connected you can chat now!")
    
    # checks for the format color"sentence i want in x color" also accepts '' <-- single quotes
    def inline_color(chat, color_map, reset=RESET):
        pattern = r'(red|yellow|orange|green|blue|purple|pink|grey|black|white)(["\'])([^"\']+)\2' 
        
        # returns sentence / section denoted to be color in said color
        def add_color(match):
            color_name = match.group(1).lower()
            sentence = match.group(3)
            text_color = color_map.get(color_name, "")
            return f"{text_color}{sentence}{reset}"

        return re.sub(pattern, add_color, chat)
    
    # byte array to store recv'd msgs
    buf = bytearray()

    # listens to msg from server, listener function
    def listener(connect, mask):
        try:
            msg = connect.recv(16384)
        except OSError as e:
            print(f"{RED}Connection lost?: {e}")
            sys.exit(1)
        if not msg:
            print(f"\n{RED}Disconnected from server")
            sel.unregister(connect)
            connect.close()
            sys.exit()

        buf.extend(msg)
        while True:
            b = buf.find(b"\n")
            if b == -1:
                break
            msg = buf[:b]
            del buf[:b + 1]
            msg = msg.decode(encoding="ascii", errors="xmlcharrefreplace")
            print(f"\r\033[K{msg}", end="\n", flush=True)

    # checks if a cmd was entered / completes corrisponding actions
    def cmd_check(msg):
        if msg == "/exit":
            print(f"\n{ORANGE}Exiting Client")
            sys.exit()
        elif msg == "/clear":
            print(f"\033[2J\033[H", end="")
            return True
        
        elif msg == "/help":
            print(f"=" * 30 + f"{RED} HELP {RESET}" + ("=" * 30) + "\n")
            print(f"{BLUE}  Currently Implemented Commands:{RESET}\n")
            print(f"{BLUE} '/clear' -- clears chat (client side){RESET}")
            print(f"{RED} '/exit' -- exits client{RESET}")
            print(f"{PINK} '/help' -- shows list of commands{RESET}\n")
            print(f"=" * 30 + f"{RED} HELP {RESET}" + ("=" * 30))
            return True

        elif msg.startswith("/"):
            print(f"{ORANGE}Unrecognized Command do '{RESET}{PINK}/help{RESET}{ORANGE}' to list of commands{RESET}")
            return True
       
        return False

    # sends msgs to server, writer function
    def writer(stdin, mask):
        chat = stdin.readline()
        if chat:

            chat = chat.strip()
            
            if chat:
                
                # checks for cmd
                if cmd_check(chat):
                    return
                # checks color
                chat = inline_color(chat, color_map)

                chat_bytes = chat.encode(encoding="ascii", errors="xmlcharrefreplace")
                
            try:
                connect.sendall(chat_bytes)
            except OSError as e:
                print(f"{RED}Error has occured {e}")


        else:
            print(f"\n{RED}Exiting Client")
            sys.exit()

    connect.setblocking(False)
    sel.register(connect, selectors.EVENT_READ, listener)
    sel.register(sys.stdin, selectors.EVENT_READ, writer)
    
    time = datetime.datetime.now().strftime("%H:%M")
    print(f"{user}[{time}]: ", end="", flush=True)

    while True:
        events = sel.select()
        for log, mask in events:
            callback = log.data
            callback(log.fileobj, mask)
            time = datetime.datetime.now().strftime("%H:%M")
            print(f"{user}[{time}]: ", end="", flush=True)

# error handling
except OSError as e:
    print(f"{RED}An error has occured, shutting down client: {e}")
    sys.exit(1)

except KeyboardInterrupt:
    print(f"\nShutting down/Quitting Client")
    sys.exit(0)

except ValueError as e:
    print(f"{RED}Maybe you misspelled something, {e}")
    sys.exit(1)

