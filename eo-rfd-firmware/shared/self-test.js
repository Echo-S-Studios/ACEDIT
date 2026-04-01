// EO-RFD Self-Test Harness
// Collects per-module diagnostic results and produces aggregate health.

class SelfTest {
  constructor() {
    this._results = new Map();
  }

  /**
   * Register a module's self-test result.
   * @param {string} moduleId  — unique module identifier (e.g. 'L1_obs', 'L5_route')
   * @param {object} result    — { ok: boolean, latency: number, details: string }
   */
  register(moduleId, result) {
    this._results.set(moduleId, {
      ok: !!result.ok,
      latency: result.latency ?? 0,
      details: result.details ?? '',
      ts: Date.now()
    });
  }

  /**
   * Aggregate health across all registered modules.
   * @returns {{ ok: boolean, passed: number, failed: number, total: number,
   *             avgLatency: number, modules: object }}
   */
  get aggregate() {
    let passed = 0;
    let failed = 0;
    let totalLatency = 0;
    const modules = {};

    for (const [id, r] of this._results.entries()) {
      if (r.ok) {
        passed++;
      } else {
        failed++;
      }
      totalLatency += r.latency;
      modules[id] = { ...r };
    }

    const total = passed + failed;
    return {
      ok: failed === 0 && total > 0,
      passed,
      failed,
      total,
      avgLatency: total > 0 ? totalLatency / total : 0,
      modules
    };
  }

  /**
   * Serialize the full test report.
   */
  toJSON() {
    const agg = this.aggregate;
    return {
      timestamp: new Date().toISOString(),
      summary: {
        ok: agg.ok,
        passed: agg.passed,
        failed: agg.failed,
        total: agg.total,
        avgLatency: Math.round(agg.avgLatency * 1000) / 1000
      },
      modules: agg.modules
    };
  }
}

export const selfTest = new SelfTest();
export { SelfTest };
