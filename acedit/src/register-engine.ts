/**
 * ACEDIT Register Engine
 *
 * System Invariant: Register Sovereignty - Each codepoint belongs to exactly one register
 * Manages register detection, validation, and codepoint mapping
 */

import { UNICODE_RANGES, REGISTERS, DOMAINS, RegisterKey } from './constants-registry.js';
import { validateCodepoint, isInRegister } from './range-validator.js';

export interface RegisterInfo {
  key: RegisterKey;
  name: string;
  domain: string;
  range: {
    start: number;
    end: number;
  };
  codepoint?: number;
}

/**
 * Gets complete register information for a codepoint
 */
export function getRegisterInfo(codepoint: number): RegisterInfo | null {
  const validation = validateCodepoint(codepoint);

  if (!validation.valid || !validation.register) {
    return null;
  }

  const register = validation.register;
  const range = UNICODE_RANGES[register];

  return {
    key: register,
    name: REGISTERS[register],
    domain: DOMAINS[register],
    range: {
      start: range.start,
      end: range.end
    },
    codepoint
  };
}

/**
 * Gets register information from a string character
 */
export function getRegisterFromChar(char: string): RegisterInfo | null {
  const codepoint = char.codePointAt(0);
  if (codepoint === undefined) {
    return null;
  }
  return getRegisterInfo(codepoint);
}

/**
 * Checks if a codepoint is in the Operators register (A)
 */
export function isOperator(codepoint: number): boolean {
  return isInRegister(codepoint, 'A');
}

/**
 * Checks if a codepoint is in the Modifiers register (C)
 */
export function isModifier(codepoint: number): boolean {
  return isInRegister(codepoint, 'C');
}

/**
 * Checks if a codepoint is in the Ligatures register (E)
 */
export function isLigature(codepoint: number): boolean {
  return isInRegister(codepoint, 'E');
}

/**
 * Checks if a codepoint is in the Punctuation register (D)
 */
export function isPunctuation(codepoint: number): boolean {
  return isInRegister(codepoint, 'D');
}

/**
 * Checks if a codepoint is in the Constants register (I)
 */
export function isConstant(codepoint: number): boolean {
  return isInRegister(codepoint, 'I');
}

/**
 * Checks if a codepoint is in the Coherence register (T)
 */
export function isCoherence(codepoint: number): boolean {
  return isInRegister(codepoint, 'T');
}

/**
 * Gets all codepoints in a register
 */
export function getRegisterCodepoints(register: RegisterKey): number[] {
  const range = UNICODE_RANGES[register];
  const codepoints: number[] = [];

  for (let cp = range.start; cp <= range.end; cp++) {
    codepoints.push(cp);
  }

  return codepoints;
}

/**
 * Converts codepoint to Unicode string representation
 */
export function codepointToUnicodeString(codepoint: number): string {
  return `U+${codepoint.toString(16).toUpperCase().padStart(4, '0')}`;
}

/**
 * Converts codepoint to actual character
 */
export function codepointToChar(codepoint: number): string {
  return String.fromCodePoint(codepoint);
}

/**
 * Gets register statistics
 */
export function getRegisterStats(register: RegisterKey): {
  register: RegisterKey;
  name: string;
  domain: string;
  totalCodepoints: number;
  rangeStart: string;
  rangeEnd: string;
} {
  const range = UNICODE_RANGES[register];

  return {
    register,
    name: REGISTERS[register],
    domain: DOMAINS[register],
    totalCodepoints: range.count,
    rangeStart: codepointToUnicodeString(range.start),
    rangeEnd: codepointToUnicodeString(range.end)
  };
}

/**
 * Gets all register statistics
 */
export function getAllRegisterStats() {
  const allRegisters: RegisterKey[] = ['A', 'C', 'E', 'D', 'I', 'T'];
  return allRegisters.map(reg => getRegisterStats(reg));
}
