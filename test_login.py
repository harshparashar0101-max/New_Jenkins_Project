import pytest

@pytest.mark.xray_test("LOGI-21")
def test_valid_login():
    assert True


@pytest.mark.xray_test("LOGI-22")
def test_invalid_login():
    assert True