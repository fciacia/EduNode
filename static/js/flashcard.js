/**
 * flashcard.js — Edge flashcard module
 * Generates and renders a flip-card deck with keyboard + swipe support.
 *
 * Expected DOM IDs (provided by flashcard.html):
 *   #topicInput, #subjectSel, #langSel, #generateBtn
 *   #deckArea, #card3d, #cardFront, #cardBack, #deckDots, #deckCounter
 */

/* ---- State ---- */

let _cards = [];
let _idx   = 0;

/* ---- Helpers ---- */

function getLang()    { return document.getElementById('langSel').value; }
function getSubject() { return document.getElementById('subjectSel').value; }

/* ---- Generate ---- */

async function generateFlashcards() {
  const topic = document.getElementById('topicInput').value.trim();
  if (!topic) { alert('Please enter a topic.'); return; }

  const btn = document.getElementById('generateBtn');
  btn.disabled = true;
  btn.textContent = 'Generating…';

  try {
    const r = await fetch('/api/flashcard/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, language: getLang(), subject: getSubject() }),
    });
    const d = await r.json();
    _cards = d.flashcards || [];
    if (!_cards.length) { alert('No flashcards generated. Is Ollama running?'); return; }
    _idx = 0;
    _buildDots();
    _showCard();
    document.getElementById('deckArea').style.display = 'block';
  } catch (e) {
    alert('Error: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Make Cards';
  }
}

/* ---- Render ---- */

function _buildDots() {
  const c = document.getElementById('deckDots');
  c.innerHTML = '';
  _cards.forEach((_, i) => {
    const d = document.createElement('div');
    d.className = 'deck-dot';
    d.id = `dot-${i}`;
    c.appendChild(d);
  });
}

function _showCard() {
  document.getElementById('card3d').classList.remove('flipped');
  document.getElementById('cardFront').textContent = _cards[_idx].title || '—';
  document.getElementById('cardBack').textContent  = _cards[_idx].body  || '—';
  document.getElementById('deckCounter').textContent = `${_idx + 1} / ${_cards.length}`;
  document.querySelectorAll('.deck-dot').forEach((d, i) => {
    d.classList.toggle('active', i === _idx);
  });
}

/* ---- Navigation ---- */

function flipCard() { document.getElementById('card3d').classList.toggle('flipped'); }

function prevCard() { if (_idx > 0)               { _idx--; _showCard(); } }
function nextCard() { if (_idx < _cards.length - 1) { _idx++; _showCard(); } }

/* ---- Touch / swipe ---- */

let _touchStartX = 0;

function _initSwipe() {
  const scene = document.getElementById('deckArea');
  if (!scene) return;
  scene.addEventListener('touchstart', e => { _touchStartX = e.changedTouches[0].screenX; }, { passive: true });
  scene.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].screenX - _touchStartX;
    if (Math.abs(dx) > 40) { dx < 0 ? nextCard() : prevCard(); }
  });
}

/* ---- Keyboard ---- */

function _initKeyboard() {
  document.addEventListener('keydown', e => {
    if (!_cards.length) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown')  { e.preventDefault(); nextCard(); }
    if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')    { e.preventDefault(); prevCard(); }
    if (e.key === ' ')                                     { e.preventDefault(); flipCard(); }
  });
}

/* ---- Language persistence ---- */

function _initLangPersist() {
  const sel = document.getElementById('langSel');
  if (!sel) return;
  const saved = localStorage.getItem('edu_lang');
  if (saved) [...sel.options].forEach(o => { o.selected = (o.value === saved); });
  sel.addEventListener('change', e => localStorage.setItem('edu_lang', e.target.value));
}

/* ---- Init ---- */

document.addEventListener('DOMContentLoaded', () => {
  _initSwipe();
  _initKeyboard();
  _initLangPersist();
});
