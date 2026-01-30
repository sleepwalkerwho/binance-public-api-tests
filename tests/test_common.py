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

@pytest.mark.smoke
def test_exchange_info_status_code_and_body_format(binance_client):
    r = binance_client.exchange_info(params=None)
    data = r.json()

    assert r.status_code == 200, f"Unexpected status code: {r.status_code}, body={r.text}"
    assert isinstance(data, dict), f"Unexpected data format. Expected: dict, result: {type(data)}"

@pytest.mark.smoke
def test_exchange_info_has_required_top_level_keys(binance_client):
    r = binance_client.exchange_info(params=None)
    data = r.json()

    timezone = data["timezone"]
    server_time = data["serverTime"]
    rate_limits = data["rateLimits"]
    exchange_filters = data["exchangeFilters"]
    symbols = data["symbols"]

    assert data.keys() == {'timezone', 'serverTime', 'rateLimits', 'exchangeFilters', 'symbols'}, f"Unexpected keys: {data.keys()}"
    assert data["timezone"] == "UTC"
    assert isinstance(timezone, str), f"Unexpected format for timezone. Expected: str, result: {type(timezone)}"
    assert isinstance(server_time, int), f"Unexpected format for timezone. Expected: str, result: {type(timezone)}"
    assert isinstance(rate_limits, list), f"Unexpected format for timezone. Expected: list, result: {type(rate_limits)}"
    assert isinstance(exchange_filters, list), f"Unexpected format for timezone. Expected: list, result: {type(exchange_filters)}"
    assert isinstance(symbols, list), f"Unexpected format for timezone. Expected: list, result: {type(symbols)}"