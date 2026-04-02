/**
 * ACEDIT Range Validator
 *
 * System Invariant: Register Sovereignty - Each codepoint belongs to exactly one register
 * Validates Unicode codepoints against ACEDIT register ranges
 */

import { UNICODE_RANGES, RegisterKey, getRegisterForCodepoint } from './constants-registry.js';

export interface ValidationResult {
  valid: boolean;
  register?: RegisterKey;
  message?: string;
}

/**
 * Validates a single codepoint
 * Enforces: Register Sovereignty invariant
 */
export function validateCodepoint(codepoint: number): ValidationResult {
  if (!Number.isInteger(codepoint) || codepoint < 0 || codepoint > 0x10FFFF) {
    return {
      valid: false,
      message: `Invalid codepoint: ${codepoint.toString(16)} (must be 0x0000-0x10FFFF)`
    };
  }

  const register = getRegisterForCodepoint(codepoint);

  if (!register) {
    return {
      valid: false,
      message: `Codepoint U+${codepoint.toString(16).toUpperCase().padStart(4, '0')} not in any ACEDIT register`
    };
  }

  return {
    valid: true,
    register,
    message: `Valid codepoint in register ${register} (${UNICODE_RANGES[register].name})`
  };
}

/**
 * Validates a string contains only ACEDIT-valid codepoints
 */
export function validateString(input: string): ValidationResult {
  for (let i = 0; i < input.length; i++) {
    const codepoint = input.codePointAt(i);
    if (codepoint === undefined) {
      return {
        valid: false,
        message: `Invalid character at position ${i}`
      };
    }

    const result = validateCodepoint(codepoint);
    if (!result.valid) {
      return {
        valid: false,
        message: `${result.message} at position ${i}`
      };
    }

    // Skip surrogate pair if needed
    if (codepoint > 0xFFFF) {
      i++;
    }
  }

  return {
    valid: true,
    message: 'All codepoints valid'
  };
}

/**
 * Checks if a codepoint is in a specific register
 */
export function isInRegister(codepoint: number, register: RegisterKey): boolean {
  const range = UNICODE_RANGES[register];
  return codepoint >= range.start && codepoint <= range.end;
}

/**
 * Gets all registers that a string uses
 */
export function getStringRegisters(input: string): Set<RegisterKey> {
  const registers = new Set<RegisterKey>();

  for (let i = 0; i < input.length; i++) {
    const codepoint = input.codePointAt(i);
    if (codepoint !== undefined) {
      const register = getRegisterForCodepoint(codepoint);
      if (register) {
        registers.add(register);
      }

      // Skip surrogate pair if needed
      if (codepoint > 0xFFFF) {
        i++;
      }
    }
  }

  return registers;
}

/**
 * Validates that no register overlap exists (system integrity check)
 */
export function validateNoRegisterOverlap(): ValidationResult {
  const ranges = Object.values(UNICODE_RANGES);

  for (let i = 0; i < ranges.length; i++) {
    for (let j = i + 1; j < ranges.length; j++) {
      const a = ranges[i];
      const b = ranges[j];

      // Check for overlap
      if (!(a.end < b.start || b.end < a.start)) {
        return {
          valid: false,
          message: `Register overlap detected: ${a.register} and ${b.register}`
        };
      }
    }
  }

  return {
    valid: true,
    message: 'No register overlaps detected - Register Sovereignty maintained'
  };
}
