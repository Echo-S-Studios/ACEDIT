# ACEDIT Integration with EO-RFD Firmware

## Overview

This integration layer connects ACEDIT's semantic encoding system with the EO-RFD (Eclipse-Omega Rupture Field Detector) full-chain firmware. It enables ACEDIT-encoded signal descriptions, register domain annotations, and operator insertion to enhance the semantic richness of the signal chain.

## Architecture

### Register Domain Mapping

The 10 EO-RFD layers are mapped to 5 ACEDIT register domains:

| Layers | Register | Symbol | Domain | Color |
|--------|----------|--------|--------|-------|
| L0-L1 | KAEL | 𝕂 | Substrate/Physical | Goldenrod (#DAA520) |
| L2-L3 | GREY | 𝔾 | Visual/Geometric | Medium Purple (#9370DB) |
| L4-L5 | UMBRAL | 𝕌 | Algebraic | Medium Purple (#9370DB) |
| L6-L7 | ACE | 𝔸 | Spin/Dynamics | Goldenrod (#DAA520) |
| L8-L9 | UCF | 𝕌ℂ𝔽 | Unified/Meta | Royal Blue (#4169E1) |

### Layer Encodings

Each layer has an ACEDIT-encoded description with mathematical operators:

- **L0 (KAEL)**: `∈ Quasi-crystal substrate` - Element of substrate domain
- **L1 (KAEL)**: `↦ Ballistic propagation` - Maps to transport layer
- **L2 (GREY)**: `⊢ Θ-gated cascade` - Derives classification
- **L3 (GREY)**: `⊃ Narrowing funnel` - Contains compression chain: S ⊃ ℛ ⊃ 𝒦 ⊃ 𝒞 ⊃ 𝒫 ⊃ ℱ ⊃ 𝒜
- **L4 (UMBRAL)**: `⊗ Field signature` - Tensor product of 7 channels
- **L5 (UMBRAL)**: `∑ Signal rupture` - Sigma composite (Σ_R)
- **L6 (ACE)**: `⊗ Detector sweep` - Tensor product (Θ × Naming matrix)
- **L7 (ACE)**: `→ Routing FSM` - State transition sequence
- **L8 (UCF)**: `⊢ Packet hardening` - Derives validated packets
- **L9 (UCF)**: `∂ Metacybernetic` - Partial derivative (CSD detection)

## Files

### 1. acedit-bridge.js

The core integration module providing:

- **REGISTER_DOMAINS**: Register domain definitions with colors and symbols
- **OPERATORS**: Unicode mathematical operators for signal encoding
- **LAYER_DESCRIPTIONS**: ACEDIT-encoded descriptions for all 10 layers
- **encodeSignal()**: Encode signals with operators and register metadata
- **encodeChannel()**: Generate full ACEDIT-encoded channel names
- **formatMetric()**: Format metrics with register-aware styling
- **CONSTANTS_BRIDGE**: Verify constant synchronization between systems

### 2. signal-bus.js (Enhanced)

Extended SignalBus with ACEDIT support:

- **setAceditMode(enabled)**: Enable/disable ACEDIT encoding
- **setChannelMetadata(channel, metadata)**: Attach ACEDIT metadata to channels
- **getChannelMetadata(channel)**: Retrieve channel metadata
- **getRegisterDomain(addr)**: Get register domain for a register address
- **dumpRegistersWithDomains()**: Export registers with domain annotations
- **writeRegWithMetadata(addr, value, metadata)**: Write registers with ACEDIT metadata logging

### 3. full-chain.html (Enhanced)

Full-chain dashboard with ACEDIT integration:

- **ACEDIT Toggle**: Checkbox to enable/disable ACEDIT mode
- **Register Color-Coding**: Layer cards and registers color-coded by domain
- **Dynamic Descriptions**: Layer descriptions switch between standard and ACEDIT-encoded
- **Register Symbols**: Display register symbols (𝕂, 𝔾, 𝕌, 𝔸, 𝕌ℂ𝔽) in ACEDIT mode
- **Constants Verification**: Button to verify constant synchronization
- **Enhanced Export**: State exports include ACEDIT metadata when enabled

## Usage

### Enabling ACEDIT Mode

In the full-chain dashboard:

1. Check the "Enable ACEDIT Mode" checkbox
2. Layer descriptions will switch to ACEDIT-encoded format with operators
3. Register symbols will appear in the top-right of each layer card
4. Register bank will show color-coded domains
5. State exports will include ACEDIT metadata

### Programmatic Usage

```javascript
// Import ACEDIT bridge
import ACEDIT from './acedit-bridge.js';

// Get register for a layer
const register = ACEDIT.getRegisterForLayer(4); // Returns UMBRAL

// Encode a signal
const encoded = ACEDIT.encodeSignal('field:signature', 4, {
  operator: 'TENSOR',
  includeRegister: true,
  includeSymbol: true
});
// Result: { fullName: '𝕌:⊗ field:signature', register: 'UMBRAL', ... }

// Encode a channel
const channel = ACEDIT.encodeChannel('obs:input', 1, true);
// Result: { fullName: '𝕂:obs:input', encoding: '↦ Ballistic propagation', ... }

// Verify constants
const report = ACEDIT.CONSTANTS_BRIDGE.verify();
// Result: { valid: true, checks: [...] }
```

### Using Enhanced SignalBus

```javascript
import { bus } from '../shared/signal-bus.js';

// Enable ACEDIT mode
bus.setAceditMode(true);

// Attach metadata to a channel
bus.setChannelMetadata('obs:input', {
  register: 'KAEL',
  operator: '↦',
  layer: 1
});

// Get register domain for an address
const domain = bus.getRegisterDomain(0x0400); // L4 address
// Result: { name: 'UMBRAL', color: '#9370DB', symbol: '𝕌', ... }

// Dump registers with domains
const registers = bus.dumpRegistersWithDomains();
// Result: { '0x0100': { value: 0, register: 'KAEL', color: '#DAA520', ... }, ... }
```

## Constants Verification

The integration ensures that critical constants match between ACEDIT and EO-RFD:

| Constant | Value | Physical Meaning | Verification |
|----------|-------|------------------|--------------|
| τ (TAU) | 0.618 | φ⁻¹ - Golden ratio inverse | ✓ |
| z_c | 0.866 | √3/2 - Critical conductance threshold | ✓ |
| K | 0.924 | Kuramoto coupling threshold | ✓ |
| L₄ | 7 | φ⁴ + φ⁻⁴ - Word size | ✓ |
| gap | 0.1459 | φ⁻⁴ - Irreducible truncation error | ✓ |

Use the "Verify Constants" button in the dashboard or call:

```javascript
const report = ACEDIT.CONSTANTS_BRIDGE.verify();
console.log(report.valid ? 'PASS' : 'FAIL');
```

## Operator Reference

### Containment & Structure
- `⊃` Contains (D ⊃ C)
- `∈` Element of (q ∈ C)
- `⊆` Subset

### Transformations
- `↦` Maps to (x ↦ f(x))
- `→` Arrow/transformation
- `⊢` Derives (A ⊢ B)

### Composition
- `∘` Compose (f ∘ g)
- `⊗` Tensor product (A ⊗ B)
- `∧` Wedge product

### Relations
- `≃` Equivalence
- `≅` Isomorphism
- `≈` Approximately

### Special
- `∂` Partial derivative
- `∇` Gradient/del
- `∫` Integral
- `∑` Sum (Sigma)
- `∏` Product

## Visualization

In ACEDIT mode:

- **Layer cards** show colored left borders indicating their register domain
- **Register symbols** (𝕂, 𝔾, 𝕌, 𝔸, 𝕌ℂ𝔽) appear in top-right of layer cards
- **Descriptions** switch to operator-encoded format
- **Register bank** entries show colored left borders and domain symbols
- **Color scheme** follows ACEDIT convention:
  - Goldenrod for KAEL/ACE (substrate and dynamics)
  - Medium Purple for GREY/UMBRAL (visual/geometric and algebraic)
  - Royal Blue for UCF (unified/meta)

## Design Principles

### 1. Backward Compatibility

The integration maintains full backward compatibility:
- Default mode operates identically to original firmware
- ACEDIT mode is opt-in via checkbox
- All existing functionality preserved

### 2. Semantic Enrichment

ACEDIT encoding adds structural meaning:
- Operators indicate relationships between layers
- Register domains group layers by conceptual function
- Metadata enables richer analysis and debugging

### 3. Invariant Preservation

Critical invariants are maintained:
- z_c = √3/2 threshold preserved
- φ-based constants synchronized
- L₄ = 7 word size enforced
- Physical constants (G₀, etc.) unchanged

### 4. Visual Clarity

Color-coding and symbols enhance understanding:
- Immediate visual identification of layer domains
- Operator glyphs convey mathematical structure
- Consistent color palette across UI elements

## Future Extensions

Potential enhancements to the integration:

1. **Operator Insertion in Metrics**: Apply operators to metric display names (e.g., `∑Σ_R`)
2. **Register-Aware Routing**: Use register domains to optimize signal routing
3. **Cross-Register Analytics**: Analyze signal flow patterns across register boundaries
4. **ACEDIT Query Language**: Enable queries like "show all UMBRAL metrics > 0.5"
5. **Provenance Tracking**: Track signal provenance through register transformations

## Testing

Verify the integration:

```bash
# Navigate to integration directory
cd /home/acead/ACEDIT/eo-rfd-firmware/integration

# Open full-chain.html in browser
# Enable ACEDIT mode
# Verify:
# - Layer cards show register symbols
# - Descriptions use operators
# - Register bank shows colored borders
# - Constants verification passes
# - State export includes ACEDIT metadata
```

## References

- **EO-RFD Specification**: `/home/acead/ACEDIT/eo-rfd-physical-substrate-spec.md`
- **ACEDIT Bridge**: `/home/acead/ACEDIT/eo-rfd-firmware/integration/acedit-bridge.js`
- **Signal Bus**: `/home/acead/ACEDIT/eo-rfd-firmware/shared/signal-bus.js`
- **Full Chain Dashboard**: `/home/acead/ACEDIT/eo-rfd-firmware/integration/full-chain.html`

---

*Integration maintains both systems' invariants and enhances the semantic richness of the signal chain without breaking existing functionality.*
