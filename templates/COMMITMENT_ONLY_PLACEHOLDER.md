# Request for Confirmation of Human Review  
**— The Burgess Principle (Commitment-Only Version)**

**Date:** [DATE]  
**Reference:** [Your Case / Account / Decision Reference]  
**To:** [Institution Name & Full Address]

Dear [Institution / Team],

I hope this finds you well.

I am writing about [briefly describe the decision or action in one sentence].

Following the guidance in the Burgess Principle, I'd like to kindly ask:

**Was a human member of your team able to personally review the specific facts of *my* situation before this decision was made?**

For verification purposes, I have generated a cryptographic commitment that covers the full facts of my case:

> **Commitment:** `[COMMITMENT_HASH]`

This hash proves that my account of events existed before your response, without revealing any personal details in this message. I hold the opening values privately and can present them later if needed.

If someone did review my individual circumstances and took responsibility for the outcome, I would appreciate a short written confirmation with their name or reference.

If that did not happen, I would be grateful if you could now give my case that personal attention and let me know the result.

I'm happy to provide any further details that would help.

Thank you for your time and for treating this as the individual matter it is.

Yours sincerely,  
[Your Full Name]  
[Your Contact Details]

---

**How to fill in `[COMMITMENT_HASH]`:**

1. Write down the facts of your case in a plain text note on your phone.
2. Use the sovereign-vault tool or any SHA-256 generator to create a fresh hash:
   - On a computer: `echo -n "$(openssl rand -hex 32)YOUR FACTS" | shasum -a 256`
   - Using the sovereign-vault: `npx ts-node src/generate-commitment.ts "your facts"`
3. Paste the resulting hash into the `[COMMITMENT_HASH]` field above.
4. Keep your facts and salt private — only share the hash.
5. Generate a **new** commitment for every separate request. Never reuse a hash.

---

*Created as part of the original Burgess Principle (UK00004343685).*
