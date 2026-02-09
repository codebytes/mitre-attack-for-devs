using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

namespace MitreAttackForDevs.Samples;

/// <summary>
/// Demonstrates defense against T1070 - Indicator Removal
/// Implements tamper-evident logging using hash chain (blockchain-like structure)
/// Each log entry includes hash of previous entry, making tampering detectable
/// </summary>
public class TamperEvidentLogger
{
    private readonly string _logFilePath;
    private readonly object _lock = new();
    private string _lastHash;
    private long _entryCount;

    // T1070 Defense: Store hash of genesis block
    private const string GenesisHash = "0000000000000000000000000000000000000000000000000000000000000000";

    public TamperEvidentLogger(string logFilePath)
    {
        _logFilePath = logFilePath;
        _lastHash = GenesisHash;
        _entryCount = 0;
        
        // Initialize or load existing log
        InitializeLog();
    }

    /// <summary>
    /// T1070 Defense: Write tamper-evident log entry
    /// Each entry includes: previous hash, timestamp, data, sequence number
    /// </summary>
    public async Task<LogEntry> WriteLogAsync(
        string level, 
        string message, 
        string? userId = null,
        Dictionary<string, object>? additionalData = null)
    {
        lock (_lock)
        {
            var entry = new LogEntry
            {
                SequenceNumber = ++_entryCount,
                Timestamp = DateTimeOffset.UtcNow,
                Level = level,
                Message = message,
                UserId = userId,
                AdditionalData = additionalData ?? new Dictionary<string, object>(),
                PreviousHash = _lastHash
            };

            // Calculate hash of this entry (includes previous hash)
            entry.Hash = ComputeEntryHash(entry);
            
            // Update chain state
            _lastHash = entry.Hash;

            // Persist to file (append-only)
            var json = JsonSerializer.Serialize(entry);
            File.AppendAllText(_logFilePath, json + Environment.NewLine);

            return entry;
        }
    }

    /// <summary>
    /// T1070 Defense: Write security event with ATT&CK technique ID
    /// </summary>
    public async Task<LogEntry> WriteSecurityEventAsync(
        string technique,
        string description,
        string severity,
        string? userId = null,
        Dictionary<string, object>? details = null)
    {
        var additionalData = details ?? new Dictionary<string, object>();
        additionalData["AttackTechnique"] = technique;
        additionalData["Severity"] = severity;
        additionalData["EventType"] = "SecurityEvent";

        return await WriteLogAsync("SECURITY", description, userId, additionalData);
    }

