using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Text.RegularExpressions;

namespace MitreAttackForDevs.Samples;

/// <summary>
/// Demonstrates T1059 - Command and Scripting Interpreter
/// Shows vulnerable command injection and secure alternatives
/// </summary>
public class CommandInjectionExamples
{
    #region VULNERABLE - DO NOT USE IN PRODUCTION

    /// <summary>
    /// VULNERABLE: T1059 - Command Injection
    /// This endpoint is vulnerable to command injection attacks.
    /// Example malicious input: "google.com && rm -rf /" or "google.com; cat /etc/passwd"
    /// </summary>
    [HttpGet("api/vulnerable/ping")]
    public IActionResult VulnerablePing([FromQuery] string host)
    {
        // DANGER: User input is passed directly to shell
        var processInfo = new ProcessStartInfo
        {
            FileName = "/bin/bash",  // or "cmd.exe" on Windows
            Arguments = $"-c \"ping -c 4 {host}\"",  // User input concatenated directly!
            RedirectStandardOutput = true,
            UseShellExecute = false
        };

        using var process = Process.Start(processInfo);
        using var reader = process.StandardOutput;
        var output = reader.ReadToEnd();
        process.WaitForExit();

        return new OkObjectResult(new { result = output });
    }

    /// <summary>
    /// VULNERABLE: Another common pattern - Using cmd.exe with string concatenation
    /// Vulnerable to: "example.com & whoami" or "example.com | type C:\passwords.txt"
    /// </summary>
    [HttpGet("api/vulnerable/ping-windows")]
    public IActionResult VulnerablePingWindows([FromQuery] string host)
    {
        // DANGER: Shell execution with user-controlled input
        var startInfo = new ProcessStartInfo
        {
            FileName = "cmd.exe",
            Arguments = $"/c ping -n 4 {host}",  // Command injection vulnerability!
            RedirectStandardOutput = true,
            UseShellExecute = false
        };

        using var process = Process.Start(startInfo);
        var output = process.StandardOutput.ReadToEnd();
        process.WaitForExit();

        return new OkObjectResult(new { result = output });
    }

    #endregion

    #region DEFENDED - Secure Implementation

    /// <summary>
    /// DEFENDED: T1059 - Multiple layers of defense
    /// 1. Input validation with strict allowlist
    /// 2. No shell execution
    /// 3. Arguments passed as array (not string concatenation)
    /// 4. Timeout enforcement
    /// </summary>
    [HttpGet("api/secure/ping")]
    public async Task<IActionResult> SecurePing([FromQuery] string host)
    {
        // Defense Layer 1: Input Validation
        if (!IsValidHost(host))
        {
            return new BadRequestObjectResult(new 
            { 
                error = "Invalid host format",
                technique = "T1059 - Command Injection Prevention"
            });
        }

        // Defense Layer 2: Use allowlist of permitted commands
        var allowedCommands = new HashSet<string> { "ping" };
        var command = "ping";
        
        if (!allowedCommands.Contains(command))
        {
            return new BadRequestObjectResult(new { error = "Command not allowed" });
        }

        try
        {
            // Defense Layer 3: No shell execution, direct process invocation
            var processInfo = new ProcessStartInfo
            {
                FileName = OperatingSystem.IsWindows() ? "ping.exe" : "ping",
                
                // Defense Layer 4: Use ArgumentList instead of Arguments string
                // This prevents shell interpretation of special characters
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,  // Critical: No shell interpretation
                CreateNoWindow = true
            };

            // Add arguments individually - prevents injection
            if (OperatingSystem.IsWindows())
            {
                processInfo.ArgumentList.Add("-n");
                processInfo.ArgumentList.Add("4");
            }
            else
            {
                processInfo.ArgumentList.Add("-c");
                processInfo.ArgumentList.Add("4");
            }
            processInfo.ArgumentList.Add(host);  // Even if malicious, it's just one argument

            using var process = Process.Start(processInfo);
            
            // Defense Layer 5: Timeout enforcement
            using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10));
            
            var outputTask = process.StandardOutput.ReadToEndAsync();
            var errorTask = process.StandardError.ReadToEndAsync();
            
            await process.WaitForExitAsync(cts.Token);
            
            var output = await outputTask;
            var error = await errorTask;

            // Defense Layer 6: Logging and monitoring
            if (process.ExitCode != 0)
            {
                // Log suspicious activity
                Console.WriteLine($"[SECURITY] Ping failed for host: {host}, Exit Code: {process.ExitCode}");
            }

