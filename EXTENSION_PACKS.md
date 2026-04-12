# Extension Packs

Iris keeps extensibility deliberately small.

Extension packs are local JSON manifests that can add:

- extra template shortcuts,
- extra trigger presets,
- extra export adapter buttons for local claim packages.

They do **not** load remote JavaScript, install binaries, or bypass the local-first boundary.

## What to include

- `id`, `name`, `version`
- `templates[]` with `id`, `label`, `prompt`
- `trigger_presets[]` with `id`, `label`, `natural_language`, and optional preset fields
- `export_adapters[]` with `id`, `label`, and `format` (`json`, `markdown`, or `email`)

## How to load one

1. Open the local Iris UI.
2. Go to **Claim profile & phone settings**.
3. Click **Load Extension Pack**.
4. Select a local JSON manifest.
5. Iris validates the manifest and keeps it on the device.

## Guardrails

- Extension packs remain advisory only.
- Export adapters package existing local claim output; they do not send data anywhere.
- Trigger presets must still be reviewed by the user before saving.
- Human review remains the final authority.
