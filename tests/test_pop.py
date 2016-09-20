from emailpub.common import get_latest_messages


def test_get_latest():
    messages = get_latest_messages(n=10)
    assert len(messages) == 3


def test_respond():
    from emailpub.respond import main
    main("config_test.yml")