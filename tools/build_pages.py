#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las páginas interiores del sitio de Roque General Construction LLC.
El resultado es HTML estático (la web no depende de este script para funcionar).
Uso:  python tools/build_pages.py   (desde la raíz del proyecto)
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://roquegeneralconstruction.com"

# ----------------------------------------------------------------------------
# Bloques compartidos
# ----------------------------------------------------------------------------

TOPBAR = """  <div class="topbar">
    <div class="container topbar__row">
      <span>📍 Bend, OR — Serving Central Oregon</span>
      <span class="sep" aria-hidden="true">|</span>
      <span>Licensed · Bonded · Insured</span>
    </div>
  </div>
"""

def header(active=""):
    """active: home|about|services|gallery|contact"""
    def cur(key):
        return ' aria-current="page"' if key == active else ""
    return f"""  <header class="site-header">
    <div class="container header__row">
      <a class="brand" href="/">
        <img src="/img/logo-wide.png" alt="RGC — Roque General Construction LLC logo" width="243" height="186">
        <span class="brand__name">
          <b>Roque</b>
          <span>General Construction LLC</span>
        </span>
      </a>
      <nav class="main-nav" aria-label="Main navigation">
        <ul>
          <li><a href="/"{cur("home")}>Home</a></li>
          <li><a href="/about"{cur("about")}>About</a></li>
          <li>
            <details class="nav-item">
              <summary aria-label="Services menu">Services ▾</summary>
              <div class="nav-drop">
                <a href="/services/siding"><span class="n">01</span> Siding</a>
                <a href="/services/framing"><span class="n">02</span> Framing</a>
                <a href="/services/roofing-repairs"><span class="n">03</span> Roofing Repairs</a>
                <a href="/services/demolition"><span class="n">04</span> Demolition</a>
                <a href="/services/junk-removal"><span class="n">05</span> Junk Removal</a>
                <a href="/services"><span class="n">→</span> All services</a>
              </div>
            </details>
          </li>
          <li><a href="/gallery"{cur("gallery")}>Gallery</a></li>
        </ul>
      </nav>
      <div class="header__cta">
        <a class="header__phone" href="tel:+15414100664">
          <small>Call anytime</small>
          <b>(541) 410-0664</b>
        </a>
        <a class="btn btn--primary" href="/contact">Free Estimate</a>
      </div>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span></button>
    </div>
  </header>
"""

DRAWER = """  <div class="drawer" id="drawer" aria-hidden="true">
    <div class="drawer__scrim"></div>
    <aside class="drawer__panel" role="dialog" aria-modal="true" aria-label="Menu">
      <div class="drawer__head">
        <img src="/img/logo-wide.png" alt="RGC — Roque General Construction LLC" width="145" height="111">
        <button class="drawer__close" aria-label="Close menu">×</button>
      </div>
      <nav aria-label="Mobile navigation">
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li>
            <details>
              <summary>Services <span class="chev">▾</span></summary>
              <ul>
                <li><a href="/services/siding">Siding</a></li>
                <li><a href="/services/framing">Framing</a></li>
                <li><a href="/services/roofing-repairs">Roofing Repairs</a></li>
                <li><a href="/services/demolition">Demolition</a></li>
                <li><a href="/services/junk-removal">Junk Removal</a></li>
                <li><a href="/services">All services</a></li>
              </ul>
            </details>
          </li>
          <li><a href="/gallery">Gallery</a></li>
        </ul>
      </nav>
      <div class="drawer__cta">
        <a class="btn btn--primary" href="/contact">Get a Free Estimate</a>
        <a class="btn btn--ghost" href="tel:+15414100664">📞 (541) 410-0664</a>
        <p class="drawer__meta">Bend, OR · Mon–Fri 7am–6pm, Sat 8am–2pm<br>Licensed · Bonded · Insured</p>
      </div>
    </aside>
  </div>
"""

FOOTER = """  <footer class="site-footer">
    <div class="container">
      <div class="footer__grid">
        <div class="footer__brand">
          <img src="/img/logo-wide.png" alt="RGC — Roque General Construction LLC" loading="lazy" width="200" height="150">
          <p>One crew for siding, framing, roofing repairs, demolition and junk removal. Licensed, bonded &amp; insured — proud to call Central Oregon home. <em>Se habla español.</em></p>
        </div>
        <div class="footer__col">
          <h4>Explore</h4>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/services">Services</a></li>
            <li><a href="/gallery">Gallery</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </div>
        <div class="footer__col">
          <h4>Services</h4>
          <ul>
            <li><a href="/services/siding">Siding</a></li>
            <li><a href="/services/framing">Framing</a></li>
            <li><a href="/services/roofing-repairs">Roofing Repairs</a></li>
            <li><a href="/services/demolition">Demolition</a></li>
            <li><a href="/services/junk-removal">Junk Removal</a></li>
          </ul>
        </div>
        <div class="footer__col">
          <h4>Contact</h4>
          <p class="f-line"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.4 2.1L8.1 10a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.6 2z"/></svg><a href="tel:+15414100664">(541) 410-0664</a></p>
          <p class="f-line"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.4 2.1L8.1 10a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.6 2z"/></svg><a href="tel:+15414101136">(541) 410-1136</a></p>
          <p class="f-line"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg><a href="mailto:marioroque@yahoo.com">marioroque@yahoo.com</a></p>
          <p class="f-line"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg><span style="color:#fff;font-weight:700">Bend, Oregon</span></p>
        </div>
      </div>
      <div class="footer-legal">
        <span>© <span data-year>2026</span> Roque General Construction LLC. All rights reserved.</span>
        <span class="ccb">Licensed · Bonded · Insured — Oregon CCB</span>
        <span><a href="/sitemap.xml">Sitemap</a></span>
      </div>
    </div>
  </footer>

  <div class="mobile-cta">
    <a href="tel:+15414100664">📞 Call Now</a>
    <a href="/contact">Free Estimate →</a>
  </div>

  <button class="back-top" aria-label="Back to top">↑</button>
"""

CHECK_SVG = '<svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M6.5 12.5 2 8l1.4-1.4 3.1 3.1L13.6 2.7 15 4.1z"/></svg>'

def page(title, desc, canonical_path, active, main, jsonld, robots="index, follow, max-image-preview:large", ogimage=True):
    og_extra = ""
    if ogimage:
        og_extra = f"""
  <meta property="og:image" content="{BASE}/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="RGC — Roque General Construction LLC logo on black with red geometric shapes">
  <meta name="twitter:image" content="{BASE}/og-image.jpg">"""
    noindex = f'\n  <meta name="robots" content="{robots}"'
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{BASE}{canonical_path}">{noindex}>
  <meta name="geo.region" content="US-OR">
  <meta name="geo.placename" content="Bend, Oregon">
  <meta name="geo.position" content="44.0582;-121.3153">
  <meta name="ICBM" content="44.0582, -121.3153">
  <meta name="theme-color" content="#0a0a0c">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Roque General Construction LLC">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{BASE}{canonical_path}">
  <meta property="og:locale" content="en_US">{og_extra}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/img/icons/favicon-32x32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/img/icons/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/styles.css?v=3">
  <script type="application/ld+json">
{json.dumps(jsonld, indent=2, ensure_ascii=False)}
  </script>
  <script src="/js/main.js?v=3" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>

{TOPBAR}
{header(active)}
{DRAWER}

  <main id="main">
{main}
  </main>

