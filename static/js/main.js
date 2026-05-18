// ─── HAMBURGER ────────────────────────────────────────────────────────────────
const hamburgerBtn  = document.getElementById('hamburgerBtn');
const hamburgerIcon = document.getElementById('hamburgerIcon');
const mobileMenu    = document.getElementById('mobileMenu');

hamburgerBtn.addEventListener('click', () => {
  const isOpen = mobileMenu.classList.toggle('open');
  hamburgerIcon.className = isOpen ? 'fas fa-xmark' : 'fas fa-bars';
  hamburgerBtn.setAttribute('aria-label', isOpen ? 'Fermer le menu' : 'Ouvrir le menu');
  hamburgerBtn.setAttribute('aria-expanded', isOpen);
});

function closeMobileMenu() {
  mobileMenu.classList.remove('open');
  hamburgerIcon.className = 'fas fa-bars';
  hamburgerBtn.setAttribute('aria-label', 'Ouvrir le menu');
  hamburgerBtn.setAttribute('aria-expanded', 'false');
}

// ─── SCROLL FADE-IN ───────────────────────────────────────────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// ─── SMOOTH SCROLL ────────────────────────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      window.scrollTo({ top: target.offsetTop - 80, behavior: 'smooth' });
    }
  });
});

// ─── BARRE DE LECTURE ─────────────────────────────────────────────────────────
(function () {
  const bar = document.getElementById('read-progress');
  if (!bar) return;
  let rafPending = false;
  window.addEventListener('scroll', () => {
    if (!rafPending) {
      rafPending = true;
      requestAnimationFrame(() => {
        const scrollable = document.body.scrollHeight - window.innerHeight;
        const pct = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
        bar.style.width = pct + '%';
        rafPending = false;
      });
    }
  }, { passive: true });
})();

// ─── NAVBAR — shrink + hide/show + lien actif ─────────────────────────────────
(function () {
  const nav = document.querySelector('nav');
  if (!nav) return;
  const navAnchors = document.querySelectorAll('.nav-links a[href^="#"], .mobile-menu a[href^="#"]');
  let lastY = 0;
  let rafNav = false;

  window.addEventListener('scroll', () => {
    if (!rafNav) {
      rafNav = true;
      requestAnimationFrame(() => {
        const y = window.scrollY;
        nav.classList.toggle('nav--scrolled', y > 60);
        if (y > 100) {
          const isMobileOpen = mobileMenu && mobileMenu.classList.contains('open');
          if (!isMobileOpen) nav.classList.toggle('nav--hidden', y > lastY);
        } else {
          nav.classList.remove('nav--hidden');
        }
        lastY = y;
        rafNav = false;
      });
    }
  }, { passive: true });

  const sections = document.querySelectorAll('section[id]');
  if (sections.length) {
    const sectionObs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          navAnchors.forEach(a => a.classList.toggle('nav--active', a.getAttribute('href') === '#' + id));
        }
      });
    }, { threshold: 0.4 });
    sections.forEach(s => sectionObs.observe(s));
  }
})();

// ─── SCROLL REVEAL ────────────────────────────────────────────────────────────
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const revealObserver = (function () {
  const els = document.querySelectorAll('[class*="reveal-"]');
  if (prefersReducedMotion) {
    els.forEach(el => el.classList.add('is-visible'));
    return null;
  }
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target);
      }
    });
  }, { rootMargin: '-50px 0px', threshold: 0.12 });
  els.forEach(el => obs.observe(el));
  return obs;
})();

// ─── COMPTEURS ANIMÉS ─────────────────────────────────────────────────────────
(function () {
  const statsBand = document.querySelector('.stats-band');
  if (!statsBand) return;

  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }

  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const suffix = el.dataset.suffix || '';
    let start = parseInt(el.dataset.start || '0', 10);
    if (!el.dataset.start && target > 1000) start = Math.max(0, target - Math.round(target * 0.2));
    const duration = 1800;
    let startTime = null;
    function step(ts) {
      if (!startTime) startTime = ts;
      const progress = Math.min((ts - startTime) / duration, 1);
      const value = Math.round(start + (target - start) * easeOutCubic(progress));
      el.textContent = value.toLocaleString('fr-FR') + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  const statsObs = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.stat-number[data-target]').forEach(animateCounter);
      statsObs.unobserve(entry.target);
    }
  }, { threshold: 0.5 });
  statsObs.observe(statsBand);
})();

// ─── TIMELINE ─────────────────────────────────────────────────────────────────
(function () {
  const timeline = document.querySelector('.timeline');
  if (!timeline) return;
  if (prefersReducedMotion) {
    timeline.classList.add('is-visible');
    timeline.querySelectorAll('.timeline-item').forEach(el => el.classList.add('is-visible'));
    return;
  }
  const tlObs = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      timeline.classList.add('is-visible');
      timeline.querySelectorAll('.timeline-item').forEach((item, i) => {
        setTimeout(() => item.classList.add('is-visible'), i * 120);
      });
      tlObs.unobserve(timeline);
    }
  }, { threshold: 0.1 });
  tlObs.observe(timeline);
})();

