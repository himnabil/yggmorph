#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}yggmorph installer${NC}"
echo "This script will download and install the latest version of yggmorph."

# Determine installation directory
if [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
    echo -e "Installing to ${GREEN}${INSTALL_DIR}${NC} (system-wide)"
else
    INSTALL_DIR="$HOME/.local/bin"
    echo -e "Installing to ${GREEN}${INSTALL_DIR}${NC} (user-specific)"
    
    # Create directory if it doesn't exist
    if [ ! -d "$INSTALL_DIR" ]; then
        echo "Creating $INSTALL_DIR directory..."
        mkdir -p "$INSTALL_DIR"
    fi
    
    # Check if the directory is in PATH
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        echo -e "${YELLOW}Warning: $INSTALL_DIR is not in your PATH.${NC}"
        echo "You may need to add the following line to your shell profile:"
        echo -e "${YELLOW}export PATH=\"\$PATH:$INSTALL_DIR\"${NC}"
    fi
fi

# Get the latest release URL
echo "Fetching latest release information..."
LATEST_RELEASE_URL=$(curl -s https://api.github.com/repos/himnabil/yggmorph/releases/latest | grep "browser_download_url.*yggmorph\"" | cut -d '"' -f 4)

if [ -z "$LATEST_RELEASE_URL" ]; then
    echo -e "${RED}Error: Could not find the latest release.${NC}"
    exit 1
fi

# Download the latest release
echo "Downloading yggmorph..."
TEMP_FILE=$(mktemp)
curl -s -L -o "$TEMP_FILE" "$LATEST_RELEASE_URL"

# Install the executable
echo "Installing yggmorph to $INSTALL_DIR..."
mv "$TEMP_FILE" "$INSTALL_DIR/yggmorph"
chmod +x "$INSTALL_DIR/yggmorph"

echo -e "${GREEN}Installation complete!${NC}"
echo "You can now run yggmorph from the command line."
echo "Try running: yggmorph --help"