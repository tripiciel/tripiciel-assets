(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  addEventListener('load', () => document.body.classList.add('loaded'));
  setTimeout(() => document.body.classList.add('loaded'), 2500);

  // Año
  const y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();

  // Hero palabra por palabra
  document.querySelectorAll('#hero-title .w').forEach((w, i) => w.style.animationDelay = (0.15 + i * 0.16) + 's');


  // Palabras animadas en títulos
  const splitWords = (el) => {
    let i = 0;
    const walk = (node, inSerif) => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.append(part); return; }
            const s = document.createElement('span');
            s.className = 'wd' + (inSerif ? ' serif shine' : '');
            s.textContent = part; s.style.transitionDelay = (i++ * 0.07) + 's';
            frag.append(s);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'svg') {
          const serif = n.classList.contains('serif');
          if (serif) { n.classList.remove('serif'); n.classList.add('serif-wrap'); }
          walk(n, inSerif || serif);
        }
      });
    };
    el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    walk(el, false); el.classList.add('split');
  };
  document.querySelectorAll('.head h2, .bot h2, .final h2, .builder h3, .about h2').forEach(splitWords);

  // Menú
  const nav = document.getElementById('nav'), burger = document.getElementById('burger');
  addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 20), { passive: true });
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  });
  document.querySelectorAll('#menu a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false');
  }));

  // Aparecer al hacer scroll
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add(e.target.classList.contains('rv') ? 'in' : 'go'); io.unobserve(e.target); }
  }), { threshold: 0.18 });
  const watch = () => document.querySelectorAll('.rv:not(.in)').forEach(el => io.observe(el));
  watch();
  ['problema', 'steps'].forEach(id => { const el = document.getElementById(id); if (el) io.observe(el); });

  // Casos (data/casos.json)
  const star = '<svg viewBox="0 0 100 100" aria-hidden="true"><path fill="currentColor" d="M50 2C55 36 64 45 98 50C64 55 55 64 50 98C45 64 36 55 2 50C36 45 45 36 50 2Z"/></svg>';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const casesEl = document.getElementById('cases');
  fetch('data/casos.json').then(r => r.json()).then(casos => {
    casesEl.innerHTML = casos.map((c, i) => `
      <article class="case rv ${i % 2 ? 'd1' : ''}">
        <div class="vid">
          <video muted loop playsinline preload="none" poster="${esc(c.poster)}" data-src="${esc(c.preview)}" aria-hidden="true"></video>
          <button class="play" data-full="${esc(c.video)}" aria-label="Ver el video de ${esc(c.cliente)} en grande y con sonido"><span><svg viewBox="0 0 24 24" fill="#fff"><path d="M7 4l13 8-13 8z"/></svg></span></button>
        </div>
        <div>
          <div class="tags"><span class="tag">Antes</span><span class="tag ad">Después</span></div>
          <h3>${esc(c.cliente)}</h3>
          <p class="rubro">${esc(c.rubro)}</p>
          <ul>${c.hicimos.map(h => `<li>${esc(h)}</li>`).join('')}</ul>
          <p class="dato"><b>${esc(c.datoCifra)}</b> ${esc(c.datoTexto)}</p>
        </div>
      </article>`).join('');
    watch();
    // Carga diferida de las vistas previas
    const vio = new IntersectionObserver(es => es.forEach(e => {
      const v = e.target;
      if (e.isIntersecting) {
        if (!v.src) v.src = v.dataset.src;
        if (!reduce) v.play().catch(() => {});
      } else v.pause();
    }), { rootMargin: '200px' });
    casesEl.querySelectorAll('video').forEach(v => vio.observe(v));
  }).catch(() => {
    casesEl.innerHTML = '<p class="lead">No pudimos cargar los trabajos. Escríbenos y te los mostramos.</p>';
  });

  // Modal de video
  const modal = document.getElementById('modal'), mv = document.getElementById('modalVideo');
  let lastFocus = null;
  const close = () => { mv.pause(); mv.removeAttribute('src'); mv.load(); modal.classList.remove('open'); document.body.style.overflow = ''; lastFocus && lastFocus.focus(); };
  casesEl.addEventListener('click', e => {
    const b = e.target.closest('.play'); if (!b) return;
    lastFocus = b; mv.src = b.dataset.full; modal.classList.add('open'); document.body.style.overflow = 'hidden';
    mv.play().catch(() => {}); document.getElementById('modalClose').focus();
  });
  document.getElementById('modalClose').addEventListener('click', close);
  modal.addEventListener('click', e => { if (e.target === modal) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && modal.classList.contains('open')) close(); });

  // Arma tu presupuesto
  const WHATSAPP = ''; // Número con código de país, sin + ni espacios. Ej.: 5491122334455
  const b = document.getElementById('armar');
  if (b) {
    const count = document.getElementById('bCount'), list = document.getElementById('bList'), note = document.getElementById('bNote');
    const wa = document.getElementById('bWa'), ig = document.getElementById('bIg');
    let pedido = '';
    const update = () => {
      const items = [...b.querySelectorAll('.opt')].filter(o => o.querySelector('input').checked).map(o => {
        const out = o.querySelector('output'), nm = o.querySelector('.nm').textContent;
        return out ? `${out.textContent} ${nm.toLowerCase()}` : nm;
      });
      count.textContent = items.length;
      list.textContent = items.length ? items.join(' · ') : 'Marca al menos un servicio para armar tu pedido.';
      pedido = 'Hola, Tripiciel. TRIPI. Quiero una propuesta para: ' + items.join(', ') + '.';
      [wa, ig].forEach(x => { x.classList.toggle('is-off', !items.length); x.setAttribute('aria-disabled', !items.length); });
      wa.href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(pedido)}`;
    };
    b.addEventListener('change', update);
    b.querySelectorAll('.qty button').forEach(btn => btn.addEventListener('click', e => {
      e.preventDefault(); e.stopPropagation();
      const out = btn.parentElement.querySelector('output');
      out.textContent = Math.min(30, Math.max(1, (+out.textContent) + (btn.classList.contains('q+') ? 2 : -2))); update();
    }));
    [wa, ig].forEach(x => x.addEventListener('click', e => { if (x.classList.contains('is-off')) e.preventDefault(); }));
    ig.addEventListener('click', () => {
      if (ig.classList.contains('is-off')) return;
      if (navigator.clipboard) navigator.clipboard.writeText(pedido).then(
        () => { note.textContent = '¡Pedido copiado! Pégalo en el chat de Instagram.'; },
        () => { note.textContent = 'Copia y envíanos: ' + pedido; });
      else note.textContent = 'Copia y envíanos: ' + pedido;
    });
    update();
  }

  // Fondo: estelas y brillitos
  const cv = document.getElementById('sky');
  if (cv) {
    const ctx = cv.getContext('2d'); let W, H, dpr, stars = [], trails = [], last = 0;
    const resize = () => {
      dpr = Math.min(devicePixelRatio || 1, 2); W = innerWidth; H = innerHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(W * H / 16000);
      stars = Array.from({ length: n }, () => ({ x: Math.random() * W, y: Math.random() * H, r: Math.random() * 1.3 + .3, p: Math.random() * 6.28, s: Math.random() * .8 + .3, big: Math.random() < .08 }));
    };
    const sparkle = (x, y, r, a) => {
      ctx.save(); ctx.translate(x, y); ctx.globalAlpha = a; ctx.fillStyle = '#C9C1FF';
      ctx.beginPath(); ctx.moveTo(0, -r * 4); ctx.quadraticCurveTo(0, 0, r * 4, 0); ctx.quadraticCurveTo(0, 0, 0, r * 4); ctx.quadraticCurveTo(0, 0, -r * 4, 0); ctx.quadraticCurveTo(0, 0, 0, -r * 4); ctx.fill(); ctx.restore();
    };
    const spawn = () => {
      const fromTop = Math.random() < .6;
      trails.push({ x: fromTop ? Math.random() * W * 1.2 : W + 40, y: fromTop ? -40 : Math.random() * H * .6, vx: -(Math.random() * 3 + 4), vy: Math.random() * 1.6 + 1.6, len: Math.random() * 160 + 120, life: 0, max: Math.random() * 90 + 110, hue: Math.random() < .5 ? '169,156,255' : '91,91,245' });
    };
    let next = 800;
    const draw = (t) => {
      const dt = Math.min(t - last, 50); last = t;
      ctx.clearRect(0, 0, W, H);
      for (const s of stars) {
        const a = reduce ? .45 : (Math.sin(t / 1000 * s.s + s.p) + 1) / 2;
        if (s.big) sparkle(s.x, s.y, s.r, a * .85);
        else { ctx.globalAlpha = a * .7; ctx.fillStyle = '#F6F2EA'; ctx.beginPath(); ctx.arc(s.x, s.y, s.r * .8, 0, 6.28); ctx.fill(); }
      }
      if (!reduce) {
        next -= dt; if (next <= 0) { spawn(); next = Math.random() * 2200 + 1400; }
        trails = trails.filter(tr => tr.life < tr.max);
        for (const tr of trails) {
          tr.life++; tr.x += tr.vx; tr.y += tr.vy;
          const fade = Math.sin(Math.PI * tr.life / tr.max) * .55;
          const n = Math.hypot(tr.vx, tr.vy), ex = tr.x - tr.vx / n * tr.len, ey = tr.y - tr.vy / n * tr.len;
          const g = ctx.createLinearGradient(tr.x, tr.y, ex, ey);
          g.addColorStop(0, `rgba(${tr.hue},${fade})`); g.addColorStop(1, `rgba(${tr.hue},0)`);
          ctx.globalAlpha = 1; ctx.strokeStyle = g; ctx.lineWidth = 1.6; ctx.lineCap = 'round';
          ctx.beginPath(); ctx.moveTo(tr.x, tr.y); ctx.lineTo(ex, ey); ctx.stroke();
          sparkle(tr.x, tr.y, .9, fade);
        }
      }
      ctx.globalAlpha = 1;
      if (!reduce) requestAnimationFrame(draw);
    };
    resize(); addEventListener('resize', resize);
    requestAnimationFrame(draw);
  }

  // Demo del bot
  const chat = document.getElementById('chat');
  const msgs = [...document.querySelectorAll('#chatBody .msg')], typing = document.getElementById('typing');
  const runChat = () => {
    if (reduce) { msgs.forEach(m => m.classList.add('show')); return; }
    let t = 300;
    msgs.forEach(m => {
      if (m.classList.contains('out')) {
        setTimeout(() => { m.before(typing); typing.classList.add('show'); }, t); t += 1100;
        setTimeout(() => { typing.classList.remove('show'); m.classList.add('show'); }, t); t += 500;
      } else { setTimeout(() => m.classList.add('show'), t); t += 1300; }
    });
  };
  const cio = new IntersectionObserver(es => { if (es[0].isIntersecting) { runChat(); cio.disconnect(); } }, { threshold: 0.4 });
  cio.observe(chat);
})();
