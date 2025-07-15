#!/usr/bin/env python3
"""
Simple SIP Client for voip.ms using basic socket programming
"""

import socket
import time
import threading
import hashlib
import random
import os
import sys
from typing import Optional, Dict, Any
import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Load environment variables
load_dotenv()

console = Console()

class SimpleSIPClient:
    """Simple SIP Client using socket programming"""
    
    def __init__(self):
        self.config = {
            'domain': os.getenv('SIP_DOMAIN'),
            'username': os.getenv('SIP_USERNAME'),
            'password': os.getenv('SIP_PASSWORD'),
            'port': int(os.getenv('SIP_PORT', 5060)),
        }
        
        if not all([self.config['domain'], self.config['username'], self.config['password']]):
            console.print("[red]Error: Missing SIP configuration. Please check your .env file.[/red]")
            sys.exit(1)
            
        self.socket = None
        self.registered = False
        self.call_id = None
        self.local_tag = None
        self.remote_tag = None
        self.contact_uri = None
        self.cseq = 1
        self.branch = None
        
    def generate_call_id(self):
        """Generate a unique call ID"""
        return f"{random.randint(100000, 999999)}@{self.config['domain']}"
    
    def generate_tag(self):
        """Generate a unique tag"""
        return f"{random.randint(100000, 999999)}"
    
    def generate_branch(self):
        """Generate a unique branch"""
        return f"z9hG4bK{random.randint(100000, 999999)}"
    
    def extract_sip_headers(self, response: str):
        """Extract important headers from SIP response"""
        lines = response.split('\r\n')
        for line in lines:
            if line.startswith('To:'):
                # Extract remote tag from To header
                if 'tag=' in line:
                    self.remote_tag = line.split('tag=')[1].split(';')[0].strip()
            elif line.startswith('Contact:'):
                # Extract contact URI
                if '<' in line and '>' in line:
                    self.contact_uri = line.split('<')[1].split('>')[0].strip()
                else:
                    # Simple format without < >
                    self.contact_uri = line.split('Contact:')[1].strip().split(';')[0].strip()
    
    def create_sip_message(self, method: str, uri: str, headers: Dict[str, str], body: str = "") -> str:
        """Create a SIP message"""
        message = f"{method} {uri} SIP/2.0\r\n"
        
        for header, value in headers.items():
            message += f"{header}: {value}\r\n"
        
        message += f"Content-Length: {len(body)}\r\n"
        message += "\r\n"
        message += body
        
        return message
    
    def send_register(self) -> bool:
        """Send REGISTER request"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(10)
            
            # Generate unique identifiers
            self.call_id = self.generate_call_id()
            self.local_tag = self.generate_tag()
            self.branch = self.generate_branch()
            
            # Create REGISTER request
            uri = f"sip:{self.config['domain']}"
            headers = {
                'Via': f"SIP/2.0/UDP {socket.gethostname()}:{self.config['port']};branch={self.branch}",
                'From': f"<sip:{self.config['username']}@{self.config['domain']}>;tag={self.local_tag}",
                'To': f"<sip:{self.config['username']}@{self.config['domain']}>",
                'Call-ID': self.call_id,
                'CSeq': f"{self.cseq} REGISTER",
                'Contact': f"<sip:{self.config['username']}@{socket.gethostname()}:{self.config['port']}>",
                'Max-Forwards': '70',
                'User-Agent': 'Python SIP Client 1.0',
                'Expires': '3600'
            }
            
            message = self.create_sip_message('REGISTER', uri, headers)
            
            if os.getenv('SIP_CLIENT_DEBUG'):
                console.print(f"[yellow]Sending REGISTER request:[/yellow]\n{message}")

            # Send to server
            server_addr = (self.config['domain'], self.config['port'])
            self.socket.sendto(message.encode(), server_addr)
            
            # Wait for response
            response, addr = self.socket.recvfrom(4096)
            response_str = response.decode()
            
            if os.getenv('SIP_CLIENT_DEBUG'):
                console.print(f"[yellow]Received response:[/yellow]\n{response_str}")

            console.print(f"[blue]SIP Response:[/blue]\n{response_str}")
            
            if "401 Unauthorized" in response_str or "407 Proxy Authentication Required" in response_str:
                # Handle authentication
                return self.handle_authentication(response_str, 'REGISTER', uri)
            elif "200 OK" in response_str:
                self.registered = True
                console.print("[green]✓ Successfully registered with SIP server[/green]")
                return True
            else:
                console.print(f"[red]Registration failed: {response_str}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Registration error: {e}[/red]")
            return False
    
    def handle_authentication(self, response: str, method: str, uri: str) -> bool:
        """Handle SIP authentication"""
        try:
            # Parse authentication challenge
            auth_header = None
            for line in response.split('\r\n'):
                if line.startswith('WWW-Authenticate:') or line.startswith('Proxy-Authenticate:'):
                    auth_header = line
                    break
            
            if not auth_header:
                console.print("[red]No authentication header found[/red]")
                return False
            
            # Extract realm, nonce, etc.
            realm = None
            nonce = None
            
            parts = auth_header.split(',')
            for part in parts:
                part = part.strip()
                if 'realm=' in part:
                    realm = part.split('realm=')[1].strip('"')
                elif 'nonce=' in part:
                    nonce = part.split('nonce=')[1].strip('"')
            
            if not realm or not nonce:
                console.print("[red]Invalid authentication challenge[/red]")
                return False
            
            # Calculate response
            ha1 = hashlib.md5(f"{self.config['username']}:{realm}:{self.config['password']}".encode()).hexdigest()
            ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
            response_hash = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode()).hexdigest()
            
            # Create authenticated request
            self.cseq += 1
            self.branch = self.generate_branch()
            
            headers = {
                'Via': f"SIP/2.0/UDP {socket.gethostname()}:{self.config['port']};branch={self.branch}",
                'From': f"<sip:{self.config['username']}@{self.config['domain']}>;tag={self.local_tag}",
                'To': f"<sip:{self.config['username']}@{self.config['domain']}>",
                'Call-ID': self.call_id,
                'CSeq': f"{self.cseq} {method}",
                'Contact': f"<sip:{self.config['username']}@{socket.gethostname()}:{self.config['port']}>",
                'Max-Forwards': '70',
                'User-Agent': 'Python SIP Client 1.0',
                'Authorization': f'Digest username="{self.config["username"]}", realm="{realm}", nonce="{nonce}", uri="{uri}", response="{response_hash}"'
            }
            
            if method == 'REGISTER':
                headers['Expires'] = '3600'
                message = self.create_sip_message(method, uri, headers)
            elif method == 'INVITE':
                headers['Content-Type'] = 'application/sdp'
                # Add SDP body for INVITE - compatible with voip.ms
                local_ip = socket.gethostbyname(socket.gethostname())
                sdp_body = f"""v=0
