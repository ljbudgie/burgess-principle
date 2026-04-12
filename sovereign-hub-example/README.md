# Sovereign Hub Example 2.0

A minimal self-hosted coordination layer for Iris Phase 3.

## What it does

- accepts delta sync envelopes from Iris over HTTPS / Tailscale / WireGuard
- stores only commitment digests by default (`memory_roots`, `claim_commitments`, `trigger_heads`)
- signs every response with an Ed25519 server key so Iris can pin and verify the hub identity
- keeps a local audit log of sync events in `/data/hub-state.json`

## Environment variables

- `HUB_SHARED_SECRET` — long random shared secret used for AES-256-GCM envelopes
- `HUB_SIGNING_SEED_HEX` — 32-byte Ed25519 private seed in hex
- `HUB_SERVER_ID` — optional human-readable server id

## Run with Docker

```bash
docker build -t iris-sovereign-hub ./sovereign-hub-example
docker run --rm -p 8080:8080 \
  -e HUB_SHARED_SECRET='replace-with-a-long-random-secret' \
  -e HUB_SIGNING_SEED_HEX='replace-with-64-hex-chars' \
  -e HUB_SERVER_ID='iris-hub-starlink' \
  -v $(pwd)/.hub-data:/data \
  iris-sovereign-hub
```

## Pairing flow

1. Put the hub behind Tailscale / WireGuard / another zero-trust tunnel.
2. Open `GET /api/hub/hello` and verify the returned `public_key_hex` over a trusted side channel.
3. Paste this JSON into Iris:

```json
{
  "url": "https://iris-hub.tailnet.ts.net",
  "public_key_hex": "<value from /api/hub/hello>"
}
```

4. Enter the same `HUB_SHARED_SECRET` in Iris.
5. Use **Push commitments** or **Pull commitments** from the Phase 3 hub controls.

## Notes

- This example is commitment-only by default. It does **not** store raw Memory Palace content unless the user explicitly exports a signed receipt from Iris and chooses to move it.
- For Starlink/intermittent links, Iris queues failed sync requests locally and retries later.
- Rotate `HUB_SIGNING_SEED_HEX` and `HUB_SHARED_SECRET` if the hub is ever compromised, then re-pair Iris with the new public key.
