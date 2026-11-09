# simple-irc
This is a simple irc repo, its a IRC sorta, it's completely human written, it's definitely not secure at the moment at least, and it's just to help me learn how irc and chats in general work! Well more like for me to learn how networks interact w/ applications. 

## FEATURES (or bugs depends)
- **Private Messages (`/msg <username> <msg>`):** send to people, doesn't work if ur missing `/msg <username> or <msg>`
- **Inline Styling:** colours wow! so pwetty... `red"hello"` or `blue"world"` and more just look and you'll see supports `green'single quotes btw'`
- **Help Menu:** cmd `/help` to get help cause some people need it 
- **Clear Screen:** clear w/ `/clear` (only client side btw) another user joining will see ur previous last ten msgs btw, (check `server.py` for confirmation btw)

## Work in Progress aka [WIP] wont be added anytime soon (BRO I HATE MARKDOWN SO SO SO MUCH)
- **E2E Encryption:** some form of message encryption.
- **Media Sharing:** files, Gifs, and images.
- **Animated Text:** moving txt annotated w/ smthing like how u can use colour `red"wow"` like this but w/ animated txt.
- **Server-Wide Music Player:** because music is fun
- **Frontend:** HTML & CSS only (no JS cuz JS is corporate slop) `sadly github doesnt support yk hosting servers, and im to broke to host it plus is useless so` yea that goes in gutter.

## KNOWN ISSUES
- if a user sends msg and u had typed something before and not pressed enter, then when u write on next line it sends both what u typed before + what u typed now
- can not send coloured msgs through `/msg` cmd.

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
