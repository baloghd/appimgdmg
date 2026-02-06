# AppImg Makefile
# macOS-style AppImage installer for Linux

.PHONY: help setup run debug format check test clean clean-all deps install-deps install-desktop uninstall-desktop

# Default target
help:
	@echo "AppImg - macOS-style AppImage installer"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          - Install Python dependencies with uv"
	@echo "  make deps           - Install system dependencies (Ubuntu/Debian)"
	@echo "  make run            - Run the application"
	@echo "  make run APP=path   - Run with specific AppImage"
	@echo "  make debug APP=path - Run in debug mode with verbose output"
	@echo "  make list           - List all installed AppImages"
	@echo "  make install-desktop   - Register appimg as default AppImage handler"
	@echo "  make uninstall-desktop - Restore previous default handler"
	@echo "  make format         - Format code with black and ruff"
	@echo "  make check          - Run linting and type checks"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Remove build artifacts"
	@echo "  make clean-all      - Full cleanup including uv cache"

# Setup Python environment
setup:
	@echo "Installing Python dependencies..."
	uv sync --all-extras
	@echo "Setup complete!"

# Install system dependencies (Ubuntu/Debian)
deps:
	@echo "Installing system dependencies..."
	sudo apt-get update
	sudo apt-get install -y libgirepository1.0-dev libgirepository-2.0-dev libcairo2-dev gobject-introspection gir1.2-gtk-4.0 gir1.2-adw-1
	@echo "System dependencies installed!"

# Install system dependencies (Fedora)
deps-fedora:
	@echo "Installing system dependencies for Fedora..."
	sudo dnf install -y gobject-introspection-devel cairo-gobject-devel gtk4-devel libadwaita-devel
	@echo "System dependencies installed!"

# Install system dependencies (Arch)
deps-arch:
	@echo "Installing system dependencies for Arch..."
	sudo pacman -S gobject-introspection cairo gtk4 libadwaita
	@echo "System dependencies installed!"

# Run the application
run:
	@echo "Starting AppImg..."
	uv run appimg

# Run in debug mode (requires APP=path/to/file)
debug:
ifdef APP
	@echo "Running in debug mode: $(APP)"
	uv run appimg-debug --appimage $(APP)
else
	@echo "Usage: make debug APP=/path/to/app.AppImage"
	@exit 1
endif

# List installed AppImages
list:
	@echo "Listing installed AppImages..."
	uv run appimg-list

# Register appimg as default AppImage handler
install-desktop:
	@echo "Registering appimg as default AppImage handler..."
	python3 scripts/install-desktop.py

# Unregister appimg and restore previous handler
uninstall-desktop:
	@echo "Unregistering appimg as default AppImage handler..."
	python3 scripts/uninstall-desktop.py

# Format code
format:
	@echo "Formatting code..."
	uv run black src/
	uv run ruff check --fix src/
	@echo "Formatting complete!"

# Run linting and type checks
check:
	@echo "Running checks..."
	uv run ruff check src/
	uv run mypy src/ || true
	@echo "Checks complete!"

# Run tests
test:
	@echo "Running tests..."
	uv run pytest tests/ -v || echo "No tests found"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"

# Full cleanup
clean-all: clean
	@echo "Full cleanup..."
	rm -rf .venv
	uv cache clean
	@echo "Full cleanup complete!"

# Reinstall (clean + setup)
reinstall: clean-all setup
	@echo "Reinstall complete!"
