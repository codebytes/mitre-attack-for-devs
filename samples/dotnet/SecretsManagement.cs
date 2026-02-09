using Microsoft.Extensions.Configuration;
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

namespace MitreAttackForDevs.Samples;

/// <summary>
/// Demonstrates T1552 - Unsecured Credentials
/// Shows BAD patterns (hardcoded secrets) vs GOOD patterns (secure secrets management)
/// </summary>
public class SecretsManagementExamples
{
    #region VULNERABLE - DO NOT USE IN PRODUCTION

    /// <summary>
    /// T1552.001: VULNERABLE - Hardcoded credentials in source code
    /// These secrets would be exposed in:
    /// - Source code repositories (Git history)
    /// - Decompiled assemblies
    /// - Configuration files in repos
    /// - Log files and error messages
    /// </summary>
    public class VulnerableDataAccess_HardcodedSecrets
    {
        // DANGER: Hardcoded connection string with credentials
        private const string ConnectionString = 
            "Server=prod-db.example.com;Database=CustomerDB;User Id=admin;Password=SuperSecret123!;";

        // DANGER: Hardcoded API keys
        private const string StripeApiKey = "sk_live_51234567890abcdefghijk";
        private const string SendGridApiKey = "SG.1234567890abcdefghijklmnop";
        private const string AwsAccessKey = "AKIAIOSFODNN7EXAMPLE";
        private const string AwsSecretKey = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

        // DANGER: Hardcoded encryption keys
        private const string EncryptionKey = "MySuper$ecretK3y!12345678901234";

        public void ConnectToDatabase()
        {
            // This exposes credentials in source code, version control, and compiled assemblies
            using var connection = new System.Data.SqlClient.SqlConnection(ConnectionString);
            connection.Open();
            // ... database operations
        }

        public void CallExternalApi()
        {
            var client = new HttpClient();
            // Hardcoded API key in request header
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {StripeApiKey}");
        }
    }

    /// <summary>
    /// T1552.001: VULNERABLE - Secrets in configuration files committed to source control
    /// </summary>
    public class VulnerableConfig_SecretsInAppSettings
    {
        // This configuration would be in appsettings.json, often committed to Git
        /*
        {
          "ConnectionStrings": {
            "DefaultConnection": "Server=prod-db;User=admin;Password=Secret123!;"
          },
          "ApiKeys": {
            "Stripe": "sk_live_51234567890",
            "SendGrid": "SG.1234567890abcdef"
          },
          "Jwt": {
            "SecretKey": "MyJwtSecret12345678901234567890",
            "Issuer": "myapp.com"
          }
        }
        */
        
        // Even though it's in a config file, it's still hardcoded and in source control!
    }

    /// <summary>
    /// T1552.001: VULNERABLE - Secrets in environment variables set in code
    /// </summary>
    public class VulnerableEnvironment_HardcodedInCode
    {
        public void InitializeApp()
        {
            // Setting secrets in code defeats the purpose of environment variables
            Environment.SetEnvironmentVariable("DB_PASSWORD", "MyPassword123!");
            Environment.SetEnvironmentVariable("API_KEY", "sk_live_1234567890");
        }
    }

    /// <summary>
    /// T1552.001: VULNERABLE - Secrets logged or exposed in error messages
    /// </summary>
    public class VulnerableLogging_SecretExposure
    {
        public void ProcessPayment(string apiKey, string cardNumber)
        {
            try
            {
                // ... payment processing
                throw new Exception("Payment failed");
            }
            catch (Exception ex)
            {
                // DANGER: Logging sensitive data
                Console.WriteLine($"Payment failed with API key: {apiKey}, Card: {cardNumber}");
                
                // DANGER: Exception messages might contain secrets
                throw new Exception($"Failed to connect with connection string: {GetConnectionString()}", ex);
            }
        }

        private string GetConnectionString() => "Server=prod;User=admin;Password=Secret!";
    }

    #endregion

    #region DEFENDED - Secure Secrets Management

