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

  // Slides-page strings, merged into the per-language tables above. Kept
  // separate so the existing blocks stay untouched.
  const SLIDES_I18N = {
    'English':          { 'nav.slides':'🖥️ Slides', 'slides.title':'Lesson Slides!', 'slides.subtitle':'Turn any topic into a slide deck you can present and narrate — offline', 'slides.topicPh':'Topic (e.g. the water cycle, fractions…)', 'slides.make':'Make Slides', 'slides.making':'Generating…', 'slides.try':'Try', 'slides.narrate':'Narrate', 'slides.stop':'Stop', 'slides.playAll':'Play all', 'slides.present':'Present', 'slides.download':'Download', 'slides.preparing':'Preparing…', 'slides.prev':'Prev', 'slides.next':'Next', 'slides.exit':'Exit', 'slides.fromBook':'From your textbook', 'slides.retry':'Retry', 'slides.errOffline':'The AI tutor is starting up. Please wait a moment and try again.', 'slides.errGen':'Could not make slides for that just now. Try again or a simpler topic.' },
    'Filipino':         { 'nav.slides':'🖥️ Mga Slide', 'slides.title':'Mga Slide ng Aralin!', 'slides.subtitle':'Gawing slide deck ang anumang paksa na maipapakita at maikukuwento mo — offline', 'slides.topicPh':'Paksa (hal. ang water cycle, mga fraction…)', 'slides.make':'Gumawa ng Slide', 'slides.making':'Ginagawa…', 'slides.try':'Subukan', 'slides.narrate':'Basahin', 'slides.stop':'Itigil', 'slides.playAll':'I-play lahat', 'slides.present':'Ipakita', 'slides.download':'I-download', 'slides.preparing':'Inihahanda…', 'slides.prev':'Nakaraan', 'slides.next':'Susunod', 'slides.exit':'Lumabas', 'slides.fromBook':'Mula sa iyong aklat', 'slides.retry':'Subukang muli', 'slides.errOffline':'Nagsisimula pa ang AI tutor. Maghintay sandali at subukang muli.', 'slides.errGen':'Hindi makagawa ng slide ngayon. Subukang muli o mas simpleng paksa.' },
    'Bahasa Melayu':    { 'nav.slides':'🖥️ Slaid', 'slides.title':'Slaid Pelajaran!', 'slides.subtitle':'Tukar mana-mana topik kepada slaid yang boleh kamu bentang dan ceritakan — luar talian', 'slides.topicPh':'Topik (cth. kitaran air, pecahan…)', 'slides.make':'Buat Slaid', 'slides.making':'Menjana…', 'slides.try':'Cuba', 'slides.narrate':'Cerita', 'slides.stop':'Berhenti', 'slides.playAll':'Main semua', 'slides.present':'Bentang', 'slides.download':'Muat turun', 'slides.preparing':'Menyediakan…', 'slides.prev':'Sebelum', 'slides.next':'Seterusnya', 'slides.exit':'Keluar', 'slides.fromBook':'Daripada buku teks kamu', 'slides.retry':'Cuba lagi', 'slides.errOffline':'Tutor AI sedang dimulakan. Sila tunggu sebentar dan cuba lagi.', 'slides.errGen':'Tidak dapat membuat slaid sekarang. Cuba lagi atau topik lebih mudah.' },
    'Bahasa Indonesia': { 'nav.slides':'🖥️ Slide', 'slides.title':'Slide Pelajaran!', 'slides.subtitle':'Ubah topik apa pun menjadi slide yang bisa kamu presentasikan dan ceritakan — offline', 'slides.topicPh':'Topik (mis. siklus air, pecahan…)', 'slides.make':'Buat Slide', 'slides.making':'Membuat…', 'slides.try':'Coba', 'slides.narrate':'Bacakan', 'slides.stop':'Berhenti', 'slides.playAll':'Putar semua', 'slides.present':'Presentasi', 'slides.download':'Unduh', 'slides.preparing':'Menyiapkan…', 'slides.prev':'Sebelumnya', 'slides.next':'Berikutnya', 'slides.exit':'Keluar', 'slides.fromBook':'Dari buku pelajaranmu', 'slides.retry':'Coba lagi', 'slides.errOffline':'Tutor AI sedang dimulai. Tunggu sebentar lalu coba lagi.', 'slides.errGen':'Tidak bisa membuat slide saat ini. Coba lagi atau topik lebih sederhana.' },
    'Thai':             { 'nav.slides':'🖥️ สไลด์', 'slides.title':'สไลด์บทเรียน!', 'slides.subtitle':'เปลี่ยนหัวข้อใดก็ได้ให้เป็นสไลด์ที่นำเสนอและบรรยายได้ — ออฟไลน์', 'slides.topicPh':'หัวข้อ (เช่น วัฏจักรน้ำ เศษส่วน…)', 'slides.make':'สร้างสไลด์', 'slides.making':'กำลังสร้าง…', 'slides.try':'ลองดู', 'slides.narrate':'บรรยาย', 'slides.stop':'หยุด', 'slides.playAll':'เล่นทั้งหมด', 'slides.present':'นำเสนอ', 'slides.download':'ดาวน์โหลด', 'slides.preparing':'กำลังเตรียม…', 'slides.prev':'ก่อนหน้า', 'slides.next':'ถัดไป', 'slides.exit':'ออก', 'slides.fromBook':'จากหนังสือเรียนของคุณ', 'slides.retry':'ลองอีกครั้ง', 'slides.errOffline':'ครู AI กำลังเริ่มทำงาน กรุณารอสักครู่แล้วลองอีกครั้ง', 'slides.errGen':'สร้างสไลด์ไม่ได้ในตอนนี้ ลองอีกครั้งหรือใช้หัวข้อที่ง่ายกว่า' },
    'Vietnamese':       { 'nav.slides':'🖥️ Trình chiếu', 'slides.title':'Trình chiếu bài học!', 'slides.subtitle':'Biến mọi chủ đề thành bộ slide bạn có thể trình bày và thuyết minh — ngoại tuyến', 'slides.topicPh':'Chủ đề (vd. vòng tuần hoàn nước, phân số…)', 'slides.make':'Tạo Slide', 'slides.making':'Đang tạo…', 'slides.try':'Thử', 'slides.narrate':'Đọc', 'slides.stop':'Dừng', 'slides.playAll':'Phát tất cả', 'slides.present':'Trình bày', 'slides.download':'Tải về', 'slides.preparing':'Đang chuẩn bị…', 'slides.prev':'Trước', 'slides.next':'Tiếp', 'slides.exit':'Thoát', 'slides.fromBook':'Từ sách giáo khoa của bạn', 'slides.retry':'Thử lại', 'slides.errOffline':'Gia sư AI đang khởi động. Vui lòng đợi một lát rồi thử lại.', 'slides.errGen':'Hiện chưa tạo được slide. Hãy thử lại hoặc chọn chủ đề đơn giản hơn.' },
    'Khmer':            { 'nav.slides':'🖥️ ស្លាយ', 'slides.title':'ស្លាយមេរៀន!', 'slides.subtitle':'ប្រែប្រួលប្រធានបទណាមួយទៅជាស្លាយ ដែលអ្នកអាចបង្ហាញ និងនិយាយបាន — ក្រៅបណ្តាញ', 'slides.topicPh':'ប្រធានបទ (ឧ. វដ្តទឹក ប្រភាគ…)', 'slides.make':'បង្កើតស្លាយ', 'slides.making':'កំពុងបង្កើត…', 'slides.try':'សាកល្បង', 'slides.narrate':'អាន', 'slides.stop':'ឈប់', 'slides.playAll':'ចាក់ទាំងអស់', 'slides.present':'បង្ហាញ', 'slides.download':'ទាញយក', 'slides.preparing':'កំពុងរៀបចំ…', 'slides.prev':'មុន', 'slides.next':'បន្ទាប់', 'slides.exit':'ចេញ', 'slides.fromBook':'ពីសៀវភៅសិក្សារបស់អ្នក', 'slides.retry':'ព្យាយាមម្តងទៀត', 'slides.errOffline':'គ្រូ AI កំពុងចាប់ផ្តើម។ សូមរង់ចាំបន្តិច ហើយព្យាយាមម្តងទៀត។', 'slides.errGen':'មិនអាចបង្កើតស្លាយឥឡូវនេះទេ។ ព្យាយាមម្តងទៀត ឬប្រធានបទសាមញ្ញជាង។' },
    'Lao':              { 'nav.slides':'🖥️ ສະໄລດ໌', 'slides.title':'ສະໄລດ໌ບົດຮຽນ!', 'slides.subtitle':'ປ່ຽນຫົວຂໍ້ໃດກໍ່ໄດ້ໃຫ້ເປັນສະໄລດ໌ ທີ່ທ່ານສາມາດນຳສະເໜີ ແລະ ບັນລະຍາຍ — ອອບໄລນ໌', 'slides.topicPh':'ຫົວຂໍ້ (ຕົວຢ່າງ: ວົງຈອນນ້ຳ, ເສດສ່ວນ…)', 'slides.make':'ສ້າງສະໄລດ໌', 'slides.making':'ກຳລັງສ້າງ…', 'slides.try':'ລອງ', 'slides.narrate':'ບັນລະຍາຍ', 'slides.stop':'ຢຸດ', 'slides.playAll':'ຫຼິ້ນທັງໝົດ', 'slides.present':'ນຳສະເໜີ', 'slides.download':'ດາວໂຫຼດ', 'slides.preparing':'ກຳລັງກຽມ…', 'slides.prev':'ກ່ອນ', 'slides.next':'ຕໍ່ໄປ', 'slides.exit':'ອອກ', 'slides.fromBook':'ຈາກປຶ້ມຮຽນຂອງທ່ານ', 'slides.retry':'ລອງໃໝ່', 'slides.errOffline':'ຄູ AI ກຳລັງເລີ່ມຕົ້ນ. ກະລຸນາລໍຖ້າ ແລະ ລອງໃໝ່.', 'slides.errGen':'ສ້າງສະໄລດ໌ບໍ່ໄດ້ຕອນນີ້. ລອງໃໝ່ ຫຼື ຫົວຂໍ້ງ່າຍກວ່າ.' },
    'Burmese':          { 'nav.slides':'🖥️ ဆလိုက်', 'slides.title':'သင်ခန်းစာ ဆလိုက်များ!', 'slides.subtitle':'မည်သည့်ခေါင်းစဉ်ကိုမဆို တင်ပြ၍ ရွတ်ဆိုနိုင်သော ဆလိုက်အဖြစ် ပြောင်းပါ — အော့ဖ်လိုင်း', 'slides.topicPh':'ခေါင်းစဉ် (ဥပမာ - ရေသံသရာ၊ အပိုင်းကိန်း…)', 'slides.make':'ဆလိုက်ပြုလုပ်ပါ', 'slides.making':'ပြုလုပ်နေသည်…', 'slides.try':'စမ်းကြည့်ပါ', 'slides.narrate':'ဖတ်ပြ', 'slides.stop':'ရပ်', 'slides.playAll':'အားလုံးဖွင့်', 'slides.present':'တင်ပြ', 'slides.download':'ဒေါင်းလုဒ်', 'slides.preparing':'ပြင်ဆင်နေသည်…', 'slides.prev':'ယခင်', 'slides.next':'နောက်', 'slides.exit':'ထွက်', 'slides.fromBook':'သင့်ကျောင်းစာအုပ်မှ', 'slides.retry':'ထပ်စမ်းပါ', 'slides.errOffline':'AI ဆရာ စတင်နေသည်။ ခဏစောင့်ပြီး ထပ်စမ်းပါ။', 'slides.errGen':'ယခု ဆလိုက်မပြုလုပ်နိုင်ပါ။ ထပ်စမ်းပါ သို့မဟုတ် ပိုရိုးသောခေါင်းစဉ်သုံးပါ။' },
    'Cebuano':          { 'nav.slides':'🖥️ Mga Slide', 'slides.title':'Mga Slide sa Leksyon!', 'slides.subtitle':'Himoa nga slide deck ang bisan unsang topic nga imong mapakita ug maasoy — offline', 'slides.topicPh':'Topic (pananglitan, ang water cycle, mga fraction…)', 'slides.make':'Paghimo og Slide', 'slides.making':'Gihimo…', 'slides.try':'Sulayi', 'slides.narrate':'Basaha', 'slides.stop':'Hunong', 'slides.playAll':'I-play tanan', 'slides.present':'Ipakita', 'slides.download':'I-download', 'slides.preparing':'Giandam…', 'slides.prev':'Miagi', 'slides.next':'Sunod', 'slides.exit':'Gawas', 'slides.fromBook':'Gikan sa imong libro', 'slides.retry':'Sulayi pag-usab', 'slides.errOffline':'Nagsugod pa ang AI tutor. Paghulat kadiyot ug sulayi pag-usab.', 'slides.errGen':'Dili makahimo og slide karon. Sulayi pag-usab o mas simpleng topic.' },
    'Iban':             { 'nav.slides':'🖥️ Slaid', 'slides.title':'Slaid Pelajar!', 'slides.subtitle':'Tukar sebarang topik nyadi slaid ti ulih dipandang sereta dicerita — offline', 'slides.topicPh':'Topik (chunto: pusar ai, pecahan…)', 'slides.make':'Ngaga Slaid', 'slides.making':'Benung ngaga…', 'slides.try':'Cuba', 'slides.narrate':'Cerita', 'slides.stop':'Badu', 'slides.playAll':'Main semua', 'slides.present':'Pandang', 'slides.download':'Unduh', 'slides.preparing':'Benung nyendia…', 'slides.prev':'Sebelum', 'slides.next':'Lalu', 'slides.exit':'Pansut', 'slides.fromBook':'Ari buku nuan', 'slides.retry':'Cuba baru', 'slides.errOffline':'Tutor AI benung berengkah. Nganti sekejap lalu cuba baru.', 'slides.errGen':'Enda ulih ngaga slaid diatu. Cuba baru tauka topik ti mudah agi.' },
  };
  Object.keys(SLIDES_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], SLIDES_I18N[l]);
  });

  var _current = 'English';

  function applyLang(lang) {
    const t = TRANSLATIONS[lang] || TRANSLATIONS['English'];
    _current = TRANSLATIONS[lang] ? lang : 'English';

    // Pass 1 — data-i18n attributes
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (t[key] !== undefined) el.innerHTML = t[key];
    });

    // Pass 1b — translatable placeholders
    document.querySelectorAll('[data-i18n-ph]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-ph');
      if (t[key] !== undefined) el.setAttribute('placeholder', t[key]);
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
  function t(key) {
    var d = TRANSLATIONS[_current] || TRANSLATIONS['English'];
    if (d[key] !== undefined) return d[key];
    return TRANSLATIONS['English'][key] !== undefined ? TRANSLATIONS['English'][key] : key;
  }

  window.EduI18n = { applyLang: applyLang, setLang: setLang, t: t, TRANSLATIONS: TRANSLATIONS };

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
