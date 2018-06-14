FROM ubuntu:16.04

ENV PONYC_VERSION 0.22.6
ENV PONY_STABLE_VERSION 0.1.2-90.2af1a62
ENV OTP_VERSION 1:20.2.2
ENV ELIXIR_VERSION 1.5.2-1

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys "D401AB61 DBE1D0A2" \
  && echo "deb http://dl.bintray.com/pony-language/ponyc-debian pony-language main" >> /etc/apt/sources.list \
  && echo "deb http://dl.bintray.com/pony-language/pony-stable-debian /" >> /etc/apt/sources.list \
  && apt-get update \
  && apt-get install -y \
    build-essential \
    git \
    liblz4-dev \
    libsnappy-dev \
    libssl-dev \
    make \
    netcat \
    ponyc=${PONYC_VERSION} \
    pony-stable=${PONY_STABLE_VERSION} \
    python \
    python-dev \
    python-pip \
    wget

# python testing dependencies
RUN python2 -m pip install --upgrade pip enum34 \
  && python2 -m pip install pytest==3.2.2

# Wallaroo
RUN git clone https://github.com/wallaroolabs/wallaroo \
  && cd wallaroo \
  && make build-machida \
  # TODO: setup.py for Wallaroo?
  && cp machida/build/machida /usr/bin \
  && cp machida/wallaroo.py /usr/lib/python2.7

RUN mkdir -p /app
WORKDIR /app

COPY spamdetector.py /app/
COPY models.py /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT /app/docker-entrypoint.sh
