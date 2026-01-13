# Resonance Streaming Pipeline

This directory contains the streaming pipeline infrastructure for real-time communication between the Resonance repository and other nodes (LexAmoris and Nexus).

## Architecture

The streaming pipeline uses two primary protocols for communication:

1. **Apache Kafka** - For reliable, distributed message streaming
2. **WebSockets** - For real-time bidirectional communication

### Components

- **Kafka Producer** (`kafka_producer.py`) - Sends data streams to other nodes
- **Kafka Consumer** (`kafka_consumer.py`) - Receives data streams from other nodes
- **WebSocket Server** (`websocket_server.py`) - Handles incoming WebSocket connections
- **WebSocket Client** (`websocket_client.py`) - Connects to other node WebSocket servers
- **State Synchronizer** (`state_synchronizer.py`) - Manages state synchronization across all nodes
- **Pipeline Orchestrator** (`pipeline.py`) - Main entry point that coordinates all components

## Message Types

The pipeline supports the following message types:

- `state_update` - Broadcasts state changes across nodes
- `frequency_sync` - Synchronizes the 0.043 Hz resonance frequency
- `s_roi_update` - Updates Social Return on Integrity values
- `repository_event` - Notifies about repository changes (commits, pushes, etc.)
- `heartbeat` - Maintains connection health

## Configuration

Configuration is managed in `config.py`:

- **Kafka settings** - Bootstrap servers, topics, client configuration
- **WebSocket settings** - Host, port, ping intervals
- **Resonance parameters** - Frequency (0.043 Hz), S-ROI threshold, anchor point
- **Node endpoints** - LexAmoris and Nexus connection details

## Usage

### Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start Kafka (using Docker)
docker-compose up -d kafka
```

### Running the Pipeline

```python
# Run the complete pipeline
python -m streaming.pipeline
```

### Programmatic Usage

```python
from streaming.state_synchronizer import StateSynchronizer
from streaming.websocket_server import ResonanceWebSocketServer
import asyncio

# Initialize components
synchronizer = StateSynchronizer()
server = ResonanceWebSocketServer()

# Start the system
async def run():
    await asyncio.gather(
        server.start(),
        synchronizer.start()
    )

asyncio.run(run())
```

### Sending Messages

```python
from streaming.kafka_producer import ResonanceProducer

producer = ResonanceProducer()

# Send state update
producer.send_state_update({
    'frequency': 0.043,
    's_roi': 0.5020,
    'status': 'supraleitend'
})

# Send repository event
producer.send_repository_event('commit', {
    'sha': 'abc123',
    'message': 'Update resonance frequency',
    'author': 'hannesmitterer'
}, target_node='lexamoris')

producer.close()
```

### Receiving Messages

```python
from streaming.kafka_consumer import ResonanceConsumer

consumer = ResonanceConsumer()

# Register custom handler
def handle_state_update(message):
    print(f"State update received: {message}")

consumer.register_handler('state_update', handle_state_update)

# Process messages
consumer.process_messages()
consumer.close()
```

## WebSocket API

### Server Endpoint

- **URL**: `ws://localhost:8765`
- **Protocol**: JSON messages

### Client Connection

```javascript
const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => {
    // Send frequency sync
    ws.send(JSON.stringify({
        type: 'frequency_sync',
        frequency: 0.043,
        's_roi': 0.5020,
        anchor: 'BOLZANO_71'
    }));
};

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    console.log('Received:', message);
};
```

## Kafka Topics

- `resonance.outbound` - Messages sent from Resonance to all nodes
- `resonance.inbound` - Messages received by Resonance from all nodes
- `resonance.state.sync` - State synchronization messages
- `resonance.lexamoris` - Messages specifically for LexAmoris node
- `resonance.nexus` - Messages specifically for Nexus node

## State Synchronization

The state synchronizer automatically:

1. Broadcasts state updates every 1 second (configurable)
2. Synchronizes frequency (0.043 Hz) across all nodes
3. Maintains S-ROI (Social Return on Integrity) values
4. Sends heartbeats to detect connection issues
5. Reconnects automatically on connection loss

## Integration with Resonance System

The streaming pipeline integrates with the Resonance system parameters:

- **Frequency**: 0.043 Hz (biological resonance)
- **S-ROI**: Social Return on Integrity threshold (0.5020)
- **Anchor**: BOLZANO_71 (Portici 71, Bolzano)
- **Lex Amore Protocol**: Ethical framework integration

## Monitoring

The pipeline provides comprehensive logging:

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Run with verbose logging
python -m streaming.pipeline
```

## Security Considerations

- WebSocket connections support ping/pong for connection health
- Kafka uses consumer groups for load balancing
- All messages include timestamps for ordering
- Message validation prevents malformed data

## Troubleshooting

### Kafka Connection Issues

```bash
# Check Kafka status
docker-compose ps kafka

# View Kafka logs
docker-compose logs kafka
```

### WebSocket Connection Issues

```bash
# Test WebSocket connection
wscat -c ws://localhost:8765
```

### Message Delivery Issues

- Check Kafka consumer group offsets
- Verify topic configuration
- Ensure proper network connectivity between nodes

## Future Enhancements

- Message encryption for secure transmission
- Message acknowledgment and retry logic
- Advanced load balancing across multiple consumers
- Integration with other protocols (gRPC, MQTT)
- Metrics and performance monitoring
