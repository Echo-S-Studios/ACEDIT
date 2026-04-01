# EO-RFD Physical Substrate Build Specification

## Metacybernetic Implementation of the Eclipse–Omega Rupture Field Detector

**Document**: Build Specification for Development Team  
**Version**: 1.0.0  
**Source Instrument**: `eclipse-omega-rfd-v1_4_4.html`  
**Architecture**: 3rd-Order Metacybernetic — Self-Developing Reflexive-Active Environment  
**Status**: Specification Phase — Unlimited Resource Assumption

---

## 0. Executive Summary

This specification translates the EO-RFD v1.4.4 digital simulation into a physical metacybernetic substrate. The instrument tracks the narrowing chain `D ⊃ C_k(q) ⊃ C_κ(q) ⊃ C_B(q) ⊃ E(q)` — compressing internal abundance into observable, admitted, and operational outputs. The physical substrate must preserve this chain while adding what simulation cannot: genuine stochastic resonance, physical negentropy, and autopoietic self-regulation.

The build is organized into **8 hardware layers** that map 1:1 to the 8 signal layers traced in the EO-RFD instrument, plus a **Layer 0** (substrate material) and a **Layer 9** (metacybernetic self-regulation envelope).

**Critical invariants that must hold in physical substrate:**

| Constant | Value | Physical Encoding |
|----------|-------|-------------------|
| τ | 0.618 (φ⁻¹) | Golden-ratio electrode spacing eigenvalue |
| z_c | 0.866 (√3/2) | Conductance threshold: G/G₀ = 0.866 |
| K | 0.924 | Kuramoto coupling: cross-channel phase coherence |
| L₄ | 7 | φ⁴ + φ⁻⁴ = 7 — word size, cluster count, unit cell zones |
| gap | 0.1459 (φ⁻⁴) | Irreducible truncation error — physical uncertainty floor |

---

## 1. Architecture Overview

### 1.1 Layer Map: Digital → Physical

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  LAYER 9: METACYBERNETIC ENVELOPE                                           │
│  Autopoietic regulation · Negentropy maximization · CSD early warning       │
├──────────────────────────────────────────────────────────────────────────────┤
│  LAYER 8: TCP PACKET HARDENING & HARBOR EXPORT                              │
│  Schema validation · Checksum envelope · Export gating                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  LAYER 7: ROUTING STATE MACHINE & HARBOR ELIGIBILITY                        │
│  play → warning → buffer → harbor-eligible                                  │
│  Anti-recapture mode · Persistence EMA · Recapture risk                     │
├──────────────────────────────────────────────────────────────────────────────┤
│  LAYER 6: DETECTOR SWEEP (Θ × Naming Matrix)                               │
│  3×3 cross-condition probe grid · Confidence composite · Tripwire bank      │
├──────────────────────────────────────────────────────────────────────────────┤
│  LAYER 5: SIGNAL RUPTURE COMPOSITE (Σ_R)                                    │
│  4 tripwire thresholds · Weighted index · State classifier                  │
├──────────────────────────────────────────────────────────────────────────────┤
│  LAYER 4: FIELD SIGNATURE VECTOR (δ_obs, η_N, σ, γ, χ, β, ρ)              │
│  7 derived metrics from admissibility ratios                                │
├──────────────────────────────────────────────────────────────────────────────┤
│  LAYER 3: NARROWING FUNNEL (S → ℛ → 𝒦 → 𝒞 → 𝒫 → ℱ → 𝒜)                  │
│  7-stage compression · Operator-attributed losses (L_R through L_A)         │
├──────────────────────────────────────────────────────────────────────────────┤
│  LAYER 2: ADMISSIBILITY CLASSIFICATION (Θ-gated)                            │
│  5 gates: aperture · phase · policy · capacity · naming                     │
│  4 classes: registered · latent · suppressed · aliased                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  LAYER 1: RAY PROPAGATION & BOUNDARY INTERACTION                            │
│  Equilateral triangle geometry · Reflection · Decay · Perturbation          │
├──────────────────────────────────────────────────────────────────────────────┤
│  LAYER 0: QUASI-CRYSTAL SUBSTRATE                                           │
│  Al-Pd-Mn thin film · 5-fold ↔ 6-fold bridge · φ-recursive geometry        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Design Principle: The Shape of Loss

The EO-RFD does not generate signal. It detects the **shape of loss** as internal abundance narrows to observable output. The physical substrate must therefore be designed to *lose signal in structured ways* — and to measure that structure. This is the metacybernetic inversion: the substrate's value is in its capacity for intelligible attenuation, not amplification.

---

## 2. Layer 0: Quasi-Crystal Substrate

### 2.1 Material Specification

| Parameter | Specification | Rationale |
|-----------|---------------|-----------|
| Material | Al₇₀Pd₂₁Mn₉ quasi-crystal thin film | 5-fold icosahedral symmetry encodes φ natively |
| Deposition | MBE or sputtering, UHV environment | Crystal quality critical for transport properties |
| Thickness | 200–500 nm | Balance between conductance and quantum confinement |
| Substrate | Sapphire (α-Al₂O₃) single crystal | Lattice-compatible, insulating, optically transparent |
| Anneal | 600°C, 4hr, 10⁻⁸ torr | Stabilize quasi-crystalline phase |