{FOOTER}</body>
</html>
"""

def breadcrumb(crumbs):
    """crumbs: list of (name, url|None)"""
    items = []
    for name, url in crumbs:
        if url:
            items.append(f'<li><a href="{url}">{name}</a></li>')
        else:
            items.append(f'<li><span aria-current="page">{name}</span></li>')
    return '<ul class="breadcrumb">' + "".join(items) + "</ul>"

def faq_html(qas):
    out = ['<div class="faq">']
    for q, a in qas:
        out.append(f"""          <details>
            <summary>{q} <span class="chev" aria-hidden="true">+</span></summary>
            <div class="faq__a"><p>{a}</p></div>
          </details>""")
    out.append("</div>")
    return "\n".join(out)

def faq_schema(crumbs_url, qas):
    return {
        "@type": "FAQPage",
        "@id": f"{BASE}{crumbs_url}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qas
        ],
    }

def breadcrumbs_schema(crumbs):
    items = []
    for i, (name, url) in enumerate(crumbs, start=1):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": f"{BASE}{url}"})
    return {"@type": "BreadcrumbList", "itemListElement": items}

def service_schema(name, desc, url_path):
    return {
        "@type": "Service",
        "@id": f"{BASE}{url_path}#service",
        "serviceType": name,
        "name": f"{name} in Bend & Central Oregon",
        "description": desc,
        "provider": {"@id": f"{BASE}/#business"},
        "areaServed": [
            {"@type": "City", "name": "Bend, OR"},
            {"@type": "City", "name": "Redmond, OR"},
            {"@type": "City", "name": "Sisters, OR"},
            {"@type": "City", "name": "Prineville, OR"},
            {"@type": "City", "name": "La Pine, OR"},
            {"@type": "City", "name": "Madras, OR"},
        ],
    }

CTA_BAND = """    <section class="cta-band">
      <div class="cta-band__bg" aria-hidden="true">
        <img src="/img/photos/bend-lake.webp" alt="" loading="lazy" width="1600" height="1067">
      </div>
      <div class="container">
        <p class="eyebrow" style="color:var(--red-bright)">Ready when you are</p>
        <h2>Tell us what you need. We'll make it simple.</h2>
        <p>Free, itemized estimates — usually within 48 hours. One call covers siding, framing, roofing repairs, demolition and junk removal.</p>
        <div class="cta-band__actions">
          <a class="btn btn--primary" href="/contact">Get My Free Estimate <span class="btn-arrow">→</span></a>
          <a class="btn btn--ghost" href="tel:+15414100664">📞 (541) 410-0664</a>
        </div>
      </div>
    </section>"""

def service_page(cfg):
    """cfg: dict with slug, name, title, desc, hero_img, hero_alt, hero_w, hero_h,
    intro, includes, why, local, prices, faq, related, photo2"""
    crumbs = [("Home", "/"), ("Services", "/services"), (cfg["name"], None)]
    main = f"""    <section class="page-hero">
      <div class="container page-hero__inner">
        {breadcrumb(crumbs)}
        <h1>{cfg["h1"]}</h1>
        <p class="lead">{cfg["lead"]}</p>
        <div class="page-hero__img">
          <img src="/img/photos/{cfg["hero_img"]}" alt="{cfg["hero_alt"]}" fetchpriority="high" width="{cfg["hero_w"]}" height="{cfg["hero_h"]}">
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container content-block">
        <p class="eyebrow">The service</p>
        <h2 class="headline-mark">What's included</h2>
        {cfg["intro"]}
        <div class="feature-cards">
"""
    ICONS = [
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14.7 6.3a5 5 0 0 0-6.9 6.1L2 18l4 4 5.6-5.8a5 5 0 0 0 6.1-6.9L14 13l-3-3 3.7-3.7z"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3z"/><path d="M9 12l2 2 4-4"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9 17 7M7 17l-2.1 2.1"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2s6 6.6 6 11a6 6 0 1 1-12 0c0-4.4 6-11 6-11z"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M1 5h13v11H1zM14 9h4l4 4v3h-8z"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="19" r="2"/></svg>',
    ]
    for i, inc in enumerate(cfg["includes"]):
        main += f"""          <div class="feature-card">
            <span class="fc-icon">{ICONS[i % len(ICONS)]}</span>
            <h3>{inc[0]}</h3>
            <p>{inc[1]}</p>
          </div>
"""
    main += f"""        </div>
        <div class="info-banner">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v5M12 16.5v.5"/></svg>
          <p><b>Central Oregon note:</b> {cfg["local"]}</p>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container split split--rev">
        <div class="split__media reveal">
          <img src="/img/photos/{cfg["photo2"]["img"]}" alt="{cfg["photo2"]["alt"]}" loading="lazy" width="{cfg["photo2"]["w"]}" height="{cfg["photo2"]["h"]}">
          <span class="plate plate-float">RGC standard</span>
        </div>
        <div class="reveal reveal-d1">
          <p class="eyebrow">Why us</p>
          <h2 class="headline-mark">Why homeowners pick RGC for {cfg["name"].lower()}</h2>
          <ul class="checklist">
"""
    for why in cfg["why"]:
        main += f"""            <li>{CHECK_SVG}<span><b>{why[0]}</b> <span>{why[1]}</span></span></li>
"""
    main += f"""          </ul>
          <a class="btn btn--primary" href="/contact">Get a free {cfg["name"].lower()} quote <span class="btn-arrow">→</span></a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <p class="eyebrow">Ballpark</p>
        <h2 class="headline-mark">What does {cfg["name"].lower()} cost?</h2>
        <p class="lead" style="margin-bottom:1.4rem">Every project is quoted individually after we see the scope — but here are honest ranges to orient you. Your written estimate is free and itemized.</p>
        <div class="price-hint">
"""
    for label, price, note in cfg["prices"]:
        main += f"""          <div class="ph reveal"><span>{label}</span><b>{price}</b><p style="margin:.4rem 0 0">{note}</p></div>
"""
    main += f"""        </div>
        <p class="form-note">Ranges reflect typical Central Oregon projects and materials; final pricing depends on size, access, materials and site conditions.</p>
      </div>
    </section>

    <section class="section section--paper2">
      <div class="container">
        <p class="eyebrow">FAQ</p>
        <h2 class="headline-mark">{cfg["name"]} questions</h2>
{faq_html(cfg["faq"])}
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <p class="eyebrow">Keep exploring</p>
        <h2 style="font-size:clamp(1.5rem,2.6vw,2rem)">Related services</h2>
        <div class="area-chips">
"""
    for rel_name, rel_url in cfg["related"]:
        main += f'          <a class="chip" href="{rel_url}" style="text-decoration:none">{rel_name} →</a>\n'
    main += f"""        </div>
      </div>
    </section>

