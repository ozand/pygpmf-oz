# PyPI Upload Instructions for pygpmf_oz v0.3.0

## Option 1: Web Upload (Recommended - Easiest)

1. Go to **https://pypi.org** and log in
2. Navigate to **Your projects** or go directly to **https://pypi.org/project/pygpmf-oz/**
3. Click **Upload files** button
4. Select both files from `dist/`:
   - `pygpmf_oz-0.3.0-py3-none-any.whl`
   - `pygpmf_oz-0.3.0.tar.gz`
5. Upload and wait for processing
6. Verify at: https://pypi.org/project/pygpmf-oz/0.3.0/

---

## Option 2: Command Line (If you have API token)

```powershell
# Set token (one-time setup)
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-YourTokenHere"

# Upload
cd T:\Code\python\pygpmf
python -m twine upload dist/*
```

To get a token:
1. Go to **https://pypi.org/manage/account/token/**
2. Create new token (scope: "Entire account" for first upload, or project-specific)
3. Copy token and use above

---

## Verification After Upload

```powershell
# Wait 2-3 minutes, then test install
pip install --upgrade pygpmf-oz

# Verify version
python -c "import gpmf; print(gpmf.__version__)"
# Should output: 0.3.0

# Test imports
python -c "from gpmf import gps, gyro, parse; print('✓ All modules imported')"
```

---

## Artifacts Ready

- ✅ Wheel: `dist/pygpmf_oz-0.3.0-py3-none-any.whl`
- ✅ Source: `dist/pygpmf_oz-0.3.0.tar.gz`
- ✅ Verified: Both pass `twine check`
- ✅ Tests: 134/134 passing, 79.77% coverage
- ✅ Docs: INTEGRATION_GUIDE.md ready for external teams

---

## What's in This Release

- **Hero 11-13 GPS9** (10Hz) with auto-detection
- **Gyroscope/Accelerometer** module (GYRO/ACCL)
- **UTF-8 FourCC fix** (resolves 0.2.1 decode errors)
- **134 tests**, 79.77% coverage
- **Full backward compatibility** with GPS5

---

Proceed with upload when ready!
