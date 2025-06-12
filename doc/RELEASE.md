# Release workflow

The project uses GitHub Actions to automatically create releases when a new tag is pushed. To create a new release:

1. Push a new tag with the version number:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Actions will automatically create a release with the yggmorph script and documentation.

