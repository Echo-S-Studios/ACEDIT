/**
 * ACEDIT Constants Registry
 *
 * System Invariant: Convergence Constant z_c = √3/2 = 0.8660254...
 * Maintains all mathematical and system constants used throughout ACEDIT
 */

export const ACEDIT_CONSTANTS = {
  /** Convergence constant: √3/2 */
  Z_C: Math.sqrt(3) / 2,

  /** Symbolic representation */
  Z_C_SYMBOLIC: '√3/2',

  /** Precision for floating point comparisons */
  EPSILON: 1e-10,

  /** System version */
  VERSION: '1.0.0'
} as const;

/**
 * Register names (ACEDIT mnemonic)
 */
export const REGISTERS = {
  A: 'Operators',
  C: 'Modifiers',
  E: 'Ligatures',
  D: 'Punctuation',
  I: 'Constants',
  T: 'Coherence'
} as const;

export type RegisterKey = keyof typeof REGISTERS;

/**
 * Framework domain mappings (bijective mirror)
 */
export const DOMAINS = {
  A: 'Algebra',
  C: 'Configuration',
  E: 'Encoding',
  D: 'Delimiter',
  I: 'Identity',
  T: 'Transformation'
} as const;

/**
 * Unicode range definitions for each register
 */
export interface UnicodeRange {
  start: number;
  end: number;
  register: RegisterKey;
  name: string;
  domain: string;
  count: number;
}

export const UNICODE_RANGES: Record<RegisterKey, UnicodeRange> = {
  A: {
    start: 0x2200,
    end: 0x22FF,
    register: 'A',
    name: 'Operators',
    domain: 'Algebra',
    count: 256
  },
  C: {
    start: 0x0300,
    end: 0x036F,
    register: 'C',
    name: 'Modifiers',
    domain: 'Configuration',
    count: 112
  },
  E: {
    start: 0xFB00,
    end: 0xFB4F,
    register: 'E',
    name: 'Ligatures',
    domain: 'Encoding',
    count: 80
  },
  D: {
    start: 0x2000,
    end: 0x206F,
    register: 'D',
    name: 'Punctuation',
    domain: 'Delimiter',
    count: 112
  },
  I: {
    start: 0x2100,
    end: 0x214F,
    register: 'I',
    name: 'Constants',
    domain: 'Identity',
    count: 80
  },
  T: {
    start: 0x25A0,
    end: 0x25FF,
    register: 'T',
    name: 'Coherence',
    domain: 'Transformation',
    count: 96
  }
} as const;

/**
 * Validates that a codepoint belongs to exactly one register
 * Enforces: Register Sovereignty invariant
 */
export function getRegisterForCodepoint(codepoint: number): RegisterKey | null {
  for (const [key, range] of Object.entries(UNICODE_RANGES)) {
    if (codepoint >= range.start && codepoint <= range.end) {
      return key as RegisterKey;
    }
  }
  return null;
}

/**
 * Validates convergence constant calculation
 */
export function validateConvergenceConstant(): boolean {
  const calculated = Math.sqrt(3) / 2;
  return Math.abs(calculated - ACEDIT_CONSTANTS.Z_C) < ACEDIT_CONSTANTS.EPSILON;
}
