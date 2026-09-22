/**
 * MITRE ATT&CK T1078 (Valid Accounts) — the application's half of the job.
 *
 * Impossible travel, credential stuffing, password spray, device reputation and
 * MFA are solved by your identity provider (Entra ID Protection, Okta, Auth0,
 * Cognito). Do not reimplement them: the IdP sees sign-ins across every app and
 * every tenant, your application sees one. A homegrown copy is strictly worse
 * and usually locks out mobile users on cellular networks.
 *
 * What the application still owns, and what this sample shows:
 *   1. Read the risk and authentication-strength claims the IdP already sent.
 *   2. Decide which of YOUR operations demand a stronger credential.
 *   3. Emit an ATT&CK-tagged event so the SIEM can correlate with IdP sign-in logs.
 *
 * @reference https://attack.mitre.org/techniques/T1078/
 */

'use strict';

// Operations the application considers high impact. The IdP cannot know this list:
// it has no idea that "export-customers" is more dangerous than "list-avatars".
const SENSITIVE_OPERATIONS = new Map([
  ['export-customers', { requireAcr: 'mfa', maxCredentialAgeSeconds: 900 }],
  ['rotate-api-key', { requireAcr: 'mfa', maxCredentialAgeSeconds: 300 }],
  ['change-payout-account', { requireAcr: 'mfa', maxCredentialAgeSeconds: 300 }]
]);

/**
 * Decide whether a validated token is strong enough for a given operation.
 *
 * @param {object} claims - Validated token claims. Assume signature/issuer/audience
 *   were already checked by middleware; this function only reads claims.
 * @param {string} operation - Application operation being attempted.
 * @param {number} [nowSeconds] - Current time, for testability.
 * @returns {{decision: 'allow'|'step-up'|'deny', reason: string}}
 */
function authorizeSensitiveOperation(claims, operation, nowSeconds = Math.floor(Date.now() / 1000)) {
  const policy = SENSITIVE_OPERATIONS.get(operation);
  if (!policy) {
    return { decision: 'allow', reason: 'operation is not classified as sensitive' };
  }

  // Many IdPs can stamp a risk level onto the token or expose it via an API.
  // Honour it rather than recomputing it from an IP address.
  if (claims.risk_level === 'high') {
    return { decision: 'deny', reason: 'identity provider reported high sign-in risk' };
  }

  // acr/amr describe HOW the user proved themselves. A password-only session
  // should not be able to export the customer table.
  const acr = claims.acr ?? (Array.isArray(claims.amr) && claims.amr.includes('mfa') ? 'mfa' : 'pwd');
  if (policy.requireAcr === 'mfa' && acr !== 'mfa') {
    return { decision: 'step-up', reason: 'operation requires multi-factor authentication' };
  }

  // auth_time is when the credential was actually presented, which is not the
  // same as when the token was issued. A 10-hour-old session refreshed a minute
  // ago still has a 10-hour-old credential behind it.
  const authTime = Number(claims.auth_time);
  if (Number.isFinite(authTime) && nowSeconds - authTime > policy.maxCredentialAgeSeconds) {
    return { decision: 'step-up', reason: 'credential is older than this operation allows' };
  }

  return { decision: 'allow', reason: 'token satisfies the operation policy' };
}

/**
 * Emit a structured security event. Tagging with the ATT&CK id lets the security
 * team join these against IdP sign-in logs without parsing prose.
 *
 * Never log the token, the raw claims blob, or any credential material.
 */
function emitSecurityEvent(logger, { technique, operation, decision, reason, claims }) {
  logger.warn({
    event: 'authorization.decision',
    attack_technique: technique,
    operation,
    decision,
    reason,
    // Stable pseudonymous identifiers only.
    subject: claims.sub,
    tenant: claims.tid,
    session: claims.sid
  });
}

/**
 * Express middleware factory.
 *
 * Usage:
 *   app.post('/api/export/customers',
 *     requireAuth,                       // validates signature, issuer, audience, expiry
 *     requireOperation('export-customers'),
 *     exportHandler);
 */
function requireOperation(operation, logger = console) {
  return (req, res, next) => {
    const claims = req.auth?.claims;
    if (!claims) {
      return res.status(401).json({ error: 'authentication required' });
    }

    const { decision, reason } = authorizeSensitiveOperation(claims, operation);

    if (decision === 'allow') {
      return next();
    }

    emitSecurityEvent(logger, { technique: 'T1078', operation, decision, reason, claims });

    if (decision === 'step-up') {
      // Tell the client exactly what to obtain. RFC 9470 defines this challenge so
      // the SPA can silently re-authenticate instead of showing a dead end.
      res.set('WWW-Authenticate',
        'Bearer error="insufficient_user_authentication", acr_values="mfa"');
      return res.status(401).json({ error: 'step_up_required', acr_values: 'mfa' });
    }

    return res.status(403).json({ error: 'forbidden' });
  };
}

// =============================================================================
// EXAMPLE
// =============================================================================

if (require.main === module) {
  const now = 1_700_000_000;
  const cases = [
    ['password-only session exporting customers',
      { sub: 'u1', tid: 't1', sid: 's1', acr: 'pwd', auth_time: now - 60 }],
    ['MFA session, credential presented 2 minutes ago',
      { sub: 'u1', tid: 't1', sid: 's1', acr: 'mfa', auth_time: now - 120 }],
    ['MFA session, credential presented 4 hours ago',
      { sub: 'u1', tid: 't1', sid: 's1', acr: 'mfa', auth_time: now - 14_400 }],
    ['IdP flagged the sign-in as high risk',
      { sub: 'u1', tid: 't1', sid: 's1', acr: 'mfa', auth_time: now - 60, risk_level: 'high' }]
  ];

  console.log('Operation: export-customers\n');
  for (const [label, claims] of cases) {
    const { decision, reason } = authorizeSensitiveOperation(claims, 'export-customers', now);
    console.log(`  ${decision.toUpperCase().padEnd(8)} ${label}`);
    console.log(`  ${''.padEnd(8)} ${reason}\n`);
  }

  console.log('The identity provider detects the attack. The application decides');
  console.log('which of its own operations demand a stronger credential.');
}

module.exports = {
  SENSITIVE_OPERATIONS,
  authorizeSensitiveOperation,
  requireOperation
};
