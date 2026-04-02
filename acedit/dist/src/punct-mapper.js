/**
 * ACEDIT Punctuation Mapper
 *
 * Manages punctuation mapping for Register D (Delimiter)
 * Handles general punctuation and special spaces
 */
import { isPunctuation, codepointToChar, codepointToUnicodeString } from './register-engine.js';
import { validateCodepoint } from './range-validator.js';
/**
 * Common punctuation mappings (U+2000-U+206F)
 */
const PUNCTUATION_MAPPINGS = {
    // Spaces
    0x2000: { name: 'En Quad', ascii: ' ' },
    0x2001: { name: 'Em Quad', ascii: ' ' },
    0x2002: { name: 'En Space', ascii: ' ' },
    0x2003: { name: 'Em Space', ascii: ' ' },
    0x2004: { name: 'Three-Per-Em Space', ascii: ' ' },
    0x2005: { name: 'Four-Per-Em Space', ascii: ' ' },
    0x2006: { name: 'Six-Per-Em Space', ascii: ' ' },
    0x2007: { name: 'Figure Space', ascii: ' ' },
    0x2008: { name: 'Punctuation Space', ascii: ' ' },
    0x2009: { name: 'Thin Space', ascii: ' ' },
    0x200A: { name: 'Hair Space', ascii: ' ' },
    0x200B: { name: 'Zero Width Space', ascii: '' },
    // Dashes
    0x2010: { name: 'Hyphen', ascii: '-' },
    0x2011: { name: 'Non-Breaking Hyphen', ascii: '-' },
    0x2012: { name: 'Figure Dash', ascii: '-' },
    0x2013: { name: 'En Dash', ascii: '-' },
    0x2014: { name: 'Em Dash', ascii: '--' },
    0x2015: { name: 'Horizontal Bar', ascii: '--' },
    // Quotes
    0x2018: { name: 'Left Single Quotation Mark', ascii: "'" },
    0x2019: { name: 'Right Single Quotation Mark', ascii: "'" },
    0x201A: { name: 'Single Low-9 Quotation Mark', ascii: "'" },
    0x201B: { name: 'Single High-Reversed-9 Quotation Mark', ascii: "'" },
    0x201C: { name: 'Left Double Quotation Mark', ascii: '"' },
    0x201D: { name: 'Right Double Quotation Mark', ascii: '"' },
    0x201E: { name: 'Double Low-9 Quotation Mark', ascii: '"' },
    0x201F: { name: 'Double High-Reversed-9 Quotation Mark', ascii: '"' },
    // Other punctuation
    0x2020: { name: 'Dagger', ascii: '+' },
    0x2021: { name: 'Double Dagger', ascii: '++' },
    0x2022: { name: 'Bullet', ascii: '*' },
    0x2023: { name: 'Triangular Bullet', ascii: '>' },
    0x2024: { name: 'One Dot Leader', ascii: '.' },
    0x2025: { name: 'Two Dot Leader', ascii: '..' },
    0x2026: { name: 'Horizontal Ellipsis', ascii: '...' },
    0x2027: { name: 'Hyphenation Point', ascii: '-' },
};
/**
 * Maps a punctuation character to its ASCII equivalent
 */
export function toASCII(codepoint) {
    const validation = validateCodepoint(codepoint);
    if (!validation.valid) {
        return {
            valid: false,
            output: '',
            message: `Invalid codepoint: ${validation.message}`
        };
    }
    if (!isPunctuation(codepoint)) {
        return {
            valid: false,
            output: '',
            message: `Codepoint ${codepointToUnicodeString(codepoint)} is not punctuation (not in register D)`
        };
    }
    const mapping = PUNCTUATION_MAPPINGS[codepoint];
    if (mapping && mapping.ascii) {
        return {
            valid: true,
            output: mapping.ascii,
            message: `Mapped ${mapping.name} to ASCII "${mapping.ascii}"`
        };
    }
    // Return the character itself if no ASCII mapping
    return {
        valid: true,
        output: codepointToChar(codepoint),
        message: `No ASCII mapping for ${codepointToUnicodeString(codepoint)} (returned as-is)`
    };
}
/**
 * Gets the name of a punctuation character
 */
export function getPunctuationName(codepoint) {
    if (!isPunctuation(codepoint)) {
        return null;
    }
    const mapping = PUNCTUATION_MAPPINGS[codepoint];
    return mapping ? mapping.name : null;
}
/**
 * Converts a string with special punctuation to ASCII
 */
export function stringToASCII(input) {
    let output = '';
    for (let i = 0; i < input.length; i++) {
        const codepoint = input.codePointAt(i);
        if (codepoint === undefined)
            continue;
        if (isPunctuation(codepoint)) {
            const result = toASCII(codepoint);
            output += result.output;
        }
        else {
            output += codepointToChar(codepoint);
        }
        // Skip surrogate pair if needed
        if (codepoint > 0xFFFF) {
            i++;
        }
    }
    return output;
}
/**
 * Gets all available punctuation mappings
 */
export function getAllPunctuationMappings() {
    return Object.entries(PUNCTUATION_MAPPINGS).map(([cp, info]) => {
        const codepoint = parseInt(cp, 10);
        return {
            codepoint,
            unicode: codepointToUnicodeString(codepoint),
            character: codepointToChar(codepoint),
            name: info.name,
            ascii: info.ascii
        };
    });
}
/**
 * Validates that punctuation usage is semantically correct
 */
export function validatePunctuationUsage(input) {
    // Basic validation: check for common issues
    const issues = [];
    // Check for multiple consecutive spaces of different types
    let prevWasSpace = false;
    for (let i = 0; i < input.length; i++) {
        const codepoint = input.codePointAt(i);
        if (codepoint === undefined)
            continue;
        if (codepoint >= 0x2000 && codepoint <= 0x200A) {
            if (prevWasSpace) {
                issues.push('Multiple consecutive special spaces detected');
                break;
            }
            prevWasSpace = true;
        }
        else {
            prevWasSpace = false;
        }
        if (codepoint > 0xFFFF) {
            i++;
        }
    }
    return {
        valid: issues.length === 0,
        output: input,
        message: issues.length === 0 ? 'Punctuation usage valid' : issues.join('; ')
    };
}
//# sourceMappingURL=punct-mapper.js.map