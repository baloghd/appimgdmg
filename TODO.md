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


## File/Package Support
- [ ] FEATURE: handle .dkpg / .rpm files
- [ ] FEATURE: add support for installing .flatpak files
- [ ] FEATURE: make the app file opener for .appimage files

## Packaging & Distribution
- [ ] IMPROVEMENT: package up as dpkg
- [ ] IMPROVEMENT: add support for more package managers (e.g. apt, yum)

## Quality & Testing
- [ ] IMPROVEMENT: add test suite