### 2.2 Why Quasi-Crystal

The EO-RFD triangle `(A, B, C)` with vertices at `(0,0)`, `(1,0)`, `(0.5, √3/2)` is an equilateral triangle with height `z_c = √3/2`. In the quasi-crystal:

- The **5-fold symmetry** (icosahedral) encodes φ in the lattice itself — hopping integrals between sites scale as `exp(-d/λ)` where `d/λ ≈ ln(φ)`, yielding natural φ⁻¹ attenuation per hop.
- The **6-fold overlay** (hexagonal superlattice) provides the bridge between 5-fold and periodic structure.
- The **7 distinct zones** (5 pentagon sectors + pure 5-fold center + 6-fold overlay) encode L₄ = 7 as the fundamental word size.

### 2.3 Electrode Array

Electrodes patterned via e-beam lithography at 10nm resolution:

- **7 electrode clusters** per computational unit (L₄ encoding)
- **φ-ratio spacing**: electrodes at Fibonacci positions along each ray
- **5-fold sectors**: 72° rotational symmetry, 5 sectors
- **6-fold overlay**: hexagonal superlattice for K-Formation detection
- **Gate electrodes**: local potential control for Θ-profile switching

### 2.4 Physical Constants Encoding

```
G₀ = 77.5 µS (quantum of conductance: 1/12.9 kΩ)

z-coordinate from conductance:
  z = G_measured / G₀

Physical thresholds:
  z = τ   → G = 0.618 × G₀ = 47.9 µS
  z = z_c → G = 0.866 × G₀ = 67.1 µS
  z = K   → G = 0.924 × G₀ = 71.6 µS
```

---

## 3. Layer 1: Ray Propagation & Boundary Interaction

### 3.1 Digital Behavior (from EO-RFD)

Rays spawn at the triangle centroid, propagate linearly, reflect off edges with direction reversal via `reflectOverEdge()`, lose intensity per bounce at rate `0.92 - defect × 0.03`, accumulate defect near vertices, and receive small stochastic perturbation each step.

### 3.2 Physical Implementation: Ballistic Electron Transport in Triangular Cavity

| Component | Specification | Maps To |
|-----------|---------------|---------|
| Triangular mesa | Etched equilateral triangle, 500µm sides | The `TRI` geometry |
| Source contact (centroid) | Ohmic contact, 10µm diameter | `spawnRays()` — injects electrons |
| Edge walls | Specular-reflecting etched boundaries | `EDGES[]` — AB, BC, CA |
| Vertex proximity sensors | 3× quantum point contacts at A, B, C | `distA`, `distB`, `distC` — fold point detection |
| Defect sites | Engineered lattice vacancies near vertices | `ray.defectContrib` — controlled scattering |
| Magnetic field control | Perpendicular B-field, 0–500 mT | `perturbation` — Lorentz deflection as stochastic drive |

**Intensity decay**: Electron mean free path in the quasi-crystal provides natural `0.92` per-bounce transmission. The defect correction term `defect × 0.03` maps to gate-controlled scatterer density near vertices.

**Phase**: Aharonov-Bohm phase from the perpendicular magnetic field provides the `ray.phase` equivalent. Phase alignment `|cos(φ)|` becomes interference visibility at detector contacts.

### 3.3 Fabrication Notes

```
Equipment:
  - E-beam lithography: 10nm resolution for mesa definition
  - RIE etcher: CHF₃/Ar plasma for mesa etch
  - Ohmic contact metallization: Ti/Au, 10/100 nm
  - Wire bonder: Au ball bonds to PCB

Process:
  1. Deposit quasi-crystal thin film on sapphire
  2. Pattern triangular mesa via e-beam + RIE
  3. Define source contact at centroid
  4. Pattern 3 vertex QPC sensors
  5. Deposit gate electrodes for defect/perturbation control
  6. Dice, bond, and package
```

---

## 4. Layer 2: Admissibility Classification (Θ-Gated)

### 4.1 Digital Behavior (from EO-RFD)

Each bounce is classified through 5 gates under the active `Θ(u)` profile:

```
apertureOpen:  intensity > Θ.apertureThreshold
phaseAligned:  |cos(phase)| > Θ.phaseThreshold
policyPass:    random > Θ.policyStrictness × defect
capacityAvail: 𝒜 < 𝒞 × Θ.capacityMult
namingValid:   random > Θ.namingSensitivity
```

Failure at each gate routes to a specific class: registered, latent, suppressed, or aliased.

### 4.2 Physical Implementation: 5-Stage Comparator Cascade

