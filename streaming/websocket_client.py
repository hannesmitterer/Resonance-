"""
WebSocket Client for Resonance Streaming Pipeline
Connects to other nodes (LexAmoris, Nexus) via WebSocket
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timezone

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    WebSocketClientProtocol = Any  # Type placeholder when websockets not available
    logging.warning("websockets library not installed. WebSocket functionality will be simulated.")

from .config import MESSAGE_TYPES, NODE_ENDPOINTS, RESONANCE_CONFIG

logger = logging.getLogger(__name__)


class ResonanceWebSocketClient:
    """
    WebSocket client for connecting to other nodes
    """
    
    def __init__(self, node_name: str):
        """
        Initialize WebSocket client
        
        Args:
            node_name: Name of the node to connect to (lexamoris, nexus)
        """
        self.node_name = node_name
        self.endpoint = NODE_ENDPOINTS.get(node_name)
        
        if not self.endpoint:
            raise ValueError(f"Unknown node: {node_name}")
        
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.is_connected = False
        self.message_handlers = {}
        self.reconnect_delay = 5  # seconds
    
    def register_handler(self, message_type: str, handler: Callable[[Dict[str, Any]], None]):
        """
        Register a handler function for a specific message type
        
        Args:
            message_type: Type of message to handle
            handler: Callback function to process the message
        """
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for {self.node_name}: {message_type}")
    
    async def connect(self):
        """Establish WebSocket connection to the node"""
        if not WEBSOCKETS_AVAILABLE:
            logger.warning(f"[SIMULATED] Would connect to {self.node_name} at {self.endpoint['websocket']}")
            self.is_connected = True
            return
        
        try:
            uri = self.endpoint['websocket']
            self.websocket = await websockets.connect(uri)
            self.is_connected = True
            logger.info(f"Connected to {self.node_name} at {uri}")
        except Exception as e:
            logger.error(f"Failed to connect to {self.node_name}: {e}")
            self.is_connected = False
    
    async def disconnect(self):
        """Close WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
            logger.info(f"Disconnected from {self.node_name}")
    
    async def send_message(self, message: Dict[str, Any]):
        """
        Send message to the connected node
        
        Args:
            message: Message to send
        """
        if not WEBSOCKETS_AVAILABLE or not self.is_connected:
            logger.info(f"[SIMULATED] Would send to {self.node_name}: {message}")
            return
        
        try:
            await self.websocket.send(json.dumps(message))
            logger.debug(f"Sent message to {self.node_name}: {message.get('type')}")
        except Exception as e:
            logger.error(f"Error sending message to {self.node_name}: {e}")
            self.is_connected = False
    
    async def send_frequency_sync(self, frequency: float, s_roi: float):
        """
        Send frequency synchronization message
        
        Args:
            frequency: Current resonance frequency
            s_roi: Social Return on Integrity value
        """
        message = {
            'type': MESSAGE_TYPES['FREQUENCY_SYNC'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'frequency': frequency,
            's_roi': s_roi,
            'anchor': RESONANCE_CONFIG['anchor'],
            'source': 'resonance',
        }
        await self.send_message(message)
    
    async def send_state_update(self, state_data: Dict[str, Any]):
        """
        Send state update message
        
        Args:
            state_data: State information to send
        """
        message = {
            'type': MESSAGE_TYPES['STATE_UPDATE'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'anchor': RESONANCE_CONFIG['anchor'],
            'data': state_data,
            'source': 'resonance',
        }
        await self.send_message(message)
    
    async def send_repository_event(self, event_type: str, event_data: Dict[str, Any]):
        """
        Send repository event notification
        
        Args:
            event_type: Type of repository event
            event_data: Event details
        """
        message = {
            'type': MESSAGE_TYPES['REPOSITORY_EVENT'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': event_type,
            'data': event_data,
            'source': 'resonance',
        }
        await self.send_message(message)
    
    async def send_heartbeat(self):
        """Send heartbeat message"""
        message = {
            'type': MESSAGE_TYPES['HEARTBEAT'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'anchor': RESONANCE_CONFIG['anchor'],
            'source': 'resonance',
        }
        await self.send_message(message)
    
    async def listen(self):
        """Listen for incoming messages from the node"""
        if not WEBSOCKETS_AVAILABLE or not self.is_connected:
            logger.info(f"[SIMULATED] Would be listening to {self.node_name}")
            return
        
        try:
            async for message in self.websocket:
                await self.process_message(message)
        except Exception as e:
            # Handle any connection errors (including websockets.exceptions.ConnectionClosed)
            if "ConnectionClosed" in str(type(e).__name__):
                logger.info(f"Connection to {self.node_name} closed")
            else:
                logger.error(f"Error listening to {self.node_name}: {e}")
            self.is_connected = False
    
    async def process_message(self, raw_message: str):
        """
        Process incoming message
        
        Args:
            raw_message: Raw message string
        """
        try:
            message = json.loads(raw_message)
            message_type = message.get('type')
            
            logger.debug(f"Received from {self.node_name}: {message_type}")
            
            # Call registered handler if available
            handler = self.message_handlers.get(message_type)
            if handler:
                handler(message)
            else:
                logger.debug(f"No handler for message type: {message_type}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON from {self.node_name}: {e}")
        except Exception as e:
            logger.error(f"Error processing message from {self.node_name}: {e}")
    
    async def run_with_reconnect(self):
        """Run client with automatic reconnection"""
        while True:
            try:
                await self.connect()
                if self.is_connected:
                    await self.listen()
                else:
                    logger.warning(f"Failed to connect to {self.node_name}, retrying in {self.reconnect_delay}s")
            except Exception as e:
                logger.error(f"Error in client loop for {self.node_name}: {e}")
            
            # Wait before reconnecting
            await asyncio.sleep(self.reconnect_delay)
            logger.info(f"Attempting to reconnect to {self.node_name}...")
