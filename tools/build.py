#!/usr/bin/env python3
"""Stillwater demo site generator.
Writes static HTML pages into ../site from shared fragments. Run: python3 tools/build.py
All numbers, tokens and yields are fictional examples (demo data).
The logo mark lives in ONE file, site/assets/mark.svg; every page inlines it from there."""
import os, re, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')

# ---- icons: Line Awesome by Icons8, one SVG file per icon in site/assets/icons/ (only the ones used) ----
ICON_MAP = {'swap': 'exchange-alt-solid', 'stake': 'layer-group-solid', 'portfolio': 'chart-pie-solid', 'shield': 'shield-alt-solid', 'activity': 'history-solid', 'sliders': 'sliders-h-solid', 'chev': 'angle-down-solid', 'chevr': 'angle-right-solid', 'down': 'arrow-down-solid', 'right': 'arrow-right-solid', 'search': 'search-solid', 'x': 'times-solid', 'check': 'check-solid', 'info': 'info-circle-solid', 'alert': 'exclamation-triangle-solid', 'ext': 'external-link-alt-solid', 'copy': 'copy', 'plus': 'plus-solid', 'wallet': 'wallet-solid', 'qr': 'qrcode-solid', 'key': 'key-solid', 'lock': 'lock-solid', 'clock': 'clock', 'eye': 'eye', 'globe': 'globe-africa-solid', 'refresh': 'sync-alt-solid', 'gift': 'gift-solid', 'menu': 'bars-solid', 'bolt': 'bolt-solid', 'gear': 'cog-solid', 'faceid': 'fingerprint-solid', 'recv': 'arrow-down-solid', 'send': 'arrow-up-solid', 'bell': 'bell', 'back': 'angle-left-solid', 'del': 'backspace-solid', 'user': 'user', 'chip': 'microchip-solid', 'browser': 'window-maximize', 'google': 'google', 'apple': 'apple', 'envelope': 'envelope'}
_ICON_CACHE = {}
def ic(name, cls=''):
    """Inline a Line Awesome icon (fill = currentColor) so every page imports into Figma without external refs."""
    if name not in _ICON_CACHE:
        s = open(os.path.join(SITE, 'assets', 'icons', ICON_MAP[name] + '.svg')).read()
        _ICON_CACHE[name] = s[s.index('>') + 1:s.rindex('</svg>')].strip()
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 32 32" fill="currentColor" aria-hidden="true">{_ICON_CACHE[name]}</svg>'

def load_mark():
    """Read the single logo source (site/assets/mark.svg) and return it as an inline, decorative <svg>."""
    s = open(os.path.join(SITE, 'assets', 'mark.svg')).read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S).strip()
    s = s[s.index('<svg'):]
    s = re.sub(r'\s(?:xmlns|width|height|aria-hidden|aria-label|role|class)="[^"]*"', '', s[:s.index('>')]) + s[s.index('>'):]
    s = re.sub(r'<title>.*?</title>', '', s, flags=re.S)
    return s.replace('<svg', '<svg class="mark" aria-hidden="true"', 1)
MARK = load_mark()

def _mark_inner(x, y, size):
    """The mark placed as a nested <svg> box (white) inside a larger drawing."""
    m = MARK.replace(' class="mark" aria-hidden="true"', '', 1)
    return m.replace('<svg', f'<svg x="{x:.2f}" y="{y:.2f}" width="{size:.2f}" height="{size:.2f}" color="#ffffff"', 1)

def tile(px=None, kind='app', standalone=False):
    """App icon / favicon tile built from the ONE mark: dark rounded square, hairline edge, white mark.
    kind='app' uses the app-icon proportions (mark ~56% of the tile), kind='fav' the larger favicon proportions."""
    if kind == 'fav':
        V, rx, inner, sw = 32, 7.04, 22.41, 1.0
        body = (f'<rect width="32" height="32" rx="{rx}" fill="#0b0c0e"/>'
                f'<rect x="0.5" y="0.5" width="31" height="31" rx="6.54" fill="none" stroke="#ffffff" stroke-opacity="0.14"/>')
    else:
        V, rx, inner = 1024, 229.07, 573.4
        body = (f'<rect width="1024" height="1024" rx="{rx}" fill="#0b0c0e"/>'
                f'<rect x="1" y="1" width="1022" height="1022" rx="228.07" fill="none" stroke="#ffffff" stroke-opacity="0.1" stroke-width="2"/>'
                f'<path d="M229.1 3H794.9" stroke="#ffffff" stroke-opacity="0.16" stroke-width="2"/>')
    o = (V - inner) / 2
    attrs = f'viewBox="0 0 {V} {V}"' + (f' width="{px}" height="{px}"' if px else '')
    if standalone:
        return f'<svg xmlns="http://www.w3.org/2000/svg" {attrs}>{body}{_mark_inner(o, o, inner)}</svg>\n'
    return f'<svg class="app-icon" {attrs} aria-hidden="true">{body}{_mark_inner(o, o, inner)}</svg>'

def write_icons():
    """favicon.svg, app-icon.svg and their PNGs (favicon-32/16, apple-touch-icon 180, app-icon-1024), all from mark.svg."""
    import shutil, subprocess
    A = os.path.join(SITE, 'assets')
    open(os.path.join(A, 'favicon.svg'), 'w').write(tile(kind='fav', standalone=True))
    open(os.path.join(A, 'app-icon.svg'), 'w').write(tile(kind='app', standalone=True))
    rsvg = shutil.which('rsvg-convert')
    if not rsvg:
        print('warning: rsvg-convert not found; PNG icons not regenerated'); return
    for src, out, n in [('favicon.svg','favicon-32.png',32),('favicon.svg','favicon-16.png',16),
                        ('app-icon.svg','apple-touch-icon.png',180),('app-icon.svg','app-icon-1024.png',1024)]:
        subprocess.run([rsvg, '-w', str(n), '-h', str(n), '-o', os.path.join(A, out), os.path.join(A, src)], check=True)
DEMO_TAG = '<span class="tag-demo">Demo build · Designed by Olayemi</span>'
def brand(href='/'):
    return f'<a class="brand" href="{href}" aria-label="Stillwater home">{MARK}<span>Stillwater</span></a>'

# ---- fictional demo tokens ----
# Token badges: an honest letter monogram on a calm, desaturated tint (one hue per token) with a hairline
# border. No illustrative glyphs. ti(sym) is the ONE helper for every token badge on the site and in the
# mobile frames; ti('KELP/CMD') draws a pair badge (two overlapped discs, the second cut with a 1.5-unit gap).
import colorsys
TOK = {
 #  symbol: (name, letters, hue in degrees, optical x-nudge in viewBox units)
 'CMD':  ('Calm Dollar',        'C',  158, 0.30),
 'EDDY': ('Eddy',               'E',  212, 0.45),
 'sEDDY':('Staked Eddy',        'sE', 212, 0.15),
 'SHOL': ('Shoal',              'S',  262, 0.00),
 'KELP': ('Kelp',               'K',   78, 0.30),
 'MRSH': ('Marsh (unverified)', 'M',   34, 0.00),
}
def _hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
    return '#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255))
def tok_colors(sym):
    """(fill, hairline, letter) for a token: a whisper of hue on near-black, a slightly lifted hairline, pale tinted letters."""
    h = TOK[sym][2]
    return _hsl(h, .22, .13), _hsl(h, .18, .28), _hsl(h, .38, .83)
INTER_CAP = 0.727  # Inter cap height / em, used to centre capitals on the disc's middle (optical, not em-box)
def _disc(sym, cx, shape=None):
    _, letters, _, nudge = TOK[sym]
    fill, line, ink = tok_colors(sym)
    fs = 12.5 if len(letters) > 1 else 14
    y = 16 + INTER_CAP * fs / 2
    body = shape or f'<circle cx="{cx}" cy="16" r="15.5"'
    ls = ' letter-spacing="-0.4"' if len(letters) > 1 else ''
    return (f'{body} fill="{fill}" stroke="{line}" stroke-width="1" vector-effect="non-scaling-stroke"/>'
            f'<text x="{cx + nudge:g}" y="{y:.2f}" text-anchor="middle" fill="{ink}" font-family="Inter, system-ui, sans-serif" '
            f'font-weight="600" font-size="{fs:g}"{ls}>{letters}</text>')
def ti(sym):
    """Token badge. 'EDDY' -> one disc; 'KELP/CMD' -> pair badge. Always <svg class="ti ...">, sized by CSS."""
    if '/' in sym:
        a, b = sym.split('/')
        cb, gap = 40, 1.5                       # second disc centre, gap ring around the first
        R, Rc = 15.5, 15.5 + gap
        x = (Rc**2 - R**2 + cb**2 - 16**2) / (2 * (cb - 16))
        yy = math.sqrt(max(R**2 - (x - cb)**2, 0))
        crescent = (f'<path d="M{x:.3f} {16-yy:.3f}A{R} {R} 0 1 1 {x:.3f} {16+yy:.3f}'
                    f'A{Rc} {Rc} 0 0 0 {x:.3f} {16-yy:.3f}Z"')
        return (f'<svg class="ti pair" viewBox="0 0 56 32" aria-hidden="true">'
                f'{_disc(b, cb, crescent)}{_disc(a, 16)}</svg>')
    return f'<svg class="ti" viewBox="0 0 32 32" aria-hidden="true">{_disc(sym, 16)}</svg>'

ADDR = '0x7a3f…c91e'