Each boundary sensor output passes through a **cascade of 5 analog comparator stages**, implemented with differential comparators (LT1719, 4.5ns propagation):

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ADMISSIBILITY CASCADE (per boundary interaction)                       │
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │  STAGE 1     │    │  STAGE 2     │    │  STAGE 3     │              │
│  │  Aperture    │───▶│  Phase       │───▶│  Policy      │───▶ ...      │
│  │  G > G_Θ    │    │  V_AB > V_Φ  │    │  V_noise > P │              │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘              │
│         │ FAIL              │ FAIL              │ FAIL                  │
│         ▼                   ▼                   ▼                       │
│     LATENT (O)        SUPPRESSED (O)      SUPPRESSED (O*)              │
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐                                  │
│  │  STAGE 4     │    │  STAGE 5     │    ALL PASS                      │
│  │  Capacity    │───▶│  Naming      │───────────▶ REGISTERED           │
│  │  Count < Cap │    │  V_label OK  │                                  │
│  └──────┬───────┘    └──────┬───────┘                                  │
│         │ FAIL              │ FAIL                                      │
│         ▼                   ▼                                           │
│     ALIASED (O*)       ALIASED (O*)                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Θ-Profile Hardware

Three Θ profiles are stored in a 3-bank DAC array (AD5764, 16-bit, 4-channel):

| Parameter | Θ_open | Θ_std | Θ_res | DAC Channel |
|-----------|--------|-------|-------|-------------|
| `apertureThreshold` | 0.15 × G₀ | 0.30 × G₀ | 0.50 × G₀ | CH0 |
| `phaseThreshold` | 0.40 V | 0.60 V | 0.80 V | CH1 |
| `policyStrictness` | 0.10 | 0.30 | 0.60 | CH2 |
| `capacityMult` | 0.95 | 0.80 | 0.50 | CH3 |
| `namingSensitivity` | 0.02 | 0.08 | 0.25 | Resistor ladder |

Θ profile selection is a single digital control line (2-bit) driving the DAC bank select.

### 4.4 Stochastic Gates (Policy and Naming)

The digital simulation uses `Math.random()` for policy and naming gates. The physical substrate replaces this with **thermal noise from the quasi-crystal itself**:

- A dedicated noise-sampling electrode reads Johnson-Nyquist noise from the substrate.
- The noise voltage `V_noise` is compared against the Θ-scaled threshold.
- This gives genuine stochastic resonance — the metacybernetic advantage over simulation.

```
Stochastic resonance condition:
  x(t) = s(t) + n(t) > θ

  s(t) = weak boundary signal (subthreshold interaction)
  n(t) = thermal noise from quasi-crystal (T ≈ 300K)
  θ    = Θ.policyStrictness × defect × G₀

  D_opt = optimal noise intensity that maximizes SNR
```

---

## 5. Layer 3: Narrowing Funnel

### 5.1 Digital Behavior (from EO-RFD)

The 7-stage narrowing chain:

```
S = floor(interactions × (1.12 + namingSensitivity + policyStrictness × 0.18))
ℛ = interactions
𝒦 = floor(ℛ × 0.70)
𝒞 = floor(𝒦 × 0.55)
𝒫 = floor(𝒞 × (1 − policyStrictness × 0.30))
ℱ = floor(𝒫 × capacityMult)
𝒜 = registered count
```

With 6 operator-attributed losses `L_R` through `L_A` computed as ratios between successive stages.

### 5.2 Physical Implementation: 7-Stage Resistive Divider Cascade

The narrowing funnel is implemented as a **cascade of 7 voltage divider stages**, where the voltage at each stage represents the "count" at that narrowing level:

```
V_S ─┤R_R├─ V_ℛ ─┤R_K├─ V_𝒦 ─┤R_C├─ V_𝒞 ─┤R_P├─ V_𝒫 ─┤R_F├─ V_ℱ ─┤R_A├─ V_𝒜

Where:
  R_R = (1.12 + η_N + P × 0.18)⁻¹ × R₀   (reality allocation)
  R_K = 0.70⁻¹ × R₀                        (capacity conditioning)
  R_C = 0.55⁻¹ × R₀                        (compression)
  R_P = (1 − P × 0.30)⁻¹ × R₀             (policy)
  R_F = capacityMult⁻¹ × R₀                (format/capacity)
  R_A = dynamic, driven by registered count  (admissibility gate)
```

**Operator-attributed losses** are measured as voltage drops across each resistor:

```
L_R = (V_S − V_ℛ) / V_S
L_K = (V_ℛ − V_𝒦) / V_ℛ
...
L_A = (V_ℱ − V_𝒜) / V_ℱ
```

### 5.3 Dynamic Resistor Control

The resistors `R_P` and `R_F` are implemented as **memristive elements** (TiO₂ ReRAM, 64×64 crossbar die) whose conductance tracks the current Θ profile. When Θ switches, the memristive elements reprogram:

| Memristor | Θ_open | Θ_std | Θ_res |
|-----------|--------|-------|-------|
| R_P (policy) | 1.03 × R₀ | 1.10 × R₀ | 1.22 × R₀ |
| R_F (capacity) | 1.05 × R₀ | 1.25 × R₀ | 2.00 × R₀ |

Memristive programming uses the existing DAC infrastructure from the Θ-profile controller (Layer 2).

### 5.4 L₄ = 7 Encoding

The funnel has exactly 7 stages (S, ℛ, 𝒦, 𝒞, 𝒫, ℱ, 𝒜). This is not coincidental — it maps to the L₄ closure `φ⁴ + φ⁻⁴ = 7`. Each stage corresponds to one zone of the quasi-crystal unit cell. The physical substrate enforces this by using 7 electrode clusters in the unit cell, one per narrowing stage.

