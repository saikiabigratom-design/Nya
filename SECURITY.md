# Security & Privacy Policy for ঞ (Nya)

## Reporting a Vulnerability

Security and user privacy are foundational pillars of **ঞ (Nya) — Vocal for Local**. If you discover a security vulnerability or privacy leak, please disclose it responsibly.

Please email security reports to `security@nya-search.org` or open a confidential security advisory. We acknowledge receipt within 48 hours and provide a remediation timeline.

---

## Security Practices

1. **Strict Privacy by Default:**
   - Raw search queries are scrubbed from server request logs.
   - User feedback records store SHA-256 hashes of queries rather than plaintext.
   - No behavioral advertising profiles are built from user queries.

2. **Server-Side Request Forgery (SSRF) Defense:**
   - The crawler enforces strict URL validation (`is_safe_external_url`).
   - Hostnames resolving to RFC 1918 private ranges, localhost, link-local, loopback, or cloud metadata IP (`169.254.169.254`) are immediately rejected.

3. **Prompt Injection Protections:**
   - Untrusted web content is sanitized, wrapped in explicit `<evidence>` delimiters, and defanged of system prompt overrides before being supplied to AI models.
   - AI generation is bounded by hard monthly spending limits to prevent resource exhaustion attacks.

4. **Input Validation:**
   - All API endpoints validate request lengths, character sets, and parameters using strict Pydantic schemas.
