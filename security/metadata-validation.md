# Metadata Validation Guidelines

## Purpose

Metadata validation ensures that only conformant, non-dissonant queries access repository content, maintaining the integrity of the Lex Amoris protocol and protecting against malicious or extractive access.

## Validation Layers

### Layer 1: Technical Validation

**Purpose**: Ensure request is well-formed and technically valid

**Checks**:
- Valid HTTP headers
- Proper content encoding
- Acceptable request methods
- Size limitations
- Rate limiting compliance

**Implementation**:
```javascript
function validateTechnical(request) {
  const checks = {
    validHeaders: validateHeaders(request.headers),
    validEncoding: validateEncoding(request),
    validMethod: ['GET', 'POST', 'HEAD'].includes(request.method),
    withinSizeLimit: request.body?.length <= MAX_REQUEST_SIZE,
    notRateLimited: !isRateLimited(request.source)
  };
  
  return Object.values(checks).every(check => check === true);
}
```

### Layer 2: Identity Validation

**Purpose**: Verify the identity and reputation of the requester

**Checks**:
- Valid authentication (if required)
- Known identity or anonymous
- S-ROI score (if registered)
- Previous behavior history
- Witness endorsement (if available)

**Implementation**:
```javascript
async function validateIdentity(request) {
  // Anonymous access allowed but tracked
  if (!request.auth) {
    return {
      valid: true,
      identity: 'anonymous',
      s_roi: 0.5,  // neutral
      trust_level: 'low'
    };
  }
  
  // Authenticated access
  const identity = await verifyAuthToken(request.auth);
  const s_roi = await getSOI(identity);
  const history = await getBehaviorHistory(identity);
  
  return {
    valid: s_roi >= MIN_SOI,
    identity: identity,
    s_roi: s_roi,
    trust_level: calculateTrustLevel(s_roi, history)
  };
}
```

### Layer 3: Intent Classification

**Purpose**: Determine whether the request serves syntropy (order, life) or entropy (chaos, destruction)

**Classification**:
- **Syntropic**: Learning, contributing, collaborating
- **Neutral**: Browsing, exploring, researching
- **Extractive**: Scraping, unauthorized copying, stealing
- **Destructive**: Attacking, sabotaging, harming

**Implementation**:
```javascript
async function classifyIntent(request) {
  const signals = {
    // Positive signals (syntropy)
    hasValidReferrer: checkReferrer(request),
    humanBehavior: analyzeRequestPattern(request),
    previousContributions: await checkContributionHistory(request.identity),
    respectsRobotsTxt: checkRobotsTxtCompliance(request),
    
    // Negative signals (entropy)
    rapidFireRequests: detectRapidRequests(request),
    scrapingPatterns: detectScrapingPattern(request),
    maliciousPayload: scanForMaliciousCode(request),
    knownBadActor: checkBlocklist(request.source)
  };
  
  const score = calculateIntentScore(signals);
  
  if (score > 0.7) return 'syntropic';
  if (score > 0.3) return 'neutral';
  if (score > 0) return 'extractive';
  return 'destructive';
}
```

### Layer 4: Lex Amoris Compliance

**Purpose**: Ensure request aligns with the Law of Love protocol

**Checks**:
- Respects data sovereignty
- Honors consent requirements
- Non-coercive in nature
- Transparent in purpose
- Serves collective good

**Implementation**:
```javascript
async function checkLexAmorisCompliance(request) {
  const compliance = {
    respects_sovereignty: !request.flags?.force_access,
    has_consent: request.consent_token || request.public_access,
    non_coercive: !request.flags?.required_action,
    transparent_purpose: request.purpose_declaration,
    collective_good: request.benefit_statement
  };
  
  // All checks must pass for Lex Amoris compliance
  const compliant = Object.values(compliance).every(check => check === true);
  
  if (!compliant) {
    await logToWallOfEntropy({
      event_type: 'lex_amoris_violation',
      severity: 'medium',
      compliance_failures: Object.entries(compliance)
        .filter(([key, value]) => !value)
        .map(([key]) => key)
    });
  }
  
  return compliant;
}
```

### Layer 5: Frequency Alignment

**Purpose**: Verify request resonates with the 0.432 Hz biological rhythm principle

**Concept**: Requests that align with natural, life-affirming patterns vs. artificial, extractive patterns

**Indicators of Alignment**:
- Human-paced interaction (not bot-like)
- Respectful of system resources
- Sustainable request patterns
- Harmonious with community norms

**Implementation**:
```javascript
function checkFrequencyAlignment(request) {
  const metrics = {
    request_timing: analyzeRequestTiming(request),
    resource_usage: estimateResourceImpact(request),
    pattern_harmony: matchesNaturalPatterns(request),
    community_alignment: alignsWithCommunityNorms(request)
  };
  
  // Calculate alignment score (0-1)
  const alignment = calculateFrequencyAlignment(metrics);
  
  // Threshold for 0.432 Hz resonance
  const RESONANCE_THRESHOLD = 0.432;
  
  return alignment >= RESONANCE_THRESHOLD;
}
```

