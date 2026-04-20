import time
import json
import random
import paho.mqtt.client as mqtt
import os

BROKER = os.getenv("MQTT_BROKER_URL", "mqtt")
PORT = 1883
TOPIC = "devices/sim_001/data"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def connect_mqtt():
    """Attempt reconnection until Mosquitto is fully started."""
    while True:
        try:
            client.connect(BROKER, PORT, 60)
            print(f"Connected to MQTT Broker at {BROKER}:{PORT}")
            break
        except Exception as e:
            print(f"Waiting for MQTT broker... {e}")
            time.sleep(3)

if __name__ == '__main__':
    print("Starting IoT Simulator Service...")
    connect_mqtt()
    client.loop_start()
    
    while True:
        payload = {
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 60.0), 2),
            "status": "active"
        }
        client.publish(TOPIC, json.dumps(payload))
        print(f"[SIMULATOR] Published to {TOPIC}: {payload}", flush=True)
        time.sleep(5)  # Sends telemetry every 5 seconds!
