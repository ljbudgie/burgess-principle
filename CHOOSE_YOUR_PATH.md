# Choose Your Path

This is the fastest way into Iris.

Choose **one** path and ignore the rest until you need it.

---

## 1. Send a letter now

Use this path when you need a result today.

1. Open the primary template index at [`/templates`](./templates/README.md).
2. Start with [`REQUEST_FOR_HUMAN_REVIEW.md`](./templates/REQUEST_FOR_HUMAN_REVIEW.md) if you are unsure.
3. If the institution already gave a vague answer, use [`FOLLOW_UP_WEASEL_RESPONSE.md`](./templates/FOLLOW_UP_WEASEL_RESPONSE.md).
4. If you want conversational help first, open the hosted Iris PWA at [burgess-principle.vercel.app](https://burgess-principle.vercel.app).
5. Send the letter and keep a copy.

**What to read next only if needed:** [`tutorials/README.md`](./tutorials/README.md)

---

## 2. Set up Sovereign Local Mode

Use this path when you want maximum privacy, offline use, and local audit trails.

1. Open [`SOVEREIGN_MODE.md`](./SOVEREIGN_MODE.md).
2. Run one install script from [`scripts/`](./scripts/).
3. Optionally run `python3 setup-wizard.py`.
4. Start Iris with `python3 iris-local.py`.
5. In the local UI, open **Claim profile & phone settings** and save your local profile.
6. Use **Export Backup Bundle** after first setup so you have a full local recovery file.

**What to read next only if needed:** [`ARCHITECTURE.md`](./ARCHITECTURE.md)

---

## 3. Verify or export evidence

Use this path when you already have local records and need to prove integrity without over-sharing.

1. Open the local Iris UI.
2. In **Memory Palace**, use **Export latest memory receipt** to create a selective-disclosure JSON receipt.
3. Use **Verify receipt file** to check a receipt locally in plain language.
4. Use **Export Backup Bundle** if you need a full-device migration or recovery file.
5. If you need external tooling, use the schemas in [`/schemas`](./schemas) and the contract in [`INTEGRATION_CONTRACT.md`](./INTEGRATION_CONTRACT.md).

**What to read next only if needed:** [`iris/README.md`](./iris/README.md), [`ARCHITECTURE.md`](./ARCHITECTURE.md)

---

## What each path preserves

- **Local-first:** raw facts stay on your device unless you choose to export.
- **Verifiable:** receipts and backup bundles can be checked for integrity.
- **Human-first:** AI helps prepare and organise; it does not decide the Burgess outcome.
