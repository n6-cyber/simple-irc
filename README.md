# simple-irc
This is a simple irc repo, its a IRC sorta, it's completely human written (but AI was used for fact checking and reference and like documentation) i was to lazy to google documentation, it's definitely not secure at the moment at least, and it's just to help me learn how irc and chats in general work! Well more like for me to learn how networks interact w/ applications. 

## FEATURES (or bugs depends)
- **Private Messages (`/msg <username> <msg>`):** send to people, doesn't work if ur missing `/msg <username> or <msg>`
- **Inline Styling:** colours wow! so pwetty... `red"hello"` or `blue"world"` and more just look and you'll see supports `green'single quotes btw'`
- **Help Menu:** cmd `/help` to get help cause some people need it 
- **Clear Screen:** clear w/ `/clear` (only client side btw) another user joining will see ur previous last ten msgs btw, (check `server.py` for confirmation btw)
- at one point having multiple users w/ same name was a feature

## BUG FIXES (bugs i fixed)
- fixed error where users coloured users were treated as seperate usernames
- fixed error where clients would not recieve user: X disconnected messages
- changed `client.py` to use both double quote and single quote in inline color annotation
- fixed indent error on writer(), human error man ;(
- fixed issue where if msg over byte limit client that recieved would not display it properly cutting of the msg early
-
- fixed some other issues too, again let me know if there are any issues u discovered and open an issue idc if u use my thing or not i like my project so ill keep it good

## Work in Progress aka [WIP] wont be added anytime soon (BRO I HATE MARKDOWN SO SO SO MUCH)
- **E2E Encryption:** some form of message encryption.
- **Media Sharing:** files, Gifs, and images.
- **Animated Text:** moving txt annotated w/ smthing like how u can use colour `red"wow"` like this but w/ animated txt.
- **Server-Wide Music Player:** because music is fun
- **Frontend:** HTML & CSS only (no JS cuz JS is corporate slop) `sadly github doesnt support yk hosting servers, and im to broke to host it plus is useless so` yea that goes in gutter.
- **Rust Rewrite** i might rewrite this in rust language later, once i finish learning it, wish me luck on that btw
- **TUI** usable TUI cause rn its a CLI, would be cool to have navigation, may add later (maybe in rust rewrite)
- **Persistant Memory** instead of storing things in RAM (god is it expensive now) it gets stored in storage like hard drives and stuff protects the RAM, uses storage (also expensive btw)


## KNOWN ISSUES
- if a user sends msg and u had typed something before and not pressed enter, then when u write on next line it sends both what u typed before + what u typed now
- can not send coloured msgs through `/msg` cmd
- please let me know if theres any other issues, i will try to fix them

## SETUP
```bash
git clone https://github.com/n6-cyber/simple-irc.git
cd simple-irc
python server.py
server ip: 127.0.0.1 (in example)
server port: 6667 (in example)

python client.py
colors on or off: on (example btw if u havent figured that out yet)
server ip: 127.0.0.1 (example btw)
server port: 6667 (example btw)
ur user color: blue (example whatever colour u like use it)
username: n_6 (example)
n_6[time]: hiii
```

### THE END
Thanks for looking over this it was a pleasure to try this week,
next year or whenever you host this again i'll be sure to try again
I'm not that good, I will definitely try better and start
at start of the week so i don't rush as much don't like being
this tight but thanks! id appreciate comments on what i can do
to find documentation easier since i spent more time searching things
up then i could code for so yea but thanks anyways.
P.S. more like note to self I hope to god that my project is MVP ok, and that this ships but for a first project it's all like it depends so yea