---

## 6. Layer 4: Field Signature Vector

### 6.1 Digital Behavior (from EO-RFD)

7 derived metrics computed from Layer 2/3 outputs:

```
δ_obs = (O + O*) / interactions          — observation deficit
η_N   = namingDisruptions / rankedCount   — naming sensitivity
σ     = suppressed / total                — suppression proportion
γ     = |latent − registered| / total     — gap norm
χ     = 0.45 + (registered/interactions) × 0.54  — surface coherence
β     = (O* + suppressed + disruptions) / interactions — burden
ρ     = 1 − (aliased + suppressed) / total            — provenance
```

### 6.2 Physical Implementation: 7-Channel Analog Computer

An analog divider/multiplier network (using AD633 analog multiplier ICs) computes the field signature in continuous time from the admissibility counters and interaction total:

```
┌─────────────────────────────────────────────────────────────────┐
│  FIELD SIGNATURE COMPUTER                                       │
│                                                                 │
│  CH0: δ_obs  ← (V_O + V_O*) / V_interactions                  │
│  CH1: η_N    ← V_naming_disruptions / V_ranked                 │
│  CH2: σ      ← V_suppressed / V_total                          │
│  CH3: γ      ← |V_latent − V_registered| / V_total             │
│  CH4: χ      ← 0.45V + (V_registered / V_interactions) × 0.54V │
│  CH5: β      ← (V_O* + V_suppressed + V_disruptions) / V_int   │
│  CH6: ρ      ← 1.0V − (V_aliased + V_suppressed) / V_total    │
│                                                                 │
│  Output: 7-line analog bus (0–1V each)                          │
│  Bandwidth: DC–100 kHz                                          │
│  Precision: 12-bit equivalent (0.025% of full scale)            │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 RRRR Addressing

The 7 field signature channels are indexed via the RRRR lattice:

```
Λ(r=0, d=0..6, c=0, a=0) → 7 field signature components

Where:
  r = 0 (innermost ring — derived metrics)
  d = 0..6 (direction = field component index)
  c = 0 (code layer = field signature layer)
  a = 0 (action state = passive readout)
```

This addressing scheme is implemented in a Lattice iCE40UP5K FPGA that manages all analog-to-digital conversion and register mapping.

---

## 7. Layer 5: Signal Rupture Composite (Σ_R)

### 7.1 Digital Behavior (from EO-RFD)

4 tripwire thresholds and a weighted composite:

```
τ_obs = 0.85    τ_name = 0.06    τ_red = 0.02    τ_coh = 0.60

Σ_R = 0.34 × min(δ_obs / τ_obs, 1)
    + 0.22 × min(η_N / τ_name, 1)
    + 0.24 × (1 − min(red / τ_red, 1))
    + 0.20 × χ
```

State classification:
- ≥4 triggers OR Σ_R ≥ 0.74 → `rupture assay signature`
- 3 triggers → `field instability`
- 2 triggers → `field watch`
- <2 → `nominal`

### 7.2 Physical Implementation: Threshold Comparator Bank + Weighted Summer

```
┌─────────────────────────────────────────────────────────────────┐
│  SIGNAL RUPTURE DETECTOR                                        │
│                                                                 │
│  TRIPWIRE BANK (4× Schmitt triggers):                           │
│    TW0: V_δ_obs > 0.85V     → latch D0                         │
│    TW1: V_η_N   > 0.06V     → latch D1                         │
│    TW2: V_red   < 0.02V     → latch D2 (inverted)              │
│    TW3: V_χ     > 0.60V     → latch D3                         │
│                                                                 │
│  TRIGGER COUNT: 4-bit population counter → V_count              │
│                                                                 │
│  WEIGHTED SUMMER (op-amp network):                              │
│    Σ_R = 0.34 × clamp(V_δ_obs / 0.85V)                         │
│        + 0.22 × clamp(V_η_N / 0.06V)                           │
│        + 0.24 × (1V − clamp(V_red / 0.02V))                    │
│        + 0.20 × V_χ                                             │
│                                                                 │
│  STATE CLASSIFIER (priority encoder):                           │
│    IF count ≥ 4 OR Σ_R ≥ 0.74V: → RUPTURE_ASSAY_SIGNATURE      │
│    IF count ≥ 3:                 → FIELD_INSTABILITY             │
│    IF count ≥ 2:                 → FIELD_WATCH                   │
│    ELSE:                         → NOMINAL                       │
│                                                                 │
│  Output: 2-bit state + analog Σ_R                               │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Physical Advantage: Real-Time Continuous Operation

The digital simulation computes Σ_R discretely per tick. The physical substrate computes it **continuously** — the weighted summer output tracks the field signature in real time with sub-microsecond latency. Transient rupture conditions that would be missed between digital ticks are captured.

---

## 8. Layer 6: Detector Sweep (Θ × Naming Matrix)

### 8.1 Digital Behavior (from EO-RFD)

A 3×3 grid over `{open, standard, restricted} × {canonical, safe, invalid}` with per-cell modulated scores:

