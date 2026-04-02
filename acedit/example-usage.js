#!/usr/bin/env node

/**
 * ACEDIT Usage Examples
 * Demonstrates the core functionality of the ACEDIT system
 */

import {
  initializeACEDIT,
  getRegisterInfo,
  getAllRegisterStats,
  validateStringCoherence,
  transcodeString,
  resolveLigature,
  toASCII,
  codepointToChar
} from './dist/src/index.js';

console.log('='.repeat(60));
console.log('ACEDIT Typographic Firmware Layer - Usage Examples');
console.log('='.repeat(60));
console.log();

// Initialize the system
console.log('1. System Initialization');
console.log('-'.repeat(60));
const system = initializeACEDIT();
console.log(`✅ System Valid: ${system.valid}`);
console.log(`   Version: ${system.version}`);
console.log(`   Convergence Constant (z_c): ${system.convergenceConstant}`);
console.log(`   Errors: ${system.errors.length === 0 ? 'None' : system.errors.join(', ')}`);
console.log();

// Display register architecture
console.log('2. Register Architecture');
console.log('-'.repeat(60));
const stats = getAllRegisterStats();
stats.forEach(stat => {
  console.log(`${stat.register} - ${stat.name.padEnd(12)} | ${stat.domain.padEnd(16)} | ${stat.rangeStart}-${stat.rangeEnd} (${stat.totalCodepoints} codepoints)`);
});
console.log();

// Register detection
console.log('3. Register Detection');
console.log('-'.repeat(60));
const testCodepoints = [
  { cp: 0x2200, char: '∀' },
  { cp: 0x0301, char: 'á' },
  { cp: 0xFB01, char: 'ﬁ' },
  { cp: 0x2014, char: '—' },
  { cp: 0x2102, char: 'ℂ' },
  { cp: 0x25A0, char: '■' }
];

testCodepoints.forEach(({ cp, char }) => {
  const info = getRegisterInfo(cp);
  if (info) {
    console.log(`${char} U+${cp.toString(16).toUpperCase().padStart(4, '0')} → Register ${info.key} (${info.name}/${info.domain})`);
  }
});
console.log();

// Coherence validation
console.log('4. Coherence Validation');
console.log('-'.repeat(60));
const sampleText = 'Sample text with coherence markers ▲■●';
const coherence = validateStringCoherence(sampleText);
console.log(`Text: "${sampleText}"`);
console.log(`Coherence Score: ${coherence.score.toFixed(4)}`);
console.log(`Message: ${coherence.message}`);
console.log();

// Transcoding example
console.log('5. Transcoding Between Registers');
console.log('-'.repeat(60));
const operator = codepointToChar(0x2200); // ∀
console.log(`Original: ${operator} (U+2200) in Register A (Operators)`);

const transcoded = transcodeString(operator, 'C');
console.log(`Transcoded to Register C: ${transcoded.output}`);
console.log(`Is Passthrough: ${transcoded.isPassthrough}`);
console.log(`Message: ${transcoded.message}`);
console.log();

// Ligature resolution
console.log('6. Ligature Resolution');
console.log('-'.repeat(60));
const ligatureCP = 0xFB01; // ﬁ
const ligResult = resolveLigature(ligatureCP);
console.log(`Ligature: ${codepointToChar(ligatureCP)} (U+FB01)`);
console.log(`Resolved to: "${ligResult.output}"`);
console.log(`Message: ${ligResult.message}`);
console.log();

// Punctuation mapping
console.log('7. Punctuation to ASCII Mapping');
console.log('-'.repeat(60));
const emDash = 0x2014;
const asciiResult = toASCII(emDash);
console.log(`Unicode: ${codepointToChar(emDash)} (U+2014)`);
console.log(`ASCII Equivalent: "${asciiResult.output}"`);
console.log(`Message: ${asciiResult.message}`);
console.log();

console.log('='.repeat(60));
console.log('All examples completed successfully!');
console.log('='.repeat(60));
