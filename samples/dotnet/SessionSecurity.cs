using Microsoft.AspNetCore.Http;
using System.Security.Cryptography;
using System.Text;
using System.Collections.Concurrent;

namespace MitreAttackForDevs.Samples;

/// <summary>
/// Demonstrates defense against:
/// - T1185: Browser Session Hijacking
/// - T1098: Account Manipulation
/// - T1550.004: Web Session Cookie
/// 
/// Implements secure session management with fingerprinting, rotation, and anomaly detection
/// </summary>
public class SecureSessionManager
{
    private readonly ILogger<SecureSessionManager> _logger;
    
    // Track active sessions with metadata
    private readonly ConcurrentDictionary<string, SessionMetadata> _activeSessions = new();
    
    // Track concurrent sessions per user
    private readonly ConcurrentDictionary<string, HashSet<string>> _userSessions = new();

    // Configuration
    private readonly SessionSecurityOptions _options;

    public SecureSessionManager(ILogger<SecureSessionManager> logger, SessionSecurityOptions? options = null)
    {
        _logger = logger;
        _options = options ?? new SessionSecurityOptions();
    }

    /// <summary>
    /// T1185 Defense: Create session with fingerprinting
    /// Binds session to client characteristics to prevent hijacking
    /// </summary>
    public async Task<SecureSession> CreateSessionAsync(
        string userId, 
        HttpContext httpContext,
        string? privilegeLevel = "standard")
    {
        var sessionId = GenerateSecureSessionId();
        var fingerprint = GenerateClientFingerprint(httpContext);
        
        var session = new SecureSession
        {
            SessionId = sessionId,
            UserId = userId,
            Fingerprint = fingerprint,
            CreatedAt = DateTimeOffset.UtcNow,
            LastAccessedAt = DateTimeOffset.UtcNow,
            ExpiresAt = DateTimeOffset.UtcNow.Add(_options.SessionTimeout),
            PrivilegeLevel = privilegeLevel ?? "standard",
            IpAddress = GetClientIpAddress(httpContext),
            UserAgent = httpContext.Request.Headers["User-Agent"].ToString()
        };

        var metadata = new SessionMetadata
        {
            Session = session,
            AccessCount = 1,
            LastRotationAt = DateTimeOffset.UtcNow
        };

        _activeSessions[sessionId] = metadata;
        
        // Track user sessions for concurrent session detection
        _userSessions.AddOrUpdate(
            userId,
            _ => new HashSet<string> { sessionId },
            (_, sessions) =>
            {
                lock (sessions)
                {
                    sessions.Add(sessionId);
                    return sessions;
                }
            });

        // T1185: Check for suspicious concurrent sessions
        await DetectConcurrentSessionAnomaliesAsync(userId, session);

        _logger.LogInformation(
            "[T1185] Session created for user {UserId}, SessionId: {SessionId}, IP: {IpAddress}",
            userId, sessionId, session.IpAddress);

        return session;
    }

