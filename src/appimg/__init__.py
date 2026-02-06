from .main import main, debug_main, list_main, sound_toggle_main
from .appimage import AppImageParser, AppImageInfo
from .installer import AppImageInstaller
from .installed import InstalledAppsManager
from .settings import SettingsManager, AppSettings
from .sound import SoundManager, MockSoundManager

__version__ = "0.1.0"
__all__ = ["main", "debug_main", "list_main", "sound_toggle_main", "AppImageParser", "AppImageInfo", "AppImageInstaller", "InstalledAppsManager", "SettingsManager", "AppSettings", "SoundManager", "MockSoundManager"]

if __name__ == "__main__":
    main()
