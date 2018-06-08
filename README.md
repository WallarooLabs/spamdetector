# Spamdetector

A demo of how Wallaroo can be used alongside a chat
installation to detect in near-real-time the presence
of malicious clients.


# Howto

## Prerequisites

- `make amoc` - downloads the xmpp bots
- `make mongooseim` - downloads the xmpp server

## Launching

1. (Terminal 1): `make build-chat start-chat`
2. (Terminal 1): `make start-sink`
3. (Terminal 2): `make start-spamdetector`
4. (Terminal 3): `make start-bots`

This should result, after some time elapses, in
reports of users sending repeated messages arriving
in Terminal 1.

# TODO:

1. Launch all the components as a Pulumi stack
2. Partition state and use 3 Wallaroo workers
3. Visualize the incoming data in a flask app or similar


# Stretch goals

1. Look at more interesting things besides unique message body counts


# Extra

You can log in to the chat server yourself with the `mcabber` cli
tool. (available via your OS)

  mcabber -f mcabberrc

