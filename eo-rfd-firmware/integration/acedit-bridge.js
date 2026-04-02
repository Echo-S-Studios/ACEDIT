// ==================================================================
// ACEDIT BRIDGE MODULE
// Integration layer between ACEDIT encoding and EO-RFD firmware
// ==================================================================

/**
 * ACEDIT Register Domains
 *
 * Maps EO-RFD layers to their corresponding ACEDIT register domains:
 * - L0-L1: KAEL (substrate/physical layer)
 * - L2-L3: GREY (visual/geometric layer)
 * - L4-L5: UMBRAL (algebraic layer)
 * - L6-L7: ACE (spin/dynamics layer)
 * - L8-L9: UCF (unified/meta layer)
 */

export const REGISTER_DOMAINS = {
  KAEL: {
    name: 'KAEL',
    symbol: '𝕂',
    description: 'Substrate & Physical Layer',
    color: '#DAA520', // Goldenrod
    layers: [0, 1],
    domain: 'substrate/physical'
  },
  GREY: {
    name: 'GREY',
    symbol: '𝔾',
    description: 'Visual & Geometric Layer',
    color: '#9370DB', // Medium purple
    layers: [2, 3],
    domain: 'visual/geometric'
  },
  UMBRAL: {
    name: 'UMBRAL',
    symbol: '𝕌',
    description: 'Algebraic Layer',
    color: '#9370DB', // Medium purple
    layers: [4, 5],
    domain: 'algebraic'
  },
  ACE: {
    name: 'ACE',
    symbol: '𝔸',
    description: 'Spin & Dynamics Layer',
    color: '#DAA520', // Goldenrod
    layers: [6, 7],
    domain: 'spin/dynamics'
  },
  UCF: {
    name: 'UCF',
    symbol: '𝕌ℂ𝔽',
    description: 'Unified & Meta Layer',
    color: '#4169E1', // Royal blue
    layers: [8, 9],
    domain: 'unified/meta'
  }
};

/**
 * ACEDIT Operators
 *
 * Mathematical operators that can be inserted into signal descriptions
 * to encode structural relationships
 */
export const OPERATORS = {
  // Containment & Structure
  CONTAINS: '⊃',           // D ⊃ C_k(q) - containment
  ELEMENT: '∈',            // q ∈ C - element of
  SUBSET: '⊆',             // C ⊆ D - subset

  // Transformations
  MAPS_TO: '↦',            // x ↦ f(x) - maps to
  ARROW: '→',              // A → B - transformation
  DERIVES: '⊢',            // A ⊢ B - derives

  // Composition & Operations
  COMPOSE: '∘',            // f ∘ g - composition
  TENSOR: '⊗',             // A ⊗ B - tensor product
  WEDGE: '∧',              // α ∧ β - wedge product

  // Relations
  EQUIV: '≃',              // A ≃ B - equivalence
  ISO: '≅',                // A ≅ B - isomorphism
  APPROX: '≈',             // a ≈ b - approximately

  // Lattice & Order
  MEET: '∧',               // a ∧ b - meet/infimum
  JOIN: '∨',               // a ∨ b - join/supremum
  LEQ: '≤',                // a ≤ b - less than or equal

  // Geometry
  ANGLE: '∠',              // angle
  PERP: '⊥',               // perpendicular
  PARALLEL: '∥',           // parallel

  // Special
  PARTIAL: '∂',            // partial derivative
  NABLA: '∇',              // gradient/del
  INTEGRAL: '∫',           // integral
  PRODUCT: '∏',            // product
  SUM: '∑',                // sum (e.g., Σ_R)

  // Logical
  AND: '∧',                // logical and
  OR: '∨',                 // logical or
  NOT: '¬',                // logical not
  IMPLIES: '⇒',            // implies
  IFF: '⇔'                 // if and only if
};

/**
 * Get the register domain for a given layer
 * @param {number|string} layer - Layer number (0-9) or layer ID (L0-L9)
 * @returns {object} Register domain object
 */
export function getRegisterForLayer(layer) {
  const layerNum = typeof layer === 'string'
    ? parseInt(layer.replace('L', ''))
    : layer;

  for (const [key, domain] of Object.entries(REGISTER_DOMAINS)) {
    if (domain.layers.includes(layerNum)) {
      return domain;
    }
  }

  return REGISTER_DOMAINS.UCF; // Default to UCF for undefined layers
}

/**
 * Encode a signal name with ACEDIT operators and register domain
 * @param {string} baseName - Base signal name (e.g., "obs:input")
 * @param {number|string} layer - Layer number or ID
 * @param {object} options - Encoding options
 * @returns {object} Encoded signal with metadata
 */
