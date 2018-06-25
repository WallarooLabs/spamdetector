FROM wallaroo-labs-docker-wallaroolabs.bintray.io/release/wallaroo:0.4.3

COPY docker-entrypoint.sh spamdetector.py models.py requirements.txt\
     /app/

RUN env-setup\
    && pip install -r /app/requirements.txt\
    && chmod +x /app/docker-entrypoint.sh

ENTRYPOINT /app/docker-entrypoint.sh
