// EO-RFD PHYSICAL SUBSTRATE FIRMWARE CONSTANTS
export const PHI       = (1 + Math.sqrt(5)) / 2;
export const TAU       = 1 / PHI;
export const SQRT3     = Math.sqrt(3);
export const SQRT3_HALF = SQRT3 / 2;
export const Z_C       = SQRT3_HALF;
export const K_FORM    = 0.924;
export const L4        = 7;
export const GAP       = Math.pow(PHI, -4);

export const THETA = {
  open:       { label: 'Θ_open',  apertureThreshold: 0.15, phaseThreshold: 0.4,
                capacityMult: 0.95, namingSensitivity: 0.02, policyStrictness: 0.1 },
  standard:   { label: 'Θ_std',   apertureThreshold: 0.30, phaseThreshold: 0.6,
                capacityMult: 0.80, namingSensitivity: 0.08, policyStrictness: 0.3 },
  restricted: { label: 'Θ_res',   apertureThreshold: 0.50, phaseThreshold: 0.8,
                capacityMult: 0.50, namingSensitivity: 0.25, policyStrictness: 0.6 }
};

export const ROUTING = {
  warningHarbor:    0.40,
  bufferHarbor:     0.62,
  harborHarbor:     0.82,
  warningRecapture: 0.45,
  antiRecapture:    0.66,
  bufferPersistence: 0.32,
  strongPersistence: 0.58,
  sigmaActive:      0.74
};

export const SIGMA_TAU = {
  obs:  0.85,
  name: 0.06,
  red:  0.02,
  coh:  0.60
};

export const TRI = {
  A: { x: 0, y: 0, label: 'A', fold: 'extension-entry' },
  B: { x: 1, y: 0, label: 'B', fold: 'closure-return' },
  C: { x: 0.5, y: SQRT3_HALF, label: 'C', fold: 'irrational-apex' }
};

export const DETECTOR_MODS = {
  theta: { open: 0.88, standard: 1.00, restricted: 1.16 },
  name:  { canonical: 0.92, safe: 1.00, invalid: 1.14 }
};

export const SIGMA_NEG = 1 / Math.pow(1 - Z_C, 2);
export const G0 = 77.5e-6;

export function clamp01(v) { return Math.max(0, Math.min(1, v)); }
export function fnv1a(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return (h >>> 0).toString(16).padStart(8, '0');
}