    /// <summary>
    /// T1185 Defense: Validate session with fingerprint verification
    /// Detects session hijacking attempts by comparing fingerprints
    /// </summary>
    public async Task<SessionValidationResult> ValidateSessionAsync(
        string sessionId, 
        HttpContext httpContext)
    {
        if (!_activeSessions.TryGetValue(sessionId, out var metadata))
        {
            _logger.LogWarning("[T1185] Invalid session attempted: {SessionId}", sessionId);
            return SessionValidationResult.Invalid("Session not found");
        }

        var session = metadata.Session;
        
        // Check expiration
        if (DateTimeOffset.UtcNow > session.ExpiresAt)
        {
            await InvalidateSessionAsync(sessionId, "Session expired");
            return SessionValidationResult.Invalid("Session expired");
        }

        // T1185: Verify session fingerprint
        var currentFingerprint = GenerateClientFingerprint(httpContext);
        if (currentFingerprint != session.Fingerprint)
        {
            _logger.LogWarning(
                "[T1185] SECURITY ALERT: Session hijacking attempt detected! " +
                "SessionId: {SessionId}, UserId: {UserId}, " +
                "Original IP: {OriginalIp}, Current IP: {CurrentIp}",
                sessionId, session.UserId, session.IpAddress, GetClientIpAddress(httpContext));

            // Invalidate potentially compromised session
            await InvalidateSessionAsync(sessionId, "Fingerprint mismatch - potential hijacking");
            
            return SessionValidationResult.Invalid("Session validation failed");
        }

        // T1185: Detect IP address changes (potential hijacking)
        var currentIp = GetClientIpAddress(httpContext);
        if (currentIp != session.IpAddress && _options.EnforceIpBinding)
        {
            _logger.LogWarning(
                "[T1185] IP address change detected for session {SessionId}: {OldIp} -> {NewIp}",
                sessionId, session.IpAddress, currentIp);

            // Depending on policy, might invalidate or just log
            if (_options.StrictIpBinding)
            {
                await InvalidateSessionAsync(sessionId, "IP address changed");
                return SessionValidationResult.Invalid("Session IP address mismatch");
            }
        }

        // Update session activity
        session.LastAccessedAt = DateTimeOffset.UtcNow;
        metadata.AccessCount++;

        // T1185: Automatic session rotation on high activity
        if (ShouldRotateSession(metadata))
        {
            await RotateSessionAsync(sessionId, httpContext);
        }

        return SessionValidationResult.Valid(session);
    }

    /// <summary>
    /// T1098 Defense: Rotate session ID on privilege escalation
    /// Prevents session fixation attacks during privilege changes
    /// </summary>
    public async Task<string> RotateSessionOnPrivilegeChangeAsync(
        string oldSessionId, 
        string newPrivilegeLevel,
        HttpContext httpContext)
    {
        if (!_activeSessions.TryGetValue(oldSessionId, out var metadata))
        {
            throw new InvalidOperationException("Session not found");
        }

        var oldSession = metadata.Session;
        
        _logger.LogInformation(
            "[T1098] Rotating session due to privilege change: {UserId}, " +
            "Old Privilege: {OldPrivilege}, New Privilege: {NewPrivilege}",
            oldSession.UserId, oldSession.PrivilegeLevel, newPrivilegeLevel);

        // Create new session ID
        var newSessionId = GenerateSecureSessionId();
        
        // Create new session with updated privileges
        var newSession = new SecureSession
        {
            SessionId = newSessionId,
            UserId = oldSession.UserId,
            Fingerprint = GenerateClientFingerprint(httpContext), // Re-fingerprint
            CreatedAt = DateTimeOffset.UtcNow,
            LastAccessedAt = DateTimeOffset.UtcNow,
            ExpiresAt = DateTimeOffset.UtcNow.Add(_options.SessionTimeout),
            PrivilegeLevel = newPrivilegeLevel,
            IpAddress = GetClientIpAddress(httpContext),
            UserAgent = httpContext.Request.Headers["User-Agent"].ToString(),
            RotatedFrom = oldSessionId
        };

        var newMetadata = new SessionMetadata
        {
            Session = newSession,
            AccessCount = 0,
            LastRotationAt = DateTimeOffset.UtcNow
        };

        // Replace old session with new one
        _activeSessions[newSessionId] = newMetadata;
        await InvalidateSessionAsync(oldSessionId, "Rotated due to privilege change");

        // Update user session tracking
        if (_userSessions.TryGetValue(oldSession.UserId, out var sessions))
        {
            lock (sessions)
            {
                sessions.Remove(oldSessionId);
                sessions.Add(newSessionId);
            }
        }

        return newSessionId;
    }

    /// <summary>
    /// T1185 Defense: Detect concurrent session anomalies
    /// Alerts when user has suspicious number of concurrent sessions
    /// </summary>
    private async Task DetectConcurrentSessionAnomaliesAsync(string userId, SecureSession newSession)
    {
        if (!_userSessions.TryGetValue(userId, out var sessions))
            return;

        int activeCount;
        lock (sessions)
        {
            // Clean up expired sessions
            sessions.RemoveWhere(sid => 
            {
                if (_activeSessions.TryGetValue(sid, out var meta))
                {
                    return DateTimeOffset.UtcNow > meta.Session.ExpiresAt;
                }
                return true;
            });

            activeCount = sessions.Count;
        }

        // T1185: Alert on suspicious concurrent session count
        if (activeCount > _options.MaxConcurrentSessions)
        {
            _logger.LogWarning(
                "[T1185] SECURITY ALERT: User {UserId} has {Count} concurrent sessions " +
                "(max: {Max}). Possible account compromise.",
                userId, activeCount, _options.MaxConcurrentSessions);

            // Optional: Implement policy to invalidate oldest sessions or require re-authentication
            await EnforceConcurrentSessionLimitAsync(userId);
        }
    }