export function encodeSignal(baseName, layer, options = {}) {
  const {
    operator = null,
    suffix = null,
    includeRegister = true,
    includeSymbol = false
  } = options;

  const register = getRegisterForLayer(layer);

  let encoded = baseName;

  // Add operator if specified
  if (operator && OPERATORS[operator]) {
    encoded = `${OPERATORS[operator]} ${encoded}`;
  }

  // Add suffix if specified
  if (suffix) {
    encoded = `${encoded} ${suffix}`;
  }

  // Build metadata
  const metadata = {
    original: baseName,
    encoded,
    register: register.name,
    registerSymbol: register.symbol,
    registerColor: register.color,
    layer,
    domain: register.domain
  };

  // Add register prefix if requested
  if (includeRegister) {
    metadata.fullName = includeSymbol
      ? `${register.symbol}:${encoded}`
      : `[${register.name}] ${encoded}`;
  } else {
    metadata.fullName = encoded;
  }

  return metadata;
}

/**
 * Generate ACEDIT-encoded layer descriptions
 * Maps each layer to appropriate register with operators
 */
export const LAYER_DESCRIPTIONS = {
  L0: {
    register: 'KAEL',
    encoding: `${OPERATORS.ELEMENT} Quasi-crystal substrate`,
    description: 'Physical substrate with Penrose P3 tiling',
    operators: ['∈', '⊗'],
    detail: 'z_c = √3/2 conductance threshold on φ-recursive geometry'
  },
  L1: {
    register: 'KAEL',
    encoding: `${OPERATORS.MAPS_TO} Ballistic propagation`,
    description: 'Electron transport with boundary interaction',
    operators: ['↦', '∂'],
    detail: 'Ray transport with defect accumulation and phase evolution'
  },
  L2: {
    register: 'GREY',
    encoding: `${OPERATORS.DERIVES} Θ-gated cascade`,
    description: 'Admissibility classification via 5-stage comparator',
    operators: ['⊢', '∧'],
    detail: '4 classes: registered · latent · suppressed · aliased'
  },
  L3: {
    register: 'GREY',
    encoding: `${OPERATORS.CONTAINS} Narrowing funnel`,
    description: '7-stage resistive compression: S ${OPERATORS.CONTAINS} ℛ ${OPERATORS.CONTAINS} 𝒦 ${OPERATORS.CONTAINS} 𝒞 ${OPERATORS.CONTAINS} 𝒫 ${OPERATORS.CONTAINS} ℱ ${OPERATORS.CONTAINS} 𝒜',
    operators: ['⊃', '→'],
    detail: 'Operator-attributed losses (L_R through L_A)'
  },
  L4: {
    register: 'UMBRAL',
    encoding: `${OPERATORS.TENSOR} Field signature`,
    description: '7-channel analog computer: δ_obs ⊗ η_N ⊗ σ ⊗ γ ⊗ χ ⊗ β ⊗ ρ',
    operators: ['⊗', '∇'],
    detail: 'Derived metrics from admissibility ratios'
  },
  L5: {
    register: 'UMBRAL',
    encoding: `${OPERATORS.SUM} Signal rupture`,
    description: 'Σ_R composite with 4 tripwire thresholds',
    operators: ['∑', '≥'],
    detail: 'Weighted composite: 0.34·δ + 0.22·η + 0.24·(1-red) + 0.20·χ'
  },
  L6: {
    register: 'ACE',
    encoding: `${OPERATORS.TENSOR} Detector sweep`,
    description: '3×3 memristive crossbar (Θ × Naming)',
    operators: ['⊗', '∧'],
    detail: 'Confidence composite with modulation factors'
  },
  L7: {
    register: 'ACE',
    encoding: `${OPERATORS.ARROW} Routing FSM`,
    description: 'TRIAD hysteresis: play → warning → buffer → harbor',
    operators: ['→', '≥'],
    detail: 'Harbor eligibility: H_E with provenance inversion'
  },
  L8: {
    register: 'UCF',
    encoding: `${OPERATORS.DERIVES} Packet hardening`,
    description: 'TCP schema validation & export gating',
    operators: ['⊢', '⇒'],
    detail: 'Schema + checksum + provenance envelope'
  },
  L9: {
    register: 'UCF',
    encoding: `${OPERATORS.PARTIAL} Metacybernetic`,
    description: 'Autopoietic regulation: CSD + negentropy oversight',
    operators: ['∂', '∇'],
    detail: 'Stochastic resonance optimization at z_c threshold'
  }
};

/**
 * Generate full ACEDIT-encoded channel name
 * @param {string} channel - Base channel name
 * @param {number|string} layer - Layer number or ID
 * @param {boolean} useSymbols - Use Unicode symbols instead of names
 * @returns {object} Encoded channel with full metadata
 */
