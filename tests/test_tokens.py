

from emailpub.common import generate_token_and_address, validate_token, token_from_email

def test_token_from_email():
    assert token_from_email("ross+test@somewhere.com") == "test"
    assert token_from_email("ross.jones@somewhere.com") == ""

def test_token_gen():
    address = generate_token_and_address("email", "dataset")

    token = token_from_email(address)

    res = validate_token(token, "email")
    print res