# PyLoxone2Mqtt
## Install for development
```bash
pip install -r requirements.txt
create a .env file next to the main.py
fill out the .env file with the necessary information
run the main.py
```


## Env File with the following content
```dotenv
LOG_LEVEL=INFO

# Mqtt
MQTT_BROKER=
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_PORT=1883
MQTT_TOPICS="mqtt2loxone/#"  # Do not change this for now

# Loxone
WEBSOCKET_URL=
WEBSOCKET_USERNAME=
WEBSOCKET_PASSWORD=

```