def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="theme-color" content="#040506">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/Inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/styles.css">
</head>
"""
FOOTJS = ('<script src="/assets/vendor/gsap.min.js" defer></script>\n<script src="/assets/vendor/ScrollTrigger.min.js" defer></script>\n'
          '<script src="/assets/vendor/SplitText.min.js" defer></script>\n<script src="/assets/motion.js" defer></script>\n</body>\n</html>\n')

def write(path, html):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f: f.write(html)

# ---------------- shared app fragments ----------------
NAV = [('swap','Swap','/app/swap/','swap'),('stake','Stake','/app/stake/','stake'),('portfolio','Portfolio','/app/portfolio/','portfolio'),
       ('approvals','Approvals','/app/portfolio/#approvals','shield'),('activity','Activity','/app/portfolio/#activity','activity')]
def sidebar(active, connected=True):
    items = ''.join(f'<a class="nav-i{" on" if k==active else ""}" href="{h}">{ic(i)}<span>{l}</span>{"<span class=count>3</span>" if k=="approvals" and connected is True else ""}</a>' for k,l,h,i in NAV)
    return f"""<aside class="side" aria-label="App navigation">
  <div style="display:flex;align-items:center;gap:8px">{brand()}</div>
  <div><div class="grp">Trade</div><nav>{items}</nav></div>
  <div class="foot">
    {DEMO_TAG}
  </div>
</aside>"""

def topbar(title, connected=True):
    w = ('<a class="btn btn-ghost" href="/app/login/" data-roll><span class="lbl-roll">Sign in</span></a>' if connected == 'guest' else
         f'<button class="wallet" type="button" data-copy="0x7a3f9e21b4c05d8817aa3e6f02bd94c7e5a1c91e" aria-label="Copy wallet address {ADDR}"><span class="avatar">{ic("user")}</span><span class="tick">{ic("check")}</span><span class="addr">{ADDR}</span></button>' if connected
         else '<a class="btn btn-primary" href="/app/connect/" data-roll><span class="lbl-roll">Connect wallet</span></a>')
    return f"""<header class="top">
  <h1>{title}</h1>
  <span class="m-brand">{MARK.replace('<svg','<svg width="26" height="26"',1)}</span>
  <div class="tools">
    <span class="net"><span class="dot"></span><span class="lbl">Main network</span>{ic('chev')}</span>
    {w}
  </div>
</header>"""

def tabbar(active):
    t = [('swap','Swap','/app/swap/','swap'),('stake','Stake','/app/stake/','stake'),('portfolio','Portfolio','/app/portfolio/','portfolio'),('activity','Activity','/app/portfolio/#activity','activity')]
    return '<nav class="tabbar" aria-label="App sections">' + ''.join(f'<a href="{h}" class="{"on" if k==active else ""}">{ic(i)}<span>{l}</span></a>' for k,l,h,i in t) + '</nav>'

def app_page(path, title, desc, active, page_title, content, overlay='', connected=True):
    bc = (' class="has-toast"' if 'toast-wrap' in overlay else ' class="has-overlay"') if overlay else ''
    html = head(f'{title} · Stillwater', desc) + f"""<body{bc}>
<div class="app">
{sidebar(active, connected)}
<div class="main">
{topbar(page_title, connected)}
<main class="content" id="main">
{content}
</main>
</div>
</div>
{tabbar(active)}
{overlay}
""" + FOOTJS
    write(path, html)

def drow(k, v, strong=False, tip=True):
    return f'<div class="drow{" strong" if strong else ""}"><span>{k}{ic("info") if tip else ""}</span><span>{v}</span></div>'

def swap_card(state='filled', compact=False):
    if state == 'empty':
        pay_amt, pay_sub, rec_amt, rec_sub = '<span class="amt ph">0</span>', '$0.00', '<span class="amt ph">0</span>', '—'
        rec_tok = '<span class="tok" style="padding-left:12px">Select token' + ic('chev','chev') + '</span>'
    else:
        pay_amt, pay_sub = '<span class="amt">250.00</span>', '$250.00 · ₦ 375,000'
        rec_amt, rec_sub = '<span class="amt">0.0742</span>', '$249.90 · ₦ 374,850'
        rec_tok = f'<span class="tok">{ti("EDDY")}EDDY{ic("chev","chev")}</span>'
    details = '' if (state=='empty' or compact) else f"""
  <div class="details">
    {drow('Rate', '1 EDDY = 3,369.27 CMD', tip=False)}
    {drow('Price impact', '<span class="ok">0.04% · Low</span>')}
    {drow('Network fee', '$0.38 · ₦ 570')}
    {drow('Slippage', '0.5% · Auto')}
    {drow('Route', 'CMD → EDDY · 1 pool', tip=False)}
    {drow('You receive at least', '0.0738 EDDY', strong=True)}
  </div>"""
    cta = ('<a class="btn btn-primary btn-lg btn-block" href="/app/signup/" data-roll><span class="lbl-roll">Sign in to swap</span></a>' if state=='guest'
           else '<a class="btn btn-primary btn-lg btn-block" href="/app/swap-review/" data-roll><span class="lbl-roll">Review swap</span></a>' if state!='empty'
           else '<span class="btn btn-quiet btn-lg btn-block" style="color:var(--smoke)">Enter an amount</span>')
    return f"""<section class="swap" aria-label="Swap">
  <div class="swap-head">
    <div class="tabs"><span class="t on">Swap</span><span class="t">Limit</span><span class="t">Send</span></div>
    <a class="icon-btn" href="/app/swap-settings/" aria-label="Transaction settings">{ic('sliders')}</a>
  </div>
  <div class="field">
    <div class="row"><span class="lbl">You pay</span>{'' if state=='guest' else '<span class="sub">Balance 1,240.00 · <span style="color:var(--white)">Max</span></span>'}</div>
    <div class="row">{pay_amt}<a class="tok" href="/app/swap-token-select/">{ti("CMD")}CMD{ic("chev","chev")}</a></div>
    <div class="row"><span class="sub">{pay_sub}</span></div>
  </div>
  <div class="flip"><span>{ic('down')}</span></div>
  <div class="field">
    <div class="row"><span class="lbl">You receive</span>{'' if state=='guest' else '<span class="sub">Balance 0.4120</span>'}</div>
    <div class="row">{rec_amt}{rec_tok}</div>
    <div class="row"><span class="sub">{rec_sub}</span></div>
  </div>{details}
  <div class="cta">{cta}</div>
</section>"""

def wallet_panel():
    rows = [('CMD','Calm Dollar','1,240.00','$1,240.00'),('EDDY','Eddy','0.4120','$1,388.10'),('SHOL','Shoal','820.50','$615.38'),('KELP','Kelp','2,150.00','$301.00')]
    li = ''.join(f'<div class="li">{ti(s)}<div class="grow"><span class="t1">{s}</span><span class="t2">{n}</span></div><div class="r"><span class="t1">{b}</span><span class="t2">{v}</span></div></div>' for s,n,b,v in rows)
    return f'<section class="panel key"><h3>Your wallet <span class="badge-example badge">Example</span></h3><div class="list">{li}</div></section>'

def sign_panel(step=0):
    s1 = 'done' if step>0 else 'now'
    s2 = 'now' if step>0 else ''
    return f"""<section class="panel key"><h3>What you'll sign <span class="muted" style="font-size:12px;font-weight:400">2 steps</span></h3>
  <div class="stepper">
    <div class="st {s1}"><span class="b">{ic('check') if step>0 else '1'}</span><div><div class="t1">Approve exactly 250 CMD</div><div class="t2">Lets Stillwater move this amount once. Not your whole balance.</div></div></div>
    <div class="st {s2}"><span class="b">2</span><div><div class="t1">Swap 250 CMD for EDDY</div><div class="t2">You get at least 0.0738 EDDY, or the swap cancels and only the fee is spent.</div></div></div>
  </div>
  <div class="note">{ic('info')}<span>Fees are shown in dollars and naira. Change it in settings.</span></div>
</section>"""

def guest_panel():
    return (f'<section class="panel key guest-panel"><h3>Browsing as a guest</h3>'
            f'<p class="muted" style="margin:0;font-size:13.5px;line-height:20px">Browse prices and pools freely. Sign in only when you’re ready to swap or stake.</p>'
            f'<div style="display:flex;gap:8px"><a class="btn btn-primary" style="flex:1" href="/app/signup/" data-roll><span class="lbl-roll">Create account</span></a>'
            f'<a class="btn btn-ghost" style="flex:1" href="/app/connect/" data-roll><span class="lbl-roll">Connect wallet</span></a></div></section>')

def swap_content(state='filled'):
    return f"""<div class="page-head"><div><h2>Swap</h2><p>Every cost in dollars and naira before you sign.</p></div></div>
<div class="swap-layout">
  <div class="swap-center">
    {swap_card(state)}
    <p class="muted" style="font-size:12.5px;margin:0;text-align:center">Quote refreshes every 15s · <span class="mono">Example data</span></p>
  </div>
  <div style="display:flex;flex-direction:column;gap:16px">{sign_panel()}{guest_panel() if state=='guest' else wallet_panel()}</div>
</div>"""

def overlay(inner, label):
    return f'<div class="overlay" role="dialog" aria-modal="true" aria-label="{label}">{inner}</div>'

# ---------------- pages ----------------
def page_swap():
    app_page('app/swap/index.html','Swap','Stillwater swap screen, open without an account: amount, rate, price impact, fees in $ and ₦, and minimum received.','swap','Swap',swap_content('guest'),connected='guest')

def page_token_select():
    rows = [
      ('CMD','Calm Dollar','1,240.00','$1,240.00','0x1c4e…08aa',True,False),
      ('EDDY','Eddy','0.4120','$1,388.10','0x93d1…7f02',True,True),
      ('SHOL','Shoal','820.50','$615.38','0x5b20…e4c9',True,False),
      ('KELP','Kelp','2,150.00','$301.00','0xa7c8…1d36',True,False),
    ]
    r = ''
    for s,n,b,v,a,ver,hov in rows:
        r += f'<div class="tok-row{" hover" if hov else ""}">{ti(s)}<div class="grow"><span class="t1">{s}{ic("shield","verified") if ver else ""}</span><span class="t2">{n} · <span class="mono">{a}</span>{ic("copy","copy")}</span></div><div class="r"><span>{b}</span><span class="t2">{v}</span></div></div>'
    unver = f"""<div class="tok-row">{ti('MRSH')}<div class="grow"><span class="t1">MRSH <span class="badge badge-warn"><span class="dot"></span>Unverified</span></span><span class="t2">Marsh · <span class="mono">0xee01…9b4d</span>{ic("copy","copy")}</span></div><div class="r"><span>0.00</span><span class="t2">—</span></div></div>
