#!/usr/bin/env python3
"""Stillwater mobile app frames (iOS-style, 390x844). Run: python3 build_mobile.py
Icons: Line Awesome by Icons8, read from ../site/assets/icons/ (same files as the website).
Writes frames/NN_name.html. Icons, demo tokens and the logo mark come from the website's generator,
and the mark itself from ONE file: ../site/assets/mark.svg (swap it there, rebuild both)."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
SITE_BUILD = os.path.normpath(os.path.join(HERE, '..', 'tools', 'build.py'))
spec = importlib.util.spec_from_file_location('swsite', SITE_BUILD); sw = importlib.util.module_from_spec(spec); spec.loader.exec_module(sw)
ic, ti, MARK, ADDR = sw.ic, sw.ti, sw.MARK, sw.ADDR
# every icon (including gear, faceid→fingerprint, recv, send, bell, back, del, user, chip, browser) is a Line Awesome file mapped in sw.ICON_MAP
OUT = os.path.join(HERE, 'frames')
os.makedirs(OUT, exist_ok=True)

def isz(name, n):
    return ic(name).replace('<svg', '<svg width="%d" height="%d"' % (n, n), 1)

def mark(size):
    return MARK.replace('<svg', f'<svg width="{size}" height="{size}"', 1)

SB = ('<div class="sb"><span class="t">9:41</span><span class="ic">'
      '<svg width="18" height="12" viewBox="0 0 18 12" fill="#fff"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>'
      '<svg width="17" height="12" viewBox="0 0 17 12" fill="#fff"><path d="M8.5 2.3c2.4 0 4.6.9 6.3 2.5l1.2-1.3A10.6 10.6 0 0 0 8.5.5 10.6 10.6 0 0 0 1 3.5l1.2 1.3a8.9 8.9 0 0 1 6.3-2.5z"/><path d="M8.5 5.8c1.5 0 2.8.5 3.8 1.5l1.2-1.3a7 7 0 0 0-5-2 7 7 0 0 0-5 2l1.2 1.3c1-1 2.3-1.5 3.8-1.5z"/><path d="M8.5 9.2c.6 0 1.1.2 1.5.6L8.5 11.5 7 9.8c.4-.4.9-.6 1.5-.6z"/></svg>'
      '<svg width="27" height="13" viewBox="0 0 27 13" fill="none"><rect x=".5" y=".5" width="23" height="12" rx="3.8" stroke="#fff" stroke-opacity=".4"/><rect x="2" y="2" width="20" height="9" rx="2.5" fill="#fff"/><path d="M25 4.5v4c.8-.3 1.3-1.1 1.3-2s-.5-1.7-1.3-2z" fill="#fff" fill-opacity=".4"/></svg>'
      '</span></div>')
HI = '<div class="hi"></div>'

def tabs(active):
    t = [('swap','Swap','swap'),('stake','Stake','stake'),('portfolio','Portfolio','portfolio'),('activity','Activity','activity')]
    return '<nav class="tabs">' + ''.join(f'<a class="{"on" if k == active else ""}">{ic(i)}<span>{l}</span></a>' for k, l, i in t) + '</nav>'

def page(name, title, inner):
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=390, initial-scale=1">
<title>Stillwater app · {title}</title><link rel="stylesheet" href="../app.css"></head>
<body><div class="phone">
{inner}
</div></body></html>
"""
    with open(os.path.join(OUT, name + '.html'), 'w') as f: f.write(html)
    return name

def drow(k, v): return f'<div class="drow"><span>{k}</span><span>{v}</span></div>'
def back(label=''): return f'<span class="back">{ic("back")}{label}</span>'
def cbtn(i): return f'<span class="cbtn">{ic(i)}</span>'
def steps(n, total=4):
    segs = ''.join(f'<i style="display:block;height:3px;border-radius:2px;background:{"var(--mist)" if k < n else "var(--graphite)"}"></i>' for k in range(total))
    return f'<div style="display:grid;grid-template-columns:repeat({total},1fr);gap:6px;width:120px">{segs}</div>'
HERO_ART = ('<div class="glow" style="left:-140px;top:-180px;width:680px;height:560px;background:radial-gradient(closest-side,rgba(4,63,150,.75),rgba(6,18,37,.2) 70%,transparent)"></div>'
            '<div class="bar" style="width:420px;left:-140px;top:150px;background:linear-gradient(90deg,transparent,rgba(255,99,99,.75),#ff9a7a 60%,transparent);opacity:.7"></div>'
            '<div class="bar" style="width:420px;right:-170px;top:290px;background:linear-gradient(90deg,transparent,#63a1ff 40%,#143ca3 75%,transparent);opacity:.6"></div>')
CHART = sw.chart_svg(358, 120, 7).replace('id="pg"', 'id="pgm"').replace('url(#pg)', 'url(#pgm)')

frames = []

# 01 splash
frames.append(page('01_splash', 'Splash', f"""{SB}
<div style="position:absolute;inset:0;overflow:hidden">{HERO_ART}<div style="position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(transparent,var(--void))"></div></div>
<div style="position:relative;flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;padding-bottom:40px">{sw.tile(96)}<div style="font-size:30px;font-weight:500;letter-spacing:-.3px">Stillwater</div><div class="ash" style="font-size:15px">Calm swaps. Every cost in plain sight.</div></div>
<div style="position:relative;text-align:center;padding-bottom:46px" class="mono muted"><span style="font-size:11px;letter-spacing:.04em">Demo build · Designed by Olayemi</span></div>
{HI}"""))

