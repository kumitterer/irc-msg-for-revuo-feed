import random
import feedparser
import pprint 
import os
import socket
import time
import json
import pprint
import pickle
import tweepy
import ssl

botnick = b"revuoxmr"
botpass = b"hunter2!"
api_key= ""
api_secret_key = ""

loc_long = 55.4920
loc_lat = -4.6796
api_bearer = ""


consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
url_preview = 1

def send_msg(chan,msg):
    global botnick, botpass
    server = "irc.libera.chat"
    #server = "irc.freenode.net"
    ctx = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc = ctx.wrap_socket(sock) 
    print("connecting to:"+server)
    irc.connect((server, 6697))                                                         #connects to the server
    irc.send(b"USER "+ botnick + b" "+ botnick + b" "+ botnick + b" :hello\n") #user authentication
    irc.send(b"NICK "+ botnick +b"\n")                            #sets nick
    #time.sleep(3)
    irc.send(b"PRIVMSG NICKSERV :IDENTIFY " + botnick + b" " + botpass + b"\n")
    #time.sleep(3)
    ddos = 0
    text = b""
    irc.send(b"JOIN " + chan + b"\n")  
    #time.sleep(5)
    while 1:
        ddos += 1
        if ddos > 10000:
            break
        text+=irc.recv(2040) 
        print(text)
        if irc.recv(2040).find(b'PING') != -1:                          #check if 'PING' is found
            irc.send(b'PONG ' + irc.recv(2040).split()[1] + b'\r\n') #returnes 'PONG' back to the server (prevents pinging out!)
        if b"[m]" in text or b"now logged in as" in text or b"||" in text or b"binaryFate" in text or b"pools" in text: # or b"You are now identified" in text:
            irc.send(b"PRIVMSG " + chan + b" :" + msg + b"\n")
            print(b"PRIVMSG " + chan + b" :" + msg + b"\n")
            #print("send msg")
            print("FULL SEND")
            break

def send_tweet(tweet):
	global consumer_key, consumer_secret, access_token, access_token_secret
	global loc_long, loc_lat

	client = tweepy.Client(consumer_key=consumer_key,
	                   consumer_secret=consumer_secret,
	                   access_token=access_token,
	                   access_token_secret=access_token_secret
	)
	response = client.create_tweet(text=tweet)
	print(response)
	'''
	global api_key, api_secret_key, access_token, access_token_secret
	global loc_lat, loc_long, url_preview
	global bearer_token
	auth = tweepy.OAuthHandler(api_key, api_secret_key)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	#return
	if url_preview == 0:
	    api.update_status(status = tweet, card_uri='tombstone://card', long=loc_long, lat=loc_lat, display_coordinates=1 )
	else:
	    api.update_status(status = tweet, lat=loc_lat, long=loc_long, display_coordinates=1 )
	'''
def main():
    if os.path.isfile("filename.pickle"):
        with open('filename.pickle', 'rb') as handle:
            unserialized_data = pickle.load(handle)
        last_msg = unserialized_data["msg"]
    else:
        last_msg = "~"
    chanlist = [b"#monero-community", b"#monero", b"#monero-markets", b"#monero-pools"]
    #chanlist = [b"#monero-pools"]
    NewsFeed = feedparser.parse("https://revuo-xmr.com/atom.xml")
    entry = NewsFeed.entries[0]

    msg = f"Revuo Monero {entry['title']}. {entry['link']}"
    tweet = f"We're pleased to share Revuo #Monero {entry['title']} is now available! {entry['link']}"
    if last_msg != msg:
        data = {"msg": msg}
        # Store data (serialize)
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # Load data (deserialize)
        print("New")
        msg = bytes(msg, 'ascii')
        #send_msg(chanlist, msg)
        send_tweet(tweet)
        for chan in chanlist:
            send_msg(chan,msg)
            time.sleep(30)

if __name__ == "__main__":
    main()
