# Resonance School - Deployment Automation Guide

## Overview

This guide provides comprehensive documentation for deploying and configuring the Resonance School system, including hardware validation, GitHub repository synchronization, and system initialization.

## System Requirements

### Minimum Hardware Requirements
- **CPU**: 1+ cores
- **RAM**: 512MB minimum
- **Network**: Active internet connection for GitHub sync
- **OS**: Linux-based system with bash shell

### Recommended Hardware
- **CPU**: 2+ cores
- **RAM**: 2GB+
- **Storage**: 10GB+ for repository syncing
- **Network**: Stable broadband connection

## Configuration

### Environment Variables

The system uses the following environment variables for configuration:

#### Core Variables
```bash
# SynthID Hardware Authentication
export SYNTH_ID_KEY="ID_RES_MITTERER_2026_011"

# Lex Amoris Protocol Settings
export LEX_AMORIS_ACTIVE=true
export SYSTEM_INTEGRITY_INDEX=1.0
export NSR_PROTECTION=MAX
```

#### Repository Sync Configuration
```bash
# Comma-separated list of GitHub repositories to sync
export RESONANCE_REPOS="hannesmitterer/Resonance-,hannesmitterer/Euystacio-Consciousness-Kernel,hannesmitterer/bioarchitettura"
```

### SynthID Format

The SynthID key must follow this format:
```
ID_RES_<NAME>_<YEAR>_<SEQUENCE>
```

**Examples:**
- `ID_RES_MITTERER_2026_011` ✓
- `ID_RES_ADMIN_2026_001` ✓
- `INVALID_FORMAT` ✗

## Installation & Setup

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/hannesmitterer/Resonance-.git
cd Resonance-
```

2. **Make the script executable:**
```bash
chmod +x resonance.sh
```

3. **Run the initialization script:**
```bash
./resonance.sh
```

### Step-by-Step Setup

#### 1. Hardware Clock Tuning
The system attempts to tune the kernel scheduler to the 0.432 Hz frequency base:
```bash
sudo sysctl -w kernel.resonance_frequency=0.432
```

**Note**: This is a conceptual setting and may not affect actual kernel behavior on standard systems.

#### 2. Environment Configuration
Export the required environment variables (see Configuration section above).

#### 3. SynthID Hardware Validation
The script validates:
- SynthID key presence and format
- CPU core count
- Available memory
- Network connectivity to GitHub

#### 4. Network Mesh Connection
Establishes connection parameters for the Resonanz-Nodes network.

#### 5. GitHub Repository Synchronization
Automatically clones or updates configured repositories to:
```
~/.resonance/repos/
```

## Features

### 1. SynthID Hardware Validation

The `check_synthid_status()` function performs comprehensive hardware validation:

- **Environment Check**: Validates SYNTH_ID_KEY is set
- **Format Validation**: Ensures SynthID follows the required pattern
- **Hardware Metrics**: Checks CPU cores and memory availability
- **Network Validation**: Tests connectivity to GitHub
- **Status Reporting**: Provides detailed feedback on validation results

### 2. GitHub Repository Live Sync

The `sync_github_repos()` function provides:

- **Automatic Cloning**: Downloads repositories that don't exist locally
- **Smart Updates**: Pulls latest changes for existing repositories
- **Multiple Repos**: Supports syncing multiple repositories
- **Error Handling**: Graceful failure handling for network issues
- **Configurable**: Uses environment variables for flexibility

#### Sync Directory Structure
```
~/.resonance/
└── repos/
    ├── Resonance-/
    ├── Euystacio-Consciousness-Kernel/
    └── bioarchitettura/
