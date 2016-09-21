

from emailpub.common import (generate_token_and_address,
                             validate_token,
                             invalidate_token,
                             token_from_email)

def test_token_from_email():
    assert token_from_email("ross+test@somewhere.com") == "test"
    assert token_from_email("ross.jones@somewhere.com") == ""

def test_token_gen():
    address = generate_token_and_address("email", "dataset", "10/10/2016")
    token = token_from_email(address)
    res = validate_token(token, "email")
    print res

def test_token_invalidation():
    address = generate_token_and_address("email", "dataset", "10/10/2016")
    token = token_from_email(address)
    success, _ = validate_token(token, "email")
    assert success
    invalidate_token(token)
    success, _ = validate_token(token, "email")
    assert not success