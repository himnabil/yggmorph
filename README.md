# yggmorph

A command-line tool for managing Maven settings.xml profiles.

## Requirements
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Python package installer and resolver


## Installation

### Automatic Installation

You can install yggmorph automatically using our installation script:

```bash
# Using curl
curl -sSL https://raw.githubusercontent.com/himnabil/yggmorph/main/install.sh | bash

# Or using wget
wget -qO- https://raw.githubusercontent.com/himnabil/yggmorph/main/install.sh | bash
```

The script will:
- Download the latest release of yggmorph
- Install it to `/usr/local/bin` (if you have write permissions) or `$HOME/.local/bin`
- Make it executable and ready to use

### Manual Installation

#### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/himnabil/yggmorph.git
   ```

2. Make the script executable:
   ```bash
   chmod +x yggmorph/yggmorph
   ```

3. Add the script to your PATH or create a symbolic link to it in a directory that's already in your PATH:
   ```bash
   # Option 1: Add to PATH
   export PATH="$PATH:/path/to/yggmorph"

   # Option 2: Create a symbolic link
   ln -s /path/to/yggmorph/yggmorph ~/.local/bin/yggmorph
   ```

## Usage

### Manage Maven settings.xml profiles:

```bash
# List available profiles
yggmorph maven list-profiles

# Save current settings.xml as a profile
yggmorph maven save -p profile_name

# Apply a saved profile
yggmorph maven apply -p profile_name

# Remove settings.xml (apply default profile)
yggmorph maven apply -p default
```
