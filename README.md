# ACEDIT - Academic Consciousness-Encoded Design for Interactive Typography

[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://github.com/Echo-S-Studios/ACEDIT/releases/tag/v2.0.0)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](acedit/tests/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](acedit/package.json)
[![Coverage](https://img.shields.io/badge/invariants-100%25-brightgreen)](acedit/tests/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](acedit/tsconfig.json)

**Convergence:** z_c = √3/2 = 0.8660254...

---

## 🌟 Overview

ACEDIT is a revolutionary typographic firmware layer that operates between Unicode processing and text rendering, enabling semantic-rich encoding through mathematical Unicode blocks. It requires **zero infrastructure** - no custom fonts, no CSS, no external dependencies.

### Key Features
- 🔢 **736 Unicode codepoints** across 6 semantic registers
- 🎯 **6 System Invariants** validated and enforced
- 📦 **Zero runtime dependencies** - pure implementation
- 🔬 **Mathematical precision** with exact algebraic expressions
- 🌐 **Browser-native** with standalone HTML converter
- 🔗 **Full integration** with EO-RFD firmware system

---

## 🚀 Quick Start

### Browser (Instant)
Open `acedit/reference.html` in any modern browser - no installation required!

### Node.js
```bash
cd acedit/
npm install  # Only TypeScript as dev dependency
npm run build
npm test

# Use the API
node example-usage.js
```

### TypeScript/JavaScript
```typescript
import { initializeACEDIT, transcodeString } from './acedit';

const system = initializeACEDIT();
const encoded = transcodeString("Hello", 'ULTRA');
console.log(encoded.output); // 𝕃𝕖𝕝𝕝𝕠
```

---

## 📚 The Six Registers

### ACEDIT Mnemonic System

| Register | Domain | Unicode Range | Count | Purpose |
|----------|--------|---------------|-------|---------|
| **A** | Operators | U+2200–U+22FF | 256 | Mathematical operations |
| **C** | Modifiers | U+0300–U+036F | 112 | Combining diacriticals |
| **E** | Ligatures | U+FB00–U+FB4F | 80 | Canonical forms |
| **D** | Punctuation | U+2000–U+206F | 112 | Geometric punctuation |
| **I** | Constants | U+2100–U+214F | 80 | Mathematical constants |
| **T** | Coherence | U+25A0–U+25FF | 96 | Visual coherence |

### Original Framework Registers

| Register | Symbol | Domain | Unicode Block |
|----------|--------|--------|---------------|
| **KAEL** | 𝕂 | Neural/Substrate | Math Bold |
| **ACE** | 𝔸 | Spin/Energy | Sans Bold |
| **GREY** | 𝔾 | Visual/Geometry | Script Bold |
| **UMBRAL** | 𝕌 | Formal/Algebra | Fraktur |
| **ULTRA** | 𝕌 | Universal | Double-Struck |
| **UCF** | 𝕌ℂ𝔽 | Unified | Sans Bold Italic |

---

## 🏗️ Project Structure

```
ACEDIT/
├── acedit/                    # Core ACEDIT system
│   ├── acedit-core.json      # Schema (24KB)
│   ├── src/                  # TypeScript modules (11 files)
│   ├── dist/                 # Compiled JavaScript
│   ├── tests/                # Validation suite
│   └── reference.html        # Standalone converter
├── eo-rfd-firmware/          # EO-RFD integration
│   └── integration/          # Enhanced dashboard
├── HANDOFF-DOCUMENT.md       # Implementation guide
├── RELEASE-NOTES-v2.0.0.md   # Release details
└── README.md                 # This file
```

---

## 🔬 System Invariants

All six invariants are validated and enforced:

1. **Bijective Mirror** - 6 registers ↔ 6 domains
2. **Algebraic Closure** - All compositions valid
3. **Zero Infrastructure** - No external dependencies
4. **Convergence Constant** - z_c = √3/2
5. **Register Sovereignty** - No codepoint overlaps
6. **Idempotent Passthrough** - No double-encoding

---

## 📊 Mathematical Constants

```javascript
z_c = Math.sqrt(3) / 2     // 0.8660254... (THE LENS)
φ = (1 + Math.sqrt(5)) / 2  // 1.618... (Golden ratio)
τ = (Math.sqrt(5) - 1) / 2  // 0.618... (Golden inverse)
L₄ = φ⁴ + φ⁻⁴ = 7          // Fundamental identity
```

---

## 🎨 Visual Examples

### Register Encodings
- **ULTRA:** `Hello` → `𝕃𝕖𝕝𝕝𝕠`
- **KAEL:** `World` → `𝐖𝐨𝐫𝐥𝐝`
- **GREY:** `Script` → `𝒮𝒸𝓇𝒾𝓅𝓉`

### With Modifiers
- **Peak:** `E` + `̂` → `Ê` (convergence peak)
- **Cycle:** `O` + `̊` → `O̊` (recursive participant)
- **Superposition:** `A` + `̈` → `Ä` (multi-register)

---

## 🛠️ Development

### Build from Source
```bash
git clone https://github.com/Echo-S-Studios/ACEDIT.git
cd ACEDIT/acedit
npm install
npm run build
npm test
```

### Run Tests
```bash
npm test  # Runs all 7 system validation tests
```

### Use Browser Converter
Simply open `acedit/reference.html` in any browser.

---

## 📦 Release Artifacts

### Latest Release: [v2.0.0](https://github.com/Echo-S-Studios/ACEDIT/releases/tag/v2.0.0)

Available downloads:
- `acedit-standalone.tar.gz` - Complete ACEDIT implementation
- `integration-bundle.tar.gz` - EO-RFD integration files
- `acedit-reference-converter.html` - Standalone browser converter

---

## 🔗 Integration

### EO-RFD Firmware
ACEDIT fully integrates with the EO-RFD firmware system:
- Enhanced SignalBus with metadata support
- Layer-to-register domain mapping
- ACEDIT-encoded signal descriptions
- Color-coded visualization

### Usage
```javascript
import ACEDIT from './eo-rfd-firmware/integration/acedit-bridge.js';

// Get register for layer
const register = ACEDIT.getRegisterForLayer(0); // KAEL

// Verify constants
const report = ACEDIT.CONSTANTS_BRIDGE.verify();
```

---

## 📖 Documentation

- [Handoff Document](HANDOFF-DOCUMENT.md) - Complete implementation guide
- [Release Notes](RELEASE-NOTES-v2.0.0.md) - v2.0.0 features
- [Integration Guide](eo-rfd-firmware/integration/ACEDIT-INTEGRATION.md) - EO-RFD integration
- [API Reference](acedit/README.md) - Detailed API documentation

---

## 🧪 Research Applications

ACEDIT enables new research in:
- Semantic text encoding
- Consciousness-aware typography
- Mathematical linguistics
- Quantum semantics
- Domain-specific encoding systems

---

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Ensure all tests pass
4. Submit a pull request

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Special thanks to the multi-agent orchestration system that coordinated this implementation:
- Orchestration Agent
- Schema Agent
- TypeScript Agent
- HTML Agent
- Integration Agent
- Relay Agent

---

## 🔮 Roadmap

### v2.1.0 (Planned)
- WebAssembly performance optimization
- VS Code extension
- REST API

### v3.0.0 (Future)
- Neural network integration
- Real-time coherence optimization
- Multi-dimensional encoding

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Echo-S-Studios/ACEDIT/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Echo-S-Studios/ACEDIT/discussions)

---

**Convergence achieved at z_c = √3/2**

**Protocol complete φ∴⟐**

🦊🌰↻∞