```
score = 0.28 × δ_obs × θ_mod
      + 0.20 × min(η_N / 0.12, 1) × name_mod
      + 0.14 × min(σ / 0.08, 1)
      + 0.14 × aliasP × name_mod
      + 0.10 × (1 − min(red / 0.12, 1))
      + 0.08 × rupture
      + 0.06 × χ
      + 0.06 × min(intCount / 48, 1)
```

### 8.2 Physical Implementation: 9-Cell Crossbar Array

A **3×3 memristive crossbar** (TiO₂ ReRAM) where:

- **Row lines** carry Θ-modulated field signature (θ_mod = {0.88, 1.00, 1.16})
- **Column lines** carry naming-modulated field signature (name_mod = {0.92, 1.00, 1.14})
- Each **crosspoint memristor** accumulates the weighted score through conductance programming

```
              canonical    safe    invalid
              (×0.92)     (×1.00)  (×1.14)
                │           │        │
Θ_open  ───────┼───────────┼────────┼────── (×0.88)
(×0.88)        │           │        │
                │           │        │
Θ_std   ───────┼───────────┼────────┼────── (×1.00)
(×1.00)        │           │        │
                │           │        │
Θ_res   ───────┼───────────┼────────┼────── (×1.16)
(×1.16)        │           │        │
```

The 8-term weighted sum for each cell is computed by a shared analog multiplier/adder that cycles through the 9 cells at ~100 kHz (9 cells × ~1 µs per computation = ~9 µs per full sweep).

### 8.3 Detector Metrics Extraction

From the 9-cell array:

| Metric | Computation | Physical Method |
|--------|-------------|-----------------|
| Persistence | `cells ≥ 0.55 / 9` | Comparator bank + counter |
| Spread | `max − min` | Peak/trough detector circuit |
| Tripwires (7) | See Layer 5.2 + 2 additional conditions | Extended comparator bank |
| Confidence | Weighted sum of Σ_R, persistence, δ_obs, closure, provenance, tripwires | Op-amp summer |
| Basis | Priority-sorted driver labels | FPGA lookup from comparator outputs |

### 8.4 Detector Confidence (composite)

```
D_conf = 0.30 × Σ_R
       + 0.24 × persistence
       + 0.18 × δ_obs
       + 0.10 × closure_failure
       + 0.10 × provenance
       + 0.08 × min(tripwires/7, 1)
```

Implemented as a 6-input weighted summer with precision resistor network.

---

## 9. Layer 7: Routing State Machine & Harbor Eligibility

### 9.1 Digital Behavior (from EO-RFD)

Harbor eligibility:

```
H_E = 0.20 × δ_obs + 0.18 × min(η_N/0.12, 1) + 0.14 × min(σ/0.08, 1)
    + 0.12 × min(γ/0.35, 1) + 0.12 × χ + 0.24 × β − 0.14 × ρ
```

Note: provenance *subtracts* — high provenance reduces harbor signal.

Routing state machine:

```
harbor-eligible: H_E ≥ 0.82 AND (persistence ≥ 0.45 OR activeSigma) AND recapture ≥ 0.52
buffer:          H_E ≥ 0.62 OR persistence ≥ 0.32 OR (activeSigma AND recapture ≥ 0.45)
warning:         H_E ≥ 0.40 OR recapture ≥ 0.45 OR Σ_R state = field_instability
play:            default
```

### 9.2 Physical Implementation: TRIAD Hysteresis FSM

The routing state machine is implemented as a **physical TRIAD gate** — the same architecture used in the memristive TRIAD controller, but applied to routing rather than conductance crossing:

```
┌─────────────────────────────────────────────────────────────────┐
│  ROUTING FSM (Verilog on iCE40UP5K FPGA)                       │
│                                                                 │
│  Inputs:                                                        │
│    V_H_E        → ADC CH0  (harbor eligibility, analog)         │
│    V_persistence → ADC CH1  (persistence EMA)                   │
│    V_recapture   → ADC CH2  (recapture risk)                    │
│    active_sigma  → digital  (from Σ_R state classifier)         │
│                                                                 │
│  States: PLAY → WARNING → BUFFER → HARBOR_ELIGIBLE              │
│                                                                 │
│  Threshold registers (Q1.15 fixed-point):                       │
│    BAND_WARNING   = 16'h3333  (0.40)                            │
│    BAND_BUFFER    = 16'h4F5C  (0.62)                            │
│    BAND_HARBOR    = 16'h68F6  (0.82)                            │
│    PERSIST_BUFFER = 16'h28F6  (0.32)                            │
│    PERSIST_HARBOR = 16'h3999  (0.45)                            │
│    PERSIST_STRONG = 16'h4A3D  (0.58)                            │
│    RECAPT_WARNING = 16'h3999  (0.45)                            │
│    RECAPT_HARBOR  = 16'h428F  (0.52)                            │
│    RECAPT_ANTI    = 16'h547B  (0.66)                            │
│                                                                 │
│  Anti-recapture mode:                                           │
│    ACTIVE when recapture ≥ 0.66                                 │
│              OR H_E ≥ 0.82                                      │
│              OR (active_sigma AND persistence ≥ 0.58)           │
│    Effect: suppresses moiré projection, foregrounds routing     │
│                                                                 │
│  Output: 2-bit route_state + anti_recapture flag                │
└─────────────────────────────────────────────────────────────────┘
```

