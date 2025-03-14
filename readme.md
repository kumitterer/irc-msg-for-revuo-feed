# irc-msg-for-revuo-feed

Sends a json packet to [WMB](https://github.com/cfindlayisme/wmb) instance. Tweets. And is also on Nostr, courtesy of Pluja's relay @ https://github.com/pluja/nerostr using https://github.com/Asone/nostrss.

## Installation

```sh
cd /usr/local/src # or wherever
sudo git clone https://github.com/rottenwheel/irc-msg-for-revuo-feed.git
cd irc-msg-for-revuo-feed
docker compose pull
docker compose build
```

## Configuration

Put your environment variables in `docker-compose.override.yml`, which won't be committed to VCS. 

```sh
sudo cp docker-compose.override.sample.yml docker-compose.override.yml
sudo vim docker-compose.override.yml # Set your config here
```

## Running

```sh
docker compose up -d
docker compose logs -f # For logging
```

## TODO: Move this junk to files?

### wmb config file
```
export IRC_SERVER="irc.libera.chat:6665"
export IRC_CHANNEL="#monero-community"
export IRC_NICK="revuoxmr"
export NICKSERV_PASSWORD="hunter2"
export PASSWORD=""
export OTHER_IRC_CHANNELS="#monero,#monero-markets,#monero-pools"
export PORT="8089"
```
### nostrss config files
```
[{
        "id": "revuoxmr",
        "name":"Revuo Monero (XMR)",
        "url": "https://www.revuo-xmr.com/atom.xml",
        "schedule": "1/2 * * * * * *",
        "template": "template-file.template"
}]
```
```
[{
        "id": "revuoxmr",
        "private_key": "nsec",
        "about": "Revuo Monero - Monero (XMR) newsletter.\nRSS: https://www.revuo-xmr.com/atom.xml\nSupport: https://www.revuo-xmr.com/support",
        "name": "RevuoXMR",
        "display_name": "RevuoXMR",
        "description": "Revuo Monero - Monero (XMR) newsletter.\nRSS: https://www.revuo-xmr.com/atom.xml\nSupport: https://www.revuo-xmr.com/support/",
        "picture": "https://media.primal.net/uploads/7/60/49/760492ca78444b213b8bee258d2b461d5934556084fef8993be372ebd5d4566d.png",
        "banner": "https://media.primal.net/uploads/7/ff/39/7ff39edf5f9cf405aa35c955b735924704f4cf59856fa7267a905a949e75ebb3.png",
        "nip05": "revuoxmr@ok0.org",
        "lud16": "nicestarfish5@primal.net"
}]
```
```
[{
        "name": "pluja-usenostr",
        "target": "wss://xmr.usenostr.org",
        "active": true,
        "proxy": null
}]
```
