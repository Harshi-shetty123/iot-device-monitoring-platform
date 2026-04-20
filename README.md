# IoT Device Monitoring Platform 🚀

A real-time, scalable back-end system for monitoring Internet of Things (IoT) devices, analyzing their metrics, and generating alerts. 

## 📖 Overview
This project serves as the core infrastructure for an IoT network. It manages device registration, handles secure real-time data ingestion via MQTT and REST, and caches data for low-latency dashboard visualization.

### What are the Devices Used?
In an IoT ecosystem, "devices" can be:
- **Temperature / Humidity Sensors (e.g., DHT11/22 on ESP32 or Raspberry Pi)**
- **Smart Thermostats**
- **Industrial Controllers (PLCs)**
- **Simulated Devices (Python Scripts)** for testing purposes.

These devices communicate with our server by sending lightweight telemetry payloads (typically JSON format).

### How Devices Communicate
Devices can securely publish their sensor metrics using two methods:
1. **MQTT (Message Queuing Telemetry Transport):** The primary and most efficient IoT protocol. Devices maintain a lightweight, continuous connection to the `Eclipse Mosquitto` broker on port `1883`, publishing data to specific topics like `devices/{device_id}/data`.
2. **REST API:** A fallback method where devices can POST JSON data directly to our Flask API's `/data` endpoint.

## 🏢 Server Details
The entire environment runs smoothly via **Docker Compose**:
- **Backend API (Flask):** The entry point logic, deployed via Gunicorn/Flask server.
- **Database (PostgreSQL 15):** Stores users, device assignments, and historical metrics permanently.
- **Cache (Redis 7):** Used to immediately fetch the most recent statistics for live dashboards without stressing the Database.
- **Message Broker (Mosquitto):** Handles rapid MQTT messages published by hardware devices.

## ⚙️ Quick Start

**1. Clone & Build**
```bash
git clone git@github.com:Harshi-shetty123/iot-device-monitoring-platform.git
cd iot-device-monitoring-platform
docker-compose up --build
```
**2. Test the API Endpoints**
Navigate to `http://localhost:5000/health` to confirm the network bridge is active!

---
*For an in-depth visual illustration of how the system works end-to-end, check out [architecture.md](./architecture.md).*
