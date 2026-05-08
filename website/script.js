/* Sipurima — v1 interactions. Vanilla JS, no dependencies. */
(function () {
  'use strict';

  // Current year in footer
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Mobile nav toggle
  var navToggle = document.getElementById('nav-toggle');
  var navLinks = document.getElementById('nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      var open = navLinks.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', open);
    });
    navLinks.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navLinks.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', false);
      });
    });
  }

  // Floating WhatsApp button
  var waFloat = document.getElementById('wa-float');
  function onScroll() {
    if (!waFloat) return;
    var scrolled = window.scrollY || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - window.innerHeight;
    var pct = height > 0 ? scrolled / height : 0;
    if (pct > 0.3) {
      waFloat.classList.add('is-visible');
    } else {
      waFloat.classList.remove('is-visible');
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // CTA circle buttons — first tap opens, second tap navigates
  document.querySelectorAll('.cta-circle').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!btn.classList.contains('is-open')) {
        e.preventDefault();
        btn.classList.add('is-open');
      }
    });
  });

  var waLinks = document.querySelectorAll('[data-wa]');
  waLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      var label = link.getAttribute('data-wa');
      if (window.gtag) {
        window.gtag('event', 'click_whatsapp', { label: label });
      }
    });
  });

  // Accessibility widget
  var a11yToggle = document.getElementById('a11y-toggle');
  var a11yPanel = document.getElementById('a11y-panel');
  var fontLevel = 0;

  if (a11yToggle && a11yPanel) {
    a11yToggle.addEventListener('click', function () {
      var open = a11yPanel.classList.toggle('is-open');
      a11yToggle.setAttribute('aria-expanded', open);
    });

    document.addEventListener('click', function (e) {
      if (!e.target.closest('.a11y-widget')) {
        a11yPanel.classList.remove('is-open');
        a11yToggle.setAttribute('aria-expanded', false);
      }
    });

    a11yPanel.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-a11y]');
      if (!btn) return;
      var action = btn.getAttribute('data-a11y');

      if (action === 'font-up' && fontLevel < 4) {
        fontLevel++;
        document.documentElement.style.fontSize = (100 + fontLevel * 15) + '%';
      } else if (action === 'font-down' && fontLevel > -2) {
        fontLevel--;
        document.documentElement.style.fontSize = (100 + fontLevel * 15) + '%';
      } else if (action === 'contrast') {
        document.body.classList.toggle('a11y-contrast');
        btn.classList.toggle('is-active');
      } else if (action === 'grayscale') {
        document.body.classList.toggle('a11y-grayscale');
        btn.classList.toggle('is-active');
      } else if (action === 'links') {
        document.body.classList.toggle('a11y-links');
        btn.classList.toggle('is-active');
      } else if (action === 'animations') {
        document.body.classList.toggle('a11y-no-animations');
        btn.classList.toggle('is-active');
      } else if (action === 'reset') {
        fontLevel = 0;
        document.documentElement.style.fontSize = '';
        document.body.classList.remove('a11y-contrast', 'a11y-grayscale', 'a11y-links', 'a11y-no-animations');
        a11yPanel.querySelectorAll('.is-active').forEach(function (b) { b.classList.remove('is-active'); });
      }
    });
  }

  // Scroll-spy: highlight active nav link based on visible section
  var scrollSections = document.querySelectorAll('.scroll-section');
  var navSectionLinks = document.querySelectorAll('[data-section]');
  if (scrollSections.length && navSectionLinks.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id;
          navSectionLinks.forEach(function (link) {
            link.classList.toggle('is-active', link.getAttribute('data-section') === id);
          });
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    scrollSections.forEach(function (s) { observer.observe(s); });
  }

  // Scroll-reveal animations
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    reveals.forEach(function (el) { revealObserver.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  var form = document.getElementById('contact-form');
  var status = document.getElementById('form-status');

  if (form) {
    var submitting = false;
    var submitBtn = form.querySelector('[type="submit"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!status || submitting) return;

      var name  = form.name.value.trim();
      var phone = form.phone.value.trim();
      var type  = form.type.value;

      if (!name || !phone || !type) {
        status.textContent = 'אנא מלאו שם, טלפון וסוג אירוע.';
        status.className = 'form-status is-error';
        return;
      }

      if (!/^[0-9\-+\s]{7,15}$/.test(phone)) {
        status.textContent = 'מספר טלפון לא תקין.';
        status.className = 'form-status is-error';
        return;
      }

      submitting = true;
      if (submitBtn) submitBtn.disabled = true;

      var data = new FormData(form);
      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(data).toString()
      }).then(function (res) {
        if (res.ok) {
          status.textContent = 'תודה! הפנייה התקבלה, אחזור אליכם בהקדם.';
          status.className = 'form-status is-success';
          form.reset();
        } else {
          status.textContent = 'משהו השתבש. אפשר לפנות בוואטסאפ.';
          status.className = 'form-status is-error';
        }
      }).catch(function () {
        status.textContent = 'שגיאת רשת. נסו שוב או פנו בוואטסאפ.';
        status.className = 'form-status is-error';
      }).finally(function () {
        submitting = false;
        if (submitBtn) submitBtn.disabled = false;
      });
    });
  }
})();
