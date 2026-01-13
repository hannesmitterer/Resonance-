#!/usr/bin/env python3
"""
Resonance Streaming Pipeline CLI
Command-line interface for managing the streaming pipeline
"""

import argparse
import asyncio
import logging
import sys
from typing import Optional

from streaming.pipeline import ResonancePipeline
from streaming.kafka_producer import ResonanceProducer
from streaming.config import RESONANCE_CONFIG, KAFKA_TOPICS


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


async def start_pipeline(args):
    """Start the complete streaming pipeline"""
    print("Starting Resonance Streaming Pipeline...")
    print(f"Anchor: {RESONANCE_CONFIG['anchor']}")
    print(f"Frequency: {RESONANCE_CONFIG['frequency']} Hz")
    print(f"S-ROI Threshold: {RESONANCE_CONFIG['s_roi_threshold']}")
    print("\nPress Ctrl+C to stop\n")
    
    pipeline = ResonancePipeline()
    try:
        await pipeline.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        await pipeline.stop()


def send_message(args):
    """Send a test message via Kafka"""
    producer = ResonanceProducer()
    
    message_data = {
        'test': True,
        'content': args.message,
    }
    
    if args.type == 'state':
        success = producer.send_state_update(message_data)
        print(f"State update {'sent' if success else 'failed'}")
    elif args.type == 'frequency':
        success = producer.send_frequency_sync(
            RESONANCE_CONFIG['frequency'],
            RESONANCE_CONFIG['s_roi_threshold']
        )
        print(f"Frequency sync {'sent' if success else 'failed'}")
    elif args.type == 'event':
        success = producer.send_repository_event('test', message_data, args.target)
        print(f"Repository event {'sent' if success else 'failed'}")
    
    producer.close()


def show_config(args):
    """Display current configuration"""
    print("\n=== Resonance Streaming Configuration ===\n")
    
    print("Resonance Parameters:")
    for key, value in RESONANCE_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\nKafka Topics:")
    for key, value in KAFKA_TOPICS.items():
        print(f"  {key}: {value}")
    
    print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Resonance Streaming Pipeline CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start the complete pipeline
  %(prog)s start
  
  # Send a test state update
  %(prog)s send --type state --message "Test update"
  
  # Send a repository event to LexAmoris
  %(prog)s send --type event --target lexamoris --message "New commit"
  
  # Show configuration
  %(prog)s config
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start the streaming pipeline')
    
    # Send command
    send_parser = subparsers.add_parser('send', help='Send a test message')
    send_parser.add_argument(
        '--type',
        choices=['state', 'frequency', 'event'],
        required=True,
        help='Type of message to send'
    )
    send_parser.add_argument(
        '--message',
        default='Test message',
        help='Message content'
    )
    send_parser.add_argument(
        '--target',
        choices=['lexamoris', 'nexus'],
        help='Target node (for event messages)'
    )
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Show configuration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    setup_logging(args.verbose)
    
    # Execute command
    if args.command == 'start':
        asyncio.run(start_pipeline(args))
    elif args.command == 'send':
        send_message(args)
    elif args.command == 'config':
        show_config(args)


if __name__ == '__main__':
    main()
