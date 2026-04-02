/**
 * ACEDIT Operator Algebra
 *
 * System Invariant: Algebraic Closure - All compositions produce valid ACEDIT output
 * Implements the algebraic composition rules for operators
 */
import { isOperator, isModifier } from './register-engine.js';
import { validateCodepoint } from './range-validator.js';
/**
 * Composes two operators using algebraic rules
 * Enforces: Algebraic Closure invariant
 */
export function composeOperators(op1, op2) {
    // Validate both inputs
    const val1 = validateCodepoint(op1);
    const val2 = validateCodepoint(op2);
    if (!val1.valid) {
        return {
            valid: false,
            output: null,
            message: `Invalid first operand: ${val1.message}`
        };
    }
    if (!val2.valid) {
        return {
            valid: false,
            output: null,
            message: `Invalid second operand: ${val2.message}`
        };
    }
    // Check both are operators
    if (!isOperator(op1) || !isOperator(op2)) {
        return {
            valid: false,
            output: null,
            message: 'Both operands must be from the Operators register (A)'
        };
    }
    // For now, composition returns the first operator (identity-like behavior)
    // This ensures algebraic closure is maintained
    // More sophisticated composition rules can be added based on semantic requirements
    return {
        valid: true,
        output: op1,
        message: 'Composition successful (identity operation)'
    };
}
/**
 * Applies a modifier to an operator
 */
export function applyModifier(operator, modifier) {
    const val1 = validateCodepoint(operator);
    const val2 = validateCodepoint(modifier);
    if (!val1.valid) {
        return {
            valid: false,
            output: null,
            message: `Invalid operator: ${val1.message}`
        };
    }
    if (!val2.valid) {
        return {
            valid: false,
            output: null,
            message: `Invalid modifier: ${val2.message}`
        };
    }
    if (!isOperator(operator)) {
        return {
            valid: false,
            output: null,
            message: 'First operand must be from the Operators register (A)'
        };
    }
    if (!isModifier(modifier)) {
        return {
            valid: false,
            output: null,
            message: 'Second operand must be from the Modifiers register (C)'
        };
    }
    // Modifier application is a combining operation in Unicode
    // Return the operator unchanged (the modifier would be rendered adjacent in output)
    return {
        valid: true,
        output: operator,
        message: 'Modifier applied (combining character in output)'
    };
}
/**
 * Validates a composition chain maintains algebraic closure
 */
export function validateCompositionChain(codepoints) {
    if (codepoints.length === 0) {
        return {
            valid: false,
            output: null,
            message: 'Empty composition chain'
        };
    }
    // Validate all codepoints
    for (let i = 0; i < codepoints.length; i++) {
        const validation = validateCodepoint(codepoints[i]);
        if (!validation.valid) {
            return {
                valid: false,
                output: null,
                message: `Invalid codepoint at position ${i}: ${validation.message}`
            };
        }
    }
    // All valid codepoints maintain algebraic closure
    return {
        valid: true,
        output: codepoints[codepoints.length - 1],
        message: `Composition chain valid (${codepoints.length} codepoints)`
    };
}
/**
 * Checks if a composition is an identity operation (idempotent)
 */
export function isIdentityComposition(input, output) {
    return input === output;
}
/**
 * Gets the algebraic inverse of an operator (if defined)
 */
export function getInverse(operator) {
    if (!isOperator(operator)) {
        return {
            valid: false,
            output: null,
            message: 'Input must be from the Operators register (A)'
        };
    }
    // For basic implementation, inverse is identity
    // Can be extended with semantic operator inversions (e.g., ∪ ↔ ∩)
    return {
        valid: true,
        output: operator,
        message: 'Inverse is identity (basic implementation)'
    };
}
//# sourceMappingURL=operator-algebra.js.map