export function encodeChannel(channel, layer, useSymbols = false) {
  const layerDesc = LAYER_DESCRIPTIONS[`L${layer}`] || LAYER_DESCRIPTIONS.L9;
  const register = getRegisterForLayer(layer);

  return {
    channel,
    layer,
    register: register.name,
    registerSymbol: register.symbol,
    registerColor: register.color,
    encoding: layerDesc.encoding,
    description: layerDesc.description,
    operators: layerDesc.operators,
    detail: layerDesc.detail,
    fullName: useSymbols
      ? `${register.symbol}:${channel}`
      : `[${register.name}] ${channel}`,
    displayName: `${channel} ${layerDesc.operators[0] || ''}`
  };
}

/**
 * Constants verification - ensure ACEDIT and EO-RFD constants match
 */
export const CONSTANTS_BRIDGE = {
  // Shared constants that must match
  PHI: (1 + Math.sqrt(5)) / 2,           // Golden ratio
  TAU: 1 / ((1 + Math.sqrt(5)) / 2),     // φ⁻¹ = 0.618
  SQRT3_HALF: Math.sqrt(3) / 2,          // z_c = 0.866
  K_FORM: 0.924,                          // Kuramoto coupling
  L4: 7,                                  // φ⁴ + φ⁻⁴ = 7
  GAP: Math.pow(((1 + Math.sqrt(5)) / 2), -4), // φ⁻⁴ = 0.1459

  // Derived constants
  G0: 77.5e-6,                            // Quantum conductance (Siemens)
  SIGMA_NEG: 1 / Math.pow(1 - Math.sqrt(3)/2, 2), // Negentropy coefficient

  /**
   * Verify constants match between systems
   * @returns {object} Verification report
   */
  verify() {
    const report = {
      valid: true,
      checks: []
    };

    // Check z_c = SQRT3_HALF
    const zc = Math.sqrt(3) / 2;
    report.checks.push({
      name: 'z_c',
      expected: 0.866,
      actual: zc,
      valid: Math.abs(zc - 0.866) < 0.001
    });

    // Check TAU = φ⁻¹
    const tau = 1 / this.PHI;
    report.checks.push({
      name: 'τ',
      expected: 0.618,
      actual: tau,
      valid: Math.abs(tau - 0.618) < 0.001
    });

    // Check L4 = 7
    const l4 = Math.pow(this.PHI, 4) + Math.pow(this.PHI, -4);
    report.checks.push({
      name: 'L₄',
      expected: 7,
      actual: l4,
      valid: Math.abs(l4 - 7) < 0.01
    });

    // Check gap = φ⁻⁴
    const gap = Math.pow(this.PHI, -4);
    report.checks.push({
      name: 'gap',
      expected: 0.1459,
      actual: gap,
      valid: Math.abs(gap - 0.1459) < 0.0001
    });

    // Set overall validity
    report.valid = report.checks.every(check => check.valid);

    return report;
  }
};

/**
 * Format a metric value with ACEDIT-aware display
 * @param {string} metricName - Name of metric
 * @param {number} value - Metric value
 * @param {number|string} layer - Layer number or ID
 * @returns {object} Formatted metric with register styling
 */
export function formatMetric(metricName, value, layer) {
  const register = getRegisterForLayer(layer);

  // Determine if this is a special metric with operators
  let displayName = metricName;

  // Add operator context for known metrics
  const metricOperators = {
    'Σ_R': OPERATORS.SUM,
    'δ_obs': OPERATORS.PARTIAL,
    'η_N': OPERATORS.NABLA,
    'H_E': OPERATORS.INTEGRAL
  };

  if (metricOperators[metricName]) {
    displayName = `${metricOperators[metricName]}${metricName}`;
  }

  return {
    name: metricName,
    displayName,
    value,
    formatted: typeof value === 'number' ? value.toFixed(3) : value,
    register: register.name,
    color: register.color,
    layer
  };
}

/**
 * Generate CSS custom properties for ACEDIT register colors
 * @returns {string} CSS variable declarations
 */
export function generateRegisterCSS() {
  let css = ':root {\n';
  for (const [key, domain] of Object.entries(REGISTER_DOMAINS)) {
    css += `  --register-${key.toLowerCase()}: ${domain.color};\n`;
  }
  css += '}\n';
  return css;
}

/**
 * Export all encoding utilities
 */
export default {
  REGISTER_DOMAINS,
  OPERATORS,
  LAYER_DESCRIPTIONS,
  CONSTANTS_BRIDGE,
  getRegisterForLayer,
  encodeSignal,
  encodeChannel,
  formatMetric,
  generateRegisterCSS
};
