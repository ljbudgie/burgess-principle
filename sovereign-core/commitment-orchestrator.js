(function attachIrisSovereignCommitmentOrchestrator(globalScope) {
  // Burgess Compliance: commitments make evidence tamper-evident, but they do not
  // decide whether a human adequately reviewed the user's specific situation.
  const existing = globalScope.IrisSovereignCore || {};
  const utils = existing.utils || {};

  function createCommitmentOrchestrator(adapter) {
    if (!adapter || typeof adapter.sha256Hex !== 'function' || typeof adapter.canonicalize !== 'function') {
      throw new Error('Commitment orchestrator requires sha256Hex and canonicalize adapters.');
    }

    async function createSignedRecord({
      namespace,
      recordId,
      createdAt,
      previousCommitmentHash = '',
      payload,
      signer = null,
      metadata = {},
    }) {
      const signedPayload = {
        namespace: namespace || 'sovereign-record',
        created_at: createdAt || new Date().toISOString(),
        previous_commitment_hash: previousCommitmentHash || '',
        payload,
        payload_hash: await adapter.sha256Hex(adapter.canonicalize(payload)),
        metadata,
        record_version: 1,
      };

      let signatureHex = '';
      let publicKeyHex = '';
      if (signer && typeof signer.signPayload === 'function') {
        const signed = await signer.signPayload(signedPayload);
        signatureHex = signed && signed.signature_hex || '';
        publicKeyHex = signed && signed.public_key_hex || '';
      }

      const commitmentHash = await adapter.sha256Hex(adapter.canonicalize({
        payload: signedPayload,
        signature_hex: signatureHex,
      }));

      return {
        id: recordId || (typeof adapter.generateId === 'function' ? adapter.generateId(namespace || 'sovereign-record') : `${namespace || 'sovereign-record'}-${signedPayload.created_at}`),
        namespace: signedPayload.namespace,
        created_at: signedPayload.created_at,
        previous_commitment_hash: signedPayload.previous_commitment_hash,
        payload,
        payload_hash: signedPayload.payload_hash,
        metadata,
        record_version: signedPayload.record_version,
        signature_hex: signatureHex,
        public_key_hex: publicKeyHex,
        commitment_hash: commitmentHash,
      };
    }

    async function verifySignedRecord(record, options = {}) {
      const payloadHash = await adapter.sha256Hex(adapter.canonicalize(record.payload));
      if (payloadHash !== record.payload_hash) {
        throw new Error(`${record.namespace || 'record'} payload hash mismatch.`);
      }
      const recomputedCommitment = await adapter.sha256Hex(adapter.canonicalize({
        payload: {
          namespace: record.namespace,
          created_at: record.created_at,
          previous_commitment_hash: record.previous_commitment_hash || '',
          payload: record.payload,
          payload_hash: record.payload_hash,
          metadata: record.metadata || {},
          record_version: record.record_version || 1,
        },
        signature_hex: record.signature_hex || '',
      }));
      if (recomputedCommitment !== record.commitment_hash) {
        throw new Error(`${record.namespace || 'record'} commitment mismatch.`);
      }
      if (options.verifySignature && record.signature_hex && record.public_key_hex) {
        const valid = await options.verifySignature({
          payload: {
            namespace: record.namespace,
            created_at: record.created_at,
            previous_commitment_hash: record.previous_commitment_hash || '',
            payload: record.payload,
            payload_hash: record.payload_hash,
            metadata: record.metadata || {},
            record_version: record.record_version || 1,
          },
          signatureHex: record.signature_hex,
          publicKeyHex: record.public_key_hex,
        });
        if (!valid) {
          throw new Error(`${record.namespace || 'record'} signature verification failed.`);
        }
      }
      return true;
    }

    return {
      createSignedRecord,
      verifySignedRecord,
    };
  }

  globalScope.IrisSovereignCore = {
    ...existing,
    createCommitmentOrchestrator,
    commitment: {
      ...(existing.commitment || {}),
      createCommitmentOrchestrator,
      canonicalize: utils.canonicalize,
    },
  };
})(typeof globalThis !== 'undefined' ? globalThis : self);
