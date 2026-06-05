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

  // Quiz + Flashcard page strings (shared slides.* keys reused for try/retry/
  // offline/from-textbook/generating/prev/next). {t}/{k}/{total}/{n} are filled in JS.
  const QC_I18N = {
    'English':          { 'ui.enterTopic':'Please enter a topic!', 'quiz.title':'Quiz Challenge!', 'quiz.subtitle':'Test your knowledge and earn certificates', 'quiz.namePh':'Your name…', 'quiz.topicPh':'Enter a topic (e.g. the water cycle, fractions…)', 'quiz.generate':'Generate Quiz', 'quiz.submit':'Submit Answers', 'quiz.newQuiz':'New Quiz', 'quiz.answered':'answered', 'quiz.scoreGood':'Amazing work! Keep it up!', 'quiz.scoreTry':'Good try! Keep practising!', 'quiz.errGen':'Could not make a quiz for that just now. Try again or pick a simpler topic.', 'quiz.confirmSubmit':'You have unanswered questions. Submit anyway?', 'quiz.cert':'Download {t} Certificate', 'cards.title':'Flashcard Deck!', 'cards.subtitle':'Tap a card to flip it and see the answer', 'cards.topicPh':'Topic (e.g. plant cells, multiplication tables…)', 'cards.make':'Make Cards', 'cards.reviewDue':'Review due', 'cards.shuffle':'Shuffle', 'cards.known':'known', 'cards.review':'review', 'cards.concept':'Concept', 'cards.reveal':'Tap to reveal!', 'cards.definition':'Definition', 'cards.reviewAgain':'Review again', 'cards.gotIt':'Got it!', 'cards.deckComplete':'Deck complete!', 'cards.perfect':'Perfect! You know them all!', 'cards.great':'Great work!', 'cards.keepGoing':'Keep practising!', 'cards.mastered':'{k} / {total} cards mastered.', 'cards.markedReview':'{n} marked for review.', 'cards.restart':'Restart', 'cards.reviewMarked':'Review marked', 'cards.errGen':'Could not make cards for that just now. Try again or pick a simpler topic.' },
    'Filipino':         { 'ui.enterTopic':'Maglagay ng paksa!', 'quiz.title':'Hamon sa Quiz!', 'quiz.subtitle':'Subukin ang iyong kaalaman at makakuha ng sertipiko', 'quiz.namePh':'Pangalan mo…', 'quiz.topicPh':'Maglagay ng paksa (hal. ang water cycle, mga fraction…)', 'quiz.generate':'Gumawa ng Quiz', 'quiz.submit':'Isumite ang Sagot', 'quiz.newQuiz':'Bagong Quiz', 'quiz.answered':'nasagot', 'quiz.scoreGood':'Ang galing! Ipagpatuloy mo!', 'quiz.scoreTry':'Magaling! Magpatuloy sa pag-aaral!', 'quiz.errGen':'Hindi makagawa ng quiz ngayon. Subukang muli o mas simpleng paksa.', 'quiz.confirmSubmit':'May hindi pa nasagot. Isusumite pa rin?', 'quiz.cert':'I-download ang Sertipiko ng {t}', 'cards.title':'Deck ng Flashcard!', 'cards.subtitle':'Pindutin ang kard para baligtarin at makita ang sagot', 'cards.topicPh':'Paksa (hal. mga selula ng halaman, multiplication tables…)', 'cards.make':'Gumawa ng Kard', 'cards.reviewDue':'Review na', 'cards.shuffle':'Haluin', 'cards.known':'alam', 'cards.review':'review', 'cards.concept':'Konsepto', 'cards.reveal':'Pindutin para makita!', 'cards.definition':'Kahulugan', 'cards.reviewAgain':'Ulitin', 'cards.gotIt':'Alam ko na!', 'cards.deckComplete':'Tapos na ang deck!', 'cards.perfect':'Perpekto! Alam mo lahat!', 'cards.great':'Ang galing!', 'cards.keepGoing':'Magpatuloy sa pagsasanay!', 'cards.mastered':'{k} / {total} kard ang natutunan.', 'cards.markedReview':'{n} markado para sa review.', 'cards.restart':'Ulitin', 'cards.reviewMarked':'I-review ang markado', 'cards.errGen':'Hindi makagawa ng kard ngayon. Subukang muli o mas simpleng paksa.' },
    'Bahasa Melayu':    { 'ui.enterTopic':'Sila masukkan topik!', 'quiz.title':'Cabaran Kuiz!', 'quiz.subtitle':'Uji pengetahuan kamu dan dapatkan sijil', 'quiz.namePh':'Nama kamu…', 'quiz.topicPh':'Masukkan topik (cth. kitaran air, pecahan…)', 'quiz.generate':'Buat Kuiz', 'quiz.submit':'Hantar Jawapan', 'quiz.newQuiz':'Kuiz Baru', 'quiz.answered':'dijawab', 'quiz.scoreGood':'Hebat! Teruskan!', 'quiz.scoreTry':'Bagus! Teruskan berlatih!', 'quiz.errGen':'Tidak dapat membuat kuiz sekarang. Cuba lagi atau topik lebih mudah.', 'quiz.confirmSubmit':'Ada soalan belum dijawab. Hantar juga?', 'quiz.cert':'Muat turun Sijil {t}', 'cards.title':'Dek Kad Imbas!', 'cards.subtitle':'Ketik kad untuk membaliknya dan lihat jawapan', 'cards.topicPh':'Topik (cth. sel tumbuhan, sifir…)', 'cards.make':'Buat Kad', 'cards.reviewDue':'Ulang kaji', 'cards.shuffle':'Kocok', 'cards.known':'tahu', 'cards.review':'ulang', 'cards.concept':'Konsep', 'cards.reveal':'Ketik untuk lihat!', 'cards.definition':'Takrif', 'cards.reviewAgain':'Ulang semula', 'cards.gotIt':'Faham!', 'cards.deckComplete':'Dek selesai!', 'cards.perfect':'Sempurna! Kamu tahu semua!', 'cards.great':'Kerja yang bagus!', 'cards.keepGoing':'Teruskan berlatih!', 'cards.mastered':'{k} / {total} kad dikuasai.', 'cards.markedReview':'{n} ditanda untuk ulang kaji.', 'cards.restart':'Mula semula', 'cards.reviewMarked':'Ulang yang ditanda', 'cards.errGen':'Tidak dapat membuat kad sekarang. Cuba lagi atau topik lebih mudah.' },
    'Bahasa Indonesia': { 'ui.enterTopic':'Silakan masukkan topik!', 'quiz.title':'Tantangan Kuis!', 'quiz.subtitle':'Uji pengetahuanmu dan dapatkan sertifikat', 'quiz.namePh':'Namamu…', 'quiz.topicPh':'Masukkan topik (mis. siklus air, pecahan…)', 'quiz.generate':'Buat Kuis', 'quiz.submit':'Kirim Jawaban', 'quiz.newQuiz':'Kuis Baru', 'quiz.answered':'dijawab', 'quiz.scoreGood':'Hebat! Pertahankan!', 'quiz.scoreTry':'Bagus! Terus berlatih!', 'quiz.errGen':'Tidak bisa membuat kuis saat ini. Coba lagi atau topik lebih sederhana.', 'quiz.confirmSubmit':'Ada soal yang belum dijawab. Tetap kirim?', 'quiz.cert':'Unduh Sertifikat {t}', 'cards.title':'Dek Kartu Belajar!', 'cards.subtitle':'Ketuk kartu untuk membaliknya dan lihat jawaban', 'cards.topicPh':'Topik (mis. sel tumbuhan, tabel perkalian…)', 'cards.make':'Buat Kartu', 'cards.reviewDue':'Perlu diulang', 'cards.shuffle':'Acak', 'cards.known':'tahu', 'cards.review':'ulang', 'cards.concept':'Konsep', 'cards.reveal':'Ketuk untuk lihat!', 'cards.definition':'Definisi', 'cards.reviewAgain':'Ulangi', 'cards.gotIt':'Paham!', 'cards.deckComplete':'Dek selesai!', 'cards.perfect':'Sempurna! Kamu tahu semua!', 'cards.great':'Kerja bagus!', 'cards.keepGoing':'Terus berlatih!', 'cards.mastered':'{k} / {total} kartu dikuasai.', 'cards.markedReview':'{n} ditandai untuk diulang.', 'cards.restart':'Mulai ulang', 'cards.reviewMarked':'Ulang yang ditandai', 'cards.errGen':'Tidak bisa membuat kartu saat ini. Coba lagi atau topik lebih sederhana.' },
    'Thai':             { 'ui.enterTopic':'กรุณาใส่หัวข้อ!', 'quiz.title':'ท้าทายควิซ!', 'quiz.subtitle':'ทดสอบความรู้ของคุณและรับใบประกาศ', 'quiz.namePh':'ชื่อของคุณ…', 'quiz.topicPh':'ใส่หัวข้อ (เช่น วัฏจักรน้ำ เศษส่วน…)', 'quiz.generate':'สร้างควิซ', 'quiz.submit':'ส่งคำตอบ', 'quiz.newQuiz':'ควิซใหม่', 'quiz.answered':'ตอบแล้ว', 'quiz.scoreGood':'เยี่ยมมาก! ทำต่อไป!', 'quiz.scoreTry':'พยายามได้ดี! ฝึกต่อไป!', 'quiz.errGen':'สร้างควิซไม่ได้ในตอนนี้ ลองอีกครั้งหรือเลือกหัวข้อที่ง่ายกว่า', 'quiz.confirmSubmit':'ยังมีข้อที่ไม่ได้ตอบ ส่งเลยไหม?', 'quiz.cert':'ดาวน์โหลดใบประกาศ {t}', 'cards.title':'ชุดบัตรคำ!', 'cards.subtitle':'แตะบัตรเพื่อพลิกดูคำตอบ', 'cards.topicPh':'หัวข้อ (เช่น เซลล์พืช สูตรคูณ…)', 'cards.make':'สร้างบัตร', 'cards.reviewDue':'ถึงเวลาทบทวน', 'cards.shuffle':'สับ', 'cards.known':'รู้แล้ว', 'cards.review':'ทบทวน', 'cards.concept':'แนวคิด', 'cards.reveal':'แตะเพื่อดู!', 'cards.definition':'ความหมาย', 'cards.reviewAgain':'ทบทวนอีก', 'cards.gotIt':'เข้าใจแล้ว!', 'cards.deckComplete':'จบชุดแล้ว!', 'cards.perfect':'สมบูรณ์แบบ! คุณรู้ทั้งหมด!', 'cards.great':'เยี่ยมมาก!', 'cards.keepGoing':'ฝึกต่อไป!', 'cards.mastered':'เชี่ยวชาญ {k} / {total} บัตร', 'cards.markedReview':'ทำเครื่องหมายทบทวน {n} ใบ', 'cards.restart':'เริ่มใหม่', 'cards.reviewMarked':'ทบทวนที่ทำเครื่องหมาย', 'cards.errGen':'สร้างบัตรไม่ได้ในตอนนี้ ลองอีกครั้งหรือเลือกหัวข้อที่ง่ายกว่า' },
    'Vietnamese':       { 'ui.enterTopic':'Vui lòng nhập chủ đề!', 'quiz.title':'Thử thách Kiểm tra!', 'quiz.subtitle':'Kiểm tra kiến thức và nhận chứng chỉ', 'quiz.namePh':'Tên của bạn…', 'quiz.topicPh':'Nhập chủ đề (vd. vòng tuần hoàn nước, phân số…)', 'quiz.generate':'Tạo Bài Kiểm Tra', 'quiz.submit':'Nộp Bài', 'quiz.newQuiz':'Bài Mới', 'quiz.answered':'đã trả lời', 'quiz.scoreGood':'Tuyệt vời! Cứ thế nhé!', 'quiz.scoreTry':'Cố gắng tốt! Tiếp tục luyện tập!', 'quiz.errGen':'Hiện chưa tạo được bài kiểm tra. Hãy thử lại hoặc chọn chủ đề đơn giản hơn.', 'quiz.confirmSubmit':'Bạn còn câu chưa trả lời. Vẫn nộp chứ?', 'quiz.cert':'Tải chứng chỉ {t}', 'cards.title':'Bộ Thẻ Học!', 'cards.subtitle':'Chạm vào thẻ để lật và xem đáp án', 'cards.topicPh':'Chủ đề (vd. tế bào thực vật, bảng cửu chương…)', 'cards.make':'Tạo Thẻ', 'cards.reviewDue':'Cần ôn', 'cards.shuffle':'Xáo trộn', 'cards.known':'đã biết', 'cards.review':'ôn lại', 'cards.concept':'Khái niệm', 'cards.reveal':'Chạm để xem!', 'cards.definition':'Định nghĩa', 'cards.reviewAgain':'Ôn lại', 'cards.gotIt':'Hiểu rồi!', 'cards.deckComplete':'Hoàn thành bộ thẻ!', 'cards.perfect':'Hoàn hảo! Bạn biết hết!', 'cards.great':'Làm tốt lắm!', 'cards.keepGoing':'Tiếp tục luyện tập!', 'cards.mastered':'Đã thuộc {k} / {total} thẻ.', 'cards.markedReview':'{n} thẻ được đánh dấu ôn lại.', 'cards.restart':'Bắt đầu lại', 'cards.reviewMarked':'Ôn thẻ đã đánh dấu', 'cards.errGen':'Hiện chưa tạo được thẻ. Hãy thử lại hoặc chọn chủ đề đơn giản hơn.' },
    'Khmer':            { 'ui.enterTopic':'សូមបញ្ចូលប្រធានបទ!', 'quiz.title':'បញ្ហាប្រកួតសំណួរ!', 'quiz.subtitle':'សាកល្បងចំណេះដឹងរបស់អ្នក ហើយទទួលបានវិញ្ញាបនបត្រ', 'quiz.namePh':'ឈ្មោះរបស់អ្នក…', 'quiz.topicPh':'បញ្ចូលប្រធានបទ (ឧ. វដ្តទឹក ប្រភាគ…)', 'quiz.generate':'បង្កើតសំណួរ', 'quiz.submit':'ដាក់ស្នើចម្លើយ', 'quiz.newQuiz':'សំណួរថ្មី', 'quiz.answered':'បានឆ្លើយ', 'quiz.scoreGood':'ល្អណាស់! បន្តទៅ!', 'quiz.scoreTry':'ល្អ! បន្តអនុវត្ត!', 'quiz.errGen':'មិនអាចបង្កើតសំណួរឥឡូវនេះទេ។ ព្យាយាមម្តងទៀត ឬប្រធានបទសាមញ្ញជាង។', 'quiz.confirmSubmit':'នៅមានសំណួរមិនទាន់ឆ្លើយ។ ដាក់ស្នើដែរឬ?', 'quiz.cert':'ទាញយកវិញ្ញាបនបត្រ {t}', 'cards.title':'កញ្ចប់កាតសិក្សា!', 'cards.subtitle':'ប៉ះកាតដើម្បីត្រឡប់ និងមើលចម្លើយ', 'cards.topicPh':'ប្រធានបទ (ឧ. កោសិការុក្ខជាតិ តារាងគុណ…)', 'cards.make':'បង្កើតកាត', 'cards.reviewDue':'ត្រូវរំលឹក', 'cards.shuffle':'លាយ', 'cards.known':'ដឹង', 'cards.review':'រំលឹក', 'cards.concept':'គំនិត', 'cards.reveal':'ប៉ះដើម្បីមើល!', 'cards.definition':'និយមន័យ', 'cards.reviewAgain':'រំលឹកម្តងទៀត', 'cards.gotIt':'យល់ហើយ!', 'cards.deckComplete':'ចប់កញ្ចប់ហើយ!', 'cards.perfect':'ល្អឥតខ្ចោះ! អ្នកដឹងទាំងអស់!', 'cards.great':'ល្អណាស់!', 'cards.keepGoing':'បន្តអនុវត្ត!', 'cards.mastered':'ស្ទាត់ {k} / {total} កាត។', 'cards.markedReview':'សម្គាល់ {n} សម្រាប់រំលឹក។', 'cards.restart':'ចាប់ផ្តើមឡើងវិញ', 'cards.reviewMarked':'រំលឹកអ្វីដែលសម្គាល់', 'cards.errGen':'មិនអាចបង្កើតកាតឥឡូវនេះទេ។ ព្យាយាមម្តងទៀត ឬប្រធានបទសាមញ្ញជាង។' },
    'Lao':              { 'ui.enterTopic':'ກະລຸນາໃສ່ຫົວຂໍ້!', 'quiz.title':'ສິ່ງທ້າທາຍ ຄຳຖາມ!', 'quiz.subtitle':'ທົດສອບຄວາມຮູ້ຂອງທ່ານ ແລະ ຮັບໃບຢັ້ງຢືນ', 'quiz.namePh':'ຊື່ຂອງທ່ານ…', 'quiz.topicPh':'ໃສ່ຫົວຂໍ້ (ຕົວຢ່າງ: ວົງຈອນນ້ຳ, ເສດສ່ວນ…)', 'quiz.generate':'ສ້າງຄຳຖາມ', 'quiz.submit':'ສົ່ງຄຳຕອບ', 'quiz.newQuiz':'ຄຳຖາມໃໝ່', 'quiz.answered':'ຕອບແລ້ວ', 'quiz.scoreGood':'ດີຫຼາຍ! ສືບຕໍ່ໄປ!', 'quiz.scoreTry':'ດີ! ຝຶກຕໍ່ໄປ!', 'quiz.errGen':'ສ້າງຄຳຖາມບໍ່ໄດ້ຕອນນີ້. ລອງໃໝ່ ຫຼື ຫົວຂໍ້ງ່າຍກວ່າ.', 'quiz.confirmSubmit':'ຍັງມີຄຳຖາມບໍ່ທັນຕອບ. ສົ່ງເລີຍບໍ?', 'quiz.cert':'ດາວໂຫຼດໃບຢັ້ງຢືນ {t}', 'cards.title':'ຊຸດໄພ້ຮຽນ!', 'cards.subtitle':'ແຕະໄພ້ເພື່ອປີ້ນ ແລະ ເບິ່ງຄຳຕອບ', 'cards.topicPh':'ຫົວຂໍ້ (ຕົວຢ່າງ: ເຊລພືດ, ຕາຕະລາງຄູນ…)', 'cards.make':'ສ້າງໄພ້', 'cards.reviewDue':'ຮອດເວລາທົບທວນ', 'cards.shuffle':'ສະຫຼັບ', 'cards.known':'ຮູ້', 'cards.review':'ທົບທວນ', 'cards.concept':'ແນວຄິດ', 'cards.reveal':'ແຕະເພື່ອເບິ່ງ!', 'cards.definition':'ນິຍາມ', 'cards.reviewAgain':'ທົບທວນອີກ', 'cards.gotIt':'ເຂົ້າໃຈແລ້ວ!', 'cards.deckComplete':'ຈົບຊຸດແລ້ວ!', 'cards.perfect':'ສົມບູນແບບ! ທ່ານຮູ້ໝົດ!', 'cards.great':'ດີຫຼາຍ!', 'cards.keepGoing':'ຝຶກຕໍ່ໄປ!', 'cards.mastered':'ຊຳນານ {k} / {total} ໄພ້.', 'cards.markedReview':'ໝາຍ {n} ສຳລັບທົບທວນ.', 'cards.restart':'ເລີ່ມໃໝ່', 'cards.reviewMarked':'ທົບທວນທີ່ໝາຍ', 'cards.errGen':'ສ້າງໄພ້ບໍ່ໄດ້ຕອນນີ້. ລອງໃໝ່ ຫຼື ຫົວຂໍ້ງ່າຍກວ່າ.' },
    'Burmese':          { 'ui.enterTopic':'ခေါင်းစဉ်ထည့်ပါ!', 'quiz.title':'Quiz စိန်ခေါ်မှု!', 'quiz.subtitle':'အသိပညာစမ်းသပ်ပြီး လက်မှတ်ရယူပါ', 'quiz.namePh':'သင့်နာမည်…', 'quiz.topicPh':'ခေါင်းစဉ်ထည့်ပါ (ဥပမာ - ရေသံသရာ၊ အပိုင်းကိန်း…)', 'quiz.generate':'Quiz ဖန်တီးပါ', 'quiz.submit':'အဖြေတင်ပါ', 'quiz.newQuiz':'Quiz အသစ်', 'quiz.answered':'ဖြေပြီး', 'quiz.scoreGood':'အရမ်းကောင်းတယ်! ဆက်လုပ်ပါ!', 'quiz.scoreTry':'ကြိုးစားမှုကောင်းတယ်! ဆက်လေ့ကျင့်ပါ!', 'quiz.errGen':'ယခု Quiz မဖန်တီးနိုင်ပါ။ ထပ်စမ်းပါ သို့မဟုတ် ပိုရိုးသောခေါင်းစဉ်သုံးပါ။', 'quiz.confirmSubmit':'မဖြေရသေးသော မေးခွန်းရှိသည်။ တင်မလား?', 'quiz.cert':'{t} လက်မှတ် ဒေါင်းလုဒ်', 'cards.title':'ဖလက်ရှ်ကတ် အစုံ!', 'cards.subtitle':'အဖြေကြည့်ရန် ကတ်ကိုတို့ပါ', 'cards.topicPh':'ခေါင်းစဉ် (ဥပမာ - အပင်ဆဲလ်များ၊ မြှောက်ဇယား…)', 'cards.make':'ကတ်ပြုလုပ်ပါ', 'cards.reviewDue':'ပြန်လည်သုံးသပ်ရန်', 'cards.shuffle':'မွှေပါ', 'cards.known':'သိ', 'cards.review':'ပြန်ကြည့်', 'cards.concept':'အယူအဆ', 'cards.reveal':'ကြည့်ရန်တို့ပါ!', 'cards.definition':'အဓိပ္ပါယ်', 'cards.reviewAgain':'ထပ်ကြည့်', 'cards.gotIt':'နားလည်ပြီ!', 'cards.deckComplete':'အစုံပြီးပါပြီ!', 'cards.perfect':'ပြီးပြည့်စုံ! အကုန်သိတယ်!', 'cards.great':'အရမ်းကောင်းတယ်!', 'cards.keepGoing':'ဆက်လေ့ကျင့်ပါ!', 'cards.mastered':'ကတ် {k} / {total} ကျွမ်းကျင်ပြီ။', 'cards.markedReview':'{n} ကို ပြန်ကြည့်ရန် မှတ်ထားသည်။', 'cards.restart':'ပြန်စပါ', 'cards.reviewMarked':'မှတ်ထားသည်များ ပြန်ကြည့်', 'cards.errGen':'ယခု ကတ်မပြုလုပ်နိုင်ပါ။ ထပ်စမ်းပါ သို့မဟုတ် ပိုရိုးသောခေါင်းစဉ်သုံးပါ။' },
    'Cebuano':          { 'ui.enterTopic':'Palihog pagbutang og topic!', 'quiz.title':'Hagit sa Quiz!', 'quiz.subtitle':'Sulayi ang imong kahibalo ug makakuha og sertipiko', 'quiz.namePh':'Imong ngalan…', 'quiz.topicPh':'Pagbutang og topic (pananglitan, water cycle, mga fraction…)', 'quiz.generate':'Paghimo og Quiz', 'quiz.submit':'Isumiter ang Tubag', 'quiz.newQuiz':'Bag-ong Quiz', 'quiz.answered':'natubag', 'quiz.scoreGood':'Maayo kaayo! Padayon!', 'quiz.scoreTry':'Maayong pagsulay! Padayon sa pagpraktis!', 'quiz.errGen':'Dili makahimo og quiz karon. Sulayi pag-usab o mas simpleng topic.', 'quiz.confirmSubmit':'Naa pay wala matubag. Isumiter gihapon?', 'quiz.cert':'I-download ang Sertipiko sa {t}', 'cards.title':'Deck sa Flashcard!', 'cards.subtitle':'I-tap ang kard aron mabali ug makita ang tubag', 'cards.topicPh':'Topic (pananglitan, mga selula sa tanom, multiplication tables…)', 'cards.make':'Paghimo og Kard', 'cards.reviewDue':'Repaso na', 'cards.shuffle':'Sagol', 'cards.known':'nahibal-an', 'cards.review':'repaso', 'cards.concept':'Konsepto', 'cards.reveal':'I-tap aron makita!', 'cards.definition':'Kahulugan', 'cards.reviewAgain':'Repasohon usab', 'cards.gotIt':'Nakuha nako!', 'cards.deckComplete':'Human na ang deck!', 'cards.perfect':'Perpekto! Nahibalo ka sa tanan!', 'cards.great':'Maayo kaayo!', 'cards.keepGoing':'Padayon sa pagpraktis!', 'cards.mastered':'{k} / {total} ka kard ang namastero.', 'cards.markedReview':'{n} ang gimarkahan para repaso.', 'cards.restart':'Sugdan pag-usab', 'cards.reviewMarked':'Repasohon ang gimarkahan', 'cards.errGen':'Dili makahimo og kard karon. Sulayi pag-usab o mas simpleng topic.' },
    'Iban':             { 'ui.enterTopic':'Tolong tama topik!', 'quiz.title':'Pencabar Quiz!', 'quiz.subtitle':'Uji penemu nuan lalu bulih sijil', 'quiz.namePh':'Nama nuan…', 'quiz.topicPh':'Tama topik (chunto: pusar ai, pecahan…)', 'quiz.generate':'Ngaga Quiz', 'quiz.submit':'Kirum Saut', 'quiz.newQuiz':'Quiz Baru', 'quiz.answered':'disaut', 'quiz.scoreGood':'Manah amat! Terus!', 'quiz.scoreTry':'Manah! Terus belajar!', 'quiz.errGen':'Enda ulih ngaga quiz diatu. Cuba baru tauka topik ti mudah agi.', 'quiz.confirmSubmit':'Bisi tanya ti apin disaut. Kirum mega?', 'quiz.cert':'Unduh Sijil {t}', 'cards.title':'Dek Kad Belajar!', 'cards.subtitle':'Tekan kad kena malik lalu meda saut', 'cards.topicPh':'Topik (chunto: sel tumboh, sifir…)', 'cards.make':'Ngaga Kad', 'cards.reviewDue':'Patut diulang', 'cards.shuffle':'Kocok', 'cards.known':'nemu', 'cards.review':'ulang', 'cards.concept':'Konsep', 'cards.reveal':'Tekan kena meda!', 'cards.definition':'Reti', 'cards.reviewAgain':'Ulang baru', 'cards.gotIt':'Nemu udah!', 'cards.deckComplete':'Dek udah tembu!', 'cards.perfect':'Sempurna! Nuan nemu semua!', 'cards.great':'Kereja ti manah!', 'cards.keepGoing':'Terus belajar!', 'cards.mastered':'{k} / {total} kad udah dikuasai.', 'cards.markedReview':'{n} ditanda kena diulang.', 'cards.restart':'Berengkah baru', 'cards.reviewMarked':'Ulang ti ditanda', 'cards.errGen':'Enda ulih ngaga kad diatu. Cuba baru tauka topik ti mudah agi.' },
  };
  Object.keys(QC_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], QC_I18N[l]);
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
