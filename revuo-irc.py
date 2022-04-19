import random
import feedparser
import pprint 
import os
import socket
import time
import json
import pprint
import pickle

def send_msg(channels,msg):
    server = "irc.libera.chat"
    #server = "irc.freenode.net"
    #this function will hang while waiting for someone to say hello
    botnick = b"fyi"
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
    print("connecting to:"+server)
    irc.connect((server, 6667))                                                         #connects to the server
    irc.send(b"USER "+ botnick + b" "+ botnick + b" "+ botnick + b" :hello\n") #user authentication
    irc.send(b"NICK "+ botnick +b"\n")                            #sets nick
    irc.send(b"PRIVMSG nickserv :iNOOPE\r\n")    #auth
    
    for channel in channels:
        irc.send(b"JOIN "+ channel +b"\n")  
        while 1:
            text=irc.recv(2040) 
            #print(text)
            if text.find(b'PING') != -1:                          #check if 'PING' is found
                irc.send(b'PONG ' + text.split()[1] + b'\r\n') #returnes 'PONG' back to the server (prevents pinging out!)
            if b"End of /NAMES list" in text:
                #irc.send(b"PRIVMSG " + channel + b" :" + msg + b"\n")
                print(b"PRIVMSG " + channel + b" :" + msg + b"\n")
                break

def main():
    if os.path.isfile("filename.pickle"):
        with open('filename.pickle', 'rb') as handle:
            unserialized_data = pickle.load(handle)
        last_msg = unserialized_data["msg"]
    else:
        last_msg = "~"
    chanlist = [b"#monero", b"#monero-community", b"#monero-markets"]
    NewsFeed = feedparser.parse("https://revuo-xmr.com/atom.xml")
    entry = NewsFeed.entries[0]

    msg = f"{entry['title']}. {entry['link']}"
    if last_msg != msg:
        data = {"msg": msg}
        # Store data (serialize)
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # Load data (deserialize)

        msg = bytes(msg, 'ascii')
        send_msg(chanlist, msg)

if __name__ == "__main__":
    main()
