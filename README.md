# Roque General Construction LLC — Sitio web

Sitio estático (HTML/CSS/JS vanilla + `server.py`) para **Roque General Construction LLC**
— general contractor en Bend, Oregon. Siding · Framing · Roofing Repairs · Demolition · Junk Removal.

- Marca: negro `#0a0a0c` + rojo RGC `#ee1111` + blanco (derivada del logo y la tarjeta del cliente).
- Tipografías: Anton (display) + Manrope (texto), Google Fonts.
- 10 páginas indexables + 404: `/`, `/about`, `/services`, `/services/{siding,framing,roofing-repairs,demolition,junk-removal}`, `/gallery`, `/contact`.
- SEO: titles/descriptions únicos, canonical, OG/Twitter, geo tags, JSON-LD `@graph`
  (GeneralContractor + WebSite + WebPage + OfferCatalog + BreadcrumbList + Service por página + FAQPage), `sitemap.xml`, `robots.txt`.

## ⚠️ Pendientes del cliente (reemplazar antes de producción)

| # | Pendiente | Dónde |
|---|-----------|-------|
| 1 | **Número de licencia CCB** (la tarjeta traía placeholder `000000`). El sitio muestra "Oregon CCB" **sin número** en toda la UI y sin `identifier` en el JSON-LD. Cuando el cliente dé el número real: buscar `Oregon CCB` en los HTML y añadir `identifier` al JSON-LD del home. | grep `CCB` |
| 2 | **Dominio placeholder `roquegeneralconstruction.com`**. Reemplazar en canonicals, OG, JSON-LD, sitemap y robots cuando se confirme el dominio real. | grep `roquegeneralconstruction.com` + `sitemap.xml` + `robots.txt` |
| 3 | **Formulario**: usa FormSubmit hacia `marioroque@yahoo.com`. **El primer envío real genera un correo de activación de FormSubmit** — hay que hacer clic una sola vez para habilitar la entrega. Ver "Formulario" abajo. | `contact.html` |
| 4 | **Facebook**: la tarjeta dice "VISIT US" con QR a Facebook. Enlazar la URL real de la página cuando el cliente la confirme (se puede añadir a `sameAs` del JSON-LD). | — |
| 5 | **Testimonios de ejemplo** (Sarah M./Diego R./Kelli T.) — reemplazar por reseñas reales del cliente cuando las tenga. No marcar con schema Review hasta que sean reales. | `index.html` |
| 6 | **Fotos**: son imágenes representativas CC0 (ver `CREDITS.md`). Sustituir por fotos reales de proyectos del cliente en cuanto las tenga (misma ruta/nombre `img/photos/*.webp`). | `img/photos/` |
| 7 | **Horarios** asumidos L–V 7–6, Sáb 8–2 (la tarjeta no los trae). Confirmar. | footer, contact, JSON-LD `openingHoursSpecification` |
| 8 | Código postal `97701` asumido para Bend (el cliente no dio dirección). Confirmar o dejar solo localidad. | JSON-LD |
| 9 | Rangos de precios orientativos por servicio — validarlos con Mario. | páginas de servicio, sección "Ballpark" |

## Estructura

```
index.html  about.html  services.html  gallery.html  contact.html  404.html
services/   siding.html  framing.html  roofing-repairs.html  demolition.html  junk-removal.html
css/styles.css   js/main.js
img/             logo, favicons, og-image, photos/ (webp)
server.py        rutas amigables + 301 + modo demo + seguridad
tools/           build_pages.py (regenera las páginas interiores), cloudflared.exe (no se sube)
demo.py + demo-server.bat   demo pública para el cliente vía Cloudflare Tunnel
Dockerfile       despliegue en Coolify (puerto por $PORT)
```

## Editar contenido

Las páginas interiores se generan con `tools/build_pages.py` (mantiene header/footer/SEO
idénticos en todo el sitio). Editar ahí y regenerar:

```bash
python tools/build_pages.py
```

`index.html` es independiente (éditarlo directamente). Después de cualquier cambio de CSS/JS,
subir la versión `?v=n` en los `<link>`/`<script>` (cache-busting).

## Formulario (FormSubmit, sin cuenta)

- Endpoint AJAX: `https://formsubmit.co/ajax/marioroque@yahoo.com` en `contact.html`.
- **Activación única**: al primer envío real, FormSubmit manda un correo de confirmación a
  `marioroque@yahoo.com`; hacer clic en "Activate" y a partir de ahí llegan todos.
- Anti-spam: honeypot `_honey` + validación en cliente. Si el servicio falla, hay fallback
  automático a `mailto:` pre-llenado.

## Probar en local

```bash
python server.py          # http://localhost:8080 (producción local)
DEMO=1 python server.py   # modo demo: noindex + sin caché
```

## Demo para el cliente

Doble clic en `demo-server.bat` → copiar la URL `https://*.trycloudflare.com`
(también queda en `demo-url.txt`) y enviarla. El enlace vive mientras la ventana esté abierta.

## Despliegue (Coolify)

1. Subir el repo a GitHub (sin `tools/cloudflared.exe`, ya está en `.gitignore`).
2. Coolify → nuevo recurso → conectar el repo → detecta el `Dockerfile`.
3. Asignar dominio y verificar: rutas limpias, 301 de `.html`, formulario, `/sitemap.xml`, `/robots.txt`, `/healthz`.
4. Google Search Console: enviar `sitemap.xml`. Crear/perfil de Google Business para el SEO local.