    /// <summary>
    /// T1552 Defense: Using IConfiguration with multiple secure sources
    /// Secrets come from User Secrets (dev), Environment Variables, or Key Vault (prod)
    /// </summary>
    public class SecureDataAccess_ConfigurationPattern
    {
        private readonly IConfiguration _configuration;
        private readonly ILogger<SecureDataAccess_ConfigurationPattern> _logger;

        public SecureDataAccess_ConfigurationPattern(
            IConfiguration configuration,
            ILogger<SecureDataAccess_ConfigurationPattern> logger)
        {
            _configuration = configuration;
            _logger = logger;
        }

        public void ConnectToDatabase()
        {
            // ✅ SECURE: Connection string from configuration provider
            // Sources (in priority order):
            // 1. User Secrets (development only - stored outside project)
            // 2. Environment Variables (server/container config)
            // 3. Azure Key Vault (production)
            var connectionString = _configuration.GetConnectionString("DefaultConnection");
            
            if (string.IsNullOrEmpty(connectionString))
            {
                _logger.LogError("[T1552] Connection string not configured");
                throw new InvalidOperationException("Database connection not configured");
            }

            using var connection = new System.Data.SqlClient.SqlConnection(connectionString);
            connection.Open();
            
            // ✅ Log access without exposing credentials
            _logger.LogInformation("[T1552] Database connection established to {Server}", 
                connection.DataSource);
        }

        public async Task<string> GetApiKeyAsync()
        {
            // ✅ SECURE: API key from secure configuration
            var apiKey = _configuration["ApiKeys:Stripe"];
            
            if (string.IsNullOrEmpty(apiKey))
            {
                _logger.LogError("[T1552] API key not configured");
                throw new InvalidOperationException("Stripe API key not configured");
            }

            return apiKey;
        }
    }

    /// <summary>
    /// T1552 Defense: Using Options Pattern with validation
    /// Provides type-safe access to configuration with validation
    /// </summary>
    public class SecureOptions_TypedConfiguration
    {
        // Configuration classes (no secrets hardcoded)
        public class DatabaseOptions
        {
            public const string SectionName = "Database";
            
            public required string ConnectionString { get; set; }
            public int MaxRetries { get; set; } = 3;
            public int CommandTimeout { get; set; } = 30;
        }

        public class ApiOptions
        {
            public const string SectionName = "ExternalApis";
            
            public required string StripeApiKey { get; set; }
            public required string SendGridApiKey { get; set; }
            public string? BaseUrl { get; set; }
        }

        // Usage in service
        public class SecurePaymentService
        {
            private readonly ApiOptions _apiOptions;
            private readonly ILogger<SecurePaymentService> _logger;

            public SecurePaymentService(
                IOptions<ApiOptions> apiOptions,
                ILogger<SecurePaymentService> logger)
            {
                _apiOptions = apiOptions.Value;
                _logger = logger;
                
                // ✅ Validate configuration on startup
                ValidateConfiguration();
            }

            private void ValidateConfiguration()
            {
                if (string.IsNullOrEmpty(_apiOptions.StripeApiKey))
                {
                    throw new InvalidOperationException(
                        "[T1552] Stripe API key not configured. " +
                        "Set via User Secrets, Environment Variable, or Key Vault.");
                }

                if (_apiOptions.StripeApiKey.Contains("YOUR_KEY_HERE") ||
                    _apiOptions.StripeApiKey.Contains("REPLACE_ME"))
                {
                    throw new InvalidOperationException(
                        "[T1552] Stripe API key appears to be a placeholder. " +
                        "Configure a real key in secure storage.");
                }
            }

            public async Task ProcessPaymentAsync(decimal amount)
            {
                var client = new HttpClient();
                
                // ✅ Use secret from validated configuration
                client.DefaultRequestHeaders.Add(
                    "Authorization", 
                    $"Bearer {_apiOptions.StripeApiKey}");

                // ✅ Log operation without exposing secret
                _logger.LogInformation(
                    "[T1552] Processing payment of {Amount} (API key: ****{Suffix})",
                    amount,
                    _apiOptions.StripeApiKey.Substring(Math.Max(0, _apiOptions.StripeApiKey.Length - 4)));
            }
        }
    }

