/* Sipurima — v1 interactions. Vanilla JS, no dependencies. */
(function () {
  'use strict';

  // Current year in footer
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Floating WhatsApp button — appears after 30% scroll (mobile + desktop)
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

  // Track WhatsApp clicks (placeholder — will hook into GA4 later)
  var waLinks = document.querySelectorAll('[data-wa]');
  waLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      var label = link.getAttribute('data-wa');
      // GA4 placeholder:
      if (window.gtag) {
        window.gtag('event', 'click_whatsapp', { label: label });
      }
      // Console trace during dev:
      if (window.console && console.log) console.log('[wa-click]', label);
    });
  });

  // Contact form — v1: basic client-side validation + mailto fallback.
  // Once a backend endpoint (Netlify Forms / Formspree) is in, swap the submit handler.
  var form = document.getElementById('contact-form');
  var status = document.getElementById('form-status');

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!status) return;

      var name  = form.name.value.trim();
      var phone = form.phone.value.trim();
      var type  = form.type.value;
      var date  = form.date.value;

      if (!name || !phone || !type) {
        status.textContent = 'אנא מלאו שם, טלפון וסוג אירוע.';
        status.className = 'form-status is-error';
        return;
      }

      // v1: open mailto with the form contents, so Rima receives an email.
      // Also offer WhatsApp as an immediate follow-up.
      var typeLabels = {
        series: 'סדרת הצגות',
        single: 'הצגה בודדת',
        private: 'הצגה פרטית / יום הולדת',
        other: 'אחר'
      };
      var body = 'שם: ' + name + '\n'
               + 'טלפון: ' + phone + '\n'
               + 'סוג אירוע: ' + (typeLabels[type] || type) + '\n'
               + 'תאריך מועדף: ' + (date || 'לא צוין');
      var mail = 'mailto:hello@sipurima.co.il'
               + '?subject=' + encodeURIComponent('פנייה חדשה מהאתר — ' + name)
               + '&body=' + encodeURIComponent(body);
      window.location.href = mail;

      status.textContent = 'תודה! נפתחה אצלכם הודעת מייל — אם לא, אפשר לפנות בוואטסאפ.';
      status.className = 'form-status is-success';
      form.reset();
    });
  }
})();
