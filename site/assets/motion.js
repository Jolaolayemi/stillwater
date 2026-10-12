/* Stillwater motion layer v2 — enhancement only (GSAP 3.15 + ScrollTrigger + SplitText, self-hosted).
   Every element is fully visible without this file. It does nothing with ?figma=1 (clean import)
   or when the visitor prefers reduced motion. Hover effects run on mouse/trackpad devices only. */
(function(){
  var q = new URLSearchParams(location.search);
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (q.has('figma') || q.has('static')) { root.classList.add('static'); return; }
  if (reduce) return;
  var fine = window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches;

  // 1. Letter roll (Visuvate-style). Each letter becomes a clipped column of two copies that slides up
  //    one row on hover: 520ms, cubic-bezier(.22,.61,.36,1), 18ms stagger, same order on the way back.
  //    Screen readers get the label once (sr-only copy); the rolling copy is aria-hidden.
  if (fine) document.querySelectorAll('[data-roll]').forEach(function(el){
    if (el.querySelector('.roll')) return;
    var label = el.querySelector('.lbl-roll') || el;
    var text = (label.textContent || '').replace(/\s+/g, ' ').trim();
    if (!text) return;
    var sr = document.createElement('span'); sr.className = 'sr-only'; sr.textContent = text;
    var roll = document.createElement('span'); roll.className = 'roll'; roll.setAttribute('aria-hidden', 'true');
    Array.from(text).forEach(function(ch, i){
      var c = document.createElement('span'); c.className = 'roll-c'; c.style.setProperty('--i', Math.min(i, 24));
      var a = document.createElement('span'), b = document.createElement('span');
      a.textContent = b.textContent = ch; c.appendChild(a); c.appendChild(b); roll.appendChild(c);
    });
    if (label === el) {
      // nav links: keep any icon, replace only the text nodes
      Array.from(el.childNodes).forEach(function(n){ if (n.nodeType === 3) el.removeChild(n); });
      el.appendChild(sr); el.appendChild(roll);
    } else { label.textContent = ''; label.appendChild(sr); label.appendChild(roll); }
  });

  // 3. Marquee: clone the track once so it can loop seamlessly.
  document.querySelectorAll('.strip-track').forEach(function(t){
    Array.from(t.children).forEach(function(c){ var d = c.cloneNode(true); d.setAttribute('aria-hidden','true'); t.appendChild(d); });
  });

  root.classList.add('m');

  // 6. Card glow (Visuvate-style): a radial highlight on the card's hairline border plus a soft inner light,
  //    both following the cursor. Mouse only; one delegated listener, updated once per frame.
  if (fine) {
    var cards = document.querySelectorAll('[data-glow]');
    cards.forEach(function(c){
      c.classList.add('has-glow');
      var f = document.createElement('span'); f.className = 'gl-fill'; f.setAttribute('aria-hidden','true');
      var g = document.createElement('span'); g.className = 'gl-ring'; g.setAttribute('aria-hidden','true');
      c.appendChild(f); c.appendChild(g);
    });
    if (cards.length) {
      var cur = null, px = 0, py = 0, pend = false;
      var paint = function(){
        pend = false;
        if (!cur) return;
        var r = cur.getBoundingClientRect();
        if (!r) return;
        cur.style.setProperty('--gx', (px - r.left).toFixed(1) + 'px');
        cur.style.setProperty('--gy', (py - r.top).toFixed(1) + 'px');
      };
      document.addEventListener('pointermove', function(e){
        if (e.pointerType && e.pointerType !== 'mouse') return;
        var t = e.target && e.target.closest ? e.target.closest('.has-glow') : null;
        if (t !== cur) { if (cur) cur.classList.remove('glow-on'); cur = t; if (cur) cur.classList.add('glow-on'); }
        px = e.clientX; py = e.clientY;
        if (cur && !pend) { pend = true; requestAnimationFrame(paint); }
      }, { passive: true });
      document.addEventListener('pointerleave', function(){ if (cur) cur.classList.remove('glow-on'); cur = null; });
    }
  }

  // 7. Calm water background: a tiny canvas of slow drifting cool light with faint ripple rings.
  //    Drawn at half resolution, capped at 30fps, paused when offscreen or when the tab is hidden.
  document.querySelectorAll('[data-water]').forEach(function(host){
    var cv = document.createElement('canvas');
    cv.className = 'water'; cv.setAttribute('aria-hidden', 'true');
    var before = host.querySelector('.fade');
    if (before) host.insertBefore(cv, before); else host.appendChild(cv);
    var ctx = cv.getContext && cv.getContext('2d');
    if (!ctx) return;
    var kind = host.getAttribute('data-water') || 'page';
    var S = 0.5, W = 0, H = 0, visible = true, raf = 0, last = 0, t0 = performance.now();
    var blobs = [
      { c: [28, 74, 168], a: .30, x: .22, y: .18, ax: .10, ay: .06, p: 61, r: .62 },
      { c: [24, 118, 140], a: .16, x: .78, y: .30, ax: .09, ay: .08, p: 73, r: .52 },
      { c: [80, 104, 190], a: .14, x: .50, y: .62, ax: .14, ay: .05, p: 89, r: .58 },
      { c: [255, 99, 99], a: .06, x: .64, y: .12, ax: .12, ay: .06, p: 67, r: .34 }
    ];
    if (kind === 'hero') blobs.forEach(function(b){ b.a *= .7; });
    var srcs = [{ x: .30, y: .58, ph: 0 }, { x: .74, y: .44, ph: .5 }];
    var size = function(){
      var r = host.getBoundingClientRect();
      if (!r) return;
      W = Math.max(1, Math.round(r.width * S)); H = Math.max(1, Math.round(r.height * S));
      cv.width = W; cv.height = H;
    };
    var draw = function(now){
      var t = (now - t0) / 1000;
      ctx.clearRect(0, 0, W, H);
      ctx.globalCompositeOperation = 'lighter';
      var m = Math.max(W, H);
      blobs.forEach(function(b, i){
        var x = W * (b.x + b.ax * Math.sin(t * 2 * Math.PI / b.p + i * 1.7));
        var y = H * (b.y + b.ay * Math.cos(t * 2 * Math.PI / (b.p * 1.3) + i));
        var rad = m * b.r;
        var g = ctx.createRadialGradient(x, y, 0, x, y, rad);
        g.addColorStop(0, 'rgba(' + b.c + ',' + b.a + ')');
        g.addColorStop(1, 'rgba(' + b.c + ',0)');
        ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      });
      ctx.globalCompositeOperation = 'source-over';
      ctx.lineWidth = 0.8;
      srcs.forEach(function(s){
        for (var k = 0; k < 5; k++) {
          var ph = ((t / 11) + s.ph + k / 5) % 1;
          var rx = ph * W * 0.55, ry = rx * 0.3;
          var al = 0.07 * (1 - ph) * Math.min(1, ph * 5);
          if (al <= 0.002) continue;
          ctx.strokeStyle = 'rgba(190,210,255,' + al.toFixed(3) + ')';
          ctx.beginPath(); ctx.ellipse(W * s.x, H * s.y, rx, ry, 0, 0, Math.PI * 2); ctx.stroke();
        }
      });
    };
    var loop = function(now){
      raf = 0;
      if (!visible || document.hidden) return;
      if (now - last >= 33) { last = now; draw(now); }
      raf = requestAnimationFrame(loop);
    };
    var start = function(){ if (!raf && visible && !document.hidden) raf = requestAnimationFrame(loop); };
    size(); draw(performance.now()); cv.classList.add('on');
    var sec = host.closest('section') || host;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function(es){
        es.forEach(function(e){ visible = e.isIntersecting; sec.classList.toggle('paused', !visible); if (visible) start(); });
      }).observe(host);
    }
    document.addEventListener('visibilitychange', start);
    var rt = 0; addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(function(){ size(); draw(performance.now()); }, 150); });
    start();
  });

  // 8. Resend timer on the verify screen (the static text already reads 0:42).
  document.querySelectorAll('[data-countdown]').forEach(function(el){
    var s = parseInt(el.getAttribute('data-countdown'), 10) || 0;
    var iv = setInterval(function(){
      s = Math.max(0, s - 1);
      el.textContent = Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
      if (!s) clearInterval(iv);
    }, 1000);
  });

  // ---------------------------------------------------------------------------------------------
  // GSAP layer (self-hosted gsap 3.15 + ScrollTrigger + SplitText). Built with gsap.matchMedia so
  // everything reverts if the visitor switches to reduced motion. Nothing in the markup starts hidden.
  // ---------------------------------------------------------------------------------------------
  var G = window.gsap, ST = window.ScrollTrigger, SPL = window.SplitText;
  if (!G || !ST) return;
  G.registerPlugin(ST); if (SPL) G.registerPlugin(SPL);
  root.classList.add('gs-pre');
  var unhide = function(){ root.classList.remove('gs-pre'); };
  setTimeout(unhide, 2500);   // safety net: never leave the hero hidden

  var init = function(){
    var mm = G.matchMedia();
    mm.add({ ok: '(prefers-reduced-motion: no-preference)', desk: '(min-width: 981px)' }, function(ctx){
      if (!ctx.conditions.ok) { unhide(); return; }
      var desk = ctx.conditions.desk;
      var hero = document.querySelector('.hero');

      // A. Headings: masked line reveal (SplitText lines + mask), on load in the hero, on scroll elsewhere.
      document.querySelectorAll('[data-reveal]').forEach(function(el){
        var inHero = !!(hero && hero.contains(el)) || !!el.closest('.idx');
        var trig = inHero ? null : { trigger: el, start: 'top 88%', once: true };
        if (!SPL) { G.from(el, { autoAlpha: 0, y: 24, duration: .9, ease: 'power3.out', scrollTrigger: trig }); return; }
        SPL.create(el, { type: 'lines', mask: 'lines', autoSplit: true, linesClass: 'sw-line',
          onSplit: function(self){ return G.from(self.lines, { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: .09, delay: inHero ? .12 : 0, scrollTrigger: trig }); } });
      });

      // B. Appear: fade + rise + de-blur, batched so neighbours stagger together (Profound-style 0.6-0.9s ease-out).
      var appear = Array.from(document.querySelectorAll('[data-appear]'));
      var heroAppear = appear.filter(function(e){ return hero && hero.contains(e) && !e.closest('.principles'); });
      var rest = appear.filter(function(e){ return heroAppear.indexOf(e) < 0; });
      G.set(appear, { autoAlpha: 0, y: 24, filter: 'blur(6px)' });
      if (heroAppear.length) G.to(heroAppear, { autoAlpha: 1, y: 0, filter: 'blur(0px)', duration: .9, ease: 'power3.out', stagger: .1, delay: .3, clearProps: 'filter' });
      ST.batch(rest, { start: 'top 92%', once: true,
        onEnter: function(b){ G.to(b, { autoAlpha: 1, y: 0, filter: 'blur(0px)', duration: .85, ease: 'power3.out', stagger: .09, overwrite: true, clearProps: 'filter' }); } });

      // C. Hero app window: rises in, then flattens from a tilt as you scroll (scrubbed), and its UI staggers in.
      var shot = document.querySelector('.hero-shot'), win = shot && shot.querySelector('.window');
      if (win) {
        G.from(shot, { y: 60, autoAlpha: 0, duration: 1.2, ease: 'expo.out', delay: .55 });
        G.fromTo(win, { rotationX: 16, scale: .92, opacity: .6, transformOrigin: '50% 0%' },
          { rotationX: 0, scale: 1, opacity: 1, ease: 'none', scrollTrigger: { trigger: shot, start: 'top 88%', end: 'top 22%', scrub: 1 } });
        var bits = win.querySelectorAll('.swap .field, .swap .drow, .swap .btn, .plain, .stepper .st');
        if (bits.length) G.from(bits, { y: 14, autoAlpha: 0, duration: .7, ease: 'power3.out', stagger: .045, delay: .9 });
      }
      unhide();

      // D. Statement: words brighten as you scroll through it (scrubbed).
      var stmt = document.querySelector('[data-scrub-words]');
      if (stmt && SPL) {
        var sw = SPL.create(stmt, { type: 'words' });
        G.fromTo(sw.words, { opacity: .16 }, { opacity: 1, ease: 'none', stagger: .12,
          scrollTrigger: { trigger: stmt, start: 'top 82%', end: 'bottom 42%', scrub: .6 } });
      }

      // E. How it works: a hairline fills across the three steps as you scroll.
      var line = document.querySelector('.steps-line i');
      if (line) G.fromTo(line, { scaleX: 0 }, { scaleX: 1, ease: 'none', scrollTrigger: { trigger: '.steps-wrap', start: 'top 82%', end: 'bottom 62%', scrub: .6 } });

      // F. Number tickers (APR, stats, totals): count up once in view, then settle on the exact text.
      document.querySelectorAll('[data-ticker]').forEach(function(el){
        var txt = el.textContent, m = txt.match(/^(\D*?)(\d[\d,]*(?:\.\d+)?)([\s\S]*)$/);
        if (!m) return;
        var pre = m[1], num = m[2], suf = m[3], dec = (num.split('.')[1] || '').length, comma = num.indexOf(',') > -1;
        var target = parseFloat(num.replace(/,/g, '')); if (!isFinite(target)) return;
        var fmt = function(v){ var s = v.toFixed(dec); if (comma) { var p = s.split('.'); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); s = p.join('.'); } return pre + s + suf; };
        var r = el.getBoundingClientRect();
        if (r && getComputedStyle(el).display === 'inline') el.style.display = 'inline-block';
        if (r) el.style.minWidth = Math.ceil(r.width) + 'px';
        var o = { v: 0 };
        G.to(o, { v: target, duration: 1.4, ease: 'power2.out',
          scrollTrigger: { trigger: el, start: 'top 94%', once: true },
          onStart: function(){ el.textContent = fmt(0); },
          onUpdate: function(){ el.textContent = fmt(o.v); },
          onComplete: function(){ el.textContent = txt; } });
      });

      // G. Magnetic primary buttons (mouse, desktop): a small pull toward the cursor, springing back on leave.
      if (fine && desk) document.querySelectorAll('.hero .btn-primary.btn-lg, .cta-band .btn-primary, .site-nav .btn-primary').forEach(function(b){
        var xT = G.quickTo(b, 'x', { duration: .5, ease: 'power3' }), yT = G.quickTo(b, 'y', { duration: .5, ease: 'power3' });
        b.addEventListener('pointermove', function(e){ var r = b.getBoundingClientRect(); if (!r) return; xT((e.clientX - r.left - r.width / 2) * .16); yT((e.clientY - r.top - r.height / 2) * .22); });
        b.addEventListener('pointerleave', function(){ G.to(b, { x: 0, y: 0, duration: .8, ease: 'elastic.out(1,.6)', overwrite: true }); });
      });

      // H. Segmented controls: an indicator pill slides to the chosen option.
      document.querySelectorAll('.seg').forEach(function(seg){
        var items = Array.from(seg.children).filter(function(c){ return c.nodeType === 1; });
        if (items.length < 2) return;
        var on = seg.querySelector(':scope > .on') || items[0];
        var ind = document.createElement('span'); ind.className = 'seg-ind'; ind.setAttribute('aria-hidden', 'true');
        seg.appendChild(ind); seg.classList.add('has-ind');
        var place = function(el, t){ G.to(ind, { x: el.offsetLeft, width: el.offsetWidth, duration: t, ease: 'power3.out', overwrite: true }); };
        place(on, 0);
        items.forEach(function(it){ it.addEventListener('click', function(){
          items.forEach(function(x){ x.classList.remove('on'); }); it.classList.add('on');
          var inp = it.querySelector('input'); if (inp) inp.checked = true;
          place(it, .45);
        }); });
        addEventListener('resize', function(){ var cur = seg.querySelector(':scope > .on') || items[0]; place(cur, 0); });
      });

      // I. Copy wallet address: a tick pops in, "Copied", then it settles back.
      document.querySelectorAll('button.wallet[data-copy]').forEach(function(b){
        var addr = b.querySelector('.addr'), tick = b.querySelector('.tick'), orig = addr ? addr.textContent : '', tm = 0;
        b.addEventListener('click', function(){
          try { if (navigator.clipboard) navigator.clipboard.writeText(b.getAttribute('data-copy')).catch(function(){}); } catch (e) {}
          b.classList.add('copied'); if (addr) addr.textContent = 'Copied';
          if (tick) G.fromTo(tick, { scale: .3, rotation: -25, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: .45, ease: 'back.out(2.2)' });
          clearTimeout(tm); tm = setTimeout(function(){ b.classList.remove('copied'); if (addr) addr.textContent = orig; }, 1600);
        });
      });

      // J. Success: the check ring pops and the tick draws on left to right.
      document.querySelectorAll('[data-draw]').forEach(function(el){
        var svg = el.querySelector('svg');
        var tl = G.timeline({ delay: .2 });
        tl.from(el, { scale: .55, autoAlpha: 0, duration: .6, ease: 'back.out(1.8)' });
        if (svg) tl.fromTo(svg, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: .5, ease: 'power2.out' }, '-=.25');
      });

      // K. Portfolio chart: the line draws itself in, the fill fades up after it.
      document.querySelectorAll('.chart svg').forEach(function(svg){
        var ps = svg.querySelectorAll('path'); if (!ps.length) return;
        ps.forEach(function(p){
          if (p.getAttribute('stroke') && p.getAttribute('stroke') !== 'none' && p.getTotalLength) {
            var L = p.getTotalLength(); G.fromTo(p, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: 1.6, ease: 'power2.inOut', scrollTrigger: { trigger: svg, start: 'top 90%', once: true } });
          } else G.from(p, { opacity: 0, duration: 1, delay: .9, ease: 'power1.out', scrollTrigger: { trigger: svg, start: 'top 90%', once: true } });
        });
      });

      // L. FAQ: answers open and close with a smooth height change instead of a jump.
      document.querySelectorAll('.faq details').forEach(function(d){
        var sum = d.querySelector('summary'), body = d.querySelector('p');
        if (!sum || !body) return;
        d.classList.add('anim');
        sum.addEventListener('click', function(e){
          e.preventDefault();
          if (d.open) G.to(body, { height: 0, opacity: 0, duration: .35, ease: 'power2.inOut', onComplete: function(){ d.open = false; G.set(body, { clearProps: 'height,opacity' }); } });
          else { d.open = true; G.from(body, { height: 0, opacity: 0, duration: .45, ease: 'power3.out', clearProps: 'height,opacity' }); }
        });
      });

      ST.refresh();
    });
  };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(init, init); else init();
})();
