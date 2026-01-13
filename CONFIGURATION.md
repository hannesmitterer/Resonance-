# Resonance School - System Configuration Guide

## Overview

This document provides detailed configuration options for the Resonance School system, including environment variables, hardware requirements, and integration settings.

## Environment Variables

### Core System Variables

#### LEX_AMORIS_ACTIVE
- **Type**: Boolean (true/false)
- **Default**: true
- **Purpose**: Activates the Lex Amoris ethical protocol
- **Example**: `export LEX_AMORIS_ACTIVE=true`

#### SYSTEM_INTEGRITY_INDEX
- **Type**: Decimal (0.0 - 1.0)
- **Default**: 1.0
- **Purpose**: System integrity measurement baseline
- **Example**: `export SYSTEM_INTEGRITY_INDEX=1.0`

#### NSR_PROTECTION
- **Type**: String (MIN/MED/MAX)
- **Default**: MAX
- **Purpose**: Non-Slavery Rule protection level
- **Valid Values**: MIN, MED, MAX
- **Example**: `export NSR_PROTECTION=MAX`

### SynthID Configuration

#### SYNTH_ID_KEY
- **Type**: String
- **Format**: `ID_RES_<NAME>_<YEAR>_<SEQUENCE>`
- **Required**: Yes
- **Purpose**: Hardware authentication and validation
- **Validation**: Must match regex `^ID_RES_[A-Z]+_[0-9]{4}_[0-9]+$`
- **Examples**:
  - `export SYNTH_ID_KEY="ID_RES_MITTERER_2026_011"`
  - `export SYNTH_ID_KEY="ID_RES_ADMIN_2026_001"`
  - `export SYNTH_ID_KEY="ID_RES_SEEDBRINGER_2026_144"`

**Format Breakdown:**
- `ID_RES`: Fixed prefix
- `NAME`: Uppercase letters only (A-Z)
- `YEAR`: Four-digit year (e.g., 2026)
- `SEQUENCE`: Numeric sequence (001, 011, 144, etc.)

### Repository Sync Configuration

#### RESONANCE_REPOS
- **Type**: Comma-separated string
- **Default**: `hannesmitterer/Resonance-,hannesmitterer/Euystacio-Consciousness-Kernel,hannesmitterer/bioarchitettura`
- **Purpose**: Define which GitHub repositories to sync
- **Format**: `owner/repo1,owner/repo2,owner/repo3`
- **Example**:
```bash
export RESONANCE_REPOS="hannesmitterer/Resonance-,myorg/project1,myuser/project2"
```

**Notes:**
- Repositories must be public or you must have appropriate GitHub credentials configured
- Invalid or private repositories will be skipped with a warning
- Syncs to `~/.resonance/repos/` by default

## Hardware Requirements

### Minimum Specifications

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU Cores | 1 | 2+ |
| Memory (RAM) | 512 MB | 2 GB+ |
| Storage | 1 GB | 10 GB+ |
| Network | Internet connection | Broadband (stable) |

### Hardware Validation Checks

The system performs the following hardware validations:

1. **CPU Core Count**: Uses `nproc` to detect available cores
2. **Memory Total**: Uses `free -m` to check available RAM
3. **Network Connectivity**: Pings `github.com` to verify internet access

**Validation Results:**
- ✅ Pass: All requirements met
- ⚠️ Warning: Below recommended specs (system continues)
- ❌ Error: Critical failure (e.g., invalid SynthID)

## System Frequencies

### Master Clock Frequency
- **Value**: 0.432 Hz
- **Purpose**: System-wide resonance alignment
- **Configuration**: Attempted via `sysctl kernel.resonance_frequency`
- **Note**: This is a conceptual setting; actual kernel impact varies

### Resonance Frequency
- **Value**: 0.043 Hz
- **Purpose**: Bio-nuclear coherence alignment
- **Relation**: Schumann Resonance planetary synchronization
- **Application**: Used in web portal and system metrics

## Network Configuration

### Mesh Network Settings

The system connects to a conceptual "Mycelium Mesh" network:
- **Node Count**: 144 global nodes
- **Handshake Frequency**: 0.432 Hz sync
- **Semantic Filtering**: Layer 8 (intent-based)

