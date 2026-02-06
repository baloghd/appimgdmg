"""Installation logic for AppImages"""

import shutil
import os
import shlex
from pathlib import Path
import subprocess
from datetime import datetime

from .appimage import AppImageInfo
from .installed import InstalledAppsManager, InstalledApp


class AppImageInstaller:
    """Install AppImages to the user's system"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.apps_dir = Path.home() / "Applications"
        self.local_share = Path.home() / ".local" / "share"
        self.applications_dir = self.local_share / "applications"
        self.icons_dir = self.local_share / "icons" / "hicolor"
        self.registry = InstalledAppsManager()
        
    def install(self, appimage_path: str, info: AppImageInfo) -> InstalledApp:
        """Install an AppImage to ~/Applications with desktop integration"""
        appimage_src = Path(appimage_path)
        
        # Ensure directories exist
        self.apps_dir.mkdir(parents=True, exist_ok=True)
        self.applications_dir.mkdir(parents=True, exist_ok=True)
        
        # Use original filename to preserve version info
        target_appimage = self.apps_dir / appimage_src.name
        
        # Desktop file uses sanitized app name
        safe_name = self._sanitize_filename(info.name)
        desktop_file = self.applications_dir / f"{safe_name}.desktop"
        
        if self.debug:
            print(f"[DEBUG] Installing to: {target_appimage}")
        
        try:
            # Copy AppImage
            shutil.copy2(appimage_src, target_appimage)
            target_appimage.chmod(0o755)  # Make executable
            
            # Install icon if found
            if info.icon_path:
                self._install_icon(info.icon_path, info.icon_name)
            
            # Create .desktop file
            self._create_desktop_entry(target_appimage, info)
            
            # Update desktop database
            self._update_desktop_database()
            
            # Register in registry
            installed_app = InstalledApp(
                name=info.name,
                version=info.version or "unknown",
                source_path=str(appimage_src),
                install_path=str(target_appimage),
                icon_name=info.icon_name,
                categories=info.categories,
                install_date=datetime.now().isoformat(),
                comment=info.comment,
                desktop_file=str(desktop_file)
            )
            self.registry.add(installed_app)
            
            if self.debug:
                print(f"[DEBUG] Successfully installed {info.name}")
            
            return installed_app
            
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Installation failed: {e}")
            raise
    
    def _sanitize_filename(self, name: str) -> str:
        """Create a safe filename from app name"""
        # Remove/replace unsafe characters
        unsafe = '<>:"/\\|?*'
        for char in unsafe:
            name = name.replace(char, '')
        return name.strip() or "Application"
    
    def _install_icon(self, icon_path: Path, icon_name: str):
        """Install icon to user's icon directory"""
        if icon_path.suffix == '.svg':
            target_dir = self.icons_dir / "scalable" / "apps"
            target_name = f"{icon_name}.svg"
        else:
            # Try to determine size, default to 128x128
            target_dir = self.icons_dir / "128x128" / "apps"
            target_name = f"{icon_name}.png"
        
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / target_name
        
        if self.debug:
            print(f"[DEBUG] Installing icon: {target_path}")
        
        shutil.copy2(icon_path, target_path)
    
    def _is_electron_app(self, appimage_path: Path) -> bool:
        """Detect if AppImage is Electron-based by checking for Chrome sandbox"""
        try:
            # Test if the app runs without --no-sandbox
            result = subprocess.run(
                [str(appimage_path), "--version"],
                capture_output=True,
                timeout=10
            )
            
            # Check stderr for sandbox-related errors even if exit code is 0
            stderr = result.stderr.decode('utf-8', errors='ignore').lower()
            if 'sandbox' in stderr or 'setuid' in stderr or 'namespace' in stderr:
                return True
                
            # If return code is non-zero, check for sandbox errors
            if result.returncode != 0:
                if 'sandbox' in stderr or 'setuid' in stderr or 'namespace' in stderr:
                    return True
                    
            return False
            
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Error detecting Electron app: {e}")
            return False
    
    def _create_desktop_entry(self, appimage_path: Path, info: AppImageInfo):
        """Create a .desktop file for the installed AppImage"""
        desktop_file = self.applications_dir / f"{self._sanitize_filename(info.name)}.desktop"
        
        # Quote the exec path to handle spaces in filename
        exec_path = shlex.quote(str(appimage_path))
        
        # Check if this is an Electron app that needs --no-sandbox
        is_electron = self._is_electron_app(appimage_path)
        
        if is_electron:
            exec_path = f"{exec_path} --no-sandbox"
            if self.debug:
                print(f"[DEBUG] Detected Electron app, adding --no-sandbox flag")
        
        # Build desktop entry content
        lines = [
            "[Desktop Entry]",
            f"Name={info.name}",
            f"Exec={exec_path}",
            f"Icon={info.icon_name}",
            "Type=Application",
            "Terminal=false",
        ]
        
        if info.categories:
            lines.append(f"Categories={';'.join(info.categories)};")
        
        if info.comment:
            lines.append(f"Comment={info.comment}")
        
        lines.append("")  # Trailing newline
        
        content = "\n".join(lines)
        
        if self.debug:
            print(f"[DEBUG] Creating .desktop file: {desktop_file}")
            print(f"[DEBUG] Content:\n{content}")
        
        desktop_file.write_text(content, encoding="utf-8")
        desktop_file.chmod(0o644)
    
    def _update_desktop_database(self):
        """Update the desktop database to register the new application"""
        try:
            subprocess.run(
                ["update-desktop-database", str(self.applications_dir)],
                capture_output=True,
                check=False
            )
            
            # Also update icon cache
            subprocess.run(
                ["gtk-update-icon-cache", "-f", "-t", str(self.icons_dir)],
                capture_output=True,
                check=False
            )
            
            if self.debug:
                print("[DEBUG] Updated desktop database and icon cache")
                
        except FileNotFoundError:
            # Commands might not be available, that's okay
            if self.debug:
                print("[DEBUG] update-desktop-database or gtk-update-icon-cache not found (optional)")
