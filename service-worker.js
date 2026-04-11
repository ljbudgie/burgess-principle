const CACHE_NAME = 'burgess-principle-pwa-v0-9-0';
const VAULT_DB_NAME = 'burgess-principle-vault';
const VAULT_DB_VERSION = 1;
const PRECACHE_URLS = ['/', '/index.html', '/manifest.json', '/service-worker.js', '/banner.png', '/START_HERE.md', '/SOVEREIGN_MODE.md'];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))).then(() => self.clients.claim())
  );
});

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

function openDb() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(VAULT_DB_NAME, VAULT_DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains('fingerprintQueue')) db.createObjectStore('fingerprintQueue', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('reminders')) db.createObjectStore('reminders', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('claims')) db.createObjectStore('claims', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('settings')) db.createObjectStore('settings', { keyPath: 'key' });
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

self.addEventListener('sync', event => {
  if (event.tag === 'burgess-fingerprint-sync') {
    event.waitUntil(flushFingerprintQueue());
  }
  if (event.tag === 'burgess-reminder-sync') {
    event.waitUntil(notifyDueReminders());
  }
});

self.addEventListener('message', event => {
  if (!event.data || typeof event.data.type !== 'string') return;
  if (event.data.type === 'SYNC_FINGERPRINTS') {
    event.waitUntil(flushFingerprintQueue());
  }
  if (event.data.type === 'CHECK_REMINDERS') {
    event.waitUntil(notifyDueReminders());
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
