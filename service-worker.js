const PWA_CORE_VERSION = '1.1.1-phase1';
const STATIC_CACHE_NAME = `burgess-principle-static-${PWA_CORE_VERSION}`;
const RUNTIME_CACHE_NAME = `burgess-principle-runtime-${PWA_CORE_VERSION}`;
const API_CACHE_NAME = `burgess-principle-api-${PWA_CORE_VERSION}`;
const VAULT_DB_NAME = 'burgess-principle-vault';
const VAULT_DB_VERSION = 3;
const TRIGGER_MIN_INTERVAL_MS = 60 * 60 * 1000;
const TRIGGER_CRYPTO_SETTING_KEY = 'living-trigger-crypto';
const TRIGGER_LAST_RECEIPT_SETTING_KEY = 'living-trigger-last-receipt';
const TRIGGER_LAST_RECEIPT_ID_SETTING_KEY = 'living-trigger-last-receipt-id';
const TRIGGER_ADVISORY_NOTE = 'Human review required — advisory only.';
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/service-worker.js',
  '/banner.png',
  '/signed-update-manifest.json'
];
const CRITICAL_PATHS = new Set(PRECACHE_URLS);

async function postClientMessage(message) {
  const allClients = await clients.matchAll({ type: 'window', includeUncontrolled: true });
  for (const client of allClients) {
    client.postMessage(message);
  }
}

async function putIfOk(cacheName, request, response) {
  if (!response || !response.ok || response.type === 'opaque') {
    return response;
  }
  const cache = await caches.open(cacheName);
  await cache.put(request, response.clone());
  return response;
}

async function warmCriticalAssets() {
  await Promise.all(
    PRECACHE_URLS.map(async path => {
      try {
        const request = new Request(path, { cache: 'reload' });
        const response = await fetch(request);
        await putIfOk(CRITICAL_PATHS.has(path) ? STATIC_CACHE_NAME : RUNTIME_CACHE_NAME, request, response);
      } catch (_error) {
        // Stay offline-first — the cached shell remains authoritative until connectivity returns.
      }
    })
  );
  await postClientMessage({ type: 'PWA_CRITICAL_PATHS_REFRESHED', version: PWA_CORE_VERSION });
}

async function staleWhileRevalidate(request, cacheName, fallbackUrl) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const networkFetch = fetch(request)
    .then(response => putIfOk(cacheName, request, response))
    .catch(() => null);

  if (cached) {
    return cached;
  }

  const networkResponse = await networkFetch;
  if (networkResponse) {
    return networkResponse;
  }

  if (fallbackUrl) {
    const fallback = await caches.match(fallbackUrl);
    if (fallback) {
      return fallback;
    }
  }

  return Response.error();
}

async function networkFirst(request, cacheName, fallbackUrl) {
  try {
    const response = await fetch(request);
    return await putIfOk(cacheName, request, response);
  } catch (_error) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    if (cached) {
      return cached;
    }
    if (fallbackUrl) {
      const fallback = await caches.match(fallbackUrl);
      if (fallback) {
        return fallback;
      }
    }
    return Response.error();
  }
}

async function handleNavigation(event) {
  try {
    const preload = await event.preloadResponse;
    if (preload) {
      return await putIfOk(STATIC_CACHE_NAME, event.request, preload);
    }
    const response = await fetch(event.request);
    return await putIfOk(STATIC_CACHE_NAME, event.request, response);
  } catch (_error) {
    const cached = await caches.match('/index.html');
    return cached || Response.error();
  }
}

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => warmCriticalAssets())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys
        .filter(key => ![STATIC_CACHE_NAME, RUNTIME_CACHE_NAME, API_CACHE_NAME].includes(key))
        .map(key => caches.delete(key))
    );
    if (self.registration.navigationPreload) {
      await self.registration.navigationPreload.enable().catch(() => undefined);
    }
    await self.clients.claim();
    await postClientMessage({ type: 'PWA_VERSION_READY', version: PWA_CORE_VERSION });
  })());
});