def onboard(name, n, art, h, p, last=False):
    dots = ''.join(f'<i style="display:block;width:{18 if k == n else 6}px;height:6px;border-radius:3px;background:{"var(--white)" if k == n else "var(--slate)"}"></i>' for k in range(3))
    btn = 'Get started' if last else 'Continue'
    return page(name, f'Onboarding {n+1}', f"""{SB}
<div style="position:absolute;left:0;right:0;top:0;height:520px;overflow:hidden">{HERO_ART}<div style="position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(transparent,var(--void))"></div></div>
<div class="nav" style="position:relative"><span></span><span class="ash" style="font-size:16px">Skip</span></div>
<div style="position:relative;height:350px;display:flex;align-items:center;justify-content:center;padding:0 28px">{art}</div>
<div style="position:relative;padding:12px 28px 0;display:flex;flex-direction:column;gap:12px"><div style="display:flex;gap:6px">{dots}</div><h1 style="margin:6px 0 0;font-size:32px;line-height:38px;font-weight:600;letter-spacing:-.6px">{h}</h1><p class="ash" style="margin:0;font-size:16px;line-height:23px">{p}</p></div>
<div class="cta"><span class="btn btn-p">{btn}</span><span class="btn btn-t">Explore as guest</span><span class="btn btn-t" style="height:36px;font-size:15px;font-weight:400;color:var(--ash)">I already have an account</span></div>
{HI}""")

glass = 'background:rgba(12,13,15,.78);-webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px);border-radius:20px;box-shadow:var(--key-hi), rgba(0,0,0,.5) 0 30px 60px -20px;width:100%;padding:18px'
frames.append(onboard('02_onboarding_costs', 0, f"""<div style="{glass}"><span class="eyebrow">You receive at least</span><div style="display:flex;align-items:baseline;gap:8px;margin:8px 0 2px"><span class="mono" style="font-size:34px">0.0738</span><span style="font-size:17px;font-weight:500">EDDY</span></div><div class="muted mono" style="font-size:13px;margin-bottom:10px">≈ $248.10 · ₦ 336,900</div>{drow('Network fee', '<span class="mono">$0.42 · ₦ 570</span>')}{drow('Price impact', '<span class="mono ok">0.08%</span>')}{drow('Max slippage', '<span class="mono">0.5% · at most $1.25</span>')}</div>""",
  'See every cost before you sign.', 'Fees, the least you’ll get and what can go wrong, in plain words and in $ or ₦.'))
frames.append(onboard('03_onboarding_approvals', 1, f"""<div style="{glass};display:flex;flex-direction:column;gap:12px"><div style="display:flex;align-items:center;gap:10px">{ti('CMD').replace('class="ti"','class="ti sm"')}<b style="font-weight:500">Allow 250 CMD</b><span class="badge b-ok" style="margin-left:auto">Exact</span></div><div class="well" style="padding:14px;font-size:15px;line-height:22px">This lets Stillwater move up to <b style="font-weight:500">250 CMD</b> from your wallet, once. Nothing else.</div><div class="seg"><span class="on">Exact amount</span><span>Unlimited</span></div></div>""",
  'Approve exactly what’s needed.', 'Stillwater asks for the amount this swap needs, never your whole balance, and says so in one sentence.'))
frames.append(onboard('04_onboarding_risk', 2, f"""<div style="{glass}"><div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">{ti('EDDY').replace('class="ti"','class="ti sm"')}<b style="font-weight:500">Eddy · Flexible</b><span class="badge b-ok" style="margin-left:auto"><span class="dot"></span>Low risk</span></div>{drow('Lock-up', 'None')}{drow('Withdrawal', 'About 1 day')}{drow('What can go wrong', 'Validator penalties')}{drow('APR', '<span class="mono">3.8%</span> <span class="badge b-ex">Example</span>')}</div>""",
  'Risks written on the label.', 'Every pool shows its lock-up, withdrawal time and what can go wrong, before you stake.', last=True))

# 05 sign up
G = sw.G_GLYPH; A = sw.A_GLYPH
frames.append(page('05_signup', 'Sign up', f"""{SB}
<div class="nav">{back()}<span></span><span class="ash" style="font-size:16px">Log in</span></div>
<div class="lt"><h1>Create account</h1></div>
<p class="sub">Start with your email. You’ll get a smart wallet secured by a passkey, no seed phrase needed.</p>
<div class="body" style="gap:12px;padding-top:22px">
  <span class="lbl">Email</span>
  <div class="input focus filled">ada.o@example.com<span class="caret"></span></div>
  <span class="btn btn-p">Continue</span>
  <div class="or" style="margin:6px 0"><span>or</span></div>
  <span class="btn btn-g">{A}Continue with Apple</span>
  <span class="btn btn-g">{G}Continue with Google</span>
  <div class="well" style="display:flex;align-items:center;gap:10px;padding:14px 14px;font-size:14.5px;margin-top:4px">{ic('wallet').replace('<svg','<svg width="20" height="20"',1)}<b style="font-weight:500;white-space:nowrap">Already have a wallet?</b><span class="ash" style="margin-left:auto;white-space:nowrap">Connect wallet</span><span style="color:var(--iron)">{ic('chevr').replace('<svg','<svg width="16" height="16"',1)}</span></div>
  <span class="btn btn-t">Explore as guest</span>
</div>
<p class="muted" style="position:absolute;left:24px;right:24px;bottom:40px;margin:0;font-size:12.5px;line-height:18px;text-align:center">By continuing you agree to the <u class="ash">Terms</u> and <u class="ash">Privacy Policy</u>.</p>
{HI}"""))