<div class="warnbox">{ic('alert')}<span><b style="color:#fff;font-weight:500">New token, low liquidity.</b> Created 2 days ago and not on any token list. Names can be copied, so check the contract address before you swap.</span></div>"""
    chips = ''.join(f'<span class="chip">{ti(s)}{s}</span>' for s in ['CMD','EDDY','SHOL','KELP'])
    inner = f"""<div class="modal">
  <div class="modal-head"><h2>Select a token</h2><a class="icon-btn" href="/app/swap/" aria-label="Close">{ic('x')}</a></div>
  <div class="modal-body">
    <div class="search">{ic('search')}<span>Search name or paste address</span><span class="kbd">/</span></div>
    <div class="chips">{chips}</div>
    <hr class="hr">
    <div class="lbl-sm"><span>Your tokens</span><span class="mono" style="font-weight:400">Balance</span></div>
    <div>{r}</div>
    <div class="lbl-sm"><span>Search results</span></div>
    <div>{unver}</div>
  </div>
</div>"""
    app_page('app/swap-token-select/index.html','Select token','Token selector with search, balances, verified badges and an unverified-token warning.','swap','Swap',swap_content(),overlay(inner,'Select a token'))

def page_settings():
    presets = [('Auto','0.5%',True),('0.1%','',False),('0.5%','',False),('1%','',False),('Custom','',False)]
    seg = '<div class="seg" role="radiogroup" aria-label="Slippage">' + ''.join(f'<span class="{"on" if on else ""}">{a}</span>' for a,b,on in presets) + '</div>'
    expl = [('Auto · 0.5%','Stillwater picks a safe tolerance for this pair. Good for most swaps.'),
            ('0.1%','Tightest. Best price, but the swap may fail if the price moves even slightly.'),
            ('1%','Looser. Goes through in busy markets, but you may get up to 1% less.')]
    ex = ''.join(f'<div class="drow" style="padding:4px 0"><span style="color:var(--white);font-weight:500;min-width:96px">{a}</span><span style="font-family:var(--sans);font-size:12.5px;color:var(--smoke);text-align:left;flex:1">{b}</span></div>' for a,b in expl)
    inner = f"""<div class="modal wide">
  <div class="modal-head"><h2>Transaction settings</h2><a class="icon-btn" href="/app/swap/" aria-label="Close">{ic('x')}</a></div>
  <div class="modal-body">
    <div class="lbl-sm"><span>Slippage tolerance</span><span class="mono" style="font-weight:400;color:var(--white)">0.5%</span></div>
    {seg}
    <div class="note">{ic('info')}<span><b style="color:#fff;font-weight:500">In plain words:</b> if the price moves against you by more than 0.5% before your swap lands, it cancels. On this swap that is at most <span class="mono" style="color:#fff">$1.25 · ₦ 1,875</span>.</span></div>
    <div style="display:flex;flex-direction:column">{ex}</div>
    <hr class="hr">
    <div class="lbl-sm"><span>Approval amount</span></div>
    <div class="opt-grid"><div class="opt on"><span class="radio"></span><div><div class="t1">Exact amount <span class="badge badge-ok">Recommended</span></div><div class="t2">Approve only what this swap needs.</div></div></div>
    <div class="opt"><span class="radio"></span><div><div class="t1">Unlimited</div><div class="t2">Stillwater could move any amount until you revoke it.</div></div></div></div>
    <hr class="hr">
    <div class="drow"><span>Show fees in</span><span><span class="seg" style="display:inline-grid;width:120px;padding:3px"><span class="on" style="height:26px">$</span><span style="height:26px">₦</span></span></span></div>
    <a class="btn btn-primary btn-lg btn-block" href="/app/swap/" data-roll><span class="lbl-roll">Save settings</span></a>
  </div>
</div>"""
    app_page('app/swap-settings/index.html','Settings','Slippage presets with one-line explanations, exact vs unlimited approvals, fee currency.','swap','Swap',swap_content(),overlay(inner,'Transaction settings'))

def page_review():
    inner = f"""<div class="modal wide">
  <div class="modal-head"><h2>Review swap</h2><a class="icon-btn" href="/app/swap/" aria-label="Close">{ic('x')}</a></div>
  <div class="modal-body">
    <div class="pay-row"><div class="l"><span class="lbl-sm">You pay</span><span class="v">250.00 CMD</span></div><div style="display:flex;align-items:center;gap:10px"><span class="mono muted" style="font-size:12px">$250.00</span>{ti('CMD').replace('class="ti"','class="ti" width="32" height="32"')}</div></div>
    <div class="hero-num">
      <span class="lbl-sm">You receive at least</span>
      <span class="big">0.0738 EDDY {ti('EDDY')}</span>
      <span class="mono muted" style="font-size:12px">Expected 0.0742 · $249.90 · ₦ 374,850</span>
    </div>
    <div class="details" style="padding:0 2px">
      {drow('Rate','1 EDDY = 3,369.27 CMD',tip=False)}
      {drow('Price impact','<span class="ok">0.04% · Low</span>')}
      {drow('Network fee','$0.38 · ₦ 570')}
      {drow('Slippage','0.5% · Auto')}
      {drow('Time','~30 seconds',tip=False)}
    </div>
    <div class="plain ember">{ic('lock')}<span><b>What you're signing:</b> this lets Stillwater move up to <b>250 CMD</b> from your wallet, once. Nothing else.</span></div>
    <div class="stepper">
      <div class="st now"><span class="b">1</span><div><div class="t1">Approve 250 CMD <span class="muted" style="font-weight:400">· Step 1 of 2</span></div><div class="t2">Needed once so the swap can use your CMD.</div></div></div>
      <div class="st"><span class="b">2</span><div><div class="t1">Confirm swap</div><div class="t2">Sign in your wallet. Nothing moves until you do.</div></div></div>
    </div>
    <div style="display:flex;gap:8px"><a class="btn btn-ghost btn-lg" href="/app/swap/">Back</a><a class="btn btn-primary btn-lg" style="flex:1" href="/app/success/" data-roll><span class="lbl-roll">Approve 250 CMD</span></a></div>
  </div>
</div>"""
    app_page('app/swap-review/index.html','Review swap','Review modal: you pay, you receive at least, price impact, fees in $ and ₦, plain-English signing summary.','swap','Swap',swap_content(),overlay(inner,'Review swap'))

def page_success():
    content = f"""<div class="page-head"><div><h2>Swap</h2><p>Every cost in dollars and naira before you sign.</p></div></div>
<div class="swap-layout">
  <div class="swap-center">
    <section class="swap done-card key" style="max-width:520px">
      <span class="done-ring" data-draw>{ic('check')}</span>
      <h3 style="margin:0;font-size:22px;font-weight:500">Swap complete</h3>
      <p class="muted" style="margin:0;font-size:14px">You swapped <span class="mono" style="color:#fff">250.00 CMD</span> for <span class="mono" style="color:#fff">0.0741 EDDY</span>.<br>That's within your minimum of 0.0738.</p>
      <div class="txs" style="width:100%;text-align:left">
        <div><span class="k"><i></i>Approved</span><span class="v">250 CMD · exact</span></div>
        <div><span class="k"><i></i>Signed</span><span class="v">14:02:31</span></div>
        <div><span class="k"><i></i>Pending</span><span class="v">24 sec</span></div>
        <div><span class="k"><i></i>Confirmed</span><span class="v">14:02:55</span></div>
      </div>
      <div class="details" style="width:100%;padding:0">
        {drow('Network fee paid','$0.36 · ₦ 540',tip=False)}
        {drow('Transaction','<a href="#" style="display:inline-flex;gap:6px;align-items:center">0x4be2…a91f '+ic('ext')+'</a>',tip=False)}
      </div>
      <div style="display:flex;gap:8px;width:100%"><a class="btn btn-ghost btn-lg" style="flex:1" href="/app/swap/">New swap</a><a class="btn btn-primary btn-lg" style="flex:1" href="/app/stake/" data-roll><span class="lbl-roll">Stake your EDDY</span></a></div>
    </section>
  </div>
  <div style="display:flex;flex-direction:column;gap:16px">{sign_panel(step=2).replace('<div class="st now"><span class="b">2</span>','<div class="st done"><span class="b">'+ic('check')+'</span>')}{wallet_panel().replace('0.4120','0.4861').replace('$1,388.10','$1,637.81').replace('1,240.00','990.00').replace('$1,240.00','$990.00')}</div>
</div>"""
    toast = f"""<div class="toast-wrap" role="status" aria-live="polite">
  <div class="toast"><span class="ic">{ic('check')}</span><div class="grow"><span class="t1">Swap confirmed</span><span class="t2">0.0741 EDDY is in your wallet. Fee: $0.36.</span>
    <div class="acts"><a href="#">View on explorer {ic('ext')}</a><a href="/app/portfolio/" class="muted" style="color:var(--ash)">See activity</a></div>
    <div class="prog"><i></i></div></div><a class="x" href="#" aria-label="Dismiss">{ic('x')}</a></div>
