/**
 * ACEDIT Coherence Validator
 *
 * System Invariant: Validates visual coherence using Register T (Transformation)
 * Uses geometric shapes to verify rendering and transformation correctness
 */

import { isCoherence, codepointToChar, codepointToUnicodeString } from './register-engine.js';
import { validateCodepoint } from './range-validator.js';
import { ACEDIT_CONSTANTS } from './constants-registry.js';

export interface CoherenceResult {
  valid: boolean;
  score: number;
  message: string;
}

/**
 * Geometric shape mappings (U+25A0-U+25FF)
 */
const SHAPE_MAPPINGS: Record<number, { name: string; type: string }> = {
  0x25A0: { name: 'Black Square', type: 'square' },
  0x25A1: { name: 'White Square', type: 'square' },
  0x25A2: { name: 'White Square with Rounded Corners', type: 'square' },
  0x25AA: { name: 'Black Small Square', type: 'square' },
  0x25AB: { name: 'White Small Square', type: 'square' },

  0x25B2: { name: 'Black Up-Pointing Triangle', type: 'triangle' },
  0x25B3: { name: 'White Up-Pointing Triangle', type: 'triangle' },
  0x25B4: { name: 'Black Up-Pointing Small Triangle', type: 'triangle' },
  0x25B5: { name: 'White Up-Pointing Small Triangle', type: 'triangle' },
  0x25B6: { name: 'Black Right-Pointing Triangle', type: 'triangle' },
  0x25B7: { name: 'White Right-Pointing Triangle', type: 'triangle' },
  0x25BC: { name: 'Black Down-Pointing Triangle', type: 'triangle' },
  0x25BD: { name: 'White Down-Pointing Triangle', type: 'triangle' },
  0x25C0: { name: 'Black Left-Pointing Triangle', type: 'triangle' },
  0x25C1: { name: 'White Left-Pointing Triangle', type: 'triangle' },

  0x25CB: { name: 'White Circle', type: 'circle' },
  0x25CF: { name: 'Black Circle', type: 'circle' },
  0x25D8: { name: 'Inverse Bullet', type: 'circle' },
  0x25D9: { name: 'Inverse White Circle', type: 'circle' },

  0x25C6: { name: 'Black Diamond', type: 'diamond' },
  0x25C7: { name: 'White Diamond', type: 'diamond' },
};

/**
 * Validates a coherence marker (geometric shape)
 */
export function validateCoherenceMarker(codepoint: number): CoherenceResult {
  const validation = validateCodepoint(codepoint);

  if (!validation.valid) {
    return {
      valid: false,
      score: 0,
      message: `Invalid codepoint: ${validation.message}`
    };
  }

  if (!isCoherence(codepoint)) {
    return {
      valid: false,
      score: 0,
      message: `Codepoint ${codepointToUnicodeString(codepoint)} is not a coherence marker (not in register T)`
    };
  }

  const shape = SHAPE_MAPPINGS[codepoint];

  return {
    valid: true,
    score: 1.0,
    message: shape ? `Valid coherence marker: ${shape.name}` : 'Valid coherence marker (unknown shape)'
  };
}

/**
 * Validates visual coherence of a string using the convergence constant
 *
 * The coherence score is calculated based on:
 * - Presence of coherence markers (geometric shapes)
 * - Ratio of coherence markers to total characters
 * - Convergence towards z_c = 3/2
 */
export function validateStringCoherence(input: string): CoherenceResult {
  let totalChars = 0;
  let coherenceMarkers = 0;

  for (let i = 0; i < input.length; i++) {
    const codepoint = input.codePointAt(i);
    if (codepoint === undefined) continue;

    totalChars++;

    if (isCoherence(codepoint)) {
      coherenceMarkers++;
    }

    // Skip surrogate pair if needed
    if (codepoint > 0xFFFF) {
      i++;
    }
  }

  if (totalChars === 0) {
    return {
      valid: true,
      score: 1.0,
      message: 'Empty string has perfect coherence'
    };
  }

  // Calculate coherence ratio
  const ratio = coherenceMarkers / totalChars;

  // Coherence score: how close the ratio is to z_c
  // Perfect coherence = ratio of 3/2
  const targetRatio = ACEDIT_CONSTANTS.Z_C;
  const difference = Math.abs(ratio - targetRatio);
  const score = Math.max(0, 1 - difference);

  return {
    valid: true,
    score,
    message: `Coherence score: ${score.toFixed(4)} (${coherenceMarkers}/${totalChars} markers, target ratio: ${targetRatio.toFixed(4)})`
  };
}

/**
 * Calculates the optimal number of coherence markers for a given text length
 */
export function getOptimalMarkerCount(textLength: number): number {
  return Math.round(textLength * ACEDIT_CONSTANTS.Z_C);
}

/**
 * Suggests coherence markers to add to achieve optimal coherence
 */
export function suggestCoherenceMarkers(input: string): CoherenceResult {
  let totalChars = 0;

  for (let i = 0; i < input.length; i++) {
    const codepoint = input.codePointAt(i);
    if (codepoint === undefined) continue;

    totalChars++;

    if (codepoint > 0xFFFF) {
      i++;
    }
  }

  const optimal = getOptimalMarkerCount(totalChars);
  const suggested = codepointToChar(0x25B2); // Black Up-Pointing Triangle

  return {
    valid: true,
    score: ACEDIT_CONSTANTS.Z_C,
    message: `For ${totalChars} characters, add ${optimal} coherence markers (suggestion: ${suggested})`
  };
}

/**
 * Gets all available coherence markers
 */
export function getAllCoherenceMarkers(): Array<{
  codepoint: number;
  unicode: string;
  character: string;
  name: string;
  type: string;
}> {
  return Object.entries(SHAPE_MAPPINGS).map(([cp, info]) => {
    const codepoint = parseInt(cp, 10);
    return {
      codepoint,
      unicode: codepointToUnicodeString(codepoint),
      character: codepointToChar(codepoint),
      name: info.name,
      type: info.type
    };
  });
}

/**
 * Validates that coherence is maintained throughout a transformation
 */
export function validateTransformationCoherence(input: string, output: string): CoherenceResult {
  const inputCoherence = validateStringCoherence(input);
  const outputCoherence = validateStringCoherence(output);

  const scoreDifference = Math.abs(inputCoherence.score - outputCoherence.score);

  return {
    valid: scoreDifference < 0.1, // Allow 10% variance
    score: Math.min(inputCoherence.score, outputCoherence.score),
    message: `Transformation coherence: input=${inputCoherence.score.toFixed(4)}, output=${outputCoherence.score.toFixed(4)}, difference=${scoreDifference.toFixed(4)}`
  };
}
