# yggmorph

A command-line tool for managing Maven settings.xml profiles written in Rust.

## Requirements
- Rust toolchain with Cargo


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

2. Build the project using Cargo:
   ```bash
   cd yggmorph
   cargo build --release
   ```

3. Copy the resulting binary to a directory in your `PATH`:
   ```bash
   cp target/release/yggmorph ~/.local/bin/
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