self.addEventListener('fetch', event => {
  const { request } = event;
  if (request.method !== 'GET') {
    return;
  }

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) {
    return;
  }

  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request, API_CACHE_NAME, null));
    return;
  }

  if (request.mode === 'navigate') {
    event.respondWith(handleNavigation(event));
    return;
  }

  if (url.pathname === '/signed-update-manifest.json') {
    const uncachedRequest = new Request(request.url, { cache: 'reload', credentials: 'same-origin' });
    event.respondWith(networkFirst(uncachedRequest, RUNTIME_CACHE_NAME, null));
    return;
  }

  if (CRITICAL_PATHS.has(url.pathname)) {
    event.respondWith(staleWhileRevalidate(request, STATIC_CACHE_NAME, '/index.html'));
    event.waitUntil(warmCriticalAssets());
    return;
  }

  event.respondWith(staleWhileRevalidate(request, RUNTIME_CACHE_NAME, '/index.html'));
});

function openDb() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(VAULT_DB_NAME, VAULT_DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains('fingerprintQueue')) db.createObjectStore('fingerprintQueue', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('reminders')) db.createObjectStore('reminders', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('claims')) db.createObjectStore('claims', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('settings')) db.createObjectStore('settings', { keyPath: 'key' });
      if (!db.objectStoreNames.contains('triggers')) db.createObjectStore('triggers', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('triggerQueue')) db.createObjectStore('triggerQueue', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('triggerLedger')) db.createObjectStore('triggerLedger', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('triggerReceipts')) db.createObjectStore('triggerReceipts', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('pushSubscription')) db.createObjectStore('pushSubscription', { keyPath: 'key' });
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error || new Error('IndexedDB open failed'));
  });
}

async function readAll(storeName) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readonly');
    const request = tx.objectStore(storeName).getAll();
    request.onsuccess = () => resolve(request.result || []);
    request.onerror = () => reject(request.error || new Error('IndexedDB read failed'));
    tx.oncomplete = () => db.close();
  });
}

async function getById(storeName, id) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readonly');
    const request = tx.objectStore(storeName).get(id);
    request.onsuccess = () => resolve(request.result || null);
    request.onerror = () => reject(request.error || new Error('IndexedDB get failed'));
    tx.oncomplete = () => db.close();
  });
}

async function getSetting(key) {
  const value = await getById('settings', key);
  return value ? value.value : null;
}

async function deleteById(storeName, id) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readwrite');
    const request = tx.objectStore(storeName).delete(id);
    request.onsuccess = () => resolve(true);
    request.onerror = () => reject(request.error || new Error('IndexedDB delete failed'));
    tx.oncomplete = () => db.close();
  });
}

async function putRecord(storeName, value) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readwrite');
    const request = tx.objectStore(storeName).put(value);
    request.onsuccess = () => resolve(value);
    request.onerror = () => reject(request.error || new Error('IndexedDB put failed'));
    tx.oncomplete = () => db.close();
  });
}

function toBase64(bytes) {
  let binary = '';
  bytes.forEach(byte => {
    binary += String.fromCharCode(byte);
  });
  return btoa(binary);
}

function fromBase64(value) {
  const binary = atob(value);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}

function bytesToHex(bytes) {
  return Array.from(bytes).map(byte => byte.toString(16).padStart(2, '0')).join('');
}

function canonicalizeForSignature(value) {
  if (Array.isArray(value)) {
    return `[${value.map(item => canonicalizeForSignature(item)).join(',')}]`;
  }
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalizeForSignature(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

async function sha256Hex(input) {
  const bytes = typeof input === 'string' ? new TextEncoder().encode(input) : input;
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return bytesToHex(new Uint8Array(digest));
}

async function decryptTriggerEnvelope(envelope, keyB64) {
  if (!envelope || !envelope.encrypted || !keyB64) return null;
  const key = await crypto.subtle.importKey('raw', fromBase64(keyB64), { name: 'AES-GCM' }, false, ['decrypt']);
  const plaintext = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: fromBase64(envelope.iv) },
    key,
    fromBase64(envelope.ciphertext)
  );
  return JSON.parse(new TextDecoder().decode(plaintext));
}

