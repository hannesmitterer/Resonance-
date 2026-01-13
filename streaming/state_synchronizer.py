"""
State Synchronization Manager for Resonance Streaming Pipeline
Manages state synchronization across all connected nodes
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .kafka_producer import ResonanceProducer
from .websocket_client import ResonanceWebSocketClient
from .config import RESONANCE_CONFIG, NODE_ENDPOINTS

logger = logging.getLogger(__name__)


class StateSynchronizer:
    """
    Manages state synchronization across Resonance, LexAmoris, and Nexus nodes
    """
    
    def __init__(self):
        """Initialize state synchronizer"""
        self.state = {
            'frequency': RESONANCE_CONFIG['frequency'],
            's_roi': RESONANCE_CONFIG['s_roi_threshold'],
            'anchor': RESONANCE_CONFIG['anchor'],
            'last_update': datetime.utcnow().isoformat(),
            'connected_nodes': [],
        }
        
        self.kafka_producer = ResonanceProducer()
        self.websocket_clients: Dict[str, ResonanceWebSocketClient] = {}
        self.is_running = False
    
    def initialize_clients(self):
        """Initialize WebSocket clients for all nodes"""
        for node_name in NODE_ENDPOINTS.keys():
            try:
                client = ResonanceWebSocketClient(node_name)
                self.websocket_clients[node_name] = client
                logger.info(f"Initialized client for {node_name}")
            except Exception as e:
                logger.error(f"Failed to initialize client for {node_name}: {e}")
    
    def update_state(self, updates: Dict[str, Any]):
        """
        Update local state
        
        Args:
            updates: Dictionary of state updates
        """
        self.state.update(updates)
        self.state['last_update'] = datetime.utcnow().isoformat()
        logger.info(f"State updated: {updates}")
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current state
        
        Returns:
            Current state dictionary
        """
        return self.state.copy()
    
    async def broadcast_state(self):
        """Broadcast current state to all nodes"""
        state_data = self.get_state()
        
        # Send via Kafka
        self.kafka_producer.send_state_update(state_data)
        
        # Send via WebSocket to all connected clients
        for node_name, client in self.websocket_clients.items():
            if client.is_connected:
                try:
                    await client.send_state_update(state_data)
                except Exception as e:
                    logger.error(f"Error broadcasting state to {node_name}: {e}")
    
    async def broadcast_frequency_sync(self):
        """Broadcast frequency synchronization to all nodes"""
        frequency = self.state['frequency']
        s_roi = self.state['s_roi']
        
        # Send via Kafka
        self.kafka_producer.send_frequency_sync(frequency, s_roi)
        
        # Send via WebSocket to all connected clients
        for node_name, client in self.websocket_clients.items():
            if client.is_connected:
                try:
                    await client.send_frequency_sync(frequency, s_roi)
                except Exception as e:
                    logger.error(f"Error broadcasting frequency sync to {node_name}: {e}")
    
    async def notify_repository_event(self, event_type: str, event_data: Dict[str, Any], target_nodes: Optional[List[str]] = None):
        """
        Notify nodes about a repository event
        
        Args:
            event_type: Type of repository event
            event_data: Event details
            target_nodes: Specific nodes to notify (None for all)
        """
        nodes_to_notify = target_nodes or list(self.websocket_clients.keys())
        
        # Send via Kafka
        for node_name in nodes_to_notify:
            self.kafka_producer.send_repository_event(event_type, event_data, node_name)
        
        # Send via WebSocket
        for node_name in nodes_to_notify:
            client = self.websocket_clients.get(node_name)
            if client and client.is_connected:
                try:
                    await client.send_repository_event(event_type, event_data)
                except Exception as e:
                    logger.error(f"Error notifying {node_name} of repository event: {e}")
    
    async def send_heartbeat(self):
        """Send heartbeat to all nodes"""
        # Send via Kafka
        self.kafka_producer.send_heartbeat()
        
        # Send via WebSocket
        for node_name, client in self.websocket_clients.items():
            if client.is_connected:
                try:
                    await client.send_heartbeat()
                except Exception as e:
                    logger.error(f"Error sending heartbeat to {node_name}: {e}")
    
    async def periodic_sync(self):
        """Periodically synchronize state with all nodes"""
        sync_interval = RESONANCE_CONFIG['sync_interval']
        
        while self.is_running:
            try:
                # Broadcast state update
                await self.broadcast_state()
                
                # Broadcast frequency sync
                await self.broadcast_frequency_sync()
                
                # Send heartbeat
                await self.send_heartbeat()
                
                # Update connected nodes list
                connected = [name for name, client in self.websocket_clients.items() if client.is_connected]
                self.update_state({'connected_nodes': connected})
                
                logger.debug(f"Periodic sync completed. Connected nodes: {connected}")
            except Exception as e:
                logger.error(f"Error in periodic sync: {e}")
            
            # Wait for next sync interval
            await asyncio.sleep(sync_interval)
    
    async def start(self):
        """Start the state synchronizer"""
        self.is_running = True
        self.initialize_clients()
        
        # Connect all clients
        connect_tasks = []
        for node_name, client in self.websocket_clients.items():
            connect_tasks.append(client.connect())
        
        # Connect in parallel
        await asyncio.gather(*connect_tasks, return_exceptions=True)
        
        # Start periodic sync
        logger.info("State synchronizer started")
        await self.periodic_sync()
    
    async def stop(self):
        """Stop the state synchronizer"""
        self.is_running = False
        
        # Disconnect all clients
        disconnect_tasks = []
        for client in self.websocket_clients.values():
            disconnect_tasks.append(client.disconnect())
        
        await asyncio.gather(*disconnect_tasks, return_exceptions=True)
        
        # Close Kafka producer
        self.kafka_producer.close()
        
        logger.info("State synchronizer stopped")