</div>"""
    app_page('app/success/index.html','Swap confirmed','Success state with transaction status component and a confirmation toast.','swap','Swap',content,toast)

POOLS = [
 # sym, name, apr, lock, withdraw, risk, size, sel
 ('EDDY','Eddy liquid staking','3.8%','None','1–5 days','Low','12.4k EDDY',True),
 ('CMD','Calm savings','4.6%','None','Instant','Low','2.1M CMD',False),
 ('SHOL','Shoal vault','7.2%','30 days','After lock-up','Medium','480k SHOL',False),
 ('KELP/CMD','Kelp / CMD pair','18.9%','None','Instant','High','95k KELP',False),
]
def risk_badge(r):
    c = {'Low':'ok','Medium':'warn','High':'risk'}[r]
    return f'<span class="badge badge-{c}"><span class="dot"></span>{r}</span>'

def page_stake():
    rows = ''.join(f"""<tr class="{'sel' if sel else ''}"><td><div class="cell-tok">{ti(s)}<div><b>{n}</b><small>Stake {s.replace('/',' + ')}</small></div></div></td>
      <td class="n">{a}</td><td>{l}</td><td>{w}</td><td>{risk_badge(r)}</td>
      <td style="text-align:right"><span class="btn {'btn-primary' if sel else 'btn-ghost'}" style="height:30px;font-size:13px">{'Selected' if sel else 'Stake'}</span></td></tr>""" for s,n,a,l,w,r,sz,sel in POOLS)
    cards = ''.join(f"""<div class="pc{' sel' if sel else ''}"><div class="row"><div class="cell-tok">{ti(s)}<div><b>{n}</b><small>Lock-up: {l}</small></div></div>{risk_badge(r)}</div>
      <div class="row"><span class="muted">APR (example)</span><span class="mono" style="font-size:15px">{a}</span></div><div class="row"><span class="muted">Withdrawal</span><span>{w}</span></div></div>""" for s,n,a,l,w,r,sz,sel in POOLS)
    bars = ''.join(f'<i style="height:{h}%" class="{"hi" if k>=10 else ""}"></i>' for k,h in enumerate([22,30,26,38,34,44,40,52,48,58,64,70]))
    content = f"""<div class="page-head"><div><h2>Stake</h2><p>Earn on what you hold. Every pool shows its lock-up and what can go wrong.</p></div><span class="badge badge-example">Illustrative yields</span></div>
<div class="stats">
  <div class="stat key" data-glow><span class="k">Your staked</span><span class="v" data-ticker>1.2000 sEDDY</span><span class="mono muted" style="font-size:12px">$4,043.12</span></div>
  <div class="stat key" data-glow><span class="k">Rewards earned</span><span class="v" data-ticker>0.0213 EDDY</span><span class="mono muted" style="font-size:12px">$71.77</span></div>
  <div class="stat key" data-glow><span class="k">Avg. APR {ic('info').replace('<svg','<svg width="12" height="12"',1)}</span><span class="v" data-ticker>3.8%</span><span class="mono muted" style="font-size:12px">Example rate</span></div>
  <div class="stat key" data-glow><span class="k">Next reward</span><span class="v">~6 hrs</span><span class="mono muted" style="font-size:12px">Paid daily</span></div>
</div>
<div class="stake-layout">
  <div style="display:flex;flex-direction:column;gap:24px;min-width:0">
    <section class="tbl-card key">
      <div class="head"><h3>Pools</h3><div class="seg" style="width:260px"><span class="on" style="font-family:var(--sans)">All</span><span style="font-family:var(--sans)">Low risk</span><span style="font-family:var(--sans)">No lock-up</span></div></div>
      <div class="table-wrap" style="overflow-x:auto"><table class="table">
        <thead><tr><th>Pool</th><th style="text-align:right">APR (example)</th><th>Lock-up</th><th>Withdrawal</th><th>Risk</th><th></th></tr></thead>
        <tbody>{rows}</tbody></table></div>
      <div class="pool-cards">{cards}</div>
    </section>
    <section class="panel key">
      <h3>Rewards <a class="btn btn-ghost" style="height:30px;font-size:13px" href="#" data-roll><span class="lbl-roll">Claim 0.0213 EDDY</span></a></h3>
      <div style="display:flex;align-items:flex-end;gap:24px;flex-wrap:wrap">
        <div style="display:flex;flex-direction:column;gap:4px"><span class="mono" style="font-size:28px">0.0213 EDDY</span><span class="mono muted" style="font-size:12px">$71.77 · ₦ 107,655 · since Sep 30</span></div>
        <div class="bars" style="flex:1;min-width:200px" aria-label="Daily rewards, last 12 days">{bars}</div>
      </div>
    </section>
  </div>
  <section class="panel key" aria-label="Stake panel">
    <h3>Stake EDDY {risk_badge('Low')}</h3>
    <div class="field">
      <div class="row"><span class="lbl">Amount</span><span class="sub">Available 0.4120 · <span style="color:#fff">Max</span></span></div>
      <div class="row"><span class="amt">0.2500</span><span class="tok">{ti('EDDY')}EDDY</span></div>
      <div class="row"><span class="sub">$842.32 · ₦ 1,263,480</span></div>
    </div>
    <div class="details" style="padding:0 2px">
      {drow('You receive','≈ 0.2500 sEDDY',tip=True)}
      {drow('APR (example)','3.8%',tip=False)}
      {drow('Projected per year','0.0095 EDDY · $32.01',strong=True,tip=False)}
      {drow('Network fee','$0.21 · ₦ 315',tip=False)}
    </div>
    <div>
      <div class="lbl-sm" style="margin-bottom:6px"><span>Risk label</span><span class="mono" style="font-weight:400">4 lines</span></div>
      <div class="nutrition">
        <div><span>Lock-up</span><span>None. sEDDY is yours to move.</span></div>
        <div><span>Withdrawal</span><span>1–5 days in the unstake queue</span></div>
        <div><span>What can go wrong</span><span>Validator penalties can cut rewards</span></div>
        <div><span>Price</span><span>sEDDY can trade below EDDY</span></div>
      </div>
    </div>
    <a class="btn btn-primary btn-lg btn-block" href="#" data-roll><span class="lbl-roll">Review stake</span></a>
    <p class="muted" style="font-size:12px;margin:0;text-align:center">You can unstake any time. Funds arrive within 1–5 days.</p>
  </section>
</div>"""
    app_page('app/stake/index.html','Stake','Staking pools with illustrative APRs, a stake panel with a four-line risk label, and rewards.','stake','Stake',content)

def chart_svg(w=760, h=220, seed=7):
    random.seed(seed)
    n = 60; v = 100; pts = []
    for i in range(n):
        v += random.uniform(-1.6, 2.0) + (0.5 if i > 40 else 0)
        pts.append(v)
    pts = [sum(pts[max(0,i-2):i+3])/len(pts[max(0,i-2):i+3]) for i in range(n)]
    lo, hi = min(pts), max(pts)
    xy = [(i*(w/(n-1)), h-16-(p-lo)/(hi-lo)*(h-40)) for i,p in enumerate(pts)]
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x,y in xy)
    area = d + f' L{w},{h} L0,{h} Z'
    grid = ''.join(f'<line x1="0" x2="{w}" y1="{y}" y2="{y}" stroke="rgba(255,255,255,.06)"/>' for y in (40, 100, 160))
    lx, ly = xy[-1]
    return f"""<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" role="img" aria-label="Portfolio value, last 30 days (example)">
<defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6e6e6" stop-opacity=".16"/><stop offset="1" stop-color="#e6e6e6" stop-opacity="0"/></linearGradient></defs>
{grid}<path d="{area}" fill="url(#pg)"/><path d="{d}" fill="none" stroke="#e6e6e6" stroke-width="1.6" vector-effect="non-scaling-stroke"/>
<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4" fill="#fff"/><circle cx="{lx:.1f}" cy="{ly:.1f}" r="9" fill="#fff" fill-opacity=".12"/></svg>"""

