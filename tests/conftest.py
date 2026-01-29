import pytest

from src.clients.config import BinanceClientConfig
from src.clients.client import BinanceAPIClient

@pytest.fixture
def binance_client():
    return BinanceAPIClient(BinanceClientConfig())