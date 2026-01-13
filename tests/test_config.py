"""
Unit tests for Configuration
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streaming.config import (
    KAFKA_CONFIG,
    KAFKA_TOPICS,
    WEBSOCKET_CONFIG,
    RESONANCE_CONFIG,
    NODE_ENDPOINTS,
    MESSAGE_TYPES
)


class TestConfiguration(unittest.TestCase):
    """Test cases for configuration"""
    
    def test_kafka_config(self):
        """Test Kafka configuration"""
        self.assertIn('bootstrap_servers', KAFKA_CONFIG)
        self.assertIn('client_id', KAFKA_CONFIG)
        self.assertEqual(KAFKA_CONFIG['client_id'], 'resonance-node')
    
    def test_kafka_topics(self):
        """Test Kafka topics configuration"""
        self.assertIn('outbound', KAFKA_TOPICS)
        self.assertIn('inbound', KAFKA_TOPICS)
        self.assertIn('state_sync', KAFKA_TOPICS)
        self.assertIn('lexamoris', KAFKA_TOPICS)
        self.assertIn('nexus', KAFKA_TOPICS)
    
    def test_websocket_config(self):
        """Test WebSocket configuration"""
        self.assertIn('host', WEBSOCKET_CONFIG)
        self.assertIn('port', WEBSOCKET_CONFIG)
        self.assertEqual(WEBSOCKET_CONFIG['port'], 8765)
    
    def test_resonance_config(self):
        """Test Resonance system configuration"""
        self.assertIn('frequency', RESONANCE_CONFIG)
        self.assertIn('s_roi_threshold', RESONANCE_CONFIG)
        self.assertIn('anchor', RESONANCE_CONFIG)
        
        # Verify resonance frequency
        self.assertEqual(RESONANCE_CONFIG['frequency'], 0.043)
        self.assertEqual(RESONANCE_CONFIG['anchor'], 'BOLZANO_71')
    
    def test_node_endpoints(self):
        """Test node endpoints configuration"""
        self.assertIn('lexamoris', NODE_ENDPOINTS)
        self.assertIn('nexus', NODE_ENDPOINTS)
        
        # Verify LexAmoris endpoint structure
        self.assertIn('websocket', NODE_ENDPOINTS['lexamoris'])
        self.assertIn('kafka_topic', NODE_ENDPOINTS['lexamoris'])
        
        # Verify Nexus endpoint structure
        self.assertIn('websocket', NODE_ENDPOINTS['nexus'])
        self.assertIn('kafka_topic', NODE_ENDPOINTS['nexus'])
    
    def test_message_types(self):
        """Test message types configuration"""
        required_types = [
            'STATE_UPDATE',
            'FREQUENCY_SYNC',
            'S_ROI_UPDATE',
            'REPOSITORY_EVENT',
            'HEARTBEAT'
        ]
        
        for msg_type in required_types:
            self.assertIn(msg_type, MESSAGE_TYPES)


if __name__ == '__main__':
    unittest.main()
