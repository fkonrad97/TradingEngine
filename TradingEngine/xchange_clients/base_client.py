import websockets
from abc import ABC, abstractmethod
from typing import Callable


class BaseClient(ABC):
    def __init__(self, handler: Callable) -> None:
        self.handler = handler
        self.uri = None
        self.ws_reference = None
        self.params = []
        self.active_id = None

        # Heartbeat settings
        self.ping_support = None  # True if client should send ping manually
        self.built_in_pong = None  # True if websocket lib handles pong
        self.last_message_time = None  # Used for watchdog

    # This is just guard for heartbeat logic
    def validate_heartbeat_config(self):
        assert isinstance(self.ping_support, bool), \
            f"{self.__class__.__name__}: ping_support must be a boolean"
        assert isinstance(self.built_in_pong, bool), \
            f"{self.__class__.__name__}: built_in_pong must be a boolean"
        if self.built_in_pong:
            assert not self.ping_support, \
                f"{self.__class__.__name__}: If built_in_pong is True, ping_support must be False"

    async def start(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                self.ws_reference = websocket

                # Send subscription request
                request = await self.get_request()
                await websocket.send(request)

                print(f"[Connected] Subscribed with: {request}")

                # Optionally wait for confirmation (e.g., {"event": "subscribe"})
                initial_msg = await websocket.recv()
                print(f"[Received initial response]: {initial_msg}")

                async for message in websocket:
                    await self.handler(message)

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"[Disconnected] WebSocket closed on Error: {e}")
            raise
        except websockets.exceptions.ConnectionClosedOK as e:
            print(f"[Disconnected] WebSocket closed OK: {e}")
            raise
        except websockets.exceptions.ConnectionClosed as e:
            print(f"[Disconnected] WebSocket closed: {e}")
            raise
        except Exception as e:
            print(f"[Error] in start(): {e}")
            raise

    async def subscribe(self, *args: str):
        await self.add_parameter(args)

    @abstractmethod
    async def add_parameter(self, args):
        pass

    @abstractmethod
    async def get_request(self):
        pass

    @abstractmethod
    async def get_stream_identifier(self) -> str:
        pass