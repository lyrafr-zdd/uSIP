# Contributing to uSIP

Thank you for your interest in contributing to uSIP! We welcome contributions from the community and are pleased to have you join us.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to contact@usip.dev.

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

## 🚀 Getting Started

### Ways to Contribute

- 🐛 **Bug Reports** - Help us identify and fix bugs
- ✨ **Feature Requests** - Suggest new features or improvements
- 📝 **Documentation** - Improve documentation and examples
- 🧪 **Testing** - Add tests or test on different platforms
- 💻 **Code** - Implement new features or fix bugs
- 🎨 **Design** - Improve UI/UX of CLI interface

### Before You Start

1. Check existing [issues](https://github.com/yourusername/uSIP/issues) and [pull requests](https://github.com/yourusername/uSIP/pulls)
2. For major changes, please open an issue first to discuss
3. Make sure you understand the project structure and goals

## 💻 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A SIP account for testing (voip.ms recommended)

### Setup Instructions

```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/uSIP.git
cd uSIP

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install development dependencies
pip install -e ".[dev]"

# 4. Install pre-commit hooks
pre-commit install

# 5. Create your .env file for testing
cp .env.example .env
# Edit .env with your SIP credentials

# 6. Run tests to verify setup
pytest

# 7. Run type checking
mypy src/

# 8. Test the CLI
python usip_cli.py test
```

### Project Structure

```
uSIP/
├── src/sip_client/           # Main library source
│   ├── models/              # Data models
│   ├── audio/               # Audio management  
│   ├── sip/                 # SIP protocol
│   ├── utils/               # Utilities
│   └── client.py            # Main client class
├── usip_cli.py              # CLI interface
├── tests/                   # Test files
├── docs/                    # Documentation
├── pyproject.toml           # Project configuration
└── README.md                # Project documentation
```

## 📋 Contributing Guidelines

### General Guidelines

1. **Be respectful** - Treat all contributors with respect
2. **Stay focused** - Keep discussions and contributions on topic
3. **Test thoroughly** - Ensure your changes work as expected
4. **Document changes** - Update documentation when needed
5. **Follow conventions** - Maintain consistency with existing code

### Git Workflow

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
4. **Commit** your changes (`git commit -m 'Add amazing feature'`)
5. **Push** to the branch (`git push origin feature/amazing-feature`)
6. **Open** a Pull Request

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(client): add support for video calls
fix(auth): resolve digest authentication issue
docs(readme): update installation instructions
test(sip): add unit tests for message parsing
```

## 🔄 Pull Request Process

### Before Submitting

1. **Update documentation** - Ensure README and docstrings are current
2. **Add tests** - Include tests for new functionality
3. **Run tests** - Ensure all tests pass (`pytest`)
4. **Check types** - Run mypy (`mypy src/`)
5. **Format code** - Run black and isort (`black src/ && isort src/`)
6. **Update changelog** - Add entry to CHANGELOG.md

### Pull Request Template

When creating a pull request, please include:

- **Description** - What does this PR do?
- **Motivation** - Why is this change needed?
- **Testing** - How was this tested?
- **Screenshots** - If applicable, add screenshots
- **Checklist** - Complete the PR checklist

### Review Process

1. **Automated checks** - CI/CD pipeline runs tests and checks
2. **Code review** - Maintainers review the code
3. **Feedback** - Address any review comments
4. **Approval** - PR is approved by maintainers
5. **Merge** - PR is merged into main branch

## 🐛 Issue Guidelines

### Bug Reports

When reporting bugs, please include:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
- Python version: [e.g. 3.9.7]
- uSIP version: [e.g. 1.0.0]
- SIP provider: [e.g. voip.ms, Asterisk]

**Additional context**
Add any other context about the problem here.
```

### Feature Requests

When requesting features, please include:

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request.
```

## 🎨 Code Style

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these tools:

- **black** - Code formatting (line length: 88)
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking

### Code Quality Standards

- **Type hints** - All functions must have type hints
- **Docstrings** - All public functions must have docstrings
- **Error handling** - Proper exception handling required
- **Logging** - Use structured logging throughout
- **Comments** - Comment complex logic clearly

### Example Code Style

```python
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class SIPClient:
    """SIP client for voice communication.
    
    This class provides a high-level interface for SIP operations
    including registration, calling, and session management.
    
    Args:
        account: SIP account configuration
        
    Example:
        >>> client = SIPClient(account)
        >>> client.start()
        >>> client.register()
    """
    
    def __init__(self, account: SIPAccount) -> None:
        self.account = account
        self._calls: Dict[str, CallInfo] = {}
        logger.info("SIP client initialized")
    
    def make_call(self, target_uri: str) -> Optional[str]:
        """Make an outgoing call.
        
        Args:
            target_uri: Target SIP URI or phone number
            
        Returns:
            Call ID if successful, None otherwise
            
        Raises:
            SIPError: If call setup fails
        """
        try:
            # Implementation here
            logger.info(f"Making call to {target_uri}")
            return call_id
        except Exception as e:
            logger.error(f"Call failed: {e}")
            raise SIPError(f"Failed to make call: {e}")
```

## 🧪 Testing

### Test Requirements

- **Unit tests** - Test individual functions and classes
- **Integration tests** - Test component interactions
- **End-to-end tests** - Test complete workflows
- **Coverage** - Maintain >90% test coverage

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v

# Run tests for specific SIP provider
pytest -k "voip_ms"
```

### Writing Tests

```python
import pytest
from sip_client import SIPClient, SIPAccount

class TestSIPClient:
    """Test SIP client functionality."""
    
    @pytest.fixture
    def account(self):
        return SIPAccount(
            username="test",
            password="test", 
            domain="test.com"
        )
    
    @pytest.fixture
    def client(self, account):
        return SIPClient(account)
    
    def test_client_initialization(self, client, account):
        """Test client initializes correctly."""
        assert client.account == account
        assert not client.calls
    
    def test_make_call_success(self, client):
        """Test successful call creation."""
        call_id = client.make_call("+1234567890")
        assert call_id is not None
        assert call_id in client.calls
```

## 📚 Documentation

### Documentation Requirements

- **README** - Keep README.md up to date
- **Docstrings** - All public APIs must have docstrings
- **Type hints** - All functions must have type annotations
- **Examples** - Include usage examples in docstrings
- **Changelog** - Update CHANGELOG.md for all changes

### Documentation Style

```python
def make_call(self, target_uri: str, timeout: int = 30) -> Optional[str]:
    """Make an outgoing SIP call.
    
    Initiates a SIP call to the specified target URI. The call will
    automatically handle authentication, media negotiation, and session
    establishment.
    
    Args:
        target_uri: Target SIP URI (e.g., 'sip:user@domain.com') or 
                   phone number (e.g., '+1234567890')
        timeout: Call setup timeout in seconds (default: 30)
        
    Returns:
        Unique call ID if successful, None if call setup failed
        
    Raises:
        SIPError: If SIP protocol error occurs
        NetworkError: If network connectivity issues
        AuthError: If authentication fails
        
    Example:
        >>> client = SIPClient(account)
        >>> call_id = client.make_call('+1234567890')
        >>> if call_id:
        ...     print(f"Call initiated: {call_id}")
        
    Note:
        Client must be registered before making calls.
    """
```

## 🏷️ Release Process

### Version Numbers

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

### Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag release in Git
- [ ] Publish to PyPI

## 🆘 Getting Help

### Communication Channels

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and discussions
- **Email** - contact@usip.dev for private matters

### Support Guidelines

- **Search first** - Check existing issues and documentation
- **Be specific** - Provide clear, detailed information
- **Be patient** - Maintainers are volunteers
- **Be respectful** - Follow our code of conduct

## 🎉 Recognition

Contributors will be recognized in:
- **README.md** - Contributors section
- **Release notes** - Acknowledgment in releases
- **GitHub** - Contributor badge and stats

Thank you for contributing to uSIP! 🙏

---

**Happy Coding!** 💻✨ 