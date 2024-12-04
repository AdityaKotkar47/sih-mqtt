# Indoor Positioning System using MQTT

This project implements an indoor positioning system using MQTT protocol, ESP8266 devices, and RSSI-based triangulation.

## Project Structure
```
├── config/             # Configuration files for MQTT broker
│   ├── mosquitto.conf  # Mosquitto broker configuration
│   ├── acl            # Access Control List rules
│   └── passwd         # Password file (not in git)
├── backend/           # Python backend implementation
│   ├── main.py       # FastAPI + MQTT integration
│   ├── test_mqtt_ws.py # Test script for MQTT and WebSocket
│   └── .env          # Environment variables (not in git)
├── esp8266/          # ESP8266 device code (coming soon)
└── requirements.txt  # Python dependencies
```

## Setup Instructions

1. Install Python dependencies:
```bash
python -m venv broker
.\broker\Scripts\activate  # On Windows
pip install -r requirements.txt
```

2. Install Mosquitto MQTT Broker:
- Windows: Download from https://mosquitto.org/download/
- Add Mosquitto to system PATH
- Copy configuration files:
  ```bash
  # Copy from config/ to your Mosquitto installation:
  - mosquitto.conf
  - acl
  - passwd
  ```

3. Configure Environment:
Create `.env` file in backend/ with:
```env
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=backend
MQTT_PASSWORD=your_password
```

4. Start Services:
```bash
# Terminal 1: Start Mosquitto
mosquitto -c .\config\mosquitto.conf

# Terminal 2: Start FastAPI Backend
cd backend
uvicorn main:app --reload

# Terminal 3 (Optional): Run Test Script
cd backend
python test_mqtt_ws.py
```

## Features
- MQTT-based communication with authentication and ACL
- Real-time WebSocket updates for client applications
- FastAPI backend for data processing and API endpoints
- Simulated RSSI data generation for testing
- Scalable architecture for multiple ESP8266 devices

## Testing
The test script (`test_mqtt_ws.py`) provides:
- MQTT message publishing simulation
- WebSocket client connection
- Real-time data flow verification
- Varying RSSI values for testing

## Security
- MQTT broker authentication enabled
- Access Control List (ACL) implemented
- Secure password storage
- Environment variable configuration

## Coming Soon
- ESP8266 device integration
- RSSI triangulation algorithm
- Position calculation and tracking
- Flutter frontend integration