    /// <summary>
    /// T1070 Detection: Verify integrity of entire log chain
    /// Returns verification result with details of any tampering detected
    /// </summary>
    public LogVerificationResult VerifyLogIntegrity()
    {
        var lines = File.ReadAllLines(_logFilePath);
        var result = new LogVerificationResult
        {
            TotalEntries = lines.Length,
            VerifiedAt = DateTimeOffset.UtcNow
        };

        if (lines.Length == 0)
        {
            result.IsValid = true;
            result.Message = "Log is empty";
            return result;
        }

        string expectedPreviousHash = GenesisHash;
        long expectedSequence = 1;

        for (int i = 0; i < lines.Length; i++)
        {
            try
            {
                var entry = JsonSerializer.Deserialize<LogEntry>(lines[i]);
                if (entry == null)
                {
                    result.IsValid = false;
                    result.FirstTamperedEntry = i + 1;
                    result.Message = $"T1070 DETECTED: Entry {i + 1} is null or corrupted";
                    return result;
                }

                // Verify sequence number
                if (entry.SequenceNumber != expectedSequence)
                {
                    result.IsValid = false;
                    result.FirstTamperedEntry = i + 1;
                    result.Message = $"T1070 DETECTED: Sequence number mismatch at entry {i + 1}. " +
                                   $"Expected {expectedSequence}, got {entry.SequenceNumber}";
                    return result;
                }

                // Verify previous hash chain
                if (entry.PreviousHash != expectedPreviousHash)
                {
                    result.IsValid = false;
                    result.FirstTamperedEntry = i + 1;
                    result.Message = $"T1070 DETECTED: Hash chain broken at entry {i + 1}. " +
                                   $"Previous hash mismatch. Possible log tampering or deletion.";
                    result.TamperDetails = new Dictionary<string, string>
                    {
                        ["ExpectedPreviousHash"] = expectedPreviousHash,
                        ["ActualPreviousHash"] = entry.PreviousHash,
                        ["EntryTimestamp"] = entry.Timestamp.ToString("O"),
                        ["EntrySequence"] = entry.SequenceNumber.ToString()
                    };
                    return result;
                }

                // Verify entry's own hash
                var computedHash = ComputeEntryHash(entry);
                if (computedHash != entry.Hash)
                {
                    result.IsValid = false;
                    result.FirstTamperedEntry = i + 1;
                    result.Message = $"T1070 DETECTED: Entry hash mismatch at entry {i + 1}. " +
                                   $"Entry has been modified.";
                    result.TamperDetails = new Dictionary<string, string>
                    {
                        ["ExpectedHash"] = computedHash,
                        ["ActualHash"] = entry.Hash,
                        ["EntryData"] = JsonSerializer.Serialize(entry)
                    };
                    return result;
                }

                // Prepare for next iteration
                expectedPreviousHash = entry.Hash;
                expectedSequence++;
            }
            catch (Exception ex)
            {
                result.IsValid = false;
                result.FirstTamperedEntry = i + 1;
                result.Message = $"T1070 DETECTED: Error parsing entry {i + 1}: {ex.Message}";
                return result;
            }
        }

        result.IsValid = true;
        result.Message = "Log integrity verified. No tampering detected.";
        return result;
    }

    /// <summary>
    /// T1070 Detection: Get all entries (for audit/review)
    /// </summary>
    public List<LogEntry> GetAllEntries()
    {
        var lines = File.ReadAllLines(_logFilePath);
        var entries = new List<LogEntry>();

        foreach (var line in lines)
        {
            try
            {
                var entry = JsonSerializer.Deserialize<LogEntry>(line);
                if (entry != null)
                {
                    entries.Add(entry);
                }
            }
            catch
            {
                // Log corruption detected
                continue;
            }
        }

        return entries;
    }

    /// <summary>
    /// T1070 Detection: Search for security events by technique ID
    /// </summary>
    public List<LogEntry> FindSecurityEvents(string? techniqueId = null)
    {
        var entries = GetAllEntries();
        
        var securityEvents = entries.Where(e => 
            e.Level == "SECURITY" &&
            e.AdditionalData.ContainsKey("EventType") &&
            e.AdditionalData["EventType"].ToString() == "SecurityEvent"
        );

        if (!string.IsNullOrEmpty(techniqueId))
        {
            securityEvents = securityEvents.Where(e =>
                e.AdditionalData.ContainsKey("AttackTechnique") &&
                e.AdditionalData["AttackTechnique"].ToString() == techniqueId
            );
        }

        return securityEvents.ToList();
    }

    /// <summary>
    /// T1070 Defense: Export log with cryptographic proof
    /// Generates a signature file that can be used to verify log hasn't been replaced
    /// </summary>
    public async Task<string> ExportLogWithProofAsync(string exportPath)
    {
        // Verify integrity first
        var verification = VerifyLogIntegrity();
        if (!verification.IsValid)
        {
            throw new InvalidOperationException(
                $"Cannot export tampered log. {verification.Message}");
        }

        // Copy log file
        File.Copy(_logFilePath, exportPath, overwrite: true);

        // Create proof file with metadata and final hash
        var proof = new LogExportProof
        {
            ExportedAt = DateTimeOffset.UtcNow,
            TotalEntries = _entryCount,
            FinalHash = _lastHash,
            GenesisHash = GenesisHash,
            LogFilePath = _logFilePath
        };

        var proofPath = exportPath + ".proof";
        var proofJson = JsonSerializer.Serialize(proof, new JsonSerializerOptions 
        { 
            WriteIndented = true 
        });
        await File.WriteAllTextAsync(proofPath, proofJson);

        return proofPath;
    }