o={self.config['username']} 123456 123456 IN IP4 {local_ip}
s=Python SIP Client
c=IN IP4 {local_ip}
t=0 0
m=audio 10000 RTP/AVP 0 8 18 101
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:18 G729/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
a=sendrecv
"""
                message = self.create_sip_message(method, uri, headers, sdp_body)
            else:
                message = self.create_sip_message(method, uri, headers)
            
            # Send authenticated request
            server_addr = (self.config['domain'], self.config['port'])
            self.socket.sendto(message.encode(), server_addr)
            
            if os.getenv('SIP_CLIENT_DEBUG'):
                console.print(f"[yellow]Sending authenticated {method} request:[/yellow]\n{message}")

            # Wait for response
            response, addr = self.socket.recvfrom(4096)
            response_str = response.decode()
            
            if os.getenv('SIP_CLIENT_DEBUG'):
                console.print(f"[yellow]Received response:[/yellow]\n{response_str}")

            console.print(f"[blue]Authenticated Response:[/blue]\n{response_str}")
            
            if "200 OK" in response_str:
                if method == 'REGISTER':
                    self.registered = True
                    console.print("[green]✓ Successfully registered with authentication[/green]")
                elif method == 'INVITE':
                    console.print("[green]Call connected![/green]")
                    self.send_ack()
                return True
            elif "100 Trying" in response_str and method == 'INVITE':
                console.print("[yellow]Call is being processed...[/yellow]")
                # Wait for more responses
                try:
                    response, addr = self.socket.recvfrom(4096)
                    response_str = response.decode()
                    console.print(f"[blue]Call Update:[/blue]\n{response_str}")
                    
                    if "183 Session Progress" in response_str:
                        console.print("[blue]Session in progress...[/blue]")
                        # Wait for more responses
                        response, addr = self.socket.recvfrom(4096)
                        response_str = response.decode()
                        console.print(f"[blue]Call Update:[/blue]\n{response_str}")
                    
                    if "180 Ringing" in response_str:
                        console.print("[blue]Phone is ringing...[/blue]")
                        # Wait for answer
                        response, addr = self.socket.recvfrom(4096)
                        response_str = response.decode()
                        console.print(f"[blue]Call Update:[/blue]\n{response_str}")
                    
                    if "200 OK" in response_str:
                        console.print("[green]Call connected![/green]")
                        # Extract remote tag and contact URI from 200 OK response
                        self.extract_sip_headers(response_str)
                        self.send_ack()
                        return True
                    elif "486 Busy Here" in response_str:
                        console.print("[yellow]Number is busy[/yellow]")
                        return False
                    elif "404 Not Found" in response_str:
                        console.print("[yellow]Number not found[/yellow]")
                        return False
                    elif "480 Temporarily Unavailable" in response_str:
                        console.print("[yellow]Number temporarily unavailable[/yellow]")
                        return False
                    else:
                        console.print(f"[red]Call failed: {response_str}[/red]")
                        return False
                except Exception as e:
                    console.print(f"[red]Error waiting for call response: {e}[/red]")
                    return False
            else:
                console.print(f"[red]Authentication failed: {response_str}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Authentication error: {e}[/red]")
            return False
    
    def make_call(self, number: str) -> bool:
        """Make an outgoing call"""
        if not self.registered:
            console.print("[red]Not registered. Please register first.[/red]")
            return False
        
        try:
            # Format the number
            if not number.startswith('+'):
                number = f"+1{number}"  # Assuming US numbers
            
            # Generate new call identifiers
            self.call_id = self.generate_call_id()
            self.local_tag = self.generate_tag()
            self.branch = self.generate_branch()
            self.cseq = 1
            
            # Create INVITE request
            uri = f"sip:{number}@{self.config['domain']}"
            headers = {
                'Via': f"SIP/2.0/UDP {socket.gethostname()}:{self.config['port']};branch={self.branch}",
                'From': f"<sip:{self.config['username']}@{self.config['domain']}>;tag={self.local_tag}",
                'To': f"<sip:{number}@{self.config['domain']}>",
                'Call-ID': self.call_id,
                'CSeq': f"{self.cseq} INVITE",
                'Contact': f"<sip:{self.config['username']}@{socket.gethostname()}:{self.config['port']}>",
                'Max-Forwards': '70',
                'User-Agent': 'Python SIP Client 1.0',
                'Content-Type': 'application/sdp'
            }
            
            # Simple SDP body (Session Description Protocol) - compatible with voip.ms
            local_ip = socket.gethostbyname(socket.gethostname())
            sdp_body = f"""v=0
