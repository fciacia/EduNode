'use strict';

// ── DOM refs ────────────────────────────────────────────────────────────────
const chatLog      = document.getElementById('chat-log');
const chatForm     = document.getElementById('chat-form');
const inputEl      = document.getElementById('question-input');
const sendBtn      = document.getElementById('send-btn');
const micBtn       = document.getElementById('mic-btn');
const statusBtn    = document.getElementById('status-btn');
const statusModal  = document.getElementById('status-modal');
const closeModal   = document.getElementById('close-modal');
const statusList   = document.getElementById('status-list');
const subjectSel   = document.getElementById('subject-select');

// ── Chat rendering ──────────────────────────────────────────────────────────

/**
 * Append a chat bubble to the log.
 * @param {'user'|'assistant'} role
 * @param {string} text
 * @param {string|null} [ttsUrl]
 */
function addBubble(role, text, ttsUrl) {
  const wrap   = document.createElement('div');
  wrap.className = `bubble ${role}`;

  const avatar = document.createElement('div');
  avatar.className  = 'avatar';
  avatar.textContent = role === 'user' ? '🧑‍🎓' : '🤖';
  avatar.setAttribute('aria-hidden', 'true');

  const msg = document.createElement('div');
  msg.className = 'message';
  msg.textContent = text;

  if (ttsUrl) {
    const btn      = document.createElement('button');
    btn.className  = 'play-btn';
    btn.textContent = '▶ Listen';
    btn.setAttribute('aria-label', 'Play audio answer');
    let audio = null;
    btn.addEventListener('click', () => {
      if (audio) { audio.pause(); audio.currentTime = 0; }
      audio = new Audio(ttsUrl);
      btn.textContent = '⏸ Playing…';
      audio.play();
      audio.onended = () => { btn.textContent = '▶ Listen'; };
    });
    msg.appendChild(document.createElement('br'));
    msg.appendChild(btn);
  }

  if (role === 'user') {
    wrap.appendChild(msg);
    wrap.appendChild(avatar);
  } else {
    wrap.appendChild(avatar);
    wrap.appendChild(msg);
  }

  chatLog.appendChild(wrap);
  wrap.scrollIntoView({ behavior: 'smooth', block: 'end' });
  return wrap;
}

/** Append the animated "…" typing indicator. Returns the element. */
function addTyping() {
  const wrap = document.createElement('div');
  wrap.className = 'bubble assistant typing';
  wrap.setAttribute('aria-label', 'EduNode is thinking');
  wrap.innerHTML = '<div class="avatar" aria-hidden="true">🤖</div>'
    + '<div class="message">'
    + '<div class="dot"></div><div class="dot"></div><div class="dot"></div>'
    + '</div>';
  chatLog.appendChild(wrap);
  wrap.scrollIntoView({ behavior: 'smooth', block: 'end' });
  return wrap;
}

// ── Text Q&A ────────────────────────────────────────────────────────────────

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const question = inputEl.value.trim();
  if (!question) return;

  inputEl.value    = '';
  inputEl.disabled = true;
  sendBtn.disabled = true;

  addBubble('user', question);
  const typing = addTyping();

  try {
    const res  = await fetch('/api/ask', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        question,
        subject: subjectSel.value || null,
        tts:     true,
      }),
    });
    const data = await res.json();
    typing.remove();
    if (res.ok) {
      addBubble('assistant', data.answer, data.tts_url || null);
    } else {
      addBubble('assistant', `⚠ ${data.error || 'Unexpected error. Please try again.'}`);
    }
  } catch {
    typing.remove();
    addBubble('assistant', '⚠ Network error — check your connection to EduNode.');
  } finally {
    inputEl.disabled = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
});

// ── Voice recording ──────────────────────────────────────────────────────────

let mediaRecorder = null;
let audioChunks   = [];

/** Pick the best supported MIME type for MediaRecorder. */
function bestMime() {
  const candidates = [
    'audio/webm;codecs=opus',
    'audio/webm',
    'audio/ogg;codecs=opus',
    'audio/mp4',
  ];
  return candidates.find((t) => MediaRecorder.isTypeSupported(t)) || '';
}

micBtn.addEventListener('click', async () => {
  // If already recording — stop
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
    return;
  }

  if (!navigator.mediaDevices?.getUserMedia) {
    alert('Your browser does not support microphone access.');
    return;
  }

  let stream;
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch {
    alert('Microphone access was denied. Please allow it in your browser settings.');
    return;
  }

  const mime     = bestMime();
  mediaRecorder  = new MediaRecorder(stream, mime ? { mimeType: mime } : {});
  audioChunks    = [];

  mediaRecorder.ondataavailable = (e) => {
    if (e.data.size > 0) audioChunks.push(e.data);
  };

  mediaRecorder.onstop = () => {
    micBtn.classList.remove('recording');
    micBtn.textContent = '🎤';
    stream.getTracks().forEach((t) => t.stop());

    const blob = new Blob(audioChunks, { type: mediaRecorder.mimeType || 'audio/webm' });
    sendVoice(blob, mediaRecorder.mimeType || 'audio/webm');
  };

  mediaRecorder.start();
  micBtn.classList.add('recording');
  micBtn.textContent = '⏹';
  micBtn.setAttribute('aria-label', 'Stop recording');
});

/** Upload recorded audio blob and display the transcript + answer. */
async function sendVoice(blob, mimeType) {
  const ext = mimeType.includes('ogg')  ? 'ogg'
            : mimeType.includes('mp4')  ? 'm4a'
            : 'webm';

  const fd = new FormData();
  fd.append('audio',   blob, `recording.${ext}`);
  fd.append('subject', subjectSel.value || '');

  const typing = addTyping();

  try {
    const res  = await fetch('/api/voice', { method: 'POST', body: fd });
    const data = await res.json();
    typing.remove();
    if (res.ok) {
      addBubble('user',      `🎤 "${data.transcript}"`);
      addBubble('assistant', data.answer, data.tts_url || null);
    } else {
      addBubble('assistant', `⚠ ${data.error || 'Voice processing failed.'}`);
    }
  } catch {
    typing.remove();
    addBubble('assistant', '⚠ Network error during voice processing.');
  }
}

// ── Status modal ──────────────────────────────────────────────────────────────

statusBtn.addEventListener('click', async () => {
  statusList.innerHTML = '<dt>Checking…</dt>';
  statusModal.showModal();
  try {
    const res  = await fetch('/api/status');
    const d    = await res.json();
    statusList.innerHTML = `
      <dt>AI Model</dt>   <dd>${escHtml(d.model)}</dd>
      <dt>Ollama</dt>     <dd>${d.ollama ? '✅ Running' : '❌ Offline — run <code>ollama serve</code>'}</dd>
      <dt>Voice input</dt><dd>${d.stt    ? '✅ Ready'   : '⚠ Whisper.cpp not installed'}</dd>
      <dt>Audio output</dt><dd>${d.tts   ? '✅ Ready'   : '⚠ Piper TTS not installed'}</dd>
      <dt>Documents</dt>  <dd>${d.docs} chunks indexed</dd>
    `;
  } catch {
    statusList.innerHTML = '<dt>⚠ Could not reach the EduNode server.</dt>';
  }
});

closeModal.addEventListener('click', () => statusModal.close());
statusModal.addEventListener('click', (e) => {
  if (e.target === statusModal) statusModal.close();
});

// ── Utilities ─────────────────────────────────────────────────────────────────

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}
