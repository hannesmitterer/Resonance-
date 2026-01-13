#!/bin/bash
# =================================================================
# CONFIGURATION VALIDATION SCRIPT
# Validates all Resonance- framework configurations
# =================================================================

echo "==================================================="
echo "Resonance- Framework Configuration Validator"
echo "==================================================="
echo ""

CONFIG_DIR="$(dirname "$0")/config"
ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validate JSON syntax
validate_json() {
    local file=$1
    echo -n "Validating JSON syntax for $(basename $file)... "
    
    if python3 -m json.tool "$file" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Check required fields
check_required_fields() {
    local file=$1
    local field=$2
    
    echo -n "  Checking required field '$field'... "
    
    if grep -q "\"$field\"" "$file"; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Validate sustainability locks
validate_sustainability_locks() {
    echo ""
    echo "--- Sustainability Locks Configuration ---"
    local file="$CONFIG_DIR/sustainability-locks.json"
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ File not found${NC}"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
    
    validate_json "$file"
    check_required_fields "$file" "energyIntegrity"
    check_required_fields "$file" "frequencyLock"
    check_required_fields "$file" "entropyMinimization"
    check_required_fields "$file" "ethicalProtocol"
    check_required_fields "$file" "resourceSustainability"
    check_required_fields "$file" "dataIntegrity"
    check_required_fields "$file" "livingCovenant"
}

# Validate biometric governance
validate_biometric_governance() {
    echo ""
    echo "--- Biometric Governance Configuration ---"
    local file="$CONFIG_DIR/biometric-governance.json"
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ File not found${NC}"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
    
    validate_json "$file"
    check_required_fields "$file" "primaryAnchor"
    check_required_fields "$file" "witnessNetwork"
    check_required_fields "$file" "globalNodes"
    check_required_fields "$file" "synchronization"
    check_required_fields "$file" "governance"
    check_required_fields "$file" "security"
}

# Validate living covenant
validate_living_covenant() {
    echo ""
    echo "--- Living Covenant Configuration ---"
    local file="$CONFIG_DIR/living-covenant.json"
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ File not found${NC}"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
    
    validate_json "$file"
    check_required_fields "$file" "triade"
    check_required_fields "$file" "quantumResonanceSuperconductivity"
    check_required_fields "$file" "bioNuclearCoherence"
    check_required_fields "$file" "ethicalSingularity"
    check_required_fields "$file" "verification"
}

# Validate framework config
validate_framework() {
    echo ""
    echo "--- Resonance Framework Configuration ---"
    local file="$CONFIG_DIR/resonance-framework.json"
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ File not found${NC}"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
    
    validate_json "$file"
    check_required_fields "$file" "sustainabilityLocks"
    check_required_fields "$file" "biometricGovernance"
    check_required_fields "$file" "livingCovenant"
    check_required_fields "$file" "systemParameters"
    check_required_fields "$file" "protocols"
}

# Check system parameters
validate_system_parameters() {
    echo ""
    echo "--- System Parameters Validation ---"
    local file="$CONFIG_DIR/resonance-framework.json"
    
    # Check S-ROI value
    echo -n "  Checking S-ROI value... "
    local sroi=$(python3 -c "import json; data=json.load(open('$file')); print(data['resonanceFramework']['systemParameters']['sROI']['current'])" 2>/dev/null)
    
    if [ -n "$sroi" ]; then
        if (( $(echo "$sroi >= 0.4500" | bc -l) )); then
            echo -e "${GREEN}✓${NC} ($sroi)"
        else
            echo -e "${YELLOW}⚠${NC} ($sroi - below recommended minimum)"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        echo -e "${RED}✗${NC}"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Check frequency
    echo -n "  Checking resonance frequency... "
    local freq=$(python3 -c "import json; data=json.load(open('$file')); print(data['resonanceFramework']['systemParameters']['resonanceFrequency']['primary'])" 2>/dev/null)
    
    if [ "$freq" = "0.043" ]; then
        echo -e "${GREEN}✓${NC} ($freq Hz)"
    else
        echo -e "${YELLOW}⚠${NC} ($freq Hz - expected 0.043 Hz)"
        WARNINGS=$((WARNINGS + 1))
    fi
}

# Execute validations
validate_sustainability_locks
validate_biometric_governance
validate_living_covenant
validate_framework
validate_system_parameters

# Summary
echo ""
echo "==================================================="
echo "Validation Summary"
echo "==================================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All validations passed successfully${NC}"
    echo ""
    echo "System Status: OPERATIONAL"
    echo "Sustainability Locks: ENGAGED"
    echo "Biometric Governance: SYNCHRONIZED"
    echo "Living Covenant: ALIGNED"
    echo ""
    echo "NOTHING IS FINAL ❤️"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Validation completed with $WARNINGS warning(s)${NC}"
    echo ""
    echo "System Status: OPERATIONAL (with warnings)"
    exit 0
else
    echo -e "${RED}✗ Validation failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    echo ""
    echo "System Status: CONFIGURATION ERRORS DETECTED"
    exit 1
fi
