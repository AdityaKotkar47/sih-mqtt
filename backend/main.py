import os
from fastapi import FastAPI
from paho.mqtt import client as mqtt_client
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI(title="Indoor Positioning System")

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "backend")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "backend_password")
MQTT_CLIENT_ID = "backend_service"

# MQTT client setup
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            # Subscribe to all device RSSI topics
            client.subscribe("device/+/rssi")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            device_id = msg.topic.split('/')[1]
            process_rssi_data(device_id, payload)
        except Exception as e:
            print(f"Error processing message: {e}")

    client = mqtt_client.Client(MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client

def process_rssi_data(device_id: str, data: dict):
    """Process RSSI data and calculate position"""
    # TODO: Implement triangulation logic
    print(f"Received RSSI data from device {device_id}: {data}")

# Create MQTT client instance
mqtt_client = connect_mqtt()

@app.on_event("startup")
async def startup_event():
    """Start MQTT client loop in a separate thread"""
    mqtt_client.loop_start()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup MQTT client connection"""
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

@app.get("/")
async def root():
    return {"status": "running", "service": "Indoor Positioning System"} 