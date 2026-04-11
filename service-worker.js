const CACHE_NAME = 'burgess-principle-pwa-v1-0-0';
const VAULT_DB_NAME = 'burgess-principle-vault';
const VAULT_DB_VERSION = 2;
const PRECACHE_URLS = ['/', '/index.html', '/manifest.json', '/service-worker.js', '/banner.png'];
const TRIGGER_MIN_INTERVAL_MS = 60 * 60 * 1000; // 1 hour — minimum gap between trigger firings

// ------------------------------------------------------------------ //
// Install — precache app shell, skip waiting for instant activation   //
// ------------------------------------------------------------------ //
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS)).then(() => self.skipWaiting()));
});

// ------------------------------------------------------------------ //
// Activate — purge old caches, claim all clients immediately          //
// ------------------------------------------------------------------ //
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))).then(() => self.clients.claim())
  );
});

// ------------------------------------------------------------------ //
// Fetch — cache-first for app shell, network-first for API            //
// ------------------------------------------------------------------ //
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (url.pathname.startsWith('/api/')) {
    return;
  }
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
      const copy = response.clone();
      caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
      return response;
    }).catch(() => caches.match('/index.html')))
  );
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
        flushFingerprintQueue()
      ])
    );
  }
});

// ================================================================== //
// Push event — handle incoming web push notifications                 //
// ================================================================== //
self.addEventListener('push', event => {
  let title = 'Iris — Sovereign Companion';
  let options = {
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