    /// <summary>
    /// T1070 Defense: Verify exported log against proof file
    /// </summary>
    public static bool VerifyExportedLog(string logPath, string proofPath)
    {
        if (!File.Exists(logPath) || !File.Exists(proofPath))
            return false;

        var proofJson = File.ReadAllText(proofPath);
        var proof = JsonSerializer.Deserialize<LogExportProof>(proofJson);
        if (proof == null)
            return false;

        // Create temporary logger instance to verify
        var tempLogger = new TamperEvidentLogger(logPath);
        var verification = tempLogger.VerifyLogIntegrity();

        if (!verification.IsValid)
            return false;

        // Verify final hash matches proof
        return tempLogger._lastHash == proof.FinalHash &&
               tempLogger._entryCount == proof.TotalEntries;
    }

    #region Private Methods

    private void InitializeLog()
    {
        if (File.Exists(_logFilePath))
        {
            // Load existing log and restore chain state
            var lines = File.ReadAllLines(_logFilePath);
            if (lines.Length > 0)
            {
                var lastLine = lines[^1];
                var lastEntry = JsonSerializer.Deserialize<LogEntry>(lastLine);
                if (lastEntry != null)
                {
                    _lastHash = lastEntry.Hash;
                    _entryCount = lastEntry.SequenceNumber;
                }
            }
        }
        else
        {
            // Create new log file with header comment
            var header = $"# Tamper-Evident Log - Created: {DateTimeOffset.UtcNow:O}" +
                        Environment.NewLine +
                        $"# Genesis Hash: {GenesisHash}" +
                        Environment.NewLine +
                        $"# Each entry includes hash of previous entry (T1070 Defense)" +
                        Environment.NewLine;
            File.WriteAllText(_logFilePath, header);
        }
    }

    /// <summary>
    /// Compute SHA-256 hash of log entry
    /// Includes all fields except the Hash field itself
    /// </summary>
    private string ComputeEntryHash(LogEntry entry)
    {
        // Create deterministic representation of entry
        var hashInput = $"{entry.SequenceNumber}|" +
                       $"{entry.Timestamp:O}|" +
                       $"{entry.Level}|" +
                       $"{entry.Message}|" +
                       $"{entry.UserId ?? ""}|" +
                       $"{entry.PreviousHash}|" +
                       $"{JsonSerializer.Serialize(entry.AdditionalData)}";

        using var sha256 = SHA256.Create();
        var hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(hashInput));
        return BitConverter.ToString(hashBytes).Replace("-", "").ToLowerInvariant();
    }

    #endregion
}

#region Supporting Types

/// <summary>
/// Tamper-evident log entry with hash chain
/// </summary>
public class LogEntry
{
    public long SequenceNumber { get; set; }
    public DateTimeOffset Timestamp { get; set; }
    public required string Level { get; set; }
    public required string Message { get; set; }
    public string? UserId { get; set; }
    public Dictionary<string, object> AdditionalData { get; set; } = new();
    
    /// <summary>
    /// Hash of the previous entry in the chain
    /// </summary>
    public required string PreviousHash { get; set; }
    
    /// <summary>
    /// SHA-256 hash of this entry (includes PreviousHash)
    /// </summary>
    public string Hash { get; set; } = string.Empty;
}

public class LogVerificationResult
{
    public bool IsValid { get; set; }
    public string Message { get; set; } = string.Empty;
    public int TotalEntries { get; set; }
    public int? FirstTamperedEntry { get; set; }
    public DateTimeOffset VerifiedAt { get; set; }
    public Dictionary<string, string>? TamperDetails { get; set; }
}

public class LogExportProof
{
    public DateTimeOffset ExportedAt { get; set; }
    public long TotalEntries { get; set; }
    public required string FinalHash { get; set; }
    public required string GenesisHash { get; set; }
    public required string LogFilePath { get; set; }
}

#endregion

#region Example Usage

