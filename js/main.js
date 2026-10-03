/* =========================================================
   ROQUE GENERAL CONSTRUCTION LLC — JS principal (vanilla)
   Header, drawer, reveal, contadores, galería + lightbox,
   FAQ, formulario (FormSubmit + fallback mailto), back-top
   ========================================================= */
(function () {
  'use strict';

  var d = document;
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Año del footer ---------- */
  d.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  /* ---------- Header: sombra al hacer scroll ---------- */
  var header = d.querySelector('.site-header');
  if (header) {
    var onScrollHeader = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 24);
    };
    window.addEventListener('scroll', onScrollHeader, { passive: true });
    onScrollHeader();
  }

  /* ---------- Hero video: pausa si prefiere menos movimiento ---------- */
  var heroVideo = d.querySelector('.hero__bg');
  if (heroVideo && prefersReduced) {
    heroVideo.removeAttribute('autoplay');
    heroVideo.pause();
  }

  /* ---------- Drawer móvil ---------- */
  var drawer = d.getElementById('drawer');
  var navToggle = d.querySelector('.nav-toggle');
  var lastFocus = null;

  function openDrawer() {
    if (!drawer) return;
    lastFocus = d.activeElement;
    drawer.classList.add('open');
    d.body.classList.add('nav-open');
    d.body.dataset.scrollY = String(window.scrollY);
    d.body.style.position = 'fixed';
    d.body.style.top = '-' + d.body.dataset.scrollY + 'px';
    d.body.style.width = '100%';
    navToggle && navToggle.setAttribute('aria-expanded', 'true');
    var first = drawer.querySelector('a, button, summary');
    first && first.focus();
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove('open');
    d.body.classList.remove('nav-open');
    d.body.style.position = '';
    d.body.style.top = '';
    d.body.style.width = '';
    var ry = parseInt(d.body.dataset.scrollY || '0', 10);
    var htmlEl = d.documentElement;
    var prevSb = htmlEl.style.scrollBehavior;
    htmlEl.style.scrollBehavior = 'auto'; // evita el "scroll fantasma" animado
    window.scrollTo(0, ry);
    htmlEl.style.scrollBehavior = prevSb;
    navToggle && navToggle.setAttribute('aria-expanded', 'false');
    drawer.querySelectorAll('details[open]').forEach(function (det) { det.removeAttribute('open'); });
    lastFocus && lastFocus.focus();
  }
  if (navToggle && drawer) {
    navToggle.addEventListener('click', function () {
      drawer.classList.contains('open') ? closeDrawer() : openDrawer();
    });
    drawer.querySelector('.drawer__scrim') && drawer.querySelector('.drawer__scrim').addEventListener('click', closeDrawer);
    drawer.querySelector('.drawer__close') && drawer.querySelector('.drawer__close').addEventListener('click', closeDrawer);
    d.addEventListener('keydown', function (e) {
      if (!drawer.classList.contains('open')) return;
      if (e.key === 'Escape') { closeDrawer(); return; }
      if (e.key === 'Tab') {
        // focus trap ligero
        var focusables = drawer.querySelectorAll('a[href], button:not([disabled]), summary');
        if (!focusables.length) return;
        var first = focusables[0], last = focusables[focusables.length - 1];
        if (e.shiftKey && d.activeElement === first) { last.focus(); e.preventDefault(); }
        else if (!e.shiftKey && d.activeElement === last) { first.focus(); e.preventDefault(); }
      }
    });
    // Cerrar al navegar un enlace del drawer
    drawer.querySelectorAll('nav a').forEach(function (a) {
      a.addEventListener('click', closeDrawer);
    });
  }

  /* ---------- Dropdown de servicios (desktop): cerrar al hacer clic fuera ---------- */
  d.querySelectorAll('details.nav-item').forEach(function (det) {
    d.addEventListener('click', function (e) {
      if (det.hasAttribute('open') && !det.contains(e.target)) det.removeAttribute('open');
    });
    det.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { det.removeAttribute('open'); det.querySelector('summary').focus(); }
    });
  });

  /* ---------- Reveal on scroll ---------- */
  var revealEls = d.querySelectorAll('.reveal');
  if (revealEls.length) {
    if (prefersReduced || !('IntersectionObserver' in window)) {
      revealEls.forEach(function (el) { el.classList.add('in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
        });
      }, { threshold: 0.14, rootMargin: '0px 0px -6% 0px' });
      revealEls.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---------- Contadores animados ---------- */
  var counters = d.querySelectorAll('[data-counter]');
  if (counters.length) {
    var animate = function (el) {
      var target = parseFloat(el.getAttribute('data-counter'));
      var dec = (String(el.getAttribute('data-counter')).split('.')[1] || '').length;
      var dur = prefersReduced ? 0 : 1500;
      var t0 = null;
      var step = function (t) {
        if (!t0) t0 = t;
        var p = Math.min((t - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = (target * eased).toFixed(dec);
        if (p < 1) requestAnimationFrame(step);
        else el.textContent = target.toFixed(dec);
      };
      requestAnimationFrame(step);
    };
    if (prefersReduced || !('IntersectionObserver' in window)) {
      counters.forEach(function (el) { el.textContent = el.getAttribute('data-counter'); });
    } else {
      var ioC = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { animate(en.target); ioC.unobserve(en.target); }
        });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { ioC.observe(el); });
    }
  }

  /* ---------- Galería: filtros ---------- */
  var filterBar = d.querySelector('.gallery-filters');
  if (filterBar) {
    var items = d.querySelectorAll('.gitem');
    filterBar.addEventListener('click', function (e) {
      var btn = e.target.closest('.gf');
      if (!btn) return;
      filterBar.querySelectorAll('.gf').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });
      var f = btn.getAttribute('data-filter');
      items.forEach(function (it) {
        var show = f === 'all' || it.getAttribute('data-cat') === f;
        it.hidden = !show;
      });
    });
  }

  /* ---------- Lightbox ---------- */
  var lightbox = d.getElementById('lightbox');
  if (lightbox) {
    var lbImg = lightbox.querySelector('img');
    var lbVideo = lightbox.querySelector('.lightbox__video');
    var lbCap = lightbox.querySelector('.lightbox__cap');
    var lbItems = [];
    var lbIndex = 0;
    var lbOpener = null;

    var visibleGalleryItems = function () {
      return Array.prototype.slice.call(d.querySelectorAll('.gitem:not([hidden])'));
    };
    var renderLb = function () {
      var it = lbItems[lbIndex];
      if (!it) return;
      var vid = it.getAttribute('data-video');
      if (vid) {
        lbImg.style.display = 'none';
        lbVideo.style.display = 'block';
        if (lbVideo.getAttribute('src') !== vid) lbVideo.src = vid;
        lbVideo.muted = true; // autoplay permitido; el usuario activa sonido desde los controles
        lbVideo.play().catch(function () {});
        lbCap.textContent = it.getAttribute('data-caption') || '';
        return;
      }
      lbVideo.pause();
      lbVideo.removeAttribute('src');
      lbVideo.style.display = 'none';
      var img = it.querySelector('img');
      var full = it.getAttribute('data-full') || img.currentSrc || img.src;
      lbImg.style.display = 'block';
      lbImg.src = full;
      lbImg.alt = img.alt || '';
      lbCap.textContent = it.getAttribute('data-caption') || img.alt || '';
    };
    var openLb = function (it) {
      lbItems = visibleGalleryItems();
      lbIndex = lbItems.indexOf(it);
      if (lbIndex < 0) return;
      lbOpener = it;
      renderLb();
      lightbox.classList.add('open');
      d.body.dataset.scrollY = String(window.scrollY);
      d.body.style.position = 'fixed';
      d.body.style.top = '-' + d.body.dataset.scrollY + 'px';
      d.body.style.width = '100%';
      lightbox.querySelector('.lightbox__close').focus();
    };
    var closeLb = function () {
      lightbox.classList.remove('open');
      lbVideo.pause();
      lbVideo.removeAttribute('src');
      lightbox.querySelector('img').src = '';
      d.body.style.position = '';
      d.body.style.top = '';
      d.body.style.width = '';
      var ry = parseInt(d.body.dataset.scrollY || '0', 10);
      var htmlEl = d.documentElement;
      var prevSb = htmlEl.style.scrollBehavior;
      htmlEl.style.scrollBehavior = 'auto';
      window.scrollTo(0, ry);
      htmlEl.style.scrollBehavior = prevSb;
      lbOpener && lbOpener.focus();
    };
    var moveLb = function (delta) {
      if (!lbItems.length) return;
      lbIndex = (lbIndex + delta + lbItems.length) % lbItems.length;
      renderLb();
    };

    d.querySelectorAll('.gitem').forEach(function (it) {
      it.addEventListener('click', function () { openLb(it); });
    });
    lightbox.querySelector('.lightbox__close').addEventListener('click', closeLb);
    lightbox.querySelector('.lightbox__prev').addEventListener('click', function () { moveLb(-1); });
    lightbox.querySelector('.lightbox__next').addEventListener('click', function () { moveLb(1); });
    lightbox.addEventListener('click', function (e) { if (e.target === lightbox) closeLb(); });
    d.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape') closeLb();
      else if (e.key === 'ArrowLeft') moveLb(-1);
      else if (e.key === 'ArrowRight') moveLb(1);
    });
  }

  /* ---------- FAQ: cerrar otros details del mismo grupo ---------- */
  d.querySelectorAll('.faq').forEach(function (group) {
    var detas = group.querySelectorAll('details');
    detas.forEach(function (det) {
      det.addEventListener('toggle', function () {
        if (det.hasAttribute('open')) {
          detas.forEach(function (o) { if (o !== det) o.removeAttribute('open'); });
        }
      });
    });
  });

  /* ---------- Formulario de cotización ---------- */
  var form = d.querySelector('form.quote-form');
  if (form) {
    var status = form.querySelector('.form-status');
    var submitBtn = form.querySelector('button[type="submit"]');
    var FORM_ENDPOINT = form.getAttribute('action'); // FormSubmit AJAX endpoint

    var setError = function (field, on) {
      var wrap = field.closest('.field');
      wrap && wrap.classList.toggle('invalid', on);
      field.setAttribute('aria-invalid', on ? 'true' : 'false');
    };
    var validate = function () {
      var ok = true;
      form.querySelectorAll('[required]').forEach(function (f) {
        var valid = f.type === 'checkbox' ? f.checked : f.value.trim().length > 0;
        if (valid && f.type === 'email') valid = /^\S+@\S+\.\S+$/.test(f.value.trim());
        if (valid && f.type === 'tel') valid = f.value.replace(/\D/g, '').length >= 7;
        setError(f, !valid);
        if (!valid) ok = false;
      });
      return ok;
    };
    form.querySelectorAll('[required]').forEach(function (f) {
      f.addEventListener('blur', function () { setError(f, f.value.trim().length === 0); });
      f.addEventListener('input', function () { setError(f, false); });
    });

    var mailtoFallback = function () {
      var subject = encodeURIComponent('Free Estimate Request — Roque General Construction website');
      var bodyLines = [];
      form.querySelectorAll('input:not([type="hidden"]):not(.hp-field input), select, textarea').forEach(function (f) {
        if (f.name && !f.closest('.hp-field')) bodyLines.push(f.name + ': ' + (f.value || ''));
      });
      window.location.href = 'mailto:marioroque@yahoo.com?subject=' + subject + '&body=' + encodeURIComponent(bodyLines.join('\n'));
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      status.className = 'form-status';
      status.textContent = '';
      if (!validate()) {
        status.classList.add('fail');
        status.textContent = 'Please check the highlighted fields and try again.';
        return;
      }
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }

      var data = new FormData(form);
      fetch(FORM_ENDPOINT, {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json' }
      }).then(function (res) {
        if (res.ok) return res.json().catch(function () { return {}; });
        throw new Error('HTTP ' + res.status);
      }).then(function () {
        status.classList.add('ok');
        status.textContent = 'Thank you! Your request was sent. Mario will get back to you shortly — usually within one business day.';
        form.reset();
      }).catch(function () {
        status.classList.add('fail');
        status.textContent = 'The form could not be sent. Opening your email app as a backup…';
        setTimeout(mailtoFallback, 900);
      }).finally(function () {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Send My Free Estimate Request'; }
      });
    });
  }

  /* ---------- Scroll horizontal piloteado ---------- */
  var hs = d.querySelector('.hscroll');
  if (hs) {
    var track = hs.querySelector('.hscroll__track');
    var hsPinned = false;
    var hsApply = function () {
      var rect = hs.getBoundingClientRect();
      var total = hs.offsetHeight - window.innerHeight;
      var progress = total > 0 ? Math.min(Math.max(-rect.top / total, 0), 1) : 0;
      var dist = track.scrollWidth - window.innerWidth;
      track.style.transform = 'translate3d(' + (-progress * dist).toFixed(1) + 'px,0,0)';
    };
    var setMode = function () {
      var wantPinned = !prefersReduced && window.matchMedia('(min-width: 861px)').matches;
      if (wantPinned && !hsPinned) {
        hsPinned = true;
        hs.classList.remove('hs-static');
        window.addEventListener('scroll', hsApply, { passive: true });
        window.addEventListener('resize', hsApply);
      } else if (!wantPinned && hsPinned) {
        hsPinned = false;
        hs.classList.add('hs-static');
        track.style.transform = '';
        window.removeEventListener('scroll', hsApply);
        window.removeEventListener('resize', hsApply);
      } else if (wantPinned) {
        hsApply();
      }
    };
    setMode();
    window.addEventListener('resize', setMode);
    // indicación de swipe: empujoncito una sola vez cuando la sección entra en vista
    var nudge = function () {
      if (prefersReduced || track.scrollLeft > 20) return;
      track.scrollBy({ left: 110, behavior: 'smooth' });
      setTimeout(function () { track.scrollBy({ left: -110, behavior: 'smooth' }); }, 480);
    };
    if (hs.classList.contains('hs-static') && 'IntersectionObserver' in window) {
      var ioNudge = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { nudge(); ioNudge.disconnect(); }
        });
      }, { threshold: 0.35 });
      ioNudge.observe(hs);
    }
  }

  /* ---------- Back to top ---------- */
  var backTop = d.querySelector('.back-top');
  if (backTop) {
    window.addEventListener('scroll', function () {
      backTop.classList.toggle('show', window.scrollY > 600);
    }, { passive: true });
    backTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: prefersReduced ? 'auto' : 'smooth' });
    });
  }
})();
