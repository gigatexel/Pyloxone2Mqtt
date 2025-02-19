import copy
import re
from ..const import LOX_MQTT_TEMPLATES, cfmt

def handle_energymanager2(key, value, LoxAPP3):

    topic = f"device/{key}/config"
    attributes_topic = f"device/{key}/attributes"


    payload = copy.deepcopy(LOX_MQTT_TEMPLATES["EnergyManager2"])
    payload["dev"].update({
        "ids": key,
        "name": value["name"],
        "suggested_area": LoxAPP3["rooms"][value["room"]]["name"]
    })
    for state in ["Gpwr","Spwr","Ppwr"]:
        payload["cmps"][state].update({
            "unique_id": f"{key}_{state}",
            "state_topic": f"loxone2mqtt/{value['states'][state]}",
            "json_attributes_topic": f"homeassistant/{attributes_topic}_state",
        })

        attributes_payload = {
        #     "Loxone Device ID": key,
        #     "Loxone State ID": value["states"][state],
        #     "Loxone Room": LoxAPP3["rooms"][value["room"]]["name"],
        #     "Loxone Category": LoxAPP3["cats"][value["cat"]]["name"],
        #     "Loxone Control": "InfoOnlyDigital",
        #     "HA Device Class": device_class,
        #     "HA State Class": state_class
        }

    return topic, attributes_topic, payload, attributes_payload