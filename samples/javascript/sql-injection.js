/**
 * MITRE ATT&CK T1190: Exploit Public-Facing Application - SQL Injection
 * Educational demonstration of SQL injection vulnerability and defense
 * 
 * @description Shows vulnerable string concatenation vs secure parameterized queries
 * @reference https://attack.mitre.org/techniques/T1190/
 */

const http = require('http');
const url = require('url');

// =============================================================================
// VULNERABLE IMPLEMENTATION
// =============================================================================

/**
 * VULNERABLE: SQL Injection via string concatenation
 * ATT&CK T1190 - Exploit Public-Facing Application
 * 
 * @description This endpoint is vulnerable to SQL injection attacks
 * @example Malicious input: userId = "1 OR 1=1--"
 * @vulnerability Attacker can extract all users, drop tables, or read sensitive data
 */
class VulnerableUserAPI {
  constructor() {
    this.users = [
      { id: 1, username: 'admin', email: 'admin@example.com', role: 'admin' },
      { id: 2, username: 'user1', email: 'user1@example.com', role: 'user' },
      { id: 3, username: 'user2', email: 'user2@example.com', role: 'user' }
    ];
  }

  /**
   * VULNERABLE: String concatenation allows SQL injection
   * @param {string} userId - User input (UNTRUSTED)
   * @returns {object} Query result
   */
  getUserById(userId) {
    // VULNERABLE: Direct string concatenation
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    
    console.log('🔴 VULNERABLE Query:', query);
    
    // Simulated SQL execution (in real code, this would hit a database)
    // Attack example: userId = "1 OR 1=1--" would return all users
    if (userId.includes('OR 1=1')) {
      console.log('⚠️  SQL INJECTION DETECTED: Returning all users!');
      return this.users; // All users leaked!
    }
    
    // Normal case
    const user = this.users.find(u => u.id === parseInt(userId));
    return user || null;
  }

  /**
   * VULNERABLE: SQL injection in login query
   * @param {string} username - User input (UNTRUSTED)
   * @param {string} password - User input (UNTRUSTED)
   */
  authenticateUser(username, password) {
    // VULNERABLE: Allows authentication bypass
    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    
    console.log('🔴 VULNERABLE Query:', query);
    
    // Attack example: username = "admin'--" bypasses password check
    if (username.includes("'--")) {
      console.log('⚠️  SQL INJECTION: Authentication bypassed!');
      return this.users.find(u => u.username === username.replace("'--", ''));
    }
    
    return null;
  }
}

// =============================================================================
// DEFENDED IMPLEMENTATION
// =============================================================================

/**
 * SECURE: Parameterized queries prevent SQL injection
 * Defense against ATT&CK T1190
 * 
 * @description Uses parameterized queries and input validation
 * @security Prevents SQL injection through proper query construction
 */
class SecureUserAPI {
  constructor() {
    this.users = [
      { id: 1, username: 'admin', email: 'admin@example.com', role: 'admin' },
      { id: 2, username: 'user1', email: 'user1@example.com', role: 'user' },
      { id: 3, username: 'user2', email: 'user2@example.com', role: 'user' }
    ];
  }

  /**
   * SECURE: Input validation and parameterized query
   * @param {string} userId - User input (validated)
   * @returns {object|null} Query result
   */
  getUserById(userId) {
    // Defense 1: Input validation
    if (!this.isValidUserId(userId)) {
      console.log('🛡️  BLOCKED: Invalid user ID format');
      return null;
    }

    // Defense 2: Parameterized query (simulated)
    const params = { id: parseInt(userId) };
    const query = 'SELECT * FROM users WHERE id = ?';
    
    console.log('✅ SECURE Query:', query);
    console.log('✅ Parameters:', params);
    
    // Simulated parameterized execution
    const user = this.users.find(u => u.id === params.id);
    return user || null;
  }

  /**
   * SECURE: Parameterized authentication query
   * @param {string} username - User input (validated)
   * @param {string} password - User input (validated)
   */
  authenticateUser(username, password) {
    // Defense 1: Input validation
    if (!this.isValidUsername(username)) {
      console.log('🛡️  BLOCKED: Invalid username format');
      return null;
    }

    // Defense 2: Parameterized query (simulated)
    const params = { username, password };
    const query = 'SELECT * FROM users WHERE username = ? AND password = ?';
    
    console.log('✅ SECURE Query:', query);
    console.log('✅ Parameters:', { username, password: '[REDACTED]' });
    
    // In real implementation, password would be hashed
    return null; // Authentication logic would go here
  }

