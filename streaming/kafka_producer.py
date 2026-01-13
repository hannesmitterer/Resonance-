"""
Apache Kafka Producer for Resonance Streaming Pipeline
Sends data streams to other nodes (LexAmoris, Nexus)
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from kafka import KafkaProducer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logging.warning("kafka-python not installed. Kafka functionality will be simulated.")

from .config import KAFKA_CONFIG, KAFKA_TOPICS, MESSAGE_TYPES, RESONANCE_CONFIG

logger = logging.getLogger(__name__)


class ResonanceProducer:
    """
    Kafka producer for streaming data from Resonance to other nodes
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Kafka producer
        
        Args:
            config: Optional custom Kafka configuration
        """
        self.config = config or KAFKA_CONFIG
        self.producer = None
        self.is_connected = False
        
        if KAFKA_AVAILABLE:
            self._initialize_producer()
        else:
            logger.warning("Running in simulation mode - no actual Kafka connection")
    
    def _initialize_producer(self):
        """Initialize the Kafka producer connection"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.config['bootstrap_servers'],
                client_id=self.config['client_id'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
            )
            self.is_connected = True
            logger.info(f"Kafka producer connected to {self.config['bootstrap_servers']}")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            self.is_connected = False
    
    def send_state_update(self, state_data: Dict[str, Any]) -> bool:
        """
        Send state update to other nodes
        
        Args:
            state_data: State information to broadcast
            
        Returns:
            True if message sent successfully, False otherwise
        """
        message = {
            'type': MESSAGE_TYPES['STATE_UPDATE'],
            'timestamp': datetime.utcnow().isoformat(),
            'anchor': RESONANCE_CONFIG['anchor'],
            'data': state_data,
        }
        return self._send_message(KAFKA_TOPICS['state_sync'], message)
    
    def send_frequency_sync(self, frequency: float, s_roi: float) -> bool:
        """
        Send frequency synchronization message
        
        Args:
            frequency: Current resonance frequency (Hz)
            s_roi: Social Return on Integrity value
            
        Returns:
            True if message sent successfully, False otherwise
        """
        message = {
            'type': MESSAGE_TYPES['FREQUENCY_SYNC'],
            'timestamp': datetime.utcnow().isoformat(),
            'frequency': frequency,
            's_roi': s_roi,
            'anchor': RESONANCE_CONFIG['anchor'],
        }
        return self._send_message(KAFKA_TOPICS['state_sync'], message)
    
    def send_repository_event(self, event_type: str, event_data: Dict[str, Any], target_node: Optional[str] = None) -> bool:
        """
        Send repository event notification
        
        Args:
            event_type: Type of repository event (commit, push, etc.)
            event_data: Event details
            target_node: Specific node to send to (lexamoris, nexus) or None for broadcast
            
        Returns:
            True if message sent successfully, False otherwise
        """
        message = {
            'type': MESSAGE_TYPES['REPOSITORY_EVENT'],
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'data': event_data,
            'source': 'resonance',
        }
        
        if target_node:
            topic = KAFKA_TOPICS.get(target_node)
            if not topic:
                logger.error(f"Unknown target node: {target_node}")
                return False
            return self._send_message(topic, message)
        else:
            # Broadcast to all nodes
            return self._send_message(KAFKA_TOPICS['outbound'], message)
    
    def send_heartbeat(self) -> bool:
        """
        Send heartbeat message to maintain connection
        
        Returns:
            True if message sent successfully, False otherwise
        """
        message = {
            'type': MESSAGE_TYPES['HEARTBEAT'],
            'timestamp': datetime.utcnow().isoformat(),
            'anchor': RESONANCE_CONFIG['anchor'],
            'frequency': RESONANCE_CONFIG['frequency'],
            's_roi': RESONANCE_CONFIG['s_roi_threshold'],
        }
        return self._send_message(KAFKA_TOPICS['state_sync'], message)
    
    def _send_message(self, topic: str, message: Dict[str, Any], key: Optional[str] = None) -> bool:
        """
        Internal method to send message to Kafka topic
        
        Args:
            topic: Kafka topic name
            message: Message to send
            key: Optional message key for partitioning
            
        Returns:
            True if message sent successfully, False otherwise
        """
        if not KAFKA_AVAILABLE or not self.is_connected:
            logger.info(f"[SIMULATED] Would send to {topic}: {message}")
            return True
        
        try:
            future = self.producer.send(topic, value=message, key=key)
            # Wait for message to be sent (with timeout)
            record_metadata = future.get(timeout=10)
            logger.debug(f"Message sent to {topic}: partition {record_metadata.partition}, offset {record_metadata.offset}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send message to {topic}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending message: {e}")
            return False
    
    def close(self):
        """Close the Kafka producer connection"""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")
