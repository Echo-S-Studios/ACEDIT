/**
 * ACEDIT Transcode Engine
 *
 * System Invariant: Idempotent Passthrough - No double-encoding
 * Handles transcoding between ACEDIT registers while maintaining all invariants
 */
import { RegisterKey } from './constants-registry.js';
export interface TranscodeResult {
    valid: boolean;
    output: string;
    sourceRegister?: RegisterKey;
    targetRegister?: RegisterKey;
    message: string;
    isPassthrough: boolean;
}
/**
 * Transcodes a single codepoint to a target register
 * Enforces: Idempotent Passthrough invariant
 */
export declare function transcodeCodepoint(codepoint: number, targetRegister: RegisterKey): TranscodeResult;
/**
 * Transcodes a string to use codepoints from a specific register
 */
export declare function transcodeString(input: string, targetRegister: RegisterKey): TranscodeResult;
/**
 * Validates that transcoding maintains coherence
 */
export declare function transcodeWithCoherenceValidation(input: string, targetRegister: RegisterKey): TranscodeResult;
/**
 * Detects the source register and suggests optimal target register
 */
export declare function detectAndSuggestTranscode(input: string): {
    sourceRegisters: RegisterKey[];
    suggestedTarget: RegisterKey | null;
    message: string;
};
/**
 * Batch transcode: converts all codepoints to their register equivalents
 */
export declare function batchTranscode(inputs: string[], targetRegister: RegisterKey): Array<TranscodeResult>;
//# sourceMappingURL=transcode-engine.d.ts.map