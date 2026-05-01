/**
 * podcast.js — EduNode podcast module
 * Generates podcast script, renders MAYA/NIKO coloured lines, plays audio.
 *
 * Expected DOM IDs (provided by podcast.html):
 *   #topicInput, #langSel, #generateBtn
 *   #podcastResult, #audioPlayer, #audioEl, #scriptContainer
 */

/* ---- Helpers ---- */

function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function getLang() { return document.getElementById('langSel').value; }

/* ---- Generate ---- */

async function generatePodcast() {
  const topic = document.getElementById('topicInput').value.trim();
  if (!topic) { alert('Please enter a topic.'); return; }

  const btn = document.getElementById('generateBtn');
  btn.disabled = true;
  btn.textContent = 'Generating…';
  document.getElementById('podcastResult').style.display = 'none';

  try {
    const r = await fetch('/api/podcast/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, language: getLang() }),
    });
    const d = await r.json();
    _renderScript(d.script || '');

    const player = document.getElementById('audioPlayer');
    const audio  = document.getElementById('audioEl');
    if (d.audio_url) {
      audio.src = d.audio_url;
      player.style.display = 'flex';
      audio.play().catch(() => {});
    } else {
      player.style.display = 'none';
    }
    document.getElementById('podcastResult').style.display = 'block';
  } catch (e) {
    alert('Error: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generate Episode';
  }
}

/* ---- Render script ---- */

function _renderScript(script) {
  const container = document.getElementById('scriptContainer');
  container.innerHTML = '';

  script.split('\n').forEach(line => {
    if (!line.trim()) return;

    const div = document.createElement('div');
    div.className = 'script-line';

    const isMaya = /^MAYA\s*:/i.test(line);
    const isNiko = /^NIKO\s*:/i.test(line);

    if (isMaya || isNiko) {
      const who  = isMaya ? 'MAYA' : 'NIKO';
      const cls  = isMaya ? 'maya' : 'niko';
      const text = line.replace(/^(MAYA|NIKO)\s*:\s*/i, '');
      div.innerHTML =
        `<span class="speaker ${cls}">${who}:</span>${escHtml(text)}`;
    } else {
      div.textContent = line;
    }

    container.appendChild(div);
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

document.addEventListener('DOMContentLoaded', _initLangPersist);
