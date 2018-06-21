import defusedexpat
from collections import namedtuple
import xml.etree.ElementTree as ET

class Stanza:
    def __init__(self, type, timestamp, sender, recipient, body):
        self.type = type
        self.timestamp = timestamp
        self.sender = sender
        self.recipient = recipient
        self.body = body

    @classmethod
    def from_dict(cls, d):
        timestamp = d[u'ts']
        sender = d[u'from']
        stanza = ET.fromstring(d[u'stanza'])
        stanza_body = stanza.find('body')
        type = stanza.tag
        recipient = stanza.attrib.get('to')

        body = stanza_body.text if (stanza_body is not None) else None
        return cls(type, timestamp, sender, recipient, body)


class MessagingStats():
    def __init__(self):
        self._users = {}

    def update_for_sender(self, stanza):
        user = stanza.sender
        user_stats = self.stats_for(user)
        user_stats.update(stanza)
        self._users[user] = user_stats

    def stats_for(self, user):
        return self._users.get(user) or UserStats()

class UserStats():
    def __init__(self):
        self.message_count = 0
        self.unique_bodies = set()
        self.unique_recipients = set()

    def update(self, stanza):
        self.unique_bodies.add(stanza.body)
        self.unique_recipients.add(stanza.recipient)
        self.message_count = self.message_count + 1

Report = namedtuple("Report", "user reason")

def maybe_report(user, user_stats):
    if len(user_stats.unique_bodies) < (user_stats.message_count/2):
        return Report(user, "repeated_message_bodies")
    else:
        return None
