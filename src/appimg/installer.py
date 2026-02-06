"""Installation logic for AppImages"""

import shutil
import os
from pathlib import Path
import subprocess

from .appimage import AppImageInfo


class AppImageInstaller:
    """Install AppImages to the user's system"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.apps_dir = Path.home() / "Applications"
        self.local_share = Path.home() / ".local" / "share"
        self.applications_dir = self.local_share / "applications"
        self.icons_dir = self.local_share / "icons" / "hicolor"
        
    def install(self, appimage_path: str, info: AppImageInfo) -> bool:
        """Install an AppImage to ~/Applications with desktop integration"""
        appimage_src = Path(appimage_path)
        
        # Ensure directories exist
        self.apps_dir.mkdir(parents=True, exist_ok=True)
        self.applications_dir.mkdir(parents=True, exist_ok=True)
        
        # Create sanitized filename
        safe_name = self._sanitize_filename(info.name)
        target_appimage = self.apps_dir / f"{safe_name}.AppImage"
        
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
            
            if self.debug:
                print(f"[DEBUG] Successfully installed {info.name}")
            
            return True
            
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
    
    def _create_desktop_entry(self, appimage_path: Path, info: AppImageInfo):
        """Create a .desktop file for the installed AppImage"""
        desktop_file = self.applications_dir / f"{self._sanitize_filename(info.name)}.desktop"
        
        # Build desktop entry content
        lines = [
            "[Desktop Entry]",
            f"Name={info.name}",
            f"Exec={appimage_path}",
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
