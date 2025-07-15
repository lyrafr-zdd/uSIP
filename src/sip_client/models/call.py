"""
Call Information Model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

from .enums import CallState


@dataclass
class CallInfo:
    """Information about a SIP call"""
    
    call_id: str
    from_uri: str
    to_uri: str
    state: CallState = CallState.IDLE
    direction: str = "outgoing"  # "incoming" or "outgoing"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    local_tag: Optional[str] = None
    remote_tag: Optional[str] = None
    local_rtp_port: Optional[int] = None
    remote_rtp_port: Optional[int] = None
    remote_rtp_address: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize call timestamps"""
        if self.start_time is None:
            self.start_time = datetime.now()
    
    @property
    def duration(self) -> Optional[float]:
        """Get call duration in seconds"""
        if not self.start_time:
            return None
        
        end_time = self.end_time or datetime.now()
        return (end_time - self.start_time).total_seconds()
    
    @property
    def is_active(self) -> bool:
        """Check if call is in an active state"""
        return self.state in [
            CallState.CALLING,
            CallState.RINGING,
            CallState.CONNECTING,
            CallState.CONNECTED
        ]
    
    @property
    def is_finished(self) -> bool:
        """Check if call is finished"""
        return self.state in [
            CallState.DISCONNECTED,
            CallState.FAILED
        ] 