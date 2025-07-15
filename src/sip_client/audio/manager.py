"""
Audio Manager - Handles audio streaming for SIP calls
"""

import logging
from typing import Optional, Dict, Any
from .devices import AudioDevice, get_default_input_device, get_default_output_device

logger = logging.getLogger(__name__)


class AudioManager:
    """Manages audio streaming for SIP calls"""
    
    def __init__(self):
        """Initialize audio manager"""
        self.input_device: Optional[AudioDevice] = None
        self.output_device: Optional[AudioDevice] = None
        self.is_streaming = False
        self.stream_config: Dict[str, Any] = {}
        
        # Get default devices
        self.input_device = get_default_input_device()
        self.output_device = get_default_output_device()
        
        logger.info("Audio manager initialized")
    
    def start_streaming(self, call_id: str, rtp_port: int, 
                       remote_address: str, remote_port: int) -> bool:
        """Start audio streaming for a call"""
        try:
            logger.info(f"Starting audio streaming for call {call_id}")
            logger.info(f"RTP: Local port {rtp_port}, Remote {remote_address}:{remote_port}")
            
            # In a real implementation, this would:
            # 1. Initialize audio input/output streams
            # 2. Set up RTP sender/receiver
            # 3. Connect audio pipeline
            
            self.is_streaming = True
            self.stream_config = {
                'call_id': call_id,
                'rtp_port': rtp_port,
                'remote_address': remote_address,
                'remote_port': remote_port
            }
            
            logger.info("Audio streaming started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start audio streaming: {e}")
            return False
    
    def stop_streaming(self, call_id: str) -> bool:
        """Stop audio streaming for a call"""
        try:
            if not self.is_streaming:
                return True
            
            logger.info(f"Stopping audio streaming for call {call_id}")
            
            # In a real implementation, this would:
            # 1. Stop RTP sender/receiver
            # 2. Close audio streams
            # 3. Clean up resources
            
            self.is_streaming = False
            self.stream_config.clear()
            
            logger.info("Audio streaming stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop audio streaming: {e}")
            return False
    
    def set_input_device(self, device: AudioDevice) -> bool:
        """Set the input audio device"""
        try:
            self.input_device = device
            logger.info(f"Input device set to: {device}")
            return True
        except Exception as e:
            logger.error(f"Failed to set input device: {e}")
            return False
    
    def set_output_device(self, device: AudioDevice) -> bool:
        """Set the output audio device"""
        try:
            self.output_device = device
            logger.info(f"Output device set to: {device}")
            return True
        except Exception as e:
            logger.error(f"Failed to set output device: {e}")
            return False
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.is_streaming:
            self.stop_streaming("cleanup")
        
        logger.info("Audio manager cleaned up") 