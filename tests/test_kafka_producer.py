"""
Unit tests for Kafka Producer
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streaming.kafka_producer import ResonanceProducer
from streaming.config import MESSAGE_TYPES, RESONANCE_CONFIG


class TestResonanceProducer(unittest.TestCase):
    """Test cases for ResonanceProducer"""
    
    def setUp(self):
        """Set up test producer"""
        self.producer = ResonanceProducer()
    
    def test_initialization(self):
        """Test producer initialization"""
        self.assertIsNotNone(self.producer)
        self.assertIsNotNone(self.producer.config)
    
    def test_send_state_update(self):
        """Test sending state update"""
        state_data = {
            'frequency': 0.043,
            's_roi': 0.5020,
            'status': 'active'
        }
        result = self.producer.send_state_update(state_data)
        # In simulation mode, this should return True
        self.assertTrue(result)
    
    def test_send_frequency_sync(self):
        """Test sending frequency synchronization"""
        frequency = RESONANCE_CONFIG['frequency']
        s_roi = RESONANCE_CONFIG['s_roi_threshold']
        result = self.producer.send_frequency_sync(frequency, s_roi)
        self.assertTrue(result)
    
    def test_send_repository_event(self):
        """Test sending repository event"""
        event_data = {
            'sha': 'abc123',
            'message': 'Test commit',
            'author': 'test_user'
        }
        result = self.producer.send_repository_event('commit', event_data)
        self.assertTrue(result)
    
    def test_send_repository_event_to_specific_node(self):
        """Test sending repository event to specific node"""
        event_data = {'test': 'data'}
        result = self.producer.send_repository_event('update', event_data, 'lexamoris')
        self.assertTrue(result)
    
    def test_send_heartbeat(self):
        """Test sending heartbeat"""
        result = self.producer.send_heartbeat()
        self.assertTrue(result)
    
    def tearDown(self):
        """Clean up after tests"""
        self.producer.close()


if __name__ == '__main__':
    unittest.main()
