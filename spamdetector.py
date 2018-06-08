import json
from models import *
import wallaroo

def application_setup(args):
    in_host, in_port = wallaroo.tcp_parse_input_addrs(args)[0]
    out_host, out_port = wallaroo.tcp_parse_output_addrs(args)[0]

    ab = wallaroo.ApplicationBuilder("Spam Detector")
    ab.new_pipeline("Message text analysis",
                    wallaroo.TCPSourceConfig(in_host, in_port, decoder))
    ab.to(filter_messages_only)
    ab.to_stateful(update_user_stats, MessagingStats,
                   "Count per-user messaging statistics")
    ab.to_sink(wallaroo.TCPSinkConfig(out_host, out_port, encoder))
    return ab.build()

@wallaroo.computation(name="Filter XMPP Messages from other stanzas")
def filter_messages_only(stanza):
    if stanza.type == "message":
        return stanza
    else:
        pass

@wallaroo.state_computation(name="Count per-user messaging statistics")
def update_user_stats(stanza, state):
    state.update_for_sender(stanza)
    user_stats = state.stats_for(stanza.sender)
    return (maybe_report(stanza.sender, user_stats), True)

@wallaroo.decoder(header_length=4, length_fmt=">I")
def decoder(bs):
    try:
        stanza = stanza_from_dict(json.loads(bs.decode("utf-8")))
        return stanza
    except:
        print "failed decoding"
        print bs
        pass

@wallaroo.encoder
def encoder(report):
    payload = json.dumps({"user": report.user, "reason": report.reason})
    return payload + '\n'
