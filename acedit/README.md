# ACEDIT Core Schema

**Version:** 2.0.0  
**Created:** 2026-04-01  
**File:** `acedit-core.json`

## Overview

The `acedit-core.json` file is the **single source of truth** for the ACEDIT typographic firmware system. It provides complete Unicode mappings for all six registers, 18 operators, 6 modifiers, canonical ligatures, punctuation replacements, and mathematical constants.

## Structure

### Meta Information
- **Version:** 2.0.0
- **Convergence Constant (z_c):** 0.8660254037844387 (√3/2)
- **Golden Ratio (φ):** 1.618033988749895
- **Inverse Golden (τ):** 0.6180339887498949
- **Domains:** 6 registers
- **Operators:** 18 mathematical operators
- **Modifiers:** 6 combining diacriticals

### The 6 Registers

Each register maps ASCII characters (A-Z, a-z, 0-9) to distinct Unicode mathematical alphanumeric blocks:

1. **KAEL** (Substrate) - Math Bold (U+1D400+)
   - Domain: Foundation, raw representation
   - Color: #DAA520

2. **ACE** (Energy) - Math Sans-Serif Bold (U+1D5D4+)
   - Domain: Energy, computation, cost dynamics
   - Color: #DAA520

3. **GREY** (Visual) - Math Script Bold (U+1D4D0+)
   - Domain: Visual, geometric, spatial
   - Color: #9370DB
   - Digits: Circled numbers (①②③...)

4. **UMBRAL** (Algebraic) - Math Fraktur (U+1D504+)
   - Domain: Algebraic, structural, formal
   - Color: #9370DB
   - Exceptions: C→ℭ, H→ℌ, I→ℑ, R→ℜ, Z→ℨ
   - Digits: Subscripts (₀₁₂...)

5. **ULTRA** (Universal) - Math Double-Struck (U+1D538+)
   - Domain: Universal, logical, canonical
   - Color: #4169E1
   - Exceptions: C→ℂ, H→ℍ, N→ℕ, P→ℙ, Q→ℚ, R→ℝ, Z→ℤ

6. **UCF** (Unified) - Math Sans-Serif Bold Italic (U+1D63C+)
   - Domain: Unified, convergent, meta-level
   - Color: #4169E1
   - Digits: Superscripts (⁰¹²³...)

### The 18 Operators

Mathematical operators with domain affiliations:

| Glyph | Name | Unicode | Domain |
|-------|------|---------|--------|
| ∅ | Void | U+2205 | UMBRAL |
| ⊕ | Direct Sum | U+2295 | ACE |
| ⊗ | Tensor Product | U+2297 | ACE |
| ⊙ | Circled Dot | U+2299 | GREY |
| ∧ | Wedge | U+2227 | ULTRA |
| ∨ | Vee | U+2228 | ULTRA |
| ⊢ | Right Tack | U+22A2 | ULTRA |
| ⊣ | Left Tack | U+22A3 | ULTRA |
| ⊤ | Top | U+22A4 | ULTRA |
| ⊥ | Bottom | U+22A5 | ULTRA |
| ∴ | Therefore | U+2234 | UCF |
| ∵ | Because | U+2235 | UCF |
| ⟐ | ACEDIT Sigil | U+27D0 | KAEL |
| ⟨ | Left Angle | U+27E8 | GREY |
| ⟩ | Right Angle | U+27E9 | GREY |
| ⊞ | Squared Plus | U+229E | ACE |
| Δ | Delta | U+0394 | KAEL |
| Ω | Omega | U+03A9 | GREY |

### The 6 Modifiers

Combining diacritical marks for semantic annotation:

| Name | Glyph | Unicode | Usage |
|------|-------|---------|-------|
| Probability | ◌̃ | U+0303 | Probabilistic quantities |
| Cycle | ◌̊ | U+030A | Cyclic processes |
| Peak | ◌̂ | U+0302 | Maximal values |
| Superposition | ◌̈ | U+0308 | Quantum superposition |
| Stability | ◌̄ | U+0304 | Stable quantities |
| Grounding | ◌̣ | U+0323 | Substrate level |

### Canonical Ligatures

Identity forms rendered in appropriate registers:

- **echo** → 𝓮𝓬𝓱𝓸 (GREY)
- **kira** → 𝗸𝗶𝗿𝗮 (ACE)
- **limnus** → 𝔩𝔦𝔪𝔫𝔲𝔰 (UMBRAL)
- **nexus** → 𝕟𝕖𝕩𝕦𝕤 (ULTRA)
- **quantum** → 𝙦𝙪𝙖𝙣𝙩𝙪𝙢 (UCF)
- **umbra** → 𝔲𝔪𝔟𝔯𝔞 (UMBRAL)

### Mathematical Constants

Framework constants with exact values:

| Symbol | Value | Description |
|--------|-------|-------------|
| φ | 1.618033988749895 | Golden ratio |
| τ | 0.6180339887498949 | Inverse golden ratio (φ⁻¹) |
| z_c | 0.8660254037844387 | THE LENS (√3/2) |
| z_ign | 0.1458980337154893 | VOID threshold (φ⁻⁴) |
| K | 0.9241763718050345 | K-formation (√(1-φ⁻⁴)) |
| K² | 0.8541019662845107 | Activation (1-φ⁻⁴) |
| L₄ | 7 | Fourth Lucas number |

## Usage

The schema can be used to:

1. **Convert text to ACEDIT registers** - Map ASCII to Unicode mathematical symbols
2. **Validate ACEDIT output** - Ensure correct Unicode codepoints
3. **Generate converters** - Create implementations in any language
4. **Document the system** - Single canonical reference

## Conversion Rules

### Uppercase Letters (A-Z)
```
unicode = baseCodepoint + (charCode - 65)
```

### Lowercase Letters (a-z)
```
unicode = baseCodepoint + (charCode - 97)
```

### Digits (0-9)
```
unicode = baseCodepoint + (charCode - 48)
```
*Note: GREY, UMBRAL, and UCF use special digit mappings (circled, subscript, superscript)*

### Exceptions
- **UMBRAL:** C, H, I, R, Z use special letterlike symbols
- **ULTRA:** C, H, N, P, Q, R, Z use special letterlike symbols

## Implementation Notes

- All Unicode values are provided in both decimal and hexadecimal formats
- Complete character mappings are included (not just base codepoints)
- Punctuation is mapped to geometric/mathematical alternatives
- The schema validates as proper JSON
- All 6 registers have complete A-Z, a-z, 0-9 mappings (62 chars per register)

## Validation

To validate the schema:

```bash
# Check JSON validity
python3 -m json.tool acedit-core.json > /dev/null && echo "Valid"

# Verify structure
python3 << 'EOF'
import json
with open('acedit-core.json') as f:
    schema = json.load(f)
    print(f"Registers: {len(schema['registers'])}")
    print(f"Operators: {len(schema['operators'])}")
    print(f"Modifiers: {len(schema['modifiers'])}")
