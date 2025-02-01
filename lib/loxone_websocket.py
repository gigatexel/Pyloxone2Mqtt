import asyncio

import aiofiles
import websockets
from aiomqtt import Topic

from .event_bus import EventBus
import logging

from .pyloxone_api.connection import LoxoneConnection

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel("DEBUG")

class LoxoneWebSocketClient:
    def __init__(self, uri: str, host:str, port:str, username:str, password:str, event_bus: EventBus):

        self.uri = uri
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.event_bus = event_bus

    async def publish_to_eventbus(self, message: dict) -> None:
        _LOGGER.debug("Publishing message to event bus websocket_in %s", message)
        await self.event_bus.publish(Topic("websocket_in/"), message)

    async def token_safe(self, data) -> None:
         async with aiofiles.open("token.json", "w") as file:
            await file.write(str(data))

    async def token_load(self) -> None:
        try:
            async with aiofiles.open("token.json", "r") as file:
                content = await file.read()
                try:
                    content = eval(content)
                except:
                    return None
                return content
        except FileNotFoundError:
            return None

    async def connect_and_listen(self) -> None:
        token = await self.token_load()
        api = LoxoneConnection(
            host=self.host,
            port=int(self.port),
            username=self.username,
            password=self.password,
            token=token,
            token_safe_callback=self.token_safe
        )

        listening_task = asyncio.create_task(await api.start_listening(callback=self.publish_to_eventbus))

        # pass
        # while True:
        #     await asyncio.sleep(1)
        #     await self.event_bus.publish("websocket_in/", {"uuid":"asdfas"})

        # async with websockets.connect(self.uri) as websocket:
        #     while True:
        #         await asyncio.sleep(1)
        #         # message = await websocket.recv()
        #         # Publish WebSocket messages to the event bus
        #         await self.event_bus.publish("websocket_in", message)

    async def send(self, message: dict):
        """Send a message to the WebSocket."""
        _LOGGER.debug("Sending message to WebSocket %s", message )

        #async with websockets.connect(self.uri) as websocket:
        #    await websocket.send(message["payload"])