function sanitizeExcerpt(text, maxLength = 180) {
  return String(text || '').replace(/\s+/g, ' ').trim().slice(0, maxLength);
}

function runLocalPreBurgessInference({ text = '', matchedKeywords = [], source = 'conversation', trigger = {} }) {
  const lower = String(text || '').toLowerCase();
  let score = 0.18 + Math.min(0.32, matchedKeywords.length * 0.12);
  const weightMap = [
    { pattern: /(benefit|dwp|universal credit|sanction)/, add: 0.18, question: 'Was a named human able to review the benefits facts personally?' },
    { pattern: /(reasonable adjustment|disability|accessibility)/, add: 0.2, question: 'Who personally considered the requested adjustment and the specific barriers?' },
    { pattern: /(urgent|deadline|court|enforcement|bailiff|fraud)/, add: 0.16, question: 'Is there an urgent decision or enforcement step that needs a documented human review?' },
    { pattern: /(help me now|help me|panic)/, add: 0.2, question: 'Do you need an immediate human review flow to stabilise the situation?' },
  ];
  const suggested_questions = [];
  for (const item of weightMap) {
    if (item.pattern.test(lower)) {
      score += item.add;
      suggested_questions.push(item.question);
    }
  }
  if (source === 'voice') {
    score += 0.08;
  }
  const bounded = Math.max(0.05, Math.min(0.95, score));
  return {
    advisory_only: true,
    source,
    matched_keywords: matchedKeywords,
    risk_level: bounded >= 0.72 ? 'high' : bounded >= 0.45 ? 'medium' : 'low',
    confidence: Number(bounded.toFixed(2)),
    suggested_questions: suggested_questions.length > 0 ? suggested_questions : [
      'Was a human member of the team able to review the specific facts personally?',
      'What named person, team, or role can confirm the review?'
    ],
    rationale: `Local advisory score only for ${trigger.label || 'trigger'} — ${TRIGGER_ADVISORY_NOTE}`
  };
}

function buildTriggerNotification(trigger, queueItem) {
  const advisory = queueItem && queueItem.inference && queueItem.inference.risk_level
    ? `${queueItem.inference.risk_level} advisory risk`
    : 'advisory risk';
  return {
    title: trigger.label || 'Potential Burgess review needed',
    body: `${sanitizeExcerpt(trigger.description || queueItem.evidence && queueItem.evidence.reason || 'Potential Burgess review needed')} (${advisory}). Human review required.`,
  };
}

function buildTriggerUrl(triggerId, receiptId) {
  const params = new URLSearchParams();
  params.set('trigger', triggerId);
  if (receiptId) {
    params.set('triggerReceipt', receiptId);
  }
  return `/?${params.toString()}`;
}

async function importLedgerPrivateKey() {
  const profile = await getSetting(TRIGGER_CRYPTO_SETTING_KEY);
  if (!profile || !profile.ledger_private_key_jwk) {
    return { key: null, profile: null };
  }
  const key = await crypto.subtle.importKey('jwk', profile.ledger_private_key_jwk, { name: 'Ed25519' }, false, ['sign']);
  return { key, profile };
}

