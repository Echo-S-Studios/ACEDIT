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
export { loadCore, validateCore, initializeCore, type ACEDITCore } from './core-loader.js';
export { ACEDIT_CONSTANTS, REGISTERS, DOMAINS, UNICODE_RANGES, type RegisterKey, type UnicodeRange, getRegisterForCodepoint, validateConvergenceConstant } from './constants-registry.js';
export { validateCodepoint, validateString, isInRegister, getStringRegisters, validateNoRegisterOverlap, type ValidationResult } from './range-validator.js';
export { getRegisterInfo, getRegisterFromChar, isOperator, isModifier, isLigature, isPunctuation, isConstant, isCoherence, getRegisterCodepoints, codepointToUnicodeString, codepointToChar, getRegisterStats, getAllRegisterStats, type RegisterInfo } from './register-engine.js';
export { composeOperators, applyModifier, validateCompositionChain, isIdentityComposition, getInverse, type CompositionResult } from './operator-algebra.js';
export { applyModifierStack, extractModifiers, normalizeModifierOrder, validateModifierCombination, getMaxStackDepth, isStackDepthExceeded, type ModifierStackResult } from './modifier-stack.js';
export { resolveLigature, createLigature, resolveAllLigatures, createAllLigatures, getAllLigatureMappings, type LigatureResult } from './ligature-resolver.js';
export { toASCII, getPunctuationName, stringToASCII, getAllPunctuationMappings, validatePunctuationUsage, type PunctuationResult } from './punct-mapper.js';
export { validateCoherenceMarker, validateStringCoherence, getOptimalMarkerCount, suggestCoherenceMarkers, getAllCoherenceMarkers, validateTransformationCoherence, type CoherenceResult } from './coherence-validator.js';
export { transcodeCodepoint, transcodeString, transcodeWithCoherenceValidation, detectAndSuggestTranscode, batchTranscode, type TranscodeResult } from './transcode-engine.js';
/**
 * ACEDIT System Initialization and Validation
 */
export declare function initializeACEDIT(): {
    valid: boolean;
    version: string;
    convergenceConstant: number;
    errors: string[];
};
//# sourceMappingURL=index.d.ts.map