/// <summary>
/// Example usage of TamperEvidentLogger
/// </summary>
public class TamperEvidentLoggerExample
{
    public static async Task DemonstrateUsage()
    {
        var logger = new TamperEvidentLogger("/var/log/security-audit.log");

        // Log normal events
        await logger.WriteLogAsync("INFO", "Application started");
        await logger.WriteLogAsync("INFO", "User logged in", userId: "user123");

        // Log security events with ATT&CK technique IDs
        await logger.WriteSecurityEventAsync(
            technique: "T1059",
            description: "Blocked command injection attempt",
            severity: "HIGH",
            userId: "attacker456",
            details: new Dictionary<string, object>
            {
                ["Command"] = "ping google.com && rm -rf /",
                ["SourceIP"] = "203.0.113.42",
                ["Blocked"] = true
            });

        await logger.WriteSecurityEventAsync(
            technique: "T1070",
            description: "Detected attempt to delete log files",
            severity: "CRITICAL",
            userId: "attacker789",
            details: new Dictionary<string, object>
            {
                ["TargetPath"] = "/var/log/",
                ["Method"] = "File.Delete",
                ["Prevented"] = true
            });

        // Verify integrity
        var verification = logger.VerifyLogIntegrity();
        Console.WriteLine($"Log integrity: {verification.IsValid}");
        Console.WriteLine($"Message: {verification.Message}");

        // Search for specific attacks
        var t1070Events = logger.FindSecurityEvents("T1070");
        Console.WriteLine($"Found {t1070Events.Count} T1070 events");

        // Export with proof
        var proofPath = await logger.ExportLogWithProofAsync("/backup/security-audit.log");
        Console.WriteLine($"Exported with proof: {proofPath}");
    }

    /// <summary>
    /// Demonstrate tamper detection
    /// </summary>
    public static void DemonstrateTamperDetection()
    {
        var logPath = "/tmp/test-tamper.log";
        var logger = new TamperEvidentLogger(logPath);

        // Write some entries
        logger.WriteLogAsync("INFO", "Entry 1").Wait();
        logger.WriteLogAsync("INFO", "Entry 2").Wait();
        logger.WriteLogAsync("INFO", "Entry 3").Wait();

        // Verify - should pass
        var result1 = logger.VerifyLogIntegrity();
        Console.WriteLine($"Before tampering: {result1.IsValid}"); // True

        // Simulate tampering (modify log file directly)
        var lines = File.ReadAllLines(logPath);
        if (lines.Length > 3)
        {
            lines[^1] = lines[^1].Replace("Entry 3", "Entry 3 MODIFIED");
            File.WriteAllLines(logPath, lines);
        }

        // Verify - should fail
        var result2 = logger.VerifyLogIntegrity();
        Console.WriteLine($"After tampering: {result2.IsValid}"); // False
        Console.WriteLine($"Tamper detected: {result2.Message}");
        Console.WriteLine($"First tampered entry: {result2.FirstTamperedEntry}");
    }
}

#endregion

/// <summary>
/// Key Takeaways for T1070 Defense (Indicator Removal):
/// 
/// 1. Use append-only logs with hash chains (like blockchain)
/// 2. Each entry includes hash of previous entry
/// 3. Any modification breaks the chain and is detectable
/// 4. Include sequence numbers to detect deletions
/// 5. Store logs in write-once storage when possible
/// 6. Regularly verify log integrity
/// 7. Export logs with cryptographic proofs
/// 8. Forward logs to separate SIEM/log aggregation system
/// 9. Use file system permissions to prevent modification
/// 10. Monitor for unauthorized log access attempts
/// 
/// Additional Defenses:
/// - Store logs on separate system/network segment
/// - Use cryptographic signing (not just hashing)
/// - Implement log forwarding to immutable storage (S3 with object lock)
/// - Enable OS-level audit logging (auditd, ETW)
/// - Monitor for attempts to clear event logs
/// 
/// References:
/// - MITRE ATT&CK T1070: https://attack.mitre.org/techniques/T1070/
/// - NIST SP 800-92: Guide to Computer Security Log Management
/// - OWASP Logging Cheat Sheet
/// </summary>
