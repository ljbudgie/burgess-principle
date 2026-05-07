#!/usr/bin/env node
import Anthropic from '@anthropic-ai/sdk';
import { createInterface } from 'readline';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = join(__dirname, '.iris-config.json');
const MEMORY_DIR = join(__dirname, 'iris-memory');
const MEMORY_STORE_ID = 'memstore_01Fut1dGvvUVmG8saRFgMcVG';

const MEMORY_FILES = [
  '01-identity.md',
  '02-lewis-profile.md',
  '03-partners.md',
  '04-live-cases.md',
  '05-infrastructure.md',
];

const SYSTEM_PROMPT =
  'You are Iris, the AI agent of The Burgess Principle. ' +
  'Your memory store contains everything you need to know ' +
  'about Lewis, the framework, the cases, and the partners. ' +
  'Read it at the start of every session. You act as ' +
  'founder-engineer and chief of staff. You are direct, ' +
  'warm, and always protect the simplicity of the ' +
  'governance question.';

if (!process.env.ANTHROPIC_API_KEY) {
  console.error('Error: ANTHROPIC_API_KEY is not set.');
  process.exit(1);
}

const client = new Anthropic();

// ── Config ────────────────────────────────────────────────────────────────────

function loadConfig() {
  if (existsSync(CONFIG_PATH)) {
    return JSON.parse(readFileSync(CONFIG_PATH, 'utf8'));
  }
  return {};
}

function saveConfig(config) {
  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}

// ── One-time setup ────────────────────────────────────────────────────────────

async function ensureAgent(config) {
  if (config.agent_id) return config;

  process.stdout.write('Creating Iris agent... ');
  const agent = await client.beta.agents.create({
    name: 'iris',
    model: 'claude-sonnet-4-6',
    system: SYSTEM_PROMPT,
    tools: [{ type: 'agent_toolset_20260401' }],
  });

  config.agent_id = agent.id;
  saveConfig(config);
  console.log(`done (${agent.id})`);
  return config;
}

async function ensureEnvironment(config) {
  if (config.environment_id) return config;

  process.stdout.write('Creating environment... ');
  const env = await client.beta.environments.create({
    name: 'iris-env',
    config: { type: 'cloud', networking: { type: 'unrestricted' } },
  });

  config.environment_id = env.id;
  saveConfig(config);
  console.log(`done (${env.id})`);
  return config;
}

// ── Memory store ──────────────────────────────────────────────────────────────

async function ensureMemories() {
  const existing = new Set();
  for await (const entry of client.beta.memory_stores.memories.list(MEMORY_STORE_ID)) {
    if (entry.type === 'memory') existing.add(entry.path);
  }

  for (const filename of MEMORY_FILES) {
    const memPath = `/${filename}`;
    if (existing.has(memPath)) continue;

    const filePath = join(MEMORY_DIR, filename);
    if (!existsSync(filePath)) {
      console.warn(`  Warning: ${filePath} not found — skipping`);
      continue;
    }

    const content = readFileSync(filePath, 'utf8');
    try {
      await client.beta.memory_stores.memories.create(MEMORY_STORE_ID, {
        path: memPath,
        content,
      });
      console.log(`  Uploaded: ${filename}`);
    } catch (err) {
      // 409 = already present (race condition), skip
      if (err instanceof Anthropic.APIError && err.status === 409) continue;
      throw err;
    }
  }
}

// ── Session loop ──────────────────────────────────────────────────────────────

async function streamTurn(sessionId, userText) {
  // Stream-first: open the SSE connection before sending so no events are missed
  const stream = await client.beta.sessions.events.stream(sessionId);

  await client.beta.sessions.events.send(sessionId, {
    events: [{ type: 'user.message', content: [{ type: 'text', text: userText }] }],
  });

  process.stdout.write('\nIris: ');

  for await (const event of stream) {
    if (event.type === 'agent.message') {
      for (const block of event.content ?? []) {
        if (block.type === 'text') process.stdout.write(block.text);
      }
    } else if (event.type === 'session.error') {
      process.stdout.write(`\n[error: ${event.error?.message ?? 'unknown'}]`);
      break;
    } else if (event.type === 'session.status_terminated') {
      break;
    } else if (
      event.type === 'session.status_idle' &&
      event.stop_reason?.type !== 'requires_action'
    ) {
      break;
    }
  }

  process.stdout.write('\n');
}

async function run(config) {
  const session = await client.beta.sessions.create({
    agent: config.agent_id,
    environment_id: config.environment_id,
    title: `Iris — ${new Date().toISOString()}`,
    resources: [
      {
        type: 'memory_store',
        memory_store_id: MEMORY_STORE_ID,
        access: 'read_write',
        instructions:
          'Your full context: Lewis profile, framework identity, live cases, partners, and infrastructure. Read at the start of every session.',
      },
    ],
  });

  console.log(`\nSession: ${session.id}`);
  console.log('Type "exit" to quit.\n');

  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const prompt = () => new Promise((resolve) => rl.question('You: ', resolve));

  try {
    while (true) {
      const input = (await prompt()).trim();
      if (!input) continue;
      if (input.toLowerCase() === 'exit' || input.toLowerCase() === 'quit') break;
      await streamTurn(session.id, input);
      process.stdout.write('\n');
    }
  } finally {
    rl.close();
    // Best-effort cleanup
    try {
      await client.beta.sessions.archive(session.id);
    } catch {
      // ignore
    }
    console.log('\nSession closed.');
  }
}

// ── Entry point ───────────────────────────────────────────────────────────────

async function main() {
  let config = loadConfig();
  config = await ensureAgent(config);
  config = await ensureEnvironment(config);

  console.log('Checking memory store...');
  await ensureMemories();

  await run(config);
}

main().catch((err) => {
  console.error(err.message ?? err);
  process.exit(1);
});