o={self.config['username']} 123456 123456 IN IP4 {local_ip}
s=Python SIP Client
c=IN IP4 {local_ip}
t=0 0
m=audio 10000 RTP/AVP 0 8 18 101
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:18 G729/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
a=sendrecv
"""
            
            message = self.create_sip_message('INVITE', uri, headers, sdp_body)
            
            console.print(f"[blue]Calling {number}...[/blue]")
            
            if os.getenv('SIP_CLIENT_DEBUG'):
                console.print(f"[yellow]Sending INVITE request:[/yellow]\n{message}")

            # Send INVITE
            server_addr = (self.config['domain'], self.config['port'])
            self.socket.sendto(message.encode(), server_addr)
            
            # Wait for response
            response, addr = self.socket.recvfrom(4096)
            response_str = response.decode()
            
            if os.getenv('SIP_CLIENT_DEBUG'):
                console.print(f"[yellow]Received response:[/yellow]\n{response_str}")

            console.print(f"[blue]Call Response:[/blue]\n{response_str}")
            
            if "100 Trying" in response_str:
                console.print("[yellow]Call is being processed...[/yellow]")
                # Wait for more responses
                response, addr = self.socket.recvfrom(4096)
                response_str = response.decode()
                console.print(f"[blue]Call Update:[/blue]\n{response_str}")
            
            if "180 Ringing" in response_str:
                console.print("[blue]Phone is ringing...[/blue]")
                # Wait for answer
                response, addr = self.socket.recvfrom(4096)
                response_str = response.decode()
                console.print(f"[blue]Call Update:[/blue]\n{response_str}")
            
            if "401 Unauthorized" in response_str or "407 Proxy Authentication Required" in response_str:
                # Handle authentication for INVITE
                return self.handle_authentication(response_str, 'INVITE', uri)
            elif "200 OK" in response_str:
                console.print("[green]Call connected![/green]")
                # Extract remote tag and contact URI from 200 OK response
                self.extract_sip_headers(response_str)
                # Send ACK
                self.send_ack()
                return True
            else:
                console.print(f"[red]Call failed: {response_str}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Call error: {e}[/red]")
            return False
    
    def send_ack(self):
        """Send ACK message"""
        try:
            # Use the contact URI from the 200 OK response, or fall back to domain
            if self.contact_uri:
                uri = self.contact_uri
            else:
                uri = f"sip:{self.config['domain']}"
            
            # Generate new branch for ACK
            ack_branch = self.generate_branch()
            
            headers = {
                'Via': f"SIP/2.0/UDP {socket.gethostname()}:{self.config['port']};branch={ack_branch}",
                'From': f"<sip:{self.config['username']}@{self.config['domain']}>;tag={self.local_tag}",
                'To': f"<sip:{self.config['username']}@{self.config['domain']}>;tag={self.remote_tag}",
                'Call-ID': self.call_id,
                'CSeq': f"{self.cseq} ACK",
                'Max-Forwards': '70',
                'User-Agent': 'Python SIP Client 1.0'
            }
            
            message = self.create_sip_message('ACK', uri, headers)
            
            server_addr = (self.config['domain'], self.config['port'])
            self.socket.sendto(message.encode(), server_addr)
            
            console.print(f"[green]ACK sent to {uri}[/green]")
            
        except Exception as e:
            console.print(f"[red]ACK error: {e}[/red]")
    
    def send_session_refresh(self):
        """Send session refresh (re-INVITE) to keep the session alive"""
        try:
            if not self.call_id or not self.remote_tag:
                return
                
            self.cseq += 1
            
            # Use the contact URI from the 200 OK response, or fall back to domain
            if self.contact_uri:
                uri = self.contact_uri
            else:
                uri = f"sip:{self.config['domain']}"
            
            headers = {
                'Via': f"SIP/2.0/UDP {socket.gethostname()}:{self.config['port']};branch={self.generate_branch()}",
                'From': f"<sip:{self.config['username']}@{self.config['domain']}>;tag={self.local_tag}",
                'To': f"<sip:{self.config['username']}@{self.config['domain']}>;tag={self.remote_tag}",
                'Call-ID': self.call_id,
                'CSeq': f"{self.cseq} INVITE",
                'Max-Forwards': '70',
                'User-Agent': 'Python SIP Client 1.0',
                'Content-Type': 'application/sdp'
            }
            
            # Simple SDP body for session refresh
            local_ip = socket.gethostbyname(socket.gethostname())
            sdp_body = f"""v=0