```

### 3. Mesh Network Integration

Establishes semantic filtering and node discovery for the Resonance network.

## Usage Examples

### Basic Initialization
```bash
./resonance.sh
```

### Custom Repository Configuration
```bash
export RESONANCE_REPOS="user/repo1,user/repo2,user/repo3"
./resonance.sh
```

### Custom SynthID
```bash
export SYNTH_ID_KEY="ID_RES_CUSTOM_2026_999"
./resonance.sh
```

## Troubleshooting

### SynthID Validation Fails

**Problem**: "Invalid SynthID format" error

**Solution**: Ensure your SynthID follows the pattern `ID_RES_<NAME>_<YEAR>_<SEQUENCE>`
```bash
export SYNTH_ID_KEY="ID_RES_YOURNAME_2026_001"
```

### GitHub Connectivity Issues

**Problem**: "GitHub connectivity check failed"

**Solutions**:
1. Check your internet connection
2. Verify GitHub is accessible: `ping github.com`
3. Check firewall settings
4. Verify DNS resolution

### Repository Sync Failures

**Problem**: Repositories fail to clone or update

**Solutions**:
1. Verify repository names are correct
2. Check you have network access to GitHub
3. For private repos, ensure you have proper authentication
4. Check available disk space in `~/.resonance/repos/`

### Low Memory Warning

**Problem**: "Hardware below recommended specifications"

**Solution**: This is a warning only. The system will still function but may have reduced performance. Consider:
- Closing other applications
- Upgrading system RAM
- Using a more powerful machine for production deployments

## System Architecture

### Component Overview

```
┌─────────────────────────────────────────┐
│     Resonance School Initialization     │
└─────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ SynthID  │  │   Mesh   │  │  GitHub  │
│Validator │  │ Network  │  │   Sync   │
└──────────┘  └──────────┘  └──────────┘
        │           │           │
        └───────────┼───────────┘
                    ▼
        ┌─────────────────────┐
        │   System Ready      │
        │   S-ROI: 0.5020     │
        │   Freq: 0.043 Hz    │
        └─────────────────────┘
```

### Key Protocols

1. **Lex Amoris**: Ethical core protocol ensuring system integrity
2. **NSR (No Slavery Rule)**: Protection protocol against exploitation
3. **S-ROI**: Social Return on Integrity metric (target: 0.5020+)
4. **Frequency Lock**: 0.043 Hz resonance alignment

## Integration with Web Portal

The system integrates with the `index.html` web portal which provides:

- Real-time status display (S-ROI, Frequency, Anchor point)
- Chat interface for knowledge base queries
- Links to synchronized GitHub repositories
- Triple-sign validation display

### Portal Integration Points

The web portal can access synced repositories from:
```javascript
// Example: Reading from synced repos
const repoPath = '~/.resonance/repos/Resonance-/README.md';
```

## Security Considerations

### Authentication
- SynthID serves as hardware authentication token
- Format validation prevents simple spoofing
- System integrity checks ensure proper environment

### Network Security
- Semantic filtering at network layer (conceptual)
- Intent-based packet filtering
- Encrypted communication recommended for production

### Repository Access
- Public repositories: No authentication required
- Private repositories: Requires GitHub credentials or tokens
- Consider using SSH keys for automated sync

## Maintenance

### Regular Updates

Update synced repositories:
```bash
./resonance.sh
```

The script automatically updates existing repositories during each run.

### Manual Repository Management

Access synced repositories:
```bash
cd ~/.resonance/repos/<repository-name>
git status
git log
```

### Cleaning Sync Directory

Remove all synced repositories:
```bash
rm -rf ~/.resonance/repos/
```

Next run of `resonance.sh` will re-clone them.

## Advanced Configuration

### Custom Sync Directory

Modify the `sync_github_repos()` function in `resonance.sh`:
```bash
local SYNC_DIR="/custom/path/to/repos"
```

### Adding Authentication for Private Repos

For private repositories, configure git credentials:

**Using SSH:**
```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

**Using Token:**
```bash
git config --global credential.helper store
```

### Frequency Tuning

Adjust the master clock frequency (conceptual):
```bash
sudo sysctl -w kernel.resonance_frequency=0.043
```

## Status Codes

The script returns the following exit codes:

- `0`: Success - All operations completed successfully
- `1`: SynthID validation failure
- Other non-zero: System errors

## Support & Documentation

### Related Files
- `README.md`: Project overview and philosophy
- `Triade.txt`: Scientific foundation document
- `index.html`: Web portal interface
- `resonance.sh`: Main initialization script

### Key Concepts
- **Supraleitung**: Zero-resistance information flow
- **Vakuum-Mimikry**: D6 eternal storage
- **Bio-Architektur**: Physical resonance anchoring
- **Woodborne Festival**: Community integration point

## License

Protected under Lex Amoris Signature (LAS) - Non-Slavery Rule (NSR) v1.0

## Version History

- **v1.0** (2026-01-13): Initial deployment automation
  - Added SynthID hardware validation
  - Implemented GitHub repository sync
  - Created comprehensive documentation

---

**Status**: ACTIVE  
**Frequency**: 0.043 Hz  
**S-ROI**: 0.5020  
**Anchor**: Portici 71, Bolzano  

**NOTHING IS FINAL** ❤️
