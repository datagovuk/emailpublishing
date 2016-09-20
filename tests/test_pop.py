from emailpub.common import get_latest_messages
from emailpub.lib.fakepop import FakePOP3

def test_get_latest():
    messages = get_latest_messages(n=10, pp=FakePOP3)
    assert len(messages) == 3