async function appendTriggerLedgerEvent({ trigger, event_type, source, evidence = {}, inference = {}, notification = {}, status = 'recorded' }) {
  const previous_commitment_hash = String((await getSetting(TRIGGER_LAST_RECEIPT_SETTING_KEY)) || '');
  const payload = {
    trigger_id: trigger.id,
    label: trigger.label,
    event_type,
    source,
    status,
    advisory_only: true,
    previous_commitment_hash,
    rule_hash: await sha256Hex(canonicalizeForSignature({
      id: trigger.id,
      label: trigger.label,
      type: trigger.type,
      detection_sources: trigger.detection_sources || [],
      encrypted_payload: trigger.encrypted_payload || {},
    })),
    evidence_hash: await sha256Hex(canonicalizeForSignature(evidence || {})),
    inference_hash: await sha256Hex(canonicalizeForSignature(inference || {})),
    notification,
    timestamp: new Date().toISOString(),
    nonce: `${event_type}-${Date.now()}`,
  };
  const commitment_hash = await sha256Hex(canonicalizeForSignature(payload));
  let signature = '';
  let public_key_hex = '';
  const signer = await importLedgerPrivateKey();
  if (signer.key && signer.profile && signer.profile.ledger_public_key_hex) {
    const signed = await crypto.subtle.sign('Ed25519', signer.key, new TextEncoder().encode(canonicalizeForSignature(payload)));
    signature = bytesToHex(new Uint8Array(signed));
    public_key_hex = signer.profile.ledger_public_key_hex;
  }
  const entry = {
    id: `trigger-ledger-${Date.now()}-${Math.random().toString(16).slice(2)}`,
    trigger_id: trigger.id,
    label: trigger.label,
    event_type,
    source,
    status,
    created_at: payload.timestamp,
    previous_commitment_hash,
    commitment_hash,
    signature,
    public_key_hex,
    evidence_excerpt: sanitizeExcerpt(evidence.text_excerpt || evidence.summary || ''),
    notification_title: notification.title || '',
    notification_body: notification.body || '',
    inference,
    advisory_only: true,
  };
  await putRecord('triggerLedger', entry);
  await putRecord('settings', { key: TRIGGER_LAST_RECEIPT_SETTING_KEY, value: commitment_hash });
  if (event_type === 'queued' || event_type === 'fired' || event_type === 'notified') {
    await putRecord('triggerReceipts', {
      ...entry,
      trigger_summary: {
        id: trigger.id,
        label: trigger.label,
        type: trigger.type,
        description: trigger.description || '',
      },
      receipt_export_version: 1,
    });
    await putRecord('settings', { key: TRIGGER_LAST_RECEIPT_ID_SETTING_KEY, value: entry.id });
  }
  return entry;
}

async function flushFingerprintQueue() {
  const queue = await readAll('fingerprintQueue');
  let flushed = 0;
  for (const fingerprint of queue) {
    try {
      const response = await fetch('/api/queue-onchain-fingerprint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fingerprint })
      });
      if (response.ok) {
        await deleteById('fingerprintQueue', fingerprint.id);
        flushed += 1;
      }
    } catch (_error) {
      // Keep queued until the next sync.
    }
  }
  if (flushed > 0) {
    await self.registration.showNotification('Fingerprint sync complete', {
      body: `${flushed} claim fingerprint${flushed === 1 ? '' : 's'} staged for privacy-first posting.`,
      icon: '/banner.png',
      badge: '/banner.png',
      tag: 'fingerprint-sync'
    });
  }
}

async function notifyDueReminders() {
  const reminders = await readAll('reminders');
  for (const reminder of reminders) {
    if (!reminder.due_at || reminder.notified_at || Date.parse(reminder.due_at) > Date.now()) continue;
    await self.registration.showNotification('14-day escalation reminder', {
      body: reminder.commitment_hash
        ? `Claim ${reminder.commitment_hash} reached the follow-up point.`
        : 'A saved Burgess Claim reached the follow-up point.',
      icon: '/banner.png',
      badge: '/banner.png',
      tag: reminder.id,
      data: { url: '/?shortcut=new-claim' }
    });
    reminder.notified_at = new Date().toISOString();
    await putRecord('reminders', reminder);
  }
}

