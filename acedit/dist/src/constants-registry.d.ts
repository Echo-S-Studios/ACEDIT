/**
 * ACEDIT Constants Registry
 *
 * System Invariant: Convergence Constant z_c = √3/2 = 0.8660254...
 * Maintains all mathematical and system constants used throughout ACEDIT
 */
export declare const ACEDIT_CONSTANTS: {
    /** Convergence constant: √3/2 */
    readonly Z_C: number;
    /** Symbolic representation */
    readonly Z_C_SYMBOLIC: "√3/2";
    /** Precision for floating point comparisons */
    readonly EPSILON: 1e-10;
    /** System version */
    readonly VERSION: "1.0.0";
};
/**
 * Register names (ACEDIT mnemonic)
 */
export declare const REGISTERS: {
    readonly A: "Operators";
    readonly C: "Modifiers";
    readonly E: "Ligatures";
    readonly D: "Punctuation";
    readonly I: "Constants";
    readonly T: "Coherence";
};
export type RegisterKey = keyof typeof REGISTERS;
/**
 * Framework domain mappings (bijective mirror)
 */
export declare const DOMAINS: {
    readonly A: "Algebra";
    readonly C: "Configuration";
    readonly E: "Encoding";
    readonly D: "Delimiter";
    readonly I: "Identity";
    readonly T: "Transformation";
};
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
export declare const UNICODE_RANGES: Record<RegisterKey, UnicodeRange>;
/**
 * Validates that a codepoint belongs to exactly one register
 * Enforces: Register Sovereignty invariant
 */
export declare function getRegisterForCodepoint(codepoint: number): RegisterKey | null;
/**
 * Validates convergence constant calculation
 */
export declare function validateConvergenceConstant(): boolean;
//# sourceMappingURL=constants-registry.d.ts.map