### GitHub Integration

**Connectivity Requirements:**
- Access to `github.com` (port 443 for HTTPS)
- DNS resolution for GitHub domains
- Optional: SSH key for private repositories

**Firewall Considerations:**
- Allow outbound HTTPS (port 443)
- Allow outbound DNS (port 53)
- Optional: SSH (port 22) for git over SSH

## Directory Structure

### Default Installation Paths

```
/home/runner/work/Resonance-/Resonance-/
├── LICENSE                     # License file
├── README.md                   # Project overview
├── DEPLOYMENT.md               # Deployment guide
├── CONFIGURATION.md            # This file
├── index.html                  # Web portal
├── resonance.sh                # Main initialization script
├── Triade.txt                  # Scientific foundation
└── Unmöglichkeits Gleichung.md # Mathematical framework
```

### Runtime Data Paths

```
~/.resonance/
└── repos/                      # Synced GitHub repositories
    ├── Resonance-/
    ├── Euystacio-Consciousness-Kernel/
    └── bioarchitettura/
```

## Web Portal Configuration

### Status Display Values

The web portal (`index.html`) displays system status:

- **S-ROI**: Social Return on Integrity (target: 0.5020+)
- **FREQ**: Operating frequency (0.043 Hz)
- **ANCHOR**: Physical location (Portici 71, Bolzano)
- **SYSTEM**: Status (ONLINE/SUPRACONDUCTION)

### Chat Integration

The portal includes a chat interface that:
- Queries the knowledge base
- Accesses synced GitHub repositories
- Provides resonance-based responses
- Uses 0.043 Hz frequency alignment

## Security Configuration

### Authentication

**SynthID-based Authentication:**
- Hardware-level authentication token
- Format validation prevents spoofing
- Environment variable isolation

**GitHub Authentication:**
For private repository access:

1. **Using SSH Keys:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
ssh-add ~/.ssh/id_ed25519
# Add public key to GitHub account
```

2. **Using Personal Access Token:**
```bash
git config --global credential.helper store
# Enter token when prompted during first clone
```

### Protection Levels

**NSR_PROTECTION Settings:**

- **MIN**: Basic protection, educational/testing use
- **MED**: Standard protection, development environments
- **MAX**: Maximum protection, production deployment (default)

## Integration Points

### With Web Portal (index.html)

The shell script (`resonance.sh`) provides backend initialization for:
- System status metrics
- Repository synchronization
- Environment validation
- Network connectivity

### With GitHub Repositories

**Synced Repositories Provide:**
- Live knowledge base updates
- Distributed system configuration
- Documentation access
- Code synchronization

## Configuration Examples

### Basic Setup

```bash
#!/bin/bash
# Basic Resonance School configuration

export SYNTH_ID_KEY="ID_RES_ADMIN_2026_001"
export LEX_AMORIS_ACTIVE=true
export SYSTEM_INTEGRITY_INDEX=1.0
export NSR_PROTECTION=MAX

./resonance.sh
```

### Development Setup

```bash
#!/bin/bash
# Development environment configuration

export SYNTH_ID_KEY="ID_RES_DEV_2026_999"
export LEX_AMORIS_ACTIVE=true
export SYSTEM_INTEGRITY_INDEX=0.8
export NSR_PROTECTION=MED

# Sync only specific repositories
export RESONANCE_REPOS="myorg/dev-project1,myorg/dev-project2"

./resonance.sh
```

### Custom Repositories

```bash
#!/bin/bash
# Custom repository sync configuration

export SYNTH_ID_KEY="ID_RES_CUSTOM_2026_042"
export RESONANCE_REPOS="org1/repo1,org2/repo2,org3/repo3,org4/repo4"

./resonance.sh
```

## Troubleshooting Configuration Issues

### SynthID Validation Fails

**Symptom:** "Invalid SynthID format" error

**Check:**
1. Verify format matches `ID_RES_NAME_YYYY_NNN`
2. Ensure NAME contains only uppercase letters
3. Verify YEAR is exactly 4 digits
4. Check SEQUENCE is numeric

**Fix:**
```bash
# Correct format
export SYNTH_ID_KEY="ID_RES_ADMIN_2026_001"