def page_portfolio():
    bal = [('sEDDY','Staked Eddy','1.2000','$4,043.12',53.3),('EDDY','Eddy','0.4120','$1,388.10',18.3),('CMD','Calm Dollar','1,240.00','$1,240.00',16.3),('SHOL','Shoal','820.50','$615.38',8.1),('KELP','Kelp','2,150.00','$301.00',4.0)]
    shades = ['#e6e6e6','#9c9c9d','#6a6b6c','#454647','#2f3031']
    alloc = '<div class="alloc" aria-hidden="true">' + ''.join(f'<i style="width:{p}%;background:{shades[k]}"></i>' for k,(*_,p) in enumerate(bal)) + '</div>'
    brows = ''.join(f"""<tr><td><div class="cell-tok">{ti(s)}<div><b>{s}</b><small>{n}</small></div></div></td><td class="n">{b}</td><td class="n">{v}</td>
      <td style="width:28%"><div style="display:flex;align-items:center;gap:10px"><div class="alloc"><i style="width:{p}%;background:{shades[k]}"></i></div><span class="mono muted" style="font-size:12px;min-width:44px;text-align:right">{p}%</span></div></td></tr>""" for k,(s,n,b,v,p) in enumerate(bal))
    bcards = ''.join(f'<div class="li">{ti(s)}<div class="grow"><span class="t1">{s}</span><span class="t2">{p}% of portfolio</span></div><div class="r"><span class="t1">{v}</span><span class="t2">{b}</span></div></div>' for s,n,b,v,p in bal)
    acts = [
      ('swap','Swapped CMD → EDDY','250.00 CMD → 0.0741 EDDY','Confirmed','ok','2 min ago'),
      ('key','Approved 250 CMD','Exact amount · Stillwater Router','Confirmed','ok','3 min ago'),
      ('refresh','Swap retried','Price moved past 0.5%, retried at a fresh quote','Failed → fixed','warn','Oct 10'),
      ('stake','Staked 1.0000 EDDY','Received 1.0000 sEDDY','Confirmed','ok','Oct 9'),
      ('gift','Claimed rewards','0.0040 EDDY','Confirmed','ok','Oct 3'),
    ]
    arows = ''.join(f'<div class="li"><span class="act-ico">{ic(i)}</span><div class="grow"><span class="t1">{t}</span><span class="t2">{d}</span></div><div class="r"><span class="badge badge-{c}"><span class="dot"></span>{s}</span><span class="t2" style="font-family:var(--sans)">{w}</span></div></div>' for i,t,d,s,c,w in acts)
    apps = [('Stillwater Router','250 CMD · exact','Low','Used',False),('Eddy Staking','1.0 EDDY · exact','Low','Active',False),('Old DEX router','Unlimited SHOL','High','Since 2025',True)]
    aprows = ''.join(f'<div class="li"><span class="act-ico">{ic("shield")}</span><div class="grow"><span class="t1">{n}</span><span class="t2"><span class="mono">{a}</span> · {s}</span></div><div class="r" style="flex-direction:row;align-items:center;gap:8px">{risk_badge(r)}<span class="btn {"btn-primary" if hot else "btn-ghost"}" style="height:28px;font-size:12.5px">Revoke</span></div></div>' for n,a,r,s,hot in apps)
    content = f"""<div class="page-head"><div><h2>Portfolio</h2><p>Everything you hold, stake and have approved, in one place.</p></div><span class="badge badge-example">Example data</span></div>
<div class="port-top">
  <section class="chart-card key">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap">
      <div style="display:flex;flex-direction:column;gap:8px"><span class="lbl-sm">Total value</span><span class="total" data-ticker>$7,587.60</span>
        <span class="mono" style="font-size:12.5px"><span class="ok">+$82.14 (1.09%)</span> <span class="muted">· 7 days · ₦ 11,381,400</span></span></div>
      <div class="seg" style="width:200px"><span>1D</span><span>1W</span><span class="on">1M</span><span>1Y</span></div>
    </div>
    <div class="chart">{chart_svg()}</div>
    <div class="mono muted" style="display:flex;justify-content:space-between;font-size:11px"><span>Sep 12</span><span>Sep 22</span><span>Oct 2</span><span>Oct 12</span></div>
  </section>
  <section class="panel key">
    <h3>Allocation</h3>{alloc}
    <div class="list">{''.join(f'<div class="drow"><span><i style="width:8px;height:8px;border-radius:2px;background:{shades[k]};display:inline-block"></i>{s}</span><span>{p}%</span></div>' for k,(s,n,b,v,p) in enumerate(bal))}</div>
    <hr class="hr">
    <div class="drow"><span>Staked</span><span>$4,043.12</span></div>
    <div class="drow"><span>Unclaimed rewards</span><span>$71.77</span></div>
    <div class="drow"><span>Networks</span><span>Main + L2</span></div>
  </section>
</div>
<section class="tbl-card key">
  <div class="head"><h3>Balances</h3><span class="muted" style="font-size:12.5px">5 tokens · 2 networks</span></div>
  <div class="table-wrap" style="overflow-x:auto"><table class="table"><thead><tr><th>Token</th><th style="text-align:right">Balance</th><th style="text-align:right">Value</th><th>Allocation</th></tr></thead><tbody>{brows}</tbody></table></div>
  <div class="pool-cards" style="padding:4px 16px">{bcards}</div>
</section>
<div class="two">
  <section class="panel key" id="activity"><h3>Recent activity <a class="link" href="#" style="font-size:13px">View all</a></h3><div class="list">{arows}</div></section>
  <section class="panel key" id="approvals"><h3>Approvals <span class="muted" style="font-size:12px;font-weight:400">Who can spend your tokens</span></h3><div class="list">{aprows}</div>
    <div class="warnbox">{ic('alert')}<span>One app can still spend <b style="color:#fff;font-weight:500">unlimited SHOL</b>. You haven't used it since 2025. Revoking costs about $0.20.</span></div></section>
</div>"""
    app_page('app/portfolio/index.html','Portfolio','Portfolio dashboard: total value, chart, balances, activity and an approvals manager.','portfolio','Portfolio',content)

def page_connect():
    sk = ''.join(f'<div class="li"><span class="act-ico"></span><div class="grow"><span class="skel" style="width:{w}%"></span><span class="skel" style="width:{w-20}%;height:8px;margin-top:6px"></span></div></div>' for w in (60,48,54))
    content = f"""<div class="page-head"><div><h2>Portfolio</h2><p>Everything you hold, stake and have approved, in one place.</p></div></div>
<section class="key"><div class="empty"><span class="empty-ic">{ic("wallet")}</span><h3>Connect a wallet to begin</h3><p>See your balances, swap with every cost shown up front, and stake with the risks spelled out.</p>
  <a class="btn btn-primary btn-lg" href="/app/connect/" data-roll><span class="lbl-roll">Connect wallet</span></a>
  <span class="muted" style="font-size:12.5px">Read-only until you sign something.</span></div></section>
<div class="two"><section class="panel key"><h3>Recent activity</h3><div class="list">{sk}</div></section><section class="panel key"><h3>Approvals</h3><div class="list">{sk}</div></section></div>"""
    opts = [('wallet','Browser wallet','Detected in this browser','Detected',True),('qr','Mobile wallet','Scan a QR code with your phone','',False),('key','Smart wallet','Sign in with a passkey. No seed phrase.','New',False)]
    def wbadge(b):
        if not b: return ''
        cls = 'badge badge-ok' if b == 'Detected' else 'badge'
        return ' <span class="' + cls + '">' + b + '</span>'
    o = ''.join(f'<div class="wallet-opt{" hover" if hov else ""}"><span class="wi">{ic(i)}</span><div class="grow"><span class="t1">{t}{wbadge(b)}</span><span class="t2">{d}</span></div>{ic("chevr")}</div>' for i,t,d,b,hov in opts)
    inner = f"""<div class="modal">
  <div class="modal-head"><h2>Connect a wallet</h2><a class="icon-btn" href="/app/portfolio/" aria-label="Close">{ic('x')}</a></div>
  <div class="modal-body">
    <div style="display:flex;flex-direction:column;gap:8px">{o}</div>
    <div class="note">{ic('eye')}<span><b style="color:#fff;font-weight:500">Connecting only shares your public address.</b> Stillwater can't move anything without your signature, and every signature is explained first.</span></div>
    <p class="muted" style="margin:0;font-size:12px;text-align:center">New to wallets? <a href="#" style="color:#fff">Start here</a></p>
  </div>
</div>"""
    app_page('app/connect/index.html','Connect wallet','Empty dashboard with the connect-wallet modal: browser, mobile and smart wallet options.','portfolio','Portfolio',content,overlay(inner,'Connect a wallet'),connected=False)

def mini_shots():
    s = []
    chart_mini = chart_svg(300,90,3).replace('id="pg"','id="pg2"').replace('url(#pg)','url(#pg2)')
    s.append(f'<div class="shot"><span class="eyebrow">Swap · quote</span><div class="field" style="padding:12px;gap:4px"><div class="row"><span class="amt" style="font-size:22px">250.00</span><span class="tok" style="height:30px">{ti("CMD")}CMD</span></div></div><div class="field" style="padding:12px;gap:4px"><div class="row"><span class="amt" style="font-size:22px">0.0742</span><span class="tok" style="height:30px">{ti("EDDY")}EDDY</span></div></div><div class="drow" style="padding:0"><span>Fee</span><span>$0.38 · ₦ 570</span></div></div>')
    s.append('<div class="shot"><span class="eyebrow">Review</span><span class="lbl-sm">You receive at least</span><span class="mono" style="font-size:30px;line-height:1.1">0.0738 EDDY</span><div class="drow" style="padding:0"><span>Price impact</span><span class="ok">0.04%</span></div><div class="drow" style="padding:0"><span>Slippage</span><span>0.5%</span></div><span class="btn btn-primary" style="margin-top:auto">Approve 250 CMD</span></div>')
    s.append(f'<div class="shot"><span class="eyebrow">Stake · risk label</span><div style="display:flex;justify-content:space-between;align-items:center"><span class="mono" style="font-size:28px">3.8%</span>{risk_badge("Low")}</div><div class="nutrition"><div><span>Lock-up</span><span>None</span></div><div><span>Withdrawal</span><span>1–5 days</span></div><div><span>Can go wrong</span><span>Penalties</span></div></div></div>')
    s.append('<div class="shot"><span class="eyebrow">Transaction</span><div class="stepper"><div class="st done"><span class="b">' + ic('check') + '</span><div><div class="t1">Approved</div><div class="t2">250 CMD · exact</div></div></div><div class="st done"><span class="b">' + ic('check') + '</span><div><div class="t1">Signed</div><div class="t2">14:02:31</div></div></div><div class="st now"><span class="b">3</span><div><div class="t1">Pending</div><div class="t2">Usually under 30s</div></div></div></div></div>')
    s.append(f'<div class="shot"><span class="eyebrow">Portfolio</span><span class="mono" style="font-size:26px">$7,587.60</span><span class="mono ok" style="font-size:11px">+1.09% · 7d</span><div class="chart" style="margin-top:auto">{chart_mini}</div></div>')
    s.append('<div class="shot"><span class="eyebrow">Approvals</span><div class="li" style="padding:6px 0"><span class="act-ico">' + ic('shield') + '</span><div class="grow"><span class="t1">Stillwater Router</span><span class="t2">250 CMD · exact</span></div>' + risk_badge('Low') + '</div><div class="li" style="padding:6px 0"><span class="act-ico">' + ic('shield') + '</span><div class="grow"><span class="t1">Old DEX router</span><span class="t2">Unlimited SHOL</span></div>' + risk_badge('High') + '</div><span class="btn btn-ghost" style="margin-top:auto">Revoke unlimited</span></div>')
    return ''.join(s)

