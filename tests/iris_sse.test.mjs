// Unit test for the SSE parser embedded in iris.html.
// Mirrors the node:test pattern used by sovereign_core.test.mjs.
//
// We extract parseSSEEvent and readSSE from iris.html so that the test
// exercises the code that ships in the page, not a separate copy.

import assert from 'node:assert';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, '..');
const IRIS_HTML = readFileSync(resolve(REPO_ROOT, 'iris.html'), 'utf8');

function extractFunction(source, name) {
  // Match optional "async " prefix so that async functions evaluate correctly.
  const re = new RegExp(`(async\\s+)?function\\s+${name}\\s*\\(`);
  const match = re.exec(source);
  if (!match) throw new Error(`function ${name} not found in iris.html`);
  const idx = match.index;
  // Find the matching brace for the function body.
  const braceStart = source.indexOf('{', idx);
  let depth = 0;
  for (let i = braceStart; i < source.length; i += 1) {
    const ch = source[i];
    if (ch === '{') depth += 1;
    else if (ch === '}') {
      depth -= 1;
      if (depth === 0) {
        return source.slice(idx, i + 1);
      }
    }
  }
  throw new Error(`unterminated function ${name}`);
}

const parseSSEEventSource = extractFunction(IRIS_HTML, 'parseSSEEvent');
const readSSESource = extractFunction(IRIS_HTML, 'readSSE');

const context = vm.createContext({
  console,
  TextDecoder: globalThis.TextDecoder,
  setTimeout,
  clearTimeout,
});

vm.runInContext(parseSSEEventSource, context, { filename: 'iris-sse.parseSSEEvent.js' });
vm.runInContext(readSSESource, context, { filename: 'iris-sse.readSSE.js' });

const parseSSEEvent = context.parseSSEEvent;
const readSSE = context.readSSE;

test('parseSSEEvent: returns null for empty/comment-only frames', () => {
  assert.equal(parseSSEEvent(''), null);
  assert.equal(parseSSEEvent(': keepalive comment'), null);
  assert.equal(parseSSEEvent('event: ping'), null); // no data
});

test('parseSSEEvent: extracts data and defaults event to "message"', () => {
  const evt = parseSSEEvent('data: {"content":"Hello"}');
  assert.deepEqual(evt, { event: 'message', data: '{"content":"Hello"}' });
});

test('parseSSEEvent: respects custom event names', () => {
  const evt = parseSSEEvent('event: content_block_delta\ndata: {"delta":{"text":"hi"}}');
  assert.deepEqual(evt, {
    event: 'content_block_delta',
    data: '{"delta":{"text":"hi"}}',
  });
});

test('parseSSEEvent: joins multi-line data with \\n', () => {
  const evt = parseSSEEvent('data: line1\ndata: line2');
  assert.equal(evt.data, 'line1\nline2');
});

test('parseSSEEvent: handles \\r\\n line endings', () => {
  const evt = parseSSEEvent('event: foo\r\ndata: bar');
  assert.deepEqual(evt, { event: 'foo', data: 'bar' });
});

test('parseSSEEvent: strips a single leading space after the colon (per SSE spec)', () => {
  const evt = parseSSEEvent('data:  two-leading-spaces');
  // First space is the optional space; second is preserved.
  assert.equal(evt.data, ' two-leading-spaces');
});

// Build a minimal mock ReadableStream that yields fixed Uint8Array chunks.
function mockResponse(chunks) {
  const encoder = new TextEncoder();
  const queue = chunks.map((c) => encoder.encode(c));
  return {
    body: {
      getReader() {
        return {
          read() {
            if (queue.length === 0) return Promise.resolve({ done: true, value: undefined });
            return Promise.resolve({ done: false, value: queue.shift() });
          },
          releaseLock() {},
        };
      },
    },
  };
}

test('readSSE: dispatches each \\n\\n-separated event in order', async () => {
  const response = mockResponse([
    'data: {"content":"Hel"}\n\n',
    'data: {"content":"lo"}\n\n',
    'data: [DONE]\n\n',
  ]);
  const events = [];
  await readSSE(response, (e) => events.push(e));
  assert.deepEqual(events, [
    { event: 'message', data: '{"content":"Hel"}' },
    { event: 'message', data: '{"content":"lo"}' },
    { event: 'message', data: '[DONE]' },
  ]);
});

test('readSSE: handles events split across chunk boundaries', async () => {
  const response = mockResponse([
    'data: {"con',
    'tent":"split"}\n',
    '\ndata: [DONE]\n\n',
  ]);
  const events = [];
  await readSSE(response, (e) => events.push(e));
  assert.equal(events.length, 2);
  assert.equal(events[0].data, '{"content":"split"}');
  assert.equal(events[1].data, '[DONE]');
});

test('readSSE: flushes a trailing event without a terminator', async () => {
  const response = mockResponse(['data: tail-only']);
  const events = [];
  await readSSE(response, (e) => events.push(e));
  assert.deepEqual(events, [{ event: 'message', data: 'tail-only' }]);
});
