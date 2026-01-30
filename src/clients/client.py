import requests

from typing import Literal

from .config import BinanceClientConfig
from .exceptions import BinanceNetworkError

HTTPMethod: Literal['GET', 'POST']
class BinanceAPIClient():
    def __init__(self, config: BinanceClientConfig):
        self.base_url = config.base_url
        self.timeout = config.timeout
    def _request(self, method: HTTPMethod, path: str, params: dict):
        url = f"{self.base_url}{path}"
        try:
            resp = requests.request(method=method, url=url, params=params, timeout=self.timeout)
        except (requests.Timeout, requests.ConnectionError) as e:
            raise BinanceNetworkError(str(e)) from e
        
        return resp
    
    def ping(self):
        return self._request("GET", "/api/v3/ping", params=None)
    
    def time(self):
        return self._request("GET", "/api/v3/time", params=None)
    
    def exchange_info(self, params):
        return self._request("GET", "/api/v3/exchangeInfo", params=params)