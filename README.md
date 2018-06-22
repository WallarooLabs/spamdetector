# Spamdetector

A demo of how Wallaroo can be used alongside a chat
installation to detect in near-real-time the presence
of malicious clients.


# Howto (Docker-compose)

    $ make deps
    $ docker-compose up
	 (.. wait for docker to download the world ..)
	$ tail -f sink_output/sink.log

Open http://localhost:4000 to see the statistics for your pipeline.


# Development & running w/out Docker

	- Install erlang > 18 and the development libraries for:
		ssl, expat, zlib, and unixodbc

   - Run `make deps build-chat`

   - You now have two directories: `mongooseim` and `amoc`.

   - The chat server lives in `mongooseim` and is preconfigured for:
     a) Allowing logins from all <USER>@localhost, where password=<USER>
     b) Sending a copy of every XMPP stanza to a TCP socked defined by
   	  the environment variable WALLAROO_TCP_HOSTPORT

   - The spam simluation script lives `amoc/spambots.erl` and can be
     launched with the `run.sh` script found in `amoc`.
     Use `./run.sh spambots 1 13` to launch 12 regular users and 1 spammer.

   - Run `setup` to set up a Virtualenv in `.env`
   - As instructed, copy the `machida` executable and `wallaroo.py` into the
     virtualenv. If you don't have these, follow the [Wallaroo Tutorial]() to
     get them.

   - Run `make run-locally` to launch all the required components locally. If
     you modify anything under `mongooseim`, you will have to `make build-chat`
     to recompile the chat server.

   - Take a look at `log/local_sink.log` to see the spam detector publishing
     its results.


## Prerequisites

 * [docker-compose](https://docs.docker.com/compose/)
