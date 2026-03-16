# MCPScan PyPI Publishing Setup

## Status (2026-03-14)
- ✅ GitHub Actions workflow `publish.yml` exists in remote repo (`kryptonomeai-cloud/mcpscan`)
- ✅ GitHub release `v0.2.0` already created (published 2026-03-14T08:56:39Z)
- ⏳ PyPI trusted publisher registration still needed (manual step)

## Steps to Complete PyPI Trusted Publisher Setup

### 1. PyPI Account
- Go to https://pypi.org/account/register/ and create an account (or log in)
- Enable 2FA (required for trusted publisher setup)

### 2. Register Trusted Publisher (Pending Publisher)

Since `mcpscan` doesn't exist on PyPI yet, use **Pending Publisher**:

1. Go to https://pypi.org/manage/account/publishing/
2. Scroll to **"Create a new pending publisher"**
3. Fill in:
   - **PyPI project name:** `mcpscan`
   - **Owner:** `kryptonomeai-cloud`
   - **Repository name:** `mcpscan`
   - **Workflow name:** `publish.yml`
   - **Environment name:** leave blank (or `release` if the workflow uses one)
4. Click **"Add"**

### 3. Trigger the Workflow

The workflow is triggered by GitHub releases. Since `v0.2.0` already exists, either:

**Option A:** Create a new release (e.g., `v0.2.1`):
```bash
gh release create v0.2.1 --repo kryptonomeai-cloud/mcpscan --title "v0.2.1" --notes "PyPI publish test"
```

**Option B:** Re-run the workflow manually (if workflow_dispatch is configured):
```bash
gh workflow run publish.yml --repo kryptonomeai-cloud/mcpscan
```

**Option C:** Delete and recreate v0.2.0:
```bash
gh release delete v0.2.0 --repo kryptonomeai-cloud/mcpscan --yes
gh release create v0.2.0 --repo kryptonomeai-cloud/mcpscan --title "v0.2.0" --notes "Initial PyPI release"
```

### 4. Verify
- Check workflow run: https://github.com/kryptonomeai-cloud/mcpscan/actions
- Check PyPI: https://pypi.org/project/mcpscan/

## Workflow Reference
The `publish.yml` workflow should:
1. Build the package (sdist + wheel)
2. Use `pypa/gh-action-pypi-publish@release/v1` to publish
3. Authenticate via OIDC (trusted publisher — no API tokens needed)

## Notes
- The v0.2.0 release was created on 2026-03-14 but the PyPI trusted publisher wasn't registered yet, so the publish step likely failed
- After registering the trusted publisher, re-trigger the workflow
- Local project at `/Users/miniclaw/.openclaw/workspace/projects/mcpscan/` only contains `dist/mcpscan-0.1.0.tar.gz`
