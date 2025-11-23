# Publishing SmartKDB to PyPI

## Quick Publish

```bash
# Clean old builds
Remove-Item -Recurse -Force dist, build, *.egg-info

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

---

## Prerequisites

1. **Account on PyPI**
   - Create account at https://pypi.org
   - Get API token from Account Settings

2. **Required Tools**
   ```bash
   pip install build twine
   ```

---

## Step-by-Step Publishing

### 1. Update Version
Edit `pyproject.toml`:
```toml
version = "5.0.1"  # Increment this
```

### 2. Update Changelog
Edit `docs/CHANGELOG.md`:
```markdown
## [5.0.1] - 2024-XX-XX
### Added
- New feature X

### Fixed
- Bug Y
```

### 3. Clean & Build
```bash
# Remove old builds
Remove-Item -Recurse -Force dist, build, *.egg-info

# Build new package
python -m build
```

This creates:
- `dist/smartkdb-5.0.1.tar.gz` (source)
- `dist/smartkdb-5.0.1-py3-none-any.whl` (wheel)

### 4. Test Locally (Optional)
```bash
pip install dist/smartkdb-5.0.1-py3-none-any.whl
```

### 5. Upload to PyPI
```bash
twine upload dist/*
```

Enter credentials:
- Username: `__token__`
- Password: `pypi-your-api-token-here`

### 6. Verify
Visit: https://pypi.org/project/smartkdb/

---

## Semantic Versioning

Follow [SemVer](https://semver.org/):

- **5.0.0** → **5.0.1** : Bug fixes
- **5.0.0** → **5.1.0** : New features (backward compatible)
- **5.0.0** → **6.0.0** : Breaking changes

---

## Testing Before Publishing

### Test on Test PyPI (Recommended)
```bash
# Upload to test server
twine upload --repository testpypi dist/*

# Install from test server
pip install --index-url https://test.pypi.org/simple/ smartkdb
```

---

## Checklist Before Publishing

- [ ] Version number updated in `pyproject.toml`
- [ ] Changelog updated in `docs/CHANGELOG.md`
- [ ] All tests passing (`python -m pytest`)
- [ ] README.md is up to date
- [ ] Examples work correctly
- [ ] No sensitive data in code

---

## Common Issues

### Issue: "File already exists"
**Solution:** You can't re-upload the same version. Increment version number.

### Issue: "Invalid token"
**Solution:** Generate new token at https://pypi.org/manage/account/token/

### Issue: "Package name taken"
**Solution:** Choose different name in `pyproject.toml`

---

**Ready to publish! 🚀**
