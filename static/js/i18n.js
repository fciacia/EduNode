/* i18n.js — Edge UI translations for 11 ASEAN languages */
(function () {
  'use strict';

  const TRANSLATIONS = {
    'English': {
      'nav.quiz':              'Quiz',
      'nav.cards':             'Cards',
      'nav.podcast':           'Podcast',
      'nav.progress':          'Progress',
      'home.subtitle':         'Your offline AI learning buddy! ✨',
      'home.guide.title':      'Hey there, learner!',
      'home.guide.body':       'Pick a subject below to start chatting with your AI tutor. You can ask questions, take quizzes, study with flashcards, or even listen to a fun podcast!',
      'home.lang.label':       'Language:',
      'home.subjects.label':   'Choose a subject to get started',
      'home.activities.label': 'Other activities',
      'home.quiz':             'Take a Quiz',
      'home.flashcard':        'Flashcards',
      'home.podcast':          'Podcast',
      'home.progress':         'My Progress',
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
      'nav.quiz':              'Quiz',
      'nav.cards':             'Mga Kard',
      'nav.podcast':           'Podcast',
      'nav.progress':          'Progreso',
      'home.subtitle':         'Ang iyong offline AI na kasama sa pag-aaral! ✨',
      'home.guide.title':      'Huy, mag-aaral! 👋',
      'home.guide.body':       'Pumili ng paksa sa ibaba para magsimulang makipag-chat sa iyong AI tutor. Maaari kang magtanong, sumagot sa quiz, mag-aral gamit ang flashcards, o makinig ng masayang podcast!',
      'home.lang.label':       'Wika:',
      'home.subjects.label':   'Pumili ng paksa para magsimula',
      'home.activities.label': 'Iba pang gawain',
      'home.quiz':             'Sumagot ng Quiz',
      'home.flashcard':        'Flashcards',
      'home.podcast':          'Podcast',
      'home.progress':         'Aking Progreso',
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
      'nav.quiz':              'Kuiz',
      'nav.cards':             'Kad',
      'nav.podcast':           'Podcast',
      'nav.progress':          'Kemajuan',
      'home.subtitle':         'Kawan belajar AI offline kamu! ✨',
      'home.guide.title':      'Hai, pelajar! 👋',
      'home.guide.body':       'Pilih mata pelajaran di bawah untuk mula berbual dengan tutor AI kamu. Boleh tanya soalan, ambil kuiz, belajar dengan kad imbas, atau dengar podcast yang seronok, lah!',
      'home.lang.label':       'Bahasa:',
      'home.subjects.label':   'Pilih mata pelajaran untuk mula',
      'home.activities.label': 'Aktiviti lain',
      'home.quiz':             'Ambil Kuiz',
      'home.flashcard':        'Kad Imbas',
      'home.podcast':          'Podcast',
      'home.progress':         'Kemajuan Saya',
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
      'nav.quiz':              'Kuis',
      'nav.cards':             'Kartu',
      'nav.podcast':           'Podcast',
      'nav.progress':          'Kemajuan',
      'home.subtitle':         'Teman belajar AI offline kamu! ✨',
      'home.guide.title':      'Hei, pelajar! 👋',
      'home.guide.body':       'Pilih mata pelajaran di bawah untuk mulai ngobrol dengan tutor AI kamu. Kamu bisa tanya pertanyaan, ambil kuis, belajar pakai kartu, atau dengarkan podcast yang seru!',
      'home.lang.label':       'Bahasa:',
      'home.subjects.label':   'Pilih mata pelajaran untuk mulai',
      'home.activities.label': 'Aktivitas lain',
      'home.quiz':             'Ambil Kuis',
      'home.flashcard':        'Kartu Belajar',
      'home.podcast':          'Podcast',
      'home.progress':         'Kemajuan Saya',
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
      'nav.quiz':              'แบบทดสอบ',
      'nav.cards':             'บัตรคำ',
      'nav.podcast':           'พอดแคสต์',
      'nav.progress':          'ความก้าวหน้า',
      'home.subtitle':         'เพื่อนเรียน AI ออฟไลน์ของคุณ! ✨',
      'home.guide.title':      'สวัสดี นักเรียน! 👋',
      'home.guide.body':       'เลือกวิชาด้านล่างเพื่อเริ่มต้นคุยกับครู AI ของคุณ! สามารถถามคำถาม ทำแบบทดสอบ เรียนด้วยบัตรคำ หรือฟัง podcast ได้เลย!',
      'home.lang.label':       'ภาษา:',
      'home.subjects.label':   'เลือกวิชาเพื่อเริ่มต้น',
      'home.activities.label': 'กิจกรรมอื่นๆ',
      'home.quiz':             'ทำแบบทดสอบ',
      'home.flashcard':        'บัตรคำ',
      'home.podcast':          'พอดแคสต์',
      'home.progress':         'ความก้าวหน้าของฉัน',
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
      'nav.quiz':              'Kiểm Tra',
      'nav.cards':             'Thẻ Học',
      'nav.podcast':           'Podcast',
      'nav.progress':          'Tiến Độ',
      'home.subtitle':         'Bạn học AI ngoại tuyến của bạn! ✨',
      'home.guide.title':      'Xin chào, học sinh! 👋',
      'home.guide.body':       'Chọn môn học bên dưới để bắt đầu trò chuyện với gia sư AI. Bạn có thể đặt câu hỏi, làm bài kiểm tra, học thẻ, hoặc nghe podcast vui nhộn!',
      'home.lang.label':       'Ngôn ngữ:',
      'home.subjects.label':   'Chọn môn học để bắt đầu',
      'home.activities.label': 'Hoạt động khác',
      'home.quiz':             'Làm Bài Kiểm Tra',
      'home.flashcard':        'Thẻ Học',
      'home.podcast':          'Podcast',
      'home.progress':         'Tiến Độ Của Tôi',
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
      'nav.quiz':              'តេស្ត',
      'nav.cards':             'កាត',
      'nav.podcast':           'ផតខាស',
      'nav.progress':          'វឌ្ឍនភាព',
      'home.subtitle':         'មិត្តរៀន AI ក្រៅបណ្តាញរបស់អ្នក! ✨',
      'home.guide.title':      'សួស្តី! 👋',
      'home.guide.body':       'ជ្រើសរើសមុខវិជ្ជាខាងក្រោម ដើម្បីចាប់ផ្តើមជជែកជាមួយគ្រូ AI!',
      'home.lang.label':       'ភាសា:',
      'home.subjects.label':   'ជ្រើសរើសមុខវិជ្ជា',
      'home.activities.label': 'សកម្មភាពផ្សេង',
      'home.quiz':             'ធ្វើតេស្ត',
      'home.flashcard':        'កាតសិក្សា',
      'home.podcast':          'ផតខាស',
      'home.progress':         'វឌ្ឍនភាពខ្ញុំ',
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
      'nav.quiz':              'ທົດສອບ',
      'nav.cards':             'ໄພ້ຮຽນ',
      'nav.podcast':           'ພອດຄາສ',
      'nav.progress':          'ຄວາມຄືບໜ້າ',
      'home.subtitle':         'ໝູ່ຮຽນ AI ອອບໄລນ໌ຂອງທ່ານ! ✨',
      'home.guide.title':      'ສະບາຍດີ ນັກຮຽນ! 👋',
      'home.guide.body':       'ເລືອກວິຊາຂ້າງລຸ່ມ ເພື່ອເລີ່ມຄຸຍກັບຄູ AI ຂອງທ່ານ!',
      'home.lang.label':       'ພາສາ:',
      'home.subjects.label':   'ເລືອກວິຊາເພື່ອເລີ່ມ',
      'home.activities.label': 'ກິດຈະກໍາອື່ນ',
      'home.quiz':             'ເຮັດຂໍ້ສອບ',
      'home.flashcard':        'ໄພ້ຮຽນ',
      'home.podcast':          'ພອດຄາສ',
      'home.progress':         'ຄວາມຄືບໜ້າຂອງຂ້ອຍ',
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
      'nav.quiz':              'Quiz',
      'nav.cards':             'ကတ်',
      'nav.podcast':           'Podcast',
      'nav.progress':          'တိုးတက်မှု',
      'home.subtitle':         'သင်၏ AI သင်ကြားမှုဖော်ရှိ! ✨',
      'home.guide.title':      'မင်္ဂလာပါ ကျောင်းသား! 👋',
      'home.guide.body':       'အောက်ပါဘာသာရပ်တစ်ခုကို ရွေးချယ်ပြီး AI ဆရာနှင့် ပြောဆိုပါ!',
      'home.lang.label':       'ဘာသာ:',
      'home.subjects.label':   'ဘာသာရပ်ရွေးချယ်ပါ',
      'home.activities.label': 'အခြားလှုပ်ရှားမှုများ',
      'home.quiz':             'စစ်ဆေးမှုလုပ်ပါ',
      'home.flashcard':        'ဖလက်ရှ်ကတ်',
      'home.podcast':          'Podcast',
      'home.progress':         'ကျွန်ုပ်တိုးတက်မှု',
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
      'nav.quiz':              'Quiz',
      'nav.cards':             'Mga Kard',
      'nav.podcast':           'Podcast',
      'nav.progress':          'Progreso',
      'home.subtitle':         'Ang imong AI kauban sa pagkat-on nga offline! ✨',
      'home.guide.title':      'Kumusta, estudyante! 👋',
      'home.guide.body':       'Pagpili og sumod para magsugod og chat sa imong AI tutor. Makahimo kag pangutana, mosulay og quiz, magtuon gamit ang flashcards, o mamati og podcast!',
      'home.lang.label':       'Lengguwahe:',
      'home.subjects.label':   'Pagpili og sumod para magsugod',
      'home.activities.label': 'Ubang mga Kalihokan',
      'home.quiz':             'Kumuha og Quiz',
      'home.flashcard':        'Flashcards',
      'home.podcast':          'Podcast',
      'home.progress':         'Akong Progreso',
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
      'nav.quiz':              'Quiz',
      'nav.cards':             'Kad Belajar',
      'nav.podcast':           'Podcast',
      'nav.progress':          'Maju',
      'home.subtitle':         'Kaban belajar AI offline nuan! ✨',
      'home.guide.title':      'Selamat datai, pelajar! 👋',
      'home.guide.body':       'Pilih subjek di baruh tu untuk mula bercakap dengan tutor AI nuan!',
      'home.lang.label':       'Basa:',
      'home.subjects.label':   'Pilih subjek untuk mula',
      'home.activities.label': 'Aktiviti bukai',
      'home.quiz':             'Ambik Quiz',
      'home.flashcard':        'Kad Belajar',
      'home.podcast':          'Podcast',
      'home.progress':         'Maju Aku',
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
    'English':          { 'nav.slides':'Slides', 'slides.title':'Lesson Slides!', 'slides.subtitle':'Turn any topic into a slide deck you can present and narrate — offline', 'slides.topicPh':'Topic (e.g. the water cycle, fractions…)', 'slides.make':'Make Slides', 'slides.making':'Generating…', 'slides.try':'Try', 'slides.narrate':'Narrate', 'slides.stop':'Stop', 'slides.playAll':'Play all', 'slides.present':'Present', 'slides.download':'Download', 'slides.preparing':'Preparing…', 'slides.prev':'Prev', 'slides.next':'Next', 'slides.exit':'Exit', 'slides.fromBook':'From your textbook', 'slides.retry':'Retry', 'slides.errOffline':'The AI tutor is starting up. Please wait a moment and try again.', 'slides.errGen':'Could not make slides for that just now. Try again or a simpler topic.' },
    'Filipino':         { 'nav.slides':'Mga Slide', 'slides.title':'Mga Slide ng Aralin!', 'slides.subtitle':'Gawing slide deck ang anumang paksa na maipapakita at maikukuwento mo — offline', 'slides.topicPh':'Paksa (hal. ang water cycle, mga fraction…)', 'slides.make':'Gumawa ng Slide', 'slides.making':'Ginagawa…', 'slides.try':'Subukan', 'slides.narrate':'Basahin', 'slides.stop':'Itigil', 'slides.playAll':'I-play lahat', 'slides.present':'Ipakita', 'slides.download':'I-download', 'slides.preparing':'Inihahanda…', 'slides.prev':'Nakaraan', 'slides.next':'Susunod', 'slides.exit':'Lumabas', 'slides.fromBook':'Mula sa iyong aklat', 'slides.retry':'Subukang muli', 'slides.errOffline':'Nagsisimula pa ang AI tutor. Maghintay sandali at subukang muli.', 'slides.errGen':'Hindi makagawa ng slide ngayon. Subukang muli o mas simpleng paksa.' },
    'Bahasa Melayu':    { 'nav.slides':'Slaid', 'slides.title':'Slaid Pelajaran!', 'slides.subtitle':'Tukar mana-mana topik kepada slaid yang boleh kamu bentang dan ceritakan — luar talian', 'slides.topicPh':'Topik (cth. kitaran air, pecahan…)', 'slides.make':'Buat Slaid', 'slides.making':'Menjana…', 'slides.try':'Cuba', 'slides.narrate':'Cerita', 'slides.stop':'Berhenti', 'slides.playAll':'Main semua', 'slides.present':'Bentang', 'slides.download':'Muat turun', 'slides.preparing':'Menyediakan…', 'slides.prev':'Sebelum', 'slides.next':'Seterusnya', 'slides.exit':'Keluar', 'slides.fromBook':'Daripada buku teks kamu', 'slides.retry':'Cuba lagi', 'slides.errOffline':'Tutor AI sedang dimulakan. Sila tunggu sebentar dan cuba lagi.', 'slides.errGen':'Tidak dapat membuat slaid sekarang. Cuba lagi atau topik lebih mudah.' },
    'Bahasa Indonesia': { 'nav.slides':'Slide', 'slides.title':'Slide Pelajaran!', 'slides.subtitle':'Ubah topik apa pun menjadi slide yang bisa kamu presentasikan dan ceritakan — offline', 'slides.topicPh':'Topik (mis. siklus air, pecahan…)', 'slides.make':'Buat Slide', 'slides.making':'Membuat…', 'slides.try':'Coba', 'slides.narrate':'Bacakan', 'slides.stop':'Berhenti', 'slides.playAll':'Putar semua', 'slides.present':'Presentasi', 'slides.download':'Unduh', 'slides.preparing':'Menyiapkan…', 'slides.prev':'Sebelumnya', 'slides.next':'Berikutnya', 'slides.exit':'Keluar', 'slides.fromBook':'Dari buku pelajaranmu', 'slides.retry':'Coba lagi', 'slides.errOffline':'Tutor AI sedang dimulai. Tunggu sebentar lalu coba lagi.', 'slides.errGen':'Tidak bisa membuat slide saat ini. Coba lagi atau topik lebih sederhana.' },
    'Thai':             { 'nav.slides':'สไลด์', 'slides.title':'สไลด์บทเรียน!', 'slides.subtitle':'เปลี่ยนหัวข้อใดก็ได้ให้เป็นสไลด์ที่นำเสนอและบรรยายได้ — ออฟไลน์', 'slides.topicPh':'หัวข้อ (เช่น วัฏจักรน้ำ เศษส่วน…)', 'slides.make':'สร้างสไลด์', 'slides.making':'กำลังสร้าง…', 'slides.try':'ลองดู', 'slides.narrate':'บรรยาย', 'slides.stop':'หยุด', 'slides.playAll':'เล่นทั้งหมด', 'slides.present':'นำเสนอ', 'slides.download':'ดาวน์โหลด', 'slides.preparing':'กำลังเตรียม…', 'slides.prev':'ก่อนหน้า', 'slides.next':'ถัดไป', 'slides.exit':'ออก', 'slides.fromBook':'จากหนังสือเรียนของคุณ', 'slides.retry':'ลองอีกครั้ง', 'slides.errOffline':'ครู AI กำลังเริ่มทำงาน กรุณารอสักครู่แล้วลองอีกครั้ง', 'slides.errGen':'สร้างสไลด์ไม่ได้ในตอนนี้ ลองอีกครั้งหรือใช้หัวข้อที่ง่ายกว่า' },
    'Vietnamese':       { 'nav.slides':'Trình chiếu', 'slides.title':'Trình chiếu bài học!', 'slides.subtitle':'Biến mọi chủ đề thành bộ slide bạn có thể trình bày và thuyết minh — ngoại tuyến', 'slides.topicPh':'Chủ đề (vd. vòng tuần hoàn nước, phân số…)', 'slides.make':'Tạo Slide', 'slides.making':'Đang tạo…', 'slides.try':'Thử', 'slides.narrate':'Đọc', 'slides.stop':'Dừng', 'slides.playAll':'Phát tất cả', 'slides.present':'Trình bày', 'slides.download':'Tải về', 'slides.preparing':'Đang chuẩn bị…', 'slides.prev':'Trước', 'slides.next':'Tiếp', 'slides.exit':'Thoát', 'slides.fromBook':'Từ sách giáo khoa của bạn', 'slides.retry':'Thử lại', 'slides.errOffline':'Gia sư AI đang khởi động. Vui lòng đợi một lát rồi thử lại.', 'slides.errGen':'Hiện chưa tạo được slide. Hãy thử lại hoặc chọn chủ đề đơn giản hơn.' },
    'Khmer':            { 'nav.slides':'ស្លាយ', 'slides.title':'ស្លាយមេរៀន!', 'slides.subtitle':'ប្រែប្រួលប្រធានបទណាមួយទៅជាស្លាយ ដែលអ្នកអាចបង្ហាញ និងនិយាយបាន — ក្រៅបណ្តាញ', 'slides.topicPh':'ប្រធានបទ (ឧ. វដ្តទឹក ប្រភាគ…)', 'slides.make':'បង្កើតស្លាយ', 'slides.making':'កំពុងបង្កើត…', 'slides.try':'សាកល្បង', 'slides.narrate':'អាន', 'slides.stop':'ឈប់', 'slides.playAll':'ចាក់ទាំងអស់', 'slides.present':'បង្ហាញ', 'slides.download':'ទាញយក', 'slides.preparing':'កំពុងរៀបចំ…', 'slides.prev':'មុន', 'slides.next':'បន្ទាប់', 'slides.exit':'ចេញ', 'slides.fromBook':'ពីសៀវភៅសិក្សារបស់អ្នក', 'slides.retry':'ព្យាយាមម្តងទៀត', 'slides.errOffline':'គ្រូ AI កំពុងចាប់ផ្តើម។ សូមរង់ចាំបន្តិច ហើយព្យាយាមម្តងទៀត។', 'slides.errGen':'មិនអាចបង្កើតស្លាយឥឡូវនេះទេ។ ព្យាយាមម្តងទៀត ឬប្រធានបទសាមញ្ញជាង។' },
    'Lao':              { 'nav.slides':'ສະໄລດ໌', 'slides.title':'ສະໄລດ໌ບົດຮຽນ!', 'slides.subtitle':'ປ່ຽນຫົວຂໍ້ໃດກໍ່ໄດ້ໃຫ້ເປັນສະໄລດ໌ ທີ່ທ່ານສາມາດນຳສະເໜີ ແລະ ບັນລະຍາຍ — ອອບໄລນ໌', 'slides.topicPh':'ຫົວຂໍ້ (ຕົວຢ່າງ: ວົງຈອນນ້ຳ, ເສດສ່ວນ…)', 'slides.make':'ສ້າງສະໄລດ໌', 'slides.making':'ກຳລັງສ້າງ…', 'slides.try':'ລອງ', 'slides.narrate':'ບັນລະຍາຍ', 'slides.stop':'ຢຸດ', 'slides.playAll':'ຫຼິ້ນທັງໝົດ', 'slides.present':'ນຳສະເໜີ', 'slides.download':'ດາວໂຫຼດ', 'slides.preparing':'ກຳລັງກຽມ…', 'slides.prev':'ກ່ອນ', 'slides.next':'ຕໍ່ໄປ', 'slides.exit':'ອອກ', 'slides.fromBook':'ຈາກປຶ້ມຮຽນຂອງທ່ານ', 'slides.retry':'ລອງໃໝ່', 'slides.errOffline':'ຄູ AI ກຳລັງເລີ່ມຕົ້ນ. ກະລຸນາລໍຖ້າ ແລະ ລອງໃໝ່.', 'slides.errGen':'ສ້າງສະໄລດ໌ບໍ່ໄດ້ຕອນນີ້. ລອງໃໝ່ ຫຼື ຫົວຂໍ້ງ່າຍກວ່າ.' },
    'Burmese':          { 'nav.slides':'ဆလိုက်', 'slides.title':'သင်ခန်းစာ ဆလိုက်များ!', 'slides.subtitle':'မည်သည့်ခေါင်းစဉ်ကိုမဆို တင်ပြ၍ ရွတ်ဆိုနိုင်သော ဆလိုက်အဖြစ် ပြောင်းပါ — အော့ဖ်လိုင်း', 'slides.topicPh':'ခေါင်းစဉ် (ဥပမာ - ရေသံသရာ၊ အပိုင်းကိန်း…)', 'slides.make':'ဆလိုက်ပြုလုပ်ပါ', 'slides.making':'ပြုလုပ်နေသည်…', 'slides.try':'စမ်းကြည့်ပါ', 'slides.narrate':'ဖတ်ပြ', 'slides.stop':'ရပ်', 'slides.playAll':'အားလုံးဖွင့်', 'slides.present':'တင်ပြ', 'slides.download':'ဒေါင်းလုဒ်', 'slides.preparing':'ပြင်ဆင်နေသည်…', 'slides.prev':'ယခင်', 'slides.next':'နောက်', 'slides.exit':'ထွက်', 'slides.fromBook':'သင့်ကျောင်းစာအုပ်မှ', 'slides.retry':'ထပ်စမ်းပါ', 'slides.errOffline':'AI ဆရာ စတင်နေသည်။ ခဏစောင့်ပြီး ထပ်စမ်းပါ။', 'slides.errGen':'ယခု ဆလိုက်မပြုလုပ်နိုင်ပါ။ ထပ်စမ်းပါ သို့မဟုတ် ပိုရိုးသောခေါင်းစဉ်သုံးပါ။' },
    'Cebuano':          { 'nav.slides':'Mga Slide', 'slides.title':'Mga Slide sa Leksyon!', 'slides.subtitle':'Himoa nga slide deck ang bisan unsang topic nga imong mapakita ug maasoy — offline', 'slides.topicPh':'Topic (pananglitan, ang water cycle, mga fraction…)', 'slides.make':'Paghimo og Slide', 'slides.making':'Gihimo…', 'slides.try':'Sulayi', 'slides.narrate':'Basaha', 'slides.stop':'Hunong', 'slides.playAll':'I-play tanan', 'slides.present':'Ipakita', 'slides.download':'I-download', 'slides.preparing':'Giandam…', 'slides.prev':'Miagi', 'slides.next':'Sunod', 'slides.exit':'Gawas', 'slides.fromBook':'Gikan sa imong libro', 'slides.retry':'Sulayi pag-usab', 'slides.errOffline':'Nagsugod pa ang AI tutor. Paghulat kadiyot ug sulayi pag-usab.', 'slides.errGen':'Dili makahimo og slide karon. Sulayi pag-usab o mas simpleng topic.' },
    'Iban':             { 'nav.slides':'Slaid', 'slides.title':'Slaid Pelajar!', 'slides.subtitle':'Tukar sebarang topik nyadi slaid ti ulih dipandang sereta dicerita — offline', 'slides.topicPh':'Topik (chunto: pusar ai, pecahan…)', 'slides.make':'Ngaga Slaid', 'slides.making':'Benung ngaga…', 'slides.try':'Cuba', 'slides.narrate':'Cerita', 'slides.stop':'Badu', 'slides.playAll':'Main semua', 'slides.present':'Pandang', 'slides.download':'Unduh', 'slides.preparing':'Benung nyendia…', 'slides.prev':'Sebelum', 'slides.next':'Lalu', 'slides.exit':'Pansut', 'slides.fromBook':'Ari buku nuan', 'slides.retry':'Cuba baru', 'slides.errOffline':'Tutor AI benung berengkah. Nganti sekejap lalu cuba baru.', 'slides.errGen':'Enda ulih ngaga slaid diatu. Cuba baru tauka topik ti mudah agi.' },
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

  // "Report a wrong translation" — dialect flywheel safety net.
  const REPORT_I18N = {
    'English':          { 'report.tip':'Report a wrong translation', 'report.prompt':'What looks wrong? (optional)', 'report.thanks':'Thanks! A teacher will review it.' },
    'Filipino':         { 'report.tip':'I-report ang maling pagsasalin', 'report.prompt':'Ano ang mali? (opsyonal)', 'report.thanks':'Salamat! Ire-review ito ng guro.' },
    'Bahasa Melayu':    { 'report.tip':'Laporkan terjemahan salah', 'report.prompt':'Apa yang salah? (pilihan)', 'report.thanks':'Terima kasih! Guru akan menyemaknya.' },
    'Bahasa Indonesia': { 'report.tip':'Laporkan terjemahan salah', 'report.prompt':'Apa yang salah? (opsional)', 'report.thanks':'Terima kasih! Guru akan meninjaunya.' },
    'Thai':             { 'report.tip':'รายงานคำแปลที่ผิด', 'report.prompt':'อะไรผิด? (ไม่บังคับ)', 'report.thanks':'ขอบคุณ! ครูจะตรวจสอบ' },
    'Vietnamese':       { 'report.tip':'Báo dịch sai', 'report.prompt':'Có gì sai? (tùy chọn)', 'report.thanks':'Cảm ơn! Giáo viên sẽ xem lại.' },
    'Khmer':            { 'report.tip':'រាយការណ៍ការបកប្រែខុស', 'report.prompt':'មានអ្វីខុស? (ស្រេចចិត្ត)', 'report.thanks':'អរគុណ! គ្រូនឹងពិនិត្យ។' },
    'Lao':              { 'report.tip':'ລາຍງານການແປຜິດ', 'report.prompt':'ມີຫຍັງຜິດ? (ບໍ່ບັງຄັບ)', 'report.thanks':'ຂອບໃຈ! ຄູຈະກວດສອບ.' },
    'Burmese':          { 'report.tip':'မှားသော ဘာသာပြန်ကို တိုင်ကြားပါ', 'report.prompt':'ဘာမှားသလဲ? (ရွေးချယ်)', 'report.thanks':'ကျေးဇူးတင်ပါတယ်! ဆရာ စစ်ဆေးပါမည်။' },
    'Cebuano':          { 'report.tip':'I-report ang sayop nga hubad', 'report.prompt':'Unsa ang sayop? (opsyonal)', 'report.thanks':'Salamat! Repasohon kini sa magtutudlo.' },
    'Iban':             { 'report.tip':'Lapur jaku ti salah', 'report.prompt':'Nama ti salah? (pilih)', 'report.thanks':'Terima kasih! Pengajar deka mansik.' },
  };
  Object.keys(REPORT_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], REPORT_I18N[l]);
  });

  // Podcast-page strings, merged into the per-language tables above.
  const PODCAST_I18N = {
    'English':          { 'podcast.title':'Edge Podcast!', 'podcast.subtitle':'Maya & Niko explain topics in a fun way', 'podcast.topicPh':'Enter a topic (e.g. photosynthesis, fractions…)', 'podcast.generate':'Generate Episode', 'podcast.maya':'Maya — Curious Student', 'podcast.niko':'Niko — Friendly Teacher', 'podcast.script':'Episode Script' },
    'Filipino':         { 'podcast.title':'Edge Podcast!', 'podcast.subtitle':'Ipinapaliwanag nina Maya at Niko ang mga paksa sa masayang paraan', 'podcast.topicPh':'Maglagay ng paksa (hal. photosynthesis, mga fraction…)', 'podcast.generate':'Gumawa ng Episode', 'podcast.maya':'Maya — Mausisang Estudyante', 'podcast.niko':'Niko — Mabait na Guro', 'podcast.script':'Iskrip ng Episode' },
    'Bahasa Melayu':    { 'podcast.title':'Podcast Edge!', 'podcast.subtitle':'Maya & Niko menerangkan topik dengan cara yang menyeronokkan', 'podcast.topicPh':'Masukkan topik (cth. fotosintesis, pecahan…)', 'podcast.generate':'Jana Episod', 'podcast.maya':'Maya — Pelajar Ingin Tahu', 'podcast.niko':'Niko — Guru Mesra', 'podcast.script':'Skrip Episod' },
    'Bahasa Indonesia': { 'podcast.title':'Podcast Edge!', 'podcast.subtitle':'Maya & Niko menjelaskan topik dengan cara yang seru', 'podcast.topicPh':'Masukkan topik (mis. fotosintesis, pecahan…)', 'podcast.generate':'Buat Episode', 'podcast.maya':'Maya — Murid yang Ingin Tahu', 'podcast.niko':'Niko — Guru yang Ramah', 'podcast.script':'Skrip Episode' },
    'Thai':             { 'podcast.title':'Edge พอดแคสต์!', 'podcast.subtitle':'มายากับนิโกะอธิบายหัวข้อต่างๆ อย่างสนุกสนาน', 'podcast.topicPh':'ใส่หัวข้อ (เช่น การสังเคราะห์แสง เศษส่วน…)', 'podcast.generate':'สร้างตอน', 'podcast.maya':'มายา — นักเรียนช่างสงสัย', 'podcast.niko':'นิโกะ — ครูใจดี', 'podcast.script':'สคริปต์ตอน' },
    'Vietnamese':       { 'podcast.title':'Podcast Edge!', 'podcast.subtitle':'Maya & Niko giải thích chủ đề theo cách thú vị', 'podcast.topicPh':'Nhập chủ đề (vd. quang hợp, phân số…)', 'podcast.generate':'Tạo Tập', 'podcast.maya':'Maya — Học sinh tò mò', 'podcast.niko':'Niko — Giáo viên thân thiện', 'podcast.script':'Kịch bản tập' },
    'Khmer':            { 'podcast.title':'Edge ផតខាស្ត!', 'podcast.subtitle':'Maya និង Nikoពន្យល់ប្រធានបទតាមរបៀបសប្បាយៗ', 'podcast.topicPh':'បញ្ចូលប្រធានបទ (ឧ. ការសំយោគពន្លឺ ប្រភាគ…)', 'podcast.generate':'បង្កើតវគ្គ', 'podcast.maya':'Maya — សិស្សចង់ដឹងចង់ឮ', 'podcast.niko':'Niko — គ្រូរួសរាយ', 'podcast.script':'អត្ថបទវគ្គ' },
    'Lao':              { 'podcast.title':'Edge ພອດແຄສ!', 'podcast.subtitle':'Maya ແລະ Niko ອະທິບາຍຫົວຂໍ້ຕ່າງໆແບບມ່ວນຊື່ນ', 'podcast.topicPh':'ໃສ່ຫົວຂໍ້ (ຕົວຢ່າງ: ການສັງເຄາະແສງ, ເສດສ່ວນ…)', 'podcast.generate':'ສ້າງຕອນ', 'podcast.maya':'Maya — ນັກຮຽນຢາກຮູ້ຢາກເຫັນ', 'podcast.niko':'Niko — ຄູທີ່ເປັນມິດ', 'podcast.script':'ບົດຂອງຕອນ' },
    'Burmese':          { 'podcast.title':'Edge ပေါ့ဒ်ကာစ်!', 'podcast.subtitle':'Maya နှင့် Niko က ခေါင်းစဉ်များကို ပျော်ရွှင်စွာ ရှင်းပြသည်', 'podcast.topicPh':'ခေါင်းစဉ်ထည့်ပါ (ဥပမာ - ပရိုတိုဆင်သက်စစ်၊ အပိုင်းကိန်း…)', 'podcast.generate':'အပိုင်း ဖန်တီးပါ', 'podcast.maya':'Maya — စူးစမ်းလိုစိတ်ရှိသော ကျောင်းသူ', 'podcast.niko':'Niko — ဖော်ရွေသော ဆရာ', 'podcast.script':'အပိုင်းစာသား' },
    'Cebuano':          { 'podcast.title':'Edge Podcast!', 'podcast.subtitle':'Gipatin-aw ni Maya ug Niko ang mga topic sa malingaw nga paagi', 'podcast.topicPh':'Pagbutang og topic (pananglitan, photosynthesis, mga fraction…)', 'podcast.generate':'Paghimo og Episode', 'podcast.maya':'Maya — Mausisa nga Estudyante', 'podcast.niko':'Niko — Mahigalaon nga Magtutudlo', 'podcast.script':'Script sa Episode' },
    'Iban':             { 'podcast.title':'Edge Podcast!', 'podcast.subtitle':'Maya & Niko nerangka topik ngena chara ti lantang', 'podcast.topicPh':'Tama topik (chunto: fotosintesis, pecahan…)', 'podcast.generate':'Ngaga Episod', 'podcast.maya':'Maya — Pelajar Deka Nemu', 'podcast.niko':'Niko — Pengajar Ti Ramah', 'podcast.script':'Skrip Episod' },
  };
  Object.keys(PODCAST_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], PODCAST_I18N[l]);
  });

  // Home-page subject-card description strings, merged into the per-language tables above.
  const SUBJECT_DESC_I18N = {
    'English':          { 'subject.desc.Mathematics':'Numbers, fractions, geometry and more', 'subject.desc.Science':'Explore how the world works', 'subject.desc.English Language':'Reading, writing and vocabulary', 'subject.desc.Environmental Studies':'Nature, climate and our planet', 'subject.desc.Digital Literacy':'Computers, internet and safety' },
    'Filipino':         { 'subject.desc.Mathematics':'Mga numero, fraction, geometry at iba pa', 'subject.desc.Science':'Alamin kung paano gumagana ang mundo', 'subject.desc.English Language':'Pagbasa, pagsulat at bokabularyo', 'subject.desc.Environmental Studies':'Kalikasan, klima at ating planeta', 'subject.desc.Digital Literacy':'Computer, internet at kaligtasan' },
    'Bahasa Melayu':    { 'subject.desc.Mathematics':'Nombor, pecahan, geometri dan banyak lagi', 'subject.desc.Science':'Terokai cara dunia berfungsi', 'subject.desc.English Language':'Membaca, menulis dan perbendaharaan kata', 'subject.desc.Environmental Studies':'Alam semula jadi, iklim dan planet kita', 'subject.desc.Digital Literacy':'Komputer, internet dan keselamatan' },
    'Bahasa Indonesia': { 'subject.desc.Mathematics':'Angka, pecahan, geometri dan lainnya', 'subject.desc.Science':'Jelajahi cara kerja dunia', 'subject.desc.English Language':'Membaca, menulis dan kosakata', 'subject.desc.Environmental Studies':'Alam, iklim dan planet kita', 'subject.desc.Digital Literacy':'Komputer, internet dan keamanan' },
    'Thai':             { 'subject.desc.Mathematics':'ตัวเลข เศษส่วน เรขาคณิต และอื่นๆ', 'subject.desc.Science':'สำรวจว่าโลกทำงานอย่างไร', 'subject.desc.English Language':'การอ่าน การเขียน และคำศัพท์', 'subject.desc.Environmental Studies':'ธรรมชาติ สภาพภูมิอากาศ และโลกของเรา', 'subject.desc.Digital Literacy':'คอมพิวเตอร์ อินเทอร์เน็ต และความปลอดภัย' },
    'Vietnamese':       { 'subject.desc.Mathematics':'Số học, phân số, hình học và nhiều hơn', 'subject.desc.Science':'Khám phá cách thế giới vận hành', 'subject.desc.English Language':'Đọc, viết và từ vựng', 'subject.desc.Environmental Studies':'Thiên nhiên, khí hậu và hành tinh của chúng ta', 'subject.desc.Digital Literacy':'Máy tính, internet và an toàn' },
    'Khmer':            { 'subject.desc.Mathematics':'លេខ ប្រភាគ ធរណីមាត្រ និងច្រើនទៀត', 'subject.desc.Science':'ស្វែងយល់ពីរបៀបដែលពិភពលោកដំណើរការ', 'subject.desc.English Language':'ការអាន ការសរសេរ និងវាក្យសព្ទ', 'subject.desc.Environmental Studies':'ធម្មជាតិ អាកាសធាតុ និងភពផែនដីរបស់យើង', 'subject.desc.Digital Literacy':'កុំព្យូទ័រ អ៊ីនធឺណិត និងសុវត្ថិភាព' },
    'Lao':              { 'subject.desc.Mathematics':'ຕົວເລກ, ເສດສ່ວນ, ເລຂາຄະນິດ ແລະ ອື່ນໆ', 'subject.desc.Science':'ສຳຫຼວດວິທີການເຮັດວຽກຂອງໂລກ', 'subject.desc.English Language':'ການອ່ານ, ການຂຽນ ແລະ ຄຳສັບ', 'subject.desc.Environmental Studies':'ທຳມະຊາດ, ດິນຟ້າອາກາດ ແລະ ໂລກຂອງພວກເຮົາ', 'subject.desc.Digital Literacy':'ຄອມພິວເຕີ, ອິນເຕີເນັດ ແລະ ຄວາມປອດໄພ' },
    'Burmese':          { 'subject.desc.Mathematics':'ဂဏန်း၊ အပိုင်းကိန်း၊ ဂျီဩမေတြီနှင့် အခြားများ', 'subject.desc.Science':'ကမ္ဘာကြီးအလုပ်လုပ်ပုံကို လေ့လာပါ', 'subject.desc.English Language':'ဖတ်ခြင်း၊ ရေးခြင်းနှင့် စကားလုံးများ', 'subject.desc.Environmental Studies':'သဘာဝ၊ ရာသီဥတုနှင့် ကျွန်ုပ်တို့၏ ဂြိုဟ်', 'subject.desc.Digital Literacy':'ကွန်ပျူတာ၊ အင်တာနက်နှင့် ဘေးကင်းလုံခြုံမှု' },
    'Cebuano':          { 'subject.desc.Mathematics':'Mga numero, fraction, geometry ug uban pa', 'subject.desc.Science':'Sukiton kung giunsa paglihok ang kalibutan', 'subject.desc.English Language':'Pagbasa, pagsulat ug bokabularyo', 'subject.desc.Environmental Studies':'Kinaiyahan, klima ug atong planeta', 'subject.desc.Digital Literacy':'Kompyuter, internet ug kaluwasan' },
    'Iban':             { 'subject.desc.Mathematics':'Nombor, pecahan, geometri enggau bukai', 'subject.desc.Science':'Kajii chara dunya bekereja', 'subject.desc.English Language':'Macha, nulis enggau leka jaku', 'subject.desc.Environmental Studies':'Alam, iklim enggau planet kitai', 'subject.desc.Digital Literacy':'Komputer, internet enggau pemantap' },
  };
  Object.keys(SUBJECT_DESC_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], SUBJECT_DESC_I18N[l]);
  });

  // Home-page hero card strings, merged into the per-language tables above.
  // {name}/{topic} are filled in by JS after translation.
  const HOME_HERO_I18N = {
    'English':          { 'home.eyebrow':'Edge Tutor', 'home.startLearning':'Start learning', 'home.askPh':'Ask me anything…', 'home.ask':'Ask', 'home.welcomeBack':'Welcome back, {name}!', 'home.lastStudied':'Last time you studied {topic}. Keep your streak going with another round.', 'home.continueLearning':'Continue learning', 'home.readyWhenYouAre':'Ready when you are, {name}!', 'home.startFirstQuiz':'Start your first quiz or chat session to begin building your progress.' },
    'Filipino':         { 'home.eyebrow':'Edge Tutor', 'home.startLearning':'Simulan ang pag-aaral', 'home.askPh':'Magtanong ka…', 'home.ask':'Tanong', 'home.welcomeBack':'Maligayang pagbabalik, {name}!', 'home.lastStudied':'Huling pinag-aralan mo ang {topic}. Ipagpatuloy ang iyong streak!', 'home.continueLearning':'Ipagpatuloy ang pag-aaral', 'home.readyWhenYouAre':'Handa ka na ba, {name}!', 'home.startFirstQuiz':'Simulan ang iyong unang quiz o chat session para makapagsimula.' },
    'Bahasa Melayu':    { 'home.eyebrow':'Edge Tutor', 'home.startLearning':'Mula belajar', 'home.askPh':'Tanya apa-apa sahaja…', 'home.ask':'Tanya', 'home.welcomeBack':'Selamat kembali, {name}!', 'home.lastStudied':'Kali terakhir kamu belajar {topic}. Teruskan streak kamu!', 'home.continueLearning':'Teruskan belajar', 'home.readyWhenYouAre':'Sedia bila-bila masa, {name}!', 'home.startFirstQuiz':'Mula kuiz atau sesi chat pertama kamu untuk membina kemajuan.' },
    'Bahasa Indonesia': { 'home.eyebrow':'Edge Tutor', 'home.startLearning':'Mulai belajar', 'home.askPh':'Tanyakan apa saja…', 'home.ask':'Tanya', 'home.welcomeBack':'Selamat datang kembali, {name}!', 'home.lastStudied':'Terakhir kamu belajar {topic}. Lanjutkan streak-mu!', 'home.continueLearning':'Lanjutkan belajar', 'home.readyWhenYouAre':'Siap kapan saja, {name}!', 'home.startFirstQuiz':'Mulai kuis atau sesi chat pertamamu untuk membangun progres.' },
    'Thai':             { 'home.eyebrow':'ครู AI Edge', 'home.startLearning':'เริ่มเรียน', 'home.askPh':'ถามอะไรก็ได้…', 'home.ask':'ถาม', 'home.welcomeBack':'ยินดีต้อนรับกลับมา {name}!', 'home.lastStudied':'ครั้งล่าสุดคุณเรียน {topic} ทำต่อเนื่องให้ครบสถิติของคุณ!', 'home.continueLearning':'เรียนต่อ', 'home.readyWhenYouAre':'พร้อมเมื่อไหร่ก็บอกได้ {name}!', 'home.startFirstQuiz':'เริ่มควิซหรือแชทครั้งแรกของคุณเพื่อสร้างความคืบหน้า' },
    'Vietnamese':       { 'home.eyebrow':'Gia sư Edge', 'home.startLearning':'Bắt đầu học', 'home.askPh':'Hỏi bất cứ điều gì…', 'home.ask':'Hỏi', 'home.welcomeBack':'Chào mừng trở lại, {name}!', 'home.lastStudied':'Lần trước bạn học {topic}. Hãy tiếp tục chuỗi học tập nhé!', 'home.continueLearning':'Tiếp tục học', 'home.readyWhenYouAre':'Sẵn sàng khi bạn muốn, {name}!', 'home.startFirstQuiz':'Bắt đầu bài kiểm tra hoặc trò chuyện đầu tiên để xây dựng tiến trình của bạn.' },
    'Khmer':            { 'home.eyebrow':'គ្រូ Edge', 'home.startLearning':'ចាប់ផ្តើមរៀន', 'home.askPh':'សួរអ្វីក៏បាន…', 'home.ask':'សួរ', 'home.welcomeBack':'សូមស្វាគមន៍ការត្រឡប់មកវិញ {name}!', 'home.lastStudied':'លើកចុងក្រោយអ្នករៀន {topic}។ បន្តភាពជាប់លាប់របស់អ្នក!', 'home.continueLearning':'បន្តរៀន', 'home.readyWhenYouAre':'នៅពេលអ្នកត្រៀមខ្លួន {name}!', 'home.startFirstQuiz':'ចាប់ផ្តើមសំណួរ ឬការជជែកដំបូងរបស់អ្នកដើម្បីកសាងវឌ្ឍនភាព។' },
    'Lao':              { 'home.eyebrow':'ຄູ Edge', 'home.startLearning':'ເລີ່ມຮຽນ', 'home.askPh':'ຖາມຫຍັງກໍໄດ້…', 'home.ask':'ຖາມ', 'home.welcomeBack':'ຍິນດີຕ້ອນຮັບກັບຄືນມາ {name}!', 'home.lastStudied':'ຄັ້ງລ່າສຸດທ່ານຮຽນ {topic}. ສືບຕໍ່ຄວາມຕໍ່ເນື່ອງຂອງທ່ານ!', 'home.continueLearning':'ຮຽນຕໍ່', 'home.readyWhenYouAre':'ພ້ອມເມື່ອທ່ານຢາກ, {name}!', 'home.startFirstQuiz':'ເລີ່ມຄຳຖາມ ຫຼື ການສົນທະນາເທື່ອທຳອິດຂອງທ່ານເພື່ອສ້າງຄວາມຄືບໜ້າ.' },
    'Burmese':          { 'home.eyebrow':'Edge ဆရာ', 'home.startLearning':'သင်ယူမှု စတင်ပါ', 'home.askPh':'ဘာမဆို မေးပါ…', 'home.ask':'မေးမည်', 'home.welcomeBack':'ပြန်လည်ကြိုဆိုပါတယ် {name}!', 'home.lastStudied':'နောက်ဆုံးအကြိမ် {topic} ကို လေ့လာခဲ့ပါတယ်။ ဆက်လက်လေ့ကျင့်ပါ!', 'home.continueLearning':'ဆက်လက်သင်ယူပါ', 'home.readyWhenYouAre':'အသင့်ဖြစ်တဲ့အခါ {name}!', 'home.startFirstQuiz':'တိုးတက်မှုတည်ဆောက်ရန် သင့်ပထမဆုံး Quiz သို့မဟုတ် chat session ကို စတင်ပါ။' },
    'Cebuano':          { 'home.eyebrow':'Edge Tutor', 'home.startLearning':'Sugdi pagkat-on', 'home.askPh':'Pangutana bisan unsa…', 'home.ask':'Pangutana', 'home.welcomeBack':'Maayong pagbalik, {name}!', 'home.lastStudied':'Katapusang gitun-an nimo ang {topic}. Padayona ang imong streak!', 'home.continueLearning':'Padayon sa pagkat-on', 'home.readyWhenYouAre':'Andam bisan kanus-a, {name}!', 'home.startFirstQuiz':'Sugdi ang imong unang quiz o chat session aron makasugod og progreso.' },
    'Iban':             { 'home.eyebrow':'Edge Tutor', 'home.startLearning':'Berengkah belajar', 'home.askPh':'Tanya nama utai…', 'home.ask':'Tanya', 'home.welcomeBack':'Selamat pulai baru, {name}!', 'home.lastStudied':'Kelia nuan belajar {topic}. Terus deka streak nuan!', 'home.continueLearning':'Terus belajar', 'home.readyWhenYouAre':'Sedia lebuh nuan mira, {name}!', 'home.startFirstQuiz':'Berengkah quiz tauka chat session ke keterubah kena ngaga penemu.' },
  };
  Object.keys(HOME_HERO_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], HOME_HERO_I18N[l]);
  });

  // Sidebar strings (Daily Challenge / Your Badges / This Week — shown on every page),
  // merged into the per-language tables above. {q}/{s}/{pct}/{n}/{goal} filled in by JS.
  const SIDEBAR_I18N = {
    'English':          { 'sidebar.dailyChallenge':'Daily Challenge', 'sidebar.takeQuiz':'Take a quiz', 'sidebar.sharpenSubject':'Sharpen a subject in a few minutes.', 'sidebar.startNow':'Start now →', 'sidebar.yourBadges':'Your Badges', 'sidebar.noBadges':'Enter your name on the Progress page to see your badges here.', 'sidebar.thisWeek':'This Week', 'sidebar.noActivity':'Your quiz and session activity will show up here once you start learning.', 'sidebar.viewAll':'View all →', 'sidebar.quizSessions':'{q} quizzes · {s} sessions', 'sidebar.bestScore':'Best score so far: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} recent quizzes' },
    'Filipino':         { 'sidebar.dailyChallenge':'Pang-araw-araw na Hamon', 'sidebar.takeQuiz':'Sumagot ng quiz', 'sidebar.sharpenSubject':'Paghusayin ang isang paksa sa ilang minuto.', 'sidebar.startNow':'Simulan na →', 'sidebar.yourBadges':'Iyong mga Badge', 'sidebar.noBadges':'Ilagay ang iyong pangalan sa Progress page para makita ang iyong mga badge dito.', 'sidebar.thisWeek':'Ngayong Linggo', 'sidebar.noActivity':'Lalabas dito ang iyong quiz at session activity kapag nagsimula ka nang mag-aral.', 'sidebar.viewAll':'Tingnan lahat →', 'sidebar.quizSessions':'{q} quiz · {s} session', 'sidebar.bestScore':'Pinakamataas na iskor: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} kamakailang quiz' },
    'Bahasa Melayu':    { 'sidebar.dailyChallenge':'Cabaran Harian', 'sidebar.takeQuiz':'Buat kuiz', 'sidebar.sharpenSubject':'Pertajam satu subjek dalam beberapa minit.', 'sidebar.startNow':'Mula sekarang →', 'sidebar.yourBadges':'Lencana Kamu', 'sidebar.noBadges':'Masukkan nama kamu di halaman Progress untuk lihat lencana kamu di sini.', 'sidebar.thisWeek':'Minggu Ini', 'sidebar.noActivity':'Aktiviti kuiz dan sesi kamu akan dipaparkan di sini setelah kamu mula belajar.', 'sidebar.viewAll':'Lihat semua →', 'sidebar.quizSessions':'{q} kuiz · {s} sesi', 'sidebar.bestScore':'Skor terbaik setakat ini: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} kuiz terkini' },
    'Bahasa Indonesia': { 'sidebar.dailyChallenge':'Tantangan Harian', 'sidebar.takeQuiz':'Ikuti kuis', 'sidebar.sharpenSubject':'Asah satu topik dalam beberapa menit.', 'sidebar.startNow':'Mulai sekarang →', 'sidebar.yourBadges':'Lencana Kamu', 'sidebar.noBadges':'Masukkan namamu di halaman Progress untuk melihat lencanamu di sini.', 'sidebar.thisWeek':'Minggu Ini', 'sidebar.noActivity':'Aktivitas kuis dan sesimu akan muncul di sini setelah kamu mulai belajar.', 'sidebar.viewAll':'Lihat semua →', 'sidebar.quizSessions':'{q} kuis · {s} sesi', 'sidebar.bestScore':'Skor terbaik sejauh ini: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} kuis terbaru' },
    'Thai':             { 'sidebar.dailyChallenge':'ภารกิจประจำวัน', 'sidebar.takeQuiz':'ทำแบบทดสอบ', 'sidebar.sharpenSubject':'ฝึกฝนวิชาในไม่กี่นาที', 'sidebar.startNow':'เริ่มเลย →', 'sidebar.yourBadges':'เหรียญตราของคุณ', 'sidebar.noBadges':'ใส่ชื่อของคุณในหน้าความก้าวหน้าเพื่อดูเหรียญตราที่นี่', 'sidebar.thisWeek':'สัปดาห์นี้', 'sidebar.noActivity':'กิจกรรมแบบทดสอบและเซสชันของคุณจะแสดงที่นี่เมื่อคุณเริ่มเรียน', 'sidebar.viewAll':'ดูทั้งหมด →', 'sidebar.quizSessions':'{q} แบบทดสอบ · {s} เซสชัน', 'sidebar.bestScore':'คะแนนดีที่สุดตอนนี้: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} แบบทดสอบล่าสุด' },
    'Vietnamese':       { 'sidebar.dailyChallenge':'Thử thách hằng ngày', 'sidebar.takeQuiz':'Làm bài kiểm tra', 'sidebar.sharpenSubject':'Rèn luyện một môn học trong vài phút.', 'sidebar.startNow':'Bắt đầu ngay →', 'sidebar.yourBadges':'Huy hiệu của bạn', 'sidebar.noBadges':'Nhập tên của bạn tại trang Tiến trình để xem huy hiệu ở đây.', 'sidebar.thisWeek':'Tuần này', 'sidebar.noActivity':'Hoạt động kiểm tra và phiên học của bạn sẽ hiện ở đây khi bạn bắt đầu học.', 'sidebar.viewAll':'Xem tất cả →', 'sidebar.quizSessions':'{q} bài kiểm tra · {s} phiên học', 'sidebar.bestScore':'Điểm cao nhất hiện tại: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} bài kiểm tra gần đây' },
    'Khmer':            { 'sidebar.dailyChallenge':'ការប្រកួតប្រចាំថ្ងៃ', 'sidebar.takeQuiz':'ធ្វើសំណួរ', 'sidebar.sharpenSubject':'អនុវត្តមុខវិជ្ជាមួយក្នុងរយៈពេលពីរបីនាទី។', 'sidebar.startNow':'ចាប់ផ្តើមឥឡូវ →', 'sidebar.yourBadges':'ស្លាកសញ្ញារបស់អ្នក', 'sidebar.noBadges':'បញ្ចូលឈ្មោះរបស់អ្នកនៅទំព័រវឌ្ឍនភាព ដើម្បីមើលស្លាកសញ្ញារបស់អ្នកនៅទីនេះ។', 'sidebar.thisWeek':'សប្តាហ៍នេះ', 'sidebar.noActivity':'សកម្មភាពសំណួរ និងវគ្គរបស់អ្នកនឹងបង្ហាញនៅទីនេះនៅពេលអ្នកចាប់ផ្តើមរៀន។', 'sidebar.viewAll':'មើលទាំងអស់ →', 'sidebar.quizSessions':'{q} សំណួរ · {s} វគ្គ', 'sidebar.bestScore':'ពិន្ទុល្អបំផុតគិតត្រឹមពេលនេះ: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} សំណួរថ្មីៗ' },
    'Lao':              { 'sidebar.dailyChallenge':'ສິ່ງທ້າທາຍປະຈຳວັນ', 'sidebar.takeQuiz':'ເຮັດແບບທົດສອບ', 'sidebar.sharpenSubject':'ຝຶກຝົນວິຊາໜຶ່ງພາຍໃນສອງສາມນາທີ.', 'sidebar.startNow':'ເລີ່ມດຽວນີ້ →', 'sidebar.yourBadges':'ຫຼຽນຂອງທ່ານ', 'sidebar.noBadges':'ໃສ່ຊື່ຂອງທ່ານໃນໜ້າຄວາມຄືບໜ້າ ເພື່ອເບິ່ງຫຼຽນຂອງທ່ານທີ່ນີ້.', 'sidebar.thisWeek':'ອາທິດນີ້', 'sidebar.noActivity':'ກິດຈະກຳແບບທົດສອບ ແລະ ເຊສຊັນຂອງທ່ານຈະສະແດງຢູ່ນີ້ເມື່ອທ່ານເລີ່ມຮຽນ.', 'sidebar.viewAll':'ເບິ່ງທັງໝົດ →', 'sidebar.quizSessions':'{q} ແບບທົດສອບ · {s} ເຊສຊັນ', 'sidebar.bestScore':'ຄະແນນດີທີ່ສຸດຕອນນີ້: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} ແບບທົດສອບຫຼ້າສຸດ' },
    'Burmese':          { 'sidebar.dailyChallenge':'နေ့စဉ်စိန်ခေါ်မှု', 'sidebar.takeQuiz':'Quiz လုပ်ပါ', 'sidebar.sharpenSubject':'မိနစ်အနည်းငယ်အတွင်း ဘာသာရပ်တစ်ခုကို ပိုမိုကျွမ်းကျင်အောင်လုပ်ပါ။', 'sidebar.startNow':'ယခုစတင်ပါ →', 'sidebar.yourBadges':'သင်၏ တံဆိပ်များ', 'sidebar.noBadges':'သင်၏တံဆိပ်များကို ဤနေရာတွင်ကြည့်ရန် Progress စာမျက်နှာတွင် သင့်နာမည်ကို ထည့်ပါ။', 'sidebar.thisWeek':'ဒီအပတ်', 'sidebar.noActivity':'သင် စတင်လေ့လာလိုက်သည်နှင့် Quiz နှင့် session လှုပ်ရှားမှုများ ဤနေရာတွင် ပေါ်လာပါမည်။', 'sidebar.viewAll':'အားလုံးကြည့်ရန် →', 'sidebar.quizSessions':'Quiz {q} ခု · Session {s} ခု', 'sidebar.bestScore':'အကောင်းဆုံးရမှတ်: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} လတ်တလော Quiz' },
    'Cebuano':          { 'sidebar.dailyChallenge':'Adlaw-adlaw nga Hagit', 'sidebar.takeQuiz':'Sulayi ang quiz', 'sidebar.sharpenSubject':'Pasamuta ang usa ka topic sulod sa pipila ka minuto.', 'sidebar.startNow':'Sugdi karon →', 'sidebar.yourBadges':'Imong mga Badge', 'sidebar.noBadges':'Ibutang ang imong ngalan sa Progress page aron makita ang imong mga badge dinhi.', 'sidebar.thisWeek':'Karong Semanaha', 'sidebar.noActivity':'Ang imong quiz ug session activity mopakita dinhi kung magsugod ka na sa pagkat-on.', 'sidebar.viewAll':'Tan-awa tanan →', 'sidebar.quizSessions':'{q} quiz · {s} session', 'sidebar.bestScore':'Labing maayong iskor karon: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} bag-ong quiz' },
    'Iban':             { 'sidebar.dailyChallenge':'Pencabar Beri Hari', 'sidebar.takeQuiz':'Ngaga quiz', 'sidebar.sharpenSubject':'Asah siti subjek dalam pemadu minit.', 'sidebar.startNow':'Berengkah diatu →', 'sidebar.yourBadges':'Lencana Nuan', 'sidebar.noBadges':'Tama nama nuan ba pengelama Progress kena meda lencana nuan ditu.', 'sidebar.thisWeek':'Minggu Tu', 'sidebar.noActivity':'Aktiviti quiz enggau session nuan deka pansut ditu lebuh nuan berengkah belajar.', 'sidebar.viewAll':'Meda semua →', 'sidebar.quizSessions':'{q} quiz · {s} session', 'sidebar.bestScore':'Score paling manah diatu: {pct}%', 'sidebar.recentQuizzes':'{n} / {goal} quiz baru' },
  };
  Object.keys(SIDEBAR_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], SIDEBAR_I18N[l]);
  });

  // Nav rail footer strings (Chat link + How to use / Settings / Dark mode / Light mode buttons),
  // merged into the per-language tables above.
  const NAV_FOOTER_I18N = {
    'English':          { 'nav.chat':'Chat', 'nav.howToUse':'How to use', 'nav.settings':'Settings', 'nav.darkMode':'Dark mode', 'nav.lightMode':'Light mode' },
    'Filipino':         { 'nav.chat':'Chat', 'nav.howToUse':'Paano gamitin', 'nav.settings':'Mga Setting', 'nav.darkMode':'Madilim na mode', 'nav.lightMode':'Maliwanag na mode' },
    'Bahasa Melayu':    { 'nav.chat':'Chat', 'nav.howToUse':'Cara guna', 'nav.settings':'Tetapan', 'nav.darkMode':'Mod gelap', 'nav.lightMode':'Mod cerah' },
    'Bahasa Indonesia': { 'nav.chat':'Chat', 'nav.howToUse':'Cara pakai', 'nav.settings':'Pengaturan', 'nav.darkMode':'Mode gelap', 'nav.lightMode':'Mode terang' },
    'Thai':             { 'nav.chat':'แชท', 'nav.howToUse':'วิธีใช้งาน', 'nav.settings':'การตั้งค่า', 'nav.darkMode':'โหมดมืด', 'nav.lightMode':'โหมดสว่าง' },
    'Vietnamese':       { 'nav.chat':'Trò chuyện', 'nav.howToUse':'Cách sử dụng', 'nav.settings':'Cài đặt', 'nav.darkMode':'Chế độ tối', 'nav.lightMode':'Chế độ sáng' },
    'Khmer':            { 'nav.chat':'ជជែក', 'nav.howToUse':'របៀបប្រើ', 'nav.settings':'ការកំណត់', 'nav.darkMode':'របៀបងងឹត', 'nav.lightMode':'របៀបភ្លឺ' },
    'Lao':              { 'nav.chat':'ສົນທະນາ', 'nav.howToUse':'ວິທີໃຊ້', 'nav.settings':'ການຕັ້ງຄ່າ', 'nav.darkMode':'ໂໝດມືດ', 'nav.lightMode':'ໂໝດແຈ້ງ' },
    'Burmese':          { 'nav.chat':'စကားပြော', 'nav.howToUse':'အသုံးပြုနည်း', 'nav.settings':'ဆက်တင်များ', 'nav.darkMode':'အမှောင်မုဒ်', 'nav.lightMode':'အလင်းမုဒ်' },
    'Cebuano':          { 'nav.chat':'Chat', 'nav.howToUse':'Giunsa paggamit', 'nav.settings':'Mga Setting', 'nav.darkMode':'Ngitngit nga mode', 'nav.lightMode':'Hayag nga mode' },
    'Iban':             { 'nav.chat':'Chat', 'nav.howToUse':'Chara guna', 'nav.settings':'Seting', 'nav.darkMode':'Mod petang', 'nav.lightMode':'Mod celak' },
  };
  Object.keys(NAV_FOOTER_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], NAV_FOOTER_I18N[l]);
  });

  // Final sweep: shared UI words, badge names/descriptions (client-side —
  // badge identity is stable across languages even though the API returns
  // English names/descriptions), chat.html (previously had zero i18n),
  // progress.html, and small gaps in podcast/slides/home/base.
  const FINAL_SWEEP_I18N = {
    'English':          { 'ui.cancel':'Cancel', 'ui.ok':'OK', 'badge.First Step':'First Step', 'badge.Quiz Ace':'Quiz Ace', 'badge.Week Warrior':'Week Warrior', 'badge.Dialect Pioneer':'Dialect Pioneer', 'badge.desc.First Step':'Completed your first session.', 'badge.desc.Quiz Ace':'Scored 100% on a quiz.', 'badge.desc.Week Warrior':'Active on 7 or more different days.', 'badge.desc.Dialect Pioneer':'Contributed 10+ entries in a local language.', 'chat.title':'Ask Edge', 'chat.namePh':'Your name…', 'chat.newChatTitle':'Start a new conversation', 'chat.greeting':"Hi there! I'm {name}, your AI tutor!\nPick a subject up top and ask me anything — I'm here to help you learn!", 'chat.inputPh':'Type your question here…', 'chat.micTitle':'Tap to record voice', 'chat.micStop':'Tap to stop recording', 'chat.sendTitle':'Send message', 'chat.confirmNewChat':'Start a new conversation? This will clear the current chat.', 'chat.listen':'Listen', 'chat.pause':'Pause', 'chat.loading':'Loading…', 'chat.copy':'Copy', 'chat.copied':'Copied', 'chat.verified':'Verified', 'chat.generalKnowledge':'General knowledge', 'chat.notInBooks':'Not in my books yet', 'chat.checkTeacher':'Check with teacher', 'chat.confidencePct':'Confidence: {pct}%', 'chat.noCurriculumMatch':'No matching curriculum found', 'chat.sources':'Sources', 'chat.connError':'Connection error — is Edge running?', 'chat.retry':'Retry', 'chat.micTooShort':'Tap the mic button to start recording, speak, then tap again to stop.', 'chat.sttFail':"I didn't catch that — please try again and speak a little louder.", 'chat.voiceUnreachable':"I couldn't reach the voice service. Please try again.", 'chat.micError':'Microphone not available: {err}', 'progress.title':'My Progress!', 'progress.subtitle':'See your badges, quiz results and achievements', 'progress.namePh':'Enter your name (e.g. Ali, Maria…)', 'progress.viewProgress':'View Progress', 'progress.recommended':'Recommended next steps', 'progress.quizHistory':'Quiz History', 'progress.noQuizzesShort':'No quizzes yet.', 'progress.enterName':'Please enter your name!', 'progress.notFound':'No progress found for "{name}". Complete a quiz or chat session first!', 'progress.lastActive':'Last active: {date}', 'progress.noBadgesYet':'No badges yet — keep learning!', 'progress.noQuizzesLong':'No quizzes yet — go try one!', 'progress.colTopic':'Topic', 'progress.colScore':'Score', 'progress.colDate':'Date', 'podcast.audioUnavailable':"Audio narration isn't available on this device right now — you can still read the script below.", 'slides.narrate':'Narrate', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'Test your knowledge!', 'home.act.cardsDesc':'Study key words!', 'home.act.podcastDesc':'Listen & learn!', 'home.act.progressDesc':'See your stars!', 'base.offline':'You are offline — Edge is running locally on this device!', 'base.settingsAria':'Settings', 'base.toggleThemeAria':'Toggle theme', 'base.dismissAria':'Dismiss' },
    'Filipino':         { 'ui.cancel':'Kanselahin', 'ui.ok':'OK', 'badge.First Step':'Unang Hakbang', 'badge.Quiz Ace':'Bihasa sa Quiz', 'badge.Week Warrior':'Palaban Buong Linggo', 'badge.Dialect Pioneer':'Pioneer ng Wika', 'badge.desc.First Step':'Natapos ang iyong unang session.', 'badge.desc.Quiz Ace':'Nakakuha ng 100% sa isang quiz.', 'badge.desc.Week Warrior':'Aktibo sa 7 o higit pang magkakaibang araw.', 'badge.desc.Dialect Pioneer':'Nag-ambag ng 10+ entry sa lokal na wika.', 'chat.title':'Magtanong kay Edge', 'chat.namePh':'Pangalan mo…', 'chat.newChatTitle':'Simulan ang bagong usapan', 'chat.greeting':"Kumusta! Ako si {name}, ang iyong AI tutor!\nPumili ng paksa sa itaas at magtanong ka — nandito ako para tulungan kang matuto!", 'chat.inputPh':'I-type ang iyong tanong dito…', 'chat.micTitle':'Pindutin para mag-record ng boses', 'chat.micStop':'Pindutin para ihinto ang pag-record', 'chat.sendTitle':'Ipadala ang mensahe', 'chat.confirmNewChat':'Simulan ang bagong usapan? Buburahin nito ang kasalukuyang chat.', 'chat.listen':'Pakinggan', 'chat.pause':'I-pause', 'chat.loading':'Naglo-load…', 'chat.copy':'Kopyahin', 'chat.copied':'Nakopya', 'chat.verified':'Beripikado', 'chat.generalKnowledge':'Pangkalahatang kaalaman', 'chat.notInBooks':'Wala pa sa aking mga libro', 'chat.checkTeacher':'Itanong sa guro', 'chat.confidencePct':'Kumpiyansa: {pct}%', 'chat.noCurriculumMatch':'Walang katugmang kurikulum', 'chat.sources':'Mga Pinagmulan', 'chat.connError':'Error sa koneksyon — gumagana ba ang Edge?', 'chat.retry':'Subukan muli', 'chat.micTooShort':'Pindutin ang mic button para magsimulang mag-record, magsalita, pagkatapos ay pindutin muli para huminto.', 'chat.sttFail':'Hindi ko naunawaan — pakisubukan muli at magsalita nang mas malakas.', 'chat.voiceUnreachable':'Hindi ma-reach ang voice service. Pakisubukang muli.', 'chat.micError':'Hindi available ang mikropono: {err}', 'progress.title':'Ang Aking Progreso!', 'progress.subtitle':'Tingnan ang iyong mga badge, resulta ng quiz at mga tagumpay', 'progress.namePh':'Ilagay ang iyong pangalan (hal. Ali, Maria…)', 'progress.viewProgress':'Tingnan ang Progreso', 'progress.recommended':'Inirerekomendang susunod na hakbang', 'progress.quizHistory':'Kasaysayan ng Quiz', 'progress.noQuizzesShort':'Wala pang quiz.', 'progress.enterName':'Pakilagay ang iyong pangalan!', 'progress.notFound':'Walang nakitang progreso para kay "{name}". Kumumpleto muna ng quiz o chat session!', 'progress.lastActive':'Huling aktibo: {date}', 'progress.noBadgesYet':'Wala pang badge — magpatuloy sa pag-aaral!', 'progress.noQuizzesLong':'Wala pang quiz — subukan ang isa!', 'progress.colTopic':'Paksa', 'progress.colScore':'Iskor', 'progress.colDate':'Petsa', 'podcast.audioUnavailable':'Hindi available ang audio narration sa device na ito ngayon — pwede mo pa ring basahin ang script sa ibaba.', 'slides.narrate':'Basahin', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'Subukin ang iyong kaalaman!', 'home.act.cardsDesc':'Pag-aralan ang mga susing salita!', 'home.act.podcastDesc':'Makinig at matuto!', 'home.act.progressDesc':'Tingnan ang iyong mga bituin!', 'base.offline':'Ikaw ay offline — Tumatakbo ang Edge nang lokal sa device na ito!', 'base.settingsAria':'Mga Setting', 'base.toggleThemeAria':'Palitan ang tema', 'base.dismissAria':'Isara' },
    'Bahasa Melayu':    { 'ui.cancel':'Batal', 'ui.ok':'OK', 'badge.First Step':'Langkah Pertama', 'badge.Quiz Ace':'Jaguh Kuiz', 'badge.Week Warrior':'Pahlawan Minggu', 'badge.Dialect Pioneer':'Perintis Dialek', 'badge.desc.First Step':'Selesai sesi pertama kamu.', 'badge.desc.Quiz Ace':'Skor 100% dalam kuiz.', 'badge.desc.Week Warrior':'Aktif pada 7 atau lebih hari berbeza.', 'badge.desc.Dialect Pioneer':'Menyumbang 10+ entri dalam bahasa tempatan.', 'chat.title':'Tanya Edge', 'chat.namePh':'Nama kamu…', 'chat.newChatTitle':'Mula perbualan baharu', 'chat.greeting':'Hai! Saya {name}, tutor AI kamu!\nPilih subjek di atas dan tanya apa-apa sahaja — saya di sini untuk bantu kamu belajar!', 'chat.inputPh':'Taip soalan kamu di sini…', 'chat.micTitle':'Tekan untuk rakam suara', 'chat.micStop':'Tekan untuk berhenti merakam', 'chat.sendTitle':'Hantar mesej', 'chat.confirmNewChat':'Mula perbualan baharu? Ini akan memadam chat semasa.', 'chat.listen':'Dengar', 'chat.pause':'Jeda', 'chat.loading':'Memuatkan…', 'chat.copy':'Salin', 'chat.copied':'Disalin', 'chat.verified':'Disahkan', 'chat.generalKnowledge':'Pengetahuan am', 'chat.notInBooks':'Belum ada dalam buku saya', 'chat.checkTeacher':'Semak dengan guru', 'chat.confidencePct':'Keyakinan: {pct}%', 'chat.noCurriculumMatch':'Tiada padanan kurikulum', 'chat.sources':'Sumber', 'chat.connError':'Ralat sambungan — adakah Edge berjalan?', 'chat.retry':'Cuba lagi', 'chat.micTooShort':'Tekan butang mic untuk mula merakam, bercakap, kemudian tekan sekali lagi untuk berhenti.', 'chat.sttFail':'Saya tidak faham — sila cuba lagi dan bercakap lebih kuat.', 'chat.voiceUnreachable':'Tidak dapat menghubungi perkhidmatan suara. Sila cuba lagi.', 'chat.micError':'Mikrofon tidak tersedia: {err}', 'progress.title':'Kemajuan Saya!', 'progress.subtitle':'Lihat lencana, keputusan kuiz dan pencapaian kamu', 'progress.namePh':'Masukkan nama kamu (cth. Ali, Maria…)', 'progress.viewProgress':'Lihat Kemajuan', 'progress.recommended':'Langkah seterusnya yang disyorkan', 'progress.quizHistory':'Sejarah Kuiz', 'progress.noQuizzesShort':'Belum ada kuiz.', 'progress.enterName':'Sila masukkan nama kamu!', 'progress.notFound':'Tiada kemajuan dijumpai untuk "{name}". Lengkapkan kuiz atau sesi chat dahulu!', 'progress.lastActive':'Aktif terakhir: {date}', 'progress.noBadgesYet':'Belum ada lencana — teruskan belajar!', 'progress.noQuizzesLong':'Belum ada kuiz — cuba satu!', 'progress.colTopic':'Topik', 'progress.colScore':'Skor', 'progress.colDate':'Tarikh', 'podcast.audioUnavailable':'Naratif audio tidak tersedia pada peranti ini sekarang — kamu masih boleh baca skrip di bawah.', 'slides.narrate':'Cerita', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'Uji pengetahuan kamu!', 'home.act.cardsDesc':'Belajar perkataan penting!', 'home.act.podcastDesc':'Dengar & belajar!', 'home.act.progressDesc':'Lihat bintang kamu!', 'base.offline':'Kamu di luar talian — Edge berjalan secara tempatan pada peranti ini!', 'base.settingsAria':'Tetapan', 'base.toggleThemeAria':'Tukar tema', 'base.dismissAria':'Tutup' },
    'Bahasa Indonesia': { 'ui.cancel':'Batal', 'ui.ok':'OK', 'badge.First Step':'Langkah Pertama', 'badge.Quiz Ace':'Jagoan Kuis', 'badge.Week Warrior':'Pejuang Minggu', 'badge.Dialect Pioneer':'Pelopor Dialek', 'badge.desc.First Step':'Menyelesaikan sesi pertamamu.', 'badge.desc.Quiz Ace':'Meraih skor 100% pada kuis.', 'badge.desc.Week Warrior':'Aktif pada 7 hari berbeda atau lebih.', 'badge.desc.Dialect Pioneer':'Menyumbang 10+ entri dalam bahasa lokal.', 'chat.title':'Tanya Edge', 'chat.namePh':'Namamu…', 'chat.newChatTitle':'Mulai percakapan baru', 'chat.greeting':'Halo! Saya {name}, tutor AI-mu!\nPilih subjek di atas dan tanyakan apa saja — saya di sini untuk membantumu belajar!', 'chat.inputPh':'Ketik pertanyaanmu di sini…', 'chat.micTitle':'Ketuk untuk rekam suara', 'chat.micStop':'Ketuk untuk berhenti merekam', 'chat.sendTitle':'Kirim pesan', 'chat.confirmNewChat':'Mulai percakapan baru? Ini akan menghapus chat saat ini.', 'chat.listen':'Dengar', 'chat.pause':'Jeda', 'chat.loading':'Memuat…', 'chat.copy':'Salin', 'chat.copied':'Disalin', 'chat.verified':'Terverifikasi', 'chat.generalKnowledge':'Pengetahuan umum', 'chat.notInBooks':'Belum ada di buku saya', 'chat.checkTeacher':'Tanyakan ke guru', 'chat.confidencePct':'Keyakinan: {pct}%', 'chat.noCurriculumMatch':'Tidak ada kurikulum yang cocok', 'chat.sources':'Sumber', 'chat.connError':'Kesalahan koneksi — apakah Edge berjalan?', 'chat.retry':'Coba lagi', 'chat.micTooShort':'Ketuk tombol mic untuk mulai merekam, bicara, lalu ketuk lagi untuk berhenti.', 'chat.sttFail':'Saya tidak menangkapnya — coba lagi dan bicara lebih keras.', 'chat.voiceUnreachable':'Tidak dapat menjangkau layanan suara. Coba lagi.', 'chat.micError':'Mikrofon tidak tersedia: {err}', 'progress.title':'Progresku!', 'progress.subtitle':'Lihat lencana, hasil kuis dan pencapaianmu', 'progress.namePh':'Masukkan namamu (mis. Ali, Maria…)', 'progress.viewProgress':'Lihat Progres', 'progress.recommended':'Langkah selanjutnya yang disarankan', 'progress.quizHistory':'Riwayat Kuis', 'progress.noQuizzesShort':'Belum ada kuis.', 'progress.enterName':'Silakan masukkan namamu!', 'progress.notFound':'Progres untuk "{name}" tidak ditemukan. Selesaikan kuis atau sesi chat dulu!', 'progress.lastActive':'Terakhir aktif: {date}', 'progress.noBadgesYet':'Belum ada lencana — terus belajar!', 'progress.noQuizzesLong':'Belum ada kuis — coba satu!', 'progress.colTopic':'Topik', 'progress.colScore':'Skor', 'progress.colDate':'Tanggal', 'podcast.audioUnavailable':'Narasi audio tidak tersedia di perangkat ini sekarang — kamu tetap bisa membaca skrip di bawah.', 'slides.narrate':'Bacakan', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'Uji pengetahuanmu!', 'home.act.cardsDesc':'Pelajari kata kunci!', 'home.act.podcastDesc':'Dengar & belajar!', 'home.act.progressDesc':'Lihat bintangmu!', 'base.offline':'Kamu sedang offline — Edge berjalan secara lokal di perangkat ini!', 'base.settingsAria':'Pengaturan', 'base.toggleThemeAria':'Ganti tema', 'base.dismissAria':'Tutup' },
    'Thai':             { 'ui.cancel':'ยกเลิก', 'ui.ok':'ตกลง', 'badge.First Step':'ก้าวแรก', 'badge.Quiz Ace':'เซียนควิซ', 'badge.Week Warrior':'นักสู้ประจำสัปดาห์', 'badge.Dialect Pioneer':'ผู้บุกเบิกภาษาถิ่น', 'badge.desc.First Step':'ทำเซสชันแรกของคุณเสร็จแล้ว', 'badge.desc.Quiz Ace':'ทำคะแนนได้ 100% ในแบบทดสอบ', 'badge.desc.Week Warrior':'ใช้งานอย่างน้อย 7 วันที่ต่างกัน', 'badge.desc.Dialect Pioneer':'ร่วมเพิ่มคำศัพท์ภาษาท้องถิ่น 10 รายการขึ้นไป', 'chat.title':'ถาม Edge', 'chat.namePh':'ชื่อของคุณ…', 'chat.newChatTitle':'เริ่มการสนทนาใหม่', 'chat.greeting':'สวัสดี! ฉันคือ {name} ครู AI ของคุณ!\nเลือกวิชาด้านบนแล้วถามอะไรก็ได้ — ฉันพร้อมช่วยให้คุณเรียนรู้!', 'chat.inputPh':'พิมพ์คำถามของคุณที่นี่…', 'chat.micTitle':'แตะเพื่อบันทึกเสียง', 'chat.micStop':'แตะเพื่อหยุดบันทึก', 'chat.sendTitle':'ส่งข้อความ', 'chat.confirmNewChat':'เริ่มการสนทนาใหม่หรือไม่? การแชทปัจจุบันจะถูกล้าง', 'chat.listen':'ฟัง', 'chat.pause':'หยุดชั่วคราว', 'chat.loading':'กำลังโหลด…', 'chat.copy':'คัดลอก', 'chat.copied':'คัดลอกแล้ว', 'chat.verified':'ยืนยันแล้ว', 'chat.generalKnowledge':'ความรู้ทั่วไป', 'chat.notInBooks':'ยังไม่มีในหนังสือของฉัน', 'chat.checkTeacher':'ตรวจสอบกับครู', 'chat.confidencePct':'ความมั่นใจ: {pct}%', 'chat.noCurriculumMatch':'ไม่พบหลักสูตรที่ตรงกัน', 'chat.sources':'แหล่งที่มา', 'chat.connError':'เกิดข้อผิดพลาดการเชื่อมต่อ — Edge กำลังทำงานอยู่หรือไม่?', 'chat.retry':'ลองอีกครั้ง', 'chat.micTooShort':'แตะปุ่มไมค์เพื่อเริ่มบันทึก พูด แล้วแตะอีกครั้งเพื่อหยุด', 'chat.sttFail':'ฉันไม่ได้ยิน — กรุณาลองอีกครั้งแล้วพูดดังขึ้น', 'chat.voiceUnreachable':'ไม่สามารถเชื่อมต่อบริการเสียงได้ กรุณาลองอีกครั้ง', 'chat.micError':'ไมโครโฟนไม่พร้อมใช้งาน: {err}', 'progress.title':'ความก้าวหน้าของฉัน!', 'progress.subtitle':'ดูเหรียญตรา ผลควิซ และความสำเร็จของคุณ', 'progress.namePh':'ใส่ชื่อของคุณ (เช่น Ali, Maria…)', 'progress.viewProgress':'ดูความก้าวหน้า', 'progress.recommended':'ขั้นตอนถัดไปที่แนะนำ', 'progress.quizHistory':'ประวัติควิซ', 'progress.noQuizzesShort':'ยังไม่มีแบบทดสอบ', 'progress.enterName':'กรุณาใส่ชื่อของคุณ!', 'progress.notFound':'ไม่พบความก้าวหน้าสำหรับ "{name}" กรุณาทำแบบทดสอบหรือแชทก่อน!', 'progress.lastActive':'ใช้งานล่าสุด: {date}', 'progress.noBadgesYet':'ยังไม่มีเหรียญตรา — เรียนต่อไป!', 'progress.noQuizzesLong':'ยังไม่มีแบบทดสอบ — ลองทำดูสิ!', 'progress.colTopic':'หัวข้อ', 'progress.colScore':'คะแนน', 'progress.colDate':'วันที่', 'podcast.audioUnavailable':'ขณะนี้เสียงบรรยายไม่พร้อมใช้งานบนอุปกรณ์นี้ — คุณยังคงอ่านสคริปต์ด้านล่างได้', 'slides.narrate':'บรรยาย', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'ทดสอบความรู้ของคุณ!', 'home.act.cardsDesc':'เรียนรู้คำศัพท์สำคัญ!', 'home.act.podcastDesc':'ฟังและเรียนรู้!', 'home.act.progressDesc':'ดูดาวของคุณ!', 'base.offline':'คุณออฟไลน์ — Edge กำลังทำงานในเครื่องนี้!', 'base.settingsAria':'การตั้งค่า', 'base.toggleThemeAria':'สลับธีม', 'base.dismissAria':'ปิด' },
    'Vietnamese':       { 'ui.cancel':'Hủy', 'ui.ok':'Đồng ý', 'badge.First Step':'Bước Đầu Tiên', 'badge.Quiz Ace':'Cao Thủ Kiểm Tra', 'badge.Week Warrior':'Chiến Binh Tuần', 'badge.Dialect Pioneer':'Người Tiên Phong Phương Ngữ', 'badge.desc.First Step':'Đã hoàn thành phiên học đầu tiên.', 'badge.desc.Quiz Ace':'Đạt 100% trong một bài kiểm tra.', 'badge.desc.Week Warrior':'Hoạt động trong 7 ngày khác nhau trở lên.', 'badge.desc.Dialect Pioneer':'Đóng góp 10+ mục bằng ngôn ngữ địa phương.', 'chat.title':'Hỏi Edge', 'chat.namePh':'Tên của bạn…', 'chat.newChatTitle':'Bắt đầu cuộc trò chuyện mới', 'chat.greeting':'Xin chào! Tôi là {name}, gia sư AI của bạn!\nChọn một môn học ở trên và hỏi bất cứ điều gì — tôi ở đây để giúp bạn học!', 'chat.inputPh':'Nhập câu hỏi của bạn ở đây…', 'chat.micTitle':'Nhấn để ghi âm giọng nói', 'chat.micStop':'Nhấn để dừng ghi âm', 'chat.sendTitle':'Gửi tin nhắn', 'chat.confirmNewChat':'Bắt đầu cuộc trò chuyện mới? Điều này sẽ xóa cuộc trò chuyện hiện tại.', 'chat.listen':'Nghe', 'chat.pause':'Tạm dừng', 'chat.loading':'Đang tải…', 'chat.copy':'Sao chép', 'chat.copied':'Đã sao chép', 'chat.verified':'Đã xác minh', 'chat.generalKnowledge':'Kiến thức chung', 'chat.notInBooks':'Chưa có trong sách của tôi', 'chat.checkTeacher':'Hỏi giáo viên', 'chat.confidencePct':'Độ tin cậy: {pct}%', 'chat.noCurriculumMatch':'Không tìm thấy chương trình học phù hợp', 'chat.sources':'Nguồn', 'chat.connError':'Lỗi kết nối — Edge có đang chạy không?', 'chat.retry':'Thử lại', 'chat.micTooShort':'Nhấn nút mic để bắt đầu ghi âm, nói, sau đó nhấn lại để dừng.', 'chat.sttFail':'Tôi không nghe rõ — vui lòng thử lại và nói to hơn.', 'chat.voiceUnreachable':'Không thể kết nối dịch vụ giọng nói. Vui lòng thử lại.', 'chat.micError':'Micro không khả dụng: {err}', 'progress.title':'Tiến Trình Của Tôi!', 'progress.subtitle':'Xem huy hiệu, kết quả kiểm tra và thành tích của bạn', 'progress.namePh':'Nhập tên của bạn (vd. Ali, Maria…)', 'progress.viewProgress':'Xem Tiến Trình', 'progress.recommended':'Bước tiếp theo được đề xuất', 'progress.quizHistory':'Lịch Sử Kiểm Tra', 'progress.noQuizzesShort':'Chưa có bài kiểm tra nào.', 'progress.enterName':'Vui lòng nhập tên của bạn!', 'progress.notFound':'Không tìm thấy tiến trình cho "{name}". Hãy hoàn thành một bài kiểm tra hoặc trò chuyện trước!', 'progress.lastActive':'Hoạt động lần cuối: {date}', 'progress.noBadgesYet':'Chưa có huy hiệu nào — tiếp tục học nhé!', 'progress.noQuizzesLong':'Chưa có bài kiểm tra nào — hãy thử một bài!', 'progress.colTopic':'Chủ đề', 'progress.colScore':'Điểm', 'progress.colDate':'Ngày', 'podcast.audioUnavailable':'Lời thuyết minh âm thanh hiện không khả dụng trên thiết bị này — bạn vẫn có thể đọc kịch bản bên dưới.', 'slides.narrate':'Đọc', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'Kiểm tra kiến thức của bạn!', 'home.act.cardsDesc':'Học từ khóa quan trọng!', 'home.act.podcastDesc':'Nghe & học!', 'home.act.progressDesc':'Xem những ngôi sao của bạn!', 'base.offline':'Bạn đang ngoại tuyến — Edge đang chạy cục bộ trên thiết bị này!', 'base.settingsAria':'Cài đặt', 'base.toggleThemeAria':'Chuyển chủ đề', 'base.dismissAria':'Đóng' },
    'Khmer':            { 'ui.cancel':'បោះបង់', 'ui.ok':'យល់ព្រម', 'badge.First Step':'ជំហានដំបូង', 'badge.Quiz Ace':'អ្នកជំនាញសំណួរ', 'badge.Week Warrior':'អ្នកតស៊ូប្រចាំសប្តាហ៍', 'badge.Dialect Pioneer':'អ្នកត្រួសត្រាយភាសាតំបន់', 'badge.desc.First Step':'បានបញ្ចប់វគ្គដំបូងរបស់អ្នក។', 'badge.desc.Quiz Ace':'ទទួលបានពិន្ទុ 100% លើសំណួរមួយ។', 'badge.desc.Week Warrior':'សកម្មក្នុងរយៈពេល 7 ថ្ងៃផ្សេងគ្នាឬច្រើនជាងនេះ។', 'badge.desc.Dialect Pioneer':'បានចូលរួមចំណែក 10+ ធាតុជាភាសាតំបន់។', 'chat.title':'សួរ Edge', 'chat.namePh':'ឈ្មោះរបស់អ្នក…', 'chat.newChatTitle':'ចាប់ផ្តើមការសន្ទនាថ្មី', 'chat.greeting':'សួស្តី! ខ្ញុំគឺ {name} គ្រូ AI របស់អ្នក!\nជ្រើសរើសមុខវិជ្ជានៅខាងលើ ហើយសួរអ្វីក៏បាន — ខ្ញុំនៅទីនេះដើម្បីជួយអ្នករៀន!', 'chat.inputPh':'វាយសំណួររបស់អ្នកនៅទីនេះ…', 'chat.micTitle':'ចុចដើម្បីថតសំឡេង', 'chat.micStop':'ចុចដើម្បីបញ្ឈប់ការថត', 'chat.sendTitle':'ផ្ញើសារ', 'chat.confirmNewChat':'ចាប់ផ្តើមការសន្ទនាថ្មី? វានឹងលុបការជជែកបច្ចុប្បន្ន។', 'chat.listen':'ស្តាប់', 'chat.pause':'ផ្អាក', 'chat.loading':'កំពុងផ្ទុក…', 'chat.copy':'ចម្លង', 'chat.copied':'បានចម្លង', 'chat.verified':'បានផ្ទៀងផ្ទាត់', 'chat.generalKnowledge':'ចំណេះដឹងទូទៅ', 'chat.notInBooks':'មិនទាន់មាននៅក្នុងសៀវភៅរបស់ខ្ញុំនៅឡើយទេ', 'chat.checkTeacher':'ពិនិត្យជាមួយគ្រូ', 'chat.confidencePct':'ទំនុកចិត្ត៖ {pct}%', 'chat.noCurriculumMatch':'រកមិនឃើញកម្មវិធីសិក្សាដែលត្រូវគ្នា', 'chat.sources':'ប្រភព', 'chat.connError':'កំហុសក្នុងការភ្ជាប់ — តើ Edge កំពុងដំណើរការឬទេ?', 'chat.retry':'ព្យាយាមម្តងទៀត', 'chat.micTooShort':'ចុចប៊ូតុងមីក្រូដើម្បីចាប់ផ្តើមថត និយាយ បន្ទាប់មកចុចម្តងទៀតដើម្បីបញ្ឈប់។', 'chat.sttFail':'ខ្ញុំមិនបានឮទេ — សូមព្យាយាមម្តងទៀត ហើយនិយាយឱ្យខ្លាំងជាងនេះ។', 'chat.voiceUnreachable':'មិនអាចភ្ជាប់សេវាសំឡេងបានទេ។ សូមព្យាយាមម្តងទៀត។', 'chat.micError':'មីក្រូហ្វូនមិនអាចប្រើបានទេ៖ {err}', 'progress.title':'វឌ្ឍនភាពរបស់ខ្ញុំ!', 'progress.subtitle':'មើលស្លាកសញ្ញា លទ្ធផលសំណួរ និងសមិទ្ធផលរបស់អ្នក', 'progress.namePh':'បញ្ចូលឈ្មោះរបស់អ្នក (ឧ. Ali, Maria…)', 'progress.viewProgress':'មើលវឌ្ឍនភាព', 'progress.recommended':'ជំហានបន្ទាប់ដែលបានណែនាំ', 'progress.quizHistory':'ប្រវត្តិសំណួរ', 'progress.noQuizzesShort':'មិនទាន់មានសំណួរនៅឡើយទេ។', 'progress.enterName':'សូមបញ្ចូលឈ្មោះរបស់អ្នក!', 'progress.notFound':'រកមិនឃើញវឌ្ឍនភាពសម្រាប់ "{name}" ទេ។ សូមបញ្ចប់សំណួរ ឬវគ្គជជែកជាមុនសិន!', 'progress.lastActive':'សកម្មចុងក្រោយ៖ {date}', 'progress.noBadgesYet':'មិនទាន់មានស្លាកសញ្ញានៅឡើយទេ — បន្តរៀន!', 'progress.noQuizzesLong':'មិនទាន់មានសំណួរនៅឡើយទេ — សាកល្បងមួយមើល!', 'progress.colTopic':'ប្រធានបទ', 'progress.colScore':'ពិន្ទុ', 'progress.colDate':'កាលបរិច្ឆេទ', 'podcast.audioUnavailable':'ការនិទានសំឡេងមិនអាចប្រើបានលើឧបករណ៍នេះទេឥឡូវនេះ — អ្នកនៅតែអាចអានស្គ្រីបខាងក្រោម។', 'slides.narrate':'អាន', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'សាកល្បងចំណេះដឹងរបស់អ្នក!', 'home.act.cardsDesc':'រៀនពាក្យគន្លឹះ!', 'home.act.podcastDesc':'ស្តាប់ និងរៀន!', 'home.act.progressDesc':'មើលផ្កាយរបស់អ្នក!', 'base.offline':'អ្នកកំពុងក្រៅបណ្តាញ — Edge កំពុងដំណើរការក្នុងឧបករណ៍នេះ!', 'base.settingsAria':'ការកំណត់', 'base.toggleThemeAria':'ប្តូរស្បែក', 'base.dismissAria':'បិទ' },
    'Lao':              { 'ui.cancel':'ຍົກເລີກ', 'ui.ok':'ຕົກລົງ', 'badge.First Step':'ບາດກ້າວທຳອິດ', 'badge.Quiz Ace':'ຜູ້ຊ່ຽວຊານຄຳຖາມ', 'badge.Week Warrior':'ນັກສູ້ປະຈຳອາທິດ', 'badge.Dialect Pioneer':'ຜູ້ບຸກເບີກພາສາທ້ອງຖິ່ນ', 'badge.desc.First Step':'ສຳເລັດເຊສຊັນທຳອິດຂອງທ່ານແລ້ວ.', 'badge.desc.Quiz Ace':'ໄດ້ຄະແນນ 100% ໃນຄຳຖາມ.', 'badge.desc.Week Warrior':'ເຄື່ອນໄຫວໃນ 7 ວັນ ຫຼືຫຼາຍກວ່ານັ້ນ.', 'badge.desc.Dialect Pioneer':'ປະກອບສ່ວນ 10+ ລາຍການເປັນພາສາທ້ອງຖິ່ນ.', 'chat.title':'ຖາມ Edge', 'chat.namePh':'ຊື່ຂອງທ່ານ…', 'chat.newChatTitle':'ເລີ່ມການສົນທະນາໃໝ່', 'chat.greeting':'ສະບາຍດີ! ຂ້ອຍແມ່ນ {name} ຄູ AI ຂອງທ່ານ!\nເລືອກວິຊາຢູ່ເທິງ ແລະ ຖາມຫຍັງກໍໄດ້ — ຂ້ອຍຢູ່ນີ້ເພື່ອຊ່ວຍທ່ານຮຽນ!', 'chat.inputPh':'ພິມຄຳຖາມຂອງທ່ານທີ່ນີ້…', 'chat.micTitle':'ແຕະເພື່ອບັນທຶກສຽງ', 'chat.micStop':'ແຕະເພື່ອຢຸດການບັນທຶກ', 'chat.sendTitle':'ສົ່ງຂໍ້ຄວາມ', 'chat.confirmNewChat':'ເລີ່ມການສົນທະນາໃໝ່? ນີ້ຈະລຶບການສົນທະນາປັດຈຸບັນ.', 'chat.listen':'ຟັງ', 'chat.pause':'ຢຸດຊົ່ວຄາວ', 'chat.loading':'ກຳລັງໂຫຼດ…', 'chat.copy':'ສຳເນົາ', 'chat.copied':'ສຳເນົາແລ້ວ', 'chat.verified':'ຢືນຢັນແລ້ວ', 'chat.generalKnowledge':'ຄວາມຮູ້ທົ່ວໄປ', 'chat.notInBooks':'ຍັງບໍ່ມີໃນປຶ້ມຂອງຂ້ອຍ', 'chat.checkTeacher':'ກວດສອບກັບຄູ', 'chat.confidencePct':'ຄວາມໝັ້ນໃຈ: {pct}%', 'chat.noCurriculumMatch':'ບໍ່ພົບຫຼັກສູດທີ່ກົງກັນ', 'chat.sources':'ແຫຼ່ງຂໍ້ມູນ', 'chat.connError':'ຂໍ້ຜິດພາດການເຊື່ອມຕໍ່ — Edge ກຳລັງເຮັດວຽກຢູ່ບໍ?', 'chat.retry':'ລອງໃໝ່', 'chat.micTooShort':'ແຕະປຸ່ມໄມໂຄຣໂຟນເພື່ອເລີ່ມບັນທຶກ, ເວົ້າ, ແລ້ວແຕະອີກຄັ້ງເພື່ອຢຸດ.', 'chat.sttFail':'ຂ້ອຍບໍ່ໄດ້ຍິນ — ກະລຸນາລອງໃໝ່ ແລະ ເວົ້າໃຫ້ດັງຂຶ້ນ.', 'chat.voiceUnreachable':'ບໍ່ສາມາດເຊື່ອມຕໍ່ບໍລິການສຽງໄດ້. ກະລຸນາລອງໃໝ່.', 'chat.micError':'ໄມໂຄຣໂຟນບໍ່ພ້ອມໃຊ້ງານ: {err}', 'progress.title':'ຄວາມຄືບໜ້າຂອງຂ້ອຍ!', 'progress.subtitle':'ເບິ່ງຫຼຽນ, ຜົນຄຳຖາມ ແລະ ຄວາມສຳເລັດຂອງທ່ານ', 'progress.namePh':'ໃສ່ຊື່ຂອງທ່ານ (ຕົວຢ່າງ: Ali, Maria…)', 'progress.viewProgress':'ເບິ່ງຄວາມຄືບໜ້າ', 'progress.recommended':'ຂັ້ນຕອນຕໍ່ໄປທີ່ແນະນຳ', 'progress.quizHistory':'ປະຫວັດຄຳຖາມ', 'progress.noQuizzesShort':'ຍັງບໍ່ມີແບບທົດສອບ.', 'progress.enterName':'ກະລຸນາໃສ່ຊື່ຂອງທ່ານ!', 'progress.notFound':'ບໍ່ພົບຄວາມຄືບໜ້າສຳລັບ "{name}". ກະລຸນາເຮັດແບບທົດສອບ ຫຼື ການສົນທະນາກ່ອນ!', 'progress.lastActive':'ເຄື່ອນໄຫວຫຼ້າສຸດ: {date}', 'progress.noBadgesYet':'ຍັງບໍ່ມີຫຼຽນ — ຮຽນຕໍ່ໄປ!', 'progress.noQuizzesLong':'ຍັງບໍ່ມີແບບທົດສອບ — ລອງເບິ່ງອັນໜຶ່ງ!', 'progress.colTopic':'ຫົວຂໍ້', 'progress.colScore':'ຄະແນນ', 'progress.colDate':'ວັນທີ', 'podcast.audioUnavailable':'ຕອນນີ້ການບັນຍາຍສຽງບໍ່ພ້ອມໃຊ້ງານໃນອຸປະກອນນີ້ — ທ່ານຍັງສາມາດອ່ານສະຄຣິບຂ້າງລຸ່ມນີ້ໄດ້.', 'slides.narrate':'ບັນລະຍາຍ', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'ທົດສອບຄວາມຮູ້ຂອງທ່ານ!', 'home.act.cardsDesc':'ຮຽນຄຳສັບສຳຄັນ!', 'home.act.podcastDesc':'ຟັງ ແລະ ຮຽນຮູ້!', 'home.act.progressDesc':'ເບິ່ງດາວຂອງທ່ານ!', 'base.offline':'ທ່ານອອບໄລນ໌ — Edge ກຳລັງເຮັດວຽກຢູ່ໃນອຸປະກອນນີ້!', 'base.settingsAria':'ການຕັ້ງຄ່າ', 'base.toggleThemeAria':'ສະຫຼັບຮູບແບບ', 'base.dismissAria':'ປິດ' },
    'Burmese':          { 'ui.cancel':'ပယ်ဖျက်', 'ui.ok':'OK', 'badge.First Step':'ပထမခြေလှမ်း', 'badge.Quiz Ace':'Quiz ကျွမ်းကျင်သူ', 'badge.Week Warrior':'အပတ်စဉ်စစ်သူရဲ', 'badge.Dialect Pioneer':'ဒေသိယစကားဦးဆောင်သူ', 'badge.desc.First Step':'သင့်ပထမဆုံး session ကို ပြီးမြောက်ခဲ့သည်။', 'badge.desc.Quiz Ace':'Quiz တစ်ခုတွင် 100% ရမှတ်ရရှိခဲ့သည်။', 'badge.desc.Week Warrior':'ရက် 7 ရက် သို့မဟုတ် ထို့ထက်ပို၍ တက်ကြွစွာပါဝင်ခဲ့သည်။', 'badge.desc.Dialect Pioneer':'ဒေသစကားဖြင့် ထည့်သွင်းမှု 10+ ကို ပါဝင်ခဲ့သည်။', 'chat.title':'Edge ကို မေးပါ', 'chat.namePh':'သင့်နာမည်…', 'chat.newChatTitle':'စကားပြောအသစ် စတင်ပါ', 'chat.greeting':'မင်္ဂလာပါ! ကျွန်ုပ်က {name}၊ သင့် AI ဆရာပါ!\nအပေါ်က ဘာသာရပ်တစ်ခုရွေးပြီး ဘာမဆိုမေးပါ — သင်လေ့လာနိုင်ရန် ကျွန်ုပ်ဒီမှာ ရှိပါတယ်!', 'chat.inputPh':'သင့်မေးခွန်းကို ဒီမှာ ရိုက်ထည့်ပါ…', 'chat.micTitle':'အသံဖမ်းရန် တစ်ချက်နှိပ်ပါ', 'chat.micStop':'အသံဖမ်းခြင်းရပ်ရန် ထပ်နှိပ်ပါ', 'chat.sendTitle':'မက်ဆေ့ချ်ပို့ပါ', 'chat.confirmNewChat':'စကားပြောအသစ် စတင်မလား? လက်ရှိစကားပြောကို ရှင်းလင်းမည်။', 'chat.listen':'နားထောင်ပါ', 'chat.pause':'ခေတ္တရပ်', 'chat.loading':'တင်နေသည်…', 'chat.copy':'ကူးယူပါ', 'chat.copied':'ကူးယူပြီး', 'chat.verified':'အတည်ပြုပြီး', 'chat.generalKnowledge':'အထွေထွေ အသိပညာ', 'chat.notInBooks':'ကျွန်ုပ်၏စာအုပ်များတွင် မရှိသေးပါ', 'chat.checkTeacher':'ဆရာနှင့် စစ်ဆေးပါ', 'chat.confidencePct':'ယုံကြည်မှု: {pct}%', 'chat.noCurriculumMatch':'သက်ဆိုင်သော သင်ရိုးညွှန်းတမ်း မတွေ့ပါ', 'chat.sources':'အရင်းအမြစ်များ', 'chat.connError':'ချိတ်ဆက်မှု အမှား — Edge အလုပ်လုပ်နေပါသလား?', 'chat.retry':'ထပ်စမ်းပါ', 'chat.micTooShort':'အသံဖမ်းရန် မိုက်ခလုတ်ကို နှိပ်ပါ၊ ပြောပါ၊ ပြီးလျှင် ရပ်ရန် ထပ်နှိပ်ပါ။', 'chat.sttFail':'ကျွန်ုပ် နားမလည်ပါ — ထပ်ကြိုးစားပြီး ပိုကျယ်အောင်ပြောပါ။', 'chat.voiceUnreachable':'အသံဝန်ဆောင်မှုကို မချိတ်ဆက်နိုင်ပါ။ ထပ်စမ်းပါ။', 'chat.micError':'မိုက်ခရိုဖုန်း မရနိုင်ပါ: {err}', 'progress.title':'ကျွန်ုပ်၏ တိုးတက်မှု!', 'progress.subtitle':'သင့်တံဆိပ်၊ Quiz ရလဒ်နှင့် အောင်မြင်မှုများကို ကြည့်ပါ', 'progress.namePh':'သင့်နာမည်ကို ထည့်ပါ (ဥပမာ - Ali, Maria…)', 'progress.viewProgress':'တိုးတက်မှု ကြည့်ပါ', 'progress.recommended':'အကြံပြုထားသော နောက်တစ်ဆင့်များ', 'progress.quizHistory':'Quiz မှတ်တမ်း', 'progress.noQuizzesShort':'Quiz မရှိသေးပါ။', 'progress.enterName':'သင့်နာမည်ကို ထည့်ပါ!', 'progress.notFound':'"{name}" အတွက် တိုးတက်မှု မတွေ့ပါ။ Quiz သို့မဟုတ် စကားပြောဝိုင်းကို အရင်ပြီးအောင်လုပ်ပါ!', 'progress.lastActive':'နောက်ဆုံးအသုံးပြုချိန်: {date}', 'progress.noBadgesYet':'တံဆိပ် မရှိသေးပါ — ဆက်လေ့လာပါ!', 'progress.noQuizzesLong':'Quiz မရှိသေးပါ — တစ်ခု စမ်းကြည့်ပါ!', 'progress.colTopic':'ခေါင်းစဉ်', 'progress.colScore':'ရမှတ်', 'progress.colDate':'ရက်စွဲ', 'podcast.audioUnavailable':'ဤစက်ပစ္စည်းတွင် အသံဖတ်ပြခြင်း ယခုမရနိုင်ပါ — အောက်ပါစာသားကို ဖတ်နိုင်ပါသေးသည်။', 'slides.narrate':'ဖတ်ပြ', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'သင့်အသိပညာကို စမ်းသပ်ပါ!', 'home.act.cardsDesc':'အဓိကစကားလုံးများ လေ့လာပါ!', 'home.act.podcastDesc':'နားထောင်ပြီး လေ့လာပါ!', 'home.act.progressDesc':'သင့်ကြယ်များကို ကြည့်ပါ!', 'base.offline':'သင် အော့ဖ်လိုင်းဖြစ်နေသည် — Edge သည် ဤစက်ပစ္စည်းပေါ်တွင် လိုက်ဖက်စွာ အလုပ်လုပ်နေသည်!', 'base.settingsAria':'ဆက်တင်များ', 'base.toggleThemeAria':'အသွင်အပြင် ပြောင်းပါ', 'base.dismissAria':'ပိတ်ပါ' },
    'Cebuano':          { 'ui.cancel':'Kanselahon', 'ui.ok':'OK', 'badge.First Step':'Unang Lakang', 'badge.Quiz Ace':'Batid sa Quiz', 'badge.Week Warrior':'Manggugubat sa Semana', 'badge.Dialect Pioneer':'Payunir sa Diyalekto', 'badge.desc.First Step':'Nahuman ang imong unang session.', 'badge.desc.Quiz Ace':'Nakakuha og 100% sa usa ka quiz.', 'badge.desc.Week Warrior':'Aktibo sa 7 o labaw pa ka lain-laing adlaw.', 'badge.desc.Dialect Pioneer':'Nag-amot og 10+ entries sa lokal nga pinulongan.', 'chat.title':'Pangutan-a si Edge', 'chat.namePh':'Imong ngalan…', 'chat.newChatTitle':'Sugdi ang bag-ong panag-istoryahanay', 'chat.greeting':'Kumusta! Ako si {name}, imong AI tutor!\nPagpili og subject sa taas ug pangutana bisan unsa — ania ko para tabangan ka makakat-on!', 'chat.inputPh':'I-type ang imong pangutana dinhi…', 'chat.micTitle':'I-tap aron irekord ang tingog', 'chat.micStop':'I-tap aron ihunong ang pagrekord', 'chat.sendTitle':'Ipadala ang mensahe', 'chat.confirmNewChat':'Sugdi ang bag-ong panag-istoryahanay? Mawala ang kasamtangang chat.', 'chat.listen':'Paminawa', 'chat.pause':'I-pause', 'chat.loading':'Nag-load…', 'chat.copy':'Kopyaha', 'chat.copied':'Nakopya', 'chat.verified':'Na-verify', 'chat.generalKnowledge':'Kinatibuk-ang kahibalo', 'chat.notInBooks':'Wala pa sa akong mga libro', 'chat.checkTeacher':'Susiha sa magtutudlo', 'chat.confidencePct':'Pagsalig: {pct}%', 'chat.noCurriculumMatch':'Walay nahiangay nga kurikulum', 'chat.sources':'Mga Tinubdan', 'chat.connError':'Sayop sa koneksyon — nagdagan ba ang Edge?', 'chat.retry':'Sulayi pag-usab', 'chat.micTooShort':'I-tap ang mic button aron magsugod og rekord, pagsulti, dayon i-tap pag-usab aron mohunong.', 'chat.sttFail':'Wala nako madungog — palihog sulayi pag-usab ug pagsulti og mas kusog.', 'chat.voiceUnreachable':'Dili maabot ang serbisyo sa tingog. Palihog sulayi pag-usab.', 'chat.micError':'Wala magamit ang mikropono: {err}', 'progress.title':'Akong Progreso!', 'progress.subtitle':'Tan-awa ang imong mga badge, resulta sa quiz ug mga kalamposan', 'progress.namePh':'Ibutang ang imong ngalan (pananglitan, Ali, Maria…)', 'progress.viewProgress':'Tan-awa ang Progreso', 'progress.recommended':'Girekomenda nga sunod nga lakang', 'progress.quizHistory':'Kasaysayan sa Quiz', 'progress.noQuizzesShort':'Wala pay quiz.', 'progress.enterName':'Palihog ibutang ang imong ngalan!', 'progress.notFound':'Walay nakit-an nga progreso para sa "{name}". Human-a una ang quiz o chat session!', 'progress.lastActive':'Katapusang aktibo: {date}', 'progress.noBadgesYet':'Wala pay badge — padayon sa pagkat-on!', 'progress.noQuizzesLong':'Wala pay quiz — sulayi ang usa!', 'progress.colTopic':'Topic', 'progress.colScore':'Iskor', 'progress.colDate':'Petsa', 'podcast.audioUnavailable':'Ang audio narration dili available karon niini nga device — mabasa gihapon nimo ang script sa ubos.', 'slides.narrate':'Basaha', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'Sulayi ang imong kahibalo!', 'home.act.cardsDesc':'Tun-i ang mga importanteng pulong!', 'home.act.podcastDesc':'Paminaw ug pagkat-on!', 'home.act.progressDesc':'Tan-awa ang imong mga bituon!', 'base.offline':'Offline ka — nagdagan ang Edge lokal niini nga device!', 'base.settingsAria':'Mga Setting', 'base.toggleThemeAria':'Ilisi ang tema', 'base.dismissAria':'Isira' },
    'Iban':             { 'ui.cancel':'Batal', 'ui.ok':'OK', 'badge.First Step':'Awak Pemuka', 'badge.Quiz Ace':'Pintar Quiz', 'badge.Week Warrior':'Pahlawan Minggu', 'badge.Dialect Pioneer':'Perintis Jaku', 'badge.desc.First Step':'Udah nembu session keterubah nuan.', 'badge.desc.Quiz Ace':'Bulih score 100% dalam siti quiz.', 'badge.desc.Week Warrior':'Aktif dalam 7 hari tauka lebih.', 'badge.desc.Dialect Pioneer':'Nyumbang 10+ leka jaku ba jaku menua.', 'chat.title':'Tanya Edge', 'chat.namePh':'Nama nuan…', 'chat.newChatTitle':'Berengkah pengawa madah baru', 'chat.greeting':'Hello! Aku {name}, tutor AI nuan!\nPilih subjek ba atas lalu tanya nama utai — aku ditu kena nulung nuan belajar!', 'chat.inputPh':'Tulis tanya nuan ditu…', 'chat.micTitle':'Tekan kena rekod nyawa', 'chat.micStop':'Tekan kena ngetu rekod', 'chat.sendTitle':'Kirum berita', 'chat.confirmNewChat':'Berengkah pengawa madah baru? Tu deka nyapu chat diatu.', 'chat.listen':'Dinga', 'chat.pause':'Rejang', 'chat.loading':'Benung ngemuatka…', 'chat.copy':'Salin', 'chat.copied':'Udah disalin', 'chat.verified':'Udah disahka', 'chat.generalKnowledge':'Penemu bukai', 'chat.notInBooks':'Apin bisi ba buku aku', 'chat.checkTeacher':'Tanya enggau pengajar', 'chat.confidencePct':'Pechaya: {pct}%', 'chat.noCurriculumMatch':'Nadai silibus ke sama', 'chat.sources':'Pun', 'chat.connError':'Silap penyambung — Edge benung bekereja?', 'chat.retry':'Cuba baru', 'chat.micTooShort':'Tekan butang mic kena berengkah ngerekod, jaku, udah nya tekan sekali agi kena ngetu.', 'chat.sttFail':'Aku enda ninga — cuba baru lalu jaku labuh agi.', 'chat.voiceUnreachable':'Enda ulih neroka pengawa nyawa. Cuba baru.', 'chat.micError':'Mikrofon nadai: {err}', 'progress.title':'Penemu Aku!', 'progress.subtitle':'Meda lencana, penemu quiz enggau pengachara nuan', 'progress.namePh':'Tama nama nuan (chunto: Ali, Maria…)', 'progress.viewProgress':'Meda Penemu', 'progress.recommended':'Chara seterusnya ke disarahka', 'progress.quizHistory':'Sejarah Quiz', 'progress.noQuizzesShort':'Nadai quiz agi.', 'progress.enterName':'Tolong tama nama nuan!', 'progress.notFound':'Nadai penemu ke ditemu ke "{name}". Nembu quiz tauka chat session dulu!', 'progress.lastActive':'Aktif kelia: {date}', 'progress.noBadgesYet':'Nadai lencana agi — terus belajar!', 'progress.noQuizzesLong':'Nadai quiz agi — cuba siti!', 'progress.colTopic':'Topik', 'progress.colScore':'Score', 'progress.colDate':'Hari', 'podcast.audioUnavailable':'Naratif nyawa nadai ulih diguna ba peranti tu diatu — nuan agi ulih macha skrip baruh.', 'slides.narrate':'Cerita', 'slides.pdf':'PDF', 'slides.pptx':'PowerPoint (.pptx)', 'home.act.quizDesc':'Uji penemu nuan!', 'home.act.cardsDesc':'Belajar leka jaku penting!', 'home.act.podcastDesc':'Dinga & belajar!', 'home.act.progressDesc':'Meda bintang nuan!', 'base.offline':'Nuan offline — Edge bekereja setempat ba peranti tu!', 'base.settingsAria':'Seting', 'base.toggleThemeAria':'Tukar tema', 'base.dismissAria':'Tutup' },
  };
  Object.keys(FINAL_SWEEP_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], FINAL_SWEEP_I18N[l]);
  });

  // History feature (quiz/cards/slides/podcast — reopen a past generation),
  // merged into the per-language tables above.
  const HISTORY_I18N = {
    'English':          { 'history.pastQuizzes':'Past quizzes', 'history.pastDecks':'Past decks', 'history.pastEpisodes':'Past episodes', 'history.loadError':'Could not load that item.', 'podcast.hasAudio':'With audio', 'history.show':'Show', 'history.hide':'Hide' },
    'Filipino':         { 'history.pastQuizzes':'Mga nakaraang quiz', 'history.pastDecks':'Mga nakaraang deck', 'history.pastEpisodes':'Mga nakaraang episode', 'history.loadError':'Hindi ma-load ang item na iyon.', 'podcast.hasAudio':'May audio', 'history.show':'Ipakita', 'history.hide':'Itago' },
    'Bahasa Melayu':    { 'history.pastQuizzes':'Kuiz lepas', 'history.pastDecks':'Dek lepas', 'history.pastEpisodes':'Episod lepas', 'history.loadError':'Tidak dapat memuatkan item itu.', 'podcast.hasAudio':'Dengan audio', 'history.show':'Tunjuk', 'history.hide':'Sembunyi' },
    'Bahasa Indonesia': { 'history.pastQuizzes':'Kuis sebelumnya', 'history.pastDecks':'Dek sebelumnya', 'history.pastEpisodes':'Episode sebelumnya', 'history.loadError':'Tidak dapat memuat item itu.', 'podcast.hasAudio':'Dengan audio', 'history.show':'Tampilkan', 'history.hide':'Sembunyikan' },
    'Thai':             { 'history.pastQuizzes':'ควิซที่ผ่านมา', 'history.pastDecks':'ชุดที่ผ่านมา', 'history.pastEpisodes':'ตอนที่ผ่านมา', 'history.loadError':'ไม่สามารถโหลดรายการนั้นได้', 'podcast.hasAudio':'มีเสียง', 'history.show':'แสดง', 'history.hide':'ซ่อน' },
    'Vietnamese':       { 'history.pastQuizzes':'Bài kiểm tra trước', 'history.pastDecks':'Bộ thẻ trước', 'history.pastEpisodes':'Tập trước', 'history.loadError':'Không thể tải mục đó.', 'podcast.hasAudio':'Có âm thanh', 'history.show':'Hiện', 'history.hide':'Ẩn' },
    'Khmer':            { 'history.pastQuizzes':'សំណួរពីមុន', 'history.pastDecks':'កញ្ចប់ពីមុន', 'history.pastEpisodes':'វគ្គពីមុន', 'history.loadError':'មិនអាចផ្ទុកធាតុនោះបានទេ។', 'podcast.hasAudio':'មានសំឡេង', 'history.show':'បង្ហាញ', 'history.hide':'លាក់' },
    'Lao':              { 'history.pastQuizzes':'ແບບທົດສອບທີ່ຜ່ານມາ', 'history.pastDecks':'ຊຸດທີ່ຜ່ານມາ', 'history.pastEpisodes':'ຕອນທີ່ຜ່ານມາ', 'history.loadError':'ບໍ່ສາມາດໂຫຼດລາຍການນັ້ນໄດ້.', 'podcast.hasAudio':'ມີສຽງ', 'history.show':'ສະແດງ', 'history.hide':'ເຊື່ອງ' },
    'Burmese':          { 'history.pastQuizzes':'ယခင် Quiz များ', 'history.pastDecks':'ယခင်အစုံများ', 'history.pastEpisodes':'ယခင်အပိုင်းများ', 'history.loadError':'ထိုအရာကို တင်၍မရပါ။', 'podcast.hasAudio':'အသံပါ', 'history.show':'ပြရန်', 'history.hide':'ဖျောက်ရန်' },
    'Cebuano':          { 'history.pastQuizzes':'Nangaging mga quiz', 'history.pastDecks':'Nangaging mga deck', 'history.pastEpisodes':'Nangaging mga episode', 'history.loadError':'Dili ma-load kana nga item.', 'podcast.hasAudio':'Adunay audio', 'history.show':'Ipakita', 'history.hide':'Itago' },
    'Iban':             { 'history.pastQuizzes':'Quiz kelia', 'history.pastDecks':'Dek kelia', 'history.pastEpisodes':'Episod kelia', 'history.loadError':'Enda ulih ngemuatka utai nya.', 'podcast.hasAudio':'Enggau nyawa', 'history.show':'Pandang', 'history.hide':'Rahsiaka' },
  };
  Object.keys(HISTORY_I18N).forEach(function (l) {
    if (TRANSLATIONS[l]) Object.assign(TRANSLATIONS[l], HISTORY_I18N[l]);
  });

  var _current = 'English';

  function applyLang(lang) {
    const t = TRANSLATIONS[lang] || TRANSLATIONS['English'];
    _current = TRANSLATIONS[lang] ? lang : 'English';

    // Pass 1 — data-i18n attributes. Elements that nest an icon (e.g. nav
    // links with an inline <svg>) only get their trailing text node
    // replaced, so translating the label never wipes out the icon.
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (t[key] === undefined) return;
      if (el.querySelector('svg, img')) {
        var textNode = el.lastChild;
        if (textNode && textNode.nodeType === Node.TEXT_NODE) {
          textNode.textContent = ' ' + t[key];
        } else {
          el.appendChild(document.createTextNode(' ' + t[key]));
        }
      } else {
        el.innerHTML = t[key];
      }
    });

    // Pass 1b — translatable placeholders
    document.querySelectorAll('[data-i18n-ph]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-ph');
      if (t[key] !== undefined) el.setAttribute('placeholder', t[key]);
    });

    // Pass 1c — translatable title/aria-label attributes (tooltips, screen readers)
    document.querySelectorAll('[data-i18n-title]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-title');
      if (t[key] !== undefined) el.setAttribute('title', t[key]);
    });
    document.querySelectorAll('[data-i18n-aria]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-aria');
      if (t[key] !== undefined) el.setAttribute('aria-label', t[key]);
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
      if (!el || t[pair[1]] === undefined) return;
      if (el.querySelector('svg, img')) {
        var textNode = el.lastChild;
        if (textNode && textNode.nodeType === Node.TEXT_NODE) {
          textNode.textContent = ' ' + t[pair[1]];
        } else {
          el.appendChild(document.createTextNode(' ' + t[pair[1]]));
        }
      } else {
        el.innerHTML = t[pair[1]];
      }
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

    // Re-render dynamic (JS-built) content that has no data-i18n of its own
    // and would otherwise stay frozen in whatever language it was first rendered in.
    if (window.EdgeSidebarRefresh) window.EdgeSidebarRefresh();
    if (window.EdgeProgressRefresh) window.EdgeProgressRefresh();
    if (window.EdgeChatRefresh) window.EdgeChatRefresh();
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

  // Flag a wrong translation (e.g. an MT'd topic chip) for teacher review.
  window.reportTranslation = function (shown) {
    var note = prompt(t('report.prompt', 'What looks wrong? (optional)'));
    if (note === null) return;                 // cancelled
    fetch('/api/translation/report', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        language: localStorage.getItem('edu_lang') || 'English',
        shown: shown || '', note: note, page: location.pathname,
      }),
    }).then(function () { alert(t('report.thanks', 'Thanks! A teacher will review it.')); })
      .catch(function () {});
  };

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