{CTA_BAND}"""

    graph = [
        {"@id": f"{BASE}/#business"},
        {
            "@type": "WebPage",
            "@id": f"{BASE}{cfg['url']}#webpage",
            "url": f"{BASE}{cfg['url']}",
            "name": cfg["title"],
            "isPartOf": {"@id": f"{BASE}/#website"},
            "about": {"@id": f"{BASE}/#business"},
            "inLanguage": "en-US",
        },
        service_schema(cfg["schema_name"], cfg["desc"], cfg["url"]),
        breadcrumbs_schema(crumbs),
        faq_schema(cfg["url"], cfg["faq"]),
    ]
    return page(
        cfg["title"], cfg["desc"], cfg["url"], "services", main,
        {"@context": "https://schema.org", "@graph": graph},
    )

# ----------------------------------------------------------------------------
# Contenido de páginas
# ----------------------------------------------------------------------------

SERVICES_DATA = [
    {
        "slug": "siding", "name": "Siding", "url": "/services/siding",
        "title": "Siding Installation & Repair in Bend, OR | Roque GC",
        "desc": "Fiber cement, vinyl & wood siding installed and repaired in Bend & Central Oregon. Built for High Desert sun, wind & snow. Free estimates: (541) 410-0664.",
        "h1": "Siding Installation &amp; Repair Built for Central Oregon",
        "lead": "Your siding is your home's armor against High Desert sun, wind, snow and wildfire season. We install and repair fiber cement, vinyl and wood siding with the detail work — flashing, sealing, trim — that makes it last.",
        "hero_img": "siding-house.webp", "hero_alt": "Home with newly installed blue fiber cement siding, crisp trim and a fresh dark shingle roof", "hero_w": 1600, "hero_h": 1200,
        "intro": """<p>Siding does two jobs at once: it defines how your home looks from the street, and it takes the beating so your walls don't. In Central Oregon that beating is real — summer UV at 3,000+ feet, sub-zero snaps, wind-driven snow and decades of freeze-thaw.</p>
        <p>We install complete siding systems and surgically repair failing ones. That means correct house wrap and flashing, panels fastened to manufacturer spec (important for your warranty), and trim details that move with the seasons instead of cracking against them.</p>""",
        "includes": [
            ("Full re-sides", "Complete tear-off and replacement in fiber cement, vinyl or wood — house wrap, flashing and trim included."),
            ("Siding repair", "Cracked, warped, loose or storm-damaged panels matched and replaced without replacing the whole wall."),
            ("Trim, soffit & fascia", "The details that finish the envelope and keep water out of the structure."),
            ("Weatherproofing", "House wrap, sealing and flashing done to spec — the invisible work that prevents the expensive callbacks."),
            ("Storm & UV damage", "Central Oregon sun and wind punish south and west walls first; we restore them before rot sets in."),
            ("Prep for painting or sale", "Siding repairs and replacements that get a home market-ready fast."),
        ],
        "local": "At this elevation, UV breaks down cheaper vinyl in a few years and freeze-thaw finds every unsealed gap. We spec materials and fastening for High Desert conditions — and we'll tell you honestly when a repair beats a re-side.",
        "photo2": {"img": "siding-detail.webp", "alt": "Close-up of new fiber cement siding and crisp corner trim on a finished wall", "w": 920, "h": 780},
        "why": [
            ("Honest repair-vs-replace advice", "We won't sell you a full re-side when two days of targeted repair solves it."),
            ("Manufacturer-spec installation", "Correct fastening and clearance protect both the material and your warranty."),
            ("One crew for the whole envelope", "Siding, trim, roofing repairs and haul-off coordinated by the same team."),
            ("Clean sites, protected landscaping", "Tarps, magnet sweeps for nails and a full cleanup at the end."),
        ],
        "prices": [
            ("Targeted repair", "$300 – $2,500", "Replacing damaged panels, sealing and repainting repaired areas."),
            ("Partial re-side", "$4,000 – $12,000", "One elevation or story, including wrap and trim."),
            ("Full re-side", "$14,000 – $45,000+", "Complete siding system replacement; varies by material and home size."),
        ],
        "faq": [
            ("What siding holds up best in Bend?", "Fiber cement is the standout for Central Oregon: it resists UV, snow, rot and embers far better than basic vinyl. Vinyl is budget-friendly and low-maintenance; wood looks great but wants more care. We'll walk you through options for your home and budget."),
            ("Can you repair just the damaged section?", "Usually, yes. We color- and profile-match the existing siding so repairs blend in. If your siding is discontinued or widely failing, we'll show you exactly why replacement is the smarter spend before you commit."),
            ("How long does a full re-side take?", "Most Bend-area homes take one to two weeks depending on size, material and trim detail. Rain and snow can pause exterior work — we'll give you a realistic window up front and keep you posted."),
            ("Does new siding help with energy bills?", "When we re-side, we inspect and upgrade the weather barrier behind it. Combined with modern insulation practices, many homeowners notice fewer drafts and more stable indoor temperatures."),
        ],
        "related": [("Roofing Repairs", "/services/roofing-repairs"), ("Framing", "/services/framing"), ("Junk Removal", "/services/junk-removal")],
        "schema_name": "Siding Installation & Repair",
    },
    {
        "slug": "framing", "name": "Framing", "url": "/services/framing",
        "title": "Framing Contractor in Bend, OR | Roque General Construction",
        "desc": "Straight, code-aware framing in Bend & Central Oregon: additions, ADUs, garages, interior walls, decks & structural repairs. Free quote: (541) 410-0664.",
        "h1": "Framing That Everything Else Depends On",
        "lead": "Walls, floors and roofs that are straight, square and built to code — because every finish you see is only as good as the structure you don't. Rough framing, remodels, additions and structural repairs.",
        "hero_img": "framing-aerial.webp", "hero_alt": "Aerial view of new wooden roof trusses framed on a Central Oregon residential build", "hero_w": 1220, "hero_h": 1101,
        "intro": """<p>Framing is where a project wins or loses. A quarter inch out of square at the framing stage becomes a visible wave in the siding, a crack in the drywall and a headache for every tradesperson who follows.</p>
        <p>Our crews frame to plan — or help you shape the plan — with Central Oregon realities in mind: snow loads on roofs and decks, engineered details where spans demand them, and inspectors who expect the job done right the first time.</p>""",
        "includes": [
            ("Additions & ADUs", "From foundation ready to framed, dried-in and ready for inspection."),
            ("Garages & shops", "Detached structures framed for Central Oregon snow loads."),
            ("Interior walls & remodels", "New layouts, bonus rooms, door openings and beam installation."),
            ("Decks & outdoor structures", "Structural frames built for snow, sun and decades of barbecues."),
            ("Structural repairs", "Rot, sagging floors, damaged rafters and bearing-wall corrections."),
            ("Plan-ready precision", "We frame to your architect's plans — and flag conflicts before they become change orders."),
        ],
        "local": "Snow load is not a rounding error here — roof and deck framing in Bend, Sisters or La Pine must account for it. We size members for your zone and handle the permit drawings inspectors expect.",
        "photo2": {"img": "tools-hammer.webp", "alt": "Contractor's hammer and nails on a workbench — framing details planned before the first cut", "w": 960, "h": 641},
        "why": [
            ("Square, plumb, on plan", "We check the math before the nails — finishes go in faster when framing is true."),
            ("Snow-load aware engineering", "Members sized for your actual zone, not a national average."),
            ("Permit-ready paperwork", "We speak inspector and keep your project moving."),
            ("One crew to finish the shell", "Framing, siding and roofing repairs sequenced by the same team."),
        ],
        "prices": [
            ("Interior wall changes", "$500 – $2,500", "Non-bearing walls, openings and room reconfigurations."),
            ("Deck or garage framing", "$4,000 – $15,000", "Structure only, sized for local snow loads."),
            ("Addition / ADU framing", "$18,000 – $60,000+", "Framed and dried-in; scope and finishes drive the range."),
        ],
        "faq": [
            ("Do I need a permit to frame a new wall?", "Most structural work — bearing walls, additions, decks — needs a permit in Deschutes County and surrounding jurisdictions. Non-bearing interior walls usually don't. We handle permit drawings and scheduling for projects that need them."),
            ("Can you build from my architect's plans?", "Absolutely. We frame to plan and coordinate directly with your designer or engineer when site conditions call for adjustments — you'll hear about it before we cut, not after."),
            ("How long does framing take?", "A garage or addition frame typically runs one to two weeks once materials are on site. Weather matters: we plan around snow and don't rush structural work."),
            ("Do you work with homeowners' other contractors?", "Yes — we're happy to sequence our framing with your plumber, electrician or designer. Clear hand-offs are part of the job."),
        ],
        "related": [("Siding", "/services/siding"), ("Demolition", "/services/demolition"), ("Roofing Repairs", "/services/roofing-repairs")],
        "schema_name": "Framing",
    },
    {
        "slug": "roofing-repairs", "name": "Roofing Repairs", "url": "/services/roofing-repairs",
        "title": "Roofing Repairs in Bend, OR | Roque General Construction",
        "desc": "Leak detection, shingle & flashing repairs, storm damage fixes and emergency tarping in Bend & Central Oregon. Honest repair-vs-replace advice. Call (541) 410-0664.",
        "h1": "Roofing Repairs Before Small Leaks Get Loud",
        "lead": "A missing shingle is a five-dollar fix today and a five-thousand-dollar ceiling next winter. We find the real source of leaks, repair them properly, and tell you plainly when a patch is — and isn't — enough.",
        "hero_img": "roofing-worker.webp", "hero_alt": "Roofer securing roofing panels with a hammer on a sloped roof under a warm sky", "hero_w": 1024, "hero_h": 681,
        "intro": """<p>Central Oregon roofs work hard: heavy winter snow, spring freeze-thaw, summer UV and the occasional windstorm that lifts shingles like playing cards. Most roofs don't fail all at once — they fail at the details.</p>
        <p>We repair those details: pipe boots, step flashing, valleys, ridge caps and the wind-lifted shingles that start as a nuisance and end as rot. And when a roof is genuinely at the end of its life, we'll say so — with numbers for both paths.</p>""",
        "includes": [
            ("Leak diagnosis", "We trace water to its true entry point — not just where it drips."),
            ("Shingle replacement", "Wind-lifted, cracked or missing shingles matched and sealed."),
            ("Flashing & valley repairs", "The #1 leak source on Central Oregon roofs, fixed to spec."),
            ("Storm & snow damage", "Fast assessment, documentation for insurance, solid repairs."),
            ("Emergency tarping", "Weather-in-the-hole protection while bigger repairs are scheduled."),
            ("Vent & boot replacement", "Crumbed pipe boots and failed vents — cheap to fix, costly to ignore."),
        ],
        "local": "Freeze-thaw cycles open every hairline crack, and High Desert UV cooks the oils out of shingles years faster than the label promises. If your roof is past 15 summers, an annual look-over pays for itself.",
        "photo2": {"img": "roofing-detail.webp", "alt": "Roofer fastening panels during an active roof repair", "w": 860, "h": 630},
        "why": [
            ("We find the real leak", "Water travels — we inspect the whole path, not just the stain."),
            ("Repair-first philosophy", "If a $600 repair buys you five more years, that's what we'll recommend."),
            ("Insurance-ready documentation", "Photos and written scope you can hand straight to your adjuster."),
            ("Roof + siding coordination", "One crew fixes the leak and the water damage it left behind."),
        ],
        "prices": [
            ("Minor repair", "$250 – $800", "Shingles, boots, small flashing sections and sealing."),
            ("Moderate repair", "$800 – $2,500", "Valleys, larger flashing runs, partial sections of roof."),
            ("Full replacement", "Custom quote", "When repairs no longer make sense, we quote replacement with material options."),
        ],
        "faq": [
            ("Do you handle emergency leaks?", "Yes — call (541) 410-0664 and we'll triage same day when possible, including tarping to stop active water while we schedule the permanent repair."),
            ("Can you help with an insurance claim?", "We document storm damage with photos and a written scope of work your adjuster can use. We don't inflate claims — honest documentation gets claims approved faster."),
            ("How do I know if I need repair or replacement?", "Age plus pattern matters: one leaky valley is a repair; curling shingles across whole faces and repeated leaks usually mean replacement. We'll show you photos of exactly what we see and price both paths."),
            ("How long do repairs take?", "Most repairs are half a day to one day. Weather is the wild card — we won't pull shingles back with snow in the forecast."),
        ],
        "related": [("Siding", "/services/siding"), ("Framing", "/services/framing"), ("Junk Removal", "/services/junk-removal")],
        "schema_name": "Roofing Repairs",
    },
    {
        "slug": "demolition", "name": "Demolition", "url": "/services/demolition",
        "title": "Demolition Services in Bend, OR | Roque General Construction",
        "desc": "Safe, permitted residential demolition in Bend & Central Oregon — sheds, decks, interior gut-outs & full structures. Hauling included. Free quote: (541) 410-0664.",
        "h1": "Demolition Done Safe, Legal &amp; Clean",
        "lead": "Good demolition is controlled, permitted and quiet on your neighbors. From a gutted bathroom to a full structure teardown, we bring the right equipment, handle the permits and haul everything away.",
        "hero_img": "demolition-excavator.webp", "hero_alt": "Excavator methodically tearing down an old structure at a residential demolition site", "hero_w": 1024, "hero_h": 681,
        "intro": """<p>Demolition is where many projects actually start — and where an unlicensed crew can create expensive problems: an unmarked gas line, an unpermitted teardown, a dumpster of debris nobody wants to move twice.</p>
        <p>We demo with a plan: utilities located and disconnected, permits in hand, dust controlled, salvageable materials separated, and the site left swept and ready for whatever comes next. Because we frame and re-side too, we demo with the rebuild in mind.</p>""",
        "includes": [
            ("Selective interior demo", "Kitchens, bathrooms, flooring and walls — surgically, with the rest of the house protected."),
            ("Structure teardown", "Sheds, garages, decks, fences and mobile homes removed foundation to rooftop."),
            ("Permit handling", "We pull the required demolition permits and schedule inspections."),
            ("Utility coordination", "Gas, electric and water located and safely disconnected before the first swing."),
            ("Debris hauling included", "Ours is a one-number quote: demo and haul-off together, no dumpster rental roulette."),
            ("Site prep for the rebuild", "Backfilled, graded and swept — ready for framing or landscaping."),
        ],
        "local": "Older Central Oregon properties often hide surprises: buried fuel oil tanks, unpermitted additions, asbestos-era materials. We flag those risks during the estimate so there are no mid-demo cost bombs.",
        "photo2": {"img": "demolition-site.webp", "alt": "Excavator working through rubble and debris on a cleared demolition lot", "w": 1024, "h": 681},
        "why": [
            ("Licensed & insured demolition", "This is not a Craigslist crew with a sledgehammer — permits, insurance and process."),
            ("One quote, haul-off included", "No separate dumpster bills, no debris left 'for later'."),
            ("Rebuild-minded teardowns", "We demo precisely what the next phase of your project needs."),
            ("Neighbor-conscious worksites", "Dust control, debris netting and posted permits keep the peace."),
        ],
        "prices": [
            ("Shed / small structure", "$600 – $2,500", "Teardown, disposal and site cleanup included."),
            ("Interior gut-out", "$2,000 – $10,000", "Kitchen, bath or whole-floor demo with protection and haul-off."),
            ("Garage / large structure", "$6,000 – $20,000+", "Full teardown with permits and disposal; concrete adds cost."),
        ],
        "faq": [
            ("Do I need a permit for demolition?", "Most structural demolition in Deschutes County and nearby jurisdictions requires one; interior remodel demo usually doesn't. We confirm requirements for your address and handle the paperwork when it's needed."),
            ("Does the price include hauling everything away?", "Yes. Our demolition quotes are turnkey — labor, disposal fees and site cleanup in one number. The only surprise is how clean the site looks after."),
            ("Can you demo just part of a structure?", "That's selective demolition — our specialty. We isolate utilities, protect what stays, and remove exactly what your plans call for."),
            ("What about hazardous materials?", "Pre-1990s buildings can hide asbestos or lead. We flag the risk during the estimate; if testing is needed we'll connect you with an abatement partner before we demo."),
        ],
        "related": [("Junk Removal", "/services/junk-removal"), ("Framing", "/services/framing"), ("Siding", "/services/siding")],
        "schema_name": "Demolition",
    },
    {
        "slug": "junk-removal", "name": "Junk Removal", "url": "/services/junk-removal",
        "title": "Junk Removal in Bend, OR | Roque General Construction",
        "desc": "Fast, careful junk removal in Bend & Central Oregon: garages, yards, appliances, construction debris & cleanouts. Same-week pickup. Call (541) 410-0664.",
        "h1": "Junk Removal That Actually Shows Up",
        "lead": "Garage full, yard buried in branches, renovation debris stacked in the driveway? We load it, sweep up after and take it where it belongs — with recycling and donation before the landfill.",
        "hero_img": "crew-hivis.webp", "hero_alt": "RGC crew in high-visibility gear loading debris — we do the heavy lifting", "hero_w": 1024, "hero_h": 681,
        "intro": """<p>You shouldn't need to rent a trailer, beg a friend with a truck and spend three weekends on it. Point at the pile — we do the lifting, loading, sweeping and hauling.</p>
        <p>We handle household junk, appliance and furniture removal, yard debris, estate and rental cleanouts, and construction debris from our own job sites or yours. Metals, electronics and reusable goods are routed to recycling and donation partners — the landfill is the last stop, not the first.</p>""",
        "includes": [
            ("Household junk", "Furniture, mattresses, boxes, odds and ends — from one room or a whole house."),
            ("Appliances & e-waste", "Fridges, washers, TVs and electronics recycled properly."),
            ("Yard & fire debris", "Branches, brush, bark dust and fire-season fuel cleared from your lot."),
            ("Garage & basement cleanouts", "Decades of 'we'll deal with it later', dealt with in an afternoon."),
            ("Rental & estate cleanouts", "Discreet, thorough turnovers on your timeline."),
            ("Construction debris", "Job-site scraps hauled and sorted — including debris from your own remodeler."),
        ],
        "local": "Deschutes County landfill and recycling rules change, and some items (paint, chemicals, tires) need special handling. We sort as we load so you don't pay dump penalties — and so reusable goods skip the landfill.",
        "photo2": {"img": "craft-hands.webp", "alt": "Close-up of work-gloved hands doing careful manual work on site", "w": 960, "h": 540},
        "why": [
            ("We do all the lifting", "Point at it. That's your whole job."),
            ("Same-week pickup", "Usually within 48 hours; call for same-day availability."),
            ("Upfront volume pricing", "You approve the price before we load. No hourly creep."),
            ("Donate-recycle-first", "Usable goods go to local partners before the transfer station."),
        ],
        "prices": [
            ("Single items", "$95 – $175", "Couch, fridge, mattress, hot tub panel — one-and-done pickups."),
            ("Half-truck load", "$275 – $450", "A garage corner, a small yard pile, a room's worth of boxes."),
            ("Full load / cleanout", "$500 – $950+", "Full truck and trailer; cleanouts quoted by volume after photos."),
        ],
        "faq": [
            ("What won't you take?", "Hazardous waste: paint, chemicals, solvents, asbestos, ammunition. Deschutes County has free hazardous-waste disposal events — we'll point you to the right one. Almost everything else is fair game."),
            ("Do I need to be home for pickup?", "It helps for access and approval, but you can also text photos for a quote and prepay — we'll confirm once loaded."),
            ("How fast can you come out?", "Most pickups happen within 48 hours, and construction debris from active RGC job sites goes same day. Call (541) 410-0664 for same-day availability."),
            ("Is junk removal cheaper than a dumpster?", "Usually, yes — you don't pay for the rental days, the permit for the street or the labor to load it yourself. You pay for the volume we actually haul."),
        ],
        "related": [("Demolition", "/services/demolition"), ("Roofing Repairs", "/services/roofing-repairs"), ("Siding", "/services/siding")],
        "schema_name": "Junk Removal",
    },
]

