LOX_MQTT_TEMPLATES = {
    "Switch" : {
        "dev": {
            "ids": "dev_id",
            "name": "",
            "mf": "Loxone",
            "mdl": "Switch",
            "suggested_area": "",
        },
        "o": {"name": "Loxone2MQTT"},
        "cmps": {
            "id1": {
                "p": "switch",
                "unique_id": "",
                "name": "",
                "command_topic": "",
                "state_topic": "",
                "payload_on": "1.0",
                "payload_off": "0.0",
                "state_on": "1.0",
                "state_off": "0.0",
                "command_template": "{{ 'on' if value == '1.0' else 'off' }}",
                "json_attributes_topic": "",
                "json_attributes_template": "{{ value_json | tojson }}",
                "device_class": "switch",
                "retain": True
            }
        },
        "qos": 2
    },
    "PresenceDetector" : {
        "dev": {
            "ids": "dev_id",
            "name": "",
            "mf": "Loxone",
            "mdl": "Presence Detector",
            "suggested_area": "",
        },
        "o": {"name": "Loxone2MQTT"},
        "cmps": {
            "id1": {
                "p": "binary_sensor",
                "unique_id": "",
                "name": "",
                "command_topic": "",
                "state_topic": "",
                "payload_on": "1.0",
                "payload_off": "0.0",
                "state_on": "1.0",
                "state_off": "0.0",
                "command_template": "{{ 'on' if value == '1.0' else 'off' }}",
                "json_attributes_topic": "",
                "json_attributes_template": "{{ value_json | tojson }}",
                "device_class": "presence",
                "retain": True
            }
        },
        "qos": 2
    }
}