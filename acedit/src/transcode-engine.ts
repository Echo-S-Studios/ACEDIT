/**
 * ACEDIT Transcode Engine
 *
 * System Invariant: Idempotent Passthrough - No double-encoding
 * Handles transcoding between ACEDIT registers while maintaining all invariants
 */

import { getRegisterInfo, codepointToChar } from './register-engine.js';
import { validateCodepoint, getStringRegisters } from './range-validator.js';
import { validateStringCoherence } from './coherence-validator.js';
import { RegisterKey } from './constants-registry.js';

export interface TranscodeResult {
  valid: boolean;
  output: string;
  sourceRegister?: RegisterKey;
  targetRegister?: RegisterKey;
  message: string;
  isPassthrough: boolean;
}

/**
 * Transcodes a single codepoint to a target register
 * Enforces: Idempotent Passthrough invariant
 */
export function transcodeCodepoint(
  codepoint: number,
  targetRegister: RegisterKey
): TranscodeResult {
  const validation = validateCodepoint(codepoint);

  if (!validation.valid || !validation.register) {
    return {
      valid: false,
      output: '',
      message: `Invalid codepoint: ${validation.message}`,
      isPassthrough: false
    };
  }

  const sourceRegister = validation.register;

  // Idempotent Passthrough: If already in target register, return unchanged
  if (sourceRegister === targetRegister) {
    return {
      valid: true,
      output: codepointToChar(codepoint),
      sourceRegister,
      targetRegister,
      message: 'Passthrough: codepoint already in target register',
      isPassthrough: true
    };
  }

  // For basic implementation, transcoding maintains the character
  // Advanced transcoding rules can be added based on semantic mappings
  return {
    valid: true,
    output: codepointToChar(codepoint),
    sourceRegister,
    targetRegister,
    message: `Transcoded from register ${sourceRegister} to ${targetRegister}`,
    isPassthrough: false
  };
}

/**
 * Transcodes a string to use codepoints from a specific register
 */
export function transcodeString(
  input: string,
  targetRegister: RegisterKey
): TranscodeResult {
  if (input.length === 0) {
    return {
      valid: true,
      output: '',
      targetRegister,
      message: 'Empty input string',
      isPassthrough: true
    };
  }

  // Check if input is already entirely in the target register
  const registers = getStringRegisters(input);

  if (registers.size === 1 && registers.has(targetRegister)) {
    return {
      valid: true,
      output: input,
      sourceRegister: targetRegister,
      targetRegister,
      message: 'Passthrough: entire string already in target register',
      isPassthrough: true
    };
  }

  // Transcode each codepoint
  let output = '';
  let hadErrors = false;

  for (let i = 0; i < input.length; i++) {
    const codepoint = input.codePointAt(i);
    if (codepoint === undefined) continue;

    const result = transcodeCodepoint(codepoint, targetRegister);
    if (!result.valid) {
      hadErrors = true;
      break;
    }

    output += result.output;

    // Skip surrogate pair if needed
    if (codepoint > 0xFFFF) {
      i++;
    }
  }

  return {
    valid: !hadErrors,
    output: hadErrors ? input : output,
    targetRegister,
    message: hadErrors
      ? 'Transcoding failed, returned original input'
      : `Transcoded string to register ${targetRegister}`,
    isPassthrough: false
  };
}

/**
 * Validates that transcoding maintains coherence
 */
export function transcodeWithCoherenceValidation(
  input: string,
  targetRegister: RegisterKey
): TranscodeResult {
  const inputCoherence = validateStringCoherence(input);
  const transcodeResult = transcodeString(input, targetRegister);

  if (!transcodeResult.valid) {
    return transcodeResult;
  }

  const outputCoherence = validateStringCoherence(transcodeResult.output);

  // Check coherence is maintained (within tolerance)
  const coherenceDifference = Math.abs(inputCoherence.score - outputCoherence.score);

  if (coherenceDifference > 0.1) {
    return {
      valid: false,
      output: input,
      targetRegister,
      message: `Coherence not maintained: difference=${coherenceDifference.toFixed(4)}`,
      isPassthrough: false
    };
  }

  return {
    ...transcodeResult,
    message: `${transcodeResult.message} (coherence maintained: ${outputCoherence.score.toFixed(4)})`
  };
}

/**
 * Detects the source register and suggests optimal target register
 */
export function detectAndSuggestTranscode(input: string): {
  sourceRegisters: RegisterKey[];
  suggestedTarget: RegisterKey | null;
  message: string;
} {
  const registers = getStringRegisters(input);
  const sourceRegisters = Array.from(registers);

  if (sourceRegisters.length === 0) {
    return {
      sourceRegisters: [],
      suggestedTarget: null,
      message: 'No ACEDIT registers detected in input'
    };
  }

  if (sourceRegisters.length === 1) {
    return {
      sourceRegisters,
      suggestedTarget: sourceRegisters[0],
      message: `Input is homogeneous (register ${sourceRegisters[0]}), no transcoding needed`
    };
  }

  // For mixed content, suggest the dominant register
  const registerCounts = new Map<RegisterKey, number>();

  for (let i = 0; i < input.length; i++) {
    const codepoint = input.codePointAt(i);
    if (codepoint === undefined) continue;

    const info = getRegisterInfo(codepoint);
    if (info) {
      registerCounts.set(info.key, (registerCounts.get(info.key) || 0) + 1);
    }

    if (codepoint > 0xFFFF) {
      i++;
    }
  }

  let maxCount = 0;
  let dominantRegister: RegisterKey | null = null;

  for (const [register, count] of registerCounts.entries()) {
    if (count > maxCount) {
      maxCount = count;
      dominantRegister = register;
    }
  }

  return {
    sourceRegisters,
    suggestedTarget: dominantRegister,
    message: `Input uses ${sourceRegisters.length} registers, suggested target: ${dominantRegister}`
  };
}

/**
 * Batch transcode: converts all codepoints to their register equivalents
 */
export function batchTranscode(
  inputs: string[],
  targetRegister: RegisterKey
): Array<TranscodeResult> {
  return inputs.map(input => transcodeString(input, targetRegister));
}
