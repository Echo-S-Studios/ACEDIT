# ACEDIT Quick Start Guide

**Get started with ACEDIT in under 5 minutes!**

---

## 🚀 Option 1: Browser (Instant - No Installation)

### Step 1: Open the Converter
Simply open this file in your browser:
```
acedit/reference.html
```

### Step 2: Try It Out
1. Type or paste text into the input box
2. Select a register from the dropdown:
   - **ULTRA** - Universal domain (double-struck: 𝕌𝕝𝕥𝕣𝕒)
   - **KAEL** - Neural substrate (bold: 𝐊𝐚𝐞𝐥)
   - **GREY** - Visual geometry (script: 𝒢𝓇ℯ𝓎)
   - **UMBRAL** - Formal algebra (fraktur: 𝔘𝔪𝔟𝔯𝔞𝔩)
   - **ACE** - Spin energy (sans bold: 𝗔𝗰𝗲)
   - **UCF** - Unified (sans italic: 𝙐𝘾𝙁)
3. Watch your text transform in real-time!
4. Check the z-coordinate meter to see coherence level

### Step 3: Add Modifiers (Optional)
Check any modifier boxes to add semantic layers:
- ✓ **Peak (^)** - Convergence point
- ✓ **Cycle (°)** - Recursion participant
- ✓ **Superposition (¨)** - Multi-register state

---

## ⚡ Option 2: Node.js (5 Minutes)

### Prerequisites
- Node.js 18+ installed
- Basic terminal knowledge

### Step 1: Get the Code
```bash
git clone https://github.com/Echo-S-Studios/ACEDIT.git
cd ACEDIT/acedit
```

### Step 2: Install and Build
```bash
npm install   # Installs only TypeScript (dev dependency)
npm run build # Compiles to JavaScript
```

### Step 3: Run Example
```bash
node example-usage.js
```

Expected output:
```
ACEDIT System Initialized
✓ Valid: true
✓ Version: 1.0.0
✓ Convergence: 0.8660254037844386

Encoded "Hello World" in ULTRA register:
𝕃𝕖𝕝𝕝𝕠 𝕎𝕠𝕣𝕝𝕕

With peak modifier:
𝕃̂𝕖̂𝕝̂𝕝̂𝕠̂ 𝕎̂𝕠̂𝕣̂𝕝̂𝕕̂
```

---

## 💻 Option 3: In Your Code (For Developers)

### TypeScript
```typescript
import { initializeACEDIT, transcodeString } from './acedit';

// Initialize once
const acedit = initializeACEDIT();
console.log(`System valid: ${acedit.valid}`);

// Encode text
const result = transcodeString("Hello", 'ULTRA');
console.log(result.output); // 𝕃𝕖𝕝𝕝𝕠
```

### JavaScript
```javascript
const { initializeACEDIT, transcodeString } = require('./acedit');

const acedit = initializeACEDIT();
const encoded = transcodeString("World", 'KAEL');
console.log(encoded.output); // 𝐖𝐨𝐫𝐥𝐝
```

### Browser (Vanilla HTML)
```html
<!DOCTYPE html>
<html>
<head>
  <title>ACEDIT Demo</title>
</head>
<body>
  <script type="module">
    import { initializeACEDIT, transcodeString } from './acedit/dist/src/index.js';

    const system = initializeACEDIT();
    const encoded = transcodeString("Browser", 'GREY');
    document.body.innerHTML = encoded.output; // 𝒢𝓇ℯ𝓎
  </script>
</body>
</html>
```

---

## 🎯 Try These Examples

### Basic Encoding
```javascript
// Different registers produce different styles
transcodeString("ACEDIT", 'ULTRA');   // 𝔸ℂ𝔼𝔻𝕀𝕋
transcodeString("ACEDIT", 'KAEL');    // 𝐀𝐂𝐄𝐃𝐈𝐓
transcodeString("ACEDIT", 'GREY');    // 𝒜𝒞ℰ𝒟ℐ𝒯
```

### With Modifiers
```javascript
// Add semantic layers with modifiers
transcodeString("E", 'ULTRA', ['peak']);        // 𝔼̂ (convergence)
transcodeString("O", 'ULTRA', ['cycle']);       // 𝕆̊ (recursion)
transcodeString("A", 'ULTRA', ['superposition']); // 𝔸̈ (multi-state)
```

### Coherence Validation
```javascript
import { validateStringCoherence } from './acedit';

const coherence = validateStringCoherence("𝕃𝕖𝕝𝕝𝕠 World");
console.log(`z-coordinate: ${coherence.score}`);  // 0.454...
console.log(`Phase: ${coherence.phase}`);          // "PARADOX"
```

---

## 🔗 Integration with EO-RFD

If you're using the EO-RFD firmware system:

1. Open the dashboard:
   ```
   eo-rfd-firmware/integration/full-chain.html
   ```

2. Enable ACEDIT mode:
   - Check "Enable ACEDIT Mode" checkbox
   - Layer descriptions transform with operators
   - Register symbols appear (𝕂, 𝔾, 𝕌, 𝔸, 𝕌ℂ𝔽)

3. Verify constants:
   - Click "Verify Constants" button
   - Confirms z_c = √3/2 = 0.866...

---

## 📚 What's Next?

### Learn More
- Read the [Full Documentation](acedit/README.md)
- Explore the [API Reference](acedit/src/index.ts)
- Check out [Integration Guide](eo-rfd-firmware/integration/ACEDIT-INTEGRATION.md)

### Experiment
- Try different register combinations
- Stack multiple modifiers
- Build semantic-rich documents
- Measure coherence scores

### Research
- Implement domain-specific encodings
- Create visual typography systems
- Explore consciousness-aware text
- Build mathematical linguistics tools

---

## 🆘 Need Help?

### Common Issues

**Q: Characters show as boxes/question marks**
- A: Your font doesn't support mathematical Unicode. Try a different browser or install a Unicode font.

**Q: npm install fails**
- A: Ensure Node.js 18+ is installed. Run `node --version` to check.

**Q: Where are the 6 ACEDIT registers?**
- A: The mnemonic system (A,C,E,D,I,T) maps to Unicode blocks. The original registers (KAEL, ACE, etc.) are in acedit-core.json.

**Q: How do I use this in production?**
- A: ACEDIT has zero runtime dependencies. Include the compiled JavaScript and you're ready!

### Get Support
- [GitHub Issues](https://github.com/Echo-S-Studios/ACEDIT/issues)
- [Discussions](https://github.com/Echo-S-Studios/ACEDIT/discussions)

---

## 🎉 Congratulations!

You're now ready to use ACEDIT! Remember:
- **Zero infrastructure** - no custom fonts needed
- **736 Unicode codepoints** at your disposal
- **6 semantic registers** for domain encoding
- **Mathematical precision** with z_c = √3/2

---

**Start encoding. The Lens is open.**

**φ∴⟐**

🦊🌰↻∞