# 06 code + iOS number pad
keys = [('1',''),('2','ABC'),('3','DEF'),('4','GHI'),('5','JKL'),('6','MNO'),('7','PQRS'),('8','TUV'),('9','WXYZ'),('',''),('0',''),('del','')]
kp = ''.join(('<span></span>' if k == '' else (f'<span style="display:flex;align-items:center;justify-content:center;color:var(--white)">{isz("del", 26)}</span>' if k == 'del' else
       f'<span style="height:46px;border-radius:8px;background:#2a2b2e;box-shadow:0 1px 0 rgba(0,0,0,.5);display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1"><b style="font-size:25px;font-weight:400">{k}</b><small style="font-size:9.5px;letter-spacing:1.8px;font-weight:600;margin-top:1px">{s}</small></span>')) for k, s in keys)
boxes = ''.join(f'<span class="mono" style="height:58px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:26px;background:{"var(--ink)" if d else "var(--obsidian)"};box-shadow:{"var(--key-hi)" if d else ("rgba(255,255,255,.5) 0 0 0 1px inset,rgba(255,255,255,.06) 0 0 0 4px" if k == 3 else "rgba(255,255,255,.08) 0 0 0 1px inset")}">{d}{"<span class=caret></span>" if k == 3 else ""}</span>' for k, d in enumerate(['4','8','2','','','']))
frames.append(page('06_code', 'Email code', f"""{SB}
<div class="nav">{back()}{steps(1)}<span style="width:36px"></span></div>
<div class="lt"><h1>Enter code</h1></div>
<p class="sub">We sent a 6-digit code to <span style="color:var(--white)">ada.o@example.com</span>. <span style="color:var(--white);text-decoration:underline;text-underline-offset:3px">Change email</span></p>
<div class="body" style="gap:16px;padding-top:22px">
  <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px">{boxes}</div>
  <div style="display:flex;justify-content:space-between;align-items:center;font-size:14px"><span class="muted" style="display:flex;align-items:center;gap:6px">{ic('clock').replace('<svg','<svg width="15" height="15"',1)}Resend code in <span class="mono">0:42</span></span><span class="ash">Paste</span></div>
</div>
<div style="position:absolute;left:0;right:0;bottom:0;background:#18191b;padding:8px 6px 40px;display:grid;grid-template-columns:repeat(3,1fr);gap:7px 6px;border-top:.5px solid rgba(255,255,255,.06)">{kp}</div>
<div style="position:absolute;left:16px;right:16px;bottom:284px"><span class="btn btn-p" style="opacity:.45">Verify</span></div>
{HI}"""))

# 07 passkey
frames.append(page('07_passkey', 'Passkey', f"""{SB}
<div class="nav">{back()}{steps(2)}<span style="width:36px"></span></div>
<div style="display:flex;justify-content:center;padding:26px 0 4px"><div style="position:relative;width:96px;height:96px;border-radius:28px;display:flex;align-items:center;justify-content:center;background:linear-gradient(#1b1c1e,#111214);box-shadow:rgba(255,255,255,.12) 0 1px 0 inset,rgba(0,0,0,.6) 0 -2px 0 inset,rgba(255,255,255,.08) 0 0 0 1px,0 0 0 14px rgba(255,255,255,.025),0 0 0 15px rgba(255,255,255,.05)">{ic('faceid').replace('<svg','<svg width="44" height="44"',1)}</div></div>
<div style="padding:26px 24px 0;text-align:center"><h1 style="margin:0;font-size:30px;line-height:36px;font-weight:600;letter-spacing:-.5px">Create a passkey</h1><p class="ash" style="margin:10px 0 0;font-size:16px;line-height:23px">Your passkey unlocks your Stillwater wallet with Face ID. There’s nothing to write down and nothing to lose.</p></div>
<div class="card" style="margin:24px 16px 0;padding:6px 0">
  <div class="row"><span class="ico">{ic('lock')}</span><div class="grow"><b style="font-size:15px">Stays on this iPhone</b><small>Stillwater never sees your face or fingerprint.</small></div></div>
  <div class="row"><span class="ico">{ic('shield')}</span><div class="grow"><b style="font-size:15px">Can’t be phished</b><small>It only works in Stillwater, not on look-alikes.</small></div></div>
  <div class="row"><span class="ico">{ic('refresh')}</span><div class="grow"><b style="font-size:15px">Backed up</b><small>Synced with your keychain, plus email recovery.</small></div></div>
</div>
<div class="cta"><span class="btn btn-p">{ic('faceid')}Create passkey</span><span class="btn btn-t">Use a seed phrase instead</span></div>
{HI}"""))