def page_landing():
    hero_window = f"""<div class="window">
  <div class="chrome"><i></i><i></i><i></i><span class="addr">stillwater · swap</span></div>
  <div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;padding:24px;align-items:start" class="hero-grid">
    {swap_card('filled')}
    <div style="display:flex;flex-direction:column;gap:14px">
      <div class="plain ember">{ic('lock')}<span><b>What you're signing:</b> this lets Stillwater move up to <b>250 CMD</b> from your wallet, once. Nothing else.</span></div>
      {sign_panel()}
    </div>
  </div>
</div>"""
    principles = [('No surprises at signature','A plain-English summary before every signature.'),('Exact approvals by default','Approve what this swap needs, not your whole balance.'),('Costs in $ and ₦','Gas, slippage and impact in money, not jargon.'),('Every error has a next step','Failures explain what happened and how to retry.')]
    pr = ''.join(f'<div data-glow data-appear style="--d:{k}"><b>{a}</b><span>{b}</span></div>' for k,(a,b) in enumerate(principles))
    steps = [
      ('01','Connect, read-only','Connecting shares your public address and nothing else. Stillwater never asks for a seed phrase.', f'<div class="wallet-opt" style="padding:10px"><span class="wi">{ic("wallet")}</span><div class="grow"><span class="t1" style="font-size:14px">Browser wallet <span class="badge badge-ok">Detected</span></span></div></div>'),
      ('02','See every cost first','You see what you pay, the least you will receive, and every fee in dollars and naira before anything is signed.', f'<div class="well" style="padding:12px 14px">{drow("You receive at least","0.0738 EDDY",strong=True,tip=False)}{drow("Network fee","$0.38 · ₦ 570",tip=False)}</div>'),
      ('03','Sign once, track honestly','A two-step stepper explains the approval, then live status from signature to confirmation, with an explorer link.', '<div class="txs" style="grid-template-columns:repeat(3,1fr)"><div><span class="k"><i></i>Signed</span></div><div><span class="k"><i></i>Pending</span></div><div><span class="k"><i style="background:var(--iron)"></i>Done</span></div></div>'),
    ]
    st = ''.join(f'<article class="step key" data-glow data-appear style="--d:{k}"><span class="n">{n}</span><h3>{t}</h3><p>{d}</p><div class="demo">{demo}</div></article>' for k,(n,t,d,demo) in enumerate(steps))
    pools = ''.join(f"""<article class="pool key" data-glow data-appear style="--d:{k}"><div class="top"><div class="cell-tok">{ti(s)}<div><b>{n}</b><small class="muted">Stake {s.replace('/',' + ')}</small></div></div>{risk_badge(r)}</div>
      <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:12px"><span class="apr" data-ticker>{a}</span><span class="badge badge-example">Example APR</span></div>
      <div class="nutrition"><div><span>Lock-up</span><span>{l}</span></div><div><span>Withdrawal</span><span>{w}</span></div><div><span>What can go wrong</span><span>{wr}</span></div></div></article>"""
      for k,(s,n,a,l,w,r,wr) in enumerate([('EDDY','Eddy liquid staking','3.8%','None','1–5 days','Low','Validator penalties'),('SHOL','Shoal vault','7.2%','30 days','After lock-up','Medium','Funds locked 30 days'),('KELP/CMD','Kelp / CMD pair','18.9%','None','Instant','High','Impermanent loss')]))
    sec = [
      ('lock','Plain-English signing','Before your wallet opens, Stillwater says what the signature allows, like “This lets Stillwater move up to 250 CMD. Nothing else.”'),
      ('key','Exact-amount approvals','Approvals default to the amount you are swapping. Unlimited is there for power users, with the trade-off stated.'),
      ('shield','Approvals manager','See every app that can spend your tokens, flag the risky ones, and revoke without leaving the app.'),
      ('alert','Impostor-token warnings','Verified badges, contract addresses you can copy, and a clear warning for new or low-liquidity tokens.'),
    ]
    sc = ''.join(f'<article class="sec-card key" data-glow data-appear style="--d:{k%2}"><span class="act-ico" style="width:40px;height:40px">{ic(i)}</span><h3>{t}</h3><p>{d}</p></article>' for k,(i,t,d) in enumerate(sec))
    faqs = [
      ('Can I use Stillwater with real funds?','Not yet. This is a demo build designed by Olayemi. The tokens, prices, yields and addresses you see are example data that show how Stillwater works.'),
      ('What does “you receive at least” mean?','It is the smallest amount your swap can return. If the market moves so you would get less, the swap cancels instead, and only the network fee is spent.'),
      ('Why approve before I swap?','Your wallet has to allow an app to move a token before the swap can use it. Stillwater asks for the exact amount you are swapping, not your whole balance, and explains it once.'),
      ('What is slippage, in plain words?','How far the price may move against you while your swap is on its way. Stillwater shows it as money, like “at most $1.25”, so the setting means something.'),
      ('How is staking risk shown?','Every pool has a four-line risk label: lock-up, withdrawal time, what can go wrong, and price. Low, medium and high badges use the only colours on the page.'),
      ('What happens if a transaction fails?','You see what happened in plain words, how much gas was spent, and a suggested fix with a one-tap retry. Stuck transactions can be sped up or cancelled, with the cost of each.'),
    ]
    fq = ''.join(f'<details{" open" if k==0 else ""}><summary>{q}{ic("plus")}</summary><p>{a}</p></details>' for k,(q,a) in enumerate(faqs))
    html = head('Stillwater — swap and stake with every cost in plain sight', 'Stillwater is a calm DeFi swap and stake app, designed by Olayemi. Every cost and risk shown in plain words before you sign.') + f"""<body>
<a class="sr-only" href="#main">Skip to content</a>
<header class="site-nav"><div class="bar">
  <div class="left">{brand()}</div>
  <nav class="links" aria-label="Sections"><a class="link" href="#how" data-roll>How it works</a><a class="link" href="#swap" data-roll>Swap</a><a class="link" href="#stake" data-roll>Staking</a><a class="link" href="#security" data-roll>Security</a><a class="link" href="#faq" data-roll>FAQ</a></nav>
  <div class="right"><a class="link nav-login" href="/app/login/" data-roll>Log in</a><a class="btn btn-primary" href="/app/signup/" data-roll><span class="lbl-roll">Get started</span></a></div>
</div></header>
<main id="main">
<section class="hero">
  <div class="hero-art" aria-hidden="true" data-water="hero"><div class="glow"></div><div class="bar b1"></div><div class="bar b2"></div><div class="bar b3"></div><div class="fade"></div></div>
  <div class="wrap">
    <div class="hero-inner">
      <span class="eyebrow" data-appear>DeFi swap + stake</span>
      <h1 data-reveal>Swap and stake with every cost in plain sight.</h1>
      <p class="lede" data-appear style="--d:2">Stillwater shows what you pay, the least you will get, and what can go wrong, in plain words and in dollars and naira, before you sign anything.</p>
      <div class="ctas" data-appear style="--d:3"><a class="btn btn-primary btn-lg" href="/app/signup/" data-roll><span class="lbl-roll">Get started</span></a><a class="btn btn-ghost btn-lg" href="/app/swap/" data-roll><span class="lbl-roll">Try the app</span></a></div>
    </div>
    <div class="hero-shot">{hero_window}</div>
    <div class="principles">{pr}</div>
  </div>
</section>

<section class="strip-sec" aria-label="Screens" style="padding-top:96px">
  <div class="wrap"><div class="section-head" style="margin-bottom:24px"><span class="eyebrow" data-appear>Screens</span></div></div>
  <div class="strip"><div class="strip-track">{mini_shots()}</div></div>
</section>

<section class="statement" aria-label="Why Stillwater"><div class="wrap">
  <p data-scrub-words>DeFi asks you to sign things you can’t read. Stillwater shows what you pay, the least you’ll get and what can go wrong, in plain words, before you sign anything.</p>
</div></section>

<section class="section" id="how"><div class="wrap">
  <div class="section-head"><span class="eyebrow" data-appear>How it works</span><h2 data-reveal>Three calm steps, no hex soup.</h2><p data-appear>Built for people who were burned by a pop-up they couldn't read, and for people who sign twenty a day.</p></div>
  <div class="steps-wrap"><div class="steps-line" aria-hidden="true"><i></i></div><div class="steps">{st}</div></div>
</div></section>

<section class="section" id="swap" style="padding-top:0"><div class="wrap split">
  <div>
    <div class="section-head" style="margin-bottom:0"><span class="eyebrow" data-appear>Swap preview</span><h2 data-reveal>The least you'll receive is the hero number.</h2><p data-appear>There's no undo in DeFi, so the review screen does that job. Every figure is in money you understand.</p></div>
    <ul class="ticks">
      <li data-appear>{ic('check')}<span><b>Minimum received, up front.</b> If the price slips past it, the swap cancels.</span></li>
      <li data-appear style="--d:1">{ic('check')}<span><b>Fees in $ and ₦.</b> Gas and price impact as money, with a local-currency toggle.</span></li>
      <li data-appear style="--d:2">{ic('check')}<span><b>Slippage, explained.</b> Each preset comes with one line on what it means for you.</span></li>
    </ul>
  </div>
  <div data-appear style="display:flex;justify-content:center">{swap_card('filled')}</div>
</div></section>

<section class="section" id="stake" style="padding-top:0"><div class="wrap">
  <div class="section-head"><span class="eyebrow" data-appear>Staking</span><h2 data-reveal>Yields with the risks written on the label.</h2><p data-appear>Every pool carries a four-line risk label. Rates shown are examples.</p></div>
  <div class="pools">{pools}</div>
</div></section>

<section class="section" id="security" style="padding-top:0"><div class="wrap">
  <div class="section-head"><span class="eyebrow" data-appear>Security</span><h2 data-reveal>Built for the moment you sign.</h2><p data-appear>Bad signatures are where people get hurt, so most of the design goes there.</p></div>
  <div class="sec-grid">{sc}</div>
</div></section>

<section class="section" id="faq" style="padding-top:0"><div class="wrap">
  <div class="section-head center"><span class="eyebrow" data-appear>FAQ</span><h2 data-reveal>Questions, answered plainly.</h2></div>
  <div class="faq">{fq}</div>
</div></section>

<section class="cta-band"><div class="glow" aria-hidden="true"></div>
  <div style="position:relative;display:flex;flex-direction:column;align-items:center;gap:24px"><h2 data-reveal>Calm water, clear costs.</h2><a class="btn btn-primary btn-lg" href="/app/signup/" data-roll><span class="lbl-roll">Get started</span></a></div>
</section>
</main>
<footer class="site-foot"><div class="wrap">
  <div class="foot-grid">
    <div style="display:flex;flex-direction:column;gap:14px;align-items:flex-start"><div style="display:flex;align-items:center;gap:8px">{brand()}</div><p class="muted" style="margin:0;font-size:14px;max-width:320px">A calm DeFi swap and stake app. Every cost and risk in plain sight.</p></div>
    <div><h4>Product</h4><ul><li><a class="link" href="/app/swap/" data-roll>Swap</a></li><li><a class="link" href="/app/stake/" data-roll>Stake</a></li><li><a class="link" href="/app/portfolio/" data-roll>Portfolio</a></li></ul></div>
    <div><h4>Learn</h4><ul><li><a class="link" href="#how" data-roll>How it works</a></li><li><a class="link" href="#security" data-roll>Security</a></li><li><a class="link" href="#faq" data-roll>FAQ</a></li></ul></div>
    <div><h4>Account</h4><ul><li><a class="link" href="/app/signup/" data-roll>Create account</a></li><li><a class="link" href="/app/login/" data-roll>Log in</a></li><li><a class="link" href="/" data-roll>All screens</a></li></ul></div>
  </div>
  <div class="foot-note">
    {DEMO_TAG}
    <div class="meta-strip"><span>v0.1</span><span>Example data</span></div>
  </div>
</div></footer>
""" + FOOTJS
    write('landing/index.html', html)


