/**
 * ACEDIT Coherence Validator
 *
 * System Invariant: Validates visual coherence using Register T (Transformation)
 * Uses geometric shapes to verify rendering and transformation correctness
 */
export interface CoherenceResult {
    valid: boolean;
    score: number;
    message: string;
}
/**
 * Validates a coherence marker (geometric shape)
 */
export declare function validateCoherenceMarker(codepoint: number): CoherenceResult;
/**
 * Validates visual coherence of a string using the convergence constant
 *
 * The coherence score is calculated based on:
 * - Presence of coherence markers (geometric shapes)
 * - Ratio of coherence markers to total characters
 * - Convergence towards z_c = 3/2
 */
export declare function validateStringCoherence(input: string): CoherenceResult;
/**
 * Calculates the optimal number of coherence markers for a given text length
 */
export declare function getOptimalMarkerCount(textLength: number): number;
/**
 * Suggests coherence markers to add to achieve optimal coherence
 */
export declare function suggestCoherenceMarkers(input: string): CoherenceResult;
/**
 * Gets all available coherence markers
 */
export declare function getAllCoherenceMarkers(): Array<{
    codepoint: number;
    unicode: string;
    character: string;
    name: string;
    type: string;
}>;
/**
 * Validates that coherence is maintained throughout a transformation
 */
export declare function validateTransformationCoherence(input: string, output: string): CoherenceResult;
//# sourceMappingURL=coherence-validator.d.ts.map