// ─── PROGRAMME — stagger points ───────────────────────────────────────────────
(function () {
  if (prefersReducedMotion) {
    document.querySelectorAll('.axe-points li').forEach(li => li.classList.add('is-visible'));
    return;
  }
  document.querySelectorAll('.axe-card').forEach(card => {
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        card.querySelectorAll('.axe-points li').forEach((li, i) => {
          setTimeout(() => li.classList.add('is-visible'), i * 80);
        });
        obs.unobserve(card);
      }
    }, { threshold: 0.25 });
    obs.observe(card);
  });
})();

// ─── VISION QUOTE — mot par mot ───────────────────────────────────────────────
(function () {
  const quoteEl = document.querySelector('.vision-quote');
  if (quoteEl && !prefersReducedMotion && revealObserver) {
    const words = quoteEl.innerText.trim().split(/\s+/);
    quoteEl.innerHTML = words.map((w, i) =>
      `<span class="word reveal-up" style="display:inline-block;transition-delay:${i * 40}ms">${w}</span>`
    ).join(' ');
    quoteEl.querySelectorAll('.word').forEach(w => revealObserver.observe(w));
  }
})();

// ─── CAROUSEL HERO ────────────────────────────────────────────────────────────
(function () {
  const slides = document.querySelectorAll('#heroSlideshow .hero-slide');
  if (slides.length <= 1) return;
  let current = 0;
  setInterval(() => {
    slides[current].classList.remove('active');
    current = (current + 1) % slides.length;
    slides[current].classList.add('active');
  }, 3000);
})();

// ─── BOUTONS — RIPPLE ─────────────────────────────────────────────────────────
if (!prefersReducedMotion) {
  document.querySelectorAll('.btn-primary, .btn-outline').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const r = this.getBoundingClientRect();
      const size = Math.max(r.width, r.height) * 2;
      const ripple = document.createElement('span');
      ripple.className = 'btn-ripple';
      Object.assign(ripple.style, {
        width: size + 'px', height: size + 'px',
        left: (e.clientX - r.left - size / 2) + 'px',
        top:  (e.clientY - r.top  - size / 2) + 'px',
      });
      this.appendChild(ripple);
      ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
    });
  });
}

// ─── PUBLICATIONS — filtre par catégorie ──────────────────────────────────────
(function () {
  const grid       = document.getElementById('pubGrid');
  const noResult   = document.getElementById('pubNoResult');
  const filterBtns = document.querySelectorAll('.pub-filter-btn');
  const modal      = document.getElementById('pubModal');
  const modalClose = document.getElementById('pubModalClose');

  if (!grid) return;

  let activeFilter = 'all';

  function applyFilter() {
    const cards = Array.from(grid.querySelectorAll('.pub-card'));
    let visible = 0;
    cards.forEach(card => {
      const match = activeFilter === 'all' || card.dataset.category === activeFilter;
      card.style.display = match ? '' : 'none';
      if (match) visible++;
    });
    if (noResult) noResult.style.display = visible === 0 ? 'block' : 'none';
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeFilter = btn.dataset.filter;
      applyFilter();
    });
  });

  // ─── Modale publication ──────────────────────────────────────────────────
  if (!modal || !modalClose) return;

  function openModal(btn) {
    document.getElementById('modalBadge').textContent = btn.dataset.categoryLabel || '';
    document.getElementById('modalBadge').className =
      'pub-badge pub-badge--' + (btn.dataset.category || '');
    document.getElementById('modalTitle').textContent = btn.dataset.title || '';
    document.getElementById('modalMeta').textContent  =
      (btn.dataset.year || '') +
      (btn.dataset.institution ? '  ·  ' + btn.dataset.institution : '');
    document.getElementById('modalContent').textContent = btn.dataset.summary || '';
    const coverEl = document.getElementById('modalCover');
    const cover = btn.dataset.cover || '';
    if (cover) {
      coverEl.src = cover; coverEl.alt = btn.dataset.title; coverEl.style.display = '';
    } else {
      coverEl.src = ''; coverEl.style.display = 'none';
    }
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
    modalClose.focus();
  }

  function closeModal() {
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }

  grid.addEventListener('click', e => {
    const btn = e.target.closest('.pub-read-btn');
    if (btn) openModal(btn);
  });

  modalClose.addEventListener('click', closeModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
  });
})();

// ─── TABLEAU COMPARATIF DOUMBOUYA — reveal ligne par ligne ────────────────────
(function () {
  const rows = document.querySelectorAll('.comparison-row');
  if (!rows.length || prefersReducedMotion) {
    rows.forEach(r => r.classList.add('is-visible'));
    return;
  }
  const rowObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        rowObs.unobserve(entry.target);
      }
    });
  }, { rootMargin: '-30px 0px', threshold: 0.2 });
  rows.forEach(r => rowObs.observe(r));
})();
