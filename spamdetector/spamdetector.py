import json
import zlib
from models import *
import wallaroo

N_PARTITIONS = 1024
PARTITION_KEYS = range(0,N_PARTITIONS)

def application_setup(args):
    in_host, in_port = wallaroo.tcp_parse_input_addrs(args)[0]
    out_host, out_port = wallaroo.tcp_parse_output_addrs(args)[0]
    tcp_source = wallaroo.TCPSourceConfig(in_host, in_port, decoder)
    tcp_sink = wallaroo.TCPSinkConfig(out_host, out_port, encoder)

    ab = wallaroo.ApplicationBuilder("Spam Detector")
    ab.new_pipeline("Message text analysis", tcp_source)
    ab.to_parallel(filter_messages_only)
    ab.to_state_partition(update_user_stats, MessagingStatistics,
                          "Count per-user messaging statistics",
                          sender_to_partition_key,
                          PARTITION_KEYS)
    ab.to_state_partition(classify_user, Classifier,
                          "Classify users based on statistics",
                          stats_to_partition_key,
                          PARTITION_KEYS)
    ab.to_sink(tcp_sink)
    return ab.build()


@wallaroo.computation(name="Filter XMPP Messages from other stanzas")
def filter_messages_only(stanza):
    if stanza.type == "message":
        return stanza
    else:
        pass

@wallaroo.state_computation(name="Count per-user messaging statistics")
def update_user_stats(stanza, state):
    user_stats = state.update_for_sender(stanza)
    return (user_stats, True)

@wallaroo.state_computation(name="Classify users based on statistics")
def classify_user(stats, state):
    maybe_report = state.classify(stats)
    if maybe_report:
        return (maybe_report, True)
    else:
        return (None, False)

@wallaroo.decoder(header_length=4, length_fmt=">I")
def decoder(bs):
    stanza = Stanza.from_dict(json.loads(bs.decode("utf-8")))
    return stanza

@wallaroo.encoder
def encoder(report):
    payload = json.dumps({"user": report.user, "reason": report.reason})
    return payload + '\n'

@wallaroo.partition
def stats_to_partition_key(stats):
    return zlib.adler32(stats.user) % N_PARTITIONS

@wallaroo.partition
def sender_to_partition_key(stanza):
    return zlib.adler32(stanza.sender) % N_PARTITIONS
