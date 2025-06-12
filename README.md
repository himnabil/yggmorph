# yggmorph

A command-line tool for managing Maven settings.xml profiles.

## Releases

The project uses GitHub Actions to automatically create releases when a new tag is pushed. To create a new release:

1. Push a new tag with the version number:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Actions will automatically create a release with the yggmorph script and documentation.

## Installation

### Requirements
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Python package installer and resolver

### Installation Steps

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