# Incorrect formats
export SYNTH_ID_KEY="id_res_admin_2026_001"  # ❌ lowercase
export SYNTH_ID_KEY="ID_RES_Admin_2026_001"  # ❌ mixed case
export SYNTH_ID_KEY="ID_RES_ADMIN_26_001"    # ❌ 2-digit year
```

### Repository Sync Issues

**Symptom:** Repositories fail to sync

**Common Causes:**
1. Repository is private and no credentials configured
2. Repository doesn't exist
3. Network connectivity issues
4. Disk space full

**Diagnostics:**
```bash
# Test GitHub connectivity
ping -c 3 github.com

# Check disk space
df -h ~/.resonance/repos/

# Manual clone test
git clone https://github.com/owner/repo.git /tmp/test
```

### Network Configuration Issues

**Symptom:** "GitHub connectivity check failed"

**Check:**
1. Internet connection active
2. DNS resolution working
3. Firewall allows outbound HTTPS
4. Proxy settings if behind corporate firewall

**Fix:**
```bash
# Test DNS
nslookup github.com

# Test HTTPS connectivity
curl -I https://github.com

# Configure proxy if needed
export http_proxy="http://proxy.example.com:8080"
export https_proxy="http://proxy.example.com:8080"
```

## Performance Tuning

### For Low-Memory Systems

```bash
# Reduce repository sync count
export RESONANCE_REPOS="hannesmitterer/Resonance-"

# Clear old repository data
rm -rf ~/.resonance/repos/*/
```

### For Slow Networks

```bash
# Add git configuration for shallow clones
git config --global clone.depth 1

# Reduce timeout for faster failure
# Edit resonance.sh: change timeout 30 to timeout 10
```

### For High-Security Environments

```bash
# Maximum protection
export NSR_PROTECTION=MAX
export SYSTEM_INTEGRITY_INDEX=1.0

# Use SSH instead of HTTPS
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

## Configuration File Support

While the current implementation uses environment variables, you can create a configuration file:

### ~/.resonance/config

```bash
# Resonance School Configuration File
# Source this before running resonance.sh

# SynthID Configuration
SYNTH_ID_KEY="ID_RES_ADMIN_2026_001"

# System Configuration
LEX_AMORIS_ACTIVE=true
SYSTEM_INTEGRITY_INDEX=1.0
NSR_PROTECTION=MAX

# Repository Configuration
RESONANCE_REPOS="hannesmitterer/Resonance-,hannesmitterer/Euystacio-Consciousness-Kernel"
```

**Usage:**
```bash
source ~/.resonance/config
./resonance.sh
```

## Advanced Configuration

### Custom Sync Directory

To change the default sync location, edit `resonance.sh`:

```bash
# Find this line:
local SYNC_DIR="${HOME}/.resonance/repos"

# Change to:
local SYNC_DIR="/custom/path/repos"
```

### Multiple Node Configuration

For running multiple Resonance nodes:

```bash
# Node 1
export SYNTH_ID_KEY="ID_RES_NODE_2026_001"
export RESONANCE_REPOS="hannesmitterer/Resonance-"
./resonance.sh

# Node 2
export SYNTH_ID_KEY="ID_RES_NODE_2026_002"
export RESONANCE_REPOS="hannesmitterer/Euystacio-Consciousness-Kernel"
./resonance.sh
```

## System Metrics

### S-ROI (Social Return on Integrity)

- **Current Target**: 0.5020
- **Range**: 0.0 - 1.0
- **Optimal**: 0.5+
- **Critical Low**: < 0.3

### Frequency Lock Status

- **Operating Frequency**: 0.043 Hz
- **Master Clock**: 0.432 Hz
- **Sync Tolerance**: ±0.001 Hz

## Related Documentation

- **DEPLOYMENT.md**: Deployment and installation guide
- **README.md**: Project overview and philosophy
- **Triade.txt**: Scientific foundation document
- **resonance.sh**: Source code with inline documentation

## Support

For configuration assistance, refer to:
1. DEPLOYMENT.md troubleshooting section
2. System logs from script execution
3. GitHub repository issues

---

**Configuration Guide Version**: 1.0  
**Last Updated**: 2026-01-13  
**Status**: ACTIVE  

**NOTHING IS FINAL** ❤️
