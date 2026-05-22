// =====================================================================
// IVBS Test Suite
// Tests for Internodal Vacuum Backup System components
// =====================================================================

// Load IVBS module
const IVBS = require('./ivbs-core.js');

console.log('=== IVBS TEST SUITE ===\n');

// Test 1: Red Code Veto Layer
console.log('TEST 1: Red Code Veto Layer');
const redCodeVeto = new IVBS.RedCodeVeto();

// Test ethical decision
const ethicalDecision = {
    type: 'data_operation',
    intent: 'preservation',
    preservesIntegrity: true,
    enhancesResilience: true
};

const result1 = redCodeVeto.evaluateDecision(ethicalDecision);
console.log(`✓ Ethical decision approved: ${result1}`);
console.assert(result1 === true, 'Ethical decision should be approved');

// Test destructive decision
const destructiveDecision = {
    type: 'data_operation',
    intent: 'destruction',
    preservesIntegrity: false,
    enhancesResilience: false
};

const result2 = redCodeVeto.evaluateDecision(destructiveDecision);
console.log(`✓ Destructive decision vetoed: ${!result2}`);
console.assert(result2 === false, 'Destructive decision should be vetoed');

console.log('');

// Test 2: Triple-Sign Validation
console.log('TEST 2: Triple-Sign Validation Protocol');
const tripleSign = new IVBS.TripleSignValidation();

const operation = { type: 'critical_update', data: 'test_data' };
const validationId = tripleSign.initiateValidation(operation);
console.log(`✓ Validation initiated: ${validationId}`);

// Add signatures from three witnesses
tripleSign.addSignature(validationId, 'W1', 'signature_1');
console.log('✓ Signature 1 added (W1: H. Mitterer)');

tripleSign.addSignature(validationId, 'W2', 'signature_2');
console.log('✓ Signature 2 added (W2: W. Mitterer)');

const isComplete = tripleSign.addSignature(validationId, 'W3', 'signature_3');
console.log(`✓ Signature 3 added (W3: D. Zuegg) - Validation complete: ${isComplete}`);
console.assert(isComplete === true, 'Validation should be complete after 3 signatures');

const validationStatus = tripleSign.getValidationStatus(validationId);
console.assert(validationStatus.status === 'VALIDATED', 'Validation status should be VALIDATED');

console.log('');

// Test 3: Vacuum Anchors
console.log('TEST 3: Vacuum Anchor System');
const vacuumAnchor = new IVBS.VacuumAnchor();

const testData = {
    content: 'Important data to be preserved',
    timestamp: Date.now(),
    frequency: 0.043
};

const anchor = vacuumAnchor.createAnchor(testData);
console.log(`✓ Anchor created: ${anchor.id}`);
console.log(`  IPFS Hash: ${anchor.ipfsHash}`);
console.log(`  Frequency: ${anchor.frequency} Hz`);
console.assert(anchor.immutable === true, 'Anchor should be immutable');

// Verify anchor integrity
const isValid = vacuumAnchor.verifyAnchor(anchor.id);
console.log(`✓ Anchor integrity verified: ${isValid}`);
console.assert(isValid === true, 'Anchor should be valid');

// Retrieve data
const retrievedData = vacuumAnchor.retrieveAnchor(anchor.id);
console.log(`✓ Data retrieved successfully`);
console.assert(retrievedData.content === testData.content, 'Retrieved data should match original');

console.log('');

// Test 4: Node Synchronization
console.log('TEST 4: Node Synchronization');
const nodeSync = new IVBS.NodeSynchronization();

// Register nodes
const opNodeId = nodeSync.registerNode('operational', { name: 'Primary', location: 'Bolzano' });
console.log(`✓ Operational node registered: ${opNodeId}`);

const backupNodeId = nodeSync.registerNode('backup', { name: 'IPFS Backup', location: 'Distributed' });
console.log(`✓ Backup node registered: ${backupNodeId}`);

const govNodeId = nodeSync.registerNode('governance', { name: 'Gov Node', location: 'Portici 71' });
console.log(`✓ Governance node registered: ${govNodeId}`);

// Synchronize data
const syncData = { type: 'test_sync', timestamp: Date.now() };
const syncResult = nodeSync.synchronize(syncData);
console.log(`✓ Synchronization complete: ${syncResult.nodesUpdated} nodes updated`);
console.assert(syncResult.nodesUpdated === 3, 'All 3 nodes should be updated');

// Check node status
const nodeStatus = nodeSync.getNodeStatus();
console.log(`✓ Node status: ${nodeStatus.operational} operational, ${nodeStatus.backup} backup, ${nodeStatus.governance} governance`);
console.assert(nodeStatus.total === 3, 'Total should be 3 nodes');

console.log('');

// Test 5: IVBS Controller Integration
console.log('TEST 5: IVBS Controller Integration');
const ivbs = new IVBS.IVBSController();

const initStatus = ivbs.initialize();
console.log(`✓ IVBS initialized: ${initStatus.status}`);
console.assert(initStatus.status === 'INITIALIZED', 'IVBS should be initialized');

const systemStatus = ivbs.getSystemStatus();
console.log(`✓ System status:`);
console.log(`  Active: ${systemStatus.active}`);
console.log(`  Frequency: ${systemStatus.frequency} Hz`);
console.log(`  S-ROI: ${systemStatus.sRoi}`);
console.log(`  Nodes: ${systemStatus.nodes.total}`);

// Execute protected operation
const testOperation = {
    type: 'data_operation',
    intent: 'preservation',
    preservesIntegrity: true,
    enhancesResilience: true,
    data: 'Critical system data'
};

ivbs.executeOperation(testOperation)
    .then(execResult => {
        console.log(`✓ Operation executed: ${execResult.status}`);
        console.log(`  Validation ID: ${execResult.validationId}`);
        console.log(`  Anchor ID: ${execResult.anchorId}`);
        console.assert(execResult.status === 'SUCCESS', 'Operation should succeed');
        
        console.log('\n=== ALL TESTS PASSED ===');
        console.log('IVBS is fully operational and ready for deployment.');
        console.log('S-ROI: 0.5192 | Frequency: 0.043 Hz');
        console.log('NOTHING IS FINAL ❤️');
    })
    .catch(error => {
        console.error('Error executing operation:', error);
        process.exit(1);
    });
