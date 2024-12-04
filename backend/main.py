import os
from fastapi import FastAPI, WebSocket
from paho.mqtt import client as mqtt_client
import json
from dotenv import load_dotenv
from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI(title="Indoor Positioning System")

# Store active WebSocket connections
active_connections: List[WebSocket] = []

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "backend")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "backend_password")
MQTT_CLIENT_ID = "backend_service"

# Create event loop for MQTT async operations
executor = ThreadPoolExecutor()
loop = asyncio.get_event_loop()

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.disconnect(connection)

manager = ConnectionManager()

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
            # Schedule the coroutine on the event loop
            asyncio.run_coroutine_threadsafe(process_rssi_data(device_id, payload), loop)
        except Exception as e:
            print(f"Error processing message: {e}")

    client = mqtt_client.Client(MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client

async def process_rssi_data(device_id: str, data: dict):
    """Process RSSI data and calculate position"""
    message = f"Received RSSI data from device {device_id}: {data}"
    print(message)
    # Broadcast to all connected WebSocket clients
    await manager.broadcast(json.dumps({
        "device_id": device_id,
        "data": data
    }))

# Create MQTT client instance
mqtt_client = connect_mqtt()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle any incoming WebSocket messages if needed
            print(f"Received WebSocket message: {data}")
    except:
        manager.disconnect(websocket)

@app.on_event("startup")
async def startup_event():
    """Start MQTT client loop in a separate thread"""
    mqtt_client.loop_start()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup MQTT client connection"""
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    executor.shutdown()

@app.get("/")
async def root():
    return {"status": "running", "service": "Indoor Positioning System"} 