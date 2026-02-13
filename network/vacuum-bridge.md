# Vacuum-Bridge: Peer-to-Peer Network Architecture

## Overview

Vacuum-Bridge is the distributed networking layer of Internet Organica that enables sovereign, peer-to-peer data distribution and storage. It bridges the gap between centralized server architectures and true digital sovereignty.

## Philosophy

Traditional client-server models create dependencies and central points of control. Vacuum-Bridge implements a **distributed-first** architecture where:

- Data is owned by creators, not platforms
- No single point of failure or control
- Resilient to censorship and takedowns
- Operates with or without internet connectivity
- Respects privacy and sovereignty

## Core Technologies

### 1. IPFS (InterPlanetary File System)

**Purpose**: Content-addressed, distributed file storage

**Implementation**:
```javascript
// Example: Storing Resonance School data on IPFS
import IPFS from 'ipfs-core';

async function storeOnIPFS(content) {
  const ipfs = await IPFS.create({
    repo: './ipfs-repo',
    config: {
      Addresses: {
        Swarm: ['/dns4/ipfs.resonance-school.org/tcp/4001/wss']
      }
    }
  });
  
  const { cid } = await ipfs.add(content);
  await logToWallOfEntropy({
    type: 'ipfs_store',
    cid: cid.toString(),
    timestamp: Date.now()
  });
  
  return cid;
}
```

**Benefits**:
- Content addressing (CID)
- Automatic deduplication
- Distributed hosting
- Offline capability via local cache

### 2. DAT Protocol (Hypercore)

**Purpose**: Versioned, distributed data structures

**Use Cases**:
- Real-time synchronization
- Version history
- Cryptographic verification
- Collaborative editing

**Implementation**:
```javascript
// Example: Creating a distributed Resonance archive
import Hypercore from 'hypercore';
import Hyperdrive from 'hyperdrive';

async function createResonanceArchive() {
  const drive = new Hyperdrive('./resonance-archive');
  
  await drive.writeFile('/index.html', indexHtmlContent);
  await drive.writeFile('/config.json', configContent);
  
  // Share the drive key for distributed access
  const key = drive.key.toString('hex');
  console.log(`Archive key: ${key}`);
  
  return drive;
}
```

### 3. Custom P2P Layer

**Features**:
- Ethical peer discovery (no surveillance)
- Encrypted peer communication
- NAT traversal
- Mesh networking

## Architecture

### Network Topology

```
┌─────────────┐         ┌─────────────┐
│   Anchor    │◄───────►│   Peer 1    │
│  Portici 71 │         └─────────────┘
└─────────────┘               │
       │                      │
       │                      ▼
       │              ┌─────────────┐
       ├─────────────►│   Peer 2    │
       │              └─────────────┘
       │                      │
       ▼                      │
┌─────────────┐               │
│   Peer 3    │◄──────────────┘
└─────────────┘
```

### Data Flow

1. **Creation**: Content created at any node
2. **Signing**: Cryptographically signed by creator
3. **Distribution**: Propagated to connected peers
4. **Verification**: Signature verification at each hop
5. **Storage**: Stored by interested peers
6. **Retrieval**: Accessible from any hosting peer

## Implementation Guide

### Setting Up a Node

1. **Install Dependencies**
```bash
npm install ipfs-core hypercore hyperdrive
```

2. **Configure Node**
```javascript
// vacuum-bridge-config.json
{
  "node": {
    "id": "resonance-node-001",
    "anchor": "Portici 71",
    "protocols": {
      "ipfs": true,
      "hypercore": true,
      "custom_p2p": true
    },
    "discovery": {
      "bootstrap_nodes": [
        "/dns4/anchor.resonance-school.org/tcp/4001/p2p/QmAnchor..."
      ],
      "mdns": true,
      "dht": true
    }
  }
}
```

3. **Initialize Node**
```javascript
import { VacuumBridge } from './vacuum-bridge';

const node = await VacuumBridge.create({
  config: './vacuum-bridge-config.json',
  anchor: 'Portici 71',
  witnesses: ['H. Mitterer', 'W. Mitterer', 'D. Zuegg']
});

await node.start();
```

### Publishing Content

```javascript
// Publish Resonance School content
async function publishContent(content, metadata) {
  // 1. Sign content with creator's key
  const signature = await signContent(content, creatorKey);
  
  // 2. Create IPFS package
  const package = {
    content,
    metadata,
    signature,
    timestamp: Date.now(),
    protocol: 'lex-amoris-v1'
  };
  
  // 3. Store on IPFS
  const cid = await node.ipfs.add(JSON.stringify(package));
  
  // 4. Announce to peers
  await node.announce({
    type: 'content_published',
    cid: cid.toString(),
    metadata: {
      title: metadata.title,
      creator: metadata.creator
    }
  });
  
  return cid;
}
```