async function processTriggerQueue() {
  const queued = (await readAll('triggerQueue')).filter(item => item.status === 'queued');
  let processed = 0;
  for (const item of queued) {
    const trigger = await getById('triggers', item.trigger_id);
    if (!trigger || !trigger.enabled) {
      await deleteById('triggerQueue', item.id);
      continue;
    }
    const inference = item.inference || runLocalPreBurgessInference({
      text: item.evidence && item.evidence.text_excerpt,
      matchedKeywords: item.evidence && item.evidence.matched_keywords || [],
      source: item.source,
      trigger,
    });
    const notification = buildTriggerNotification(trigger, { ...item, inference });
    const firedEntry = await appendTriggerLedgerEvent({
      trigger,
      event_type: 'fired',
      source: item.source || 'background',
      evidence: item.evidence || {},
      inference,
      notification,
      status: 'fired'
    });
    await self.registration.showNotification(notification.title, {
      body: notification.body,
      icon: '/banner.png',
      badge: '/banner.png',
      tag: `trigger-${trigger.id}`,
      data: {
        url: buildTriggerUrl(trigger.id, firedEntry.id),
        trigger_id: trigger.id,
        receipt_id: firedEntry.id,
        commitment_hash: firedEntry.commitment_hash,
      }
    });
    await appendTriggerLedgerEvent({
      trigger,
      event_type: 'notified',
      source: item.source || 'background',
      evidence: item.evidence || {},
      inference,
      notification,
      status: 'notified'
    });
    trigger.last_fired_at = new Date().toISOString();
    trigger.last_match_source = item.source || 'background';
    trigger.last_commitment_hash = firedEntry.commitment_hash;
    trigger.chain_head = firedEntry.commitment_hash;
    trigger.queue_depth = Math.max(0, Number(trigger.queue_depth || 1) - 1);
    trigger.notified = true;
    await putRecord('triggers', trigger);
    item.status = 'notified';
    item.processed_at = new Date().toISOString();
    item.receipt_id = firedEntry.id;
    item.commitment_hash = firedEntry.commitment_hash;
    await putRecord('triggerQueue', item);
    processed += 1;
  }
  if (processed > 0) {
    await postClientMessage({ type: 'TRIGGER_QUEUE_PROCESSED', processed });
  }
}

async function evaluateTriggers() {
  const profile = await getSetting(TRIGGER_CRYPTO_SETTING_KEY);
  if (!profile || !profile.background_key_b64) {
    return;
  }
  const triggers = await readAll('triggers');
  const now = Date.now();
  for (const trigger of triggers) {
    if (!trigger.enabled) continue;
    if (trigger.last_fired_at && now - Date.parse(trigger.last_fired_at) < TRIGGER_MIN_INTERVAL_MS) continue;
    if (!['periodic', 'scheduled'].includes(trigger.type)) continue;
    const rules = await decryptTriggerEnvelope(trigger.encrypted_payload, profile.background_key_b64).catch(() => null);
    if (!rules) continue;
    let shouldQueue = false;
    let reason = '';
    if (trigger.type === 'scheduled' && rules.schedule_iso) {
      shouldQueue = Date.parse(rules.schedule_iso) <= now && !trigger.last_fired_at;
      reason = 'Scheduled review window reached.';
    }
    if (trigger.type === 'periodic' && rules.interval_hours) {
      const interval = rules.interval_hours * 60 * 60 * 1000;
      shouldQueue = !trigger.last_fired_at || (now - Date.parse(trigger.last_fired_at) >= interval);
      reason = `Periodic ${rules.interval_hours}h trigger window reached.`;
    }
    if (!shouldQueue) continue;
    const text = `${trigger.label}. ${reason} ${trigger.description || ''}`.trim();
    const inference = runLocalPreBurgessInference({ text, matchedKeywords: rules.keywords || [], source: trigger.type, trigger });
    const queueItem = {
      id: `trigger-queue-${Date.now()}-${Math.random().toString(16).slice(2)}`,
      trigger_id: trigger.id,
      label: trigger.label,
      type: trigger.type,
      source: trigger.type,
      status: 'queued',
      created_at: new Date().toISOString(),
      evidence: {
        source: trigger.type,
        reason,
        text_excerpt: sanitizeExcerpt(text),
        matched_keywords: rules.keywords || [],
      },
      inference,
      notification: buildTriggerNotification(trigger, { evidence: { reason }, inference }),
      prefill_prompt: `A Living Trigger fired on this device for "${trigger.label}". ${reason} ${TRIGGER_ADVISORY_NOTE}`,
    };
    const queuedEntry = await appendTriggerLedgerEvent({
      trigger,
      event_type: 'queued',
      source: trigger.type,
      evidence: queueItem.evidence,
      inference,
      notification: queueItem.notification,
      status: 'queued'
    });
    queueItem.commitment_hash = queuedEntry.commitment_hash;
    queueItem.receipt_id = queuedEntry.id;
    await putRecord('triggerQueue', queueItem);
    trigger.last_evaluated_at = new Date().toISOString();
    trigger.last_commitment_hash = queuedEntry.commitment_hash;
    trigger.chain_head = queuedEntry.commitment_hash;
    trigger.queue_depth = Number(trigger.queue_depth || 0) + 1;
    trigger.notified = false;
    await putRecord('triggers', trigger);
  }
}