# ---------------------------------------------------------------- ABOUT ----

about_main = """    <section class="page-hero">
      <div class="container page-hero__inner">
        """ + breadcrumb([("Home", "/"), ("About", None)]) + """
        <h1>The crew behind <span style="color:var(--red-bright)">RGC</span></h1>
        <p class="lead">Roque General Construction LLC is a locally owned general contracting company based in Bend, Oregon — built on a simple idea: one accountable crew for the five trades Central Oregon homes need most.</p>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div class="reveal">
          <p class="eyebrow">Our story</p>
          <h2 class="headline-mark">Built on craft. Backed by our name.</h2>
          <p class="lead">RGC was founded by <b>Mario Roque Bello</b>, a general contractor who spent years watching the same story repeat on Central Oregon job sites: homeowners juggling a siding crew, a framer, a roofer and a hauler — four schedules, four standards, and gaps in between where problems live.</p>
          <p>The fix wasn't a bigger company. It was a focused one: master five trades that naturally belong together — the envelope and structure of a home — and deliver them with one schedule, one standard and one person whose name is on the truck.</p>
          <p>Today RGC serves homeowners, realtors and property managers across Bend, Redmond, Sisters and the wider High Desert. Licensed, bonded and insured, we show up with straight quotes and we leave clean sites — because around here, reputation is the only marketing that compounds.</p>
          <div class="info-banner">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3z"/><path d="M9 12l2 2 4-4"/></svg>
            <p><b>Licensed · Bonded · Insured — Oregon CCB contractor.</b> Ask for our license number and certificate of insurance any time; we send both before we swing the first hammer.</p>
          </div>
          <a class="btn btn--primary" href="/contact">Talk to Mario about your project <span class="btn-arrow">→</span></a>
        </div>
        <div class="split__media reveal reveal-d1">
          <img src="/img/photos/crew-hivis.webp" alt="Roque General Construction crew in high-visibility gear collaborating on a build" loading="lazy" width="1024" height="681">
          <span class="plate plate-float">RGC crew</span>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container">
        <p class="eyebrow">How we work</p>
        <h2 class="headline-mark">Four values, zero fine print</h2>
        <div class="feature-cards feature-cards--4" style="margin-top:1.8rem">
          <div class="feature-card reveal">
            <span class="fc-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg></span>
            <h3>Trust first</h3>
            <p>Written, itemized quotes. The price we agree on is the price you pay unless you change the scope.</p>
          </div>
          <div class="feature-card reveal reveal-d1">
            <span class="fc-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m15 12 5.3 5.3L15 22.6 9.7 17.3M3 7l4-4 6 6-4 4-6-6z"/></svg></span>
            <h3>Real craft</h3>
            <p>Square framing, spec-fastened siding, leaks traced to their source. Details are the whole job.</p>
          </div>
          <div class="feature-card reveal reveal-d2">
            <span class="fc-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg></span>
            <h3>On-time, on-site</h3>
            <p>We give realistic dates and we keep them. If weather moves the schedule, you hear it from us first.</p>
          </div>
          <div class="feature-card reveal reveal-d3">
            <span class="fc-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 11 12 3l9 8M5 10v10h14V10"/></svg></span>
            <h3>Truly local</h3>
            <p>We live here. Every job site is a neighbor's home — and in Central Oregon, that travels fast.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container split split--rev">
        <div class="split__media reveal">
          <img src="/img/photos/tools-hammer.webp" alt="Contractor's hammer and nails laid out on a workbench" loading="lazy" width="960" height="641">
        </div>
        <div class="reveal reveal-d1">
          <p class="eyebrow">Service area</p>
          <h2 class="headline-mark">From Bend to the whole High Desert</h2>
          <p class="lead">Based in Bend, on the road every week across Central Oregon — Redmond, Sisters, Tumalo, Terrebonne, Prineville, La Pine, Sunriver, Powell Butte, Madras and Crooked River Ranch.</p>
          <p>Residential or light commercial, single repair to full envelope — if it's siding, framing, roofing, demo or debris, it's one call to RGC. <em>Se habla español.</em></p>
          <div class="area-chips" style="margin-top:1rem">
            <span class="chip chip--hot">📍 Bend</span><span class="chip">Redmond</span><span class="chip">Sisters</span><span class="chip">Prineville</span><span class="chip">La Pine</span><span class="chip">Madras</span>
          </div>
        </div>
      </div>
    </section>

""" + CTA_BAND

