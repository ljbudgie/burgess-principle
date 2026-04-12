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
            proof.push({
              hash: i === cursor ? right : left,
              position: i === cursor ? 'right' : 'left',
            });
            cursor = next.length - 1;
          }
        }
        level = next;
      }
      return { root: level[0], proof };
    }

    async function verifyMerkleProof(leafHash, proof, expectedRoot) {
      if (typeof leafHash !== 'string' || !leafHash || typeof expectedRoot !== 'string' || !expectedRoot) {
        throw new Error('Merkle proof verification requires a leaf hash and an expected root.');
      }
      let hashCandidates = new Set([leafHash]);
      const normalizedProof = Array.isArray(proof) ? proof : [];
      for (const step of normalizedProof) {
        const next = new Set();
        for (const candidate of hashCandidates) {
          if (typeof step === 'string') {
            next.add(await adapter.sha256Hex(adapter.canonicalize({ left: candidate, right: step })));
            next.add(await adapter.sha256Hex(adapter.canonicalize({ left: step, right: candidate })));
            continue;
          }
          if (!step || typeof step.hash !== 'string' || !step.hash) {
            continue;
          }
          if (step.position === 'left') {
            next.add(await adapter.sha256Hex(adapter.canonicalize({ left: step.hash, right: candidate })));
          } else {
            next.add(await adapter.sha256Hex(adapter.canonicalize({ left: candidate, right: step.hash })));
          }
        }
        hashCandidates = next;
        if (hashCandidates.size === 0) return false;
      }
      return hashCandidates.has(expectedRoot);
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

    async function verifyReceipt(receipt, options = {}) {
      if (!receipt || typeof receipt !== 'object') {
        throw new Error('Receipt payload must be a JSON object.');
      }
      const record = receipt.record;
      const rootRecord = receipt.root_record || receipt.rootRecord;
      if (!record || !rootRecord) {
        throw new Error('Receipt is missing the signed entry or signed root.');
      }
      if (typeof options.verifyRecord === 'function') {
        await options.verifyRecord(record, 'entry');
      }
      if (typeof options.verifyRootRecord === 'function') {
        await options.verifyRootRecord(rootRecord, 'root');
      }
      const inclusionProof = Array.isArray(receipt.inclusion_proof)
        ? receipt.inclusion_proof
        : Array.isArray(rootRecord.inclusion_proof)
          ? rootRecord.inclusion_proof
          : [];
      const inclusionProofValid = await verifyMerkleProof(
        record.commitment_hash || receipt.entry_commitment_hash || '',
        inclusionProof,
        rootRecord.merkle_root || receipt.merkle_root || ''
      );
      return {
        valid: inclusionProofValid,
        inclusion_proof_valid: inclusionProofValid,
        record_id: record.id || '',
        record_created_at: record.created_at || '',
        root_id: rootRecord.id || '',
        root_created_at: rootRecord.created_at || '',
        merkle_root: rootRecord.merkle_root || receipt.merkle_root || '',
        exported_at: receipt.exported_at || '',
        disclosure: receipt.disclosure || {},
      };
    }

    return {
      buildMerkleState,
      verifyMerkleProof,
      verifySequentialChain,
      buildReceipt,
      verifyReceipt,
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
