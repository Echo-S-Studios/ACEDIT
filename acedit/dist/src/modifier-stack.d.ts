/**
 * ACEDIT Modifier Stack
 *
 * Manages combining diacritical marks (Register C)
 * Ensures proper stacking order and rendering
 */
export interface ModifierStackResult {
    valid: boolean;
    output: string;
    message: string;
}
/**
 * Applies a stack of modifiers to a base character
 */
export declare function applyModifierStack(base: number, modifiers: number[]): ModifierStackResult;
/**
 * Extracts modifiers from a string
 */
export declare function extractModifiers(input: string): {
    base: number | null;
    modifiers: number[];
};
/**
 * Normalizes modifier order (canonical ordering)
 */
export declare function normalizeModifierOrder(modifiers: number[]): number[];
/**
 * Validates that modifiers can be combined
 */
export declare function validateModifierCombination(modifiers: number[]): ModifierStackResult;
/**
 * Gets the maximum recommended modifier stack depth
 */
export declare function getMaxStackDepth(): number;
/**
 * Checks if a modifier stack exceeds recommended depth
 */
export declare function isStackDepthExceeded(modifiers: number[]): boolean;
//# sourceMappingURL=modifier-stack.d.ts.map