about_graph = [
    {"@id": f"{BASE}/#business"},
    {
        "@type": "WebPage",
        "@id": f"{BASE}/about#webpage",
        "url": f"{BASE}/about",
        "name": "About Roque General Construction LLC",
        "isPartOf": {"@id": f"{BASE}/#website"},
        "about": {"@id": f"{BASE}/#business"},
        "inLanguage": "en-US",
    },
    {
        "@type": "AboutPage",
        "@id": f"{BASE}/about#aboutpage",
        "url": f"{BASE}/about",
        "name": "About Roque General Construction LLC",
        "inLanguage": "en-US",
    },
    breadcrumbs_schema([("Home", "/"), ("About", "/about")]),
]

# ------------------------------------------------------------- SERVICES ----

SERVICES_HUB_FAQ = [
    ("What areas around Bend do you serve?", "All of Central Oregon: Bend, Redmond, Sisters, Tumalo, Terrebonne, Prineville, La Pine, Sunriver, Powell Butte, Madras and Crooked River Ranch. Outside that circle, call — we flex for the right project."),
    ("Are you a licensed contractor in Oregon?", "Yes — Roque General Construction LLC is licensed, bonded and insured through the Oregon Construction Contractors Board. Licensing is your protection: verified insurance, a track record and recourse if something goes wrong. License number and insurance certificate available on request."),
    ("Can you combine services on one project?", "That's our whole model. Siding + roofing repairs, demolition + framing + re-side, junk removal + deck demo — bundling trades means one schedule, one point of contact and lower total cost."),
    ("How does your free estimate work?", "Send photos and a description through our quote form, or book an on-site visit for bigger scopes. You get a written, itemized estimate — usually within 24–48 hours. No pressure, no obligation."),
    ("Do you offer payment plans or financing?", "For most residential projects we accept card, check and bank transfer, with milestone payments on larger builds. Ask about options during your estimate — we keep it simple and transparent."),
    ("Are you insured if something gets damaged?", "Yes — we carry liability insurance and can share our certificate before work begins. We also protect surfaces and landscaping as standard practice, because the best claim is the one that never happens."),
    ("Do you work with property managers and realtors?", "Regularly. Pre-listing repairs, turnover cleanouts, storm damage triage — we batch-scope small jobs across units to keep costs down and tenants happy."),
    ("What if I only need one small job done?", "Perfect — small jobs are how most of our clients met us. A shed teardown, a leaky valley, a wall removed. We don't inflate small jobs into big ones."),
]

