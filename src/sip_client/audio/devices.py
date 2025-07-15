"""
Audio Device Management
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AudioDevice:
    """Audio device information"""
    
    id: int
    name: str
    channels: int
    sample_rate: int
    is_input: bool = True
    is_output: bool = True
    is_default: bool = False
    
    def __str__(self) -> str:
        """String representation of the device"""
        direction = []
        if self.is_input:
            direction.append("Input")
        if self.is_output:
            direction.append("Output")
        
        default_str = " (Default)" if self.is_default else ""
        return f"Device {self.id}: {self.name} [{'/'.join(direction)}]{default_str}"


def get_audio_devices() -> List[AudioDevice]:
    """Get list of available audio devices"""
    # Placeholder implementation - returns a mock device
    # In a real implementation, this would enumerate actual audio devices
    return [
        AudioDevice(
            id=0,
            name="Default Audio Device",
            channels=2,
            sample_rate=44100,
            is_input=True,
            is_output=True,
            is_default=True
        )
    ]


def get_default_input_device() -> Optional[AudioDevice]:
    """Get the default input device"""
    devices = get_audio_devices()
    for device in devices:
        if device.is_input and device.is_default:
            return device
    return devices[0] if devices else None


def get_default_output_device() -> Optional[AudioDevice]:
    """Get the default output device"""
    devices = get_audio_devices()
    for device in devices:
        if device.is_output and device.is_default:
            return device
    return devices[0] if devices else None 