o={self.config['username']} 123456 123456 IN IP4 {local_ip}
s=Python SIP Client
c=IN IP4 {local_ip}
t=0 0
m=audio 10000 RTP/AVP 0 8 18 101
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:18 G729/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
a=sendrecv
"""
            
            message = self.create_sip_message('INVITE', uri, headers, sdp_body)
            
            server_addr = (self.config['domain'], self.config['port'])
            self.socket.sendto(message.encode(), server_addr)
            
            console.print("[blue]Session refresh sent[/blue]")
            
        except Exception as e:
            console.print(f"[red]Session refresh error: {e}[/red]")
    
    def hangup(self):
        """Hang up the call"""
        try:
            if not self.call_id:
                console.print("[yellow]No active call to hang up[/yellow]")
                return
            
            self.cseq += 1
            uri = f"sip:{self.config['domain']}"
            headers = {
                'Via': f"SIP/2.0/UDP {socket.gethostname()}:{self.config['port']};branch={self.generate_branch()}",
                'From': f"<sip:{self.config['username']}@{self.config['domain']}>;tag={self.local_tag}",
                'To': f"<sip:{self.config['username']}@{self.config['domain']}>;tag={self.remote_tag}",
                'Call-ID': self.call_id,
                'CSeq': f"{self.cseq} BYE",
                'Max-Forwards': '70',
                'User-Agent': 'Python SIP Client 1.0'
            }
            
            message = self.create_sip_message('BYE', uri, headers)
            
            server_addr = (self.config['domain'], self.config['port'])
            self.socket.sendto(message.encode(), server_addr)
            
            console.print("[yellow]Call ended[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Hangup error: {e}[/red]")
    
    def cleanup(self):
        """Clean up resources"""
        if self.socket:
            self.socket.close()

@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug):
    """Simple Python SIP Client for voip.ms"""
    if debug:
        # In this simple client, "debug" just means printing more.
        # We'll print the messages when they are sent.
        # A more robust client would use the logging module.
        console.print("[yellow]Debug mode enabled[/yellow]")
        # This is a bit of a hack to make the flag available globally
        os.environ['SIP_CLIENT_DEBUG'] = 'true'

@cli.command()
@click.argument('number')
def call(number):
    """Make a call to the specified number"""
    client = SimpleSIPClient()
    
    console.print("[blue]Registering with SIP server...[/blue]")
    if client.send_register():
        console.print(f"[blue]Making call to {number}...[/blue]")
        if client.make_call(number):
            console.print("[green]Call initiated successfully[/green]")
            console.print("[yellow]Call is active. Press Enter to hang up...[/yellow]")
            
            # Set up session keepalive timer
            import threading
            import time
            
            def session_keepalive():
                while client.call_id and client.remote_tag:
                    time.sleep(30)  # Send refresh every 30 seconds
                    if client.call_id and client.remote_tag:
                        client.send_session_refresh()
            
            # Start keepalive thread
            keepalive_thread = threading.Thread(target=session_keepalive, daemon=True)
            keepalive_thread.start()
            
            try:
                input()  # Wait for user input
                client.hangup()
            except KeyboardInterrupt:
                client.hangup()
        else:
            console.print("[red]Call failed[/red]")
    else:
        console.print("[red]Registration failed[/red]")
    
    client.cleanup()

@cli.command()
def register():
    """Register with SIP server"""
    client = SimpleSIPClient()
    
    console.print("[blue]Registering with SIP server...[/blue]")
    if client.send_register():
        console.print("[green]Registration successful[/green]")
    else:
        console.print("[red]Registration failed[/red]")
    
    client.cleanup()

@cli.command()
def status():
    """Show client status"""
    client = SimpleSIPClient()
    
    table = Table(title="SIP Client Configuration")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("SIP Domain", client.config['domain'])
    table.add_row("Username", client.config['username'])
    table.add_row("Port", str(client.config['port']))
    
    console.print(table)
    client.cleanup()

if __name__ == '__main__':
    cli() 