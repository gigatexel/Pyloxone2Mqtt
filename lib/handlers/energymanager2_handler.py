import copy
import re
import json
import logging
from ..const import LOX_MQTT_TEMPLATES, cfmt

_LOGGER = logging.getLogger(__name__)

def handle_energymanager2(key=None, value=None, LoxAPP3=None, additional_sensors=None, payload=None):

    if additional_sensors != None and payload != None:

        new_payload = None

        for entity in json.loads(payload):
            new_payload = additional_sensors["payload"]
            if entity["uuid"] not in additional_sensors["payload"]["cmps"]:
                new_payload["cmps"][entity["uuid"]] = {}
                new_payload["cmps"][entity["uuid"]].update({
                    "p": "sensor",
                    "unique_id": entity["uuid"],
                    "name": entity["name"],
                    "state_topic": f"homeassistant/{additional_sensors['topic'].split('/')[1]}/{entity['uuid']}",
                    "value_template": "{{ value_json }}",
                    "suggested_display_precision": 3,
                    "unit_of_measurement": "kW",
                    "state_class": "measurement",
                    "device_class": "power",
                    "retain": True
                })      
                new_topic = additional_sensors["topic"]          
            # already in the 
            else:
                new_topic = f"homeassistant/{additional_sensors['topic'].split('/')[1]}/{entity['uuid']}"
                new_payload = entity["ppwr"]
        return new_topic, new_payload

    else:

        topic = f"device/{key}/config"
        attributes = {}
        
        payload = copy.deepcopy(LOX_MQTT_TEMPLATES["EnergyManager2"])
        payload["dev"].update({
            "ids": key,
            "name": value["name"],
            "suggested_area": LoxAPP3["rooms"][value["room"]]["name"]
        })
        for state in ["Gpwr","Spwr","Ppwr", "MaxSpwr"]:
            attributes_topic = f"device/{key}/attributes_{state}"
            payload["cmps"][state].update({
                "unique_id": f"{key}_{state}",
                "state_topic": f"loxone2mqtt/{value['states'][state]}",
                "json_attributes_topic": f"homeassistant/{attributes_topic}_state",
            })
            attributes[attributes_topic]= {
                "Loxone Device ID": key,
                "Loxone State ID": value["states"][state],
                "Loxone Room": LoxAPP3["rooms"][value["room"]]["name"],
                "Loxone Category": LoxAPP3["cats"][value["cat"]]["name"],
                "Loxone Control": "EnergyManager2",
                "HA Device Class": "power",
                "HA State Class": "measurement"
                }

        for state in ["Ssoc", "MinSoc"]:
            attributes_topic = f"device/{key}/attributes_{state}"
            payload["cmps"][state].update({
                "unique_id": f"{key}_{state}",
                "state_topic": f"loxone2mqtt/{value['states'][state]}",
                "json_attributes_topic": f"homeassistant/{attributes_topic}_state",
            })
            attributes[attributes_topic]= {
                "Loxone Device ID": key,
                "Loxone State ID": value["states"][state],
                "Loxone Room": LoxAPP3["rooms"][value["room"]]["name"],
                "Loxone Category": LoxAPP3["cats"][value["cat"]]["name"],
                "Loxone Control": "EnergyManager2",
                "HA Device Class": "battery",
                "HA State Class": "measurement"
                }    

        return topic, payload, attributes