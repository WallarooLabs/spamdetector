FROM ubuntu:xenial
RUN apt-get update && apt-get -y install netcat
COPY entrypoint.sh /
RUN chmod a+x /entrypoint.sh
