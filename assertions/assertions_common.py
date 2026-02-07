def assert_status_code_and_err_code(r, expected_status_code, expected_err_code):
    data = r.json()
    assert r.status_code == expected_status_code
    assert data['code'] == expected_err_code

def assert_exchange_info_basic_response(data, top_level_keys):
    assert data.keys() == top_level_keys, f"Unexpected keys: {data.keys()}"
    assert isinstance(data["timezone"], str), f"Unexpected format for timezone. Expected: str, result: {"timezone"}"
    assert isinstance(data["serverTime"], int), f"Unexpected format for timezone. Expected: str, result: {data["serverTime"]}"
    assert isinstance(data["rateLimits"], list), f"Unexpected format for timezone. Expected: list, result: {data["rateLimits"]}"
    assert isinstance(data["exchangeFilters"], list), f"Unexpected format for timezone. Expected: list, result: {data["exchangeFilters"]}"
    assert isinstance(data["symbols"], list), f"Unexpected format for timezone. Expected: list, result: {data["symbols"]}"

def assert_exchange_info_symbols_response(data, expected, symbols_level_keys):
    assert len(data["symbols"]) == len(expected)
    for i in range(len(expected)):
        assert data["symbols"][i].keys() ==  symbols_level_keys, f"Unexpected keys: {data.keys()}"
        assert data["symbols"][i]["symbol"] == expected[i]