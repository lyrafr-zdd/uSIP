#!/usr/bin/env python3
"""
Simple SIP Client using the py-sip-client library
A command-line interface for making SIP calls using the modular library
"""

import os
import sys
import time
import threading
import logging
import click
from rich.console import Console
from rich.table import Table

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from sip_client import SIPClient, SIPAccount, CallState, RegistrationState
except ImportError as e:
    print(f"Error importing sip_client library: {e}")
    print("Make sure the uSIP library is properly installed")
    sys.exit(1)

console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class SimpleSIPClientCLI:
    """Simple SIP Client CLI using the py-sip-client library"""
    
    def __init__(self):
        """Initialize the CLI client"""
        self.client = None
        self.account = None
        self.active_call_id = None
        
    def load_config(self):
        """Load configuration from environment"""
        try:
            self.account = SIPAccount(
                username=os.getenv('SIP_USERNAME', ''),
                password=os.getenv('SIP_PASSWORD', ''),
                domain=os.getenv('SIP_DOMAIN', ''),
                port=int(os.getenv('SIP_PORT', 5060))
            )
            
            if not all([self.account.username, self.account.password, self.account.domain]):
                console.print("[red]Error: Missing SIP configuration. Please check your .env file.[/red]")
                console.print("Required variables: SIP_USERNAME, SIP_PASSWORD, SIP_DOMAIN")
                return False
            
            return True
            
        except Exception as e:
            console.print(f"[red]Error loading configuration: {e}[/red]")
            return False
    
    def initialize_client(self):
        """Initialize the SIP client"""
        try:
            self.client = SIPClient(self.account)
            return self.client.start()
        except Exception as e:
            console.print(f"[red]Error initializing SIP client: {e}[/red]")
            return False
    
    def register(self):
        """Register with SIP server"""
        if not self.client:
            if not self.load_config() or not self.initialize_client():
                return False
        
        console.print("[blue]Registering with SIP server...[/blue]")
        
        try:
            success = self.client.register()
            if success:
                console.print("[green]Registration successful[/green]")
            else:
                console.print("[red]Registration failed[/red]")
            return success
        except Exception as e:
            console.print(f"[red]Registration error: {e}[/red]")
            return False
    
    def make_call(self, number):
        """Make a call to the specified number"""
        if not self.client:
            if not self.load_config() or not self.initialize_client():
                return False
        
        # Register first if not already registered
        if self.client.registration_state != RegistrationState.REGISTERED:
            if not self.register():
                return False
        
        console.print(f"[blue]Making call to {number}...[/blue]")
        
        try:
            call_id = self.client.make_call(number)
            if call_id:
                self.active_call_id = call_id
                console.print("[green]Call initiated successfully[/green]")
                console.print("[yellow]Call is active. Press Enter to hang up...[/yellow]")
                
                # Set up session keepalive (simplified)
                def session_keepalive():
                    while self.active_call_id:
                        time.sleep(30)
                        # In a real implementation, we'd send keepalive messages
                        if self.active_call_id:
                            logging.info("Session keepalive")
                
                # Start keepalive thread
                keepalive_thread = threading.Thread(target=session_keepalive, daemon=True)
                keepalive_thread.start()
                
                try:
                    input()  # Wait for user input
                    self.hangup()
                except KeyboardInterrupt:
                    self.hangup()
                
                return True
            else:
                console.print("[red]Call failed[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Call error: {e}[/red]")
            return False
    
    def hangup(self):
        """Hang up the active call"""
        if self.client and self.active_call_id:
            try:
                success = self.client.hangup(self.active_call_id)
                if success:
                    console.print("[green]Call ended[/green]")
                else:
                    console.print("[yellow]Call may have already ended[/yellow]")
                self.active_call_id = None
                return success
            except Exception as e:
                console.print(f"[red]Hangup error: {e}[/red]")
                return False
        return True
    
    def show_status(self):
        """Show client status"""
        if not self.load_config():
            return
        
        table = Table(title="SIP Client Configuration")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("SIP Domain", self.account.domain)
        table.add_row("Username", self.account.username)
        table.add_row("Port", str(self.account.port))
        
        if self.client:
            table.add_row("Registration State", str(self.client.registration_state))
            active_calls = self.client.get_calls()
            table.add_row("Active Calls", str(len(active_calls)))
        else:
            table.add_row("Registration State", "Not initialized")
            table.add_row("Active Calls", "0")
        
        console.print(table)
    
    def cleanup(self):
        """Clean up resources"""
        if self.client:
            try:
                self.client.cleanup()
            except Exception as e:
                console.print(f"[yellow]Cleanup warning: {e}[/yellow]")

# Create global CLI instance
cli_client = SimpleSIPClientCLI()

@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug):
    """Simple Python SIP Client using py-sip-client library"""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        console.print("[yellow]Debug mode enabled[/yellow]")

@cli.command()
@click.argument('number')
def call(number):
    """Make a call to the specified number"""
    try:
        cli_client.make_call(number)
    finally:
        cli_client.cleanup()

@cli.command()
def register():
    """Register with SIP server"""
    try:
        cli_client.register()
    finally:
        cli_client.cleanup()

@cli.command()
def status():
    """Show client status"""
    try:
        cli_client.show_status()
    finally:
        cli_client.cleanup()

@cli.command()
def test():
    """Test the SIP client configuration"""
    try:
        console.print("[blue]Testing SIP client configuration...[/blue]")
        
        if not cli_client.load_config():
            return
        
        console.print("[green]✓[/green] Configuration loaded successfully")
        
        if not cli_client.initialize_client():
            console.print("[red]✗[/red] Failed to initialize SIP client")
            return
        
        console.print("[green]✓[/green] SIP client initialized successfully")
        
        if cli_client.register():
            console.print("[green]✓[/green] Registration successful")
            console.print("[blue]SIP client is ready for calls![/blue]")
        else:
            console.print("[red]✗[/red] Registration failed")
        
    except Exception as e:
        console.print(f"[red]Test failed: {e}[/red]")
    finally:
        cli_client.cleanup()

if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
    finally:
        cli_client.cleanup() 