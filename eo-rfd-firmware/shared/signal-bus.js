// EO-RFD Signal Bus — inter-module event + register backbone

export const REG = {
  // ── L1: Input Observation ──
  L1_OBS_RAW:         0x0100,
  L1_OBS_HASH:        0x0101,
  L1_OBS_LEN:         0x0102,
  L1_OBS_TIMESTAMP:   0x0103,
  L1_OBS_ENCODING:    0x0104,

  // ── L2: Naming / Classification ──
  L2_NAME_CLASS:      0x0200,
  L2_NAME_CANON:      0x0201,
  L2_NAME_SAFETY:     0x0202,
  L2_NAME_CONFIDENCE: 0x0203,
  L2_NAME_ALIAS_FLAG: 0x0204,

  // ── L3: Theta Regime ──
  L3_THETA_MODE:      0x0300,
  L3_THETA_APERTURE:  0x0301,
  L3_THETA_PHASE:     0x0302,
  L3_THETA_CAPACITY:  0x0303,
  L3_THETA_STRICTNESS:0x0304,

  // ── L4: Triangular Geometry ──
  L4_TRI_POS_X:       0x0400,
  L4_TRI_POS_Y:       0x0401,
  L4_TRI_BARY_A:      0x0402,
  L4_TRI_BARY_B:      0x0403,
  L4_TRI_BARY_C:      0x0404,
  L4_TRI_FOLD:        0x0405,
  L4_TRI_CENTROID_D:  0x0406,

  // ── L5: Routing / Harbor ──
  L5_ROUTE_SIGNAL:    0x0500,
  L5_ROUTE_HARBOR:    0x0501,
  L5_ROUTE_RECAPTURE: 0x0502,
  L5_ROUTE_PERSIST:   0x0503,
  L5_ROUTE_SIGMA:     0x0504,
  L5_ROUTE_DECISION:  0x0505,

  // ── L6: Sigma-Tau Integration ──
  L6_SIGMA_OBS:       0x0600,
  L6_SIGMA_NAME:      0x0601,
  L6_SIGMA_RED:       0x0602,
  L6_SIGMA_COH:       0x0603,
  L6_SIGMA_COMPOSITE: 0x0604,
  L6_TAU_DECAY:       0x0605,

  // ── L7: Detector / Modulation ──
  L7_DET_THETA_MOD:   0x0700,
  L7_DET_NAME_MOD:    0x0701,
  L7_DET_COMBINED:    0x0702,
  L7_DET_ALERT:       0x0703,
  L7_DET_SUPPRESS:    0x0704,

  // ── L8: Policy Enforcement ──
  L8_POL_ALLOW:       0x0800,
  L8_POL_DENY:        0x0801,
  L8_POL_ESCALATE:    0x0802,
  L8_POL_REASON:      0x0803,
  L8_POL_OVERRIDE:    0x0804,

  // ── L9: Output / Emission ──
  L9_OUT_PAYLOAD:     0x0900,
  L9_OUT_STATUS:      0x0901,
  L9_OUT_LATENCY:     0x0902,
  L9_OUT_TRACE_ID:    0x0903,
  L9_OUT_EMISSION_OK: 0x0904,

  // ── Global ──
  G_TICK:             0xF000,
  G_CLOCK:            0xF001,
  G_RESET:            0xF002,
  G_HALT:             0xF003,
  G_SELF_TEST:        0xF010,
  G_FIRMWARE_VER:     0xF0FF
};

const CHANNEL_NAMES = [
  'obs:input',
  'obs:hash',
  'name:classify',
  'name:resolve',
  'theta:mode',
  'theta:update',
  'tri:position',
  'tri:barycentric',
  'tri:fold',
  'route:signal',
  'route:harbor',
  'route:decision',
  'sigma:update',
  'sigma:composite',
  'sigma:decay',
  'det:modulate',
  'det:alert',
  'det:suppress',
  'pol:evaluate',
  'pol:decision',
  'pol:escalate',
  'out:emit',
  'out:status',
  'tick',
  'reset',
  'halt',
  'self-test'
];

class SignalBus {
  constructor() {
    this._listeners = new Map();
    this._registers = new Map();
    this._history = [];
    this._maxHistory = 512;

    // Initialize all channels
    for (const ch of CHANNEL_NAMES) {
      this._listeners.set(ch, []);
    }

    // Initialize all registers to 0
    for (const key of Object.keys(REG)) {
      this._registers.set(REG[key], 0);
    }
  }

  /**
   * Subscribe to a named channel.
   * Returns an unsubscribe function.
   */
  on(channel, fn) {
    if (!this._listeners.has(channel)) {
      this._listeners.set(channel, []);
    }
    this._listeners.get(channel).push(fn);
    return () => {
      const arr = this._listeners.get(channel);
      if (arr) {
        const idx = arr.indexOf(fn);
        if (idx !== -1) arr.splice(idx, 1);
      }
    };
  }

  /**
   * Emit a signal on a named channel.
   */
  emit(channel, payload) {
    const entry = {
      channel,
      payload,
      ts: performance.now()
    };
    this._history.push(entry);
    if (this._history.length > this._maxHistory) {
      this._history.shift();
    }

    const fns = this._listeners.get(channel);
    if (fns) {
      for (const fn of fns) {
        try {
          fn(payload);
        } catch (e) {
          console.error(`[SignalBus] error on channel "${channel}":`, e);
        }
      }
    }
  }

  /**
   * Write a value to a register address.
   */
  writeReg(addr, value) {
    this._registers.set(addr, value);
  }

  /**
   * Read a value from a register address.
   */
  readReg(addr) {
    return this._registers.get(addr) ?? 0;
  }

  /**
   * Dump all registers as a plain object { addr_hex: value }.
   */
  dumpRegisters() {
    const out = {};
    for (const [addr, val] of this._registers.entries()) {
      out['0x' + addr.toString(16).padStart(4, '0')] = val;
    }
    return out;
  }

  /**
   * Return recent signal history.
   */
  getHistory(limit = 64) {
    return this._history.slice(-limit);
  }

  /**
   * Clear all registers and history.
   */
  reset() {
    for (const key of Object.keys(REG)) {
      this._registers.set(REG[key], 0);
    }
    this._history = [];
    this.emit('reset', { ts: performance.now() });
  }

  /**
   * List all registered channel names.
   */
  get channels() {
    return [...this._listeners.keys()];
  }
}

export const bus = new SignalBus();