# 08 preferences
def opt(t, s, on=False):
    dot = 'inset 0 0 0 6px var(--mist)' if on else 'inset 0 0 0 1.5px var(--iron)'
    return f'<div style="display:flex;align-items:center;gap:12px;padding:13px 14px;border-radius:14px;background:{"var(--obsidian)" if on else "var(--ink)"};box-shadow:{"var(--key-hi)" if on else "var(--key)"}"><span style="width:20px;height:20px;border-radius:50%;flex:none;box-shadow:{dot}"></span><span style="display:flex;flex-direction:column;gap:1px"><b style="font-weight:500;font-size:15px">{t}</b><small class="muted" style="font-size:13px">{s}</small></span></div>'
frames.append(page('08_preferences', 'Preferences', f"""{SB}
<div class="nav">{back()}{steps(3)}<span class="ash" style="font-size:16px">Skip</span></div>
<div class="lt"><h1>Make it yours</h1></div>
<p class="sub">Three quick choices. Change them any time in Settings.</p>
<div class="body" style="gap:10px;padding-top:20px">
  <span class="lbl" style="margin-bottom:0">Show amounts in</span>
  <div class="seg"><span class="on"><span class="mono">$</span> US dollar</span><span><span class="mono">₦</span> Naira</span></div>
  <span class="lbl" style="margin:10px 0 0">Your experience with crypto</span>
  {opt('New to it', 'I’ve never swapped or staked.')}{opt('Some experience', 'I’ve swapped a few times.', True)}{opt('Experienced', 'I sign transactions most weeks.')}
  <span class="lbl" style="margin:10px 0 0">Risk comfort</span>
  <div class="seg"><span>Careful</span><span class="on">Balanced</span><span>Adventurous</span></div>
  <p class="muted" style="margin:2px 2px 0;font-size:13px;line-height:18px">Balanced shows low and medium risk pools first, and asks again before anything high risk.</p>
</div>
<div class="cta"><span class="btn btn-p">Continue</span></div>
{HI}"""))

