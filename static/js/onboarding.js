/* onboarding.js — EduNode first-time onboarding + Duolingo-style feature tour */
(function () {
  'use strict';

  /* ── SVG icon helper ──────────────────────────────────────────────────── */
  const S = '/static/icons/sprite.svg';
  const ico = (n, c) => '<svg class="icon' + (c ? ' ' + c : '') + '" aria-hidden="true"><use href="' + S + '#icon-' + n + '"></use></svg>';

  /* ── Chat link labels by language + level ────────────────────────────── */
  const CHAT_LABELS = {
    'English':          { primary: ico('message-square') + ' Talk to Tutor', secondary: ico('message-square') + ' Chat' },
    'Filipino':         { primary: ico('message-square') + ' Kausapin ang Tutor', secondary: ico('message-square') + ' Chat' },
    'Bahasa Melayu':    { primary: ico('message-square') + ' Bercakap Tutor', secondary: ico('message-square') + ' Chat' },
    'Bahasa Indonesia': { primary: ico('message-square') + ' Bicara Tutor', secondary: ico('message-square') + ' Chat' },
    'Thai':             { primary: ico('message-square') + ' คุยกับครู', secondary: ico('message-square') + ' แชท' },
    'Vietnamese':       { primary: ico('message-square') + ' Nói chuyện với Gia sư', secondary: ico('message-square') + ' Trò chuyện' },
    'Khmer':            { primary: ico('message-square') + ' និយាយជាមួយគ្រូ', secondary: ico('message-square') + ' ជជែក' },
    'Lao':              { primary: ico('message-square') + ' ລົມກັບຄູ', secondary: ico('message-square') + ' ສົນທະນາ' },
    'Burmese':          { primary: ico('message-square') + ' ဆရာနှင့်ပြောဆို', secondary: ico('message-square') + ' ချတ်' },
    'Cebuano':          { primary: ico('message-square') + ' Pag-usap ang Tutor', secondary: ico('message-square') + ' Chat' },
    'Iban':             { primary: ico('message-square') + ' Cakap Tutor', secondary: ico('message-square') + ' Chat' },
  };

  /* ── Country → default language ───────────────────────────────────────── */
  const COUNTRY_LANG = {
    'Philippines':  'Filipino',
    'Indonesia':    'Bahasa Indonesia',
    'Malaysia':     'Bahasa Melayu',
    'Thailand':     'Thai',
    'Vietnam':      'Vietnamese',
    'Cambodia':     'Khmer',
    'Myanmar':      'Burmese',
    'Laos':         'Lao',
    'Singapore':    'English',
    'Timor-Leste':  'English',
  };

  /* ── Country data (flag + display name) ───────────────────────────────── */
  const COUNTRIES = [
    { name: 'Philippines',  flag: '🇵🇭' },
    { name: 'Indonesia',    flag: '🇮🇩' },
    { name: 'Malaysia',     flag: '🇲🇾' },
    { name: 'Thailand',     flag: '🇹🇭' },
    { name: 'Vietnam',      flag: '🇻🇳' },
    { name: 'Cambodia',     flag: '🇰🇭' },
    { name: 'Myanmar',      flag: '🇲🇲' },
    { name: 'Laos',         flag: '🇱🇦' },
    { name: 'Singapore',    flag: '🇸🇬' },
    { name: 'Timor-Leste',  flag: '🇹🇱' },
  ];

  /* ── Regional flavor greetings ────────────────────────────────────────── */
  const COUNTRY_FLAVOR = {
    'Philippines':  'Kumusta! Ako si EduNode, ang iyong AI tutor! 🌺',
    'Indonesia':    'Halo! Aku EduNode, tutor AI kamu! 🌴 Ayo belajar!',
    'Malaysia':     'Hai! Saya EduNode, tutor AI kamu! ✨ Jom belajar, lah!',
    'Thailand':     'สวัสดี! ฉันคือ EduNode ครูสอนพิเศษ AI ของคุณ! 🐘',
    'Vietnam':      'Xin chào! Mình là EduNode, gia sư AI của bạn! 🌸',
    'Cambodia':     'សួស្តី! ខ្ញុំជា EduNode គ្រូបង្រៀន AI របស់អ្នក! 🌺',
    'Myanmar':      'မင်္ဂလာပါ! ကျွန်တော် EduNode ပါ! 🌸 အတူတကွ သင်ကြရအောင်!',
    'Laos':         'ສະບາຍດີ! ຂ້ອຍແມ່ນ EduNode ຄູສອນ AI ຂອງທ່ານ! 🐘',
    'Singapore':    "Hey! I'm EduNode, your AI tutor! 🦁 Let's learn lah!",
    'Timor-Leste':  'Olá! Eu sou EduNode, o seu tutor de IA! 🌟 Aprende comigo!',
  };

  /* ── Feature tour steps (home page only) ─────────────────────────────── */
  const TOUR_STEPS = [
    {
      selector: '#subject-grid',
      mascot:   ico('bot', 'icon-xl'),
      text:     'Tap any subject to start chatting with your AI tutor and begin learning!',
      position: 'below',
    },
    {
      selector: '#act-quiz',
      fallback: '.activity-card[href="/quiz"], .quick-link[href="/quiz"]',
      mascot:   ico('brain', 'icon-xl'),
      text:     'Take a Quiz! Test what you know and earn badges!',
      position: 'above',
    },
    {
      selector: '#act-flashcard',
      fallback: '.activity-card[href="/flashcard"], .quick-link[href="/flashcard"]',
      mascot:   ico('layers', 'icon-xl'),
      text:     'Study with Flashcards! Tap the card to flip and see the answer!',
      position: 'above',
    },
    {
      selector: '#act-podcast',
      fallback: '.activity-card[href="/podcast"], .quick-link[href="/podcast"]',
      mascot:   ico('headphones', 'icon-xl'),
      text:     'Listen to a fun Podcast while you relax! Learning made easy!',
      position: 'above',
    },
    {
      selector: '#act-progress',
      fallback: '.activity-card[href="/progress"], .quick-link[href="/progress"]',
      mascot:   ico('trophy', 'icon-xl'),
      text:     "See all your badges and achievements in Progress!",
      position: 'above',
    },
  ];

  /* ── Per-page first-visit hints ───────────────────────────────────────── */
  const PAGE_HINTS = {
    '/chat':      { mascot: ico('message-square','icon-xl'), text: 'Ask me anything! Type your question or tap the mic to speak!' },
    '/quiz':      { mascot: ico('brain','icon-xl'),          text: 'Pick a topic and I will make questions just for you!' },
    '/flashcard': { mascot: ico('layers','icon-xl'),         text: 'Type a topic and tap the card to flip it! Ready to study?' },
    '/podcast':   { mascot: ico('headphones','icon-xl'),     text: 'Type a topic and listen to a fun mini-podcast!' },
    '/progress':  { mascot: ico('trophy','icon-xl'),         text: 'Enter your name to see all your progress and badges!' },
  };

  /* ── Helpers ──────────────────────────────────────────────────────────── */
  function ls(key, val) {
    if (val === undefined) return localStorage.getItem(key);
    localStorage.setItem(key, val);
  }

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  /* ── 1. applyLevel — runs on every page load ──────────────────────────── */
  function applyLevel() {
    const level = ls('edu_level');
    if (!level) return;

    document.body.setAttribute('data-level', level);

    // Show level badge in nav
    const badge = document.getElementById('nav-level-badge');
    if (badge) {
      badge.innerHTML = level === 'primary'
        ? ico('book','icon-xs') + ' Primary'
        : ico('book-open','icon-xs') + ' Secondary';
      badge.style.display = 'inline-block';
    }

    // Swap chat nav link with language-aware label
    const chatLink = document.querySelector('.nav-link[href="/chat"]');
    if (chatLink) {
      const lang   = ls('edu_lang') || 'English';
      const labels = CHAT_LABELS[lang] || CHAT_LABELS['English'];
      chatLink.innerHTML = level === 'primary' ? labels.primary : labels.secondary;
    }
  }

  /* ── 2. showOnboarding — full-screen country + level picker ──────────── */
  function showOnboarding() {
    const overlay = document.createElement('div');
    overlay.id = 'edu-onboarding';
    overlay.innerHTML = `
      <div class="onb-card">
        <!-- Step 1: country -->
        <div class="onb-step active" data-step="country">
          <h2 class="onb-heading">${ico('hand')} Welcome to EduNode!</h2>
          <p class="onb-sub">Where are you from? Pick your country to get started!</p>
          <div class="onb-country-grid">
            ${COUNTRIES.map(c => `
              <button class="onb-country-btn" data-country="${c.name}">
                <span class="flag">${c.flag}</span>
                <span>${c.name}</span>
              </button>`).join('')}
          </div>
          <button class="onb-skip" id="onb-skip-1">Skip for now</button>
        </div>

        <!-- Step 2: level -->
        <div class="onb-step" data-step="level">
          <div class="onb-mascot-wrap">
            <span class="onb-mascot">${ico('bot','icon-3xl')}</span>
          </div>
          <p class="onb-flavor" id="onb-flavor">Hello! I am EduNode, your AI tutor!</p>
          <h2 class="onb-heading" style="font-size:1.3rem;margin-bottom:.35rem">What school level are you?</h2>
          <p class="onb-sub" style="margin-bottom:1rem">This helps me explain things just right for you!</p>
          <div class="onb-level-grid">
            <button class="onb-level-btn" data-level="primary">
              <span class="level-icon">${ico('book','icon-xl')}</span>
              <span>Primary<br><small style="font-weight:600;font-size:.78rem">Grade 1 – 6</small></span>
            </button>
            <button class="onb-level-btn" data-level="secondary">
              <span class="level-icon">${ico('book-open','icon-xl')}</span>
              <span>Secondary<br><small style="font-weight:600;font-size:.78rem">Grade 7 – 12</small></span>
            </button>
          </div>
          <button class="onb-skip" id="onb-skip-2">Skip for now</button>
        </div>
      </div>`;

    document.body.appendChild(overlay);

    let selectedCountry = null;

    // Country card clicks
    overlay.querySelectorAll('.onb-country-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        selectedCountry = this.dataset.country;

        // Auto-set language
        const lang = COUNTRY_LANG[selectedCountry] || 'English';
        ls('edu_lang', lang);

        // Sync the home language chips if present
        document.querySelectorAll('.lang-chip').forEach(c => {
          c.classList.toggle('active', c.dataset.lang === lang);
        });

        // Translate UI immediately
        if (window.EduI18n) window.EduI18n.applyLang(lang);

        // Visual feedback
        overlay.querySelectorAll('.onb-country-btn').forEach(b => b.classList.remove('selected'));
        this.classList.add('selected');

        // Advance to step 2 after brief animation
        setTimeout(() => goToStep('level', selectedCountry), 220);
      });
    });

    // Level card clicks
    overlay.querySelectorAll('.onb-level-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        ls('edu_level', this.dataset.level);
        ls('edu_onboarded', '1');
        ls('edu_country', selectedCountry || '');
        finishOnboarding(overlay);
      });
    });

    // Skip buttons
    document.getElementById('onb-skip-1').addEventListener('click', function () {
      ls('edu_onboarded', '1');
      finishOnboarding(overlay);
    });
    document.getElementById('onb-skip-2').addEventListener('click', function () {
      ls('edu_onboarded', '1');
      finishOnboarding(overlay);
    });
  }

  function goToStep(stepName, country) {
    const overlay = document.getElementById('edu-onboarding');
    if (!overlay) return;
    overlay.querySelectorAll('.onb-step').forEach(s => s.classList.remove('active'));
    const next = overlay.querySelector('[data-step="' + stepName + '"]');
    if (next) next.classList.add('active');

    // Fill flavor text
    const flavorEl = document.getElementById('onb-flavor');
    if (flavorEl && country) {
      flavorEl.textContent = COUNTRY_FLAVOR[country] || "Hello! I am EduNode, your AI tutor!";
    }

    // Translate the level-picker overlay to the selected language
    if (stepName === 'level') {
      const lang = ls('edu_lang') || 'English';
      const t = (window.EduI18n && window.EduI18n.TRANSLATIONS[lang])
                || (window.EduI18n && window.EduI18n.TRANSLATIONS['English'])
                || {};
      var set = function(sel, key) {
        var el = overlay.querySelector(sel);
        if (el && t[key]) el.innerHTML = t[key];
      };
      set('[data-step="level"] .onb-heading',  'onb.level.title');
      set('[data-step="level"] .onb-sub',       'onb.level.sub');
      // Primary button
      var primBtn = overlay.querySelector('.onb-level-btn[data-level="primary"] span:last-child');
      if (primBtn && t['onb.primary']) {
        primBtn.innerHTML = t['onb.primary'] + '<br><small style="font-weight:600;font-size:.78rem">' + (t['onb.primary.sub'] || 'Grade 1 – 6') + '</small>';
      }
      // Secondary button
      var secBtn = overlay.querySelector('.onb-level-btn[data-level="secondary"] span:last-child');
      if (secBtn && t['onb.secondary']) {
        secBtn.innerHTML = t['onb.secondary'] + '<br><small style="font-weight:600;font-size:.78rem">' + (t['onb.secondary.sub'] || 'Grade 7 – 12') + '</small>';
      }
      // Skip buttons
      overlay.querySelectorAll('.onb-skip').forEach(function(btn) {
        if (t['onb.skip']) btn.textContent = t['onb.skip'];
      });
    }
  }

  function finishOnboarding(overlay) {
    overlay.style.transition = 'opacity .25s';
    overlay.style.opacity = '0';
    setTimeout(() => {
      overlay.remove();
      applyLevel();
      // Re-sync the whole page to the chosen language now that the overlay is gone
      var savedLang = ls('edu_lang') || 'English';
      if (window.EduI18n) window.EduI18n.applyLang(savedLang);
      // Always play tour after onboarding on home page
      // (clear the done flag — onboarding is a deliberate reset)
      if (window.location.pathname === '/') {
        sessionStorage.removeItem('edu_tour_done');
        setTimeout(showTour, 400);
      }
    }, 260);
  }

  /* ── 3. showTour — spotlight + mascot bubble walk-through ─────────────── */
  function showTour() {
    let stepIdx = 0;

    const overlay = document.createElement('div');
    overlay.id = 'tour-overlay';
    document.body.appendChild(overlay);

    const bubble = document.createElement('div');
    bubble.className = 'tour-bubble';
    document.body.appendChild(bubble);

    /* Find element by primary selector, then try comma-separated fallbacks */
    function findTarget(step) {
      const el = document.querySelector(step.selector);
      if (el) return el;
      if (!step.fallback) return null;
      for (const sel of step.fallback.split(',')) {
        const fb = document.querySelector(sel.trim());
        if (fb) return fb;
      }
      return null;
    }

    function renderStep(idx) {
      const step   = TOUR_STEPS[idx];
      const target = findTarget(step);
      if (!target) { advanceStep(); return; }

      document.querySelectorAll('.tour-focus').forEach(el => el.classList.remove('tour-focus'));
      target.classList.add('tour-focus');

      /* Instant scroll so getBoundingClientRect is correct in the next frame */
      const scrollY = target.getBoundingClientRect().top + window.scrollY
                      - window.innerHeight / 2 + target.offsetHeight / 2;
      window.scrollTo({ top: Math.max(0, scrollY) });

      const isLast = idx === TOUR_STEPS.length - 1;
      const dots   = TOUR_STEPS.map((_, i) =>
        `<span class="tour-dot${i === idx ? ' active' : ''}"></span>`).join('');

      bubble.className = 'tour-bubble';
      bubble.innerHTML = `
        <div class="tour-mascot-row">
          <span class="tour-mascot">${step.mascot}</span>
          <p class="tour-text">${step.text}</p>
        </div>
        <div class="tour-btns">
          <div class="tour-step-dots">${dots}</div>
          <button class="btn-outline tour-skip-btn" style="font-size:.82rem;padding:.38rem .9rem">Skip</button>
          <button class="btn-primary tour-next-btn" style="font-size:.9rem">${isLast ? ico('sparkles') + ' Got it!' : 'Next →'}</button>
        </div>`;

      bubble.querySelector('.tour-next-btn').addEventListener('click', advanceStep);
      bubble.querySelector('.tour-skip-btn').addEventListener('click', endTour);

      /* Measure after scroll is committed to the layout */
      requestAnimationFrame(() => positionBubble(target, step.position));
    }

    function positionBubble(target, pref) {
      const tRect = target.getBoundingClientRect();
      const bH    = bubble.offsetHeight;
      const bW    = bubble.offsetWidth;
      const vw    = window.innerWidth;
      const vh    = window.innerHeight;
      const gap   = 16;

      const canAbove = tRect.top  >= bH + gap + 8;
      const canBelow = vh - tRect.bottom >= bH + gap + 8;

      let top, arrowClass;
      if (pref === 'above' && canAbove) {
        top = tRect.top - bH - gap;  arrowClass = 'arrow-bottom';
      } else if (canBelow) {
        top = tRect.bottom + gap;    arrowClass = 'arrow-top';
      } else if (canAbove) {
        top = tRect.top - bH - gap;  arrowClass = 'arrow-bottom';
      } else {
        top = clamp(tRect.bottom + gap, 8, vh - bH - 8);
        arrowClass = 'arrow-top';
      }

      const left = clamp(tRect.left, 12, vw - bW - 12);
      bubble.style.top  = top  + 'px';
      bubble.style.left = left + 'px';
      bubble.classList.add(arrowClass);
    }

    function advanceStep() {
      stepIdx++;
      if (stepIdx >= TOUR_STEPS.length) { endTour(); return; }
      renderStep(stepIdx);
    }

    function endTour() {
      sessionStorage.setItem('edu_tour_done', '1');
      document.querySelectorAll('.tour-focus').forEach(el => el.classList.remove('tour-focus'));
      overlay.remove();
      bubble.remove();
    }

    renderStep(0);
  }

  /* ── 4. showPageHint — one-time mascot hint on feature pages ─────────── */
  function showPageHint() {
    const path  = window.location.pathname;
    const hint  = PAGE_HINTS[path];
    if (!hint) return;

    const key = 'edu_hint_' + path.replace('/', '');
    if (ls(key)) return;
    ls(key, '1');

    const el = document.createElement('div');
    el.className = 'page-hint';
    el.innerHTML = `
      <span class="hint-mascot">${hint.mascot}</span>
      <span class="hint-text">${hint.text}</span>
      <span class="hint-close">✕</span>`;

    document.body.appendChild(el);

    function dismiss() {
      el.classList.add('hiding');
      setTimeout(() => el.remove(), 320);
    }

    el.addEventListener('click', dismiss);
    setTimeout(dismiss, 7000);
  }

  /* ── Boot sequence ────────────────────────────────────────────────────── */
  /* Clear the saved flag and replay onboarding (manual re-trigger for demos) */
  function restartOnboarding() {
    try { localStorage.removeItem('edu_onboarded'); } catch (e) {}
    showOnboarding();
  }

  function boot() {
    applyLevel();

    // Expose globally so home page and i18n.js can call in
    window.EduOnboarding = { applyLevel: applyLevel, startTour: showTour, restart: restartOnboarding };

    // Show onboarding on first visit only. Demos can replay it on demand via
    // the ?onboarding=1 URL or window.EduOnboarding.restart().
    var forceOnboarding = new URLSearchParams(window.location.search).get('onboarding') === '1';

    if (!ls('edu_onboarded') || forceOnboarding) {
      showOnboarding();
      return;
    }

    // Show tour on every fresh home-page session
    if (window.location.pathname === '/' && !sessionStorage.getItem('edu_tour_done')) {
      setTimeout(showTour, 600);
    }
    showPageHint();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
