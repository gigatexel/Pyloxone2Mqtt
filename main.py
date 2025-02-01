import asyncio
import logging
# from mqtt_client import MQTTClient
# from websocket_client import WebSocketClient
# from api_server import create_api_server
# from event_bus import EventBus
import os

from lib.event_bus import EventBus
from lib.loxone_websocket import LoxoneWebSocketClient
from lib.mqtt_client import MQTTClient

import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file


# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def main():
    logging.info("Starting application with log level: %s", log_level)

    # Read MQTT configuration from environment variables
    mqtt_broker = os.getenv("MQTT_BROKER", None)
    mqtt_username = os.getenv("MQTT_USERNAME")
    mqtt_password = os.getenv("MQTT_PASSWORD")
    mqtt_tls = os.getenv("MQTT_TLS", "false").lower() == "true"
    mqtt_tls_cert = os.getenv("MQTT_TLS_CERT")
    mqtt_topics = os.getenv("MQTT_TOPICS", "#").split(",")  # Default: subscribe to all topics

    # Read FastAPI and WebSocket configuration
    # start_fastapi = os.getenv("START_FASTAPI", "true").lower() == "true"
    # start_websocket = os.getenv("START_WEBSOCKET", "true").lower() == "true"

    # Loxone WebSocket configuration
    websocket_url = os.getenv("WEBSOCKET_URL",None)
    websocket_port = os.getenv("WEBSOCKET_PORT", "443")  # Default: secure WebSocket
    websocket_username = os.getenv("WEBSOCKET_USERNAME")
    websocket_password = os.getenv("WEBSOCKET_PASSWORD")

    # Instantiate the event bus
    event_bus = EventBus()

    # # Initialize optional components
    websocket_client = (
        LoxoneWebSocketClient(
            uri="None",
            host=websocket_url,
            port=websocket_port,
            username=websocket_username,
            password=websocket_password,
            event_bus=event_bus,
        )
        #if start_websocket
        #else None
    )

    # # Initialize components
    # Initialize MQTT client with authentication and TLS
    # Initialize MQTT client
    mqtt_client = MQTTClient(
        broker=mqtt_broker,
        event_bus=event_bus,
        topics=mqtt_topics,
        username=mqtt_username,
        password=mqtt_password,
        tls=mqtt_tls,
        tls_cert=mqtt_tls_cert,
    )

    if websocket_client:
        pass
       #await event_bus.subscribe("websocket_out", websocket_client.send)

    # websocket_client = WebSocketClient(uri="ws://websocket.example.com", event_bus=event_bus)
    # app = create_api_server(event_bus)
    #
    # # Subscribe components to the event bus
    #async def subscribe(message:dict):
    #    print("Got message", message)
    #await subscribe("#", mqtt_client.publish)
    # await subscribe("#", mqtt_client.publish)
    # async def subscribe(message:dict):
    #     await asyncio.sleep(0)
    #     print("Got message", message)

    await event_bus.subscribe("pyloxone", websocket_client.send)
    await event_bus.subscribe("loxone2mqtt", mqtt_client.publish)


    # # Start tasks
    #mqtt_task = asyncio.create_task(mqtt_client.connect_and_listen())
    # websocket_task = asyncio.create_task(websocket_client.connect_and_listen())
    #event_bus_task = asyncio.create_task(event_bus.run())
    ###
    # # Start FastAPI as a task
    # api_task = asyncio.create_task(uvicorn.run(app, host="0.0.0.0", port=8000))
    #    # Start tasks
    # Start tasks

    # await event_bus.subscribe("mqtt_out", mqtt_client.publish)

    tasks = [
        asyncio.create_task(mqtt_client.connect_and_listen()),
        asyncio.create_task(websocket_client.connect_and_listen()),
        asyncio.create_task(event_bus.run()),
    ]

    # await asyncio.gather(mqtt_task, event_bus_task) #, websocket_task, event_bus_task, api_task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
