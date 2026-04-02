/**
 * ACEDIT Core Loader
 *
 * Loads and validates the acedit-core.json configuration
 * Enforces: All system invariants at initialization
 */
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { UNICODE_RANGES, ACEDIT_CONSTANTS } from './constants-registry.js';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
let cachedCore = null;
/**
 * Loads acedit-core.json from the project root
 */
export function loadCore() {
    if (cachedCore) {
        return cachedCore;
    }
    try {
        const corePath = join(__dirname, '..', 'acedit-core.json');
        const coreData = readFileSync(corePath, 'utf-8');
        cachedCore = JSON.parse(coreData);
        return cachedCore;
    }
    catch (error) {
        throw new Error(`Failed to load acedit-core.json: ${error}`);
    }
}
/**
 * Validates the loaded core against system invariants
 */
export function validateCore(core) {
    const errors = [];
    // Validate convergence constant
    if (Math.abs(core.metadata.convergence_constant - ACEDIT_CONSTANTS.Z_C) > ACEDIT_CONSTANTS.EPSILON) {
        errors.push(`Convergence constant mismatch: expected ${ACEDIT_CONSTANTS.Z_C}, got ${core.metadata.convergence_constant}`);
    }
    // Validate bijective mirror: 6 registers
    const registerKeys = Object.keys(core.registers);
    if (registerKeys.length !== 6) {
        errors.push(`Bijective Mirror violated: expected 6 registers, got ${registerKeys.length}`);
    }
    // Validate register names match ACEDIT mnemonic
    const expectedRegisters = ['A', 'C', 'E', 'D', 'I', 'T'];
    for (const expected of expectedRegisters) {
        if (!registerKeys.includes(expected)) {
            errors.push(`Missing required register: ${expected}`);
        }
    }
    // Validate range mappings match constants
    for (const [key, range] of Object.entries(UNICODE_RANGES)) {
        const rangeStr = `U+${range.start.toString(16).toUpperCase().padStart(4, '0')}-U+${range.end.toString(16).toUpperCase().padStart(4, '0')}`;
        const coreRegister = core.registers[key];
        if (!coreRegister) {
            errors.push(`Register ${key} missing from core`);
            continue;
        }
        if (coreRegister.range !== rangeStr) {
            errors.push(`Range mismatch for register ${key}: expected ${rangeStr}, got ${coreRegister.range}`);
        }
    }
    // Validate all invariants are documented
    const requiredInvariants = [
        'Bijective Mirror',
        'Algebraic Closure',
        'Zero Infrastructure',
        'Convergence Constant',
        'Register Sovereignty',
        'Idempotent Passthrough'
    ];
    for (const required of requiredInvariants) {
        const found = core.metadata.invariants.some(inv => inv.includes(required));
        if (!found) {
            errors.push(`Missing required invariant: ${required}`);
        }
    }
    return {
        valid: errors.length === 0,
        errors
    };
}
/**
 * Initializes and validates the ACEDIT core system
 */
export function initializeCore() {
    const core = loadCore();
    const validation = validateCore(core);
    if (!validation.valid) {
        throw new Error(`ACEDIT core validation failed:\n${validation.errors.join('\n')}`);
    }
    return core;
}
//# sourceMappingURL=core-loader.js.map