  /**
   * Validates user ID format
   * @param {string} userId - Input to validate
   * @returns {boolean} True if valid
   */
  isValidUserId(userId) {
    // Only allow numeric values
    return /^\d+$/.test(userId);
  }

  /**
   * Validates username format
   * @param {string} username - Input to validate
   * @returns {boolean} True if valid
   */
  isValidUsername(username) {
    // Alphanumeric and underscore only, 3-20 chars
    return /^[a-zA-Z0-9_]{3,20}$/.test(username);
  }
}

// =============================================================================
// EXPRESS.JS EXAMPLE
// =============================================================================

/**
 * Creates an Express-style request handler demonstrating both vulnerable and secure patterns
 * Note: This uses plain http module to avoid external dependencies
 */
function createDemoServer() {
  const vulnerableAPI = new VulnerableUserAPI();
  const secureAPI = new SecureUserAPI();

  const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;
    const query = parsedUrl.query;

    res.setHeader('Content-Type', 'application/json');

    // Vulnerable endpoint
    if (path === '/api/vulnerable/user' && query.id) {
      console.log('\n🔴 VULNERABLE ENDPOINT CALLED');
      const result = vulnerableAPI.getUserById(query.id);
      res.writeHead(200);
      res.end(JSON.stringify({ success: true, data: result }));
      return;
    }

    // Secure endpoint
    if (path === '/api/secure/user' && query.id) {
      console.log('\n✅ SECURE ENDPOINT CALLED');
      const result = secureAPI.getUserById(query.id);
      res.writeHead(200);
      res.end(JSON.stringify({ success: true, data: result }));
      return;
    }

    // Home page with examples
    if (path === '/') {
      res.setHeader('Content-Type', 'text/html');
      res.writeHead(200);
      res.end(`
        <h1>SQL Injection Demo - MITRE ATT&CK T1190</h1>
        <h2>Try these examples:</h2>
        <ul>
          <li><a href="/api/vulnerable/user?id=1">Vulnerable: Normal request (id=1)</a></li>
          <li><a href="/api/vulnerable/user?id=1 OR 1=1--">Vulnerable: SQL Injection (id=1 OR 1=1--)</a></li>
          <li><a href="/api/secure/user?id=1">Secure: Normal request (id=1)</a></li>
          <li><a href="/api/secure/user?id=1 OR 1=1--">Secure: Blocked injection attempt</a></li>
        </ul>
      `);
      return;
    }

    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not found' }));
  });

  return server;
}

// =============================================================================
// EXAMPLE USAGE
// =============================================================================

if (require.main === module) {
  console.log('='.repeat(80));
  console.log('MITRE ATT&CK T1190: SQL Injection Demo');
  console.log('='.repeat(80));

  console.log('\n--- VULNERABLE IMPLEMENTATION ---\n');
  
  const vulnerableAPI = new VulnerableUserAPI();
  
  // Normal query
  console.log('1. Normal query:');
  console.log('Result:', vulnerableAPI.getUserById('1'));
  
  // SQL Injection attack
  console.log('\n2. SQL Injection attack:');
  console.log('Result:', vulnerableAPI.getUserById('1 OR 1=1--'));
  
  // Authentication bypass
  console.log('\n3. Authentication bypass:');
  console.log('Result:', vulnerableAPI.authenticateUser("admin'--", 'anything'));

  console.log('\n--- SECURE IMPLEMENTATION ---\n');
  
  const secureAPI = new SecureUserAPI();
  
  // Normal query
  console.log('1. Normal query:');
  console.log('Result:', secureAPI.getUserById('1'));
  
  // Blocked SQL Injection
  console.log('\n2. Blocked SQL Injection attempt:');
  console.log('Result:', secureAPI.getUserById('1 OR 1=1--'));
  
  // Blocked authentication bypass
  console.log('\n3. Blocked authentication bypass:');
  console.log('Result:', secureAPI.authenticateUser("admin'--", 'anything'));

  console.log('\n--- STARTING WEB SERVER ---\n');
  
  const server = createDemoServer();
  const PORT = 3000;
  
  server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log('Press Ctrl+C to stop\n');
  });
}

module.exports = { VulnerableUserAPI, SecureUserAPI, createDemoServer };
