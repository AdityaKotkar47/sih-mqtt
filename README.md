# Indoor Positioning System using MQTT

This project implements an indoor positioning system using MQTT protocol, ESP8266 devices, and RSSI-based triangulation.

## Project Structure
```
├── config/             # Configuration files for MQTT broker
├── backend/           # Python backend implementation
├── esp8266/          # ESP8266 device code
└── requirements.txt  # Python dependencies
```

## Setup Instructions

1. Install Python dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

2. Install Mosquitto MQTT Broker:
- Windows: Download from https://mosquitto.org/download/
- Linux: `sudo apt-get install mosquitto mosquitto-clients`

3. Configure MQTT Broker:
- Copy mosquitto.conf from config/ to your Mosquitto installation
- Start the broker service

4. Start the Backend:
```bash
cd backend
python main.py
```

## Features
- MQTT-based communication
- RSSI triangulation for position calculation
- FastAPI backend for data processing
- ESP8266 integration for RSSI measurements 