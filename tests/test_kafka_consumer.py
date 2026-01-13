"""
Unit tests for Kafka Consumer
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streaming.kafka_consumer import ResonanceConsumer
from streaming.config import MESSAGE_TYPES, KAFKA_TOPICS


class TestResonanceConsumer(unittest.TestCase):
    """Test cases for ResonanceConsumer"""
    
    def setUp(self):
        """Set up test consumer"""
        self.consumer = ResonanceConsumer()
    
    def test_initialization(self):
        """Test consumer initialization"""
        self.assertIsNotNone(self.consumer)
        self.assertIsNotNone(self.consumer.config)
        self.assertIsNotNone(self.consumer.topics)
    
    def test_register_handler(self):
        """Test registering message handler"""
        def test_handler(message):
            pass
        
        self.consumer.register_handler('test_type', test_handler)
        self.assertIn('test_type', self.consumer.message_handlers)
        self.assertEqual(self.consumer.message_handlers['test_type'], test_handler)
    
    def test_handle_state_update(self):
        """Test handling state update message"""
        message = {
            'type': MESSAGE_TYPES['STATE_UPDATE'],
            'anchor': 'BOLZANO_71',
            'data': {'frequency': 0.043}
        }
        # Should not raise an exception
        self.consumer._handle_state_update(message)
    
    def test_handle_frequency_sync(self):
        """Test handling frequency sync message"""
        message = {
            'type': MESSAGE_TYPES['FREQUENCY_SYNC'],
            'frequency': 0.043,
            's_roi': 0.5020,
            'anchor': 'BOLZANO_71'
        }
        # Should not raise an exception
        self.consumer._handle_frequency_sync(message)
    
    def test_handle_repository_event(self):
        """Test handling repository event message"""
        message = {
            'type': MESSAGE_TYPES['REPOSITORY_EVENT'],
            'event_type': 'commit',
            'source': 'resonance'
        }
        # Should not raise an exception
        self.consumer._handle_repository_event(message)
    
    def test_handle_heartbeat(self):
        """Test handling heartbeat message"""
        message = {
            'type': MESSAGE_TYPES['HEARTBEAT'],
            'anchor': 'BOLZANO_71'
        }
        # Should not raise an exception
        self.consumer._handle_heartbeat(message)
    
    def tearDown(self):
        """Clean up after tests"""
        self.consumer.close()


if __name__ == '__main__':
    unittest.main()
