const PWA_CORE_VERSION = '1.1.1-phase1';
const STATIC_CACHE_NAME = `burgess-principle-static-${PWA_CORE_VERSION}`;
const RUNTIME_CACHE_NAME = `burgess-principle-runtime-${PWA_CORE_VERSION}`;
const API_CACHE_NAME = `burgess-principle-api-${PWA_CORE_VERSION}`;
const VAULT_DB_NAME = 'burgess-principle-vault';
const VAULT_DB_VERSION = 2;
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/service-worker.js',
  '/banner.png',
  '/signed-update-manifest.json'
];
const CRITICAL_PATHS = new Set(PRECACHE_URLS);
const TRIGGER_MIN_INTERVAL_MS = 60 * 60 * 1000; // 1 hour — minimum gap between trigger firings

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

// ------------------------------------------------------------------ //
// Install — precache app shell, but never force an update silently   //
// ------------------------------------------------------------------ //
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => warmCriticalAssets())
  );
});

// ------------------------------------------------------------------ //
// Activate — purge old caches, enable navigation preload, claim tabs //
// ------------------------------------------------------------------ //
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

// ------------------------------------------------------------------ //
// Fetch — navigation preload + stale-while-revalidate app shell      //
// ------------------------------------------------------------------ //
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

// ================================================================== //
// IndexedDB helpers                                                   //
// ================================================================== //
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

// ================================================================== //
// Background Sync — fingerprint queue                                 //
// ================================================================== //
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

// ================================================================== //
// Background Sync — reminder checks                                   //
// ================================================================== //
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

// ================================================================== //
// Sovereign Local Triggers — evaluate stored rules                    //
// ================================================================== //
async function evaluateTriggers() {
  let triggers = [];
  try {
    triggers = await readAll('triggers');
  } catch (_error) {
    return;
  }
  const now = Date.now();
  for (const trigger of triggers) {
    if (!trigger.enabled) continue;
    if (trigger.last_fired_at && now - Date.parse(trigger.last_fired_at) < TRIGGER_MIN_INTERVAL_MS) continue;

    let shouldFire = false;

    if (trigger.type === 'scheduled' && trigger.schedule_iso) {
      shouldFire = Date.parse(trigger.schedule_iso) <= now && !trigger.last_fired_at;
    }

    if (trigger.type === 'keyword' && trigger.keywords && trigger.keywords.length > 0) {
      // Keyword triggers are evaluated by the main app when content is available.
      // Periodic sync just checks if any were flagged but not yet notified.
      shouldFire = Boolean(trigger.flagged && !trigger.notified);
    }

    if (trigger.type === 'periodic' && trigger.interval_hours) {
      const interval = trigger.interval_hours * 60 * 60 * 1000;
      shouldFire = !trigger.last_fired_at || (now - Date.parse(trigger.last_fired_at) >= interval);
    }

    if (shouldFire) {
      const label = trigger.label || 'Burgess check ready';
      await self.registration.showNotification(label, {
        body: trigger.description || 'A sovereign local trigger has fired — open Iris to review.',
        icon: '/banner.png',
        badge: '/banner.png',
        tag: `trigger-${trigger.id}`,
        data: { url: '/?trigger=' + encodeURIComponent(trigger.id) }
      });
      trigger.last_fired_at = new Date().toISOString();
      trigger.notified = true;
      await putRecord('triggers', trigger);
    }
  }
}

// ================================================================== //
// Background Sync event                                               //
// ================================================================== //
self.addEventListener('sync', event => {
  if (event.tag === 'burgess-fingerprint-sync') {
    event.waitUntil(flushFingerprintQueue());
  }
  if (event.tag === 'burgess-reminder-sync') {
    event.waitUntil(notifyDueReminders());
  }
  if (event.tag === 'burgess-trigger-sync') {
    event.waitUntil(evaluateTriggers());
  }
  if (event.tag === 'burgess-critical-refresh') {
    event.waitUntil(warmCriticalAssets());
  }
});

// ================================================================== //
// Periodic Background Sync (gentle local refresh when supported)      //
// ================================================================== //
self.addEventListener('periodicsync', event => {
  if (event.tag === 'burgess-periodic-check') {
    event.waitUntil(
      Promise.all([
        notifyDueReminders(),
        evaluateTriggers(),
        flushFingerprintQueue(),
        warmCriticalAssets()
      ])
    );
  }
});

// ================================================================== //
// Push event — handle incoming web push notifications                 //
// ================================================================== //
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

// ================================================================== //
// Message handler — commands from the main app                        //
// ================================================================== //
self.addEventListener('message', event => {
  if (!event.data || typeof event.data.type !== 'string') return;
  if (event.data.type === 'SYNC_FINGERPRINTS') {
    event.waitUntil(flushFingerprintQueue());
  }
  if (event.data.type === 'CHECK_REMINDERS') {
    event.waitUntil(notifyDueReminders());
  }
  if (event.data.type === 'EVALUATE_TRIGGERS') {
    event.waitUntil(evaluateTriggers());
  }
  if (event.data.type === 'REFRESH_CRITICAL_PATHS') {
    event.waitUntil(warmCriticalAssets());
  }
  if (event.data.type === 'SKIP_WAITING') {
    event.waitUntil(self.skipWaiting());
  }
});

// ================================================================== //
// Notification click — open the relevant page                         //
// ================================================================== //
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