# ---------------- sign-up and login ----------------
G_GLYPH = ic('google')
A_GLYPH = ic('apple')

def steps_bar(n, total=4, label=''):
    segs = ''.join(f'<i class="{"on" if k < n else ""}"></i>' for k in range(total))
    return f'<div class="steps-bar"><span class="mono">Step {n} of {total}{" · " + label if label else ""}</span><div class="segs" aria-hidden="true">{segs}</div></div>'

MARK28 = tile(32)
def auth_aside(kind):
    if kind == 'signup':
        body = ('<span class="eyebrow">What you get</span><h2>Calm DeFi, from the first tap.</h2>'
                '<ul class="ticks">'
                f'<li>{ic("check")}<span><b>A smart wallet in seconds.</b> Secured by a passkey on your phone, no seed phrase to write down.</span></li>'
                f'<li>{ic("check")}<span><b>Every cost before you sign.</b> Fees, the least you get and what can go wrong, in $ or ₦.</span></li>'
                f'<li>{ic("check")}<span><b>Exact approvals by default.</b> Stillwater only asks for what each swap needs.</span></li></ul>')
    elif kind == 'login':
        body = ('<span class="eyebrow">Welcome back</span><h2>Your wallet, exactly as you left it.</h2>'
                '<div class="aside-stats">'
                '<div class="key"><span class="eyebrow">Portfolio</span><span class="mono v">$1,284.50</span><span class="badge badge-example">Example</span></div>'
                '<div class="key"><span class="eyebrow">Staked</span><span class="mono v">0.42 EDDY</span><span class="muted" style="font-size:12px">Earning 3.8% <span class="mono">(example)</span></span></div></div>')
    else:
        body = ('<span class="eyebrow">Your smart wallet</span><h2>Simple to start, safe to sign.</h2>'
                f'<div class="aside-wallet key"><div class="row">{MARK28}<div><b>Smart wallet</b><small class="mono muted">{ADDR}</small></div><span class="badge badge-ok"><span class="dot"></span>Protected</span></div>'
                f'<div class="drow"><span>Sign-in</span><span>Passkey · this device</span></div><div class="drow"><span>Recovery</span><span>Email + passkey</span></div><div class="drow"><span>Approvals</span><span>Exact, by default</span></div></div>')
    return f'<aside class="auth-art" aria-label="About Stillwater"><div class="auth-art-bg" aria-hidden="true" data-water="soft"><div class="glow"></div></div><div class="auth-art-in">{body}</div></aside>'

def auth_page(path, title, desc, content, aside='signup', top_link=('Log in','/app/login/','Already have an account?')):
    q, h, lead = top_link
    html = head(f'{title} · Stillwater', desc) + f"""<body class="auth-body">
<a class="sr-only" href="#main">Skip to content</a>
<div class="auth">
  <div class="auth-main">
    <header class="auth-top">{brand('/landing/')}<span class="auth-switch"><span class="muted">{lead}</span> <a class="link" href="{h}" data-roll>{q}</a></span></header>
    <main class="auth-form" id="main">
{content}
    </main>
    <footer class="auth-foot"><span>{DEMO_TAG}</span><span class="links"><a class="link" href="#" data-roll>Terms</a><a class="link" href="#" data-roll>Privacy</a><a class="link" href="/" data-roll>All screens</a></span></footer>
  </div>
  {auth_aside(aside)}
</div>
""" + FOOTJS
    write(path, html)

def social_buttons(verb='Continue'):
    return (f'<div class="social"><a class="btn btn-social btn-lg btn-block" href="/app/signup-preferences/" data-roll>{G_GLYPH}<span class="lbl-roll">{verb} with Google</span></a>'
            f'<a class="btn btn-social btn-lg btn-block" href="/app/signup-preferences/" data-roll>{A_GLYPH}<span class="lbl-roll">{verb} with Apple</span></a></div>')

def page_signup():
    c = f"""      <div class="auth-head"><h1>Create your account</h1><p>Start with your email. You’ll get a smart wallet secured by a passkey, no seed phrase needed.</p></div>
      <form class="auth-fields" action="/app/signup-verify/" method="get">
        <label class="fld"><span class="fld-l">Email</span><input class="input" type="email" name="email" autocomplete="email" placeholder="you@example.com" required></label>
        <a class="btn btn-primary btn-lg btn-block" href="/app/signup-verify/" data-roll><span class="lbl-roll">Continue with email</span></a>
      </form>
      <div class="or"><span>or</span></div>
      {social_buttons()}
      <a class="wallet-link well" href="/app/connect/">{ic('wallet')}<span><b>Already have a wallet?</b> <span class="ash">Connect wallet</span></span>{ic('chevr')}</a>
      <div class="guest-opt"><a class="btn btn-ghost btn-lg btn-block" href="/app/swap/" data-roll><span class="lbl-roll">Explore without an account</span></a><p>Browse prices and pools freely. Sign in only when you’re ready to swap or stake.</p></div>
      <p class="fine">By continuing you agree to the <a href="#">Terms</a> and <a href="#">Privacy Policy</a>.</p>"""
    auth_page('app/signup/index.html', 'Sign up', 'Create a Stillwater account with email, Google or Apple, or connect a wallet you already have.', c)

def page_signup_verify():
    digits = ['4','8','2','','','']
    boxes = ''.join(f'<input class="otp-box{" filled" if d else ""}{" active" if k==3 else ""}" type="text" inputmode="numeric" maxlength="1" value="{d}" aria-label="Digit {k+1} of 6" autocomplete="{"one-time-code" if k==0 else "off"}">' for k,d in enumerate(digits))
    c = f"""      {steps_bar(1, 4, 'Verify email')}
      <div class="auth-head"><h1>Check your email</h1><p>We sent a 6-digit code to <b class="mono">ada.o@example.com</b>. It expires in 10 minutes.</p></div>
      <div class="auth-fields">
        <fieldset class="otp"><legend class="fld-l">Verification code</legend><div class="otp-row">{boxes}</div></fieldset>
        <div class="otp-meta"><span class="muted">{ic('clock')}Resend code in <span class="mono" data-countdown="42">0:42</span></span><a class="link" href="/app/signup/" data-roll>Change email</a></div>
        <a class="btn btn-primary btn-lg btn-block" href="/app/signup-passkey/" data-roll><span class="lbl-roll">Verify</span></a>
      </div>
      <p class="fine">Can’t find it? Check spam, or wait for the timer and resend.</p>"""
    auth_page('app/signup-verify/index.html', 'Verify your email', 'Enter the 6-digit code sent to your email, with a resend timer and a change-email link.', c, aside='signup')

def page_signup_passkey():
    c = f"""      {steps_bar(2, 4, 'Secure your wallet')}
      <div class="pk-art" aria-hidden="true"><span class="pk-key">{ic('key')}</span><span class="pk-ring"></span></div>
      <div class="auth-head"><h1>Create a passkey</h1><p>A passkey unlocks your Stillwater wallet with your face, fingerprint or phone screen lock. There’s nothing to write down and nothing to lose.</p></div>
      <ul class="pk-list">
        <li>{ic('lock')}<span><b>Stays on your device.</b> Stillwater never sees your fingerprint or face.</span></li>
        <li>{ic('shield')}<span><b>Can’t be phished.</b> It only works on Stillwater, not on look-alike sites.</span></li>
        <li>{ic('refresh')}<span><b>Synced and recoverable.</b> Backed up with your phone’s keychain, plus email recovery.</span></li>
      </ul>
      <div class="auth-fields">
        <a class="btn btn-primary btn-lg btn-block" href="/app/signup-preferences/" data-roll>{ic('key')}<span class="lbl-roll">Create passkey</span></a>
        <a class="btn btn-ghost btn-lg btn-block" href="#" data-roll><span class="lbl-roll">Use a seed phrase instead</span></a>
      </div>
      <p class="fine">A seed phrase is 12 words you’d keep safe yourself. Choose it if you already manage your own keys.</p>"""
    auth_page('app/signup-passkey/index.html', 'Create a passkey', 'Create a passkey for your Stillwater smart wallet, explained in plain language, with a seed-phrase option.', c, aside='wallet', top_link=('Exit setup','/landing/',''))

