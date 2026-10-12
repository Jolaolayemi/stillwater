// Checks the final static files: run with `node --test test/`
const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const SITE = path.join(__dirname, '..', 'site');
const AUTH = ['app/signup/index.html','app/signup-verify/index.html','app/signup-passkey/index.html','app/signup-preferences/index.html','app/signup-welcome/index.html','app/login/index.html'];
const PAGES = ['index.html','landing/index.html',...AUTH,'app/swap/index.html','app/swap-token-select/index.html','app/swap-settings/index.html',
  'app/swap-review/index.html','app/success/index.html','app/stake/index.html','app/portfolio/index.html','app/connect/index.html'];
const read = p => fs.readFileSync(path.join(SITE, p), 'utf8');

test('every screen exists with title, viewport, demo tag and no "concept" labelling', () => {
  for (const p of PAGES) {
    const h = read(p);
    assert.match(h, /<title>[^<]*Stillwater[^<]*<\/title>/, p + ' title');
    assert.match(h, /name="viewport" content="width=device-width, initial-scale=1"/, p + ' viewport');
    assert.match(h, /Demo build · Designed by Olayemi/, p + ' demo tag');
    assert.doesNotMatch(h, /concept/i, p + ' concept label');
    assert.match(h, /<svg class="mark"/, p + ' logo mark inlined from assets/mark.svg');
    assert.doesNotMatch(h, /lorem|TODO|\{\{|undefined|NaN/i, p + ' placeholder');
  }
});

test('all local asset references resolve and nothing is remote', () => {
  for (const p of PAGES) {
    const h = read(p);
    for (const m of h.matchAll(/(?:src|href)="(\/[^"#?]*)"/g)) {
      let ref = m[1]; if (ref.endsWith('/')) ref += 'index.html';
      assert.ok(fs.existsSync(path.join(SITE, ref)), p + ' -> ' + m[1]);
    }
    assert.doesNotMatch(h, /(?:src|href)="https?:\/\//, p + ' remote asset');
  }
  const css = fs.readFileSync(path.join(SITE, 'assets/styles.css'), 'utf8');
  for (const m of css.matchAll(/url\("(\/[^"]+)"\)/g)) assert.ok(fs.existsSync(path.join(SITE, m[1])), m[1]);
});

test('landing carries the requested sections and the footer note', () => {
  const h = read('landing/index.html');
  for (const id of ['how','swap','stake','security','faq']) assert.match(h, new RegExp('id="' + id + '"'), id);
  assert.match(h, /Example APR/);
  assert.match(h, /href="\/app\/signup\/"[^>]*><span class="lbl-roll">Get started</);
});

test('content does not depend on JS: no element starts hidden in markup', () => {
  for (const p of PAGES) assert.doesNotMatch(read(p), /style="[^"]*(?:opacity:\s*0|display:\s*none|visibility:\s*hidden)/, p);
  const js = fs.readFileSync(path.join(SITE, 'assets/motion.js'), 'utf8');
  assert.match(js, /prefers-reduced-motion/);
  assert.match(js, /figma/);
});

test('swap review states the key numbers', () => {
  const h = read('app/swap-review/index.html');
  for (const s of ['You receive at least','0.0738 EDDY','Price impact','₦ 570','Step 1 of 2','Nothing else']) assert.ok(h.includes(s), s);
});

test('sign-up flow and login carry their key parts', () => {
  const need = {
    'app/signup/index.html': ['type="email"', 'Continue with Google', 'Continue with Apple', 'Already have a wallet?', 'Connect wallet', 'Terms', 'Privacy'],
    'app/signup-verify/index.html': ['Digit 6 of 6', 'Resend code in', 'Change email'],
    'app/signup-passkey/index.html': ['Create passkey', 'Use a seed phrase instead'],
    'app/signup-preferences/index.html': ['US dollar', 'Naira', 'Some experience', 'Risk comfort'],
    'app/signup-welcome/index.html': ['Fund your wallet', 'Illustrative', 'Start swapping'],
    'app/login/index.html': ['Log in with passkey', 'Continue with Google', 'Create account'],
  };
  for (const [p, list] of Object.entries(need)) { const h = read(p); for (const s of list) assert.ok(h.includes(s), p + ': ' + s); }
  const idx = read('index.html');
  for (const p of AUTH) { const u = '/' + p.replace('index.html', ''); assert.ok(idx.includes('href="' + u + '?figma=1"'), 'index figma link ' + u); }
});

test('motion layer: roll, glow and water are mouse/reduced-motion/figma aware', () => {
  const js = fs.readFileSync(path.join(SITE, 'assets/motion.js'), 'utf8');
  for (const s of ['pointer:fine', 'aria-hidden', 'sr-only', 'data-glow', 'data-water', 'IntersectionObserver', 'visibilitychange']) assert.ok(js.includes(s), s);
  const css = fs.readFileSync(path.join(SITE, 'assets/styles.css'), 'utf8');
  assert.match(css, /--roll-dur:520ms/); assert.match(css, /cubic-bezier\(\.22,\.61,\.36,1\)/);
  assert.match(fs.readFileSync(path.join(SITE, 'assets/mark.svg'), 'utf8'), /<svg[^>]*viewBox/);
});

test('GSAP is self-hosted and gated by matchMedia; icons are Line Awesome files', () => {
  for (const f of ['gsap.min.js', 'ScrollTrigger.min.js', 'SplitText.min.js']) assert.ok(fs.existsSync(path.join(SITE, 'assets/vendor', f)), f);
  const js = fs.readFileSync(path.join(SITE, 'assets/motion.js'), 'utf8');
  for (const s of ['matchMedia', 'prefers-reduced-motion: no-preference', 'ScrollTrigger', 'SplitText', 'data-ticker', 'quickTo']) assert.ok(js.includes(s), s);
  for (const p of PAGES) assert.match(read(p), /<script src="\/assets\/vendor\/gsap\.min\.js" defer><\/script>/, p);
  const icons = fs.readdirSync(path.join(SITE, 'assets/icons')).filter(f => f.endsWith('.svg'));
  assert.ok(icons.length >= 30, 'icon files');
  assert.ok(read('landing/index.html').includes('viewBox="0 0 32 32" fill="currentColor"'), 'Line Awesome icons inlined');
});
