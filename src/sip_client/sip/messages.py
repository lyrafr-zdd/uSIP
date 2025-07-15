"""
SIP Message Parser
"""

import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SIPMessage:
    """Represents a SIP message"""
    
    def __init__(self, raw_message: str):
        self.raw = raw_message
        self.headers: Dict[str, str] = {}
        self.body = ""
        self.method = ""
        self.uri = ""
        self.version = ""
        self.status_code = 0
        self.reason_phrase = ""
        
        self._parse()
    
    def _parse(self):
        """Parse the raw SIP message"""
        lines = self.raw.split('\n')
        if not lines:
            return
        
        # Parse first line (request line or status line)
        first_line = lines[0].strip()
        if first_line.startswith('SIP/2.0'):
            # Response
            parts = first_line.split(' ', 2)
            if len(parts) >= 2:
                self.version = parts[0]
                try:
                    self.status_code = int(parts[1])
                except ValueError:
                    pass
                if len(parts) >= 3:
                    self.reason_phrase = parts[2]
        else:
            # Request
            parts = first_line.split(' ')
            if len(parts) >= 3:
                self.method = parts[0]
                self.uri = parts[1]
                self.version = parts[2]
        
        # Parse headers
        header_end = 1
        for i, line in enumerate(lines[1:], 1):
            line = line.strip()
            if not line:
                header_end = i + 1
                break
            
            if ':' in line:
                key, value = line.split(':', 1)
                self.headers[key.strip()] = value.strip()
        
        # Parse body
        if header_end < len(lines):
            self.body = '\n'.join(lines[header_end:])
    
    @property
    def is_request(self) -> bool:
        """Check if this is a request message"""
        return bool(self.method)
    
    @property
    def is_response(self) -> bool:
        """Check if this is a response message"""
        return self.status_code > 0
    
    def get_header(self, name: str) -> Optional[str]:
        """Get a header value by name (case-insensitive)"""
        for key, value in self.headers.items():
            if key.lower() == name.lower():
                return value
        return None


class SIPMessageParser:
    """Parses SIP messages"""
    
    def __init__(self):
        """Initialize message parser"""
        pass
    
    def parse(self, raw_message: str) -> SIPMessage:
        """Parse a raw SIP message"""
        return SIPMessage(raw_message)
    
    def is_complete_message(self, data: str) -> bool:
        """Check if the data contains a complete SIP message"""
        # Simple check for double CRLF indicating end of headers
        return '\r\n\r\n' in data or '\n\n' in data 