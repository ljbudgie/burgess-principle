(function attachIrisSovereignAuditEngine(globalScope) {
  // Burgess Compliance: audits expose local integrity state so a human can inspect it;
  // they are transparency tooling, not a substitute for human judgment.
  const existing = globalScope.IrisSovereignCore || {};

  function createAuditEngine(adapter) {
    if (!adapter || typeof adapter.sha256Hex !== 'function' || typeof adapter.canonicalize !== 'function') {
      throw new Error('Audit engine requires sha256Hex and canonicalize adapters.');
    }

    async function buildMerkleState(leaves, index) {
      if (!Array.isArray(leaves) || leaves.length === 0) {
        return { root: '', proof: [] };
      }
      let level = leaves.slice();
      let cursor = Math.max(0, Math.min(index, level.length - 1));
      const proof = [];
      while (level.length > 1) {
        const next = [];
        for (let i = 0; i < level.length; i += 2) {
          const left = level[i];
          const right = level[i + 1] || left;
          next.push(await adapter.sha256Hex(adapter.canonicalize({ left, right })));
          if (i === cursor || i + 1 === cursor) {
            proof.push(i === cursor ? right : left);
            cursor = next.length - 1;
          }
        }
        level = next;
      }
      return { root: level[0], proof };
    }

    async function verifySequentialChain(records, options = {}) {
      let previousCommitmentHash = '';
      for (const record of records) {
        if ((record.previous_commitment_hash || '') !== previousCommitmentHash) {
          throw new Error(`Commitment chain broke at ${record.id || record.namespace || 'record'}.`);
        }
        if (typeof options.verifyRecord === 'function') {
          await options.verifyRecord(record);
        }
        previousCommitmentHash = record.commitment_hash || '';
      }
      return records.length;
    }

    function buildReceipt({ record, rootRecord, inclusionProof = [], disclosure = {} }) {
      return {
        receipt_export_version: 1,
        exported_at: new Date().toISOString(),
        record,
        root_record: rootRecord || null,
        inclusion_proof: inclusionProof,
        disclosure,
      };
    }

    return {
      buildMerkleState,
      verifySequentialChain,
      buildReceipt,
    };
  }

  globalScope.IrisSovereignCore = {
    ...existing,
    createAuditEngine,
    audit: {
      ...(existing.audit || {}),
      createAuditEngine,
    },
  };
})(typeof globalThis !== 'undefined' ? globalThis : self);
