/**
 * ACEDIT Register Engine
 *
 * System Invariant: Register Sovereignty - Each codepoint belongs to exactly one register
 * Manages register detection, validation, and codepoint mapping
 */
import { RegisterKey } from './constants-registry.js';
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
export declare function getRegisterInfo(codepoint: number): RegisterInfo | null;
/**
 * Gets register information from a string character
 */
export declare function getRegisterFromChar(char: string): RegisterInfo | null;
/**
 * Checks if a codepoint is in the Operators register (A)
 */
export declare function isOperator(codepoint: number): boolean;
/**
 * Checks if a codepoint is in the Modifiers register (C)
 */
export declare function isModifier(codepoint: number): boolean;
/**
 * Checks if a codepoint is in the Ligatures register (E)
 */
export declare function isLigature(codepoint: number): boolean;
/**
 * Checks if a codepoint is in the Punctuation register (D)
 */
export declare function isPunctuation(codepoint: number): boolean;
/**
 * Checks if a codepoint is in the Constants register (I)
 */
export declare function isConstant(codepoint: number): boolean;
/**
 * Checks if a codepoint is in the Coherence register (T)
 */
export declare function isCoherence(codepoint: number): boolean;
/**
 * Gets all codepoints in a register
 */
export declare function getRegisterCodepoints(register: RegisterKey): number[];
/**
 * Converts codepoint to Unicode string representation
 */
export declare function codepointToUnicodeString(codepoint: number): string;
/**
 * Converts codepoint to actual character
 */
export declare function codepointToChar(codepoint: number): string;
/**
 * Gets register statistics
 */
export declare function getRegisterStats(register: RegisterKey): {
    register: RegisterKey;
    name: string;
    domain: string;
    totalCodepoints: number;
    rangeStart: string;
    rangeEnd: string;
};
/**
 * Gets all register statistics
 */
export declare function getAllRegisterStats(): {
    register: RegisterKey;
    name: string;
    domain: string;
    totalCodepoints: number;
    rangeStart: string;
    rangeEnd: string;
}[];
//# sourceMappingURL=register-engine.d.ts.map