self.addEventListener('sync', event => {
  if (event.tag === 'burgess-fingerprint-sync') {
    event.waitUntil(flushFingerprintQueue());
  }
  if (event.tag === 'burgess-reminder-sync') {
    event.waitUntil(notifyDueReminders());
  }
  if (event.tag === 'burgess-trigger-sync') {
    event.waitUntil(Promise.all([evaluateTriggers(), processTriggerQueue()]));
  }
  if (event.tag === 'burgess-trigger-queue-sync') {
    event.waitUntil(processTriggerQueue());
  }
  if (event.tag === 'burgess-critical-refresh') {
    event.waitUntil(warmCriticalAssets());
  }
});

self.addEventListener('periodicsync', event => {
  if (event.tag === 'burgess-periodic-check') {
    event.waitUntil(
      Promise.all([
        notifyDueReminders(),
        evaluateTriggers(),
        processTriggerQueue(),
        flushFingerprintQueue(),
        warmCriticalAssets()
      ])
    );
  }
});

self.addEventListener('push', event => {
  let title = 'Iris — Sovereign Companion';
  const options = {
    body: 'Burgess check ready — open Iris?',
    icon: '/banner.png',
    badge: '/banner.png',
    tag: 'push-notification',
    data: { url: '/' }
  };

  if (event.data) {
    try {
      const payload = event.data.json();
      title = payload.title || title;
      options.body = payload.body || options.body;
      options.tag = payload.tag || options.tag;
      if (payload.url) options.data = { url: payload.url };
    } catch (_error) {
      options.body = event.data.text() || options.body;
    }
  }

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('message', event => {
  if (!event.data || typeof event.data.type !== 'string') return;
  if (event.data.type === 'SYNC_FINGERPRINTS') {
    event.waitUntil(flushFingerprintQueue());
  }
  if (event.data.type === 'CHECK_REMINDERS') {
    event.waitUntil(notifyDueReminders());
  }
  if (event.data.type === 'EVALUATE_TRIGGERS') {
    event.waitUntil(Promise.all([evaluateTriggers(), processTriggerQueue()]));
  }
  if (event.data.type === 'PROCESS_TRIGGER_QUEUE') {
    event.waitUntil(processTriggerQueue());
  }
  if (event.data.type === 'REFRESH_CRITICAL_PATHS') {
    event.waitUntil(warmCriticalAssets());
  }
  if (event.data.type === 'SKIP_WAITING') {
    event.waitUntil(self.skipWaiting());
  }
});

self.addEventListener('notificationclick', event => {
  const targetUrl = (event.notification.data && event.notification.data.url) || '/';
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
      for (const client of clientList) {
        if ('focus' in client) {
          return client.focus().then(() => {
            if ('navigate' in client) {
              return client.navigate(targetUrl).catch(() => client);
            }
            return client;
          });
        }
      }
      return clients.openWindow(targetUrl);
    })
  );
});