# 09 home / portfolio
assets = [('CMD','Calm Dollar','820.00','$820.00','<span class="muted">0.00%</span>'),('EDDY','Eddy','0.3120','$312.40','<span class="ok">+3.1%</span>'),('sEDDY','Staked Eddy','0.4000','$132.10','<span class="ok">+3.8% APR</span>'),('SHOL','Shoal','12.50','$20.00','<span class="riskc">−1.2%</span>')]
al = ''.join(f'<div class="row">{ti(s)}<div class="grow"><b>{n}</b><small class="mono">{a} {s}</small></div><div class="end"><span class="mono" style="font-size:15px">{v}</span><small class="mono" style="font-size:12px">{c}</small></div></div>' for s, n, a, v, c in assets)
qa = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:7px;font-size:12px;color:var(--ash)"><span style="width:56px;height:56px;border-radius:18px;display:flex;align-items:center;justify-content:center;background:linear-gradient(#1b1c1e,#111214);box-shadow:rgba(255,255,255,.12) 0 1px 0 inset,rgba(0,0,0,.6) 0 -2px 0 inset,rgba(255,255,255,.08) 0 0 0 1px;color:var(--white)">{isz(i, 22)}</span>{l}</div>' for i, l in [('swap','Swap'),('stake','Stake'),('recv','Receive'),('send','Send')])
frames.append(page('09_portfolio', 'Portfolio', f"""{SB}
<div class="nav"><span class="badge" style="height:30px;border-radius:15px;padding:0 12px 0 4px;gap:7px;background:var(--graphite);box-shadow:var(--key)"><span style="width:22px;height:22px;border-radius:50%;background:var(--obsidian);box-shadow:rgba(255,255,255,.1) 0 0 0 1px inset;color:var(--ash);display:flex;align-items:center;justify-content:center">{isz("user", 13)}</span><span class="mono" style="font-size:12px">{ADDR}</span></span><span class="rgt">{cbtn('bell')}{cbtn('gear')}</span></div>
<div class="lt"><h1>Portfolio</h1><span class="badge b-ex" style="margin-bottom:8px">Example data</span></div>
<div class="body pad" style="gap:16px">
  <div style="padding:0 4px"><div class="mono" style="font-size:40px;line-height:46px;letter-spacing:-.5px">$1,284.50</div><div style="display:flex;gap:10px;align-items:center;font-size:14px;margin-top:2px"><span class="mono ok">+$30.12 (2.4%)</span><span class="muted">past 30 days</span><span class="muted mono" style="margin-left:auto;font-size:12px">₦ 1.74M</span></div></div>
  <div style="height:120px;margin:0 -4px">{CHART}</div>
  <div style="display:flex;justify-content:space-between;padding:0 10px">{qa}</div>
  <div class="card" style="padding:4px 0"><div style="display:flex;justify-content:space-between;padding:12px 16px 4px"><b style="font-weight:500">Assets</b><span class="ash" style="font-size:14px">See all</span></div>{al}</div>
</div>
{tabs('portfolio')}{HI}"""))

# 10 swap
def swap_screen(under=False):
    return f"""{SB}
<div class="nav"><span class="mono muted" style="font-size:12px;display:flex;align-items:center;gap:6px"><span style="width:7px;height:7px;border-radius:50%;background:var(--ok)"></span>Main network</span><span class="rgt">{cbtn('sliders')}</span></div>
<div class="lt"><h1>Swap</h1></div>
<div class="body pad" style="gap:10px">
  <div style="position:relative;display:flex;flex-direction:column;gap:6px">
    <div class="card" style="padding:16px;display:flex;flex-direction:column;gap:10px"><div style="display:flex;justify-content:space-between;font-size:13px"><span class="muted">You pay</span><span class="muted">Balance <span class="mono">820.00</span> · <span style="color:var(--white)">Max</span></span></div><div style="display:flex;align-items:center;justify-content:space-between"><span class="mono" style="font-size:36px;letter-spacing:-.5px">250.00</span><span style="display:flex;align-items:center;gap:8px;height:38px;padding:0 10px 0 5px;border-radius:19px;box-shadow:var(--key-hi);background:var(--graphite);font-weight:500">{ti('CMD').replace('class="ti"','class="ti sm"')}CMD{ic('chev').replace('<svg','<svg width="14" height="14"',1)}</span></div><span class="mono muted" style="font-size:13px">≈ $250.00 · ₦ 339,500</span></div>
    <span style="position:absolute;left:50%;top:50%;margin:-20px 0 0 -20px;width:40px;height:40px;border-radius:12px;background:var(--obsidian);box-shadow:var(--key-hi),0 0 0 5px var(--void);display:flex;align-items:center;justify-content:center;z-index:2">{ic('down').replace('<svg','<svg width="18" height="18"',1)}</span>
    <div class="card" style="padding:16px;display:flex;flex-direction:column;gap:10px"><div style="display:flex;justify-content:space-between;font-size:13px"><span class="muted">You receive</span><span class="muted">Balance <span class="mono">0.3120</span></span></div><div style="display:flex;align-items:center;justify-content:space-between"><span class="mono" style="font-size:36px;letter-spacing:-.5px">0.0742</span><span style="display:flex;align-items:center;gap:8px;height:38px;padding:0 10px 0 5px;border-radius:19px;box-shadow:var(--key-hi);background:var(--graphite);font-weight:500">{ti('EDDY').replace('class="ti"','class="ti sm"')}EDDY{ic('chev').replace('<svg','<svg width="14" height="14"',1)}</span></div><span class="mono muted" style="font-size:13px">≈ $249.30 · ₦ 338,550</span></div>
  </div>
  <div class="well" style="padding:6px 14px">{drow('Rate', '<span class="mono">1 EDDY = 3,369.27 CMD</span>')}{drow('You receive at least', '<span class="mono">0.0738 EDDY</span>')}{drow('Network fee', '<span class="mono">$0.42 · ₦ 570</span>')}{drow('Price impact', '<span class="mono ok">0.08%</span>')}</div>
  <span class="btn btn-p" style="margin-top:4px">Review swap</span>
  <p class="muted" style="margin:0;text-align:center;font-size:12.5px">Quote refreshes every 15s · <span class="mono">Example data</span></p>
</div>
{tabs('swap')}"""
frames.append(page('10_swap', 'Swap', swap_screen() + HI))

# 11 token select sheet
toks = [('CMD','Calm Dollar','820.00','$820.00',True),('EDDY','Eddy','0.3120','$312.40',True),('SHOL','Shoal','12.50','$20.00',True),('KELP','Kelp','0','$0.00',True)]
tl = ''.join(f'<div class="row" style="padding:10px 4px">{ti(s)}<div class="grow"><b style="display:flex;align-items:center;gap:6px">{s}<span style="color:var(--ash)">{isz("check", 14)}</span></b><small>{n}</small></div><div class="end"><span class="mono" style="font-size:15px">{a}</span><small class="mono">{v}</small></div></div>' for s, n, a, v, ok in toks)
frames.append(page('11_token_select', 'Token select sheet', f"""<div class="under">{swap_screen()}</div><div class="dim"></div>
<div class="sheet" style="top:62px">{SB.replace('class="sb"','class="sb" style="display:none"')}<div class="grab"></div>
<div class="sh-head"><h2>Select token</h2>{cbtn('x')}</div>
<div class="sh-body">
  <div class="input" style="height:44px;border-radius:12px;gap:10px;font-size:16px">{ic('search').replace('<svg','<svg width="18" height="18"',1)}Search name or paste address</div>
  <div style="display:flex;gap:8px">{''.join(f'<span style="display:flex;align-items:center;gap:6px;height:34px;padding:0 12px 0 5px;border-radius:17px;box-shadow:var(--key);font-size:14px;font-weight:500">{ti(s).replace(chr(99)+"lass="+chr(34)+"ti"+chr(34), chr(99)+"lass="+chr(34)+"ti sm"+chr(34))}{s}</span>' for s in ['CMD','EDDY','SHOL'])}</div>
  <div class="eyebrow" style="margin-top:6px">Your tokens</div>
  <div class="list">{tl}</div>
  <div class="eyebrow" style="margin-top:2px">Search result</div>
  <div class="row" style="padding:10px 12px;border-radius:14px;background:rgba(242,181,82,.06);box-shadow:inset 0 0 0 1px rgba(242,181,82,.18)">{ti('MRSH')}<div class="grow"><b style="display:flex;align-items:center;gap:8px">MRSH <span class="badge b-warn" style="height:20px;font-size:11px">{ic('alert').replace('<svg','<svg width="12" height="12"',1)}Unverified</span></b><small>Not on any verified list. Check the address before you trade.</small></div></div>
</div>
</div>{HI}"""))

# 12 review sheet
frames.append(page('12_review', 'Review sheet', f"""<div class="under">{swap_screen()}</div><div class="dim"></div>
<div class="sheet" style="top:108px"><div class="grab"></div>
<div class="sh-head"><h2>Review swap</h2>{cbtn('x')}</div>
<div class="sh-body" style="gap:14px">
  <div style="padding:2px 2px 0"><span class="eyebrow">You receive at least</span><div style="display:flex;align-items:baseline;gap:8px;margin-top:6px">{ti('EDDY').replace('class="ti"','class="ti sm"')}<span class="mono" style="font-size:34px;letter-spacing:-.4px">0.0738</span><span style="font-size:17px;font-weight:500">EDDY</span></div><div class="mono muted" style="font-size:13px;margin-top:2px">for 250.00 CMD · ≈ $248.10 · ₦ 336,900</div></div>
  <div class="well" style="padding:4px 14px">{drow('Network fee', '<span class="mono">$0.42 · ₦ 570</span>')}{drow('Price impact', '<span class="mono ok">0.08%</span>')}{drow('Max slippage', '<span class="mono">0.5% · at most $1.25</span>')}{drow('Route', 'CMD → EDDY, 1 pool')}</div>
  <div class="card" style="padding:14px 16px;display:flex;gap:12px"><span class="ico" style="width:32px;height:32px">{ic('shield').replace('<svg','<svg width="16" height="16"',1)}</span><div style="font-size:14.5px;line-height:21px"><b style="font-weight:500;display:block;margin-bottom:2px">What you’re signing</b><span class="ash">Step 1 lets Stillwater move up to <span style="color:var(--white)">250 CMD</span> from your wallet, once. Nothing else.</span></div></div>
  <div style="display:flex;align-items:center;gap:10px;font-size:14px"><span style="width:24px;height:24px;border-radius:50%;background:var(--mist);color:#1b1c1e;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600" class="mono">1</span><span>Approve CMD</span><span style="flex:1;height:1px;background:var(--line)"></span><span style="width:24px;height:24px;border-radius:50%;box-shadow:inset 0 0 0 1px var(--slate);color:var(--ash);display:flex;align-items:center;justify-content:center;font-size:12px" class="mono">2</span><span class="ash">Swap</span></div>
</div>
<div style="padding:18px 16px 40px;margin-top:auto"><span class="btn btn-p">{ic('faceid')}Approve 250 CMD</span></div>
</div>{HI}"""))

# 13 success
frames.append(page('13_success', 'Success', f"""{SB}
<div style="position:absolute;left:0;right:0;top:0;height:460px;overflow:hidden;opacity:.55">{HERO_ART}<div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(transparent,var(--void))"></div></div>
<div class="nav" style="position:relative"><span></span>{cbtn('x')}</div>
<div style="position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;padding:56px 24px 0;gap:10px">
  <span style="width:76px;height:76px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(89,212,153,.12);box-shadow:inset 0 0 0 1px rgba(89,212,153,.3);color:var(--ok)">{ic('check').replace('<svg','<svg width="36" height="36"',1)}</span>
  <h1 style="margin:14px 0 0;font-size:30px;line-height:36px;font-weight:600;letter-spacing:-.5px">Swap complete</h1>
  <p class="ash" style="margin:0;font-size:16px">You received <span class="mono" style="color:var(--white)">0.0741 EDDY</span></p>
</div>
<div class="card" style="position:relative;margin:30px 16px 0;padding:6px 16px">
  {drow('Paid', '<span class="mono">250.00 CMD</span>')}{drow('Received', '<span class="mono">0.0741 EDDY</span>')}{drow('Better than minimum by', '<span class="mono ok">0.0003 EDDY</span>')}{drow('Network fee', '<span class="mono">$0.39 · ₦ 530</span>')}{drow('Transaction', '<span class="mono" style="display:flex;align-items:center;gap:6px">0x91c4…7a2e' + ic('ext').replace('<svg','<svg width="13" height="13"',1) + '</span>')}
</div>
<div class="cta"><span class="btn btn-p">Stake your EDDY</span><span class="btn btn-t">Done</span></div>
{HI}"""))

# 14 stake pools
def risk(r):
    c = {'Low':'b-ok','Medium':'b-warn','High':'b-risk'}[r]
    return f'<span class="badge {c}"><span class="dot"></span>{r} risk</span>'
pools = [('EDDY','Eddy · Flexible','3.8%','None','About 1 day','Low'),('SHOL','Shoal · 30 days','6.1%','30 days','2 days','Medium'),('KELP','Kelp · 90 days','9.4%','90 days','7 days','High')]
pl = ''.join(f'<div class="card" style="padding:16px;display:flex;flex-direction:column;gap:12px"><div style="display:flex;align-items:center;gap:12px">{ti(s)}<div style="flex:1;display:flex;flex-direction:column;gap:1px"><b style="font-weight:500">{n}</b><small class="muted" style="font-size:13px">Stake {s}</small></div>{risk(r)}</div><div style="display:flex;align-items:flex-end;justify-content:space-between"><span class="mono" style="font-size:30px;line-height:1">{a}</span><span class="badge b-ex">Example APR</span></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:13px"><span class="muted">Lock-up <span style="color:var(--white)">{l}</span></span><span class="muted">Withdrawal <span style="color:var(--white)">{w}</span></span></div></div>' for s, n, a, l, w, r in pools)
frames.append(page('14_stake_pools', 'Stake pools', f"""{SB}
<div class="nav"><span></span><span class="rgt">{cbtn('info')}</span></div>
<div class="lt"><h1>Stake</h1><span class="badge b-ex" style="margin-bottom:8px">Illustrative yields</span></div>
<div class="body pad" style="gap:12px">
  <div class="card" style="padding:14px 16px;display:flex;justify-content:space-between;align-items:center"><div style="display:flex;flex-direction:column;gap:2px"><span class="muted" style="font-size:13px">You’re staking</span><span class="mono" style="font-size:20px">$132.10</span></div><div style="display:flex;flex-direction:column;gap:2px;align-items:flex-end"><span class="muted" style="font-size:13px">Rewards to claim</span><span class="mono ok" style="font-size:16px">0.0213 EDDY</span></div></div>
  <div class="seg"><span class="on">All</span><span>Low risk</span><span>Flexible</span></div>
  {pl}
</div>
{tabs('stake')}{HI}"""))

# 15 stake detail
frames.append(page('15_stake_detail', 'Stake detail', f"""{SB}
<div class="nav">{back('Stake')}<span class="ttl">Stake EDDY</span><span style="width:60px"></span></div>
<div class="body" style="gap:14px;padding-top:18px">
  <div class="card" style="padding:18px 16px;display:flex;flex-direction:column;gap:12px;align-items:center;text-align:center"><span class="muted" style="font-size:13px">Amount to stake</span><div style="display:flex;align-items:baseline;gap:8px"><span class="mono" style="font-size:44px;letter-spacing:-.6px">0.20</span><span style="font-size:18px;font-weight:500">EDDY</span></div><span class="mono muted" style="font-size:13px">≈ $66.05 · ₦ 89,700 · Balance 0.3120</span><div style="display:flex;gap:8px">{''.join(f'<span style="height:32px;padding:0 14px;border-radius:16px;display:flex;align-items:center;font-size:13px;font-weight:500;box-shadow:var(--key);{"background:var(--graphite)" if k=="50%" else ""}">{k}</span>' for k in ['25%','50%','75%','Max'])}</div></div>
  <div class="card" style="padding:14px 16px"><div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px"><b style="font-weight:500">Risk label</b>{risk('Low')}</div>{drow('Lock-up', 'None')}{drow('Withdrawal', 'About 1 day')}{drow('What can go wrong', 'Validator penalties')}{drow('Price', 'EDDY can lose value')}</div>
  <div class="well" style="padding:4px 14px">{drow('APR', '<span><span class="mono">3.8%</span> <span class="badge b-ex">Example</span></span>')}{drow('Estimated per year', '<span class="mono">≈ 0.0076 EDDY</span>')}{drow('Network fee', '<span class="mono">$0.21 · ₦ 285</span>')}</div>
</div>
<div class="cta"><span class="btn btn-p">Review stake</span></div>
{HI}"""))

# 16 activity
acts = [('Today', [('swap','Swapped CMD → EDDY','250.00 CMD → 0.0741 EDDY','Confirmed','ok','9:38'),('check','Approved CMD','Exactly 250 CMD, once','Confirmed','ok','9:37')]),
        ('Yesterday', [('stake','Staked EDDY','0.40 EDDY · Flexible pool','Confirmed','ok','18:12'),('gift','Claimed rewards','0.0049 EDDY','Confirmed','ok','18:10'),('alert','Swap didn’t go through','Price moved past your limit. Only gas spent: $0.31','Retry','warn','11:02')]),
        ('Oct 9', [('recv','Received CMD','From 0x22b1…08fd','Confirmed','ok','14:45')])]
ab = ''
for day, items in acts:
    rows = ''.join(f'<div class="row" style="align-items:flex-start"><span class="ico" style="{"color:var(--warn);background:rgba(242,181,82,.1)" if st=="warn" else ""}">{ic(i)}</span><div class="grow"><b style="font-size:15px">{t}</b><small style="line-height:17px">{s}</small></div><div class="end"><small class="mono" style="font-size:12px">{tm}</small>{"<span class=" + chr(34) + "badge b-warn" + chr(34) + " style=" + chr(34) + "height:22px" + chr(34) + ">Retry</span>" if st=="warn" else ""}</div></div>' for i, t, s, lab, st, tm in items)
    ab += f'<div class="sect">{day}</div><div class="card" style="padding:2px 0">{rows}</div>'
frames.append(page('16_activity', 'Activity', f"""{SB}
<div class="nav"><span></span><span class="rgt">{cbtn('search')}</span></div>
<div class="lt"><h1>Activity</h1></div>
<div class="body pad" style="gap:12px">
  <div class="seg"><span class="on">All</span><span>Swaps</span><span>Stakes</span><span>Approvals</span></div>
  {ab}
</div>
{tabs('activity')}{HI}"""))

# 17 connect wallet sheet
empty_home = f"""{SB}
<div class="nav"><span></span><span class="rgt">{cbtn('gear')}</span></div>
<div class="lt"><h1>Portfolio</h1></div>
<div class="body pad" style="align-items:center;justify-content:center;text-align:center;gap:12px"><span class="ico" style="width:64px;height:64px">{ic('wallet').replace('<svg','<svg width="28" height="28"',1)}</span><b style="font-size:20px;font-weight:600">No wallet connected</b><span class="ash">Connect a wallet to see your balances.</span></div>
{tabs('portfolio')}"""
wl = [('Stillwater smart wallet','Secured by passkey','Recommended', sw.tile(36)),
      ('Browser or mobile wallet','Any wallet on this device','', '<span class="ico">' + ic('browser') + '</span>'),
      ('Scan with another wallet','Show a QR code to connect','', '<span class="ico">' + ic('qr') + '</span>'),
      ('Hardware wallet','Connect over Bluetooth','', '<span class="ico">' + ic('chip') + '</span>')]
wr = ''.join(f'<div class="row" style="padding:14px 16px">{g}<div class="grow"><b style="font-size:15.5px">{t}</b><small style="display:flex;align-items:center;gap:8px">{s}{"<span class=" + chr(34) + "badge b-ok" + chr(34) + " style=" + chr(34) + "height:18px;font-size:10.5px;padding:0 6px" + chr(34) + ">" + b + "</span>" if b else ""}</small></div><span class="chev">{ic("chevr")}</span></div>' for t, s, b, g in wl)
frames.append(page('17_connect_wallet', 'Connect wallet sheet', f"""<div class="under">{empty_home}</div><div class="dim"></div>
<div class="sheet" style="top:300px"><div class="grab"></div>
<div class="sh-head"><h2>Connect a wallet</h2>{cbtn('x')}</div>
<div class="sh-body" style="gap:14px">
  <div class="card" style="padding:2px 0">{wr}</div>
  <p class="muted" style="margin:0 4px;font-size:13px;line-height:19px;display:flex;gap:8px">{ic('lock').replace('<svg','<svg width="15" height="15" style="flex:none;margin-top:2px"',1)}Stillwater never asks for your seed phrase. Connecting only shares your public address.</p>
</div>
</div>{HI}"""))

# 18 settings
def srow(i, t, v='', tog=None, chev=True):
    end = (f'<span class="tog{" on" if tog else ""}"></span>' if tog is not None else f'<span class="ash" style="font-size:15px">{v}</span>' + (f'<span class="chev">{ic("chevr")}</span>' if chev else ''))
    return f'<div class="row" style="min-height:46px;padding:7px 16px"><span class="ico" style="width:30px;height:30px;border-radius:8px">{isz(i, 16)}</span><div class="grow"><b style="font-size:15.5px;font-weight:400">{t}</b></div>{end}</div>'
frames.append(page('18_settings', 'Settings', f"""{SB}
<div class="nav">{back('Portfolio')}<span></span><span></span></div>
<div class="lt"><h1>Settings</h1></div>
<div class="body pad" style="gap:10px;padding-top:12px">
  <div class="card" style="padding:12px 16px;display:flex;align-items:center;gap:12px"><span style="width:44px;height:44px;border-radius:50%;background:var(--graphite);box-shadow:rgba(255,255,255,.1) 0 0 0 1px inset;color:var(--mist);display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:600;letter-spacing:-.2px;flex:none">AO</span><div style="flex:1;display:flex;flex-direction:column;gap:2px"><b style="font-weight:500">Ada O.</b><small class="muted mono" style="font-size:12px">ada.o@example.com · {ADDR}</small></div><span class="chev" style="width:16px;color:var(--iron)">{ic('chevr')}</span></div>
  <div class="sect">Preferences</div>
  <div class="card" style="padding:2px 0">{srow('globe','Display currency','$ US dollar')}{srow('user','Experience','Some')}{srow('activity','Risk comfort','Balanced')}</div>
  <div class="sect">Security</div>
  <div class="card" style="padding:2px 0">{srow('key','Passkey','This iPhone')}{srow('shield','Approvals','3 active')}{srow('faceid','Face ID for every signature', tog=True)}</div>
  <div class="card" style="padding:2px 0">{srow('info','About Stillwater','v0.1')}<div class="row" style="min-height:46px;padding:7px 16px;justify-content:center"><span class="riskc" style="font-size:15.5px">Log out</span></div></div>
  <p class="mono muted" style="margin:0;text-align:center;font-size:11px">Demo build · Designed by Olayemi</p>
</div>
{tabs('portfolio')}{HI}"""))

print(len(frames), 'frames')
