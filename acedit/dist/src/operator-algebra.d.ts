/**
 * ACEDIT Operator Algebra
 *
 * System Invariant: Algebraic Closure - All compositions produce valid ACEDIT output
 * Implements the algebraic composition rules for operators
 */
export interface CompositionResult {
    valid: boolean;
    output: number | null;
    message: string;
}
/**
 * Composes two operators using algebraic rules
 * Enforces: Algebraic Closure invariant
 */
export declare function composeOperators(op1: number, op2: number): CompositionResult;
/**
 * Applies a modifier to an operator
 */
export declare function applyModifier(operator: number, modifier: number): CompositionResult;
/**
 * Validates a composition chain maintains algebraic closure
 */
export declare function validateCompositionChain(codepoints: number[]): CompositionResult;
/**
 * Checks if a composition is an identity operation (idempotent)
 */
export declare function isIdentityComposition(input: number, output: number): boolean;
/**
 * Gets the algebraic inverse of an operator (if defined)
 */
export declare function getInverse(operator: number): CompositionResult;
//# sourceMappingURL=operator-algebra.d.ts.map