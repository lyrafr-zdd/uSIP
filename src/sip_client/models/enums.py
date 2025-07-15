"""
Enumerations for SIP Client States
"""

from enum import Enum, auto


class CallState(Enum):
    """Call state enumeration"""
    
    IDLE = auto()
    CALLING = auto()
    RINGING = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    DISCONNECTING = auto()
    DISCONNECTED = auto()
    FAILED = auto()


class RegistrationState(Enum):
    """Registration state enumeration"""
    
    UNREGISTERED = auto()
    REGISTERING = auto()
    REGISTERED = auto()
    UNREGISTERING = auto()
    FAILED = auto() 