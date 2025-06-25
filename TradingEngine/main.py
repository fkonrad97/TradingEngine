from xchange_clients.binance_streams import BinanceTickerStream, binance_bidask_stream_log_handler
from xchange_clients.okx_streams import OKXTickerStream, okx_bidask_stream_log_handler
from util import format_symbol, run_client_with_retries
import asyncio

async def main():
    # Create clients
    binance_ticker_stream = BinanceTickerStream(binance_bidask_stream_log_handler)
    okx_ticker_stream = OKXTickerStream(okx_bidask_stream_log_handler)

    # Subscribe to tickers
    await binance_ticker_stream.subscribe(format_symbol("Binance", "BTC", "USDT"))
    await okx_ticker_stream.subscribe(format_symbol("OKX", "BTC", "USDT"))

    # Run both clients concurrently with retries
    await asyncio.gather(
        run_client_with_retries(binance_ticker_stream),
        run_client_with_retries(okx_ticker_stream),
    )

if __name__ == '__main__':
    asyncio.run(main())