services_main = """    <section class="page-hero">
      <div class="container page-hero__inner">
        """ + breadcrumb([("Home", "/"), ("Services", None)]) + """
        <h1>Services — five trades, <span style="color:var(--red-bright)">one crew</span></h1>
        <p class="lead">Everything below is delivered by our own licensed crew with the same standard: honest scopes, itemized quotes and clean sites. Pick a service to see what's included, what it costs and how we work.</p>
        <div class="page-hero__img">
          <img src="/img/photos/hero-framing.webp" alt="Aerial view of a new home framed with wooden trusses at a Central Oregon construction site" fetchpriority="high" width="1920" height="1440">
        </div>
      </div>
    </section>
"""

svc_block_template = """
    <section class="section{sec}">
      <div class="container split{rev}">
        <div class="split__media reveal">
          <img src="/img/photos/{img}" alt="{alt}" loading="lazy" width="{w}" height="{h}">
          <span class="plate plate-float">{num}</span>
        </div>
        <div class="reveal reveal-d1">
          <p class="eyebrow">{num} — {name}</p>
          <h2 class="headline-mark">{heading}</h2>
          <p class="lead">{blurb}</p>
          <ul class="checklist">
{checks}
          </ul>
          <div style="display:flex;gap:.8rem;flex-wrap:wrap">
            <a class="btn btn--primary" href="{url}">Explore {name} <span class="btn-arrow">→</span></a>
            <a class="btn btn--ghost{ghost}" href="/contact">Get a quote</a>
          </div>
        </div>
      </div>
    </section>"""

svc_blocks = [
    ("01", "Siding", "Siding built for High Desert weather",
     "Fiber cement, vinyl and wood — installed to manufacturer spec or repaired to blend invisibly. UV-proof thinking included.",
     [("Full re-sides & new construction siding", ""), ("Storm, UV & rot repairs", ""), ("Trim, soffit & fascia", "")],
     "siding-house.webp", "House with fresh blue fiber cement siding and a new dark shingle roof", 1600, 1200),
    ("02", "Framing", "Framing that's square, plumb & permitted",
     "Additions, garages, ADUs, interior walls and structural repairs — engineered for Central Oregon snow loads.",
     [("Additions, ADUs & garages", ""), ("Interior walls & structural repairs", ""), ("Decks built for real snow loads", "")],
     "framing-aerial.webp", "Aerial view of new wooden roof trusses on a residential build", 1220, 1101),
    ("03", "Roofing Repairs", "Leaks found, fixed & documented",
     "We trace the water to its true entry point and repair it properly — and tell you honestly when a patch isn't enough.",
     [("Leak diagnosis & shingle replacement", ""), ("Flashing, valleys & vents", ""), ("Storm damage & insurance documentation", "")],
     "roofing-worker.webp", "Roofer securing panels with a hammer under a warm sky", 1024, 681),
    ("04", "Demolition", "Safe, permitted teardowns",
     "Sheds, decks, interiors and full structures — with permits, utility disconnects and haul-off in one number.",
     [("Selective & full demolition", ""), ("Permits & utility coordination", ""), ("Debris hauling included", "")],
     "demolition-excavator.webp", "Excavator tearing down an old residential structure", 1024, 681),
    ("05", "Junk Removal", "Point at it. It's gone.",
     "Garages, yards, appliances, cleanouts and construction debris — loaded, swept and hauled same week.",
     [("Household & yard debris", ""), ("Appliances & e-waste recycled", ""), ("Estate & rental cleanouts", "")],
     "craft-hands.webp", "Gloved crew member lifting debris by hand — we do the heavy lifting", 960, 540),
]