### Subscribing to Content

```javascript
// Subscribe to updates from the Resonance School
async function subscribeToResonance() {
  await node.subscribe('resonance-school', async (update) => {
    // Verify signature
    const valid = await verifySignature(update);
    if (!valid) {
      await logToWallOfEntropy({
        type: 'invalid_signature',
        update: update.cid
      });
      return;
    }
    
    // Check Lex Amoris compliance
    const compliant = await checkLexAmorisCompliance(update);
    if (!compliant) {
      await logToWallOfEntropy({
        type: 'non_compliant_content',
        update: update.cid
      });
      return;
    }
    
    // Process valid update
    await processUpdate(update);
  });
}
```

## Security Considerations

### 1. Peer Validation

Before connecting to a peer:
- Verify peer identity
- Check reputation (S-ROI)
- Validate compliance with NSR
- Log connection attempt

### 2. Content Verification

Before accepting content:
- Verify cryptographic signature
- Check creator's credentials
- Validate against Lex Amoris protocol
- Scan for malicious content

### 3. Privacy Protection

- No IP address logging
- Encrypted peer communication
- Anonymous peer discovery options
- Traffic obfuscation available

## Distributed Backup Strategy

### Backup Topology

1. **Primary Anchor**: Portici 71 (Always online)
2. **Witness Nodes**: 5 witness locations
3. **Community Nodes**: Voluntary hosting by community
4. **Archive Nodes**: Long-term storage nodes

### Backup Process

```javascript
async function createDistributedBackup() {
  // 1. Create snapshot of current state
  const snapshot = await createSnapshot();
  
  // 2. Encrypt with witness multi-sig
  const encrypted = await encryptWithWitnesses(snapshot);
  
  // 3. Store on multiple protocols
  const ipfsCid = await storeOnIPFS(encrypted);
  const datKey = await storeOnHypercore(encrypted);
  
  // 4. Distribute to witness nodes
  await distributeToWitnesses({
    ipfs: ipfsCid,
    dat: datKey,
    timestamp: Date.now()
  });
  
  // 5. Log backup completion
  await logToWallOfEntropy({
    type: 'backup_completed',
    ipfs: ipfsCid.toString(),
    witnesses: witnessConfirmations
  });
}
```

## Urbit Integration (Future)

### Vision

Urbit provides personal sovereign servers (planets) that can host Resonance School content independently.

### Prototype Plan

1. **Phase 1**: Study Urbit architecture
2. **Phase 2**: Create Resonance School agent (gall app)
3. **Phase 3**: Implement P2P sync between Urbit ships
4. **Phase 4**: Full migration path from web to Urbit

### Example Urbit Agent

```hoon
:: resonance-school.hoon
:: Urbit agent for Resonance School
::
|%
+$  state
  $:  %0
      frequency=@rd          :: 0.432 Hz
      s-roi=@rd              :: Social Return on Integrity
      anchor=(unit @t)       :: Physical anchor location
      content=(map @t json)  :: Stored content
  ==
--
```

## Monitoring and Metrics

### Health Metrics

- Peer count
- Data redundancy level
- Network latency
- S-ROI of connected peers
- Lex Amoris compliance rate

### Dashboard

```javascript
async function getNetworkStatus() {
  return {
    peers: node.peers.length,
    ipfs_repo_size: await node.ipfs.repo.stat(),
    uptime: node.uptime(),
    s_roi_avg: await calculateAverageSOI(),
    frequency_sync: checkFrequencySync(0.432)
  };
}
```

## Troubleshooting

### Common Issues

1. **Cannot connect to peers**
   - Check firewall settings
   - Verify bootstrap nodes
   - Enable UPnP/NAT-PMP

2. **Slow content retrieval**
   - Increase peer connections
   - Pin frequently accessed content
   - Use local IPFS gateway

3. **Verification failures**
   - Update witness public keys
   - Check system clock synchronization
   - Verify signature algorithms

## Resources

### Documentation
- [IPFS Documentation](https://docs.ipfs.io)
- [Hypercore Protocol](https://hypercore-protocol.org)
- [Urbit Documentation](https://urbit.org/docs)

### Community
- Resonance School P2P Network
- Internet Organica Developers
- Distributed Web Community

---

**Status**: Active  
**Version**: 1.0  
**Protocols**: IPFS, Hypercore, Custom P2P  
**Compliance**: NSR, Lex Amoris

*Distributed sovereignty. Nothing is final. ❤️*
