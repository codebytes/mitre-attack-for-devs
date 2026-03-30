const { describe, it } = require('node:test');
const assert = require('node:assert');

describe('smoke tests', () => {
  it('package.json is valid', () => {
    const pkg = require('../package.json');
    assert.ok(pkg.name);
    assert.ok(pkg.version);
  });
});
