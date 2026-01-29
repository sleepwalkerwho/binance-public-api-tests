import pytest
import time

@pytest.mark.smoke
def test_ping_status_code_and_body(binance_client):
    r = binance_client.ping()
    assert r.status_code == 200, f"Вернулся неожиданный код: {r.status_code}"
    assert r.json() == {}, f"Неожиданное тело ответа: {r.json()}"

@pytest.mark.smoke
def test_time_status_code_and_body(binance_client):
    r = binance_client.time()
    data = r.json()
    assert r.status_code == 200, f"Вернулся неожиданный код: {r.status_code}"
    assert set(data.keys()) == {"serverTime"}, f"Неожиданный ключ в ответе: {data} != 'serverTime'"

@pytest.mark.smoke
def test_time_is_correct(binance_client):
    r = binance_client.time()
    current_local_time_utc = time.time_ns() // 1_000_000
    binance_server_time = r.json()['serverTime']
    delta_ms = binance_server_time - current_local_time_utc
    assert delta_ms < 1_000, f"Время в serverTime {binance_server_time} отличается от текущего времени {current_local_time_utc} на {delta_ms} мс"

@pytest.mark.smoke
def test_time_is_increasing(binance_client):
    t1 = binance_client.time().json()["serverTime"]
    t2 = binance_client.time().json()["serverTime"]
    t3 = binance_client.time().json()["serverTime"]
    t4 = binance_client.time().json()["serverTime"]

    assert t1 < t2 < t3 < t4, "Время в serverTime не увеличивается"