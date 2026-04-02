/**
 * ACEDIT Core Loader
 *
 * Loads and validates the acedit-core.json configuration
 * Enforces: All system invariants at initialization
 */
export interface ACEDITCore {
    metadata: {
        version: string;
        specification: string;
        convergence_constant: number;
        convergence_constant_symbolic: string;
        invariants: string[];
    };
    registers: Record<string, {
        name: string;
        domain: string;
        range: string;
        description: string;
        codepoint_count: number;
    }>;
    range_mappings: Record<string, string>;
    transcoding_rules: {
        input_detection: string;
        passthrough_check: string;
        composition_algebra: string;
        validation: string;
    };
}
/**
 * Loads acedit-core.json from the project root
 */
export declare function loadCore(): ACEDITCore;
/**
 * Validates the loaded core against system invariants
 */
export declare function validateCore(core: ACEDITCore): {
    valid: boolean;
    errors: string[];
};
/**
 * Initializes and validates the ACEDIT core system
 */
export declare function initializeCore(): ACEDITCore;
//# sourceMappingURL=core-loader.d.ts.map