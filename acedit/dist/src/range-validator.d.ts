/**
 * ACEDIT Range Validator
 *
 * System Invariant: Register Sovereignty - Each codepoint belongs to exactly one register
 * Validates Unicode codepoints against ACEDIT register ranges
 */
import { RegisterKey } from './constants-registry.js';
export interface ValidationResult {
    valid: boolean;
    register?: RegisterKey;
    message?: string;
}
/**
 * Validates a single codepoint
 * Enforces: Register Sovereignty invariant
 */
export declare function validateCodepoint(codepoint: number): ValidationResult;
/**
 * Validates a string contains only ACEDIT-valid codepoints
 */
export declare function validateString(input: string): ValidationResult;
/**
 * Checks if a codepoint is in a specific register
 */
export declare function isInRegister(codepoint: number, register: RegisterKey): boolean;
/**
 * Gets all registers that a string uses
 */
export declare function getStringRegisters(input: string): Set<RegisterKey>;
/**
 * Validates that no register overlap exists (system integrity check)
 */
export declare function validateNoRegisterOverlap(): ValidationResult;
//# sourceMappingURL=range-validator.d.ts.map