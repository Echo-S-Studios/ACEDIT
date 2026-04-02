/**
 * ACEDIT - Typographic Firmware Layer
 *
 * A zero-infrastructure Unicode encoding system mapping 6 registers to 6 framework domains
 *
 * System Invariants:
 * 1. Bijective Mirror: 6 registers � 6 framework domains
 * 2. Algebraic Closure: All compositions produce valid ACEDIT output
 * 3. Zero Infrastructure: No custom fonts, CSS, or build tools for output
 * 4. Convergence Constant: z_c = 3/2 = 0.8660254...
 * 5. Register Sovereignty: Each codepoint belongs to exactly one register
 * 6. Idempotent Passthrough: No double-encoding
 */

// Core system
export {
  loadCore,
  validateCore,
  initializeCore,
  type ACEDITCore
} from './core-loader.js';

// Constants and configuration
export {
  ACEDIT_CONSTANTS,
  REGISTERS,
  DOMAINS,
  UNICODE_RANGES,
  type RegisterKey,
  type UnicodeRange,
  getRegisterForCodepoint,
  validateConvergenceConstant
} from './constants-registry.js';

// Range validation
export {
  validateCodepoint,
  validateString,
  isInRegister,
  getStringRegisters,
  validateNoRegisterOverlap,
  type ValidationResult
} from './range-validator.js';

// Register engine
export {
  getRegisterInfo,
  getRegisterFromChar,
  isOperator,
  isModifier,
  isLigature,
  isPunctuation,
  isConstant,
  isCoherence,
  getRegisterCodepoints,
  codepointToUnicodeString,
  codepointToChar,
  getRegisterStats,
  getAllRegisterStats,
  type RegisterInfo
} from './register-engine.js';

// Operator algebra
export {
  composeOperators,
  applyModifier,
  validateCompositionChain,
  isIdentityComposition,
  getInverse,
  type CompositionResult
} from './operator-algebra.js';

// Modifier stack
export {
  applyModifierStack,
  extractModifiers,
  normalizeModifierOrder,
  validateModifierCombination,
  getMaxStackDepth,
  isStackDepthExceeded,
  type ModifierStackResult
} from './modifier-stack.js';

// Ligature resolver
export {
  resolveLigature,
  createLigature,
  resolveAllLigatures,
  createAllLigatures,
  getAllLigatureMappings,
  type LigatureResult
} from './ligature-resolver.js';

// Punctuation mapper
export {
  toASCII,
  getPunctuationName,
  stringToASCII,
  getAllPunctuationMappings,
  validatePunctuationUsage,
  type PunctuationResult
} from './punct-mapper.js';

// Coherence validator
export {
  validateCoherenceMarker,
  validateStringCoherence,
  getOptimalMarkerCount,
  suggestCoherenceMarkers,
  getAllCoherenceMarkers,
  validateTransformationCoherence,
  type CoherenceResult
} from './coherence-validator.js';

// Transcode engine
export {
  transcodeCodepoint,
  transcodeString,
  transcodeWithCoherenceValidation,
  detectAndSuggestTranscode,
  batchTranscode,
  type TranscodeResult
} from './transcode-engine.js';

// Import functions for initialization
import { initializeCore } from './core-loader.js';
import { ACEDIT_CONSTANTS, validateConvergenceConstant } from './constants-registry.js';
import { validateNoRegisterOverlap } from './range-validator.js';

/**
 * ACEDIT System Initialization and Validation
 */
export function initializeACEDIT(): {
  valid: boolean;
  version: string;
  convergenceConstant: number;
  errors: string[];
} {
  try {
    // Initialize core
    const core = initializeCore();

    // Validate register sovereignty
    const registerCheck = validateNoRegisterOverlap();
    if (!registerCheck.valid) {
      return {
        valid: false,
        version: core.metadata.version,
        convergenceConstant: ACEDIT_CONSTANTS.Z_C,
        errors: [registerCheck.message || 'Register overlap detected']
      };
    }

    // Validate convergence constant
    if (!validateConvergenceConstant()) {
      return {
        valid: false,
        version: core.metadata.version,
        convergenceConstant: ACEDIT_CONSTANTS.Z_C,
        errors: ['Convergence constant validation failed']
      };
    }

    return {
      valid: true,
      version: core.metadata.version,
      convergenceConstant: ACEDIT_CONSTANTS.Z_C,
      errors: []
    };
  } catch (error) {
    return {
      valid: false,
      version: '1.0.0',
      convergenceConstant: ACEDIT_CONSTANTS.Z_C,
      errors: [String(error)]
    };
  }
}
