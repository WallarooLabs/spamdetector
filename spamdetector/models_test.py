import json
from models import *
import unittest
from mock import Mock, MagicMock

def example_json_event():
    d = """
    {"ts":1528218310158,"stanza":"<message xml:lang='en' type='chat' to='108@localhost' id='s740958d65f69101212fd15e6f20af6d3'><body>LNen</body></message>","from":"13@localhost/res1"}
    """
    return json.loads(d)

class StanzaTest(unittest.TestCase):

    def test_message_is_parsed(self):
        s = Stanza.from_dict({u'ts': 1,
                              u'stanza': ("<message to='x' id='1'>" +
                                          "<body>A</body></message>"),
                              u'from': u"a"})
        self.assertEqual(s.type, "message")
        self.assertEqual(s.timestamp, 1)
        self.assertEqual(s.sender, u'a')
        self.assertEqual(s.recipient, u'x')
        self.assertEqual(s.body, u'A')

    def test_presence_is_parsed(self):
        s = Stanza.from_dict({u'ts': 2,
                              u'stanza': "<presence />",
                              u'from': u"x"})
        self.assertEqual(s.type, "presence")
        self.assertEqual(s.timestamp, 2)
        self.assertEqual(s.sender, u'x')
        self.assertEqual(s.recipient, None)
        self.assertEqual(s.body, None)

    def test_iq_is_parsed(self):
        s = Stanza.from_dict({u'ts': 3,
                              u'stanza': '<iq to="x" type="get" id="1"></iq>',
                              u'from': u"x"})
        self.assertEqual(s.type, "iq")
        self.assertEqual(s.timestamp, 3)
        self.assertEqual(s.sender, u'x')
        self.assertEqual(s.recipient, u'x')
        self.assertEqual(s.body, None)


class UserStatsTest(unittest.TestCase):

    def test_unique_bodies_are_a_set(self):
        stanza = Mock()
        us = UserStats()
        self.assertEqual(us.unique_bodies, set())

    def test_unique_bodies_are_updated(self):
        stanza = Mock()
        stanza.body = "a"

        us = UserStats()
        us.update(stanza)
        self.assertEqual(us.unique_bodies, set({"a"}))

    def test_duplicate_unique_bodies_are_not_reflected(self):
        stanza1 = Mock()
        stanza1.body = "a"

        stanza2 = Mock()
        stanza2.body = "a"

        us = UserStats()
        us.update(stanza1)
        us.update(stanza2)
        self.assertEqual(us.unique_bodies, set({"a"}))


    def test_message_count(self):
        stanza1 = Mock()
        stanza1.body = "a"

        stanza2 = Mock()
        stanza2.body = "a"

        us = UserStats()
        us.update(stanza1)
        us.update(stanza2)
        self.assertEqual(us.message_count, 2)

    def test_unique_recipients(self):
        stanza1 = Mock()
        stanza1.body = "a"
        stanza1.recipient = "R"

        stanza2 = Mock()
        stanza2.body = "a"
        stanza2.recipient = "Q"

        us = UserStats()
        us.update(stanza1)
        us.update(stanza2)
        self.assertEqual(len(us.unique_recipients), 2)

class MaybeReportTest(unittest.TestCase):

    def test_it_is_null_if_the_user_is_normal(self):
        us = Mock()
        us.message_count = 10
        us.unique_bodies = set("%s"%i for i in range(1,11))
        us.unique_recipients = 5
        self.assertEqual(None, maybe_report("a", us))

    def test_report_not_returned_if_there_is_enough_unique_messages(self):
        us = Mock()
        us.message_count = 10
        us.unique_bodies = set("%s"%i for i in range(1,6))
        self.assertEqual(None, maybe_report("a", us))

    def test_report_is_returned_if_more_than_half_of_msgs_are_the_same(self):
        us = Mock()
        us.message_count = 10
        us.unique_bodies = set(("a","b","c"))
        self.assertEqual(("a","repeated_message_bodies"),
                         maybe_report("a", us))


if __name__ == '__main__':
    unittest.main()
