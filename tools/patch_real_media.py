#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parche robusto: integra material real del cliente (regex por nombre de archivo)."""
import re

p = "tools/build_pages.py"
b = open(p, encoding="utf-8").read()

def re_sub(pattern, repl, label, count=0):
    global b
    b, n = re.subn(pattern, repl, b, count=count)
    print(f"{label}: {n} reemplazo(s)")
    return n

# ---------- 1) heroes de páginas de servicio ----------
re_sub(r'"hero_img": "siding-house\.webp", "hero_alt": "[^"]*", "hero_w": 1600, "hero_h": 1200,',
       '"hero_img": "siding-house.webp", "hero_alt": "Completed two-story home with dark lap siding, crisp trim and fresh gutters installed by RGC", "hero_w": 1600, "hero_h": 1200,',
       "hero siding")
re_sub(r'"hero_img": "framing-aerial\.webp", "hero_alt": "[^"]*", "hero_w": \d+, "hero_h": \d+,',
       '"hero_img": "framing-aerial.webp", "hero_alt": "Residential build at framing stage with gable roof structure and stone column entry", "hero_w": 1600, "hero_h": 1200,',
       "hero framing")
re_sub(r'"hero_img": "roofing-worker\.webp", "hero_alt": "[^"]*", "hero_w": \d+, "hero_h": \d+,',
       '"hero_img": "roofing-worker.webp", "hero_alt": "Roof deck with battens and panels staged during an active reroof", "hero_w": 1600, "hero_h": 2133,',
       "hero roofing")
re_sub(r'"hero_img": "demolition-excavator\.webp", "hero_alt": "[^"]*", "hero_w": \d+, "hero_h": \d+,',
       '"hero_img": "demolition-excavator.webp", "hero_alt": "Interior gut-out: framing exposed and debris staged for haul-off", "hero_w": 1600, "hero_h": 2133,',
       "hero demolition")
re_sub(r'"hero_img": "crew-hivis\.webp", "hero_alt": "[^"]*", "hero_w": \d+, "hero_h": \d+,',
       '"hero_img": "crew-hivis.webp", "hero_alt": "RGC trailer parked on a Central Oregon job site, ready for haul-off", "hero_w": 1600, "hero_h": 1200,',
       "hero junk")

# ---------- 2) photo2 por img ----------
re_sub(r'"photo2": \{"img": "siding-detail\.webp", "alt": "[^"]*", "w": \d+, "h": \d+\},',
       '"photo2": {"img": "siding-detail.webp", "alt": "Fresh lap siding gable with black-framed windows installed by our crew", "w": 1200, "h": 1600},',
       "photo2 siding")
re_sub(r'"photo2": \{"img": "tools-hammer\.webp", "alt": "[^"]*", "w": \d+, "h": \d+\},',
       '"photo2": {"img": "framing-corner.webp", "alt": "Building corner with wall framing, house wrap and lumber staged on site", "w": 1200, "h": 1600},',
       "photo2 framing")
re_sub(r'"photo2": \{"img": "roofing-detail\.webp", "alt": "[^"]*", "w": \d+, "h": \d+\},',
       '"photo2": {"img": "roofing-detail.webp", "alt": "Detail of roof battens and underlayment ready for panels", "w": 1200, "h": 1600},',
       "photo2 roofing")
re_sub(r'"photo2": \{"img": "demolition-site\.webp", "alt": "[^"]*", "w": \d+, "h": \d+\},',
       '"photo2": {"img": "demolition-site.webp", "alt": "Demolition debris separated and staged for disposal on site", "w": 1200, "h": 1600},',
       "photo2 demolition")
re_sub(r'"photo2": \{"img": "craft-hands\.webp", "alt": "[^"]*", "w": \d+, "h": \d+\},',
       '"photo2": {"img": "demolition-site.webp", "alt": "Debris and junk separated for donation, recycling and disposal", "w": 1200, "h": 1600},',
       "photo2 junk")

# ---------- 3) hub blocks ----------
re_sub(r'"siding-house\.webp", "House with fresh blue fiber cement siding[^"]*", 1600, 1200',
       '"siding-house.webp", "Completed two-story home with dark lap siding by RGC", 1600, 1200', "hub siding")
re_sub(r'"framing-aerial\.webp", "Aerial view of new wooden roof trusses on a residential build", \d+, \d+',
       '"framing-aerial.webp", "Home at framing stage with gable structure and stone columns", 1600, 1200', "hub framing")
re_sub(r'"roofing-worker\.webp", "Roofer securing panels with a hammer under a warm sky", \d+, \d+',
       '"roofing-worker.webp", "Roof deck with battens and panels during an active reroof", 1600, 2133', "hub roofing")
re_sub(r'"demolition-excavator\.webp", "Excavator tearing down an old residential structure", \d+, \d+',
       '"demolition-excavator.webp", "Interior gut-out with debris staged for haul-off", 1600, 2133', "hub demolition")
re_sub(r'"craft-hands\.webp", "Gloved crew member lifting debris by hand — we do the heavy lifting", 960, 540',
       '"crew-hivis.webp", "RGC trailer on site — hauling and cleanouts", 1600, 1200', "hub junk")

