# System Architecture & Flow Diagram

This document illustrates the end-to-end communication flow of the IoT Device Monitoring platform. We use **Mermaid** graphs to visualize how devices, the Flask API, databases, and clients interact.

## 1. High-Level Architecture
Here is the high-level architecture mapped to our containerized services.

```mermaid
graph TD
    %% Entities
    subgraph IoT Devices
    Sensor1[ESP32 / Raspberry Pi]
    Sensor2[Simulated Device]
    end

    subgraph Docker Local Network
    MQTT[Mosquitto Broker]
    FlaskAPI[Flask Backend API]
    Celery[Celery Background Workers]
    Postgres[(PostgreSQL DBS)]
    Redis[(Redis Cache)]
    end

    Client[Web Dashboard / Admin]

    %% Flow
    Sensor1 -- "Publishes MQTT data" --> MQTT
    Sensor2 -- "POST REST data" --> FlaskAPI
    MQTT -- "Subscribes/Ingests" --> FlaskAPI
    
    FlaskAPI -- "Persist History" --> Postgres
    FlaskAPI -- "Cache Live Data" --> Redis
    
    Client -- "HTTP Requests (JWT)" --> FlaskAPI
    
    Celery -- "Read Rules" --> Postgres
    Celery -- "Stream & Thresholds" --> Redis
    Celery -- "Triggers" --> Alerts[Email / SMS Logs]
```

## 2. Request Flow: Device Registration vs Data Ingestion

### Device Registration (Admin/User)
1. **User logs in** and receives a JWT token.
2. User sends `POST /devices` with device details.
3. The **Flask API** validates the JWT, generates a unique `api_key` or identifier for the device, and stores it in **PostgreSQL**.
4. The system grants the physical device access to start transmitting.

### Real-Time Data Ingestion Flow
```mermaid
sequenceDiagram
    participant Device as IoT Device
    participant Broker as Mosquitto (MQTT)
    participant API as Flask Backend
    participant Redis as Redis Cache
    participant DB as Postgres

    Device->>Broker: Publish JSON {temp: 22, humidity: 45} on topic 'devices/123/data'
    Broker->>API: Deliver Message (Consumer runs continuously)
    API->>Redis: Update 'latest' key for instant Dashboard access
    API->>DB: Asynchronously store historical metric row
```

## 3. Tech Rationale
* **Why Flask?** Provides a clean, minimalistic framework perfectly suited for crafting specific REST APIs without unnecessary overhead.
* **Why MQTT?** IoT devices typically lack vast processing power. MQTT is extremely lightweight and ensures fast, low-bandwidth data telemetry out-of-the-box.
* **Why Redis?** When a dashboard needs to render "Live" metrics for hundreds of devices, reading direct from Postgres is slow. Redis acts as a lightning-fast memory store.
