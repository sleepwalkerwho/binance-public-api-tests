import pytest

@pytest.mark.smoke
def test_ping_is_ok(binance_client):
    r = binance_client.ping()
    assert r.status_code == 200, f"Вернулся неожиданный код: {r.status_code}"
    assert r.json() == {}, f"Неожиданное тело ответа: {r.json()}"