for i, (num, name, heading, blurb, checks, img, alt_txt, w, h) in enumerate(svc_blocks):
    dark = i % 2 == 1
    rev = " split--rev" if i % 2 == 0 else ""
    checks_html = "\n".join(
        f'            <li>{CHECK_SVG}<span><b>{c[0]}</b>{f" <span>{c[1]}</span>" if c[1] else ""}</span></li>'
        for c in checks)
    url = "/services/" + ["siding", "framing", "roofing-repairs", "demolition", "junk-removal"][i]
    services_main += svc_block_template.format(
        sec=" section--dark" if dark else "", rev=rev, img=img, alt=alt_txt, w=w, h=h,
        ghost="" if dark else "-dark",
        num=num, name=name, heading=heading, blurb=blurb, checks=checks_html, url=url)

services_main += """
    <section class="section section--paper2">
      <div class="container">
        <p class="eyebrow">Common questions</p>
        <h2 class="headline-mark">Good to know before you call</h2>
""" + faq_html(SERVICES_HUB_FAQ) + """
      </div>
    </section>

""" + CTA_BAND

services_graph = [
    {"@id": f"{BASE}/#business"},
    {
        "@type": "WebPage",
        "@id": f"{BASE}/services#webpage",
        "url": f"{BASE}/services",
        "name": "Construction Services in Bend, OR",
        "isPartOf": {"@id": f"{BASE}/#website"},
        "about": {"@id": f"{BASE}/#business"},
        "inLanguage": "en-US",
    },
    {
        "@type": "ItemList",
        "@id": f"{BASE}/services#list",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "item": {"@type": "Service", "name": cfg["schema_name"], "url": BASE + cfg["url"]}}
            for i, cfg in enumerate(SERVICES_DATA)
        ],
    },
    breadcrumbs_schema([("Home", "/"), ("Services", "/services")]),
    faq_schema("/services", SERVICES_HUB_FAQ),
]

# -------------------------------------------------------------- GALLERY ----

GALLERY_ITEMS = [
    ("siding", "Fiber cement re-side, full elevation", "siding-house.webp", "House with freshly installed blue fiber cement siding and new dark shingle roof", 1600, 1200),
    ("siding", "Crisp corners & trim detail", "siding-detail.webp", "Close-up of new fiber cement siding and corner trim on a finished wall", 920, 780),
    ("framing", "Roof frame set, braced & true", "hero-framing.webp", "Aerial view of a full residential roof framed with wooden trusses", 1920, 1440),
    ("framing", "Trusses up close", "framing-aerial.webp", "Aerial close-up of new roof trusses against the sky", 1220, 1101),
    ("roofing", "Panel roof installation", "roofing-worker.webp", "Roofer fastening metal roofing panels with a hammer", 1024, 681),
    ("crew", "Tools of the trade, ready at dawn", "tools-hammer.webp", "Contractor's hammer and nails laid out on a workbench", 960, 641),
    ("demolition", "Structure teardown, step by step", "demolition-excavator.webp", "Excavator demolishing an old residential structure", 1024, 681),
    ("demolition", "Site cleared & sorted for disposal", "demolition-site.webp", "Excavator working through sorted rubble on a demolition site", 1024, 681),
    ("junk", "Heavy lifting included", "craft-hands.webp", "Gloved crew member lifting debris by hand during a cleanout", 960, 540),
    ("crew", "RGC crew on site", "crew-hivis.webp", "Construction crew in high-visibility vests working together", 1024, 681),
]

CATS = [("all", "All work"), ("siding", "Siding"), ("framing", "Framing"), ("roofing", "Roofing"), ("demolition", "Demolition"), ("junk", "Junk Removal"), ("crew", "Our Crew")]

gallery_main = """    <section class="page-hero">
      <div class="container page-hero__inner">
        """ + breadcrumb([("Home", "/"), ("Gallery", None)]) + """
        <h1>Work worth <span style="color:var(--red-bright)">walking around</span></h1>
        <p class="lead">Representative shots of the trades we run every week across Central Oregon — siding systems, structural framing, roofing details, controlled tear-downs and clean finishes.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="gallery-filters" role="group" aria-label="Filter gallery by service">
"""
for key, label in CATS:
    gallery_main += f'          <button class="gf" type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>\n'
gallery_main += """        </div>
        <div class="gallery-grid" id="gallery-grid">
"""
for cat, cap, img, alt, w, h in GALLERY_ITEMS:
    thumb = img.replace(".webp", "-640.webp") if w > 700 else img
    gallery_main += f"""          <button class="gitem" type="button" data-cat="{cat}" data-caption="{cap}" data-full="/img/photos/{img}">
            <img src="/img/photos/{thumb}" alt="{alt}" loading="lazy" width="680" height="510">
            <figcaption>{cap} <span class="tag">{dict((k, l) for k, l in CATS)[cat]}</span></figcaption>
          </button>
"""
gallery_main += """        </div>
        <p class="form-note" style="margin-top:1.4rem">Want your project on this page? It starts with a free estimate — <a href="/contact">tell us about it</a>.</p>
      </div>
    </section>

    <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer">
      <button class="lightbox__btn lightbox__close" aria-label="Close viewer">×</button>
      <button class="lightbox__btn lightbox__prev" aria-label="Previous image">←</button>
      <img src="" alt="">
      <p class="lightbox__cap"></p>
      <button class="lightbox__btn lightbox__next" aria-label="Next image">→</button>
    </div>

""" + CTA_BAND

gallery_graph = [
    {"@id": f"{BASE}/#business"},
    {
        "@type": "WebPage",
        "@id": f"{BASE}/gallery#webpage",
        "url": f"{BASE}/gallery",
        "name": "Project Gallery | Roque General Construction",
        "isPartOf": {"@id": f"{BASE}/#website"},
        "inLanguage": "en-US",
    },
    {
        "@type": "CollectionPage",
        "@id": f"{BASE}/gallery#collection",
        "url": f"{BASE}/gallery",
        "name": "Project Gallery",
        "inLanguage": "en-US",
    },
    breadcrumbs_schema([("Home", "/"), ("Gallery", "/gallery")]),
]

# --------------------------------------------------------------- CONTACT ----

