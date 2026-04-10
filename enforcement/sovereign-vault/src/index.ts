import { sha256 } from '@noble/hashes/sha256';
import { ed25519 } from '@noble/curves/ed25519';
import { randomBytes as nobleRandomBytes } from '@noble/hashes/utils';
import { pbkdf2 } from '@noble/hashes/pbkdf2';
import { bytesToHex, hexToBytes } from '@noble/hashes/utils';

// ---------- AES-256-GCM helpers (Node.js built-in crypto) ----------
import { createCipheriv, createDecipheriv } from 'crypto';

const AES_KEY_BYTES = 32;   // 256 bits
const IV_BYTES = 12;        // 96-bit IV recommended for GCM
const AUTH_TAG_BYTES = 16;  // 128-bit authentication tag
const PBKDF2_ITERATIONS = 210_000; // OWASP 2023 recommendation for SHA-256
const PBKDF2_SALT_BYTES = 16;

/**
 * Encrypt plaintext with AES-256-GCM.
 * Returns a hex string: salt || iv || authTag || ciphertext.
 */
function aes256GcmEncrypt(plaintext: string, passphrase: string): string {
  const salt = nobleRandomBytes(PBKDF2_SALT_BYTES);
  const key = pbkdf2(sha256, new TextEncoder().encode(passphrase), salt, {
    c: PBKDF2_ITERATIONS,
    dkLen: AES_KEY_BYTES,
  });
  const iv = nobleRandomBytes(IV_BYTES);
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
  const authTag = cipher.getAuthTag();

  // Pack: salt (16) + iv (12) + authTag (16) + ciphertext
  const packed = new Uint8Array(salt.length + iv.length + authTag.length + encrypted.length);
  packed.set(salt, 0);
  packed.set(iv, salt.length);
  packed.set(authTag, salt.length + iv.length);
  packed.set(encrypted, salt.length + iv.length + authTag.length);
  return bytesToHex(packed);
}

/**
 * Decrypt a hex blob produced by aes256GcmEncrypt.
 */
function aes256GcmDecrypt(packed: string, passphrase: string): string {
  const data = hexToBytes(packed);
  const salt = data.slice(0, PBKDF2_SALT_BYTES);
  const iv = data.slice(PBKDF2_SALT_BYTES, PBKDF2_SALT_BYTES + IV_BYTES);
  const authTag = data.slice(PBKDF2_SALT_BYTES + IV_BYTES, PBKDF2_SALT_BYTES + IV_BYTES + AUTH_TAG_BYTES);
  const ciphertext = data.slice(PBKDF2_SALT_BYTES + IV_BYTES + AUTH_TAG_BYTES);

  const key = pbkdf2(sha256, new TextEncoder().encode(passphrase), salt, {
    c: PBKDF2_ITERATIONS,
    dkLen: AES_KEY_BYTES,
  });
  const decipher = createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);
  const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  return decrypted.toString('utf8');
}

// ---------- Canonical message serialisation ----------

/**
 * Build a canonical message string for signing / verification.
 * Uses JSON with sorted keys and no whitespace — deterministic
 * and immune to concatenation-ambiguity attacks.
 */
function canonicalReceiptMessage(receipt: { commitment: string; type: string; date: string; organisation: string }): string {
  return JSON.stringify({
    commitment: receipt.commitment,
    date: receipt.date,
    organisation: receipt.organisation,
    type: receipt.type,
  }, Object.keys({
    commitment: '',
    date: '',
    organisation: '',
    type: '',
  }).sort());
}

// ---------- Public types ----------

export interface Facts {
  situation: string;
  requestedAction: string;
  evidence?: string;
  timestamp?: string;
}

export interface SignedReceipt {
  type: 'SOVEREIGN' | 'NULL';
  commitment: string;
  reviewerPubKey: string;
  signature: string;
  date: string;
  organisation: string;
}

// ---------- Vault ----------

export class SovereignVault {
  private encryptedVault: string = '';
  private passphrase: string;

  /** Salt used for the latest commitment (generated fresh each time). */
  private commitmentSalt: string = '';

  /** Plaintext facts JSON (kept in memory while the vault is open). */
  private factsJson: string = '';

  constructor(passphrase: string) {
    if (!passphrase || passphrase.length < 8) {
      throw new Error('Passphrase must be at least 8 characters');
    }
    this.passphrase = passphrase;
  }

  async storeFacts(facts: Facts): Promise<void> {
    const data = JSON.stringify({ ...facts, timestamp: new Date().toISOString() });
    this.factsJson = data;
    this.encryptedVault = aes256GcmEncrypt(data, this.passphrase);
  }

  /**
   * Generate a fresh commitment: SHA-256( random-salt || facts-json ).
   * A new 32-byte salt is drawn every call so that repeated
   * commitments over the same facts are unlinkable.
   */
  async generateCommitment(): Promise<string> {
    if (!this.factsJson) throw new Error('No facts stored yet');
    const salt = nobleRandomBytes(32);
    this.commitmentSalt = bytesToHex(salt);
    const preimage = this.commitmentSalt + this.factsJson;
    return bytesToHex(sha256(new TextEncoder().encode(preimage)));
  }

  /** Return the salt used for the most recent commitment (for later opening / verification). */
  getCommitmentSalt(): string {
    if (!this.commitmentSalt) throw new Error('No commitment generated yet');
    return this.commitmentSalt;
  }

  async receiveReceipt(receipt: SignedReceipt): Promise<void> {
    const message = canonicalReceiptMessage(receipt);
    const isValid = await this.verifySignature(message, receipt.signature, receipt.reviewerPubKey);
    if (!isValid) throw new Error('Invalid receipt signature');

    const vaultData = this.getDecryptedData();
    vaultData.receipts = vaultData.receipts || [];
    vaultData.receipts.push(receipt);
    const json = JSON.stringify(vaultData);
    this.factsJson = json;
    this.encryptedVault = aes256GcmEncrypt(json, this.passphrase);
  }

  private async verifySignature(message: string, signature: string, pubKey: string): Promise<boolean> {
    if (!pubKey) {
      throw new Error('Receipt must include a reviewerPubKey for signature verification');
    }
    try {
      const msgBytes = new TextEncoder().encode(message);
      const sigBytes = hexToBytes(signature);
      const publicKeyBytes = hexToBytes(pubKey);
      return ed25519.verify(sigBytes, msgBytes, publicKeyBytes);
    } catch {
      return false;
    }
  }

  async challenge(): Promise<{ challenge: string; nullReceipts: SignedReceipt[]; commitment: string }> {
    const data = this.getDecryptedData();
    const nullReceipts = (data.receipts ?? []).filter((r: SignedReceipt) => r.type === 'NULL');
    return {
      challenge: 'I request a SOVEREIGN human review under the Burgess Principle.',
      nullReceipts,
      commitment: await this.generateCommitment(),
    };
  }

  async exportRecord(): Promise<{ commitment: string; receipts: SignedReceipt[]; exportDate: string; note: string }> {
    const data = this.getDecryptedData();
    return {
      commitment: await this.generateCommitment(),
      receipts: data.receipts ?? [],
      exportDate: new Date().toISOString(),
      note: 'This bundle is cryptographically verifiable. SOVEREIGN receipts prove a human reviewed the specific facts.',
    };
  }

  private getDecryptedData(): { receipts?: SignedReceipt[]; [key: string]: unknown } {
    if (!this.encryptedVault) return {};
    const decrypted = aes256GcmDecrypt(this.encryptedVault, this.passphrase);
    return JSON.parse(decrypted || '{}') as { receipts?: SignedReceipt[]; [key: string]: unknown };
  }
}