# ---------- 4) GALLERY_ITEMS ----------
i0 = b.index("GALLERY_ITEMS = [")
i1 = b.index("]\n\nCATS") + 1
new_g = '''GALLERY_ITEMS = [
    ("siding", "Completed re-side, two-story", "siding-house.webp", "Completed two-story home with dark lap siding and fresh gutters", 1600, 1200),
    ("siding", "Gable corner, stone & timber", "framing-timber.webp", "Siding gable corner with stone column and timber accents", 1200, 1600),
    ("siding", "Dark lap siding corner detail", "craft-hands.webp", "Close-up of dark lap siding corner and trim detail", 1200, 1600),
    ("siding", "Modern panel cladding", "tools-hammer.webp", "Modern cream panel cladding with black metal accents", 1200, 1600),
    ("framing", "Roof structure framed & braced", "framing-aerial.webp", "Residential build at framing stage with gable roof structure", 1600, 1200),
    ("framing", "Second story, framed", "framing-vert.webp", "Two-story home framed with lumber staged on site", 1200, 899),
    ("roofing", "Reroof in progress", "roofing-worker.webp", "Roof deck with battens and panels staged during a reroof", 1600, 2133),
    ("demolition", "Interior gut-out & haul-off", "demolition-excavator.webp", "Interior gut-out with framing exposed and debris staged", 1600, 2133),
    ("junk", "RGC trailer on site", "crew-hivis.webp", "RGC trailer parked on a Central Oregon job site", 1600, 1200),
    ("projects", "Modern home & fire-pit patio", "project-patio.webp", "Completed modern home with paved patio and fire pit", 1600, 1200),
    ("projects", "Farmhouse build, finished", "project-farmhouse.webp", "Completed white farmhouse-style home with covered porch", 1600, 1200),
    ("projects", "Garage & entry, finished", "project-garage.webp", "Completed modern home with garage and wood accent entry", 1600, 1200),
    ("projects", "Craftsman exterior, finished", "project-craftsman.webp", "Completed craftsman home with stone and cedar details", 1600, 1200),
    ("projects", "Dark modern facade", "modern-dark.webp", "Dark modern cladding facade against the sky", 1200, 1600),
    ("siding", "Porch & cedar columns tour", "videos/siding-tour.mp4", "Walking tour of a cedar column porch with fresh siding", None, None),
    ("projects", "Interior finish walkthrough", "videos/interior-tour.mp4", "Walking tour of a finished interior with wood floors", None, None),
]'''
b = b[:i0] + new_g + b[i1:]
print("gallery: reemplazada")

old_cats = 'CATS = [("all", "All work"), ("siding", "Siding"), ("framing", "Framing"), ("roofing", "Roofing"), ("demolition", "Demolition"), ("junk", "Junk Removal"), ("crew", "Our Crew")]'
new_cats = 'CATS = [("all", "All work"), ("siding", "Siding"), ("framing", "Framing"), ("roofing", "Roofing"), ("demolition", "Demolition"), ("junk", "Junk Removal"), ("projects", "Finished Projects")]'
assert old_cats in b, "cats"
b = b.replace(old_cats, new_cats)

# ---------- 5) generador de items con video ----------
i0 = b.index("for cat, cap, img, alt, w, h in GALLERY_ITEMS:")
i1 = b.index('gallery_main += """        </div>\n        <p class="form-note" style="margin-top:1.4rem">')
new_item = '''CAT_LABELS = dict((k, l) for k, l in CATS)
for cat, cap, path, alt, w, h in GALLERY_ITEMS:
    if path.endswith(".mp4"):
        gallery_main += f"""          <button class="gitem" type="button" data-cat="{cat}" data-caption="{cap}" data-video="/{path}">
            <video src="/{path}" muted playsinline preload="metadata" tabindex="-1"></video>
            <span class="play-badge" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>
            <figcaption>{cap} <span class="tag">Video · {CAT_LABELS[cat]}</span></figcaption>
          </button>
"""
    else:
        thumb = path.replace(".webp", "-640.webp") if w > 700 else path
        gallery_main += f"""          <button class="gitem" type="button" data-cat="{cat}" data-caption="{cap}" data-full="/img/photos/{path}">
            <img src="/img/photos/{thumb}" alt="{alt}" loading="lazy" width="680" height="510">
            <figcaption>{cap} <span class="tag">{CAT_LABELS[cat]}</span></figcaption>
          </button>
"""
'''
b = b[:i0] + new_item + b[i1:]
print("generador de items: reemplazado")

# ---------- 6) lightbox con video ----------
old_lb = '''      <img src="" alt="">
      <p class="lightbox__cap"></p>'''
assert old_lb in b, "lightbox"
b = b.replace(old_lb, '''      <img src="" alt="">
      <video class="lightbox__video" controls playsinline preload="metadata"></video>
      <p class="lightbox__cap"></p>''')
b = b.replace('aria-label="Image viewer"', 'aria-label="Media viewer"')

# ---------- 7) about con fotos reales ----------
re_sub(r'<img src="/img/photos/crew-hivis\.webp" alt="[^"]*" loading="lazy" width="1024" height="681">',
       '<img src="/img/photos/crew-hivis.webp" alt="RGC trailer on a Central Oregon job site" loading="lazy" width="1600" height="1200">',
       "about trailer")
re_sub(r'<img src="/img/photos/tools-hammer\.webp" alt="[^"]*" loading="lazy" width="960" height="641">',
       '<img src="/img/photos/project-patio.webp" alt="Completed modern home with fire-pit patio built in Central Oregon" loading="lazy" width="1600" height="1200">',
       "about service-area")

# ---------- 8) cache-bust v12 ----------
b = b.replace('?v=11"', '?v=12"')
open(p, "w", encoding="utf-8").write(b)
print("builder guardado:", len(b))
