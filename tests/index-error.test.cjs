const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const html = fs.readFileSync('index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script, 'index script must exist');

async function loadWithFailure(protocol) {
  const elements = {
    cardContainer: { innerHTML: '' },
    '.header .emoji': { textContent: '' },
    '.header .title-text': { textContent: '' },
    '.header .sub': { textContent: '' },
    '.footer': { innerHTML: '' }
  };
  const document = {
    getElementById: key => elements[key],
    querySelector: key => elements[key]
  };
  vm.runInNewContext(script, {
    document,
    location: { protocol },
    fetch: () => Promise.reject(new Error('network unavailable'))
  });
  await new Promise(resolve => setImmediate(resolve));
  return elements.cardContainer.innerHTML;
}

test('file URL failure explains local server recovery', async () => {
  const message = await loadWithFailure('file:');
  assert.match(message, /python3 -m http\.server 8000/);
  assert.match(message, /http:\/\/localhost:8000\//);
});

test('HTTP failure retains network error and retry advice', async () => {
  const message = await loadWithFailure('http:');
  assert.match(message, /network unavailable/);
  assert.match(message, /请刷新页面重试/);
  assert.doesNotMatch(message, /python3 -m http\.server/);
});
