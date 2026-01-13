"""
Resonance Streaming Pipeline Orchestrator
Main entry point for the streaming pipeline system
"""

import asyncio
import logging
import signal
from typing import Optional

from .websocket_server import ResonanceWebSocketServer
from .state_synchronizer import StateSynchronizer
from .kafka_consumer import ResonanceConsumer
from .config import RESONANCE_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class ResonancePipeline:
    """
    Main orchestrator for Resonance streaming pipelines
    Manages WebSocket server, Kafka consumers, and state synchronization
    """
    
    def __init__(self):
        """Initialize the pipeline orchestrator"""
        self.websocket_server = ResonanceWebSocketServer()
        self.state_synchronizer = StateSynchronizer()
        self.kafka_consumer = ResonanceConsumer()
        self.is_running = False
        self.tasks = []
    
    def setup_kafka_handlers(self):
        """Setup handlers for Kafka consumer"""
        def on_state_update(message):
            logger.info(f"Received state update: {message.get('data')}")
        
        def on_frequency_sync(message):
            frequency = message.get('frequency')
            s_roi = message.get('s_roi')
            logger.info(f"Received frequency sync: {frequency} Hz, S-ROI: {s_roi}")
        
        def on_repository_event(message):
            event_type = message.get('event_type')
            source = message.get('source')
            logger.info(f"Received repository event from {source}: {event_type}")
        
        self.kafka_consumer.register_handler('state_update', on_state_update)
        self.kafka_consumer.register_handler('frequency_sync', on_frequency_sync)
        self.kafka_consumer.register_handler('repository_event', on_repository_event)
    
    async def start(self):
        """Start all pipeline components"""
        logger.info("Starting Resonance Streaming Pipeline...")
        logger.info(f"Anchor: {RESONANCE_CONFIG['anchor']}")
        logger.info(f"Frequency: {RESONANCE_CONFIG['frequency']} Hz")
        logger.info(f"S-ROI Threshold: {RESONANCE_CONFIG['s_roi_threshold']}")
        
        self.is_running = True
        self.setup_kafka_handlers()
        
        # Start all components concurrently
        self.tasks = [
            asyncio.create_task(self.websocket_server.start()),
            asyncio.create_task(self.state_synchronizer.start()),
        ]
        
        # Start Kafka consumer in a separate task
        kafka_task = asyncio.create_task(self.run_kafka_consumer())
        self.tasks.append(kafka_task)
        
        logger.info("Resonance Streaming Pipeline started successfully")
        
        # Wait for all tasks
        await asyncio.gather(*self.tasks, return_exceptions=True)
    
    async def run_kafka_consumer(self):
        """Run Kafka consumer in async loop"""
        loop = asyncio.get_event_loop()
        while self.is_running:
            await loop.run_in_executor(None, self.kafka_consumer.process_messages, 1000, 10)
            await asyncio.sleep(0.1)
    
    async def stop(self):
        """Stop all pipeline components"""
        logger.info("Stopping Resonance Streaming Pipeline...")
        self.is_running = False
        
        # Stop all components
        await self.websocket_server.stop()
        await self.state_synchronizer.stop()
        self.kafka_consumer.close()
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        logger.info("Resonance Streaming Pipeline stopped")
    
    def handle_shutdown(self, sig):
        """Handle shutdown signals"""
        logger.info(f"Received signal {sig}, shutting down...")
        asyncio.create_task(self.stop())


async def main():
    """Main entry point for the streaming pipeline"""
    pipeline = ResonancePipeline()
    
    # Setup signal handlers
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda s=sig: pipeline.handle_shutdown(s))
    
    try:
        await pipeline.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
    finally:
        await pipeline.stop()


if __name__ == '__main__':
    asyncio.run(main())