    /// <summary>
    /// T1550.004 Defense: Invalidate session and log event
    /// </summary>
    public async Task InvalidateSessionAsync(string sessionId, string reason)
    {
        if (_activeSessions.TryRemove(sessionId, out var metadata))
        {
            var session = metadata.Session;
            
            _logger.LogInformation(
                "[T1185] Session invalidated: {SessionId}, UserId: {UserId}, Reason: {Reason}",
                sessionId, session.UserId, reason);

            // Remove from user session tracking
            if (_userSessions.TryGetValue(session.UserId, out var sessions))
            {
                lock (sessions)
                {
                    sessions.Remove(sessionId);
                }
            }

            // Could also add to a blacklist or audit log here
            await Task.CompletedTask;
        }
    }

    /// <summary>
    /// T1185: Invalidate all sessions for a user (e.g., on password change or suspected compromise)
    /// </summary>
    public async Task InvalidateAllUserSessionsAsync(string userId, string reason)
    {
        if (!_userSessions.TryRemove(userId, out var sessions))
            return;

        List<string> sessionIds;
        lock (sessions)
        {
            sessionIds = sessions.ToList();
        }

        _logger.LogWarning(
            "[T1185] Invalidating all sessions for user {UserId}. Count: {Count}, Reason: {Reason}",
            userId, sessionIds.Count, reason);

        foreach (var sessionId in sessionIds)
        {
            await InvalidateSessionAsync(sessionId, reason);
        }
    }

    #region Private Helper Methods

    private string GenerateSecureSessionId()
    {
        // Generate cryptographically secure random session ID
        var bytes = new byte[32];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(bytes);
        return Convert.ToBase64String(bytes)
            .Replace('+', '-')
            .Replace('/', '_')
            .TrimEnd('=');
    }

    /// <summary>
    /// T1185: Generate client fingerprint from IP + User-Agent
    /// More sophisticated implementations might include TLS fingerprinting, canvas fingerprinting, etc.
    /// </summary>
    private string GenerateClientFingerprint(HttpContext context)
    {
        var ip = GetClientIpAddress(context);
        var userAgent = context.Request.Headers["User-Agent"].ToString();
        
        // Could include additional entropy like Accept-Language, Accept-Encoding, etc.
        var fingerprintData = $"{ip}|{userAgent}";
        
        using var sha256 = SHA256.Create();
        var hash = sha256.ComputeHash(Encoding.UTF8.GetBytes(fingerprintData));
        return Convert.ToBase64String(hash);
    }

    private string GetClientIpAddress(HttpContext context)
    {
        // Check for forwarded IP (behind proxy/load balancer)
        var forwardedFor = context.Request.Headers["X-Forwarded-For"].FirstOrDefault();
        if (!string.IsNullOrEmpty(forwardedFor))
        {
            return forwardedFor.Split(',')[0].Trim();
        }

        return context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
    }

    private bool ShouldRotateSession(SessionMetadata metadata)
    {
        // Rotate session ID periodically to reduce hijacking window
        var timeSinceRotation = DateTimeOffset.UtcNow - metadata.LastRotationAt;
        return timeSinceRotation > _options.RotationInterval;
    }

    private async Task RotateSessionAsync(string oldSessionId, HttpContext httpContext)
    {
        if (!_activeSessions.TryGetValue(oldSessionId, out var metadata))
            return;

        var newSessionId = GenerateSecureSessionId();
        var newMetadata = new SessionMetadata
        {
            Session = metadata.Session with 
            { 
                SessionId = newSessionId,
                RotatedFrom = oldSessionId
            },
            AccessCount = 0,
            LastRotationAt = DateTimeOffset.UtcNow
        };

        _activeSessions[newSessionId] = newMetadata;
        _activeSessions.TryRemove(oldSessionId, out _);

        _logger.LogInformation(
            "[T1185] Session rotated: {OldId} -> {NewId}",
            oldSessionId, newSessionId);

        await Task.CompletedTask;
    }

