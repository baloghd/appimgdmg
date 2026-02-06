#!/usr/bin/env python3
"""Uninstall appimg and restore previous default handler"""

import sys
from pathlib import Path
import subprocess

def main():
    """Remove appimg desktop entry and restore previous handler"""
    
    home = Path.home()
    desktop_dir = home / ".local" / "share" / "applications"
    icons_dir = home / ".local" / "share" / "icons" / "hicolor" / "128x128" / "apps"
    
    # Remove desktop file
    desktop_file = desktop_dir / "appimg.desktop"
    if desktop_file.exists():
        desktop_file.unlink()
        print(f"Removed: {desktop_file}")
    else:
        print("appimg.desktop not found (already uninstalled?)")
    
    # Remove icon
    icon_file = icons_dir / "appimg.png"
    if icon_file.exists():
        icon_file.unlink()
        print(f"Removed: {icon_file}")
    
    # Restore previous default handler
    backup_file = home / ".config" / "appimg" / "previous_handler.txt"
    if backup_file.exists():
        previous_handler = backup_file.read_text().strip()
        if previous_handler:
            try:
                subprocess.run(
                    ["xdg-mime", "default", previous_handler, "application/vnd.appimage"],
                    check=True
                )
                print(f"Restored previous handler: {previous_handler}")
            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to restore previous handler: {e}")
        backup_file.unlink()
    else:
        # Fallback to gear lever
        try:
            subprocess.run(
                ["xdg-mime", "default", "it.mijorus.gearlever.desktop", "application/vnd.appimage"],
                check=True
            )
            print("Restored default handler to: it.mijorus.gearlever.desktop")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to restore gear lever: {e}")
    
    # Update desktop database
    subprocess.run(
        ["update-desktop-database", str(desktop_dir)],
        capture_output=True,
        check=False
    )
    print("Updated desktop database")
    
    print("\n✅ Uninstallation complete!")


if __name__ == "__main__":
    main()
