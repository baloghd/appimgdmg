from .main import main, debug_main, list_main
from .appimage import AppImageParser, AppImageInfo
from .installer import AppImageInstaller
from .installed import InstalledAppsManager

__version__ = "0.1.0"
__all__ = ["main", "debug_main", "list_main", "AppImageParser", "AppImageInfo", "AppImageInstaller", "InstalledAppsManager"]

if __name__ == "__main__":
    main()
