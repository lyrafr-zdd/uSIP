# uSIP - Modern Python SIP Client Library

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, professional Python SIP client library with voice support, modular architecture, and comprehensive CLI interface. Perfect for building VoIP applications, softphones, and telecommunications tools.

## ✨ Features

### 🚀 Core Features
- **Full SIP Protocol Support** - RFC 3261 compliant implementation
- **Voice Communication** - RTP-based audio streaming with device management
- **Authentication** - SIP digest authentication support
- **Registration Management** - Automatic re-registration with keep-alive
- **Call Management** - Multiple concurrent calls with state tracking
- **Modular Architecture** - Clean separation of concerns

### 🛠️ Developer Experience
- **Rich CLI Interface** - Beautiful command-line interface with colored output
- **Comprehensive Logging** - Structured logging with multiple output formats
- **Type Safety** - Full type hints and mypy compliance
- **Professional APIs** - Clean, intuitive programming interfaces
- **Extensive Documentation** - Complete guides and examples
- **Cross-Platform** - Works on Windows, macOS, and Linux

### 📞 Telecommunications
- **SIP Providers** - Works with Asterisk, FreeSWITCH, voip.ms, Twilio SIP
- **Audio Devices** - Enumeration and runtime switching
- **Session Management** - Proper SIP session handling
- **Error Recovery** - Robust error handling and recovery
- **Network Resilience** - NAT traversal and network change handling

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (when published)
pip install usip

# Or install from source
git clone https://github.com/yourusername/uSIP.git
cd uSIP
pip install -e .
```

### Configuration

Create a `.env` file with your SIP credentials:

```env
SIP_DOMAIN=your-sip-provider.com
SIP_USERNAME=your-username
SIP_PASSWORD=your-password
SIP_PORT=5060
```

### CLI Usage

```bash
# Test your configuration
usip-cli test

# Register with SIP server
usip-cli register

# Make a call
usip-cli call +1234567890

# Show status
usip-cli status
```

### Library Usage

```python
from sip_client import SIPClient, SIPAccount

# Create account
account = SIPAccount(
    username="your-username",
    password="your-password", 
    domain="your-sip-provider.com"
)

# Initialize client
client = SIPClient(account)
client.start()

# Register
if client.register():
    print("Registration successful!")
    
    # Make a call
    call_id = client.make_call("sip:+1234567890@provider.com")
    if call_id:
        print(f"Call initiated: {call_id}")
        
        # Hang up after some time
        input("Press Enter to hang up...")
        client.hangup(call_id)

# Clean up
client.stop()
```

## 📚 Documentation

### API Reference

#### SIPClient
Main client class for SIP operations:

```python
class SIPClient:
    def __init__(self, account: SIPAccount)
    def start() -> bool
    def stop()
    def register() -> bool
    def make_call(target_uri: str) -> Optional[str]
    def hangup(call_id: str) -> bool
    def get_calls() -> List[CallInfo]
```

#### SIPAccount  
Account configuration:

```python
@dataclass
class SIPAccount:
    username: str
    password: str
    domain: str
    port: int = 5060
    display_name: Optional[str] = None
```

#### Call States
```python
class CallState(Enum):
    IDLE = auto()
    CALLING = auto()
    RINGING = auto()
    CONNECTED = auto()
    DISCONNECTED = auto()
    FAILED = auto()
```

### CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `test` | Test SIP configuration | `usip-cli test` |
| `register` | Register with SIP server | `usip-cli register` |
| `call <number>` | Make a call | `usip-cli call +1234567890` |
| `status` | Show client status | `usip-cli status` |

### Configuration

Environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SIP_DOMAIN` | SIP server domain | Yes | - |
| `SIP_USERNAME` | SIP username | Yes | - |
| `SIP_PASSWORD` | SIP password | Yes | - |
| `SIP_PORT` | SIP server port | No | 5060 |

## 🏗️ Architecture

### Modular Design

```
uSIP/
├── src/sip_client/           # Main library
│   ├── models/              # Data models
│   │   ├── account.py       # SIP account configuration
│   │   ├── call.py          # Call information
│   │   └── enums.py         # State enumerations
│   ├── audio/               # Audio management
│   │   ├── manager.py       # Audio streaming
│   │   └── devices.py       # Device enumeration
│   ├── sip/                 # SIP protocol
│   │   ├── protocol.py      # Core SIP implementation
│   │   └── messages.py      # Message parsing
│   ├── utils/               # Utilities
│   │   └── helpers.py       # Helper functions
│   └── client.py            # Main client class
├── usip_cli.py              # CLI interface
└── pyproject.toml           # Project configuration
```

### Components

- **Client Layer** - High-level SIP client API
- **Protocol Layer** - SIP message handling and networking  
- **Audio Layer** - RTP streaming and device management
- **Model Layer** - Data structures and state management
- **CLI Layer** - Command-line interface

## 🧪 Testing

### Supported Providers

Tested with:
- ✅ **voip.ms** - Full compatibility
- ✅ **Asterisk** - Complete support
- ✅ **FreeSWITCH** - Full functionality
- ✅ **Twilio SIP** - Voice calling
- 🔄 **Other RFC 3261 compliant servers**

### Test Results

```bash
$ usip-cli test
Testing SIP client configuration...
✓ Configuration loaded successfully
✓ SIP client initialized successfully  
✓ Registration successful
SIP client is ready for calls!
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/uSIP.git
cd uSIP

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run type checking
mypy src/

# Format code
black src/
isort src/
```

## 📋 Requirements

- **Python 3.8+**
- **click** - CLI framework
- **rich** - Terminal formatting
- **cryptography** - Authentication

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Built for the Python telecommunications community
- Inspired by modern VoIP standards and practices
- Designed for both beginners and professionals

## 📞 Support

- 📖 **Documentation**: [usip.readthedocs.io](https://usip.readthedocs.io)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/uSIP/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/uSIP/discussions)
- 📧 **Email**: contact@usip.dev

---

**uSIP** - Modern Python SIP Client Library for Professional VoIP Applications 