import asyncio
import traceback

async def connect_with_retries(client, max_retries: int = 5, base_wait: int = 2, retry_forever: bool = True):
    retries = 0
    while retry_forever or retries < max_retries:
        try:
            print(f"[Retry {retries}] Connecting to {client.uri}...")
            await client.start()
            print("[Info] WebSocket session ended normally.")
            break  # If client.start() returns without exception
        except Exception as e:
            print(f"[Error] Connection attempt {retries} failed: {e}")
            traceback.print_exc()
            wait_time = min(base_wait ** retries, 60)  # Cap backoff at 60s
            print(f"[Info] Reconnecting in {wait_time} seconds...")
            await asyncio.sleep(wait_time)
            retries += 1

    if not retry_forever and retries >= max_retries:
        raise RuntimeError("Max retry attempts reached. Giving up.")

async def run_client_with_retries(client):
    try:
        await connect_with_retries(client, max_retries=10, base_wait=2)
    except Exception as e:
        print(f"[Fatal] Client {client.__class__.__name__} failed: {e}")


def format_symbol(exchange: str, base: str, quote: str) -> str:
    if exchange == "Binance":
        return (base + quote).lower()
    elif exchange in {"OKX"}:
        return f"{base}-{quote}".upper()
    else:
        raise ValueError(f"Unsupported exchange: {exchange}")

async def ping_loop(websocket, interval=20):
    try:
        while True:
            await asyncio.sleep(interval)
            await websocket.ping()
            print("[Ping] Sent ping to keep connection alive.")
    except Exception as e:
        print(f"[Ping Loop Error] {e}")
        raise