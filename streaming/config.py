"""
Resonance Streaming Pipeline Configuration
Configures Apache Kafka and WebSocket connections for inter-repository communication
"""

# Kafka Configuration
KAFKA_CONFIG = {
    'bootstrap_servers': ['localhost:9092'],
    'client_id': 'resonance-node',
    'group_id': 'resonance-group',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True,
}

# Kafka Topics
KAFKA_TOPICS = {
    'outbound': 'resonance.outbound',
    'inbound': 'resonance.inbound',
    'state_sync': 'resonance.state.sync',
    'lexamoris': 'resonance.lexamoris',
    'nexus': 'resonance.nexus',
}

# WebSocket Configuration
WEBSOCKET_CONFIG = {
    'host': '0.0.0.0',
    'port': 8765,
    'ping_interval': 20,
    'ping_timeout': 10,
}

# Resonance System Parameters
RESONANCE_CONFIG = {
    'frequency': 0.043,  # Hz - biological resonance frequency
    's_roi_threshold': 0.5020,  # Social Return on Integrity threshold
    'anchor': 'BOLZANO_71',
    'sync_interval': 1.0,  # seconds between state updates
}

# Node Endpoints
NODE_ENDPOINTS = {
    'lexamoris': {
        'websocket': 'ws://lexamoris-node:8766',
        'kafka_topic': 'resonance.lexamoris',
    },
    'nexus': {
        'websocket': 'ws://nexus-node:8767',
        'kafka_topic': 'resonance.nexus',
    },
}

# Message Types
MESSAGE_TYPES = {
    'STATE_UPDATE': 'state_update',
    'FREQUENCY_SYNC': 'frequency_sync',
    'S_ROI_UPDATE': 's_roi_update',
    'REPOSITORY_EVENT': 'repository_event',
    'HEARTBEAT': 'heartbeat',
}