contact_main = """    <section class="page-hero">
      <div class="container page-hero__inner">
        """ + breadcrumb([("Home", "/"), ("Contact", None)]) + """
        <h1>Let's talk about your <span style="color:var(--red-bright)">project</span></h1>
        <p class="lead">Call, text or send the form — you'll get a straight answer and a free, itemized estimate, usually within 48 hours. <em>Se habla español.</em></p>
      </div>
    </section>

    <section class="section">
      <div class="container contact-layout">
        <div class="contact-card reveal">
          <h2 style="font-size:1.4rem">Contact RGC</h2>
          <div class="contact-line">
            <span class="cl-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.4 2.1L8.1 10a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.6 2z"/></svg></span>
            <div>
              <b>Call or text — primary</b>
              <a href="tel:+15414100664">(541) 410-0664</a>
              <small>Fastest response, 7am–6pm</small>
            </div>
          </div>
          <div class="contact-line">
            <span class="cl-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.4 2.1L8.1 10a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.6 2z"/></svg></span>
            <div>
              <b>Secondary line</b>
              <a href="tel:+15414101136">(541) 410-1136</a>
              <small>If the first line is on a roof, try here</small>
            </div>
          </div>
          <div class="contact-line">
            <span class="cl-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></span>
            <div>
              <b>Email</b>
              <a href="mailto:marioroque@yahoo.com">marioroque@yahoo.com</a>
              <small>Photos help us quote faster</small>
            </div>
          </div>
          <div class="contact-line">
            <span class="cl-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></span>
            <div>
              <b>Service area</b>
              <span class="val">Bend, OR — Central Oregon</span>
              <small>Redmond · Sisters · Prineville · La Pine · Madras &amp; more</small>
            </div>
          </div>
          <div class="contact-line">
            <span class="cl-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg></span>
            <div>
              <b>Hours</b>
              <span class="val">Mon–Fri 7am–6pm · Sat 8am–2pm</span>
              <small>Urgent leak? Call — we triage same day when possible</small>
            </div>
          </div>
          <div class="contact-line">
            <span class="cl-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3z"/><path d="M9 12l2 2 4-4"/></svg></span>
            <div>
              <b>Credentials</b>
              <span class="val">Licensed · Bonded · Insured</span>
              <small>Oregon CCB licensed &amp; insured — certificate available on request</small>
            </div>
          </div>
        </div>

        <form class="quote-form reveal reveal-d1" action="https://formsubmit.co/ajax/marioroque@yahoo.com" method="POST" novalidate>
          <h2>Request your free estimate</h2>
          <p style="color:var(--muted);font-size:.92rem">Attach details in the message — project type, city and a few photos (email us the photos) — and we'll come back with a clear number.</p>
          <div class="form-grid">
            <div class="field">
              <label for="cf-name">Full name <span class="req">*</span></label>
              <input id="cf-name" name="Name" type="text" autocomplete="name" required>
              <span class="err">Please enter your name.</span>
            </div>
            <div class="field">
              <label for="cf-phone">Phone <span class="req">*</span></label>
              <input id="cf-phone" name="Phone" type="tel" autocomplete="tel" placeholder="Your phone number" required>
              <span class="err">Please enter a valid phone number.</span>
            </div>
            <div class="field">
              <label for="cf-email">Email <span class="req">*</span></label>
              <input id="cf-email" name="Email" type="email" autocomplete="email" placeholder="you@email.com" required>
              <span class="err">Please enter a valid email.</span>
            </div>
            <div class="field">
              <label for="cf-city">City</label>
              <input id="cf-city" name="City" type="text" placeholder="Bend, Redmond…">
            </div>
            <div class="field full">
              <label for="cf-service">Service needed <span class="req">*</span></label>
              <select id="cf-service" name="Service" required>
                <option value="">Select a service…</option>
                <option>Siding</option>
                <option>Framing</option>
                <option>Roofing Repairs</option>
                <option>Demolition</option>
                <option>Junk Removal</option>
                <option>Several services / not sure</option>
              </select>
              <span class="err">Please choose a service.</span>
            </div>
            <div class="field full">
              <label for="cf-msg">Project details <span class="req">*</span></label>
              <textarea id="cf-msg" name="Details" placeholder="Tell us what you need: what, where, and roughly when. Photos welcome by email." required></textarea>
              <span class="err">Tell us a bit about the project.</span>
            </div>
            <div class="hp-field" aria-hidden="true">
              <label>Leave this field empty</label>
              <input type="text" name="_honey" tabindex="-1" autocomplete="off">
            </div>
            <input type="hidden" name="_subject" value="Free Estimate Request — Roque GC website">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <div class="full">
              <button class="btn btn--primary" type="submit" style="width:100%">Send My Free Estimate Request</button>
              <div class="form-status" role="status" aria-live="polite"></div>
              <p class="form-note">100% free, no obligation. We reply within one business day — usually much faster.</p>
            </div>
          </div>
        </form>
      </div>
    </section>

""" + CTA_BAND

contact_graph = [
    {"@id": f"{BASE}/#business"},
    {
        "@type": "WebPage",
        "@id": f"{BASE}/contact#webpage",
        "url": f"{BASE}/contact",
        "name": "Contact Roque General Construction",
        "isPartOf": {"@id": f"{BASE}/#website"},
        "inLanguage": "en-US",
    },
    {
        "@type": "ContactPage",
        "@id": f"{BASE}/contact#contactpage",
        "url": f"{BASE}/contact",
        "name": "Contact Roque General Construction",
        "inLanguage": "en-US",
    },
    breadcrumbs_schema([("Home", "/"), ("Contact", "/contact")]),
]

# ------------------------------------------------------------------ 404 ----

notfound_main = """    <section class="page-hero">
      <div class="container page-hero__inner" style="text-align:center;max-width:760px;margin-inline:auto">
        <span class="plate" style="margin-bottom:1.2rem">Error 404</span>
        <h1>This one needs <span style="color:var(--red-bright)">demolition</span></h1>
        <p class="lead" style="margin-inline:auto">The page you're looking for got hauled away — but unlike our junk removal, it's not coming back. Let's get you somewhere useful.</p>
        <div style="display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap;margin-top:1.6rem">
          <a class="btn btn--primary" href="/">Back to Home <span class="btn-arrow">→</span></a>
          <a class="btn btn--ghost" href="/services">View Services</a>
          <a class="btn btn--ghost" href="/contact">Contact Us</a>
        </div>
      </div>
    </section>"""

# ---------------------------------------------------------------- Build ----

PAGES = {
    "about.html": page(
        "About Us | Roque General Construction — Bend, OR",
        "Meet Mario Roque Bello and the RGC crew: a licensed, bonded & insured general contractor in Bend, OR serving all of Central Oregon. Se habla español.",
        "/about", "about", about_main, {"@context": "https://schema.org", "@graph": about_graph},
    ),
    "services.html": page(
        "Siding, Framing & Roofing Repairs in Bend, OR | Roque GC",
        "Five trades, one licensed crew: siding, framing, roofing repairs, demolition & junk removal in Bend and Central Oregon. Free itemized estimates.",
        "/services", "services", services_main, {"@context": "https://schema.org", "@graph": services_graph},
    ),
    "gallery.html": page(
        "Project Gallery | Roque General Construction — Bend, OR",
        "See representative work from RGC: siding installs, framing, roofing repairs, demolition and junk removal across Central Oregon.",
        "/gallery", "gallery", gallery_main, {"@context": "https://schema.org", "@graph": gallery_graph},
    ),
    "contact.html": page(
        "Contact & Free Estimates | Roque General Construction — Bend, OR",
        "Request a free estimate from Roque General Construction: call (541) 410-0664, (541) 410-1136 or send the form. Serving Bend & Central Oregon. Se habla español.",
        "/contact", "contact", contact_main, {"@context": "https://schema.org", "@graph": contact_graph},
    ),
    "404.html": page(
        "Page Not Found | Roque General Construction",
        "The page you are looking for was not found. Head back to the Roque General Construction home page.",
        "/404", "", notfound_main, {"@context": "https://schema.org", "@graph": [{"@id": f"{BASE}/#business"}]},
        robots="noindex, nofollow",
    ),
}

for cfg in SERVICES_DATA:
    cfg["schema_name"] = cfg["schema_name"]
    PAGES["services/" + cfg["slug"] + ".html"] = service_page(cfg)

def main():
    for relpath, html in PAGES.items():
        dest = os.path.join(ROOT, relpath)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print("OK", relpath, f"({len(html)//1024} KB)")

if __name__ == "__main__":
    main()