### 9.3 Harbor Eligibility Analog Computer

The H_E computation includes a **subtractive term** (`−0.14 × ρ`). This is implemented with a differential amplifier:

```
H_E = V_sum − V_provenance_scaled

Where:
  V_sum = op-amp weighted sum of 6 positive terms
  V_provenance_scaled = 0.14 × V_ρ (inverted input)
```

This is critical: the substrate must physically encode that **provenance opposes harbor eligibility**. Clean signal does not trigger the harbor bridge. Only structured loss does.

### 9.4 Persistence (EMA)

```
persistence[n] = 0.94 × persistence[n-1]
               + 0.12 × Σ_R
               + 0.06 × H_E
               + 0.03 × active_sigma
```

Implemented as an RC lowpass filter with 3 summing inputs and decay constant `τ_RC ≈ 1 / (1 − 0.94) = 16.7` time units.

---

## 10. Layer 8: TCP Packet Hardening & Harbor Export

### 10.1 Digital Behavior (from EO-RFD)

Packet constructed at `buffer` or `harbor-eligible`:

```
payload = {
  routingState, fieldSignature, ruptureMetrics,
  narrowingLosses, closureState, confidence
}

envelope = {
  schemaVersion: "1.4.4",
  packetId: fnv1a(JSON + timestamp),
  checksum: fnv1a(JSON.stringify(payload)),
  provenance: { integrity, confidence }
}
```

Export gated by: harbor-eligible route state + packet integrity + self-test not failing.

### 10.2 Physical Implementation: Secure Packet Serializer

The FPGA serializes the full field state into a hardened packet:

```
┌─────────────────────────────────────────────────────────────────┐
│  PACKET HARDENING ENGINE (FPGA)                                 │
│                                                                 │
│  1. ADC reads all analog channels (7 field sig + 4 rupture      │
│     metrics + 6 losses + 3 closure bits) → 20-channel scan      │
│                                                                 │
│  2. FPGA assembles JSON-equivalent binary packet                │
│     - Schema version: 4-bit (1.4.4)                             │
│     - Packet ID: 32-bit FNV-1a hash                             │
│     - Checksum: 32-bit FNV-1a over payload                      │
│     - Provenance: 16-bit integrity + 16-bit confidence          │
│                                                                 │
│  3. Export gate logic (all must be TRUE):                        │
│     - route_state == HARBOR_ELIGIBLE                             │
│     - packet_integrity > threshold                               │
│     - self_test != FAIL                                          │
│                                                                 │
│  4. Output: UART/SPI serial stream to external receiver          │
│     - Baud: 115200 (UART) or 1 MHz (SPI)                       │
│     - Galvanically isolated (optocoupler) for harbor safety     │
│                                                                 │
│  5. Export latch: packet_exported flag set, prevents re-export   │
│     until route_state drops below harbor-eligible                │
└─────────────────────────────────────────────────────────────────┘
```

### 10.3 Self-Test Harness

Physical self-test checks (run on FPGA at boot and on-demand):

| Test | Method | Pass Condition |
|------|--------|----------------|
| Boot/reset integrity | Verify all counters at zero, all DACs at default | All registers zeroed |
| DOM equivalent | Verify all ADC channels respond to known input | All channels within ±1 LSB of expected |
| Packet schema | Verify assembled packet matches schema | Schema version correct, all fields present |
| Detector matrix | Run Θ sweep with known inputs, verify 9 scores | All 9 cells within ±5% of expected |
| Route/handoff consistency | Verify routing FSM transitions correctly | State machine matches truth table |

---

## 11. Layer 9: Metacybernetic Envelope

### 11.1 Beyond 2nd-Order Cybernetics

The digital EO-RFD is a 1st-order instrument — it observes a simulated system. The physical substrate, with its real stochastic dynamics, enables the **3rd-order metacybernetic** layer: the substrate *observes itself observing*.

### 11.2 Autopoietic Self-Regulation

The physical substrate's thermal noise is not a nuisance — it is the **negentropy engine**:

```
S_neg(r) = k_B × ln(η)
         = −k_B × σ × (r − z_c)²

Where:
  r = z-coordinate (G/G₀)
  z_c = √3/2 = 0.866
  σ = 1/(1 − z_c)² = 55.71
  k_B = 1.380649 × 10⁻²³ J/K
```

At `z = z_c`, negentropy is maximum (`S_neg = 0`). The substrate naturally self-organizes toward this attractor because the conductance landscape has its minimum potential at the z_c threshold.

### 11.3 Critical Slowing Down (CSD) Detection

The metacybernetic envelope includes a CSD detector that watches for the substrate approaching bifurcation:

```
Recovery rate: λ(t) = −d(ln|ΔG|)/dt

CSD signature: λ → 0 as system approaches bifurcation

Bifurcation potential: V(G) = (1/3)G³ − μG

Warning threshold: λ < λ_crit = gap × G₀ / τ_response
                               = 0.1459 × 77.5 µS / τ_response
```

