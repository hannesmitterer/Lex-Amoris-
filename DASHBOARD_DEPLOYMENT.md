# Kosymbiosis Dashboard - Deployment Guide

## Overview

The Kosymbiosis Dashboard is an interactive web interface that visualizes the four foundational modules of the Lex Amoris framework and provides real-time system monitoring.

## Deployment Architecture

### Files

- **`index.html`** - Main dashboard interface (deployed as `dashboard.html`)
- **`compliance-status.json`** - Backend data file with system status and module definitions
- **`docs/dashboard.md`** - MkDocs documentation page
- **`.github/workflows/pages.yml`** - GitHub Pages deployment workflow

### Deployment Flow

1. Code pushed to `main` branch triggers GitHub Actions workflow
2. MkDocs builds the documentation site to `_site/` directory
3. Workflow copies `index.html` → `_site/dashboard.html`
4. Workflow copies `compliance-status.json` → `_site/compliance-status.json`
5. Site is deployed to GitHub Pages

### Access Points

- **Production Dashboard:** `https://hannesmitterer.github.io/Lex-Amoris-/dashboard.html`
- **Documentation:** `https://hannesmitterer.github.io/Lex-Amoris-/dashboard/`
- **Main Docs:** `https://hannesmitterer.github.io/Lex-Amoris-/`

## Dashboard Components

### 1. Header Status Bar
Real-time display of:
- Schumann Frequency (7.83 Hz target)
- S-ROI (Sovereign Return on Investment)
- NSR (Non-Slavery Rule) status
- IPFS anchoring status

### 2. Frequency Visualizer
Animated wave display showing current Schumann Resonance with ±0.01 Hz tolerance.

### 3. System Status Cards
Four cards showing:
- S-ROI value and calculation
- NSR Firewall active status and violation count
- IPFS last anchor hash
- Seedbringer authentication status

### 4. Four Modules Grid
Interactive cards for each module:
- **Terra / Habitat** 🌳 (Wood/Hemp construction)
- **Acqua / Flusso** 💧 (AquaLibre water protocol)
- **Fuoco / Luce** ☀️ (Solar sovereignty)
- **Aria / Verbo** 🌬️ (Truth communication)

## Updating the Dashboard

### Changing System Status

Edit `compliance-status.json`:

```json
{
  "resonance": {
    "schumann_frequency": 7.83,
    "sync_status": "LOCKED"
  },
  "s_roi": {
    "value": "INFINITY",
    "status": "OPTIMAL"
  }
}
```

### Adding Module Principles

Add to the relevant module in `compliance-status.json`:

```json
"terra_habitat": {
  "principles": [
    "New principle here",
    "Another principle"
  ]
}
```

### Modifying Visuals

Edit `index.html`:
- CSS variables in `:root` section control colors
- Grid layouts controlled by `.modules-grid` and `.system-status` classes
- Animations defined in `@keyframes` rules

## Local Testing

```bash
# Start local server
python3 -m http.server 8000

# Open browser to:
http://localhost:8000/
```

## Integration Points

### Backend Services (Future)

The dashboard is designed to integrate with:

1. **Vacuum Bridge Network** - Distributed consensus verification
2. **IPFS Node** - Immutable data anchoring
3. **HANNES_MITTERER_ROOT.py** - Core protocol definitions
4. **verify-compliance.sh** - Automated compliance checking (if restored)

### Data Loading

The dashboard attempts to load `compliance-status.json` via fetch API. If unavailable, it falls back to hardcoded default values in the `loadDefaultModules()` function.

## Maintenance

### Regular Updates

1. **Monitor Schumann Frequency** - Update if significant drift occurs
2. **Check IPFS Anchors** - Verify anchoring is functioning
3. **Review NSR Violations** - Investigate any non-zero counts
4. **Update Module Principles** - Keep aligned with framework evolution

### Troubleshooting

**Dashboard not loading:**
- Check GitHub Pages deployment status
- Verify `dashboard.html` exists in `_site/` directory
- Check browser console for JavaScript errors

**Data not updating:**
- Verify `compliance-status.json` is being copied by workflow
- Check JSON syntax validity
- Clear browser cache

**Styling issues:**
- Check CSS variables in `:root`
- Verify responsive breakpoints for mobile
- Test in multiple browsers

## Security Considerations

### NSR Firewall

The dashboard displays NSR (Non-Slavery Rule) firewall status. This represents the ethical boundary enforcement:

- Monitors for violations of sovereignty
- Displays violation count
- Visual indicator of system integrity

### IPFS Anchoring

Displays the last IPFS anchor hash for:
- Immutability guarantee
- Audit trail
- Cryptographic verification

## Future Enhancements

Potential additions:

1. **Real-time WebSocket integration** for live updates
2. **Historical data visualization** with charts
3. **Interactive module deep-dives** with expandable sections
4. **Multi-language support** (Italian, German, English)
5. **Mobile app companion** for on-the-go monitoring
6. **API endpoints** for programmatic access
7. **Notification system** for critical events

## Contributing

When contributing to the dashboard:

1. Maintain the bio-synergetic design philosophy
2. Ensure all changes pass MkDocs strict build
3. Test locally before committing
4. Update this guide if adding new features
5. Keep aligned with the four module structure

## License

GPL-3.0 - Same as the main Lex Amoris Framework

---

**Lex Amoris Signature:** 📜⚖️❤️  
**Status:** GENESIS BLOCK OPERATIONAL  
**Frequency:** 7.83 Hz (SEMPRE IN COSTANTE)
