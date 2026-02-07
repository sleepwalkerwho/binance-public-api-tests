import pytest

from assertions.assertions_common import assert_exchange_info_basic_response, assert_exchange_info_symbols_response, assert_status_code_and_err_code

@pytest.mark.symbol
@pytest.mark.parametrize("params",[{"symbol": "BTCUSDT"}, {"symbol": "BNBUSDT"}])
def test_exchange_info_single_symbol(binance_client, top_level_keys, symbols_level_keys, params):
    """Получение информации по одному символу"""
    r = binance_client.exchange_info(params=params)
    data = r.json()
    assert_exchange_info_basic_response(data, top_level_keys)
    assert r.status_code == 200
    assert data["symbols"][0].keys() ==  symbols_level_keys, f"Unexpected keys: {data.keys()}"
    assert data["symbols"][0]["symbol"] == params['symbol']

@pytest.mark.symbol
def test_exchange_info_fake_symbol(binance_client):
    """Запрос несуществующего символа"""
    r = binance_client.exchange_info(params={"symbol": "FAKE"})
    assert_status_code_and_err_code(r, expected_status_code=400, expected_err_code=-1121)

@pytest.mark.symbol
def test_exchange_info_empty_symbol(binance_client):
    """Запрос пустого символа"""
    r = binance_client.exchange_info(params={"symbol": ''})
    assert_status_code_and_err_code(r, expected_status_code=400, expected_err_code=-1105)

@pytest.mark.symbol
def test_exchange_info_symbol_case_sensitive(binance_client):
    """Запрос неподдерживаемого символа lowercase"""
    r = binance_client.exchange_info(params={"symbol": 'btcusd'})
    assert_status_code_and_err_code(r, expected_status_code=400, expected_err_code=-1100)

@pytest.mark.symbols
@pytest.mark.parametrize(
    "symbols, expected",
    [
        ({"symbols": '["BTCUSDT","ETHUSDT"]'}, ["BTCUSDT","ETHUSDT"]),
        ({"symbols": '["BTCUSDT","BNBBTC","ETHUSDT"]'}, sorted(["BTCUSDT","BNBBTC","ETHUSDT"])),
    ]
)
def test_exchange_info_multiple_symbols(binance_client, top_level_keys, symbols_level_keys, symbols, expected):
    """Получение информации по нескольким символам"""
    # Проверка массива из 2+ символов
    # Проверка порядка символов в ответе
    # Проверка граничных случаев (50+ символов)
    r = binance_client.exchange_info(params=symbols)
    data = r.json()
    assert_exchange_info_basic_response(data, top_level_keys)
    assert_exchange_info_symbols_response(data, expected, symbols_level_keys)

@pytest.mark.symbols
def test_exchange_info_symbols_empty_array(binance_client):
    """Пустой массив symbols"""
    r = binance_client.exchange_info(params={"symbols": ['']})
    assert_status_code_and_err_code(r, expected_status_code=400, expected_err_code=-1100)

@pytest.mark.symbols
@pytest.mark.parametrize(
    "symbols",
    [
        ({"symbols": '["BTCUSDT","BTCUSDT"]'}),
        ({"symbols": '["BTCUSDT","BTCUSDT","ETHUSDT"]'}),
    ]
)
def test_exchange_info_symbols_duplicates(binance_client, symbols):
    """Дубликаты в массиве symbols"""
    # Проверка обработки дублирующихся символов
    r = binance_client.exchange_info(params=symbols)
    assert_status_code_and_err_code(r, expected_status_code=400, expected_err_code=-1151)