    /// <summary>
    /// T1552 Defense: Azure Key Vault integration
    /// Secrets stored in managed key vault, accessed at runtime
    /// </summary>
    public class SecureKeyVault_AzureKeyVault
    {
        private readonly SecretClient _secretClient;
        private readonly ILogger<SecureKeyVault_AzureKeyVault> _logger;

        // ✅ Key Vault URL can be in config (not a secret)
        private const string KeyVaultUrl = "https://myapp-keyvault.vault.azure.net/";

        public SecureKeyVault_AzureKeyVault(ILogger<SecureKeyVault_AzureKeyVault> logger)
        {
            _logger = logger;
            
            // ✅ SECURE: Use Managed Identity or DefaultAzureCredential
            // No credentials in code - uses Azure AD authentication
            // Priority: Environment -> Managed Identity -> Visual Studio -> Azure CLI
            _secretClient = new SecretClient(
                new Uri(KeyVaultUrl), 
                new DefaultAzureCredential());
        }

        public async Task<string> GetDatabasePasswordAsync()
        {
            try
            {
                // ✅ Retrieve secret from Key Vault at runtime
                KeyVaultSecret secret = await _secretClient.GetSecretAsync("DatabasePassword");
                
                _logger.LogInformation("[T1552] Retrieved database password from Key Vault");
                
                return secret.Value;
            }
            catch (Exception ex)
            {
                // ✅ Log error without exposing secrets
                _logger.LogError(ex, "[T1552] Failed to retrieve secret from Key Vault");
                throw;
            }
        }

        public async Task<string> GetConnectionStringAsync()
        {
            var password = await GetDatabasePasswordAsync();
            var server = await GetSecretAsync("DatabaseServer");
            var database = await GetSecretAsync("DatabaseName");
            var username = await GetSecretAsync("DatabaseUser");

            // ✅ Build connection string from individual secrets
            return $"Server={server};Database={database};User Id={username};Password={password};";
        }

        private async Task<string> GetSecretAsync(string secretName)
        {
            KeyVaultSecret secret = await _secretClient.GetSecretAsync(secretName);
            return secret.Value;
        }
    }

    /// <summary>
    /// T1552 Defense: Configuration setup showing secure sources
    /// </summary>
    public class SecureConfigurationSetup
    {
        public static IConfiguration BuildSecureConfiguration()
        {
            var environment = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production";
            
            var builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                
                // ✅ Base configuration (non-sensitive settings)
                .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                .AddJsonFile($"appsettings.{environment}.json", optional: true, reloadOnChange: true);

            if (environment == "Development")
            {
                // ✅ User Secrets (stored in user profile, not in project)
                // Initialized with: dotnet user-secrets init
                // Set with: dotnet user-secrets set "ConnectionStrings:DefaultConnection" "value"
                builder.AddUserSecrets<SecureConfigurationSetup>();
            }

            // ✅ Environment Variables (set in hosting environment)
            // Azure App Service, Kubernetes Secrets, Docker, etc.
            builder.AddEnvironmentVariables();

            if (environment == "Production")
            {
                // ✅ Azure Key Vault (for production secrets)
                var config = builder.Build();
                var keyVaultUrl = config["KeyVault:Url"];
                
                if (!string.IsNullOrEmpty(keyVaultUrl))
                {
                    builder.AddAzureKeyVault(
                        new Uri(keyVaultUrl),
                        new DefaultAzureCredential());
                }
            }

            return builder.Build();
        }
    }

    /// <summary>
    /// T1552 Defense: Safe error handling and logging
    /// </summary>
    public class SecureErrorHandling
    {
        private readonly ILogger<SecureErrorHandling> _logger;

        public SecureErrorHandling(ILogger<SecureErrorHandling> logger)
        {
            _logger = logger;
        }

