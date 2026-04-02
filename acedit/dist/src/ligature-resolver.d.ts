/**
 * ACEDIT Ligature Resolver
 *
 * Manages ligature resolution for Register E (Encoding)
 * Handles alphabetic presentation forms
 */
export interface LigatureResult {
    valid: boolean;
    output: string;
    message: string;
}
/**
 * Resolves a ligature to its component characters
 */
export declare function resolveLigature(codepoint: number): LigatureResult;
/**
 * Attempts to create a ligature from component characters
 */
export declare function createLigature(components: string): LigatureResult;
/**
 * Processes a string and resolves all ligatures
 */
export declare function resolveAllLigatures(input: string): string;
/**
 * Processes a string and creates ligatures where possible
 */
export declare function createAllLigatures(input: string): string;
/**
 * Gets all available ligature mappings
 */
export declare function getAllLigatureMappings(): Array<{
    codepoint: number;
    unicode: string;
    character: string;
    decomposition: string;
}>;
//# sourceMappingURL=ligature-resolver.d.ts.map