function canonicalize(value) {
  if (Array.isArray(value)) {
    return `[${value.map(item => canonicalize(item)).join(',')}]`;
  }
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

async function sha256Hex(value) {
  const bytes = typeof value === 'string' ? new TextEncoder().encode(value) : value;
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest)).map(byte => byte.toString(16).padStart(2, '0')).join('');
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
      next.push(await sha256Hex(canonicalize({ left, right })));
      if (i === cursor || i + 1 === cursor) {
        proof.push(i === cursor ? right : left);
        cursor = next.length - 1;
      }
    }
    level = next;
  }
  return { root: level[0], proof };
}

function scoreText(query, text) {
  const q = String(query || '').trim().toLowerCase();
  const haystack = String(text || '').toLowerCase();
  if (!q || !haystack) return 0;
  if (haystack.includes(q)) return 100 - haystack.indexOf(q);
  const queryTokens = q.split(/\s+/).filter(Boolean);
  const haystackTokens = haystack.split(/[^a-z0-9]+/i).filter(Boolean);
  let score = 0;
  for (const token of queryTokens) {
    if (haystackTokens.some(candidate => candidate.startsWith(token))) score += 18;
    else if (haystackTokens.some(candidate => candidate.includes(token))) score += 10;
  }
  return score;
}

function searchEntries(query, entries) {
  return (entries || [])
    .map(entry => {
      const corpus = [entry.title, entry.summary, entry.detail, ...(entry.tags || [])].join(' ');
      return { ...entry, score: scoreText(query, corpus) };
    })
    .filter(entry => entry.score > 0)
    .sort((left, right) => right.score - left.score || Date.parse(right.created_at || 0) - Date.parse(left.created_at || 0));
}

self.addEventListener('message', async event => {
  const { id, type, payload } = event.data || {};
  try {
    let result = null;
    if (type === 'merkle-state') {
      result = await buildMerkleState(payload.leaves || [], payload.index || 0);
    }
    if (type === 'search') {
      result = searchEntries(payload.query || '', payload.entries || []);
    }
    self.postMessage({ id, result });
  } catch (error) {
    self.postMessage({ id, error: error.message || String(error) });
  }
});
