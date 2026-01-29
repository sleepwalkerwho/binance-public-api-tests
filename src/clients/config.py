from dataclasses import dataclass

@dataclass
class BinanceClientConfig():
    base_url: str = "https://api.binance.com"
    timeout: float = 10.0