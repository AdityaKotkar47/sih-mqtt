import paho.mqtt.client as mqtt
import json
import time
import os
from dotenv import load_dotenv
import websockets
import asyncio

# Load environment variables
load_dotenv()

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "backend")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "backend_password")

# Test device data
def generate_test_data():
    return {
        "device_id": "esp8266_001",
        "rssi": -65 + (time.time() % 10),  # Varying RSSI
        "timestamp": time.time()
    }

# MQTT Publisher
def publish_test_data():
    client = mqtt.Client("test_publisher")
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()
    return client

async def publish_periodic(client, interval=2):
    """Publish test data periodically"""
    while True:
        test_data = generate_test_data()
        topic = f"device/{test_data['device_id']}/rssi"
        client.publish(topic, json.dumps(test_data))
        print(f"Published test data to {topic}: {test_data}")
        await asyncio.sleep(interval)

# WebSocket Client
async def websocket_client():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        try:
            while True:
                message = await websocket.recv()
                print(f"Received from WebSocket: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")

async def main():
    # Start MQTT publisher
    mqtt_client = publish_test_data()
    
    # Create tasks for publishing and receiving
    publish_task = asyncio.create_task(publish_periodic(mqtt_client))
    websocket_task = asyncio.create_task(websocket_client())
    
    try:
        # Wait for both tasks
        await asyncio.gather(publish_task, websocket_task)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    print("Starting test script...")
    print("1. Make sure Mosquitto broker is running")
    print("2. Make sure FastAPI backend is running")
    print("3. This script will publish MQTT messages and listen for WebSocket updates")
    asyncio.run(main()) 