/**
 * ACEDIT Modifier Stack
 *
 * Manages combining diacritical marks (Register C)
 * Ensures proper stacking order and rendering
 */

import { isModifier, codepointToChar } from './register-engine.js';
import { validateCodepoint } from './range-validator.js';

export interface ModifierStackResult {
  valid: boolean;
  output: string;
  message: string;
}

/**
 * Applies a stack of modifiers to a base character
 */
export function applyModifierStack(base: number, modifiers: number[]): ModifierStackResult {
  // Validate base
  const baseValidation = validateCodepoint(base);
  if (!baseValidation.valid) {
    return {
      valid: false,
      output: '',
      message: `Invalid base character: ${baseValidation.message}`
    };
  }

  // Validate all modifiers
  for (let i = 0; i < modifiers.length; i++) {
    const modValidation = validateCodepoint(modifiers[i]);
    if (!modValidation.valid) {
      return {
        valid: false,
        output: '',
        message: `Invalid modifier at position ${i}: ${modValidation.message}`
      };
    }

    if (!isModifier(modifiers[i])) {
      return {
        valid: false,
        output: '',
        message: `Codepoint at position ${i} is not a modifier (not in register C)`
      };
    }
  }

  // Build output string: base + modifiers in sequence
  let output = codepointToChar(base);
  for (const modifier of modifiers) {
    output += codepointToChar(modifier);
  }

  return {
    valid: true,
    output,
    message: `Applied ${modifiers.length} modifier(s) to base character`
  };
}

/**
 * Extracts modifiers from a string
 */
export function extractModifiers(input: string): {
  base: number | null;
  modifiers: number[];
} {
  const modifiers: number[] = [];
  let base: number | null = null;

  for (let i = 0; i < input.length; i++) {
    const codepoint = input.codePointAt(i);
    if (codepoint === undefined) continue;

    if (isModifier(codepoint)) {
      modifiers.push(codepoint);
    } else if (base === null) {
      base = codepoint;
    }

    // Skip surrogate pair if needed
    if (codepoint > 0xFFFF) {
      i++;
    }
  }

  return { base, modifiers };
}

/**
 * Normalizes modifier order (canonical ordering)
 */
export function normalizeModifierOrder(modifiers: number[]): number[] {
  // For Unicode combining marks, canonical ordering is by combining class
  // For ACEDIT, we maintain insertion order (simplest approach)
  // More sophisticated ordering can be added based on Unicode combining classes
  return [...modifiers];
}

/**
 * Validates that modifiers can be combined
 */
export function validateModifierCombination(modifiers: number[]): ModifierStackResult {
  if (modifiers.length === 0) {
    return {
      valid: true,
      output: '',
      message: 'Empty modifier stack (valid)'
    };
  }

  // Check all are valid modifiers
  for (let i = 0; i < modifiers.length; i++) {
    if (!isModifier(modifiers[i])) {
      return {
        valid: false,
        output: '',
        message: `Codepoint at position ${i} is not a modifier`
      };
    }
  }

  // Build output
  let output = '';
  for (const mod of modifiers) {
    output += codepointToChar(mod);
  }

  return {
    valid: true,
    output,
    message: `Valid modifier combination (${modifiers.length} modifiers)`
  };
}

/**
 * Gets the maximum recommended modifier stack depth
 */
export function getMaxStackDepth(): number {
  // Unicode typically supports up to 4-5 combining marks before rendering issues
  return 5;
}

/**
 * Checks if a modifier stack exceeds recommended depth
 */
export function isStackDepthExceeded(modifiers: number[]): boolean {
  return modifiers.length > getMaxStackDepth();
}