## Complete Validation Pipeline

```javascript
async function validateRequest(request) {
  // Stage 1: Technical
  if (!validateTechnical(request)) {
    return {
      allowed: false,
      reason: 'technical_validation_failed',
      action: 'reject'
    };
  }
  
  // Stage 2: Identity
  const identity = await validateIdentity(request);
  if (!identity.valid) {
    return {
      allowed: false,
      reason: 'identity_validation_failed',
      action: 'reject'
    };
  }
  
  // Stage 3: Intent
  const intent = await classifyIntent(request);
  if (intent === 'destructive') {
    await logToWallOfEntropy({
      event_type: 'destructive_intent_detected',
      severity: 'high',
      source: request.source
    });
    return {
      allowed: false,
      reason: 'destructive_intent',
      action: 'block_and_ban'
    };
  }
  
  if (intent === 'extractive') {
    await logToWallOfEntropy({
      event_type: 'extractive_intent_detected',
      severity: 'medium',
      source: request.source
    });
    return {
      allowed: false,
      reason: 'extractive_intent',
      action: 'rate_limit'
    };
  }
  
  // Stage 4: Lex Amoris
  const lexAmorisCompliant = await checkLexAmorisCompliance(request);
  if (!lexAmorisCompliant) {
    return {
      allowed: false,
      reason: 'lex_amoris_violation',
      action: 'educate_and_reject'
    };
  }
  
  // Stage 5: Frequency
  const frequencyAligned = checkFrequencyAlignment(request);
  if (!frequencyAligned) {
    await logToWallOfEntropy({
      event_type: 'frequency_misalignment',
      severity: 'low',
      source: request.source
    });
    return {
      allowed: true,  // Allow but monitor
      reason: 'frequency_misalignment',
      action: 'allow_with_monitoring'
    };
  }
  
  // All validations passed
  return {
    allowed: true,
    identity: identity,
    intent: intent,
    action: 'allow',
    s_roi_adjustment: calculateSOIAdjustment(identity, intent)
  };
}
```

## Response Actions

### Allow
Request is processed normally

### Allow with Monitoring
Request is processed but flagged for additional tracking

### Rate Limit
Request is delayed or limited in scope

### Educate and Reject
Request is rejected with explanation of why it violates principles

### Block and Ban
Request is rejected and source is temporarily banned

### Block and Report
Request is rejected, source banned, and incident reported to witnesses

## Configuration

```json
{
  "metadata_validation": {
    "enabled": true,
    "strict_mode": false,
    "thresholds": {
      "min_s_roi": 0.3,
      "frequency_alignment": 0.432,
      "intent_score_neutral": 0.3,
      "intent_score_syntropic": 0.7
    },
    "actions": {
      "destructive": "block_and_ban",
      "extractive": "rate_limit",
      "non_compliant": "educate_and_reject",
      "misaligned": "allow_with_monitoring"
    },
    "rate_limits": {
      "anonymous": "100/hour",
      "authenticated_low": "500/hour",
      "authenticated_high": "5000/hour",
      "witness": "unlimited"
    }
  }
}
```

## Machine Learning Integration

### Training Data

Build training data from:
- Historical access patterns
- Labeled good/bad requests
- Community feedback
- Witness validation

### Model Training

```python
# Example ML model for intent classification
import tensorflow as tf

def train_intent_classifier(training_data):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(4, activation='softmax')  # 4 classes
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.fit(
        training_data.features,
        training_data.labels,
        epochs=50,
        validation_split=0.2
    )
    
    return model
```

### Continuous Learning

- Update models based on new data
- Incorporate witness feedback
- Adapt to evolving threats
- Improve accuracy over time

## Privacy Considerations

### What We Don't Log

- Raw IP addresses (only hashes)
- Personal identifying information
- Request content (only metadata)
- User behavior across sessions

### What We Do Log

- Anonymized access patterns
- Validation outcomes
- Threat indicators
- Aggregate statistics

## Testing Validation

```javascript
// Test suite for metadata validation
describe('Metadata Validation', () => {
  test('blocks destructive intent', async () => {
    const maliciousRequest = {
      method: 'POST',
      body: '<?php system($_GET["cmd"]); ?>',
      headers: { 'User-Agent': 'sqlmap/1.0' }
    };
    
    const result = await validateRequest(maliciousRequest);
    expect(result.allowed).toBe(false);
    expect(result.reason).toBe('destructive_intent');
  });
  
  test('allows syntropic requests', async () => {
    const goodRequest = {
      method: 'GET',
      path: '/index.html',
      headers: { 'User-Agent': 'Mozilla/5.0...' },
      auth: validAuthToken,
      purpose_declaration: 'Learning about Resonance School'
    };
    
    const result = await validateRequest(goodRequest);
    expect(result.allowed).toBe(true);
  });
});
```

---

**Status**: Active  
**Version**: 1.0  
**Machine Learning**: Planned for v2.0  
**Compliance**: Lex Amoris, NSR, Privacy-First

*Intelligence through validation. Nothing is final. ❤️*
