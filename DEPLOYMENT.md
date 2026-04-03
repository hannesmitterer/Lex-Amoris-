# GitHub Pages Deployment Guide

## Overview

This repository is configured for automatic deployment to GitHub Pages using GitHub Actions. The deployment includes all compliance artifacts, documentation, and a web dashboard.

## Deployment Configuration

### GitHub Actions Workflow

**File**: `.github/workflows/deploy-pages.yml`

The deployment workflow:
1. **Verifies compliance** - Runs `verify-compliance.sh` to ensure all 40+ checks pass
2. **Deploys to GitHub Pages** - Uploads all files to GitHub Pages environment

### Trigger Conditions

The deployment workflow triggers on:
- Push to `main` branch
- Push to `copilot/conduct-code-review` branch
- Manual trigger via `workflow_dispatch`

## Deployed Content

### Web Dashboard
- **index.html** - Main landing page with compliance status
- Self-contained HTML with inline CSS (no external dependencies)

### Compliance Artifacts (JSON)
- `living-covenant.json` - Constitutional principles
- `ipfs-anchoring.json` - Distributed storage configuration  
- `key-trust-protocol.json` - Cryptographic trust protocol
- `trust-anchors.json` - Trust service provider registry
- `g-csi-compliance.json` - G-CSI-2026 framework
- `nsr-enforcement.json` - No Surveillance Regime enforcement

### Documentation
- `README.md` - Project overview
- `VERIFICATION.md` - Verification procedures
- `IMPLEMENTATION.md` - Implementation details
- `CONTRIBUTING.md` - Contribution guidelines
- `SECURITY.md` - Security policy
- `DEPLOYMENT.md` - This file

### Verification Script
- `verify-compliance.sh` - Automated compliance validation (40+ checks)

## GitHub Pages Settings

### Required Permissions

The workflow requires these permissions:
```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

### Repository Settings

In GitHub repository settings → Pages:
1. **Source**: GitHub Actions
2. **Branch**: Deployment via workflow (not branch-based)
3. **Environment**: `github-pages`

## Deployment Process

### Automatic Deployment

1. Push changes to `main` or `copilot/conduct-code-review` branch
2. GitHub Actions automatically:
   - Runs compliance verification
   - Deploys to GitHub Pages (if verification passes)
3. Site is live at: `https://hannesmitterer.github.io/Lex-Amoris-/`

### Manual Deployment

1. Go to Actions tab in GitHub
2. Select "Deploy to GitHub Pages" workflow
3. Click "Run workflow"
4. Select branch
5. Click "Run workflow" button

## Verification

### Pre-Deployment Checks

Before deploying, verify locally:
```bash
# Run compliance verification
./verify-compliance.sh

# Should output:
# ✓ Passed: 40
# ✗ Failed: 0
# ⚠ Warnings: 0
```

### Post-Deployment Verification

After deployment:
1. Visit the GitHub Pages URL
2. Verify the web dashboard loads correctly
3. Check that all JSON artifacts are accessible
4. Confirm compliance status shows "VERIFIED"

## Troubleshooting

### Deployment Fails

1. Check GitHub Actions logs in the "Actions" tab
2. Verify compliance verification passes locally
3. Ensure all required files are committed
4. Check repository permissions and Pages settings

### Site Not Loading

1. Verify GitHub Pages is enabled in repository settings
2. Check that `.nojekyll` file exists (prevents Jekyll processing)
3. Confirm workflow completed successfully
4. Wait a few minutes for DNS propagation

### Compliance Verification Fails

1. Run `./verify-compliance.sh` locally to see errors
2. Fix any failing checks
3. Commit and push changes
4. Deployment will retry automatically

## Files Required for Deployment

### Essential Files
- ✅ `.nojekyll` - Prevents Jekyll processing
- ✅ `index.html` - Main page
- ✅ All 6 JSON compliance artifacts
- ✅ `verify-compliance.sh` - Verification script

### Optional Files
- Documentation (MD files)
- License file
- Contributing guidelines

## Security Considerations

### Content Security
- All JSON artifacts are publicly accessible
- No sensitive data should be in the repository
- Compliance verification runs before deployment
- Deployment only proceeds if all checks pass

### Access Control
- Repository visibility: Public
- GitHub Pages visibility: Public
- No authentication required for viewing

## Deployment Status

Current deployment branch: `copilot/conduct-code-review`

To check deployment status:
```bash
# Via GitHub CLI
gh run list --workflow=deploy-pages.yml

# Via web interface
https://github.com/hannesmitterer/Lex-Amoris-/actions
```

## Support

For deployment issues:
1. Check GitHub Actions logs
2. Review this deployment guide
3. Consult GitHub Pages documentation
4. Open an issue in the repository

---

**Last Updated**: 2026-04-03  
**Deployment Type**: GitHub Actions → GitHub Pages  
**Status**: ✅ Active
