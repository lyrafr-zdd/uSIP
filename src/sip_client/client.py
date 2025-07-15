"""
Simplified SIP Client using existing simple_sip_client.py functionality
"""

import os
import sys
import importlib.util
import logging
from typing import Optional

# Import the original SimpleSIPClient
# This is a bridge to use the working simple_sip_client.py
spec = importlib.util.spec_from_file_location("simple_sip_client", 
                                              os.path.join(os.path.dirname(__file__), "../../simple_sip_client.py"))
if spec and spec.loader:
    simple_sip_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(simple_sip_module)
    SimpleSIPClient = simple_sip_module.SimpleSIPClient
else:
    raise ImportError("Could not load simple_sip_client.py")

from .models.account import SIPAccount
from .models.call import CallInfo
from .models.enums import CallState, RegistrationState
from .audio.manager import AudioManager
from .audio.devices import AudioDevice

logger = logging.getLogger(__name__)


class SIPClient:
    """Main SIP client - bridges to the working simple_sip_client.py"""
    
    def __init__(self, account: Optional[SIPAccount] = None):
        """Initialize SIP client"""
        if account is None:
            account = SIPAccount(
                username=os.getenv('SIP_USERNAME', ''),
                password=os.getenv('SIP_PASSWORD', ''),
                domain=os.getenv('SIP_DOMAIN', ''),
                port=int(os.getenv('SIP_PORT', 5060))
            )
        
        self.account = account
        self._simple_client = SimpleSIPClient()
        self.audio_manager = AudioManager()
        
        # State
        self.registration_state = RegistrationState.UNREGISTERED
        self.calls = {}
        
        logger.info("SIP client initialized")
    
    def start(self) -> bool:
        """Start the SIP client"""
        logger.info("SIP client started")
        return True
    
    def stop(self):
        """Stop the SIP client"""
        self._simple_client.cleanup()
        self.audio_manager.cleanup()
        logger.info("SIP client stopped")
    
    def register(self) -> bool:
        """Register with SIP server"""
        try:
            success = self._simple_client.send_register()
            if success:
                self.registration_state = RegistrationState.REGISTERED
                logger.info("Registration successful")
            else:
                self.registration_state = RegistrationState.FAILED
                logger.error("Registration failed")
            return success
        except Exception as e:
            logger.error(f"Registration error: {e}")
            self.registration_state = RegistrationState.FAILED
            return False
    
    def unregister(self) -> bool:
        """Unregister from SIP server"""
        try:
            # Simple client doesn't have explicit unregister, just cleanup
            self.registration_state = RegistrationState.UNREGISTERED
            logger.info("Unregistered")
            return True
        except Exception as e:
            logger.error(f"Unregistration error: {e}")
            return False
    
    def make_call(self, target_uri: str, input_device: Optional[int] = None, 
                  output_device: Optional[int] = None) -> Optional[str]:
        """Make an outgoing call"""
        try:
            # Extract number from URI if needed
            if target_uri.startswith('sip:'):
                # Extract the user part from sip:user@domain
                number = target_uri.split(':')[1].split('@')[0]
            else:
                number = target_uri
            
            success = self._simple_client.make_call(number)
            if success:
                call_id = f"call_{number}"
                self.calls[call_id] = {
                    'target': target_uri,
                    'state': CallState.CONNECTED,
                    'call_id': call_id
                }
                logger.info(f"Call to {target_uri} initiated")
                return call_id
            else:
                logger.error(f"Call to {target_uri} failed")
                return None
        except Exception as e:
            logger.error(f"Make call error: {e}")
            return None
    
    def hangup(self, call_id: Optional[str] = None) -> bool:
        """Hang up a call"""
        try:
            self._simple_client.hangup()
            if call_id and call_id in self.calls:
                del self.calls[call_id]
            logger.info("Call ended")
            return True
        except Exception as e:
            logger.error(f"Hangup error: {e}")
            return False
    
    def get_calls(self):
        """Get list of active calls"""
        return list(self.calls.values())
    
    def get_audio_devices(self):
        """Get list of available audio devices"""
        return self.audio_manager.get_audio_devices()
    
    def cleanup(self):
        """Clean up resources"""
        self.stop() 