    private async Task EnforceConcurrentSessionLimitAsync(string userId)
    {
        if (!_userSessions.TryGetValue(userId, out var sessions))
            return;

        List<(string sessionId, DateTimeOffset lastAccess)> sessionList;
        
        lock (sessions)
        {
            sessionList = sessions
                .Select(sid => 
                {
                    if (_activeSessions.TryGetValue(sid, out var meta))
                    {
                        return (sid, meta.Session.LastAccessedAt);
                    }
                    return (sid, DateTimeOffset.MinValue);
                })
                .OrderBy(s => s.lastAccess)
                .ToList();

            // Keep only the most recent sessions
            var toRemove = sessionList
                .Take(sessionList.Count - _options.MaxConcurrentSessions)
                .Select(s => s.sessionId)
                .ToList();

            foreach (var sessionId in toRemove)
            {
                await InvalidateSessionAsync(sessionId, "Concurrent session limit exceeded");
            }
        }
    }

    #endregion
}

#region Supporting Types

public record SecureSession
{
    public required string SessionId { get; init; }
    public required string UserId { get; init; }
    public required string Fingerprint { get; init; }
    public required DateTimeOffset CreatedAt { get; init; }
    public required DateTimeOffset LastAccessedAt { get; set; }
    public required DateTimeOffset ExpiresAt { get; init; }
    public required string PrivilegeLevel { get; init; }
    public required string IpAddress { get; init; }
    public required string UserAgent { get; init; }
    public string? RotatedFrom { get; init; }
}

internal class SessionMetadata
{
    public required SecureSession Session { get; set; }
    public int AccessCount { get; set; }
    public DateTimeOffset LastRotationAt { get; set; }
}

public record SessionValidationResult
{
    public bool IsValid { get; init; }
    public string? ErrorMessage { get; init; }
    public SecureSession? Session { get; init; }

    public static SessionValidationResult Valid(SecureSession session) =>
        new() { IsValid = true, Session = session };

    public static SessionValidationResult Invalid(string message) =>
        new() { IsValid = false, ErrorMessage = message };
}

public class SessionSecurityOptions
{
    public TimeSpan SessionTimeout { get; set; } = TimeSpan.FromMinutes(30);
    public TimeSpan RotationInterval { get; set; } = TimeSpan.FromMinutes(15);
    public int MaxConcurrentSessions { get; set; } = 3;
    public bool EnforceIpBinding { get; set; } = true;
    public bool StrictIpBinding { get; set; } = false; // If true, IP change invalidates session
}

#endregion

/// <summary>
/// Key Takeaways for Session Security:
/// 
/// T1185 - Browser Session Hijacking Defense:
/// 1. Bind sessions to client fingerprint (IP + User-Agent hash)
/// 2. Detect and alert on IP address changes
/// 3. Implement automatic session rotation
/// 4. Monitor for concurrent session anomalies
/// 5. Use cryptographically secure session IDs
/// 
/// T1098 - Account Manipulation Defense:
/// 1. Rotate session on privilege changes
/// 2. Invalidate all sessions on password change
/// 3. Enforce maximum concurrent sessions
/// 4. Log all session lifecycle events
/// 
/// T1550.004 - Web Session Cookie Defense:
/// 1. Use HttpOnly and Secure cookie flags (in middleware)
/// 2. Implement SameSite cookie policy
/// 3. Set appropriate session timeouts
/// 4. Never expose session tokens in URLs
/// 
/// References:
/// - MITRE ATT&CK T1185: https://attack.mitre.org/techniques/T1185/
/// - MITRE ATT&CK T1098: https://attack.mitre.org/techniques/T1098/
/// - MITRE ATT&CK T1550.004: https://attack.mitre.org/techniques/T1550/004/
/// - OWASP Session Management Cheat Sheet
/// </summary>
