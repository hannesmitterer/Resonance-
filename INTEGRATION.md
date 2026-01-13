# Integration Guide for Streaming Pipelines

This guide explains how to integrate the Resonance streaming pipelines with LexAmoris and Nexus repositories.

## Architecture Overview

```
┌──────────────┐         Kafka Topics          ┌──────────────┐
│              │◄──────────────────────────────►│              │
│  Resonance   │   resonance.lexamoris          │  LexAmoris   │
│              │◄──────────────────────────────►│              │
└──────┬───────┘   WebSocket (ws://8766)        └──────────────┘
       │
       │           Kafka Topics
       │           resonance.nexus
       ▼           WebSocket (ws://8767)
┌──────────────┐
│              │◄──────────────────────────────►┌──────────────┐
│   Nexus      │                                 │    Kafka     │
│              │                                 │   Cluster    │
└──────────────┘                                 └──────────────┘
```

## Setup Instructions

### 1. Prerequisites

Install required dependencies:

```bash
pip install -r requirements.txt
```

For production use with actual Kafka and WebSocket support:

```bash
pip install kafka-python websockets
```

### 2. Start Kafka Infrastructure

Using Docker Compose (recommended):

```bash
docker-compose up -d kafka zookeeper
```

This will start:
- ZooKeeper on port 2181
- Kafka on port 9092
- Kafka UI on port 8080 (optional monitoring)

### 3. Configure Node Endpoints

Edit `streaming/config.py` to update node endpoints:

```python
NODE_ENDPOINTS = {
    'lexamoris': {
        'websocket': 'ws://lexamoris-server:8766',
        'kafka_topic': 'resonance.lexamoris',
    },
    'nexus': {
        'websocket': 'ws://nexus-server:8767',
        'kafka_topic': 'resonance.nexus',
    },
}
```

### 4. Start the Streaming Pipeline

Using CLI:

```bash
python resonance_cli.py start
```

Using Docker:

```bash
docker-compose up resonance-pipeline
```

Programmatically:

```python
import asyncio
from streaming.pipeline import ResonancePipeline

async def main():
    pipeline = ResonancePipeline()
    await pipeline.start()

asyncio.run(main())
```

## Integration with LexAmoris

### LexAmoris Requirements

The LexAmoris repository should:

1. **Subscribe to Kafka topic**: `resonance.lexamoris`
2. **Publish to Kafka topic**: `resonance.inbound`
3. **Run WebSocket server on**: `ws://localhost:8766`
4. **Handle message types**:
   - `state_update` - Receive state updates from Resonance
   - `frequency_sync` - Synchronize 0.043 Hz frequency
   - `repository_event` - Receive repository events

### Sample LexAmoris Consumer

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'resonance.lexamoris',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    if data['type'] == 'state_update':
        # Handle state update
        print(f"State update: {data['data']}")
    elif data['type'] == 'frequency_sync':
        # Synchronize frequency
        print(f"Frequency: {data['frequency']} Hz")
```

### Sample LexAmoris WebSocket Server

```python
import asyncio
import websockets
import json

async def handle_client(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        # Process message from Resonance
        print(f"Received from Resonance: {data['type']}")
        
        # Send acknowledgment
        await websocket.send(json.dumps({
            'type': 'ack',
            'original_type': data['type']
        }))

start_server = websockets.serve(handle_client, "0.0.0.0", 8766)
asyncio.get_event_loop().run_until_complete(start_server)
```

## Integration with Nexus

### Nexus Requirements

The Nexus repository should:

1. **Subscribe to Kafka topic**: `resonance.nexus`
2. **Publish to Kafka topic**: `resonance.inbound`
3. **Run WebSocket server on**: `ws://localhost:8767`
4. **Handle message types**: Same as LexAmoris

### Configuration

Same pattern as LexAmoris, just use different port (8767) and topic (resonance.nexus).

## Message Protocol

### State Update Message

```json
{
  "type": "state_update",
  "timestamp": "2026-01-13T02:00:00+00:00",
  "anchor": "BOLZANO_71",
  "data": {
    "frequency": 0.043,
    "s_roi": 0.5020,
    "status": "operational"
  }
}
```

### Frequency Sync Message

```json
{
  "type": "frequency_sync",
  "timestamp": "2026-01-13T02:00:00+00:00",
  "frequency": 0.043,
  "s_roi": 0.5020,
  "anchor": "BOLZANO_71"
}
```

### Repository Event Message

```json
{
  "type": "repository_event",
  "timestamp": "2026-01-13T02:00:00+00:00",
  "event_type": "commit",
  "data": {
    "sha": "abc123",
    "message": "Update feature",
    "author": "user"
  },
  "source": "resonance"
}
```

### Heartbeat Message

```json
{
  "type": "heartbeat",
  "timestamp": "2026-01-13T02:00:00+00:00",
  "anchor": "BOLZANO_71",
  "frequency": 0.043,
  "s_roi": 0.5020
}
```

## Testing the Integration

### 1. Test Kafka Connection

```bash
# Send test message
python resonance_cli.py send --type state --message "Test"

# Check Kafka topics
docker exec -it resonance-kafka kafka-topics --list --bootstrap-server localhost:9093
```

### 2. Test WebSocket Connection

```bash
# Install wscat if needed
npm install -g wscat

# Connect to Resonance WebSocket server
wscat -c ws://localhost:8765

# Send test message
{"type": "heartbeat", "anchor": "TEST"}
```

### 3. Monitor Message Flow

Access Kafka UI at http://localhost:8080 to monitor:
- Topic message counts
- Consumer lag
- Message content

## Troubleshooting

### Kafka Connection Issues

```bash
# Check Kafka logs
docker-compose logs kafka

# Verify Kafka is running
docker-compose ps kafka
```

### WebSocket Connection Issues

```bash
# Check if WebSocket server is listening
netstat -tulpn | grep 8765

# Test with curl
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" http://localhost:8765
```

### No Messages Received

1. Verify Kafka topics exist
2. Check consumer group offsets
3. Ensure correct topic names in configuration
4. Verify network connectivity between services

## Production Deployment

### Security Considerations

1. **Enable Kafka SSL/TLS**
2. **Use WebSocket Secure (wss://)**
3. **Implement authentication**
4. **Use API keys for node communication**
5. **Enable message encryption**

### Scaling

1. **Multiple Kafka brokers** for high availability
2. **Consumer groups** for parallel processing
3. **Load balancing** for WebSocket connections
4. **Monitoring** with Prometheus/Grafana

### Monitoring

Monitor these metrics:
- Message throughput (messages/sec)
- Consumer lag
- WebSocket connections count
- Error rates
- Frequency drift from 0.043 Hz target

## Support

For issues or questions:
- Check logs: `docker-compose logs resonance-pipeline`
- Review configuration: `python resonance_cli.py config`
- Run tests: `python -m unittest discover tests/`
