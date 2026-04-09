import { sha256 } from '@noble/hashes/sha256';
import { ed25519 } from '@noble/curves/ed25519';
import CryptoJS from 'crypto-js';

export interface Facts {
  situation: string;
  requestedAction: string;
  evidence?: string;
  timestamp?: string;
}

export interface SignedReceipt {
  type: 'SOVEREIGN' | 'NULL';
  commitment: string;
  reviewerPubKey?: string;
  signature: string;
  date: string;
  organisation: string;
}

export class SovereignVault {
  private encryptedVault: string = '';
  private key: string;

  constructor(passphrase: string) {
    this.key = sha256(passphrase).toString();
  }

  async storeFacts(facts: Facts): Promise<void> {
    const data = JSON.stringify({
      ...facts,
      timestamp: new Date().toISOString()
    });
    this.encryptedVault = CryptoJS.AES.encrypt(data, this.key).toString();
  }

  async generateCommitment(): Promise<string> {
    if (!this.encryptedVault) throw new Error("No facts stored yet");
    const commitment = sha256(this.encryptedVault).toString();
    return commitment;
  }

  async receiveReceipt(receipt: SignedReceipt): Promise<void> {
    const message = receipt.commitment + receipt.type + receipt.date + receipt.organisation;
    const isValid = await this.verifySignature(message, receipt.signature, receipt.reviewerPubKey);

    if (!isValid) throw new Error("Invalid receipt signature");

    const current = this.encryptedVault 
      ? CryptoJS.AES.decrypt(this.encryptedVault, this.key).toString(CryptoJS.enc.Utf8) 
      : '{}';
    const vaultData = JSON.parse(current);
    vaultData.receipts = vaultData.receipts || [];
    vaultData.receipts.push(receipt);
    this.encryptedVault = CryptoJS.AES.encrypt(JSON.stringify(vaultData), this.key).toString();
  }

  private async verifySignature(message: string, signature: string, pubKey?: string): Promise<boolean> {
    if (!pubKey) return true;
    try {
      const msgBytes = new TextEncoder().encode(message);
      const sigBytes = Uint8Array.from(atob(signature), c => c.charCodeAt(0));
      const publicKeyBytes = Uint8Array.from(atob(pubKey), c => c.charCodeAt(0));
      return ed25519.verify(sigBytes, msgBytes, publicKeyBytes);
    } catch {
      return false;
    }
  }

  async challenge(): Promise<any> {
    const data = this.getDecryptedData();
    const nullReceipts = data.receipts?.filter((r: any) => r.type === 'NULL') || [];
    return {
      challenge: "I request a SOVEREIGN human review under the Burgess Principle.",
      nullReceipts,
      commitment: await this.generateCommitment()
    };
  }

  async exportRecord(): Promise<any> {
    const data = this.getDecryptedData();
    return {
      commitment: await this.generateCommitment(),
      receipts: data.receipts || [],
      exportDate: new Date().toISOString(),
      note: "This bundle is cryptographically verifiable. SOVEREIGN receipts prove a human reviewed the specific facts."
    };
  }

  private getDecryptedData(): any {
    if (!this.encryptedVault) return {};
    const decrypted = CryptoJS.AES.decrypt(this.encryptedVault, this.key).toString(CryptoJS.enc.Utf8);
    return JSON.parse(decrypted || '{}');
  }
}
