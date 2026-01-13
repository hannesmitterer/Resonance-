"""
WebSocket Server for Resonance Streaming Pipeline
Provides real-time bidirectional communication with other nodes
"""

import asyncio
import json
import logging
from typing import Dict, Any, Set, Optional
from datetime import datetime

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    logging.warning("websockets library not installed. WebSocket functionality will be simulated.")

from .config import WEBSOCKET_CONFIG, MESSAGE_TYPES, RESONANCE_CONFIG

logger = logging.getLogger(__name__)


class ResonanceWebSocketServer:
    """
    WebSocket server for real-time communication with other nodes
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize WebSocket server
        
        Args:
            config: Optional custom WebSocket configuration
        """
        self.config = config or WEBSOCKET_CONFIG
        self.clients: Set[WebSocketServerProtocol] = set()
        self.server = None
        self.is_running = False
    
    async def register_client(self, websocket: WebSocketServerProtocol):
        """
        Register a new client connection
        
        Args:
            websocket: WebSocket connection
        """
        self.clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
        
        # Send welcome message with current state
        await self.send_to_client(websocket, {
            'type': MESSAGE_TYPES['STATE_UPDATE'],
            'timestamp': datetime.utcnow().isoformat(),
            'frequency': RESONANCE_CONFIG['frequency'],
            's_roi': RESONANCE_CONFIG['s_roi_threshold'],
            'anchor': RESONANCE_CONFIG['anchor'],
            'message': 'Connected to Resonance node',
        })
    
    async def unregister_client(self, websocket: WebSocketServerProtocol):
        """
        Unregister a client connection
        
        Args:
            websocket: WebSocket connection
        """
        self.clients.discard(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def send_to_client(self, websocket: WebSocketServerProtocol, message: Dict[str, Any]):
        """
        Send message to a specific client
        
        Args:
            websocket: WebSocket connection
            message: Message to send
        """
        try:
            await websocket.send(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending message to client: {e}")
    
    async def broadcast(self, message: Dict[str, Any], exclude: Optional[WebSocketServerProtocol] = None):
        """
        Broadcast message to all connected clients
        
        Args:
            message: Message to broadcast
            exclude: Optional client to exclude from broadcast
        """
        if not self.clients:
            logger.debug("No clients connected for broadcast")
            return
        
        disconnected = set()
        for client in self.clients:
            if client == exclude:
                continue
            try:
                await client.send(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(client)
        
        # Clean up disconnected clients
        for client in disconnected:
            await self.unregister_client(client)
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """
        Handle incoming client connections and messages
        
        Args:
            websocket: WebSocket connection
            path: Connection path
        """
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                await self.process_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client connection closed")
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def process_message(self, websocket: WebSocketServerProtocol, raw_message: str):
        """
        Process incoming message from client
        
        Args:
            websocket: WebSocket connection
            raw_message: Raw message string
        """
        try:
            message = json.loads(raw_message)
            message_type = message.get('type')
            
            logger.debug(f"Received message type: {message_type}")
            
            if message_type == MESSAGE_TYPES['FREQUENCY_SYNC']:
                await self.handle_frequency_sync(websocket, message)
            elif message_type == MESSAGE_TYPES['STATE_UPDATE']:
                await self.handle_state_update(websocket, message)
            elif message_type == MESSAGE_TYPES['REPOSITORY_EVENT']:
                await self.handle_repository_event(websocket, message)
            elif message_type == MESSAGE_TYPES['HEARTBEAT']:
                await self.handle_heartbeat(websocket, message)
            else:
                logger.warning(f"Unknown message type: {message_type}")
                await self.send_to_client(websocket, {
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}',
                })
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON message: {e}")
            await self.send_to_client(websocket, {
                'type': 'error',
                'message': 'Invalid JSON format',
            })
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    async def handle_frequency_sync(self, websocket: WebSocketServerProtocol, message: Dict[str, Any]):
        """Handle frequency synchronization request"""
        # Broadcast frequency sync to all other clients
        await self.broadcast(message, exclude=websocket)
        
        # Send acknowledgment
        await self.send_to_client(websocket, {
            'type': 'ack',
            'original_type': MESSAGE_TYPES['FREQUENCY_SYNC'],
            'timestamp': datetime.utcnow().isoformat(),
        })
    
    async def handle_state_update(self, websocket: WebSocketServerProtocol, message: Dict[str, Any]):
        """Handle state update"""
        # Broadcast state update to all other clients
        await self.broadcast(message, exclude=websocket)
        
        # Send acknowledgment
        await self.send_to_client(websocket, {
            'type': 'ack',
            'original_type': MESSAGE_TYPES['STATE_UPDATE'],
            'timestamp': datetime.utcnow().isoformat(),
        })
    
    async def handle_repository_event(self, websocket: WebSocketServerProtocol, message: Dict[str, Any]):
        """Handle repository event"""
        logger.info(f"Repository event: {message.get('event_type')} from {message.get('source')}")
        
        # Broadcast to all clients
        await self.broadcast(message, exclude=websocket)
        
        # Send acknowledgment
        await self.send_to_client(websocket, {
            'type': 'ack',
            'original_type': MESSAGE_TYPES['REPOSITORY_EVENT'],
            'timestamp': datetime.utcnow().isoformat(),
        })
    
    async def handle_heartbeat(self, websocket: WebSocketServerProtocol, message: Dict[str, Any]):
        """Handle heartbeat"""
        # Respond with heartbeat
        await self.send_to_client(websocket, {
            'type': MESSAGE_TYPES['HEARTBEAT'],
            'timestamp': datetime.utcnow().isoformat(),
            'anchor': RESONANCE_CONFIG['anchor'],
        })
    
    async def start(self):
        """Start the WebSocket server"""
        if not WEBSOCKETS_AVAILABLE:
            logger.warning("[SIMULATED] WebSocket server would start on {host}:{port}".format(**self.config))
            self.is_running = True
            return
        
        try:
            self.server = await websockets.serve(
                self.handle_client,
                self.config['host'],
                self.config['port'],
                ping_interval=self.config['ping_interval'],
                ping_timeout=self.config['ping_timeout'],
            )
            self.is_running = True
            logger.info(f"WebSocket server started on {self.config['host']}:{self.config['port']}")
            
            # Keep server running
            await asyncio.Future()  # run forever
        except Exception as e:
            logger.error(f"Error starting WebSocket server: {e}")
            self.is_running = False
    
    async def stop(self):
        """Stop the WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.is_running = False
            logger.info("WebSocket server stopped")
