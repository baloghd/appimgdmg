"""Sound effects for appimg using libcanberra"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

import subprocess
import shutil
from pathlib import Path


class SoundManager:
    """Manage sound effects for the application"""
    
    def __init__(self):
        self.enabled = True
        self._canberra_available = self._check_canberra()
        
    def _check_canberra(self) -> bool:
        """Check if canberra-gtk-play is available"""
        return shutil.which('canberra-gtk-play') is not None
    
    def play_success(self):
        """Play macOS-style success sound"""
        if not self.enabled or not self._canberra_available:
            return
            
        try:
            # Try to play a success sound
            # 'message' is a standard freedesktop sound that works on most systems
            subprocess.run(
                ['canberra-gtk-play', '-i', 'message'],
                capture_output=True,
                timeout=2
            )
        except (subprocess.TimeoutExpired, Exception):
            pass  # Silently fail if sound can't play
    
    def play_error(self):
        """Play error sound"""
        if not self.enabled or not self._canberra_available:
            return
            
        try:
            subprocess.run(
                ['canberra-gtk-play', '-i', 'dialog-error'],
                capture_output=True,
                timeout=2
            )
        except (subprocess.TimeoutExpired, Exception):
            pass


class MockSoundManager:
    """Mock sound manager when sounds are disabled or unavailable"""
    
    def __init__(self):
        pass
    
    def play_success(self):
        pass
    
    def play_error(self):
        pass