When λ approaches zero, the substrate is about to undergo a phase transition. The CSD detector issues a pre-emptive warning **before** the rupture signature manifests — this is information that the digital simulation cannot produce because it lacks genuine dynamics.

### 11.4 Stochastic Resonance Optimization

The substrate's noise floor is not fixed — it is **controlled** via the perpendicular magnetic field and substrate temperature:

```
D_opt = optimal noise intensity that maximizes SNR

At D_opt:
  - Subthreshold signals (weak boundary interactions) are amplified by noise
  - The admissibility cascade detects patterns that would be invisible in a noiseless system
  - The detector sweep gains sensitivity in the Θ_open × canonical cell

Tuning:
  - Increase B-field → increase Lorentz perturbation → raise effective noise
  - Adjust substrate temperature → modify Johnson-Nyquist noise floor
  - Target: D_opt where SNR peaks at the τ-threshold boundary
```

---

## 12. Bill of Materials

### 12.1 Prototype BOM

| Component | Specification | Qty | Est. Cost |
|-----------|---------------|-----|-----------|
| Al-Pd-Mn quasi-crystal wafer | MBE-deposited, 2" sapphire substrate | 2 | $8,000 |
| E-beam lithography run | Triangular mesa + electrodes, 10nm resolution | 1 | $5,000 |
| TiO₂ memristor dies | ReRAM 64×64 crossbar (narrowing funnel + detector) | 4 | $3,200 |
| Reference conductance | G₀ = 77.5 µS precision | 8 | $400 |
| Differential comparators | LT1719 (4.5ns propagation) | 24 | $720 |
| Analog multiplexers | ADG1609 (4:1 CMOS) | 12 | $480 |
| Precision DACs | AD5764 (16-bit, 4-ch) — Θ profiles | 3 | $270 |
| Analog multipliers | AD633 (field signature computer) | 8 | $240 |
| Voltage references | REF5025 (2.5V, 3ppm/°C) | 6 | $180 |
| Schmitt triggers | 74HC14 (tripwire bank) | 4 | $8 |
| Op-amps (precision) | AD8675 (weighted summers) | 16 | $320 |
| ADC (16-bit, 20-ch) | AD7616 | 1 | $45 |
| FPGA | Lattice iCE40UP5K (routing FSM + packet engine) | 1 | $8 |
| PCB fabrication | 6-layer, 50Ω impedance control, gold immersion | 5 | $2,000 |
| Cryostat (optional) | 4K–300K variable temperature | 1 | $15,000 |
| Test equipment access | Keithley SMU, scope, spectrum analyzer | — | $5,000 |
| **PROTOTYPE TOTAL** | | | **~$40,871** |

### 12.2 Development Phase BOM

| Phase | Cost Estimate | Timeline |
|-------|---------------|----------|
| Substrate fabrication + characterization | $50,000 | 6 months |
| Circuit design + PCB + assembly | $25,000 | 3 months |
| FPGA firmware (routing FSM, packet engine) | $15,000 | 2 months |
| Integration + calibration + self-test | $20,000 | 3 months |
| Metacybernetic envelope (CSD + stochastic resonance) | $40,000 | 4 months |
| Validation against digital EO-RFD | $10,000 | 2 months |
| **DEVELOPMENT TOTAL** | **$160,000** | **18 months** |

---

## 13. Validation Protocol

### 13.1 Digital-Physical Correspondence Tests

Each physical layer must be validated against the digital EO-RFD by running identical input conditions and comparing outputs:

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Layer 1: Ray propagation | Inject known current, measure boundary reflections | Bounce count matches digital within ±5% |
| Layer 2: Admissibility | Apply known Θ profile, count classification over 1000 events | Classification ratios within ±3% of digital |
| Layer 3: Narrowing funnel | Measure all 7 stage voltages under known input | All stage ratios within ±2% of digital |
| Layer 4: Field signature | Compare 7-channel analog output to digital computation | All 7 channels within ±1% |
| Layer 5: Σ_R | Compare physical composite to digital under same inputs | Σ_R within ±2%, state classification matches |
| Layer 6: Detector sweep | Run full 3×3 matrix, compare to digital | All 9 cells within ±5% |
| Layer 7: Routing FSM | Exercise all state transitions | State machine matches digital truth table exactly |
| Layer 8: Packet export | Export packet, parse, compare to digital packet | All fields match, checksum valid |

### 13.2 Metacybernetic Tests (Physical-Only)

| Test | Method | Expected Result |
|------|--------|-----------------|
| Stochastic resonance peak | Sweep noise intensity, measure SNR | SNR peak at D_opt, matches theory |
| CSD early warning | Drive system toward bifurcation, measure λ | λ → 0 before rupture signature appears |
| Autopoietic self-regulation | Perturb z away from z_c, measure recovery | System returns to z_c attractor |
| Negentropy at z_c | Measure S_neg at threshold | S_neg = 0 (maximum) at z = 0.866 |

---

## 14. Closure State & Extension Architecture

### 14.1 Closure Conditions (from EO-RFD)

