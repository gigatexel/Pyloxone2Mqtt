cfmt = r"""(%(?:(?:[-+0 #]{0,5})(?:\d+|\*)?(?:\.(?:\d+|\*))?(?:h|l|ll|w|I|I32|I64)?[cCdiouxXeEfgGaAnpsSZ])|%%)"""

LOX_MQTT_TEMPLATES = {
    "Switch" : {
        "dev": {
            "mf": "Loxone",
            "mdl": "Switch",
        },
        "o": {"name": "Loxone2MQTT"},
        "cmps": {
            "id1": {
                "p": "switch",
                "payload_on": "1.0",
                "payload_off": "0.0",
                "state_on": "1.0",
                "state_off": "0.0",
                "command_template": "{{ 'on' if value == '1.0' else 'off' }}",
                "json_attributes_template": "{{ value_json | tojson }}",
                "device_class": "switch",
                "retain": True
            },
        },
        "qos": 2
    },
    "PresenceDetector" : {
        "dev": {
            "mf": "Loxone",
            "mdl": "Presence Detector",
        },
        "o": {"name": "Loxone2MQTT"},
        "cmps": {
            "id1": {
                "p": "binary_sensor",
                "payload_on": "1.0",
                "payload_off": "0.0",
                "state_on": "1.0",
                "state_off": "0.0",
                "command_template": "{{ 'on' if value == '1.0' else 'off' }}",
                "json_attributes_template": "{{ value_json | tojson }}",
                "device_class": "presence",
                "retain": True
            }
        },
        "qos": 2
    },
    "Jalousie": {
        "dev": {
            "mf": "Loxone",
            "mdl": "Jalousie",
        },
        "o": {"name": "Loxone2MQTT"},
        "cmps": {
            "id1": {
                "p": "cover",
                "payload_open": "1.0",
                "payload_close": "0.0",
                "position_open": "100",
                "position_closed": "0",
                "command_template": "{{ 'open' if value == '1.0' else 'close' }}",
                "json_attributes_template": "{{ value_json | tojson }}",
                "retain": True
            }
        },
        "qos": 2
        },
    "Gate": {
        "dev": {
            "mf": "Loxone",
            "mdl": "Gate",
        },
        "o": {"name": "Loxone2MQTT"},
        "cmps": {
            "id1": {
                "p": "cover",
                "payload_open": "1.0",
                "payload_close": "0.0",
                "position_open": "100",
                "position_closed": "0",
                "command_template": "{{ 'open' if value == '1.0' else 'close' }}",
                "json_attributes_template": "{{ value_json | tojson }}",
                "device_class": None,
                "retain": True
            }
        },
        "qos": 2
#         },
#    "LightControllerV2": {
#         "dev": {
#             "mf": "Loxone",
#             "mdl": "LightControllerV2",
#         },
#         "o": {"name": "Loxone2MQTT"},
#         "cmps": {
#             "id1": {
#                 "p": "cover",
#                 "json_attributes_template": "{{ value_json | tojson }}",
#                 "retain": True
#             }
#         },
#         "qos": 2
        },
    "InfoOnlyAnalog" : {
        "dev": {
            "mf": "Loxone",
            "mdl": "InfoOnlyAnalog",
        },
        "o": {"name": "Loxone2MQTT"},
        "cmps": {
            "id1": {
                "p": "sensor",
                "json_attributes_template": "{{ value_json | tojson }}",
                "device_class": "switch",
                "retain": True
            },
        },
        "qos": 2
    },
    "InfoOnlyDigital" : {
        "dev": {
            "mf": "Loxone",
            "mdl": "InfoOnlyDigital",
        },
        "o": {"name": "Loxone2MQTT"},
        "cmps": {
            "id1": {
                "p": "binary_sensor",
                "payload_off": "0.0",
                "payload_on": "1.0",
                "json_attributes_template": "{{ value_json | tojson }}",
                "retain": True
            },
        },
        "qos": 2
    }            
}