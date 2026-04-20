"""
Apache Kafka Consumer for Resonance Streaming Pipeline
Receives data streams from other nodes (LexAmoris, Nexus)
"""

import json
import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime

try:
    from kafka import KafkaConsumer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logging.warning("kafka-python not installed. Kafka functionality will be simulated.")

from .config import KAFKA_CONFIG, KAFKA_TOPICS, MESSAGE_TYPES

logger = logging.getLogger(__name__)


class ResonanceConsumer:
    """
    Kafka consumer for receiving data streams from other nodes
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, topics: Optional[List[str]] = None):
        """
        Initialize Kafka consumer
        
        Args:
            config: Optional custom Kafka configuration
            topics: List of topics to subscribe to
        """
        self.config = config or KAFKA_CONFIG
        self.topics = topics or [KAFKA_TOPICS['inbound'], KAFKA_TOPICS['state_sync']]
        self.consumer = None
        self.is_connected = False
        self.message_handlers = {}
        
        if KAFKA_AVAILABLE:
            self._initialize_consumer()
        else:
            logger.warning("Running in simulation mode - no actual Kafka connection")
    
    def _initialize_consumer(self):
        """Initialize the Kafka consumer connection"""
        try:
            self.consumer = KafkaConsumer(
                *self.topics,
                bootstrap_servers=self.config['bootstrap_servers'],
                group_id=self.config['group_id'],
                auto_offset_reset=self.config['auto_offset_reset'],
                enable_auto_commit=self.config['enable_auto_commit'],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
            )
            self.is_connected = True
            logger.info(f"Kafka consumer connected, subscribed to: {self.topics}")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {e}")
            self.is_connected = False
    
    def register_handler(self, message_type: str, handler: Callable[[Dict[str, Any]], None]):
        """
        Register a handler function for a specific message type
        
        Args:
            message_type: Type of message to handle (from MESSAGE_TYPES)
            handler: Callback function to process the message
        """
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for message type: {message_type}")
    
    def process_messages(self, timeout_ms: int = 1000, max_messages: Optional[int] = None):
        """
        Process incoming messages from Kafka
        
        Args:
            timeout_ms: Timeout for polling messages in milliseconds
            max_messages: Maximum number of messages to process (None for continuous)
        """
        if not KAFKA_AVAILABLE or not self.is_connected:
            logger.info("[SIMULATED] Would be processing messages from Kafka")
            return
        
        message_count = 0
        try:
            for message in self.consumer:
                self._handle_message(message.value)
                message_count += 1
                
                if max_messages and message_count >= max_messages:
                    break
        except KeyboardInterrupt:
            logger.info("Message processing interrupted by user")
        except Exception as e:
            logger.error(f"Error processing messages: {e}")
    
    def _handle_message(self, message: Dict[str, Any]):
        """
        Internal method to handle incoming messages
        
        Args:
            message: Decoded message from Kafka
        """
        try:
            message_type = message.get('type')
            if not message_type:
                logger.warning("Received message without type field")
                return
            
            logger.debug(f"Processing message type: {message_type}")
            
            # Call registered handler if available
            handler = self.message_handlers.get(message_type)
            if handler:
                handler(message)
            else:
                # Default handling based on message type
                if message_type == MESSAGE_TYPES['STATE_UPDATE']:
                    self._handle_state_update(message)
                elif message_type == MESSAGE_TYPES['FREQUENCY_SYNC']:
                    self._handle_frequency_sync(message)
                elif message_type == MESSAGE_TYPES['REPOSITORY_EVENT']:
                    self._handle_repository_event(message)
                elif message_type == MESSAGE_TYPES['HEARTBEAT']:
                    self._handle_heartbeat(message)
                else:
                    logger.warning(f"No handler for message type: {message_type}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def _handle_state_update(self, message: Dict[str, Any]):
        """Handle state update message"""
        logger.info(f"State update from {message.get('anchor')}: {message.get('data')}")
    
    def _handle_frequency_sync(self, message: Dict[str, Any]):
        """Handle frequency synchronization message"""
        frequency = message.get('frequency')
        s_roi = message.get('s_roi')
        anchor = message.get('anchor')
        logger.info(f"Frequency sync from {anchor}: {frequency} Hz, S-ROI: {s_roi}")
    
    def _handle_repository_event(self, message: Dict[str, Any]):
        """Handle repository event message"""
        event_type = message.get('event_type')
        source = message.get('source')
        logger.info(f"Repository event from {source}: {event_type}")
    
    def _handle_heartbeat(self, message: Dict[str, Any]):
        """Handle heartbeat message"""
        anchor = message.get('anchor')
        logger.debug(f"Heartbeat from {anchor}")
    
    def close(self):
        """Close the Kafka consumer connection"""
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed")
