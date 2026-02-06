#!/usr/bin/env python3
"""Install appimg as the default handler for AppImage files"""

import sys
import shutil
from pathlib import Path
import subprocess

def main():
    """Install appimg desktop entry and set as default handler"""
    
    home = Path.home()
    desktop_dir = home / ".local" / "share" / "applications"
    icons_dir = home / ".local" / "share" / "icons" / "hicolor" / "128x128" / "apps"
    bin_dir = home / ".local" / "bin"
    
    # Create directories
    desktop_dir.mkdir(parents=True, exist_ok=True)
    icons_dir.mkdir(parents=True, exist_ok=True)
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    # Get current default handler to save it for uninstall
    current_default = get_current_default()
    if current_default:
        save_backup(current_default)
        print(f"Backed up current handler: {current_default}")
    
    # Create wrapper script in ~/.local/bin
    project_dir = Path(__file__).parent.parent
    create_wrapper_script(bin_dir, project_dir)
    print(f"Created wrapper: {bin_dir / 'appimg'}")
    
    # Create desktop entry
    desktop_file = desktop_dir / "appimg.desktop"
    desktop_content = create_desktop_entry()
    desktop_file.write_text(desktop_content)
    desktop_file.chmod(0o755)
    print(f"Created: {desktop_file}")
    
    # Copy icon (if it exists in data/)
    icon_source = project_dir / "data" / "appimg.png"
    if icon_source.exists():
        shutil.copy2(icon_source, icons_dir / "appimg.png")
        print(f"Installed icon: {icons_dir / 'appimg.png'}")
    else:
        print("Note: No icon found, using system icon")
    
    # Update desktop database
    subprocess.run(
        ["update-desktop-database", str(desktop_dir)],
        capture_output=True,
        check=False
    )
    print("Updated desktop database")
    
    # Set as default handler for AppImage files
    subprocess.run(
        ["xdg-mime", "default", "appimg.desktop", "application/vnd.appimage"],
        check=True
    )
    print("Set appimg as default handler for AppImage files")
    
    # Check if ~/.local/bin is in PATH
    if str(bin_dir) not in os.environ.get("PATH", ""):
        print(f"\n⚠️  Warning: {bin_dir} may not be in your PATH")
        print("   Add this to your ~/.bashrc or ~/.zshrc:")
        print(f'   export PATH="$HOME/.local/bin:$PATH"')
    
    print("\n✅ Installation complete!")
    print("Right-click any .appimage file → 'Open With' → 'AppImg Installer'")


def get_current_default():
    """Get the current default handler for AppImage files"""
    try:
        result = subprocess.run(
            ["xdg-mime", "query", "default", "application/vnd.appimage"],
            capture_output=True,
            text=True,
            check=False
        )
        default = result.stdout.strip()
        return default if default else None
    except Exception:
        return None


def save_backup(default_handler):
    """Save the current default handler for restore on uninstall"""
    backup_file = Path.home() / ".config" / "appimg" / "previous_handler.txt"
    backup_file.parent.mkdir(parents=True, exist_ok=True)
    backup_file.write_text(default_handler)


def create_wrapper_script(bin_dir: Path, project_dir: Path):
    """Create a wrapper script that calls uv run appimg"""
    wrapper_path = bin_dir / "appimg"
    wrapper_content = f"""#!/bin/bash
# AppImg wrapper - runs appimg via uv
exec uv run --project {project_dir} appimg "$@"
"""
    wrapper_path.write_text(wrapper_content)
    wrapper_path.chmod(0o755)


def create_desktop_entry():
    """Create the .desktop file content for appimg"""
    return """[Desktop Entry]
Name=AppImg Installer
Comment=macOS-style AppImage installer
Exec=appimg %f
Icon=appimg
Type=Application
Terminal=false
Categories=System;PackageManager;
MimeType=application/vnd.appimage;
"""


if __name__ == "__main__":
    import os
    main()
