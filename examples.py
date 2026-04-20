#!/usr/bin/env python3
"""
Example usage of Resonance Streaming Pipeline
Demonstrates how to use the streaming infrastructure
"""

import asyncio
import logging
from streaming.kafka_producer import ResonanceProducer
from streaming.kafka_consumer import ResonanceConsumer
from streaming.state_synchronizer import StateSynchronizer
from streaming.websocket_server import ResonanceWebSocketServer
from streaming.config import RESONANCE_CONFIG

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_kafka_producer():
    """Example: Using Kafka Producer to send messages"""
    print("\n=== Kafka Producer Example ===\n")
    
    producer = ResonanceProducer()
    
    # Send state update
    print("Sending state update...")
    state_data = {
        'frequency': RESONANCE_CONFIG['frequency'],
        's_roi': RESONANCE_CONFIG['s_roi_threshold'],
        'status': 'operational',
        'anchor': RESONANCE_CONFIG['anchor'],
    }
    producer.send_state_update(state_data)
    
    # Send frequency sync
    print("Sending frequency synchronization...")
    producer.send_frequency_sync(0.043, 0.5020)
    
    # Send repository event
    print("Sending repository event...")
    event_data = {
        'sha': 'abc123def456',
        'message': 'Add streaming pipelines',
        'author': 'hannesmitterer',
        'timestamp': '2026-01-13T02:00:00Z',
    }
    producer.send_repository_event('commit', event_data)
    
    # Send to specific node
    print("Sending event to LexAmoris node...")
    producer.send_repository_event('update', {'status': 'active'}, target_node='lexamoris')
    
    # Send heartbeat
    print("Sending heartbeat...")
    producer.send_heartbeat()
    
    producer.close()
    print("\nProducer example completed!")


def example_kafka_consumer():
    """Example: Using Kafka Consumer to receive messages"""
    print("\n=== Kafka Consumer Example ===\n")
    
    consumer = ResonanceConsumer()
    
    # Register custom handlers
    def on_state_update(message):
        print(f"Received state update: {message.get('data')}")
    
    def on_frequency_sync(message):
        freq = message.get('frequency')
        s_roi = message.get('s_roi')
        print(f"Received frequency sync: {freq} Hz, S-ROI: {s_roi}")
    
    def on_repository_event(message):
        event_type = message.get('event_type')
        print(f"Received repository event: {event_type}")
    
    consumer.register_handler('state_update', on_state_update)
    consumer.register_handler('frequency_sync', on_frequency_sync)
    consumer.register_handler('repository_event', on_repository_event)
    
    print("Listening for messages (simulated)...")
    print("In a real setup, this would process messages from Kafka")
    
    # Note: In simulation mode, this won't actually receive messages
    # With real Kafka, you would call: consumer.process_messages()
    
    consumer.close()
    print("\nConsumer example completed!")


async def example_state_synchronizer():
    """Example: Using State Synchronizer"""
    print("\n=== State Synchronizer Example ===\n")
    
    sync = StateSynchronizer()
    
    # Get current state
    print(f"Initial state: {sync.get_state()}")
    
    # Update state
    print("\nUpdating state...")
    sync.update_state({
        'frequency': 0.043,
        's_roi': 0.5030,
        'status': 'supraleitend',
    })
    
    print(f"Updated state: {sync.get_state()}")
    
    # Initialize clients (in simulation mode)
    print("\nInitializing node clients...")
    sync.initialize_clients()
    
    print("\nState synchronizer example completed!")


async def example_websocket_server():
    """Example: WebSocket Server (simulation)"""
    print("\n=== WebSocket Server Example ===\n")
    
    server = ResonanceWebSocketServer()
    
    print(f"WebSocket server configured on {server.config['host']}:{server.config['port']}")
    print("In a real setup, this would start accepting connections")
    print("Clients could connect to ws://localhost:8765")
    
    # Note: In a real scenario, you would await server.start()
    # For this example, we just show the configuration
    
    print("\nWebSocket server example completed!")


async def run_examples():
    """Run all examples"""
    print("\n" + "="*60)
    print("Resonance Streaming Pipeline - Usage Examples")
    print("="*60)
    
    # Kafka examples (synchronous)
    example_kafka_producer()
    example_kafka_consumer()
    
    # Async examples
    await example_state_synchronizer()
    await example_websocket_server()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60 + "\n")
    
    print("Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Start Kafka: docker-compose up -d kafka")
    print("3. Run the pipeline: python resonance_cli.py start")
    print("4. Or run pipeline programmatically: python -m streaming.pipeline")


if __name__ == '__main__':
    asyncio.run(run_examples())
