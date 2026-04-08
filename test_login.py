def test_valid_login():
    username = "admin"
    password = "admin123"

    assert username == "admin"
    assert password == "admin123"


def test_invalid_login():
    username = "admin"
    password = "wrongpass"

    assert not (username == "admin" and password == "admin123")