def opt(title, sub, on=False, name='x'):
    return f'<label class="opt{" on" if on else ""}" data-glow><input type="radio" name="{name}"{" checked" if on else ""}><span class="opt-dot" aria-hidden="true"></span><span><b>{title}</b><small>{sub}</small></span></label>'

def page_signup_preferences():
    c = f"""      {steps_bar(3, 4, 'Preferences')}
      <div class="auth-head"><h1>Make it yours</h1><p>Three quick choices. You can change any of them later in Settings.</p></div>
      <div class="auth-fields">
        <fieldset class="pref"><legend class="fld-l">Show amounts in</legend>
          <div class="seg seg-cur"><label class="on"><input type="radio" name="cur" checked><span class="mono">$</span> US dollar</label><label><input type="radio" name="cur"><span class="mono">₦</span> Naira</label></div>
        </fieldset>
        <fieldset class="pref"><legend class="fld-l">Your experience with crypto</legend>
          <div class="opts">{opt('New to it','I’ve never swapped or staked.', False, 'exp')}{opt('Some experience','I’ve swapped a few times.', True, 'exp')}{opt('Experienced','I sign transactions most weeks.', False, 'exp')}</div>
        </fieldset>
        <fieldset class="pref"><legend class="fld-l">Risk comfort</legend>
          <div class="seg seg-risk"><label><input type="radio" name="risk">Careful</label><label class="on"><input type="radio" name="risk" checked>Balanced</label><label><input type="radio" name="risk">Adventurous</label></div>
          <p class="hint">{ic('info')}Balanced shows low and medium risk pools first, and asks again before anything high risk.</p>
        </fieldset>
        <a class="btn btn-primary btn-lg btn-block" href="/app/signup-welcome/" data-roll><span class="lbl-roll">Continue</span></a>
      </div>"""
    auth_page('app/signup-preferences/index.html', 'Your preferences', 'Choose $ or ₦ as display currency, your experience level and your risk comfort.', c, aside='wallet', top_link=('Exit setup','/landing/',''))

def page_signup_welcome():
    rows = [('Account','ada.o@example.com'),('Wallet', f'<span class="mono">{ADDR}</span>'),('Secured by','Passkey · this device'),('Amounts in','$ US dollar'),('Experience','Some experience'),('Risk comfort','Balanced')]
    summ = ''.join(f'<div class="drow"><span>{k}</span><span>{v}</span></div>' for k,v in rows)
    fund = [('globe','Bank transfer in ₦','Arrives as CMD in about 10 min'),('wallet','From another wallet','Send any supported token'),('qr','Receive with QR','Share your wallet address')]
    fl = ''.join(f'<a class="fund-i" href="#" data-glow><span class="act-ico">{ic(i)}</span><span><b>{t}</b><small>{s}</small></span>{ic("chevr")}</a>' for i,t,s in fund)
    c = f"""      {steps_bar(4, 4, 'All set')}
      <div class="auth-head"><span class="done-ico" aria-hidden="true">{ic('check')}</span><h1>You’re all set, Ada</h1><p>Your smart wallet is ready. Here’s what we set up.</p></div>
      <div class="summary well">{summ}</div>
      <section class="fund"><div class="fund-h"><h2>Fund your wallet</h2><span class="badge badge-example">Illustrative</span></div>{fl}</section>
      <div class="auth-fields">
        <a class="btn btn-primary btn-lg btn-block" href="/app/swap/" data-roll><span class="lbl-roll">Start swapping</span></a>
        <a class="btn btn-quiet btn-lg btn-block" href="/app/portfolio/" data-roll><span class="lbl-roll">Skip for now</span></a>
      </div>"""
    auth_page('app/signup-welcome/index.html', 'Welcome', 'Account summary, an illustrative Fund your wallet step and Start swapping.', c, aside='wallet', top_link=('Exit setup','/landing/',''))

def page_login():
    c = f"""      <div class="auth-head"><h1>Log in to Stillwater</h1><p>Use your passkey, or the email you signed up with.</p></div>
      <div class="auth-fields">
        <a class="btn btn-primary btn-lg btn-block" href="/app/portfolio/" data-roll>{ic('key')}<span class="lbl-roll">Log in with passkey</span></a>
      </div>
      <div class="or"><span>or</span></div>
      <form class="auth-fields" action="/app/portfolio/" method="get">
        <label class="fld"><span class="fld-l">Email</span><input class="input" type="email" name="email" autocomplete="email" placeholder="you@example.com"></label>
        <a class="btn btn-quiet btn-lg btn-block" href="/app/signup-verify/" data-roll><span class="lbl-roll">Email me a code</span></a>
      </form>
      {social_buttons()}
      <a class="wallet-link well" href="/app/connect/">{ic('wallet')}<span><b>Use a wallet instead?</b> <span class="ash">Connect wallet</span></span>{ic('chevr')}</a>
      <div class="guest-opt"><a class="btn btn-ghost btn-lg btn-block" href="/app/swap/" data-roll><span class="lbl-roll">Explore without an account</span></a><p>Browse prices and pools freely. Sign in only when you’re ready to swap or stake.</p></div>
      <p class="fine">By continuing you agree to the <a href="#">Terms</a> and <a href="#">Privacy Policy</a>.</p>"""
    auth_page('app/login/index.html', 'Log in', 'Log in to Stillwater with a passkey, email, Google, Apple or a wallet.', c, aside='login', top_link=('Create account','/app/signup/','New to Stillwater?'))

SCREENS = [
 ('Landing page','Marketing site with the motion: hero, how it works, swap preview, staking examples, security, FAQ, footer.','/landing/'),
 ('Sign up','Create an account: email, Continue with Google or Apple, or connect a wallet you already have.','/app/signup/'),
 ('Sign up · verify email','Six-digit code input with a resend timer and a change-email link.','/app/signup-verify/'),
 ('Sign up · passkey','Create a passkey for the smart wallet, in plain language, with a seed-phrase fallback.','/app/signup-passkey/'),
 ('Sign up · preferences','Display currency ($ or ₦), experience level and risk comfort.','/app/signup-preferences/'),
 ('Sign up · welcome','Summary, an illustrative “Fund your wallet” step and Start swapping.','/app/signup-welcome/'),
 ('Log in','Passkey-first login with email, Google, Apple or a wallet.','/app/login/'),
 ('Swap · guest','Open without an account: a live-looking quote, fees in $ and ₦, minimum received, and a quiet Sign in. Signing up is optional.','/app/swap/'),
 ('Swap · token select','Token selector with search, balances, verified badges and an unverified-token warning.','/app/swap-token-select/'),
 ('Swap · settings','Slippage presets with one-line explanations, exact vs unlimited approvals.','/app/swap-settings/'),
 ('Swap · review','Review modal: you receive at least, fees, plain-English signing summary, Step 1 of 2.','/app/swap-review/'),
 ('Swap · success','Confirmed state with the transaction status component and a toast.','/app/success/'),
 ('Stake','Pools with illustrative APRs, stake panel with risk label, rewards.','/app/stake/'),
 ('Portfolio','Total value, chart, balances, activity and approvals manager.','/app/portfolio/'),
 ('Connect wallet','Empty dashboard plus the connect-wallet modal.','/app/connect/'),
]
def page_index():
    cards = ''.join(f"""<article class="idx-card key" data-glow><span class="eyebrow">{k+1:02d}</span><h3>{t}</h3><p>{d}</p>
      <div class="links"><a href="{u}" data-roll><span class="lbl-roll">Open</span></a><a class="sec" href="{u}?figma=1">Figma import link</a><span class="mono muted" style="font-size:11px">{u}</span></div></article>""" for k,(t,d,u) in enumerate(SCREENS))
    html = head('Stillwater — all screens', 'Every Stillwater screen: landing, sign-up and login, swap, stake, portfolio, connect wallet and success states. Demo DeFi swap and stake app, designed by Olayemi.') + f"""<body>
<div class="page-water" data-water aria-hidden="true"></div>
<header class="site-nav"><div class="bar"><div class="left">{brand()}</div><div class="right"><a class="btn btn-primary" href="/landing/" data-roll><span class="lbl-roll">View landing</span></a></div></div></header>
<main class="idx" id="main"><div class="wrap">
  <span class="eyebrow">Screens · Designed by Olayemi</span>
  <h1 data-reveal style="margin-top:16px">Stillwater screens</h1>
  <p class="ash" style="max-width:640px;font-size:17px;margin:16px 0 0">Each screen has its own URL so it can be imported one at a time. Every page is responsive: import at 1440 for desktop and 390 for mobile. The “Figma import link” turns all motion off so the final state imports cleanly.</p>
  <div class="idx-grid">{cards}</div>
  <div class="foot-note" style="margin-top:64px"><span class="muted" style="font-size:13px">Style inspired by Raycast's design language. Motion inspired by Visuvate. No assets copied.</span>{DEMO_TAG}</div>
</div></main>
""" + FOOTJS
    write('index.html', html)

if __name__ == '__main__':
    write_icons(); page_index(); page_landing(); page_signup(); page_signup_verify(); page_signup_passkey(); page_signup_preferences(); page_signup_welcome(); page_login(); page_swap(); page_token_select(); page_settings(); page_review(); page_success(); page_stake(); page_portfolio(); page_connect()
    print('built')
