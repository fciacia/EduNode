/**
 * chat.js — EduNode chat module
 * Handles message send, voice record, TTS playback, language persistence.
 *
 * Expected DOM IDs (provided by chat.html):
 *   #chatLog, #msgInput, #micBtn, #subjectSel, #langSel, #studentName
 */

/* ---- Helpers ---- */

function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function getLang()    { return document.getElementById('langSel').value; }
function getSubject() { return document.getElementById('subjectSel').value; }
function getName()    { return (document.getElementById('studentName').value || '').trim() || 'Student'; }

/* ---- Bubble rendering ---- */

function addBubble(text, who) {
  const log = document.getElementById('chatLog');
  const d = document.createElement('div');
  d.className = 'bubble ' + who;
  d.textContent = text;
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
  return d;
}

function addTyping() {
  const log = document.getElementById('chatLog');
  const d = document.createElement('div');
  d.className = 'bubble bot typing';
  d.id = 'typing';
  d.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
}

function removeTyping() { document.getElementById('typing')?.remove(); }

function addPlayBtn(bubble, text) {
  const btn = document.createElement('button');
  btn.className = 'play-btn';
  btn.textContent = '🔊 Listen';
  btn.addEventListener('click', () => playTTS(btn, text));
  bubble.appendChild(document.createElement('br'));
  bubble.appendChild(btn);
}

/* ---- TTS ---- */

/* Browser speech fallback (used when Piper TTS is not installed on the server) */
function _browserSpeak(btn, text, orig) {
  if (!window.speechSynthesis) { btn.textContent = '🔇 No audio'; btn.disabled = false; return; }
  window.speechSynthesis.cancel();
  const utt = new SpeechSynthesisUtterance(text);
  utt.lang = 'en-US';
  utt.onstart  = () => { btn.textContent = '▶ Playing'; };
  utt.onend    = () => { btn.textContent = orig; btn.disabled = false; };
  utt.onerror  = () => { btn.textContent = orig; btn.disabled = false; };
  window.speechSynthesis.speak(utt);
}

async function playTTS(btn, text) {
  const orig = btn.textContent;
  btn.disabled = true;
  btn.textContent = '⏳ …';

  // If we already know server TTS is unavailable, skip straight to browser speech
  if (!window._serverTtsAvailable) {
    _browserSpeak(btn, text, orig);
    return;
  }

  try {
    const r = await fetch('/api/voice/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    if (!r.ok) {
      window._serverTtsAvailable = false;  // don't try again this session
      _browserSpeak(btn, text, orig);
      return;
    }
    const blob = await r.blob();
    const audio = new Audio(URL.createObjectURL(blob));
    btn.textContent = '▶ Playing';
    audio.onended = () => { btn.textContent = orig; btn.disabled = false; };
    audio.play();
  } catch (_) {
    _browserSpeak(btn, text, orig);
  }
}

/* ---- Send message ---- */

async function sendMessage(text) {
  const msg = (text || '').trim();
  if (!msg) return;

  const input = document.getElementById('msgInput');
  input.value = '';
  addBubble(msg, 'user');
  addTyping();

  try {
    const r = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: msg,
        language: getLang(),
        subject: getSubject(),
        student_name: getName(),
      }),
    });
    const d = await r.json();
    removeTyping();
    const bubble = addBubble(d.response || d.error || 'No response', 'bot');
    if (d.response) addPlayBtn(bubble, d.response);
    // Persist student_id so the Progress page can pre-fill it
    if (d.student_id) localStorage.setItem('edu_student_id', d.student_id);
  } catch (e) {
    removeTyping();
    addBubble('Connection error — is EduNode running?', 'bot');
  }
}

/* ---- Voice recording ---- */

let _mediaRec = null;
let _audioChunks = [];

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    _mediaRec = new MediaRecorder(stream);
    _audioChunks = [];
    _mediaRec.ondataavailable = e => _audioChunks.push(e.data);
    _mediaRec.start();
    document.getElementById('micBtn').classList.add('recording');
  } catch (e) {
    alert('Microphone not available: ' + e.message);
  }
}

async function stopRecording() {
  if (!_mediaRec || _mediaRec.state === 'inactive') return;
  _mediaRec.stop();
  document.getElementById('micBtn').classList.remove('recording');

  _mediaRec.onstop = async () => {
    const blob = new Blob(_audioChunks, { type: 'audio/webm' });
    const fd = new FormData();
    fd.append('audio', blob, 'voice.webm');
    addTyping();
    try {
      const r = await fetch('/api/voice/stt', { method: 'POST', body: fd });
      const d = await r.json();
      removeTyping();
      if (d.text) sendMessage(d.text);
      else addBubble('Could not transcribe audio.', 'bot');
    } catch (_) { removeTyping(); }
    _mediaRec.stream.getTracks().forEach(t => t.stop());
  };
}

/* ---- Language persistence ---- */

function initLangPersist() {
  const sel = document.getElementById('langSel');
  if (!sel) return;
  const saved = localStorage.getItem('edu_lang');
  if (saved) [...sel.options].forEach(o => { o.selected = (o.value === saved); });
  sel.addEventListener('change', e => localStorage.setItem('edu_lang', e.target.value));
}

/* ---- Keyboard shortcut ---- */

function initInputEnter() {
  const input = document.getElementById('msgInput');
  if (!input) return;
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(input.value); }
  });
}

/* ---- Auto-resize textarea ---- */

function initAutoResize() {
  const input = document.getElementById('msgInput');
  if (!input) return;
  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
  });
}

/* ---- Init ---- */

document.addEventListener('DOMContentLoaded', async () => {
  initLangPersist();
  initInputEnter();
  initAutoResize();
  // Pre-warm browser speech voices (some browsers load them lazily)
  if (window.speechSynthesis) window.speechSynthesis.getVoices();
  // Check once whether server-side Piper TTS is available.
  // If not, all Listen buttons will use browser speech — no 503 errors.
  try {
    const s = await fetch('/api/status').then(r => r.json());
    window._serverTtsAvailable = !!s.tts;
  } catch (_) {
    window._serverTtsAvailable = false;
  }
});
