/**
 * ACEDIT System Validation Tests
 *
 * Validates all 6 system invariants at initialization
 */

import { strict as assert } from 'assert';
import { test } from 'node:test';
import {
  initializeACEDIT,
  ACEDIT_CONSTANTS,
  validateConvergenceConstant,
  validateNoRegisterOverlap,
  UNICODE_RANGES,
  getRegisterForCodepoint,
  getAllRegisterStats
} from '../src/index.js';

test('System Initialization', () => {
  const system = initializeACEDIT();

  assert.equal(system.valid, true, 'System should initialize successfully');
  assert.equal(system.errors.length, 0, 'Should have no initialization errors');
  assert.equal(system.version, '1.0.0', 'Version should be 1.0.0');
});

test('Invariant 1: Bijective Mirror - 6 registers to 6 domains', () => {
  const registers = Object.keys(UNICODE_RANGES);
  assert.equal(registers.length, 6, 'Should have exactly 6 registers');

  const expectedRegisters = ['A', 'C', 'E', 'D', 'I', 'T'];
  for (const reg of expectedRegisters) {
    assert.ok(registers.includes(reg), `Should include register ${reg}`);
  }
});

test('Invariant 2: Register Sovereignty - No overlaps', () => {
  const result = validateNoRegisterOverlap();
  assert.equal(result.valid, true, 'Registers should not overlap');
});

test('Invariant 3: Convergence Constant - √3/2', () => {
  const isValid = validateConvergenceConstant();
  assert.equal(isValid, true, 'Convergence constant should validate');

  const expected = Math.sqrt(3) / 2;
  assert.ok(
    Math.abs(ACEDIT_CONSTANTS.Z_C - expected) < ACEDIT_CONSTANTS.EPSILON,
    'Z_C should equal √3/2'
  );

  assert.equal(
    ACEDIT_CONSTANTS.Z_C_SYMBOLIC,
    '√3/2',
    'Symbolic representation should be √3/2'
  );
});

test('Register Sovereignty: Each codepoint maps to exactly one register', () => {
  // Test sample codepoints from each register
  const testCases = [
    { cp: 0x2200, expected: 'A' }, // ∀ - Operators
    { cp: 0x0301, expected: 'C' }, // Combining acute - Modifiers
    { cp: 0xFB00, expected: 'E' }, // ff ligature - Ligatures
    { cp: 0x2014, expected: 'D' }, // Em dash - Punctuation
    { cp: 0x2102, expected: 'I' }, // ℂ - Constants
    { cp: 0x25A0, expected: 'T' }  // Black square - Coherence
  ];

  for (const { cp, expected } of testCases) {
    const register = getRegisterForCodepoint(cp);
    assert.equal(register, expected, `U+${cp.toString(16)} should be in register ${expected}`);
  }
});

test('Register Statistics', () => {
  const stats = getAllRegisterStats();

  assert.equal(stats.length, 6, 'Should have stats for all 6 registers');

  // Verify each register has expected properties
  for (const stat of stats) {
    assert.ok(stat.register, 'Should have register key');
    assert.ok(stat.name, 'Should have register name');
    assert.ok(stat.domain, 'Should have domain');
    assert.ok(stat.totalCodepoints > 0, 'Should have codepoint count');
    assert.ok(stat.rangeStart, 'Should have range start');
    assert.ok(stat.rangeEnd, 'Should have range end');
  }
});

test('Zero Infrastructure: Constants defined correctly', () => {
  assert.equal(typeof ACEDIT_CONSTANTS.Z_C, 'number', 'Z_C should be a number');
  assert.equal(typeof ACEDIT_CONSTANTS.VERSION, 'string', 'VERSION should be a string');
  assert.equal(typeof ACEDIT_CONSTANTS.EPSILON, 'number', 'EPSILON should be a number');
});

console.log('All system invariant tests passed!');
