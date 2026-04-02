/**
 * ACEDIT Punctuation Mapper
 *
 * Manages punctuation mapping for Register D (Delimiter)
 * Handles general punctuation and special spaces
 */
export interface PunctuationResult {
    valid: boolean;
    output: string;
    message: string;
}
/**
 * Maps a punctuation character to its ASCII equivalent
 */
export declare function toASCII(codepoint: number): PunctuationResult;
/**
 * Gets the name of a punctuation character
 */
export declare function getPunctuationName(codepoint: number): string | null;
/**
 * Converts a string with special punctuation to ASCII
 */
export declare function stringToASCII(input: string): string;
/**
 * Gets all available punctuation mappings
 */
export declare function getAllPunctuationMappings(): Array<{
    codepoint: number;
    unicode: string;
    character: string;
    name: string;
    ascii?: string;
}>;
/**
 * Validates that punctuation usage is semantically correct
 */
export declare function validatePunctuationUsage(input: string): PunctuationResult;
//# sourceMappingURL=punct-mapper.d.ts.map