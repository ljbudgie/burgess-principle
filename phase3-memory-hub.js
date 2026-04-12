(() => {
  const bridge = window.irisPhaseBridge;
  if (!bridge || !window.crypto || !window.crypto.subtle) {
    return;
  }

  const MEMORY_CRYPTO_SETTING_KEY = 'memory-palace-crypto';
  const MEMORY_ROOT_HEAD_SETTING_KEY = 'memory-palace-root-head';
  const MEMORY_LAST_RECEIPT_ID_KEY = 'memory-palace-last-receipt-id';
  const MEMORY_DERIVED_CURSOR_KEY = 'memory-palace-derived-cursor';
  const HUB_CONFIG_KEY = 'hub-config-v2';
  const HUB_DELTA_CURSOR_KEY = 'hub-delta-cursor-v2';
  const MEMORY_PBKDF2_ITERATIONS = 600000;
  const HUB_PBKDF2_ITERATIONS = 310000;
  const MEMORY_WORKER_URL = '/memory-palace-worker.js';
  const MEMORY_SEARCH_LIMIT = 40;
  const MEMORY_MAX_IMPORTS = 500;
  const MEMORY_ADVISORY_TEXT = 'Memory Palace entries are local, signed, and auditable. Human review remains the final authority.';

  let worker = null;
  let workerRequestId = 0;
  const workerResolvers = new Map();
  let memoryUi = null;
  let memoryPassphraseCache = '';

  function ensureWorker() {
    if (worker) return worker;
    worker = new Worker(MEMORY_WORKER_URL);
    worker.addEventListener('message', event => {
      const { id, result, error } = event.data || {};
      const pending = workerResolvers.get(id);
      if (!pending) return;
      workerResolvers.delete(id);
      if (error) {
        pending.reject(new Error(error));
      } else {
        pending.resolve(result);
      }
    });
    return worker;
  }

  function callWorker(type, payload) {
    const id = `memory-worker-${Date.now()}-${++workerRequestId}`;
    ensureWorker().postMessage({ id, type, payload });
    return new Promise((resolve, reject) => workerResolvers.set(id, { resolve, reject }));
  }

  function escapeHtml(value) {
    return String(value || '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');
  }

  function tagsFromInput(value) {
    return String(value || '').split(',').map(tag => tag.trim().toLowerCase()).filter(Boolean);
  }

  async function deriveWrappingKey(passphrase, salt) {
    const material = await crypto.subtle.importKey(
      'raw',
      new TextEncoder().encode(passphrase),
      'PBKDF2',
      false,
      ['deriveBits']
    );
    const bits = await crypto.subtle.deriveBits(
      { name: 'PBKDF2', salt, iterations: MEMORY_PBKDF2_ITERATIONS, hash: 'SHA-256' },
      material,
      256
    );
    return bridge.toBase64(new Uint8Array(bits));
  }

  async function importAesKey(rawKeyB64, usage) {
    return crypto.subtle.importKey('raw', bridge.fromBase64(rawKeyB64), { name: 'AES-GCM' }, false, usage);
  }

  async function encryptEnvelope(payload, rawKeyB64) {
    const key = await importAesKey(rawKeyB64, ['encrypt']);
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const ciphertext = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      key,
      new TextEncoder().encode(JSON.stringify(payload))
    );
    return {
      encrypted: true,
      algorithm: 'AES-GCM',
      iv: bridge.toBase64(iv),
      ciphertext: bridge.toBase64(new Uint8Array(ciphertext)),
    };
  }

  async function decryptEnvelope(envelope, rawKeyB64) {
    const key = await importAesKey(rawKeyB64, ['decrypt']);
    const plaintext = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: bridge.fromBase64(envelope.iv) },
      key,
      bridge.fromBase64(envelope.ciphertext)
    );
    return JSON.parse(new TextDecoder().decode(plaintext));
  }

  async function ensureMemoryCryptoProfile(passphrase, allowBackgroundUnlock) {
    const existing = await bridge.vaultStore.getSetting(MEMORY_CRYPTO_SETTING_KEY);
    if (existing && existing.wrapped_key) {
      if (allowBackgroundUnlock && !existing.background_key_b64 && passphrase) {
        const wrappingKey = await deriveWrappingKey(passphrase, bridge.fromBase64(existing.salt));
        const unlocked = await decryptEnvelope(existing.wrapped_key, wrappingKey);
        existing.background_key_b64 = unlocked.master_key_b64;
        existing.background_unlock_enabled = true;
        existing.updated_at = new Date().toISOString();
        await bridge.vaultStore.saveSetting(MEMORY_CRYPTO_SETTING_KEY, existing);
      }
      return existing;
    }
    if (!passphrase) {
      throw new Error('Enter the Memory Palace passphrase to create the encrypted memory ledger.');
    }
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const masterKeyB64 = bridge.toBase64(crypto.getRandomValues(new Uint8Array(32)));
    const wrappingKeyB64 = await deriveWrappingKey(passphrase, salt);
    const signingKeys = await crypto.subtle.generateKey({ name: 'Ed25519' }, true, ['sign', 'verify']);
    const signingPrivateJwk = await crypto.subtle.exportKey('jwk', signingKeys.privateKey);
    const signingPublicRaw = new Uint8Array(await crypto.subtle.exportKey('raw', signingKeys.publicKey));
    const profile = {
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      salt: bridge.toBase64(salt),
      wrapped_key: await encryptEnvelope({ master_key_b64: masterKeyB64 }, wrappingKeyB64),
      background_unlock_enabled: Boolean(allowBackgroundUnlock),
      background_key_b64: allowBackgroundUnlock ? masterKeyB64 : '',
      signing_private_key_jwk: signingPrivateJwk,
      signing_public_key_hex: bridge.bytesToHex(signingPublicRaw),
    };
    await bridge.vaultStore.saveSetting(MEMORY_CRYPTO_SETTING_KEY, profile);
    return profile;
  }

  async function resolveMemoryMasterKey(passphrase = '') {
    const profile = await bridge.vaultStore.getSetting(MEMORY_CRYPTO_SETTING_KEY);
    if (!profile || typeof profile !== 'object') return null;
    if (profile.background_key_b64) return profile.background_key_b64;
    if (!passphrase) return null;
    const wrappingKey = await deriveWrappingKey(passphrase, bridge.fromBase64(profile.salt));
    const unlocked = await decryptEnvelope(profile.wrapped_key, wrappingKey);
    return unlocked.master_key_b64;
  }

  async function importMemorySigningKey() {
    const profile = await bridge.vaultStore.getSetting(MEMORY_CRYPTO_SETTING_KEY);
    if (!profile || !profile.signing_private_key_jwk) {
      throw new Error('Memory Palace signing identity is missing. Recreate the encrypted memory ledger.');
    }
    return {
      profile,
      key: await crypto.subtle.importKey('jwk', profile.signing_private_key_jwk, { name: 'Ed25519' }, false, ['sign'])
    };
  }

  async function signCanonicalPayload(payload) {
    const imported = await importMemorySigningKey();
    const encoded = new TextEncoder().encode(bridge.canonicalizeForSignature(payload));
    const signature = await crypto.subtle.sign('Ed25519', imported.key, encoded);
    return {
      signature_hex: bridge.bytesToHex(new Uint8Array(signature)),
      public_key_hex: imported.profile.signing_public_key_hex,
    };
  }

  function setMemoryStatus(message, tone = '') {
    if (!memoryUi) return;
    memoryUi.status.textContent = message;
    memoryUi.status.className = 'claim-profile-status' + (tone ? ` is-${tone}` : '');
    bridge.announceStatus(message);
  }

  function setHubStatus(message, tone = '') {
    const statusEl = document.getElementById('hubStatus');
    if (!statusEl) return;
    statusEl.textContent = message;
    statusEl.className = 'claim-profile-status' + (tone ? ` is-${tone}` : '');
  }

  function getMemoryPassphrase() {
    const value = memoryUi && memoryUi.passphrase ? memoryUi.passphrase.value.trim() : '';
    if (value) memoryPassphraseCache = value;
    return value || memoryPassphraseCache;
  }

  async function buildMerkleState(leaves, index) {
    const result = await callWorker('merkle-state', { leaves, index });
    return result || { root: '', proof: [] };
  }

  async function appendMemoryEntry(options) {
    const passphrase = options.passphrase || getMemoryPassphrase();
    const allowBackgroundUnlock = Boolean(memoryUi.backgroundUnlock.checked);
    await ensureMemoryCryptoProfile(passphrase, allowBackgroundUnlock);
    const masterKey = await resolveMemoryMasterKey(passphrase);
    if (!masterKey) {
      throw new Error('Unlock the Memory Palace first.');
    }
    const entries = (await bridge.vaultStore.getAll('memoryEntries')).sort((a, b) => Date.parse(a.created_at || 0) - Date.parse(b.created_at || 0));
    const previous = entries[entries.length - 1] || null;
    const createdAt = new Date().toISOString();
    const payload = {
      title: options.title || 'Memory entry',
      summary: options.summary || '',
      detail: options.detail || '',
      tags: options.tags || [],
      source: options.source || 'manual',
      metadata: options.metadata || {},
    };
    const encrypted_payload = await encryptEnvelope(payload, masterKey);
    const signed_payload = {
      id: bridge.generateSecureId('memory-entry'),
      type: options.type || 'note',
      source: options.source || 'manual',
      source_ref: options.source_ref || '',
      created_at: createdAt,
      prev_hash: previous ? previous.commitment_hash : '',
      encrypted_hash: await bridge.sha256Hex(bridge.canonicalizeForSignature(encrypted_payload)),
      metadata: options.metadata || {},
      entry_version: 1,
    };
    const signed = await signCanonicalPayload(signed_payload);
    const commitment_hash = await bridge.sha256Hex(bridge.canonicalizeForSignature({ payload: signed_payload, signature_hex: signed.signature_hex }));
    const entry = {
      id: signed_payload.id,
      type: signed_payload.type,
      source: signed_payload.source,
      source_ref: signed_payload.source_ref,
      created_at: createdAt,
      prev_hash: signed_payload.prev_hash,
      encrypted_payload,
      signed_payload,
      signature_hex: signed.signature_hex,
      public_key_hex: signed.public_key_hex,
      commitment_hash,
    };
    await bridge.vaultStore.put('memoryEntries', entry);

    const nextLeaves = [...entries.map(item => item.commitment_hash), commitment_hash];
    const merkleState = await buildMerkleState(nextLeaves, nextLeaves.length - 1);
    const roots = (await bridge.vaultStore.getAll('memoryRoots')).sort((a, b) => Date.parse(a.created_at || 0) - Date.parse(b.created_at || 0));
    const previousRoot = roots[roots.length - 1] || null;
    const rootPayload = {
      id: bridge.generateSecureId('memory-root'),
      entry_id: entry.id,
      created_at: createdAt,
      merkle_root: merkleState.root,
      prev_root_commitment_hash: previousRoot ? previousRoot.root_commitment_hash : '',
      leaf_count: nextLeaves.length,
      latest_entry_hash: commitment_hash,
      root_version: 1,
    };
    const rootSigned = await signCanonicalPayload(rootPayload);
    const rootCommitmentHash = await bridge.sha256Hex(bridge.canonicalizeForSignature({ payload: rootPayload, signature_hex: rootSigned.signature_hex }));
    const rootRecord = {
      id: rootPayload.id,
      entry_id: entry.id,
      created_at: createdAt,
      merkle_root: merkleState.root,
      prev_root_commitment_hash: rootPayload.prev_root_commitment_hash,
      leaf_count: rootPayload.leaf_count,
      latest_entry_hash: commitment_hash,
      signed_payload: rootPayload,
      signature_hex: rootSigned.signature_hex,
      public_key_hex: rootSigned.public_key_hex,
      root_commitment_hash: rootCommitmentHash,
      inclusion_proof: merkleState.proof,
    };
    await bridge.vaultStore.put('memoryRoots', rootRecord);
    await bridge.vaultStore.saveSetting(MEMORY_ROOT_HEAD_SETTING_KEY, rootCommitmentHash);

    const receipt = {
      id: bridge.generateSecureId('memory-receipt'),
      created_at: createdAt,
      entry_id: entry.id,
      entry_commitment_hash: commitment_hash,
      root_commitment_hash: rootCommitmentHash,
      merkle_root: merkleState.root,
      inclusion_proof: merkleState.proof,
      signed_entry: entry,
      signed_root: rootRecord,
    };
    await bridge.vaultStore.put('memoryReceipts', receipt);
    await bridge.vaultStore.saveSetting(MEMORY_LAST_RECEIPT_ID_KEY, receipt.id);
    return { entry, rootRecord, receipt };
  }

  async function decryptMemoryEntry(entry, passphrase = getMemoryPassphrase()) {
    const masterKey = await resolveMemoryMasterKey(passphrase);
    if (!masterKey) {
      throw new Error('Enter the Memory Palace passphrase to unlock local memory content.');
    }
    return decryptEnvelope(entry.encrypted_payload, masterKey);
  }

  async function renderMemoryTimeline(query = '') {
    const entries = (await bridge.vaultStore.getAll('memoryEntries')).sort((a, b) => Date.parse(b.created_at || 0) - Date.parse(a.created_at || 0));
    let displayEntries = entries.slice(0, MEMORY_SEARCH_LIMIT);
    if (query.trim()) {
      const enriched = [];
      for (const entry of entries) {
        try {
          const decrypted = await decryptMemoryEntry(entry);
          enriched.push({
            id: entry.id,
            title: decrypted.title,
            summary: decrypted.summary,
            detail: decrypted.detail,
            tags: decrypted.tags || [],
            created_at: entry.created_at,
            commitment_hash: entry.commitment_hash,
          });
        } catch {
          // Search requires successful unlock.
        }
      }
      const results = await callWorker('search', { query, entries: enriched });
      const ids = new Set((results || []).map(item => item.id));
      displayEntries = entries.filter(entry => ids.has(entry.id)).slice(0, MEMORY_SEARCH_LIMIT);
    }

    if (!displayEntries.length) {
      memoryUi.timeline.innerHTML = '<div class="trigger-ledger-item">No committed memories match yet.</div>';
      return;
    }

    const fragments = [];
    for (const entry of displayEntries) {
      let decrypted = null;
      try {
        decrypted = await decryptMemoryEntry(entry);
      } catch {
        decrypted = null;
      }
      fragments.push(`
        <div class="trigger-ledger-item">
          <strong>${escapeHtml(decrypted ? decrypted.title : entry.type)}</strong> · ${escapeHtml(new Date(entry.created_at).toLocaleString())}<br>
          ${escapeHtml(decrypted ? (decrypted.summary || decrypted.detail || 'Encrypted memory entry') : 'Locked memory entry — unlock to inspect content.')}<br>
          <code>${escapeHtml(entry.commitment_hash)}</code>
        </div>
      `);
    }
    memoryUi.timeline.innerHTML = fragments.join('');
  }

  async function verifySignatureHex(publicKeyHex, signatureHex, payload) {
    const key = await crypto.subtle.importKey('raw', bridge.hexToBytes(publicKeyHex), { name: 'Ed25519' }, false, ['verify']);
    return crypto.subtle.verify(
      'Ed25519',
      key,
      bridge.hexToBytes(signatureHex),
      new TextEncoder().encode(bridge.canonicalizeForSignature(payload))
    );
  }

  async function verifyMemoryIntegrity() {
    const entries = (await bridge.vaultStore.getAll('memoryEntries')).sort((a, b) => Date.parse(a.created_at || 0) - Date.parse(b.created_at || 0));
    const roots = (await bridge.vaultStore.getAll('memoryRoots')).sort((a, b) => Date.parse(a.created_at || 0) - Date.parse(b.created_at || 0));
    let previousHash = '';
    for (const entry of entries) {
      if (entry.signed_payload.prev_hash !== previousHash) {
        throw new Error(`Memory entry ${entry.id} broke the commitment chain.`);
      }
      const validSignature = await verifySignatureHex(entry.public_key_hex, entry.signature_hex, entry.signed_payload);
      if (!validSignature) {
        throw new Error(`Memory entry ${entry.id} failed Ed25519 verification.`);
      }
      const recomputed = await bridge.sha256Hex(bridge.canonicalizeForSignature({ payload: entry.signed_payload, signature_hex: entry.signature_hex }));
      if (recomputed !== entry.commitment_hash) {
        throw new Error(`Memory entry ${entry.id} has an invalid SHA-256 commitment.`);
      }
      previousHash = entry.commitment_hash;
    }
    const merkleState = await buildMerkleState(entries.map(entry => entry.commitment_hash), Math.max(entries.length - 1, 0));
    if (entries.length && roots.length) {
      const latestRoot = roots[roots.length - 1];
      const validRootSignature = await verifySignatureHex(latestRoot.public_key_hex, latestRoot.signature_hex, latestRoot.signed_payload);
      if (!validRootSignature) {
        throw new Error('Latest Memory Palace root failed Ed25519 verification.');
      }
      if (latestRoot.merkle_root !== merkleState.root) {
        throw new Error('Latest Memory Palace root does not match the recomputed Merkle root.');
      }
    }
    return {
      entries: entries.length,
      roots: roots.length,
      merkle_root: merkleState.root || '',
    };
  }

  async function verifyTriggerLedgerChain() {
    const ledger = (await bridge.vaultStore.getAll('triggerLedger')).sort((a, b) => Date.parse(a.created_at || 0) - Date.parse(b.created_at || 0));
    let previous = '';
    for (const entry of ledger) {
      if (entry.previous_commitment_hash !== previous) {
        throw new Error(`Trigger ledger continuity broke at ${entry.id}.`);
      }
      previous = entry.commitment_hash;
    }
    return ledger.length;
  }

  async function runFullSystemIntegrityCheck() {
    const memoryResult = await verifyMemoryIntegrity();
    const triggerCount = await verifyTriggerLedgerChain();
    const queuedHub = await bridge.vaultStore.getAll('hubSyncQueue');
    setMemoryStatus(
      `Integrity check passed from genesis. ${memoryResult.entries} memories, ${memoryResult.roots} roots, ${triggerCount} trigger ledger events, ${queuedHub.filter(item => item.status === 'queued').length} queued hub syncs.`,
      'success'
    );
  }

  async function exportLatestMemoryReceipt() {
    const latestReceiptId = await bridge.vaultStore.getSetting(MEMORY_LAST_RECEIPT_ID_KEY);
    const receipt = latestReceiptId ? await bridge.vaultStore.get('memoryReceipts', latestReceiptId) : null;
    if (!receipt) {
      throw new Error('No Memory Palace receipt exists yet. Add or import a committed memory first.');
    }
    const blob = new Blob([JSON.stringify(receipt, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `iris-memory-receipt-${receipt.entry_id}.json`;
    link.click();
    URL.revokeObjectURL(url);
    setMemoryStatus('Exported the latest signed Memory Palace receipt. Nothing leaves the device unless you share the file.', 'success');
  }

  async function loadDerivedCursor() {
    return await bridge.vaultStore.getSetting(MEMORY_DERIVED_CURSOR_KEY) || {
      claims: [],
      triggerLedger: [],
      hubAudit: [],
      profileFingerprint: '',
      themeFingerprint: '',
      hubEnvironmentFingerprint: '',
    };
  }

  async function saveDerivedCursor(cursor) {
    const compact = {
      claims: cursor.claims.slice(-MEMORY_MAX_IMPORTS),
      triggerLedger: cursor.triggerLedger.slice(-MEMORY_MAX_IMPORTS),
      hubAudit: cursor.hubAudit.slice(-MEMORY_MAX_IMPORTS),
      profileFingerprint: cursor.profileFingerprint || '',
      themeFingerprint: cursor.themeFingerprint || '',
      hubEnvironmentFingerprint: cursor.hubEnvironmentFingerprint || '',
    };
    await bridge.vaultStore.saveSetting(MEMORY_DERIVED_CURSOR_KEY, compact);
  }

  function getHubEnvironmentPreferences() {
    return {
      connectivity_profile: document.getElementById('hubConnectivityProfile')?.value || 'starlink_ethernet',
      low_wireless_mode: Boolean(document.getElementById('hubLowWirelessToggle')?.checked),
      prefer_queued_syncs: Boolean(document.getElementById('hubQueuedSyncPreferenceToggle')?.checked),
      connectivity_note: (document.getElementById('hubConnectivityNote')?.value || '').trim(),
    };
  }

  function hubEnvironmentSummary(preferences = getHubEnvironmentPreferences()) {
    const parts = [];
    if (preferences.connectivity_profile === 'starlink_ethernet') {
      parts.push('Starlink + Ethernet selected for local review');
    } else if (preferences.connectivity_profile === 'wired_router') {
      parts.push('wired router profile selected for local review');
    } else if (preferences.connectivity_profile === 'wifi') {
      parts.push('Wi‑Fi profile selected for local review');
    } else if (preferences.connectivity_profile === 'cellular_fallback') {
      parts.push('cellular fallback profile selected for local review');
    }
    if (preferences.low_wireless_mode) parts.push('minimized local wireless environment requested');
    if (preferences.prefer_queued_syncs) parts.push('queued/manual sync preference enabled');
    if (preferences.connectivity_note) parts.push(preferences.connectivity_note);
    return parts.join('; ');
  }

  async function persistHubEnvironmentPreferences() {
    const existing = await loadHubConfig() || {};
    const merged = {
      ...existing,
      ...getHubEnvironmentPreferences(),
      updated_at: new Date().toISOString(),
    };
    await saveHubConfig(merged);
    if (document.getElementById('hubModeToggle')?.checked) {
      setHubStatus(`Hub preferences saved locally. ${hubEnvironmentSummary(merged) || 'Commitment-only sync remains manual-first.'}`);
    }
  }

  async function syncDerivedMemorySources() {
    const passphrase = getMemoryPassphrase();
    if (!passphrase) {
      renderMemoryTimeline().catch(() => undefined);
      return;
    }
    await ensureMemoryCryptoProfile(passphrase, Boolean(memoryUi.backgroundUnlock.checked));
    const cursor = await loadDerivedCursor();

    const claims = await bridge.vaultStore.getAll('claims');
    for (const claim of claims) {
      if (!claim.id || cursor.claims.includes(claim.id)) continue;
      await appendMemoryEntry({
        type: 'claim',
        source: 'claim',
        source_ref: claim.id,
        title: `Claim committed ${claim.template || ''}`.trim(),
        summary: `Claim ${claim.commitment_hash || claim.id} was saved into the local sovereign vault.`,
        detail: `${MEMORY_ADVISORY_TEXT} Burgess reference: ${claim.commitment_hash || 'pending'}`,
        tags: ['claim', claim.template || 'vault'],
        metadata: { commitment_hash: claim.commitment_hash || '', template: claim.template || '' },
        passphrase,
      });
      cursor.claims.push(claim.id);
    }

    const triggerLedger = await bridge.vaultStore.getAll('triggerLedger');
    for (const item of triggerLedger) {
      if (!item.id || cursor.triggerLedger.includes(item.id)) continue;
      await appendMemoryEntry({
        type: 'trigger',
        source: 'trigger-ledger',
        source_ref: item.id,
        title: `Trigger ${item.event_type}`,
        summary: item.evidence_excerpt || `${item.label || 'Trigger'} ${item.event_type}`,
        detail: `Trigger commitment ${item.commitment_hash}. ${MEMORY_ADVISORY_TEXT}`,
        tags: ['trigger', item.source || 'local'],
        metadata: { commitment_hash: item.commitment_hash || '', trigger_id: item.trigger_id || '' },
        passphrase,
      });
      cursor.triggerLedger.push(item.id);
    }

    const hubAudit = await bridge.vaultStore.getAll('hubAudit');
    for (const item of hubAudit) {
      if (!item.id || cursor.hubAudit.includes(item.id)) continue;
      await appendMemoryEntry({
        type: 'hub-sync',
        source: 'hub-audit',
        source_ref: item.id,
        title: `Hub ${item.direction || 'sync'} ${item.status || 'event'}`,
        summary: item.summary || 'Sovereign Hub coordination event recorded.',
        detail: `Hub audit ${item.commitment_hash || item.id}. ${MEMORY_ADVISORY_TEXT}`,
        tags: ['hub', item.direction || 'sync'],
        metadata: { commitment_hash: item.commitment_hash || '', hub_event_id: item.id },
        passphrase,
      });
      cursor.hubAudit.push(item.id);
    }

    const profile = await bridge.vaultStore.getSetting('personal-sovereign-profile-summary');
    const profileFingerprint = profile ? await bridge.sha256Hex(bridge.canonicalizeForSignature(profile)) : '';
    if (profileFingerprint && profileFingerprint !== cursor.profileFingerprint) {
      await appendMemoryEntry({
        type: 'governance',
        source: 'mirror-mode',
        source_ref: 'personal-sovereign-profile-summary',
        title: 'Mirror identity updated',
        summary: `${bridge.getMirrorGreeting() || 'Mirror identity changed on this device.'}`,
        detail: 'Mirror rights mapping and identity preferences were recommitted into the local Memory Palace.',
        tags: ['mirror', 'identity'],
        metadata: { profile_fingerprint: profileFingerprint },
        passphrase,
      });
      cursor.profileFingerprint = profileFingerprint;
    }

    const highContrast = await bridge.vaultStore.getSetting('high-contrast');
    const themeFingerprint = await bridge.sha256Hex(bridge.canonicalizeForSignature({ highContrast: Boolean(highContrast) }));
    if (themeFingerprint !== cursor.themeFingerprint) {
      await appendMemoryEntry({
        type: 'governance',
        source: 'settings',
        source_ref: 'high-contrast',
        title: 'Governance toggle changed',
        summary: `High contrast is now ${highContrast ? 'enabled' : 'disabled'} on this sovereign shell.`,
        detail: 'The Memory Palace recommitted a local governance preference change.',
        tags: ['governance', 'settings'],
        metadata: { high_contrast: Boolean(highContrast) },
        passphrase,
      });
      cursor.themeFingerprint = themeFingerprint;
    }

    const hubEnvironment = await loadHubConfig();
    const hubEnvironmentFingerprint = hubEnvironment
      ? await bridge.sha256Hex(bridge.canonicalizeForSignature({
        connectivity_profile: hubEnvironment.connectivity_profile || '',
        low_wireless_mode: Boolean(hubEnvironment.low_wireless_mode),
        prefer_queued_syncs: Boolean(hubEnvironment.prefer_queued_syncs),
        connectivity_note: hubEnvironment.connectivity_note || '',
      }))
      : '';
    if (hubEnvironmentFingerprint && hubEnvironmentFingerprint !== cursor.hubEnvironmentFingerprint) {
      await appendMemoryEntry({
        type: 'environment',
        source: 'hub-settings',
        source_ref: 'hub-connectivity-profile',
        title: 'Connectivity environment updated',
        summary: hubEnvironmentSummary(hubEnvironment) || 'Connectivity preferences updated for local review.',
        detail: 'The Memory Palace recommitted a local connectivity and environmental preference change for later human review.',
        tags: ['environment', 'connectivity'],
        metadata: {
          connectivity_profile: hubEnvironment.connectivity_profile || '',
          low_wireless_mode: Boolean(hubEnvironment.low_wireless_mode),
          prefer_queued_syncs: Boolean(hubEnvironment.prefer_queued_syncs),
        },
        passphrase,
      });
      cursor.hubEnvironmentFingerprint = hubEnvironmentFingerprint;
    }

    await saveDerivedCursor(cursor);
    await renderMemoryTimeline(memoryUi.search.value || '');
  }

  async function deriveHubKey(secret, salt) {
    const material = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), 'PBKDF2', false, ['deriveKey']);
    return crypto.subtle.deriveKey(
      { name: 'PBKDF2', salt, iterations: HUB_PBKDF2_ITERATIONS, hash: 'SHA-256' },
      material,
      { name: 'AES-GCM', length: 256 },
      false,
      ['encrypt', 'decrypt']
    );
  }

  async function hubEncrypt(payload, secret) {
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const key = await deriveHubKey(secret, salt);
    const ciphertext = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      key,
      new TextEncoder().encode(JSON.stringify(payload))
    );
    return {
      salt: bridge.toBase64(salt),
      iv: bridge.toBase64(iv),
      ciphertext: bridge.toBase64(new Uint8Array(ciphertext)),
    };
  }

  async function hubDecrypt(envelope, secret) {
    const key = await deriveHubKey(secret, bridge.fromBase64(envelope.salt));
    const plaintext = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: bridge.fromBase64(envelope.iv) },
      key,
      bridge.fromBase64(envelope.ciphertext)
    );
    return JSON.parse(new TextDecoder().decode(plaintext));
  }

  async function ensureHubIdentity() {
    const existing = await bridge.vaultStore.getSetting('hub-client-identity-v2');
    if (existing && existing.private_key_jwk && existing.public_key_hex) return existing;
    const keyPair = await crypto.subtle.generateKey({ name: 'Ed25519' }, true, ['sign', 'verify']);
    const identity = {
      private_key_jwk: await crypto.subtle.exportKey('jwk', keyPair.privateKey),
      public_key_hex: bridge.bytesToHex(new Uint8Array(await crypto.subtle.exportKey('raw', keyPair.publicKey))),
      device_id: bridge.generateSecureId('hub-device'),
      created_at: new Date().toISOString(),
    };
    await bridge.vaultStore.saveSetting('hub-client-identity-v2', identity);
    return identity;
  }

  async function signHubPayload(payload) {
    const identity = await ensureHubIdentity();
    const privateKey = await crypto.subtle.importKey('jwk', identity.private_key_jwk, { name: 'Ed25519' }, false, ['sign']);
    const signature = await crypto.subtle.sign('Ed25519', privateKey, new TextEncoder().encode(bridge.canonicalizeForSignature(payload)));
    return {
      device_id: identity.device_id,
      public_key_hex: identity.public_key_hex,
      signature_hex: bridge.bytesToHex(new Uint8Array(signature)),
    };
  }

  async function verifyHubSignature(publicKeyHex, payload, signatureHex) {
    const key = await crypto.subtle.importKey('raw', bridge.hexToBytes(publicKeyHex), { name: 'Ed25519' }, false, ['verify']);
    return crypto.subtle.verify('Ed25519', key, bridge.hexToBytes(signatureHex), new TextEncoder().encode(bridge.canonicalizeForSignature(payload)));
  }

  async function loadHubConfig() {
    return await bridge.vaultStore.getSetting(HUB_CONFIG_KEY) || null;
  }

  async function saveHubConfig(config) {
    await bridge.vaultStore.saveSetting(HUB_CONFIG_KEY, config);
  }

  async function buildHubDeltaBundle(direction) {
    const latestRoot = (await bridge.vaultStore.getAll('memoryRoots')).sort((a, b) => Date.parse(b.created_at || 0) - Date.parse(a.created_at || 0))[0] || null;
    const triggerLedger = (await bridge.vaultStore.getAll('triggerLedger')).sort((a, b) => Date.parse(b.created_at || 0) - Date.parse(a.created_at || 0));
    const claims = (await bridge.vaultStore.getAll('claims')).map(item => ({
      id: item.id,
      commitment_hash: item.commitment_hash || '',
      created_at: item.created_at || '',
      template: item.template || '',
    }));
    const triggers = (await bridge.vaultStore.getAll('triggers')).map(item => ({
      id: item.id,
      label: item.label,
      type: item.type,
      keywords_hash: item.keywords_hash || '',
      chain_head: item.chain_head || '',
    }));
    const deltaCursor = await bridge.vaultStore.getSetting(HUB_DELTA_CURSOR_KEY) || '';
    return {
      direction,
      exported_at: new Date().toISOString(),
      delta_cursor: deltaCursor,
      memory_root: latestRoot ? {
        root_commitment_hash: latestRoot.root_commitment_hash,
        merkle_root: latestRoot.merkle_root,
        leaf_count: latestRoot.leaf_count,
        latest_entry_hash: latestRoot.latest_entry_hash,
      } : null,
      trigger_head: triggerLedger[0] ? {
        commitment_hash: triggerLedger[0].commitment_hash,
        created_at: triggerLedger[0].created_at,
      } : null,
      claims,
      triggers,
    };
  }

  async function recordHubAudit(direction, status, summary, extra = {}) {
    const auditPayload = {
      direction,
      status,
      summary,
      created_at: new Date().toISOString(),
      extra,
    };
    const commitment_hash = await bridge.sha256Hex(bridge.canonicalizeForSignature(auditPayload));
    const audit = {
      id: bridge.generateSecureId('hub-audit'),
      direction,
      status,
      summary,
      created_at: auditPayload.created_at,
      commitment_hash,
      extra,
    };
    await bridge.vaultStore.put('hubAudit', audit);
    return audit;
  }

  async function enqueueHubSyncRequest(payload) {
    const queueItem = {
      id: bridge.generateSecureId('hub-sync'),
      created_at: new Date().toISOString(),
      status: 'queued',
      ...payload,
    };
    await bridge.vaultStore.put('hubSyncQueue', queueItem);
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.ready;
        if ('sync' in registration) {
          await registration.sync.register('burgess-hub-sync');
        }
      } catch {
        // iOS/Safari fallback: queue remains local until manual retry.
      }
    }
    return queueItem;
  }

  async function sendQueuedRequest(item) {
    const response = await fetch(item.url, {
      method: item.method,
      headers: item.headers,
      body: item.body,
    });
    if (!response.ok) {
      throw new Error(`Hub returned ${response.status}`);
    }
    return response.json();
  }

  async function performHubSync(direction) {
    const url = (document.getElementById('hubUrl')?.value || '').trim();
    const sharedSecret = (document.getElementById('hubSharedSecret')?.value || '').trim();
    const publicKeyHex = (document.getElementById('hubPublicKey')?.value || '').trim();
    if (!url || !sharedSecret || !publicKeyHex) {
      throw new Error('Hub URL, shared secret, and pinned public key are required.');
    }
    const environmentPreferences = getHubEnvironmentPreferences();
    const bundle = await buildHubDeltaBundle(direction);
    const envelope = await hubEncrypt(bundle, sharedSecret);
    const signedRequest = {
      direction,
      created_at: new Date().toISOString(),
      envelope_hash: await bridge.sha256Hex(bridge.canonicalizeForSignature(envelope)),
      delta_cursor: bundle.delta_cursor,
    };
    const clientSignature = await signHubPayload(signedRequest);
    const requestBody = JSON.stringify({ envelope, signed_request: signedRequest, client_signature: clientSignature });
    const request = {
      url: `${url.replace(/\/+$/, '')}/api/sovereign-sync-v2`,
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: requestBody,
      direction,
    };

    setHubStatus(`${direction === 'push' ? 'Pushing' : 'Pulling'} commitments to your Sovereign Hub…`);
    try {
      const data = await sendQueuedRequest(request);
      if (!data.payload || !data.signature_hex || !data.signed_response) {
        throw new Error('Hub response was missing its signed encrypted payload.');
      }
      const valid = await verifyHubSignature(publicKeyHex, data.signed_response, data.signature_hex);
      if (!valid) {
        throw new Error('Hub response signature did not match the pinned public key.');
      }
      const decrypted = await hubDecrypt(data.payload, sharedSecret);
      await bridge.vaultStore.saveSetting(HUB_DELTA_CURSOR_KEY, decrypted.next_cursor || '');
      await saveHubConfig({ url, public_key_hex: publicKeyHex, ...environmentPreferences, updated_at: new Date().toISOString() });
      await recordHubAudit(direction, 'verified', `${direction === 'push' ? 'Pushed' : 'Pulled'} ${decrypted.received || 0} commitment deltas with signature verification.`, {
        next_cursor: decrypted.next_cursor || '',
        received: decrypted.received || 0,
        remote_deltas: decrypted.remote_deltas || {},
      });
      setHubStatus(`${direction === 'push' ? 'Push' : 'Pull'} verified. ${decrypted.received || 0} commitment deltas acknowledged by your hub.`, 'success');
      await syncDerivedMemorySources();
    } catch (error) {
      await enqueueHubSyncRequest(request);
      await recordHubAudit(direction, 'queued', `Queued a ${direction} sync after a connectivity or verification failure.`, { error: error.message });
      setHubStatus(`Hub ${direction} queued locally: ${error.message}`, 'error');
    }
  }

  async function flushQueuedHubSyncs() {
    const queue = (await bridge.vaultStore.getAll('hubSyncQueue')).filter(item => item.status === 'queued');
    if (!queue.length) {
      setHubStatus('No queued hub syncs are waiting right now.');
      return;
    }
    let flushed = 0;
    for (const item of queue) {
      try {
        await sendQueuedRequest(item);
        item.status = 'completed';
        item.completed_at = new Date().toISOString();
        await bridge.vaultStore.put('hubSyncQueue', item);
        flushed += 1;
      } catch {
        item.last_attempt_at = new Date().toISOString();
        await bridge.vaultStore.put('hubSyncQueue', item);
      }
    }
    await recordHubAudit('queue', flushed > 0 ? 'flushed' : 'pending', `Hub queue flush attempted. ${flushed} request(s) sent.`, { flushed });
    setHubStatus(flushed > 0 ? `Flushed ${flushed} queued hub sync request(s).` : 'Queued hub syncs still need connectivity or a working hub endpoint.', flushed > 0 ? 'success' : 'error');
  }

  function injectMemoryPalaceUi() {
    const target = document.getElementById('hubModePanel');
    if (!target || document.getElementById('memoryPalacePanel')) return;
    target.insertAdjacentHTML('beforebegin', `
      <details class="claim-profile-panel" id="memoryPalacePanel">
        <summary>🏛️ Memory Palace</summary>
        <p class="claim-profile-desc">Commitment-chained long-term memory for Iris. Every entry is encrypted, Merkle-rooted, SHA-256 committed, and Ed25519 signed on this device.</p>
        <div class="claim-profile-actions" style="flex-direction:column;align-items:stretch;">
          <div class="claim-field"><label for="memoryPalacePassphrase">Memory Palace passphrase</label><input id="memoryPalacePassphrase" type="password" placeholder="Required to seal and unlock committed memories"></div>
          <label class="toggle-row" for="memoryBackgroundUnlockToggle"><input id="memoryBackgroundUnlockToggle" type="checkbox"> Allow device-only background unlock for Memory Palace roots</label>
          <div class="claim-field"><label for="memoryTitleInput">Memory title</label><input id="memoryTitleInput" type="text" placeholder="e.g. Voice check-in before DWP call or environmental note"></div>
          <div class="claim-field"><label for="memorySummaryInput">Summary</label><input id="memorySummaryInput" type="text" placeholder="Short local summary for the committed memory or connectivity review"></div>
          <div class="claim-field"><label for="memoryDetailInput">Detail</label><textarea id="memoryDetailInput" rows="3" placeholder="Longer private note to encrypt into the Memory Palace"></textarea></div>
          <div class="claim-field"><label for="memoryTagsInput">Tags (comma-separated)</label><input id="memoryTagsInput" type="text" placeholder="benefits, mirror, trigger, environment"></div>
          <div class="claim-field"><label for="memoryEnvironmentalContextInput">Environmental note</label><input id="memoryEnvironmentalContextInput" type="text" placeholder="Optional note about connectivity, Wi-Fi off, dish placement, comfort, or focus"></div>
          <div class="claim-profile-actions">
            <button class="sidebar-action-btn" id="memoryAddBtn" type="button">➕ Commit memory</button>
            <button class="sidebar-action-btn" id="memoryEnvironmentalNoteBtn" type="button">🌿 Commit environmental note</button>
            <button class="sidebar-action-btn" id="memoryRefreshBtn" type="button">🔓 Unlock & refresh</button>
            <button class="sidebar-action-btn" id="memoryVerifyBtn" type="button">🧪 Verify integrity</button>
            <button class="sidebar-action-btn" id="memoryFullIntegrityBtn" type="button">🛡️ Full system integrity check</button>
            <button class="sidebar-action-btn" id="memoryExportBtn" type="button">🧾 Export latest memory receipt</button>
          </div>
          <div class="claim-field"><label for="memorySearchInput">Search committed memory</label><input id="memorySearchInput" type="text" placeholder="Search local decrypted memories after unlocking"></div>
        </div>
        <div class="trigger-ledger" id="memoryTimelineList"></div>
        <div class="claim-profile-status" id="memoryStatus">The Memory Palace is local-only. Unlock it with a passphrase to inspect or search encrypted memories.</div>
      </details>
    `);

    const hubPanel = document.getElementById('hubModePanel');
    const hubActions = hubPanel.querySelector('.claim-profile-actions');
    hubActions.insertAdjacentHTML('beforeend', `
      <div class="claim-field" id="hubPublicKeyField" style="display:none;"><label for="hubPublicKey">Pinned hub Ed25519 public key</label><input id="hubPublicKey" type="text" placeholder="Paste the hub public key you verified out-of-band"></div>
      <div class="claim-field" id="hubPairingField" style="display:none;"><label for="hubPairingCode">Pairing code (JSON)</label><textarea id="hubPairingCode" rows="3" placeholder='{"url":"https://iris-hub.tailnet.ts.net","public_key_hex":"..."}'></textarea></div>
      <div class="claim-profile-actions" id="hubAdvancedActions" style="display:none;">
        <button class="sidebar-action-btn" id="hubApplyPairingBtn" type="button">📎 Apply pairing code</button>
        <button class="sidebar-action-btn" id="hubPushBtn" type="button">⬆️ Push commitments</button>
        <button class="sidebar-action-btn" id="hubPullBtn" type="button">⬇️ Pull commitments</button>
        <button class="sidebar-action-btn" id="hubFlushQueueBtn" type="button">📡 Flush queued syncs</button>
      </div>
      <div class="claim-profile-status" id="hubQueueStatus" style="display:none;">Hub sync stays manual-first and delta-based. Raw memories do not leave the device unless you explicitly export a signed receipt.</div>
    `);

    const hubToggle = document.getElementById('hubModeToggle');
    hubToggle.addEventListener('change', () => {
      const on = hubToggle.checked;
      document.getElementById('hubPublicKeyField').style.display = on ? '' : 'none';
      document.getElementById('hubPairingField').style.display = on ? '' : 'none';
      document.getElementById('hubAdvancedActions').style.display = on ? '' : 'none';
      document.getElementById('hubQueueStatus').style.display = on ? '' : 'none';
    });

    memoryUi = {
      panel: document.getElementById('memoryPalacePanel'),
      passphrase: document.getElementById('memoryPalacePassphrase'),
      backgroundUnlock: document.getElementById('memoryBackgroundUnlockToggle'),
      title: document.getElementById('memoryTitleInput'),
      summary: document.getElementById('memorySummaryInput'),
      detail: document.getElementById('memoryDetailInput'),
      tags: document.getElementById('memoryTagsInput'),
      environmentalContext: document.getElementById('memoryEnvironmentalContextInput'),
      add: document.getElementById('memoryAddBtn'),
      environmentalAdd: document.getElementById('memoryEnvironmentalNoteBtn'),
      refresh: document.getElementById('memoryRefreshBtn'),
      verify: document.getElementById('memoryVerifyBtn'),
      fullCheck: document.getElementById('memoryFullIntegrityBtn'),
      export: document.getElementById('memoryExportBtn'),
      search: document.getElementById('memorySearchInput'),
      timeline: document.getElementById('memoryTimelineList'),
      status: document.getElementById('memoryStatus'),
      hubPublicKey: document.getElementById('hubPublicKey'),
      hubPairingCode: document.getElementById('hubPairingCode'),
      hubApplyPairingBtn: document.getElementById('hubApplyPairingBtn'),
      hubPushBtn: document.getElementById('hubPushBtn'),
      hubPullBtn: document.getElementById('hubPullBtn'),
      hubFlushQueueBtn: document.getElementById('hubFlushQueueBtn'),
    };
  }

  async function hydratePhase3Ui() {
    const memoryProfile = await bridge.vaultStore.getSetting(MEMORY_CRYPTO_SETTING_KEY);
    if (memoryProfile && memoryProfile.background_unlock_enabled) {
      memoryUi.backgroundUnlock.checked = true;
      setMemoryStatus('Memory Palace background unlock is enabled. On supported browsers, roots can refresh without prompting for the passphrase again.', 'success');
    }
    const hubConfig = await loadHubConfig();
    if (hubConfig) {
      const hubUrl = document.getElementById('hubUrl');
      const hubPublicKey = document.getElementById('hubPublicKey');
      const hubConnectivityProfile = document.getElementById('hubConnectivityProfile');
      const hubLowWirelessToggle = document.getElementById('hubLowWirelessToggle');
      const hubQueuedSyncPreferenceToggle = document.getElementById('hubQueuedSyncPreferenceToggle');
      const hubConnectivityNote = document.getElementById('hubConnectivityNote');
      if (hubConfig.url) hubUrl.value = hubConfig.url;
      if (hubConfig.public_key_hex) hubPublicKey.value = hubConfig.public_key_hex;
      if (hubConfig.connectivity_profile) hubConnectivityProfile.value = hubConfig.connectivity_profile;
      hubLowWirelessToggle.checked = Boolean(hubConfig.low_wireless_mode);
      hubQueuedSyncPreferenceToggle.checked = Boolean(hubConfig.prefer_queued_syncs ?? true);
      if (hubConfig.connectivity_note) hubConnectivityNote.value = hubConfig.connectivity_note;
    }
    await renderMemoryTimeline();
  }

  function bindPhase3Events() {
    memoryUi.add.addEventListener('click', async () => {
      try {
        const passphrase = getMemoryPassphrase();
        if (!passphrase) throw new Error('Enter the Memory Palace passphrase first.');
        const created = await appendMemoryEntry({
          type: 'manual',
          source: 'manual',
          title: memoryUi.title.value.trim() || 'Manual memory',
          summary: memoryUi.summary.value.trim(),
          detail: memoryUi.detail.value.trim(),
          tags: tagsFromInput(memoryUi.tags.value),
          metadata: { created_from: 'memory-palace-panel' },
          passphrase,
        });
        memoryUi.title.value = '';
        memoryUi.summary.value = '';
        memoryUi.detail.value = '';
        memoryUi.tags.value = '';
        await renderMemoryTimeline(memoryUi.search.value || '');
        await bridge.showLocalNotification('Memory committed', 'A new Memory Palace block was sealed locally with a fresh commitment and signature.', 'memory-palace');
        setMemoryStatus(`Committed a new Memory Palace entry ${created.entry.commitment_hash.slice(0, 16)}…`, 'success');
      } catch (error) {
        setMemoryStatus(error.message, 'error');
      }
    });

    memoryUi.environmentalAdd.addEventListener('click', async () => {
      try {
        const passphrase = getMemoryPassphrase();
        if (!passphrase) throw new Error('Enter the Memory Palace passphrase first.');
        const environmentPreferences = getHubEnvironmentPreferences();
        const environmentalContext = memoryUi.environmentalContext.value.trim();
        const summary = memoryUi.summary.value.trim() || environmentalContext || hubEnvironmentSummary(environmentPreferences) || 'Connectivity and environmental review note.';
        const detailParts = [
          memoryUi.detail.value.trim(),
          environmentPreferences.connectivity_profile ? `Connectivity profile: ${environmentPreferences.connectivity_profile}` : '',
          environmentPreferences.low_wireless_mode ? 'Lower-local-wireless preference: enabled' : '',
          environmentPreferences.prefer_queued_syncs ? 'Queued/manual sync preference: enabled' : '',
          environmentalContext ? `User note: ${environmentalContext}` : '',
          MEMORY_ADVISORY_TEXT,
        ].filter(Boolean);
        const created = await appendMemoryEntry({
          type: 'environmental-note',
          source: 'environmental-review',
          title: memoryUi.title.value.trim() || 'Environmental note',
          summary,
          detail: detailParts.join(' '),
          tags: [...new Set(['environment', 'connectivity', ...tagsFromInput(memoryUi.tags.value)])],
          metadata: {
            ...environmentPreferences,
            environmental_note: environmentalContext,
          },
          passphrase,
        });
        memoryUi.title.value = '';
        memoryUi.summary.value = '';
        memoryUi.detail.value = '';
        memoryUi.tags.value = '';
        memoryUi.environmentalContext.value = '';
        await renderMemoryTimeline(memoryUi.search.value || '');
        setMemoryStatus(`Committed environmental note "${created.entry.signed_payload.id}" into the local Memory Palace.`, 'success');
      } catch (error) {
        setMemoryStatus(error.message, 'error');
      }
    });

    memoryUi.refresh.addEventListener('click', () => syncDerivedMemorySources().catch(error => setMemoryStatus(error.message, 'error')));
    memoryUi.verify.addEventListener('click', async () => {
      try {
        const result = await verifyMemoryIntegrity();
        setMemoryStatus(`Memory Palace verified. ${result.entries} entries and ${result.roots} Merkle roots checked from genesis.`, 'success');
      } catch (error) {
        setMemoryStatus(error.message, 'error');
      }
    });
    memoryUi.fullCheck.addEventListener('click', () => runFullSystemIntegrityCheck().catch(error => setMemoryStatus(error.message, 'error')));
    memoryUi.export.addEventListener('click', () => exportLatestMemoryReceipt().catch(error => setMemoryStatus(error.message, 'error')));
    memoryUi.search.addEventListener('input', () => renderMemoryTimeline(memoryUi.search.value || '').catch(error => setMemoryStatus(error.message, 'error')));
    memoryUi.backgroundUnlock.addEventListener('change', async () => {
      try {
        await ensureMemoryCryptoProfile(getMemoryPassphrase(), Boolean(memoryUi.backgroundUnlock.checked));
        setMemoryStatus(
          memoryUi.backgroundUnlock.checked
            ? 'Memory Palace background unlock enabled. Android/Chromium can refresh roots more reliably when connectivity returns.'
            : 'Memory Palace background unlock disabled. Full background refresh waits for the foreground app.',
          memoryUi.backgroundUnlock.checked ? 'success' : ''
        );
      } catch (error) {
        memoryUi.backgroundUnlock.checked = false;
        setMemoryStatus(error.message, 'error');
      }
    });

    memoryUi.hubApplyPairingBtn.addEventListener('click', () => {
      try {
        const pairing = JSON.parse(memoryUi.hubPairingCode.value || '{}');
        if (pairing.url) document.getElementById('hubUrl').value = pairing.url;
        if (pairing.public_key_hex) memoryUi.hubPublicKey.value = pairing.public_key_hex;
        setHubStatus('Applied the pairing code locally. Verify the public key before syncing.', 'success');
      } catch (error) {
        setHubStatus(`Could not parse the pairing code. ${error.message}`, 'error');
      }
    });
    memoryUi.hubPushBtn.addEventListener('click', () => performHubSync('push').catch(error => setHubStatus(error.message, 'error')));
    memoryUi.hubPullBtn.addEventListener('click', () => performHubSync('pull').catch(error => setHubStatus(error.message, 'error')));
    memoryUi.hubFlushQueueBtn.addEventListener('click', () => flushQueuedHubSyncs().catch(error => setHubStatus(error.message, 'error')));
    [
      document.getElementById('hubConnectivityProfile'),
      document.getElementById('hubLowWirelessToggle'),
      document.getElementById('hubQueuedSyncPreferenceToggle'),
      document.getElementById('hubConnectivityNote'),
    ].forEach(element => {
      if (!element) return;
      element.addEventListener('change', () => persistHubEnvironmentPreferences().catch(error => setHubStatus(error.message, 'error')));
    });

    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('message', event => {
        if (!event.data || typeof event.data.type !== 'string') return;
        if (event.data.type === 'HUB_SYNC_QUEUE_FLUSHED') {
          setHubStatus(`Service worker flushed ${event.data.flushed || 0} queued hub sync request(s).`, 'success');
          syncDerivedMemorySources().catch(() => undefined);
        }
      });
    }
  }

  injectMemoryPalaceUi();
  bindPhase3Events();
  hydratePhase3Ui().then(() => syncDerivedMemorySources().catch(() => undefined));
})();
