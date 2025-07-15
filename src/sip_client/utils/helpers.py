"""
Helper Utility Functions
"""

import random
import string
import time
from typing import Optional


def generate_call_id(domain: Optional[str] = None) -> str:
    """Generate a unique call ID"""
    timestamp = str(int(time.time()))
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    if domain:
        return f"{timestamp}_{random_part}@{domain}"
    else:
        return f"{timestamp}_{random_part}"


def generate_tag() -> str:
    """Generate a unique tag for SIP messages"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def generate_branch() -> str:
    """Generate a unique branch parameter"""
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"z9hG4bK{random_part}"


def generate_cseq() -> int:
    """Generate a CSeq number"""
    return random.randint(1, 999999)


def parse_sip_uri(uri: str) -> dict:
    """Parse a SIP URI into components"""
    # Simple parser for sip:user@domain:port format
    result = {
        'scheme': 'sip',
        'user': '',
        'domain': '',
        'port': None
    }
    
    if not uri.startswith('sip:'):
        return result
    
    uri_part = uri[4:]  # Remove 'sip:'
    
    if '@' in uri_part:
        user_part, domain_part = uri_part.split('@', 1)
        result['user'] = user_part
    else:
        domain_part = uri_part
    
    if ':' in domain_part:
        domain, port = domain_part.split(':', 1)
        result['domain'] = domain
        try:
            result['port'] = int(port)
        except ValueError:
            pass
    else:
        result['domain'] = domain_part
    
    return result 