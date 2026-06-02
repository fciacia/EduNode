/* i18n.js — Edge UI translations for 11 ASEAN languages */
(function () {
  'use strict';

  const TRANSLATIONS = {
    'English': {
      'nav.quiz':              '🧠 Quiz',
      'nav.cards':             '🃏 Cards',
      'nav.podcast':           '🎧 Podcast',
      'nav.progress':          '🏆 Progress',
      'home.subtitle':         'Your offline AI learning buddy! ✨',
      'home.guide.title':      'Hey there, learner!',
      'home.guide.body':       'Pick a subject below to start chatting with your AI tutor. You can ask questions, take quizzes, study with flashcards, or even listen to a fun podcast!',
      'home.lang.label':       '🌏 Language:',
      'home.subjects.label':   '📚 Choose a subject to get started',
      'home.activities.label': '🚀 Other activities',
      'home.quiz':             '🧠 Take a Quiz',
      'home.flashcard':        '🃏 Flashcards',
      'home.podcast':          '🎧 Podcast',
      'home.progress':         '🏆 My Progress',
      'subject.Mathematics':          'Mathematics',
      'subject.Science':              'Science',
      'subject.English Language':     'English Language',
      'subject.Environmental Studies':'Environmental Studies',
      'subject.Digital Literacy':     'Digital Literacy',
      'onb.level.title': 'What school level are you?',
      'onb.level.sub':   'This helps me explain things just right for you!',
      'onb.primary':     'Primary',
      'onb.primary.sub': 'Grade 1 – 6',
      'onb.secondary':     'Secondary',
      'onb.secondary.sub': 'Grade 7 – 12',
      'onb.skip':        'Skip for now',
    },

    'Filipino': {
      'nav.quiz':              '🧠 Quiz',
      'nav.cards':             '🃏 Mga Kard',
      'nav.podcast':           '🎧 Podcast',
      'nav.progress':          '🏆 Progreso',
      'home.subtitle':         'Ang iyong offline AI na kasama sa pag-aaral! ✨',
      'home.guide.title':      'Huy, mag-aaral! 👋',
      'home.guide.body':       'Pumili ng paksa sa ibaba para magsimulang makipag-chat sa iyong AI tutor. Maaari kang magtanong, sumagot sa quiz, mag-aral gamit ang flashcards, o makinig ng masayang podcast!',
      'home.lang.label':       '🌏 Wika:',
      'home.subjects.label':   '📚 Pumili ng paksa para magsimula',
      'home.activities.label': '🚀 Iba pang gawain',
      'home.quiz':             '🧠 Sumagot ng Quiz',
      'home.flashcard':        '🃏 Flashcards',
      'home.podcast':          '🎧 Podcast',
      'home.progress':         '🏆 Aking Progreso',
      'subject.Mathematics':          'Matematika',
      'subject.Science':              'Agham',
      'subject.English Language':     'Wikang Ingles',
      'subject.Environmental Studies':'Pag-aaral ng Kalikasan',
      'subject.Digital Literacy':     'Literasyang Digital',
      'onb.level.title': 'Anong antas ng paaralan mo?',
      'onb.level.sub':   'Tutulungan kita ng AI tutor na naaayon sa iyong antas!',
      'onb.primary':     'Primarya',
      'onb.primary.sub': 'Baitang 1 – 6',
      'onb.secondary':     'Sekundarya',
      'onb.secondary.sub': 'Baitang 7 – 12',
      'onb.skip':        'Laktawan muna',
    },

    'Bahasa Melayu': {
      'nav.quiz':              '🧠 Kuiz',
      'nav.cards':             '🃏 Kad',
      'nav.podcast':           '🎧 Podcast',
      'nav.progress':          '🏆 Kemajuan',
      'home.subtitle':         'Kawan belajar AI offline kamu! ✨',
      'home.guide.title':      'Hai, pelajar! 👋',
      'home.guide.body':       'Pilih mata pelajaran di bawah untuk mula berbual dengan tutor AI kamu. Boleh tanya soalan, ambil kuiz, belajar dengan kad imbas, atau dengar podcast yang seronok, lah!',
      'home.lang.label':       '🌏 Bahasa:',
      'home.subjects.label':   '📚 Pilih mata pelajaran untuk mula',
      'home.activities.label': '🚀 Aktiviti lain',
      'home.quiz':             '🧠 Ambil Kuiz',
      'home.flashcard':        '🃏 Kad Imbas',
      'home.podcast':          '🎧 Podcast',
      'home.progress':         '🏆 Kemajuan Saya',
      'subject.Mathematics':          'Matematik',
      'subject.Science':              'Sains',
      'subject.English Language':     'Bahasa Inggeris',
      'subject.Environmental Studies':'Kajian Alam Sekitar',
      'subject.Digital Literacy':     'Literasi Digital',
      'onb.level.title': 'Apakah tahap persekolahan kamu?',
      'onb.level.sub':   'Ini membantu tutor AI terangkan dengan cara yang sesuai!',
      'onb.primary':     'Rendah',
      'onb.primary.sub': 'Tahun 1 – 6',
      'onb.secondary':     'Menengah',
      'onb.secondary.sub': 'Tingkatan 7 – 12',
      'onb.skip':        'Langkau dulu',
    },

    'Bahasa Indonesia': {
      'nav.quiz':              '🧠 Kuis',
      'nav.cards':             '🃏 Kartu',
      'nav.podcast':           '🎧 Podcast',
      'nav.progress':          '🏆 Kemajuan',
      'home.subtitle':         'Teman belajar AI offline kamu! ✨',
      'home.guide.title':      'Hei, pelajar! 👋',
      'home.guide.body':       'Pilih mata pelajaran di bawah untuk mulai ngobrol dengan tutor AI kamu. Kamu bisa tanya pertanyaan, ambil kuis, belajar pakai kartu, atau dengarkan podcast yang seru!',
      'home.lang.label':       '🌏 Bahasa:',
      'home.subjects.label':   '📚 Pilih mata pelajaran untuk mulai',
      'home.activities.label': '🚀 Aktivitas lain',
      'home.quiz':             '🧠 Ambil Kuis',
      'home.flashcard':        '🃏 Kartu Belajar',
      'home.podcast':          '🎧 Podcast',
      'home.progress':         '🏆 Kemajuan Saya',
      'subject.Mathematics':          'Matematika',
      'subject.Science':              'IPA',
      'subject.English Language':     'Bahasa Inggris',
      'subject.Environmental Studies':'Studi Lingkungan Hidup',
      'subject.Digital Literacy':     'Literasi Digital',
      'onb.level.title': 'Kamu kelas berapa sekarang?',
      'onb.level.sub':   'Ini bantu tutor AI jelaskan dengan cara yang pas buat kamu!',
      'onb.primary':     'SD',
      'onb.primary.sub': 'Kelas 1 – 6',
      'onb.secondary':     'SMP/SMA',
      'onb.secondary.sub': 'Kelas 7 – 12',
      'onb.skip':        'Lewati dulu',
    },

    'Thai': {
      'nav.quiz':              '🧠 แบบทดสอบ',
      'nav.cards':             '🃏 บัตรคำ',
      'nav.podcast':           '🎧 พอดแคสต์',
      'nav.progress':          '🏆 ความก้าวหน้า',
      'home.subtitle':         'เพื่อนเรียน AI ออฟไลน์ของคุณ! ✨',
      'home.guide.title':      'สวัสดี นักเรียน! 👋',
      'home.guide.body':       'เลือกวิชาด้านล่างเพื่อเริ่มต้นคุยกับครู AI ของคุณ! สามารถถามคำถาม ทำแบบทดสอบ เรียนด้วยบัตรคำ หรือฟัง podcast ได้เลย!',
      'home.lang.label':       '🌏 ภาษา:',
      'home.subjects.label':   '📚 เลือกวิชาเพื่อเริ่มต้น',
      'home.activities.label': '🚀 กิจกรรมอื่นๆ',
      'home.quiz':             '🧠 ทำแบบทดสอบ',
      'home.flashcard':        '🃏 บัตรคำ',
      'home.podcast':          '🎧 พอดแคสต์',
      'home.progress':         '🏆 ความก้าวหน้าของฉัน',
      'subject.Mathematics':          'คณิตศาสตร์',
      'subject.Science':              'วิทยาศาสตร์',
      'subject.English Language':     'ภาษาอังกฤษ',
      'subject.Environmental Studies':'สิ่งแวดล้อมศึกษา',
      'subject.Digital Literacy':     'ทักษะดิจิทัล',
      'onb.level.title': 'คุณเรียนอยู่ระดับไหน?',
      'onb.level.sub':   'ครู AI จะอธิบายให้เหมาะกับระดับของคุณ!',
      'onb.primary':     'ประถม',
      'onb.primary.sub': 'ชั้น ป.1 – ป.6',
      'onb.secondary':     'มัธยม',
      'onb.secondary.sub': 'ชั้น ม.1 – ม.6',
      'onb.skip':        'ข้ามไปก่อน',
    },

    'Vietnamese': {
      'nav.quiz':              '🧠 Kiểm Tra',
      'nav.cards':             '🃏 Thẻ Học',
      'nav.podcast':           '🎧 Podcast',
      'nav.progress':          '🏆 Tiến Độ',
      'home.subtitle':         'Bạn học AI ngoại tuyến của bạn! ✨',
      'home.guide.title':      'Xin chào, học sinh! 👋',
      'home.guide.body':       'Chọn môn học bên dưới để bắt đầu trò chuyện với gia sư AI. Bạn có thể đặt câu hỏi, làm bài kiểm tra, học thẻ, hoặc nghe podcast vui nhộn!',
      'home.lang.label':       '🌏 Ngôn ngữ:',
      'home.subjects.label':   '📚 Chọn môn học để bắt đầu',
      'home.activities.label': '🚀 Hoạt động khác',
      'home.quiz':             '🧠 Làm Bài Kiểm Tra',
      'home.flashcard':        '🃏 Thẻ Học',
      'home.podcast':          '🎧 Podcast',
      'home.progress':         '🏆 Tiến Độ Của Tôi',
      'subject.Mathematics':          'Toán học',
      'subject.Science':              'Khoa học',
      'subject.English Language':     'Tiếng Anh',
      'subject.Environmental Studies':'Môi trường',
      'subject.Digital Literacy':     'Kỹ năng Số',
      'onb.level.title': 'Bạn đang học lớp mấy?',
      'onb.level.sub':   'Điều này giúp gia sư AI giải thích phù hợp với bạn!',
      'onb.primary':     'Tiểu học',
      'onb.primary.sub': 'Lớp 1 – 6',
      'onb.secondary':     'Trung học',
      'onb.secondary.sub': 'Lớp 7 – 12',
      'onb.skip':        'Bỏ qua lúc này',
    },

    'Khmer': {
      'nav.quiz':              '🧠 តេស្ត',
      'nav.cards':             '🃏 កាត',
      'nav.podcast':           '🎧 ផតខាស',
      'nav.progress':          '🏆 វឌ្ឍនភាព',
      'home.subtitle':         'មិត្តរៀន AI ក្រៅបណ្តាញរបស់អ្នក! ✨',
      'home.guide.title':      'សួស្តី! 👋',
      'home.guide.body':       'ជ្រើសរើសមុខវិជ្ជាខាងក្រោម ដើម្បីចាប់ផ្តើមជជែកជាមួយគ្រូ AI!',
      'home.lang.label':       '🌏 ភាសា:',
      'home.subjects.label':   '📚 ជ្រើសរើសមុខវិជ្ជា',
      'home.activities.label': '🚀 សកម្មភាពផ្សេង',
      'home.quiz':             '🧠 ធ្វើតេស្ត',
      'home.flashcard':        '🃏 កាតសិក្សា',
      'home.podcast':          '🎧 ផតខាស',
      'home.progress':         '🏆 វឌ្ឍនភាពខ្ញុំ',
      'subject.Mathematics':          'គណិតវិទ្យា',
      'subject.Science':              'វិទ្យាសាស្ត្រ',
      'subject.English Language':     'ភាសាអង់គ្លេស',
      'subject.Environmental Studies':'សិក្សាបរិស្ថាន',
      'subject.Digital Literacy':     'ចំណេះដឹងឌីជីថល',
      'onb.level.title': 'អ្នកនៅកម្រិតអ្វី?',
      'onb.level.sub':   'គ្រូ AI នឹងពន្យល់ត្រូវតាមកម្រិតរបស់អ្នក!',
      'onb.primary':     'បឋមសិក្សា',
      'onb.primary.sub': 'ថ្នាក់ 1 – 6',
      'onb.secondary':     'មធ្យមសិក្សា',
      'onb.secondary.sub': 'ថ្នាក់ 7 – 12',
      'onb.skip':        'រំលងសិន',
    },

    'Lao': {
      'nav.quiz':              '🧠 ທົດສອບ',
      'nav.cards':             '🃏 ໄພ້ຮຽນ',
      'nav.podcast':           '🎧 ພອດຄາສ',
      'nav.progress':          '🏆 ຄວາມຄືບໜ້າ',
      'home.subtitle':         'ໝູ່ຮຽນ AI ອອບໄລນ໌ຂອງທ່ານ! ✨',
      'home.guide.title':      'ສະບາຍດີ ນັກຮຽນ! 👋',
      'home.guide.body':       'ເລືອກວິຊາຂ້າງລຸ່ມ ເພື່ອເລີ່ມຄຸຍກັບຄູ AI ຂອງທ່ານ!',
      'home.lang.label':       '🌏 ພາສາ:',
      'home.subjects.label':   '📚 ເລືອກວິຊາເພື່ອເລີ່ມ',
      'home.activities.label': '🚀 ກິດຈະກໍາອື່ນ',
      'home.quiz':             '🧠 ເຮັດຂໍ້ສອບ',
      'home.flashcard':        '🃏 ໄພ້ຮຽນ',
      'home.podcast':          '🎧 ພອດຄາສ',
      'home.progress':         '🏆 ຄວາມຄືບໜ້າຂອງຂ້ອຍ',
      'subject.Mathematics':          'ຄະນິດສາດ',
      'subject.Science':              'ວິທະຍາສາດ',
      'subject.English Language':     'ພາສາອັງກິດ',
      'subject.Environmental Studies':'ສິ່ງແວດລ້ອມ',
      'subject.Digital Literacy':     'ດ້ານດິຈິຕ້ອລ',
      'onb.level.title': 'ທ່ານຢູ່ລະດັບໃດ?',
      'onb.level.sub':   'ຄູ AI ຈະອະທິບາຍໃຫ້ເໝາະກັບລະດັບຂອງທ່ານ!',
      'onb.primary':     'ປະຖົມ',
      'onb.primary.sub': 'ຊັ້ນ 1 – 6',
      'onb.secondary':     'ມັດທະຍົມ',
      'onb.secondary.sub': 'ຊັ້ນ 7 – 12',
      'onb.skip':        'ຂ້າມກ່ອນ',
    },

    'Burmese': {
      'nav.quiz':              '🧠 Quiz',
      'nav.cards':             '🃏 ကတ်',
      'nav.podcast':           '🎧 Podcast',
      'nav.progress':          '🏆 တိုးတက်မှု',
      'home.subtitle':         'သင်၏ AI သင်ကြားမှုဖော်ရှိ! ✨',
      'home.guide.title':      'မင်္ဂလာပါ ကျောင်းသား! 👋',
      'home.guide.body':       'အောက်ပါဘာသာရပ်တစ်ခုကို ရွေးချယ်ပြီး AI ဆရာနှင့် ပြောဆိုပါ!',
      'home.lang.label':       '🌏 ဘာသာ:',
      'home.subjects.label':   '📚 ဘာသာရပ်ရွေးချယ်ပါ',
      'home.activities.label': '🚀 အခြားလှုပ်ရှားမှုများ',
      'home.quiz':             '🧠 စစ်ဆေးမှုလုပ်ပါ',
      'home.flashcard':        '🃏 ဖလက်ရှ်ကတ်',
      'home.podcast':          '🎧 Podcast',
      'home.progress':         '🏆 ကျွန်ုပ်တိုးတက်မှု',
      'subject.Mathematics':          'သင်္ချာ',
      'subject.Science':              'သိပ္ပံ',
      'subject.English Language':     'အင်္ဂလိပ်ဘာသာ',
      'subject.Environmental Studies':'ပတ်ဝန်းကျင်လေ့လာမှု',
      'subject.Digital Literacy':     'ဒစ်ဂျစ်တယ်ကျွမ်းကျင်မှု',
      'onb.level.title': 'ကျောင်းအဆင့်ဘယ်လောက်ရှိလဲ?',
      'onb.level.sub':   'AI ဆရာ သင့်အဆင့်နဲ့ ကိုက်ညီအောင် ရှင်းပြပေးမယ်!',
      'onb.primary':     'မူလတန်း',
      'onb.primary.sub': 'တန်း ၁ – ၆',
      'onb.secondary':     'အလယ်တန်း',
      'onb.secondary.sub': 'တန်း ၇ – ၁၂',
      'onb.skip':        'ကျော်သွားဦး',
    },

    'Cebuano': {
      'nav.quiz':              '🧠 Quiz',
      'nav.cards':             '🃏 Mga Kard',
      'nav.podcast':           '🎧 Podcast',
      'nav.progress':          '🏆 Progreso',
      'home.subtitle':         'Ang imong AI kauban sa pagkat-on nga offline! ✨',
      'home.guide.title':      'Kumusta, estudyante! 👋',
      'home.guide.body':       'Pagpili og sumod para magsugod og chat sa imong AI tutor. Makahimo kag pangutana, mosulay og quiz, magtuon gamit ang flashcards, o mamati og podcast!',
      'home.lang.label':       '🌏 Lengguwahe:',
      'home.subjects.label':   '📚 Pagpili og sumod para magsugod',
      'home.activities.label': '🚀 Ubang mga Kalihokan',
      'home.quiz':             '🧠 Kumuha og Quiz',
      'home.flashcard':        '🃏 Flashcards',
      'home.podcast':          '🎧 Podcast',
      'home.progress':         '🏆 Akong Progreso',
      'subject.Mathematics':          'Matematika',
      'subject.Science':              'Siyensya',
      'subject.English Language':     'English Language',
      'subject.Environmental Studies':'Pag-aral sa Kinaiyahan',
      'subject.Digital Literacy':     'Dihital nga Literacy',
      'onb.level.title': 'Unsang lebel sa eskwelahan ikaw?',
      'onb.level.sub':   'Tabangan ka sa AI tutor base sa imong lebel!',
      'onb.primary':     'Primarya',
      'onb.primary.sub': 'Grado 1 – 6',
      'onb.secondary':     'Sekundarya',
      'onb.secondary.sub': 'Grado 7 – 12',
      'onb.skip':        'Laktaw una',
    },

    'Iban': {
      'nav.quiz':              '🧠 Quiz',
      'nav.cards':             '🃏 Kad Belajar',
      'nav.podcast':           '🎧 Podcast',
      'nav.progress':          '🏆 Maju',
      'home.subtitle':         'Kaban belajar AI offline nuan! ✨',
      'home.guide.title':      'Selamat datai, pelajar! 👋',
      'home.guide.body':       'Pilih subjek di baruh tu untuk mula bercakap dengan tutor AI nuan!',
      'home.lang.label':       '🌏 Basa:',
      'home.subjects.label':   '📚 Pilih subjek untuk mula',
      'home.activities.label': '🚀 Aktiviti bukai',
      'home.quiz':             '🧠 Ambik Quiz',
      'home.flashcard':        '🃏 Kad Belajar',
      'home.podcast':          '🎧 Podcast',
      'home.progress':         '🏆 Maju Aku',
      'subject.Mathematics':          'Matematik',
      'subject.Science':              'Sains',
      'subject.English Language':     'Bahasa Inggeris',
      'subject.Environmental Studies':'Alam Sekitar',
      'subject.Digital Literacy':     'Literasi Digital',
      'onb.level.title': 'Tahap sekulah kita bisi di manah?',
      'onb.level.sub':   'Iya nuan tutor AI njelaskan dengan cara ti patut!',
      'onb.primary':     'Rendah',
      'onb.primary.sub': 'Taun 1 – 6',
      'onb.secondary':     'Menengah',
      'onb.secondary.sub': 'Taun 7 – 12',
      'onb.skip':        'Liwat dulu',
    },
  };

  function applyLang(lang) {
    const t = TRANSLATIONS[lang] || TRANSLATIONS['English'];

    // Pass 1 — data-i18n attributes
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (t[key] !== undefined) el.innerHTML = t[key];
    });

    // Pass 2 — CSS selector fallback (works on old SW-cached HTML without data-i18n)
    [
      ['.nav-link[href="/quiz"]',              'nav.quiz'],
      ['.nav-link[href="/flashcard"]',         'nav.cards'],
      ['.nav-link[href="/podcast"]',           'nav.podcast'],
      ['.nav-link[href="/progress"]',          'nav.progress'],
      ['.hero-sub',                            'home.subtitle'],
      ['.motivation-text h3',                  'home.guide.title'],
      ['.guide-banner .guide-text h3',         'home.guide.title'],
      ['.motivation-text p',                   'home.guide.body'],
      ['.guide-banner .guide-text p',          'home.guide.body'],
      ['.lang-row label',                      'home.lang.label'],
      ['#subjects-label',                      'home.subjects.label'],
      ['#activities-label',                    'home.activities.label'],
      ['.quick-links-label',                   'home.activities.label'],
      ['.quick-link[href="/quiz"]',            'home.quiz'],
      ['.quick-link[href="/flashcard"]',       'home.flashcard'],
      ['.quick-link[href="/podcast"]',         'home.podcast'],
      ['.quick-link[href="/progress"]',        'home.progress'],
      ['.activity-card[href="/quiz"] .act-name',      'home.quiz'],
      ['.activity-card[href="/flashcard"] .act-name', 'home.flashcard'],
      ['.activity-card[href="/podcast"] .act-name',   'home.podcast'],
      ['.activity-card[href="/progress"] .act-name',  'home.progress'],
    ].forEach(function (pair) {
      var el = document.querySelector(pair[0]);
      if (el && t[pair[1]] !== undefined) el.innerHTML = t[pair[1]];
    });

    // Pass 3 — subject cards without data-i18n (SW-cached old HTML fallback)
    document.querySelectorAll('.subject-card .name:not([data-i18n])').forEach(function (el) {
      if (!el.dataset.subject) el.dataset.subject = el.textContent.trim();
      var key = 'subject.' + el.dataset.subject;
      if (t[key] !== undefined) el.textContent = t[key];
    });

    // Pass 4 — sync the active language chip so it always matches
    var activeChip = null;
    document.querySelectorAll('.lang-chip').forEach(function (c) {
      var isActive = c.dataset.lang === lang;
      c.classList.toggle('active', isActive);
      if (isActive) activeChip = c;
    });
    if (activeChip) activeChip.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });

    // Re-apply level labels in the new language
    if (window.EduOnboarding) window.EduOnboarding.applyLevel();
  }

  function setLang(lang) {
    localStorage.setItem('edu_lang', lang);
    applyLang(lang);
  }

  // Expose BEFORE boot() so onboarding.js country-click handler can call it
  // even if the script is still executing
  window.EduI18n = { applyLang: applyLang, setLang: setLang, TRANSLATIONS: TRANSLATIONS };

  function boot() {
    var lang = localStorage.getItem('edu_lang') || 'English';
    applyLang(lang);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
