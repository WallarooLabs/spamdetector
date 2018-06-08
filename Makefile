.PHONY: console-consumer metrics-ui \
	env start-spamdetector \
	build-chat start-chat stop-chat \
	start-bots \
	start-sink stop-sink


SINK_PORT := 19991
SOURCE_PORT := 19990
WAIT_FOR_IT := ./wait_for_it

amoc:
	git clone https://github.com/pzel/amoc --depth=1 &&\
	 cd amoc && make deps


mongooseim:
	@git clone https://github.com/pzel/mongooseim --depth=1 &&\
	  (cd mongooseim && ./tools/configure with-none)

build-chat: mongooseim
	cd mongooseim && make rel

start-chat:
	export WALLAROO_TCP_HOSTPORT="127.0.0.1:$(SOURCE_PORT)" &&\
	cd mongooseim && ./_build/prod/rel/mongooseim/bin/mongooseim start
	$(WAIT_FOR_IT) localhost:5222

stop-chat:
	-cd mongooseim && ./_build/prod/rel/mongooseim/bin/mongooseim stop

start-bots: amoc
	(cd amoc && ./run.sh spambots 1 100)

start-sink: stop-sink clean-sink-log
	nc -k -p $(SINK_PORT) -l 127.0.0.1 > sink.log &
	$(WAIT_FOR_IT) 127.0.0.1:$(SINK_PORT)

stop-sink:
	-pkill -f $(SINK_PORT)

clean-sink-log:
	-rm sink.log

start-spamdetector: start-sink
	-rm /tmp/spamdetector-initializer.*
	exec machida --application-module spamdetector \
	  --in 127.0.0.1:$(SOURCE_PORT) \
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

console-consumer:
	$(K_BIN)/kafka-console-consumer.sh \
	  --bootstrap-server localhost:9092 \
          --topic $(OUT_TOPIC) --from-beginning
test:
	@eval '$(shell $(MAKE) env)' && python ./*_test.py

env:
	@echo '. ./.env/bin/activate ; export PYTHONPATH="$$PYTHONPATH:."'
