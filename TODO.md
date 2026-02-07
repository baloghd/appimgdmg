## UI/UX Features
- [x] FEATURE: add settings dialog
- [x] FEATURE: add MacOS-style 'sound' after installation
- [x] FEATURE: make sound notification optional / configurable
- [x] FEATURE: "make executable" should be an option on UI, autoset to true - but user can disable it if they want
- [x] FEATURE: add system notification for successful installation / failure
- [ ] FEATURE: add support for multiple languages
- [ ] FEATURE: add progress bar for installation process
- [x] FEATURE: add option to choose installation directory
- [x] BUG: if user tries to install an appimage that is already installed, it should prompt them to either overwrite the existing one or cancel the installation, not fail with an error
- [x] BUG: application gets launched immediately after installation, even if the user has not chosen to do so (and we get the application is not responding error)
  - Fixed: `_is_electron_app()` was running the AppImage with subprocess to detect Electron. Now checks for chrome-sandbox file in extracted AppImage instead.
- [ ] BUG: we make the file executable even if we don't install it -> only make executable if user chooses to install

## File/Package Support
- [ ] FEATURE: handle .dkpg / .rpm files
- [ ] FEATURE: add support for installing .flatpak files
- [x] FEATURE: make the app file opener for .appimage files
  - Created data/badgerdrop.mime.xml MIME type definition (handles both application/vnd.appimage and application/x-appimage)
  - Created data/badgerdrop.desktop with MimeType association
  - postinst script registers badgerdrop as default handler
  - prerm script unregisters on uninstall
  - NOTE: Nautilus (GNOME Files) runs executable files directly instead of opening with default app. This is standard behavior.
    - Web-downloaded AppImages (not executable): Double-click opens with badgerdrop ✓
    - Already executable AppImages: Double-click runs directly (expected - use right-click → "Open With badgerdrop" if needed)

## Packaging & Distribution
- [x] IMPROVEMENT: package up as dpkg
  - Created debian/ packaging directory
  - Built badgerdrop_0.1.0-1_all.deb (44KB)
  - Includes entry points: badgerdrop, badgerdrop-debug, badgerdrop-list, badgerdrop-sound
  - Makefile targets: build-dpkg, install-package, reinstall-package, clean-dpkg
- [x] IMPROVEMENT: package up as rpm
  - Built badgerdrop-0.1.0-1.noarch.rpm (59KB) using fpm
  - Makefile targets: build-rpm, build-all, clean-rpm
  - Package includes all entry points and proper dependencies
- [ ] IMPROVEMENT: add support for more package managers (e.g. apt, yum)
- [ ] IMPROVEMENT: create a PPA for easy installation on Ubuntu-based systems
- [ ] IMPROVEMENT: determine Python version compatibility matrix

## Quality & Testing
- [ ] IMPROVEMENT: add test suite
