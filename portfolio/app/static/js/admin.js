/* ═══════════════════════════════════════════════════════
   ADMIN PANEL JAVASCRIPT
═══════════════════════════════════════════════════════ */
'use strict';

document.addEventListener('DOMContentLoaded', () => {
  initSidebarToggle();
  initAutoHideAlerts();
  initConfirmDeletes();
  initRangeDisplays();
});

/* ─── Sidebar Toggle ──────────────────────────────────── */
function initSidebarToggle() {
  const toggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('adminSidebar');
  const main = document.querySelector('.admin-main');
  if (!toggle || !sidebar) return;

  toggle.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
      sidebar.classList.toggle('open');
    } else {
      const collapsed = sidebar.classList.toggle('collapsed');
      sidebar.style.width = collapsed ? '64px' : '260px';
      if (main) main.style.marginLeft = collapsed ? '64px' : '260px';
      sidebar.querySelectorAll('.nav-item span, .brand-title, .brand-sub, .nav-section-label').forEach(el => {
        el.style.display = collapsed ? 'none' : '';
      });
    }
  });

  // Close sidebar on outside click (mobile)
  document.addEventListener('click', e => {
    if (window.innerWidth <= 768 && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

/* ─── Auto-hide flash messages ────────────────────────── */
function initAutoHideAlerts() {
  document.querySelectorAll('.admin-flash-container .alert').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });
}

/* ─── Range slider live display ───────────────────────── */
function initRangeDisplays() {
  document.querySelectorAll('input[type="range"]').forEach(range => {
    const display = range.parentElement.querySelector('label');
    if (!display) return;
    range.addEventListener('input', () => {
      const match = display.textContent.match(/^(.+?):\s*\d+%?$/);
      if (match) display.textContent = `${match[1]}: ${range.value}%`;
    });
  });
}

/* ─── Confirm deletes ─────────────────────────────────── */
function initConfirmDeletes() {
  document.querySelectorAll('[onsubmit]').forEach(form => {
    // Already handled inline; this is a fallback for dynamically added forms.
  });
}
