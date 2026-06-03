/* prefs.js — Edge accessibility & shared-device preferences for rural learners.
   Houses: read-aloud, big text, high contrast, lite/low-power, student switcher. */
(function () {
  'use strict';
  var S = '/static/icons/sprite.svg';
  function ico(n, c) { return '<svg class="icon' + (c ? ' ' + c : '') + '" aria-hidden="true"><use href="' + S + '#icon-' + n + '"></use></svg>'; }
  function ls(k, v) { if (v === undefined) return localStorage.getItem(k); try { localStorage.setItem(k, v); } catch (e) {} }

  /* Preference toggles: key -> {label, hint, icon, htmlClass?} */
  var PREFS = [
    { key: 'edge_readaloud', label: 'Read answers aloud', hint: 'Speak each answer automatically', icon: 'volume' },
    { key: 'edge_bigtext',   label: 'Big text',           hint: 'Larger, easier-to-read text',     icon: 'search', cls: 'a11y-large' },
    { key: 'edge_contrast',  label: 'High contrast',      hint: 'Stronger colours for sunlight',    icon: 'sun',    cls: 'a11y-contrast' },
    { key: 'edge_lite',      label: 'Lite mode',          hint: 'Less motion — saves battery',      icon: 'zap',    cls: 'lite' },
  ];

  function applyPrefs() {
    var root = document.documentElement;
    PREFS.forEach(function (p) {
      if (p.cls) root.classList.toggle(p.cls, ls(p.key) === '1');
    });
  }
  applyPrefs();

  /* ── Student switcher (shared 1-to-50 device) ─────────────────────────── */
  function students() { try { return JSON.parse(ls('edge_students') || '[]'); } catch (e) { return []; } }
  function currentStudent() { return ls('edu_student_name') || ''; }
  function switchStudent(name) {
    name = (name || '').trim();
    if (!name) return;
    var list = students().filter(function (n) { return n.toLowerCase() !== name.toLowerCase(); });
    list.unshift(name);
    ls('edge_students', JSON.stringify(list.slice(0, 8)));
    ls('edu_student_name', name);
    try { localStorage.removeItem('edu_convo'); } catch (e) {}   // fresh conversation
    location.reload();
  }

  /* Prefill any student-name field on the page with the active learner. */
  function prefillName() {
    var el = document.getElementById('studentName');
    if (el && !el.value) el.value = currentStudent();
  }

  /* ── Settings sheet ───────────────────────────────────────────────────── */
  function buildSheet() {
    var overlay = document.createElement('div');
    overlay.className = 'prefs-overlay';
    overlay.id = 'prefsOverlay';

    var cur = currentStudent();
    var pills = students().map(function (n) {
      return '<button class="student-pill' + (n === cur ? ' active' : '') + '" data-name="' + n.replace(/"/g, '&quot;') + '">' +
             ico('user') + n + '</button>';
    }).join('');

    overlay.innerHTML =
      '<div class="prefs-sheet" role="dialog" aria-label="Settings">' +
        '<h3>' + ico('settings') + 'Settings</h3>' +
        '<div class="prefs-section-label">Who is learning?</div>' +
        '<div class="student-list" id="studentList">' + pills + '</div>' +
        '<div class="student-add">' +
          '<input id="studentAdd" type="text" placeholder="Add a name…" maxlength="24">' +
          '<button class="btn-primary" id="studentAddBtn">' + ico('user') + ' Use</button>' +
        '</div>' +
        '<div class="prefs-section-label">Make it easier</div>' +
        PREFS.map(function (p) {
          var on = ls(p.key) === '1';
          return '<div class="pref-row">' + ico(p.icon) +
            '<span class="pref-text"><b>' + p.label + '</b><small>' + p.hint + '</small></span>' +
            '<button class="pref-switch" role="switch" aria-checked="' + on + '" data-key="' + p.key + '" data-cls="' + (p.cls || '') + '"></button>' +
          '</div>';
        }).join('') +
      '</div>';

    document.body.appendChild(overlay);

    overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });

    overlay.querySelectorAll('.pref-switch').forEach(function (sw) {
      sw.addEventListener('click', function () {
        var on = sw.getAttribute('aria-checked') !== 'true';
        sw.setAttribute('aria-checked', on);
        ls(sw.dataset.key, on ? '1' : '0');
        if (sw.dataset.cls) document.documentElement.classList.toggle(sw.dataset.cls, on);
      });
    });
    overlay.querySelectorAll('.student-pill').forEach(function (p) {
      p.addEventListener('click', function () { switchStudent(p.dataset.name); });
    });
    overlay.querySelector('#studentAddBtn').addEventListener('click', function () {
      switchStudent(overlay.querySelector('#studentAdd').value);
    });
    overlay.querySelector('#studentAdd').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') switchStudent(e.target.value);
    });
  }

  function open()  { document.getElementById('prefsOverlay').classList.add('open'); }
  function close() { document.getElementById('prefsOverlay').classList.remove('open'); }

  function boot() {
    buildSheet();
    prefillName();
    var fab = document.getElementById('prefsFab');
    if (fab) fab.addEventListener('click', open);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();

  /* Public API for chat read-aloud */
  window.EdgePrefs = { isReadAloud: function () { return ls('edge_readaloud') === '1'; } };
})();
