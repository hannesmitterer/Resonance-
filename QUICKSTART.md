# Quick Start Guide - Resonance Streaming Pipelines

Get the Resonance streaming pipeline up and running in 5 minutes.

## Installation

```bash
# Clone the repository
git clone https://github.com/hannesmitterer/Resonance-.git
cd Resonance-

# Install Python dependencies
pip install -r requirements.txt

# Optional: Install actual Kafka and WebSocket libraries
pip install kafka-python websockets
```

## Run with Docker (Recommended)

```bash
# Start everything (Kafka, ZooKeeper, Resonance pipeline)
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f resonance-pipeline

# Stop everything
docker-compose down
```

## Run Locally

### 1. Start Kafka (Required)

```bash
docker-compose up -d kafka zookeeper
```

### 2. Start Resonance Pipeline

```bash
# Using CLI
python resonance_cli.py start

# Or programmatically
python -m streaming.pipeline
```

## Basic Usage

### Show Configuration

```bash
python resonance_cli.py config
```

### Send Test Messages

```bash
# Send state update
python resonance_cli.py send --type state --message "System operational"

# Send frequency sync
python resonance_cli.py send --type frequency

# Send repository event to LexAmoris
python resonance_cli.py send --type event --target lexamoris --message "New commit"
```

### Run Examples

```bash
python examples.py
```

## Verify Installation

### Check All Tests Pass

```bash
python -m unittest discover tests/ -v
```

Expected output: `Ran 18 tests ... OK`

### Access Kafka UI

Open http://localhost:8080 in your browser to monitor Kafka topics and messages.

### Test WebSocket Connection

```bash
# Install wscat
npm install -g wscat

# Connect to WebSocket server
wscat -c ws://localhost:8765
```

## What's Next?

1. **Read the Documentation**: See [streaming/README.md](streaming/README.md)
2. **Integration Guide**: See [INTEGRATION.md](INTEGRATION.md) for connecting LexAmoris and Nexus
3. **Customize Configuration**: Edit `streaming/config.py`
4. **Monitor Messages**: Use Kafka UI at http://localhost:8080

## Troubleshooting

### Docker Issues

```bash
# Remove all containers and start fresh
docker-compose down -v
docker-compose up -d
```

### Port Already in Use

```bash
# Change ports in docker-compose.yml
# Or stop conflicting services
sudo lsof -i :9092  # Kafka
sudo lsof -i :8765  # WebSocket
```

### Python Import Errors

```bash
# Make sure you're in the right directory
cd /path/to/Resonance-

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Key Features

✅ **Apache Kafka** - Distributed message streaming  
✅ **WebSockets** - Real-time bidirectional communication  
✅ **State Synchronization** - Automatic state sync across nodes  
✅ **Frequency Sync** - 0.043 Hz resonance frequency synchronization  
✅ **Multi-Node** - Connect to LexAmoris and Nexus repositories  
✅ **Docker Support** - Easy deployment with docker-compose  
✅ **CLI Tool** - Simple command-line interface  
✅ **Comprehensive Tests** - 18 unit tests covering all components  

## Architecture

```
Resonance Node
├── Kafka Producer → Sends messages to other nodes
├── Kafka Consumer → Receives messages from other nodes
├── WebSocket Server → Accepts incoming connections
├── WebSocket Client → Connects to other nodes
└── State Synchronizer → Manages state across all nodes
```

## Support

- **Documentation**: [streaming/README.md](streaming/README.md)
- **Integration**: [INTEGRATION.md](INTEGRATION.md)
- **Examples**: [examples.py](examples.py)
- **Tests**: [tests/](tests/)