        public async Task<bool> AuthenticateUserAsync(string username, string password)
        {
            try
            {
                // Authentication logic...
                return true;
            }
            catch (Exception ex)
            {
                // ✅ SECURE: Log error without exposing credentials
                _logger.LogError(ex, 
                    "[T1552] Authentication failed for user {Username}", 
                    username);
                
                // ❌ NEVER DO THIS:
                // _logger.LogError($"Auth failed: {username}/{password}");
                
                return false;
            }
        }

        public void LogConnectionAttempt(string connectionString)
        {
            // ✅ Extract non-sensitive parts only
            var builder = new System.Data.SqlClient.SqlConnectionStringBuilder(connectionString);
            
            _logger.LogInformation(
                "[T1552] Connecting to {Server}/{Database} as {User}",
                builder.DataSource,
                builder.InitialCatalog,
                builder.UserID);
            
            // ❌ NEVER log the full connection string:
            // _logger.LogInformation($"Connection string: {connectionString}");
        }

        public string SanitizeForLogging(string sensitiveData)
        {
            // ✅ Show only last 4 characters
            if (sensitiveData.Length <= 4)
                return "****";
                
            return $"****{sensitiveData.Substring(sensitiveData.Length - 4)}";
        }
    }

    /// <summary>
    /// T1552 Defense: Secrets rotation and lifecycle management
    /// </summary>
    public class SecureSecretsRotation
    {
        private readonly SecretClient _keyVaultClient;
        private readonly ILogger<SecureSecretsRotation> _logger;

        public SecureSecretsRotation(
            SecretClient keyVaultClient,
            ILogger<SecureSecretsRotation> logger)
        {
            _keyVaultClient = keyVaultClient;
            _logger = logger;
        }

        /// <summary>
        /// T1552 Defense: Implement automated secrets rotation
        /// </summary>
        public async Task RotateApiKeyAsync(string secretName)
        {
            // 1. Generate new API key
            var newApiKey = GenerateSecureApiKey();

            // 2. Store new key in Key Vault
            await _keyVaultClient.SetSecretAsync(secretName, newApiKey);

            // 3. Update external service with new key
            // (Implementation depends on specific service)

            // 4. Wait for propagation period
            await Task.Delay(TimeSpan.FromMinutes(5));

            // 5. Revoke old key from external service

            _logger.LogInformation(
                "[T1552] Rotated secret {SecretName} successfully",
                secretName);
        }

        /// <summary>
        /// Check for secrets that need rotation
        /// </summary>
        public async Task<List<string>> CheckSecretsExpirationAsync()
        {
            var expiringSecrets = new List<string>();
            
            await foreach (var secretProperties in _keyVaultClient.GetPropertiesOfSecretsAsync())
            {
                if (secretProperties.ExpiresOn.HasValue &&
                    secretProperties.ExpiresOn.Value < DateTimeOffset.UtcNow.AddDays(30))
                {
                    expiringSecrets.Add(secretProperties.Name);
                    
                    _logger.LogWarning(
                        "[T1552] Secret {SecretName} expires on {ExpiresOn}",
                        secretProperties.Name,
                        secretProperties.ExpiresOn);
                }
            }

            return expiringSecrets;
        }

        private string GenerateSecureApiKey()
        {
            var bytes = new byte[32];
            using var rng = System.Security.Cryptography.RandomNumberGenerator.Create();
            rng.GetBytes(bytes);
            return Convert.ToBase64String(bytes);
        }
    }

    #endregion

    #region Configuration Examples

    /// <summary>
    /// Example: appsettings.json (safe - no secrets)
    /// </summary>
    public class ExampleAppSettings
    {
        /*
        {
          "Logging": {
            "LogLevel": {
              "Default": "Information"
            }
          },
          "KeyVault": {
            "Url": "https://myapp-keyvault.vault.azure.net/"
          },
          "ExternalApis": {
            "BaseUrl": "https://api.stripe.com"
          },
          "Database": {
            "MaxRetries": 3,
            "CommandTimeout": 30
          }
        }
        
        ✅ Notice: No secrets here! All sensitive values come from:
        - User Secrets (development)
        - Environment Variables (staging/production)
        - Azure Key Vault (production)
        */
    }

