from xchange_clients.base_client import BaseClient
from typing import Callable
import json


class BinanceTickerStream(BaseClient):
    def __init__(self, handler: Callable):
        super().__init__(handler)
        self.uri = "wss://stream.binance.com:9443/ws"
        self.ping_support = False  # Binance does not need manual pings
        self.built_in_pong = True  # Websockets handles it
        self.validate_heartbeat_config()

    async def add_parameter(self, args):
        parameter = (await self.get_stream_identifier()).format(*args)
        self.params.append(parameter)
        print(self.params)

    async def get_stream_identifier(self) -> str:
        return "{}@ticker"

    async def get_request(self):
        return json.dumps({
            "method": "SUBSCRIBE",
            "params": self.params,
            "id": self.active_id
        })

async def binance_bidask_stream_log_handler(msg):
    try:
        parsed = json.loads(msg)
        print(f"BINANCE | Symbol: {parsed['s']} | Ask: {parsed['a']} | Bid: {parsed['b']}")
    except Exception as e:
        print(f"Error handling OKX message: {e}")