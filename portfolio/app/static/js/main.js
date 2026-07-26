/* ═══════════════════════════════════════════════════════════════════
   NOOR ZAMAN PORTFOLIO — MAIN JAVASCRIPT
   Loading · Cursor · Theme · Particles · Typing · Counters · Nav
═══════════════════════════════════════════════════════════════════ */

'use strict';

/* ─── DOM Ready ──────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initLoadingScreen();
  initCustomCursor();
  initNavbar();
  initAOS();
  initParticles();
  initTypingAnimation();
  initCounters();
  initScrollReveal();
  initBackToTop();
  initAutoHideAlerts();
});

/* ─── Theme Toggle ───────────────────────────────────────────────── */
function initTheme() {
  const saved = localStorage.getItem('nz-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeIcons(saved);

  const toggles = document.querySelectorAll('#theme-toggle, #theme-toggle-mobile');
  toggles.forEach(btn => {
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('nz-theme', next);
      updateThemeIcons(next);
    });
  });
}

function updateThemeIcons(theme) {
  document.querySelectorAll('#theme-icon, #theme-icon-mobile').forEach(icon => {
    icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
  });
}

/* ─── Loading Screen ─────────────────────────────────────────────── */
function initLoadingScreen() {
  const loader = document.getElementById('loading-screen');
  if (!loader) return;
  window.addEventListener('load', () => {
    setTimeout(() => {
      loader.classList.add('hidden');
      document.body.style.overflow = 'auto';
    }, 800);
  });
  // Fallback
  setTimeout(() => loader && loader.classList.add('hidden'), 3000);
}

/* ─── Custom Cursor ──────────────────────────────────────────────── */
function initCustomCursor() {
  const outer = document.getElementById('cursor-outer');
  const inner = document.getElementById('cursor-inner');
  if (!outer || !inner || window.matchMedia('(max-width:768px)').matches) return;

  let mouseX = 0, mouseY = 0;
  let outerX = 0, outerY = 0;

  document.addEventListener('mousemove', e => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    inner.style.left = mouseX + 'px';
    inner.style.top = mouseY + 'px';
  });

  function animateCursor() {
    outerX += (mouseX - outerX) * 0.12;
    outerY += (mouseY - outerY) * 0.12;
    outer.style.left = outerX + 'px';
    outer.style.top = outerY + 'px';
    requestAnimationFrame(animateCursor);
  }
  animateCursor();

  // Hover effects on interactive elements
  document.querySelectorAll('a, button, [role="button"], .project-card, .glass-card').forEach(el => {
    el.addEventListener('mouseenter', () => {
      outer.style.width = '56px';
      outer.style.height = '56px';
      outer.style.borderColor = 'rgba(99,102,241,0.8)';
    });
    el.addEventListener('mouseleave', () => {
      outer.style.width = '36px';
      outer.style.height = '36px';
      outer.style.borderColor = 'rgba(99,102,241,0.5)';
    });
  });
}

/* ─── Navbar Scroll Effect ───────────────────────────────────────── */
function initNavbar() {
  const nav = document.getElementById('navbar');
  if (!nav) return;

  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const current = window.pageYOffset;
    if (current > 80) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
    lastScroll = current;
  }, { passive: true });
}

/* ─── AOS (Scroll Reveal) ────────────────────────────────────────── */
function initAOS() {
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 700,
      easing: 'ease-out-cubic',
      once: true,
      offset: 60,
    });
  }
}

/* ─── Canvas Particle Background ─────────────────────────────────── */
function initParticles() {
  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let particles = [];
  let animFrame;

  function resize() {
    canvas.width = canvas.parentElement.offsetWidth;
    canvas.height = canvas.parentElement.offsetHeight;
  }
  resize();
  window.addEventListener('resize', () => { resize(); createParticles(); }, { passive: true });

  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 2 + 0.5;
      this.speedX = (Math.random() - 0.5) * 0.4;
      this.speedY = (Math.random() - 0.5) * 0.4;
      this.opacity = Math.random() * 0.5 + 0.1;
      this.color = Math.random() > 0.5 ? '99,102,241' : '139,92,246';
    }
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
        this.reset();
      }
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color},${this.opacity})`;
      ctx.fill();
    }
  }

  function createParticles() {
    particles = [];
    const count = Math.min(Math.floor((canvas.width * canvas.height) / 12000), 120);
    for (let i = 0; i < count; i++) particles.push(new Particle());
  }
  createParticles();

  function connectParticles() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(99,102,241,${0.15 * (1 - dist / 120)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    connectParticles();
    animFrame = requestAnimationFrame(animate);
  }
  animate();

  // Pause when not visible
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) cancelAnimationFrame(animFrame);
    else animate();
  });
}

/* ─── Typing Animation ───────────────────────────────────────────── */
function initTypingAnimation() {
  const el = document.getElementById('typed-text');
  if (!el) return;

  const strings = window.TYPED_STRINGS || [
    'Python Developer',
    'Backend Engineer',
    'Flask Developer',
    'Cybersecurity Enthusiast',
  ];

  let sIdx = 0, cIdx = 0, isDeleting = false;

  function type() {
    const current = strings[sIdx];
    el.textContent = isDeleting
      ? current.substring(0, cIdx - 1)
      : current.substring(0, cIdx + 1);

    if (!isDeleting) {
      cIdx++;
      if (cIdx === current.length) {
        isDeleting = true;
        setTimeout(type, 1800);
        return;
      }
    } else {
      cIdx--;
      if (cIdx === 0) {
        isDeleting = false;
        sIdx = (sIdx + 1) % strings.length;
      }
    }
    setTimeout(type, isDeleting ? 60 : 100);
  }
  setTimeout(type, 600);
}

/* ─── Animated Counters ──────────────────────────────────────────── */
function initCounters() {
  const counters = document.querySelectorAll('.counter');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.counted) {
        entry.target.dataset.counted = 'true';
        animateCounter(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

function animateCounter(el) {
  const target = parseInt(el.dataset.target) || 0;
  const duration = 2000;
  const start = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    el.textContent = Math.floor(eased * target);
    if (progress < 1) requestAnimationFrame(update);
    else el.textContent = target + '+';
  }
  requestAnimationFrame(update);
}

/* ─── Skill Bar Animation ────────────────────────────────────────── */
function initScrollReveal() {
  const fills = document.querySelectorAll('.skill-bar-fill');
  if (!fills.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.width = entry.target.dataset.level + '%';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  fills.forEach(f => observer.observe(f));
}

/* ─── Back to Top ────────────────────────────────────────────────── */
function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* ─── Auto-hide Flash Alerts ─────────────────────────────────────── */
function initAutoHideAlerts() {
  document.querySelectorAll('.flash-container .alert').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(100%)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });
}

/* ─── Smooth Scroll for Anchor Links ─────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

/* ─── Navbar Mobile Toggle Close on Item Click ───────────────────── */
document.querySelectorAll('#navbarNav .nav-link:not(.dropdown-toggle)').forEach(link => {
  link.addEventListener('click', () => {
    const navCollapse = document.getElementById('navbarNav');
    if (navCollapse && navCollapse.classList.contains('show')) {
      const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
      if (bsCollapse) bsCollapse.hide();
    }
  });
});

/* ─── Inject current year in footer ─────────────────────────────── */
document.querySelectorAll('.footer-copy').forEach(el => {
  el.innerHTML = el.innerHTML.replace('{year}', new Date().getFullYear());
});