    /// <summary>
    /// Example: User Secrets (development only)
    /// Stored in: %APPDATA%\Microsoft\UserSecrets\{id}\secrets.json (Windows)
    /// or ~/.microsoft/usersecrets/{id}/secrets.json (Linux/Mac)
    /// </summary>
    public class ExampleUserSecrets
    {
        /*
        Initialize: dotnet user-secrets init
        Set secret: dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=localhost;..."
        
        {
          "ConnectionStrings": {
            "DefaultConnection": "Server=localhost;Database=DevDB;Integrated Security=true;"
          },
          "ApiKeys": {
            "Stripe": "sk_test_51234567890",
            "SendGrid": "SG.test1234567890"
          }
        }
        
        ✅ User Secrets are:
        - Stored outside the project directory
        - Never committed to source control
        - Only for local development
        - Not encrypted (so use dev/test keys only)
        */
    }

    /// <summary>
    /// Example: Environment Variables (production)
    /// </summary>
    public class ExampleEnvironmentVariables
    {
        /*
        # Linux/Mac
        export ConnectionStrings__DefaultConnection="Server=prod-db;..."
        export ApiKeys__Stripe="sk_live_51234567890"
        
        # Windows PowerShell
        $env:ConnectionStrings__DefaultConnection="Server=prod-db;..."
        $env:ApiKeys__Stripe="sk_live_51234567890"
        
        # Docker Compose
        environment:
          - ConnectionStrings__DefaultConnection=Server=prod-db;...
          - ApiKeys__Stripe=sk_live_51234567890
        
        # Kubernetes Secret
        apiVersion: v1
        kind: Secret
        metadata:
          name: app-secrets
        type: Opaque
        stringData:
          ConnectionStrings__DefaultConnection: "Server=prod-db;..."
          ApiKeys__Stripe: "sk_live_51234567890"
        
        ✅ Environment variables:
        - Set by hosting environment
        - Not in source code
        - Can be encrypted at rest (Kubernetes, Azure App Service)
        - Accessible via IConfiguration
        */
    }

    #endregion
}

/// <summary>
/// Key Takeaways for T1552 Defense (Unsecured Credentials):
/// 
/// ❌ NEVER:
/// 1. Hardcode secrets in source code
/// 2. Commit secrets to version control (even in config files)
/// 3. Log secrets or include them in error messages
/// 4. Store secrets in plain text files in the project
/// 5. Use weak or placeholder secrets in production
/// 
/// ✅ ALWAYS:
/// 1. Use IConfiguration with secure providers
/// 2. Use User Secrets for local development
/// 3. Use Environment Variables or Key Vault for production
/// 4. Use Options Pattern for type-safe configuration
/// 5. Validate configuration on startup
/// 6. Implement secrets rotation policies
/// 7. Use Managed Identity/DefaultAzureCredential (no credentials in code)
/// 8. Sanitize logs to remove sensitive data
/// 9. Set appropriate expiration dates on secrets
/// 10. Audit secret access and usage
/// 
/// Configuration Priority (ASP.NET Core):
/// 1. appsettings.json (non-sensitive)
/// 2. appsettings.{Environment}.json (non-sensitive)
/// 3. User Secrets (development)
/// 4. Environment Variables (all environments)
/// 5. Azure Key Vault (production)
/// 6. Command-line arguments (if needed)
/// 
/// Tools for Secret Detection:
/// - git-secrets
/// - TruffleHog
/// - GitHub Secret Scanning
/// - Azure DevOps Credential Scanner
/// - GitGuardian
/// 
/// References:
/// - MITRE ATT&CK T1552: https://attack.mitre.org/techniques/T1552/
/// - Safe storage of app secrets in development: https://docs.microsoft.com/aspnet/core/security/app-secrets
/// - Azure Key Vault: https://docs.microsoft.com/azure/key-vault/
/// - OWASP: Password Storage Cheat Sheet
/// </summary>
