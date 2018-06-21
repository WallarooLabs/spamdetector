.PHONY: build-chat \
	clear-log \
	deps \
	env \
	metrics-ui \
	run-locally \
	setup \
	spamdetector-chat \
	start-bots \
	start-chat \
	start-sink \
	start-spamdetector \
	stop-chat \
	stop-sink \

ACTIVATE := . ./.env/bin/activate ; export PYTHONPATH="$$PYTHONPATH:."
LOGDIR := ./log
SINK_PORT := 19991
SOURCE_PORT := 19990
WAIT_FOR_IT := ./wait_for_it -q

run-locally: deps clear-log
	@$(ACTIVATE) &&\
	 $(MAKE) metrics-ui > $(LOGDIR)/mui.log 2>&1 & \
	 $(MAKE) start-spamdetector > $(LOGDIR)/spamdetector.log 2>&1 &\
	 $(MAKE) start-chat > $(LOGDIR)/chat.log 2>&1  &
	@$(WAIT_FOR_IT) localhost:4000
	@$(WAIT_FOR_IT) localhost:$(SOURCE_PORT)
	@$(WAIT_FOR_IT) localhost:5222

deps: amoc mongooseim

spamdetector-chat:
	docker run -d --rm -p 5222:5222  \
	  -e WALLAROO_TCP_HOSTPORT=172.17.0.1:19990  \
	  --name spamdetector-chat \
	  pzel/spamdetector-chat:latest /entrypoint.sh

amoc:
	git clone https://github.com/pzel/amoc --depth=1 &&\
	 cd amoc && make deps

mongooseim:
	@git clone https://github.com/pzel/mongooseim --depth=1 &&\
	  (cd mongooseim && ./tools/configure with-none)

clear-log: $(LOGDIR)
	-rm -f $(LOGDIR)/*

$(LOGDIR):
	mkdir -p $(LOGDIR)

build-chat: mongooseim
	cd mongooseim && make rel

start-chat: stop-chat
	export WALLAROO_TCP_HOSTPORT="127.0.0.1:$(SOURCE_PORT)" &&\
	cd mongooseim && ./_build/prod/rel/mongooseim/bin/mongooseim start
	$(WAIT_FOR_IT) localhost:5222

stop-chat:
	-pkill -f mongooseim
	-sleep 0.5

start-bots: amoc
	(cd amoc && CHAT_SERVER_HOSTNAME=127.0.0.1 ./run.sh spambots 1 100)

start-sink: $(LOGDIR) stop-sink
	nc -k -p $(SINK_PORT) -l 127.0.0.1 > $(LOGDIR)/local_sink.log &
	$(WAIT_FOR_IT) 127.0.0.1:$(SINK_PORT)

stop-sink:
	-pkill -f $(SINK_PORT)

start-spamdetector: start-sink
	-rm /tmp/spamdetector-initializer.*
	-pkill -f machida
	$(ACTIVATE) &&\
	cd spamdetector && export PYTHONPATH=$$PYTHONPATH:. &&\
	exec machida --application-module spamdetector \
	  --in 0.0.0.0:$(SOURCE_PORT) \
	  --out 127.0.0.1:$(SINK_PORT) \
          --metrics 127.0.0.1:5001 \
          --control 127.0.0.1:12500 \
          --data 127.0.0.1:12501 \
          --external 127.0.0.1:5050 \
          --cluster-initializer --ponythreads=1 \
          --ponynoblock

metrics-ui:
	docker run -d --name mui -p 0.0.0.0:4000:4000 -p 0.0.0.0:5001:5001 \
	  wallaroo-labs-docker-wallaroolabs.bintray.io/release/metrics_ui:0.4.2

test:
	@$(ACTIVATE) && (cd spamdetector && python ./*_test.py)

env:
	@echo $(ACTIVATE)

setup:
	@virtualenv .env && $(ACTIVATE) && \
	  pip install -r spamdetector/requirements.txt
	@echo '\n******************************'
	@echo 'Please copy $$wallaroo_src/machida/build/machida to .env/bin'
	@echo 'And $$wallaroo_src/machida/wallaroo.py to '\
	      '.env/lib/python2.7/site-packages/'

