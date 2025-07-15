"""
SIP Protocol Implementation
"""

import socket
import logging
import threading
from typing import Optional, Callable, Dict, Any

from ..models.account import SIPAccount
from .messages import SIPMessage, SIPMessageParser
from ..utils.helpers import generate_call_id, generate_tag, generate_branch

logger = logging.getLogger(__name__)


class SIPProtocol:
    """SIP protocol implementation"""
    
    def __init__(self, account: SIPAccount):
        """Initialize SIP protocol"""
        self.account = account
        self.socket: Optional[socket.socket] = None
        self.parser = SIPMessageParser()
        self.running = False
        self.receive_thread: Optional[threading.Thread] = None
        
        # Callbacks
        self.on_response_received: Optional[Callable[[SIPMessage], None]] = None
        self.on_request_received: Optional[Callable[[SIPMessage], None]] = None
        self.on_message_received: Optional[Callable[[str], None]] = None
        
        logger.info("SIP protocol initialized")
    
    def start(self) -> bool:
        """Start the SIP protocol"""
        try:
            # Create UDP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(('', 0))  # Bind to any available port
            
            self.running = True
            
            # Start receive thread
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            
            logger.info("SIP protocol started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start SIP protocol: {e}")
            return False
    
    def stop(self):
        """Stop the SIP protocol"""
        self.running = False
        
        if self.socket:
            self.socket.close()
            self.socket = None
        
        if self.receive_thread:
            self.receive_thread.join(timeout=1.0)
        
        logger.info("SIP protocol stopped")
    
    def send_message(self, message: str, address: tuple) -> bool:
        """Send a SIP message"""
        try:
            if not self.socket:
                return False
            
            self.socket.sendto(message.encode('utf-8'), address)
            logger.debug(f"Sent SIP message to {address}: {message[:100]}...")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SIP message: {e}")
            return False
    
    def _receive_loop(self):
        """Receive loop for incoming messages"""
        while self.running and self.socket:
            try:
                data, address = self.socket.recvfrom(8192)
                message_str = data.decode('utf-8')
                
                logger.debug(f"Received SIP message from {address}: {message_str[:100]}...")
                
                # Parse message
                message = self.parser.parse(message_str)
                
                # Call callbacks
                if self.on_message_received:
                    self.on_message_received(message_str)
                
                if message.is_response and self.on_response_received:
                    self.on_response_received(message)
                elif message.is_request and self.on_request_received:
                    self.on_request_received(message)
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    logger.error(f"Error in receive loop: {e}")
                break
    
    def create_register_message(self) -> str:
        """Create a REGISTER message"""
        call_id = generate_call_id(self.account.domain)
        tag = generate_tag()
        branch = generate_branch()
        
        message = f"""REGISTER sip:{self.account.domain} SIP/2.0\r
Via: SIP/2.0/UDP {socket.getfqdn()}:5060;branch={branch}\r
From: <{self.account.uri}>;tag={tag}\r
To: <{self.account.uri}>\r
Call-ID: {call_id}\r
CSeq: 1 REGISTER\r
Contact: <{self.account.contact_uri}>\r
Max-Forwards: 70\r
User-Agent: py-sip-client/1.0.0\r
Content-Length: 0\r
\r
"""
        return message
    
    def create_invite_message(self, target_uri: str, local_rtp_port: int) -> str:
        """Create an INVITE message"""
        call_id = generate_call_id(self.account.domain)
        tag = generate_tag()
        branch = generate_branch()
        
        # Simple SDP body
        sdp_body = f"""v=0\r
o=- 123456 654321 IN IP4 {socket.getfqdn()}\r
s=-\r
c=IN IP4 {socket.getfqdn()}\r
t=0 0\r
m=audio {local_rtp_port} RTP/AVP 0\r
a=rtpmap:0 PCMU/8000\r
"""
        
        message = f"""INVITE {target_uri} SIP/2.0\r
Via: SIP/2.0/UDP {socket.getfqdn()}:5060;branch={branch}\r
From: <{self.account.uri}>;tag={tag}\r
To: <{target_uri}>\r
Call-ID: {call_id}\r
CSeq: 1 INVITE\r
Contact: <{self.account.contact_uri}>\r
Max-Forwards: 70\r
User-Agent: py-sip-client/1.0.0\r
Content-Type: application/sdp\r
Content-Length: {len(sdp_body)}\r
\r
{sdp_body}"""
        
        return message 