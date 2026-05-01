/**
 * quiz.js — EduNode quiz module
 * Handles quiz generation, answer selection, submission, result display.
 *
 * Expected DOM IDs (provided by quiz.html):
 *   #topicInput, #subjectSel, #langSel, #studentName
 *   #generateBtn, #quizArea, #questionsContainer
 *   #scoreCard, #scoreHeading, #scoreSub, #certLinks
 */

/* ---- State ---- */

let _questions = [];
const _selected = {};   // { questionIndex: 'A' | 'B' | 'C' | 'D' }

/* ---- Helpers ---- */

function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function getLang()    { return document.getElementById('langSel').value; }
function getSubject() { return document.getElementById('subjectSel').value; }
function getName()    { return (document.getElementById('studentName')?.value || '').trim() || 'Student'; }

/* ---- Generate ---- */

async function generateQuiz() {
  const topic = document.getElementById('topicInput').value.trim();
  if (!topic) { alert('Please enter a topic.'); return; }

  const btn = document.getElementById('generateBtn');
  btn.disabled = true;
  btn.textContent = 'Generating…';
  document.getElementById('quizArea').style.display = 'none';
  document.getElementById('scoreCard').style.display = 'none';
  Object.keys(_selected).forEach(k => delete _selected[k]);

  try {
    const r = await fetch('/api/quiz/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, language: getLang(), subject: getSubject() }),
    });
    const d = await r.json();
    _questions = d.questions || [];
    if (!_questions.length) { alert('Could not generate quiz. Is Ollama running?'); return; }
    _renderQuestions(_questions);
    document.getElementById('quizArea').style.display = 'block';
  } catch (e) {
    alert('Error: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generate Quiz';
  }
}

/* ---- Render ---- */

function _renderQuestions(qs) {
  const container = document.getElementById('questionsContainer');
  container.innerHTML = '';
  qs.forEach((q, i) => {
    const card = document.createElement('div');
    card.className = 'question-card';
    card.innerHTML = `<div class="q-text">Q${i + 1}. ${escHtml(q.question)}</div>
                      <div class="options" id="opts-${i}"></div>`;
    container.appendChild(card);

    const optsDiv = card.querySelector(`#opts-${i}`);
    q.options.forEach((opt, oi) => {
      const letter = 'ABCD'[oi];
      const btn = document.createElement('button');
      btn.className = 'opt-btn';
      btn.textContent = opt;
      btn.addEventListener('click', () => _selectAnswer(i, letter, optsDiv));
      optsDiv.appendChild(btn);
    });
  });
}

function _selectAnswer(qi, letter, optsDiv) {
  _selected[qi] = letter;
  [...optsDiv.querySelectorAll('.opt-btn')].forEach((b, oi) => {
    b.classList.toggle('selected', 'ABCD'[oi] === letter);
  });
}

/* ---- Submit ---- */

async function submitQuiz() {
  if (Object.keys(_selected).length < _questions.length) {
    if (!confirm('You have unanswered questions. Submit anyway?')) return;
  }

  try {
    const r = await fetch('/api/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        questions: _questions,
        answers: _selected,
        topic: document.getElementById('topicInput').value,
        student_name: getName(),
        language: getLang(),
      }),
    });
    const d = await r.json();
    _markAnswers(d.result);
    _showResults(d.result, d.microcredentials_earned || []);
  } catch (e) {
    alert('Submit error: ' + e.message);
  }
}

function _markAnswers(result) {
  _questions.forEach((q, i) => {
    const optsDiv = document.querySelector(`#opts-${i}`);
    if (!optsDiv) return;
    [...optsDiv.querySelectorAll('.opt-btn')].forEach((b, oi) => {
      const letter = 'ABCD'[oi];
      if (letter === q.answer) b.classList.add('correct');
      else if (_selected[i] === letter) b.classList.add('wrong');
      b.disabled = true;
    });
  });
}

function _showResults(result, certs) {
  const card = document.getElementById('scoreCard');
  document.getElementById('scoreHeading').textContent =
    `Score: ${result.score}/${result.total} (${result.pct}%)`;
  document.getElementById('scoreSub').textContent =
    result.pct >= 70 ? '🎉 Great work!' : 'Keep practising!';

  const certDiv = document.getElementById('certLinks');
  certDiv.innerHTML = '';
  certs.forEach(c => {
    const a = document.createElement('a');
    a.className = 'cert-link';
    a.href = c.cert_url;
    a.target = '_blank';
    a.textContent = `📄 Download ${c.topic} Certificate`;
    certDiv.appendChild(a);
  });

  card.style.display = 'block';
  card.scrollIntoView({ behavior: 'smooth' });
}

/* ---- Reset ---- */

function resetQuiz() {
  document.getElementById('quizArea').style.display = 'none';
  document.getElementById('scoreCard').style.display = 'none';
  document.getElementById('topicInput').value = '';
  _questions.length = 0;
}

/* ---- Language persistence ---- */

function initLangPersist() {
  const sel = document.getElementById('langSel');
  if (!sel) return;
  const saved = localStorage.getItem('edu_lang');
  if (saved) [...sel.options].forEach(o => { o.selected = (o.value === saved); });
  sel.addEventListener('change', e => localStorage.setItem('edu_lang', e.target.value));
}

document.addEventListener('DOMContentLoaded', initLangPersist);
