"""
Utility functions for SIP client
"""

import random
import socket


def generate_call_id(domain: str = None) -> str: # type: ignore
    """Generate a unique call ID"""
    if domain is None:
        domain = socket.gethostname()
    return f"{random.randint(100000, 999999)}@{domain}"


def generate_tag() -> str:
    """Generate a unique tag"""
    return f"{random.randint(100000, 999999)}"


def generate_branch() -> str:
    """Generate a unique branch identifier"""
    return f"z9hG4bK{random.randint(100000, 999999)}"


# def get_local_ip() -> str:
#     """Get local IP address"""
#     return socket.gethostbyname(socket.gethostname())


def get_hostname() -> str:
    """Get local hostname"""
    return socket.gethostname() 


def get_local_ip() -> str:
    """Get the primary local IPv4 address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a public IP (no packets sent, just used for routing info)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

def get_public_ip(
    stun_host: str = "stun.l.google.com",
    stun_port: int = 19302
) -> str:
    """
    Discover the public IP address using a STUN server.
    
    Returns:
        str: The detected public IPv4 address.
    Raises:
        RuntimeError: If detection fails.
    """
    import stun
    nat_type, external_ip, external_port = stun.get_ip_info(stun_host=stun_host, stun_port=stun_port)
    if not external_ip:
        raise RuntimeError("Failed to detect public IP via STUN.")
    return str(external_ip)

def get_free_udp_port(range_min: int = 10000, range_max: int = 20000):
    # Try a few random ports in the RTP range first, fallback to OS-chosen
    for _ in range(6):
        port = random.randint(range_min, range_max)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind(('', port))
            s.setblocking(False)
            # keep socket open or return port and close? depends on architecture.
            # If code expects an integer port, we should close and return the port.
            # s.close()
            return port
        except OSError:
            s.close()
            continue
    # last resort: let OS choose an ephemeral port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port
