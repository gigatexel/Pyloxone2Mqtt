import logging
import json
import copy

from aiomqtt import Client, MqttError
from .event_bus import EventBus
from .const import LOX_MQTT_TEMPLATES
from .handlers import switch_handler, presence_detector_handler, jalousie_handler, gate_handler

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class HomeAssistant:
    def __init__(
        self,
        broker: str,
        event_bus: EventBus,
        topics: list[str],
        username: str = None,
        password: str = None,
        port: int = None,
        tls: bool = False,
        tls_cert: str = None,
    ):
        """
        Initialize the MQTT client and Home Assistant integration.
        """
        self.broker = broker
        self.event_bus = event_bus
        self.topics = topics
        self.username = username
        self.password = password
        self.port = port
        self.tls = tls
        self.tls_cert = tls_cert
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10
        self.reconnect_delay = 10  # seconds
        self.LoxAPP3 = ""
        self.client = None  # Persistent MQTT client

    async def connect(self):
        """
        Establish a persistent MQTT connection.
        """
        if self.client is None:
            self.client = Client(
                self.broker,
                username=self.username,
                password=self.password,
                port=self.port,
                tls_context=self._get_tls_context() if self.tls else None,
            )
            await self.client.__aenter__()
            _LOGGER.debug("Connected to MQTT broker")

    async def disconnect(self):
        """
        Disconnect the persistent MQTT connection.
        """
        if self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None
            _LOGGER.debug("Disconnected from MQTT broker")

    async def generate_ha_mqtt_autodiscovery(self, messages: list[dict]):
        publish_queue = []

        for message in messages:
            if message["topic"].matches("loxone2mqtt/LoxAPP3"):
                self.LoxAPP3 = message["payload"]

                for key, value in self.LoxAPP3["controls"].items():
                    if value["type"] in LOX_MQTT_TEMPLATES:
                        handler = self._get_handler(value["type"])
                        if handler:
                            topic, attributes_topic, payload, attributes_payload = handler(key, value, self.LoxAPP3)
                            publish_queue.append({"topic": topic, "payload": json.dumps(payload)})
                            publish_queue.append({"topic": attributes_topic, "payload": json.dumps(attributes_payload)})

        if publish_queue:
            await self.publish(publish_queue)

        # Publish all collected messages at once
        if publish_queue:
            await self.publish(publish_queue)
    def _get_handler(self, control_type: str):
        handlers = {
            "Switch": switch_handler.handle_switch,
            "PresenceDetector": presence_detector_handler.handle_presence_detector,
            "Jalousie": jalousie_handler.handle_jalousie,
            "Gate": gate_handler.handle_gate,
        }
        return handlers.get(control_type)

    async def publish(self, messages: dict | list[dict]):
        """
        Publish MQTT messages using the persistent connection.
        """
        await self.connect()
        if isinstance(messages, list):
            for message in messages:
                await self._publish(self.client, message)
        else:
            await self._publish(self.client, messages)

    @staticmethod
    async def _publish(client: Client, message: dict):
        """
        Publish a single MQTT message with error handling.
        """
        try:
            await client.publish(f"homeassistant/{message['topic']}", str(message["payload"]))
            _LOGGER.debug(f"Published {message['topic']}: {message['payload']}")
        except MqttError as e:
            _LOGGER.error(f"Failed to publish {message['topic']}: {e}")

    def _get_tls_context(self):
        """
        Create and return an SSL/TLS context if TLS is enabled.
        """
        import ssl
        if not self.tls_cert:
            raise ValueError("TLS is enabled, but no certificate file is provided.")
        return ssl.create_default_context(cafile=self.tls_cert)
