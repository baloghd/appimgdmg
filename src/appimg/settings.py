"""Settings management for appimg"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class AppSettings:
    """Application settings"""
    play_sound_on_install: bool = True
    sound_theme: str = "default"  # Can be "default", "glass", "bloop", etc.
    auto_make_executable: bool = True  # Automatically make AppImages executable
    

class SettingsManager:
    """Manage application settings"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "appimg"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.settings_file = self.config_dir / "settings.json"
        self._settings = self._load()
    
    def _load(self) -> AppSettings:
        """Load settings from file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                return AppSettings(**data)
            except (json.JSONDecodeError, TypeError):
                pass
        return AppSettings()
    
    def save(self):
        """Save settings to file"""
        with open(self.settings_file, 'w') as f:
            json.dump(asdict(self._settings), f, indent=2)
    
    @property
    def play_sound(self) -> bool:
        return self._settings.play_sound_on_install
    
    @play_sound.setter
    def play_sound(self, value: bool):
        self._settings.play_sound_on_install = value
        self.save()
    
    @property
    def sound_theme(self) -> str:
        return self._settings.sound_theme
    
    @sound_theme.setter
    def sound_theme(self, value: str):
        self._settings.sound_theme = value
        self.save()
    
    @property
    def auto_make_executable(self) -> bool:
        return self._settings.auto_make_executable
    
    @auto_make_executable.setter
    def auto_make_executable(self, value: bool):
        self._settings.auto_make_executable = value
        self.save()
