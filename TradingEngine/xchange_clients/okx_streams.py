from xchange_clients.base_client import BaseClient
from typing import Callable
import json


class OKXTickerStream(BaseClient):
    def __init__(self, handler: Callable):
        super().__init__(handler)
        self.uri = "wss://ws.okx.com:8443/ws/v5/public"
        self.ping_support = True  # OKX expects client to send {"op": "ping"}
        self.built_in_pong = False  # No websocket-level ping/pong
        self.validate_heartbeat_config()

    async def add_parameter(self, args):
        parameter = (await self.get_stream_identifier()).format(*args)
        self.params = parameter
        print(self.params)

    async def get_stream_identifier(self) -> str:
        return "{}"

    async def get_request(self):
        return json.dumps({
            "op": "subscribe",
            "args": [{"channel": "tickers", "instId": "BTC-USDT"}]
        })

async def okx_bidask_stream_log_handler(msg):
    try:
        parsed = json.loads(msg)
        if 'data' in parsed and isinstance(parsed['data'], list) and parsed['data']:
            ticker_data = parsed['data'][0]
            print(f"OKX | Symbol: {ticker_data['instId']} | Ask: {ticker_data['askPx']} | Bid: {ticker_data['bidPx']}")
        else:
            print("Received message without data:", parsed)
    except Exception as e:
        print(f"Error handling OKX message: {e}")