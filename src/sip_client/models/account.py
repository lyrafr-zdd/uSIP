"""
SIP Account Configuration Model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SIPAccount:
    """SIP account configuration"""
    
    username: str
    password: str
    domain: str
    port: int = 5060
    display_name: Optional[str] = None
    realm: Optional[str] = None
    
    def __post_init__(self):
        """Validate account configuration"""
        if not self.username:
            raise ValueError("Username is required")
        if not self.password:
            raise ValueError("Password is required")
        if not self.domain:
            raise ValueError("Domain is required")
        if self.port <= 0 or self.port > 65535:
            raise ValueError("Port must be between 1 and 65535")
    
    @property
    def uri(self) -> str:
        """Get the SIP URI for this account"""
        return f"sip:{self.username}@{self.domain}"
    
    @property
    def contact_uri(self) -> str:
        """Get the contact URI for this account"""
        return f"sip:{self.username}@{self.domain}:{self.port}" 