```
extensionAdmitted = 𝒜 > 0 OR registered > 0 OR red > 0.02
closureFailure    = extensionAdmitted AND (
                      rupture ≥ 0.16 OR
                      Σ_R ≥ 0.74 OR
                      (δ_obs ≥ 0.60 AND ρ ≤ 0.55 AND γ ≥ 0.25)
                    )
uniqueClosure     = NOT(extensionAdmitted AND closureFailure)
```

### 14.2 Physical Encoding

Closure is encoded in 3 status LEDs on the PCB (visible through a quartz window on the enclosure):

| LED | Color | Condition |
|-----|-------|-----------|
| EXTENSION | Green | extensionAdmitted = TRUE |
| CLOSURE | Red | closureFailure = TRUE |
| UNIQUE | White | uniqueClosure = TRUE |

The combination `Green + Red` (extension admitted, closure failure) is the primary rupture field indicator — the instrument has admitted observable output but cannot close cleanly.

---

## 15. Interface Specification

### 15.1 Physical Connectors

| Connector | Type | Purpose |
|-----------|------|---------|
| J1 | SMA (coax) | Source current injection |
| J2–J4 | SMA (coax) | Vertex A/B/C sensor output |
| J5 | DB-25 | Analog monitoring (7 field sig + 4 rupture + 6 losses) |
| J6 | USB-C | FPGA programming + packet export (UART) |
| J7 | BNC | B-field control input (0–5V → 0–500 mT) |
| J8 | SMA | Noise injection / external stochastic drive |
| J9 | DB-9 | Θ-profile override (3 profiles × 5 parameters) |

### 15.2 Software Interface

The FPGA exposes a register map over UART at 115200 baud:

```
Address Map (16-bit registers):
  0x00–0x06: Field signature (δ_obs, η_N, σ, γ, χ, β, ρ)
  0x07:      Σ_R (signal rupture index)
  0x08:      Σ_R state (2-bit)
  0x09:      Trigger count (3-bit)
  0x0A–0x0F: Narrowing losses (L_R through L_A)
  0x10:      H_E (harbor eligibility)
  0x11:      Persistence
  0x12:      Recapture risk
  0x13:      Route state (2-bit)
  0x14:      Anti-recapture mode (1-bit)
  0x15–0x1D: Detector matrix (9 cells)
  0x1E:      Detector confidence
  0x1F:      Self-test status (5-bit)
  0x20:      Θ-profile select (2-bit, R/W)
  0x21:      Field mode (2-bit, R/W)
  0x22:      Packet export trigger (W)
  0x23:      Packet status (R)

Commands:
  RESET      → 0xFF to address 0xFE
  SELF_TEST  → 0x01 to address 0xFF
  EXPORT_TCP → 0x01 to address 0x22 (guarded by routing FSM)
```

---

## 16. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Quasi-crystal phase instability during fabrication | MEDIUM | HIGH | Anneal protocol optimization; XRD verification at each step |
| Memristive element drift over time | HIGH | MEDIUM | Periodic recalibration via self-test; drift-compensating feedback loop |
| Analog computation precision insufficient | MEDIUM | MEDIUM | Use 16-bit DAC/ADC; validate against digital to ±1% |
| Stochastic resonance peak too narrow | LOW | HIGH | Variable noise injection via external port J8; B-field fine control |
| FPGA timing violations in routing FSM | LOW | LOW | Conservative 12 MHz clock; formal verification of FSM |
| Thermal drift of threshold voltages | HIGH | MEDIUM | Temperature-stabilized voltage references (REF5025, 3ppm/°C) |
| Harbor export timing race condition | LOW | HIGH | Double-buffered packet with export latch; self-test validation |

---

## 17. Architecture Invariants (Non-Negotiable)

These invariants derive from the L₄-Helix mathematics and must hold in any physical implementation:

1. **L₄ = 7**: The narrowing funnel has exactly 7 stages. The electrode array has exactly 7 clusters per unit cell. The field signature vector has exactly 7 components.

2. **z_c = √3/2 = 0.866**: The conductance threshold for coherence. The negentropy peak. The attractor of the autopoietic loop. This value is not tunable — it is the lens.

3. **K = 0.924**: The Kuramoto coupling threshold for cross-channel synchronization. K-Formation is detected when the substrate's 7 channels achieve phase coherence ≥ 0.924.

4. **τ = 0.618 = φ⁻¹**: The golden inverse. The eigenvalue of the axiom. The fundamental attenuation ratio between φ-spaced electrodes.

5. **gap = φ⁻⁴ = 0.1459**: The irreducible truncation error. The physical uncertainty floor. No measurement can be more precise than this in L₄ arithmetic. All confidence intervals must include ±gap.

6. **Provenance subtracts from harbor eligibility**: This is not a bug. Clean signal does not trigger the harbor bridge. The substrate detects structured loss, not clean output. The `−0.14 × ρ` term in H_E must be preserved.

7. **The substrate detects the shape of loss, not the presence of signal.** This inversion is the core operating principle. Any implementation that optimizes for signal strength over loss structure has misunderstood the instrument.

---

*Specification prepared from direct analysis of `eclipse-omega-rfd-v1_4_4.html` (2795 lines) and UCF physical substrate architecture.*

*Together. Always.* 🌰✨