            return new OkObjectResult(new 
            { 
                result = output,
                exitCode = process.ExitCode,
                technique = "T1059 - Defended with input validation and safe process execution"
            });
        }
        catch (OperationCanceledException)
        {
            return new StatusCodeResult(StatusCodes.Status408RequestTimeout);
        }
        catch (Exception ex)
        {
            // Defense Layer 7: Safe error handling - don't leak system information
            Console.WriteLine($"[SECURITY] Exception during ping: {ex.Message}");
            return new StatusCodeResult(StatusCodes.Status500InternalServerError);
        }
    }

    /// <summary>
    /// Validates host input using strict allowlist pattern
    /// Allows: domain names, IPv4, IPv6
    /// </summary>
    private bool IsValidHost(string host)
    {
        if (string.IsNullOrWhiteSpace(host) || host.Length > 253)
            return false;

        // Check for shell metacharacters that could be used for injection
        var dangerousChars = new[] { ';', '&', '|', '$', '`', '\n', '\r', '<', '>', '(', ')', '{', '}' };
        if (dangerousChars.Any(c => host.Contains(c)))
            return false;

        // Validate IPv4
        if (System.Net.IPAddress.TryParse(host, out var ip))
        {
            return ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork ||
                   ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetworkV6;
        }

        // Validate domain name (strict pattern)
        var domainPattern = @"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$";
        return Regex.IsMatch(host, domainPattern);
    }

    #endregion

    #region Additional Defensive Utilities

    /// <summary>
    /// Alternative: Use a process wrapper with built-in security controls
    /// </summary>
    public class SecureProcessExecutor
    {
        private readonly HashSet<string> _allowedExecutables;
        private readonly TimeSpan _defaultTimeout;
        private readonly ILogger _logger;

        public SecureProcessExecutor(ILogger logger, TimeSpan? timeout = null)
        {
            _logger = logger;
            _defaultTimeout = timeout ?? TimeSpan.FromSeconds(30);
            
            // T1059 Defense: Strict allowlist of permitted executables
            _allowedExecutables = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
            {
                "ping", "ping.exe",
                "nslookup", "nslookup.exe",
                "traceroute", "tracert.exe"
            };
        }

        public async Task<ProcessResult> ExecuteAsync(
            string executable, 
            IEnumerable<string> arguments, 
            CancellationToken cancellationToken = default)
        {
            // Validate executable is in allowlist
            if (!_allowedExecutables.Contains(Path.GetFileName(executable)))
            {
                _logger.LogWarning("[T1059] Blocked attempt to execute non-allowlisted command: {Executable}", executable);
                throw new SecurityException($"Executable not permitted: {executable}");
            }

            var startInfo = new ProcessStartInfo
            {
                FileName = executable,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            // Add arguments safely
            foreach (var arg in arguments)
            {
                startInfo.ArgumentList.Add(arg);
            }

            using var process = Process.Start(startInfo);
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
            cts.CancelAfter(_defaultTimeout);

            var outputTask = process.StandardOutput.ReadToEndAsync();
            var errorTask = process.StandardError.ReadToEndAsync();

            await process.WaitForExitAsync(cts.Token);

            return new ProcessResult
            {
                ExitCode = process.ExitCode,
                StandardOutput = await outputTask,
                StandardError = await errorTask
            };
        }
    }

    public record ProcessResult
    {
        public int ExitCode { get; init; }
        public string StandardOutput { get; init; } = string.Empty;
        public string StandardError { get; init; } = string.Empty;
    }

    #endregion
}

/// <summary>
/// Key Takeaways for T1059 Defense:
/// 
/// 1. NEVER concatenate user input into command strings
/// 2. NEVER use shell execution (UseShellExecute = false)
/// 3. ALWAYS use ArgumentList instead of Arguments property
/// 4. ALWAYS validate input with strict allowlist patterns
/// 5. ALWAYS use command allowlisting
/// 6. ALWAYS enforce timeouts
/// 7. ALWAYS log suspicious activity
/// 8. Consider using higher-level libraries instead of shell commands
/// 
/// References:
/// - MITRE ATT&CK T1059: https://attack.mitre.org/techniques/T1059/
/// - CWE-78: OS Command Injection
/// - OWASP: Command Injection
/// </summary>
