/* =====================================================================
   Olive Skin · 상담 챗봇 (워크 지니어스 챗봇과 같은 방식)
   정해진 답변만 보여 줘요 (AI 아님). 답변은 아래 QA 에서 고치면 됩니다.
   "상담 남기기"에 적은 질문 · 연락처는 Apps Script 로 보내져 구글 시트 '상담' 탭에 쌓여요.
   카카오톡 채널이 생기면 KAKAO 에 1:1 채팅 링크(https://pf.kakao.com/_xxxxx/chat)를 넣으면
   한국어 페이지에 "카카오톡으로 상담하기" 버튼이 보여요.
   ===================================================================== */
(function () {
  var API = 'https://script.google.com/macros/s/AKfycbxmSmlmpWncaSchQgttNbCoqv7g3kaGwrdwCcmeqUxUf2DQaEoI_VnuC5QMCdn7ee9Wsw/exec'; // checkout.html 의 ORDER_API 와 같음
  var KAKAO = '';                       // 카카오톡 채널 1:1 채팅 링크 (비워 두면 안 보임)
  var EMAIL = 'hello@theoliveskin.com';

  function lang() { var l = document.documentElement.lang; return l === 'ko' || l === 'ja' ? l : 'en'; }
  function L(o) { return o[lang()] || o.en; }
  var KR_SITE = /\/kr\//.test(location.pathname);

  /* 자주 묻는 질문 — 사이트에 이미 있는 내용만 답해요 */
  var QA = [
    { id: 'price',
      q: { en: 'How much is it?', ko: '가격이 얼마예요?', ja: '価格はいくらですか？' },
      k: ['price', 'cost', 'how much', '가격', '얼마', '금액', '価格', '値段', 'いくら'],
      a: KR_SITE
        ? { ko: 'Glow Drop 15ml 한 병 <b>16,000원</b>이고, <b>배송비는 무료</b>예요.', en: 'Glow Drop 15ml is <b>₩16,000</b> with <b>free shipping</b> in Korea.', ja: 'Glow Drop 15mlは<b>16,000ウォン</b>、韓国内は<b>送料無料</b>です。' }
        : { en: 'Glow Drop 15ml is <b>$18 USD</b>. Shipping depends on your country and quantity, and it is <b>free on orders of $30+</b> (two bottles or more).', ko: 'Glow Drop 15ml 한 병 <b>$18</b>이에요. 배송비는 나라와 수량에 따라 정해지고, <b>$30 이상</b>(두 병부터) 주문하면 무료예요.', ja: 'Glow Drop 15mlは<b>18ドル</b>です。送料は国と数量で決まり、<b>30ドル以上</b>（2本から）で無料です。' },
      go: '#shop' },
    { id: 'how',
      q: { en: 'How do I use it?', ko: '어떻게 써요?', ja: '使い方は？' },
      k: ['how to', 'use', 'apply', 'drop', '사용', '쓰', '바르', '방법', '使い', '塗'],
      a: { en: 'Put one or two drops on nails, cuticles or any dry area, press it in and massage in small circles until absorbed. Use it at least once a day, morning or before bed.', ko: '손톱 · 큐티클 · 건조한 곳에 한두 방울 올리고, 지그시 눌러 작은 원을 그리며 흡수될 때까지 마사지해 주세요. 아침이나 잠들기 전, 하루 한 번 이상 쓰면 좋아요.', ja: '爪・甘皮・乾燥が気になる所に1〜2滴のせ、やさしく押し込み、小さな円を描くようになじませます。朝や寝る前に1日1回以上がおすすめです。' } },
    { id: 'ingr',
      q: { en: "What's in it?", ko: '성분이 뭐예요?', ja: '成分は？' },
      k: ['ingredient', 'olive', 'avocado', 'inci', '성분', '올리브', '아보카도', '전성분', '成分', 'オリーブ'],
      a: { en: 'Cold-pressed <b>olive oil</b> and <b>avocado oil</b> at the base. It also contains fragrance; the full ingredient list is in the Ingredients section of the product.', ko: '<b>콜드프레스 올리브 오일</b>과 <b>아보카도 오일</b>이 베이스예요. 향료가 들어 있고, 전성분과 알레르기 유발 성분은 제품 영역의 "성분"에서 볼 수 있어요.', ja: '<b>コールドプレスのオリーブオイル</b>と<b>アボカドオイル</b>がベースです。香料を含み、全成分は商品の「成分」でご覧いただけます。' },
      go: '#ingredients' },
    { id: 'where',
      q: { en: 'Where can I use it?', ko: '어디에 써요?', ja: 'どこに使えますか？' },
      k: ['where', 'nail', 'cuticle', 'elbow', 'heel', 'knee', 'hand', '어디', '손톱', '큐티클', '팔꿈치', '뒤꿈치', '무릎', '손', 'どこ', '爪', 'ひじ'],
      a: { en: 'Nails, cuticles, hands, elbows, knees and heels: anywhere that feels dry.', ko: '손톱, 큐티클, 손, 팔꿈치, 무릎, 뒤꿈치까지, 건조한 곳 어디든 쓸 수 있어요.', ja: '爪、甘皮、手、ひじ、ひざ、かかとなど、乾燥が気になる所ならどこでも。' } },
    { id: 'sensitive',
      q: { en: 'Is it OK for sensitive skin?', ko: '민감한 피부도 괜찮아요?', ja: '敏感肌でも大丈夫？' },
      k: ['sensitive', 'allerg', 'irritat', '민감', '알레르기', '트러블', '자극', '敏感', 'アレルギー'],
      a: { en: 'It contains fragrance, and the fragrance allergens are listed with the ingredients. If your skin is sensitive, try a little on a small area first, and stop if it gets irritated.', ko: '향료가 들어 있고, 향료 속 알레르기 유발 성분은 전성분 아래에 적어 두었어요. 피부가 민감하다면 작은 부위에 먼저 조금 발라 보고, 자극이 느껴지면 사용을 멈춰 주세요.', ja: '香料を含み、香料アレルゲンは成分表に記載しています。敏感肌の方はまず小さな範囲でお試しいただき、刺激を感じたら使用を中止してください。' } },
    { id: 'pay',
      q: { en: 'How can I pay?', ko: '결제는 어떻게 해요?', ja: '支払い方法は？' },
      k: ['pay', 'card', 'paypal', '결제', '카드', '계좌', '페이', '支払', 'カード'],
      a: KR_SITE
        ? { ko: '"바로 구매하기"를 누르고 주문서를 쓰면 페이앱으로 <b>카드 · 계좌이체 · 간편결제</b>를 할 수 있어요.', en: 'Tap "Buy now", fill in the order form, then pay by card, bank transfer or easy pay through PayApp.', ja: '「今すぐ購入」から注文書を入力し、PayAppでカード・振込・簡単決済ができます。' }
        : { en: 'Tap "Buy now" and pay securely with <b>PayPal or a card</b>. It ships from Korea by tracked international mail.', ko: '"바로 구매하기"를 누르면 <b>PayPal이나 카드</b>로 안전하게 결제할 수 있어요. 한국에서 추적 가능한 국제우편으로 보내요.', ja: '「今すぐ購入」から<b>PayPalまたはカード</b>で安全にお支払いいただけます。韓国から追跡可能な国際郵便でお届けします。' },
      go: '#shop' },
    { id: 'wholesale',
      q: { en: 'Do you sell wholesale?', ko: '네일샵 도매도 돼요?', ja: '卸売はできますか？' },
      k: ['wholesale', 'salon', 'bulk', 'b2b', '도매', '네일샵', '살롱', '대량', '卸', 'サロン'],
      a: KR_SITE
        ? { ko: '네. 네일샵 · 살롱은 <b>10병 단위</b>로 한 병 <b>7,000원</b>, <b>50병 이상</b>이면 한 병 <b>6,000원</b>이에요.', en: 'Yes. Salons order in sets of 10: ₩7,000 a bottle, or ₩6,000 from 50 bottles.', ja: 'はい。サロン向けは10本単位で1本7,000ウォン、50本以上は1本6,000ウォンです。' }
        : { en: 'Yes. Leave your salon name and contact below and we will send wholesale details.', ko: '네. 아래 "상담 남기기"에 샵 이름과 연락처를 남겨 주시면 도매 안내를 보내 드려요.', ja: 'はい。下の「相談を残す」にサロン名と連絡先をお書きください。卸売のご案内をお送りします。' },
      go: KR_SITE ? 'checkout.html?type=b2b' : '' },
    { id: 'maker',
      q: { en: 'Who makes it?', ko: '누가 만들어요?', ja: '製造元は？' },
      k: ['maker', 'made', 'cosmax', 'factory', '제조', '만들', '코스맥스', '製造', 'コスマックス'],
      a: { en: 'Made by <b>Mix and Match</b>, the nail care division of COSMAX, to global beauty brand standards.', ko: '코스맥스의 네일 케어 전문 계열사 <b>믹스앤매치</b>에서 글로벌 뷰티 브랜드와 같은 기준으로 만들어요.', ja: 'COSMAXのネイル専門部門<b>Mix and Match</b>が、グローバルブランドと同じ基準で製造しています。' } }
  ];

  var T = {
    fab: { en: 'Ask us', ko: '상담하기', ja: '相談する' },
    title: { en: 'Olive Skin', ko: '올리브 스킨', ja: 'オリーブスキン' },
    sub: { en: 'Quick answers, or leave a message', ko: '자주 묻는 질문 · 1:1 상담', ja: 'よくある質問・1:1相談' },
    hi: { en: 'Hi! This is Olive Skin. Pick a question below, or leave a message and we will reply personally.', ko: '안녕하세요, 올리브 스킨이에요.<br>궁금한 걸 골라 주시거나, 상담을 남겨 주시면 직접 답해 드릴게요.', ja: 'こんにちは、オリーブスキンです。下から質問を選ぶか、相談を残していただければ直接お返事します。' },
    next: { en: 'Anything else? Pick below.', ko: '다른 것도 궁금하면 아래에서 골라 주세요.', ja: 'ほかにも気になることがあれば下からどうぞ。' },
    more: { en: 'See it on the page', ko: '페이지에서 보기', ja: 'ページで見る' },
    leave: { en: 'Leave a message', ko: '상담 남기기', ja: '相談を残す' },
    kakao: { en: 'Chat on KakaoTalk', ko: '카카오톡으로 상담하기', ja: 'カカオトークで相談' },
    mail: { en: 'Email us', ko: '이메일 보내기', ja: 'メールする' },
    unknown: { en: "We don't have a ready answer for that. Leave your email or phone and we will reply personally.", ko: '그 질문은 바로 답하기 어려워요. 연락처를 남겨 주시면 담당자가 직접 답해 드릴게요.', ja: 'その質問にはすぐにお答えできません。連絡先を残していただければ担当者から直接ご連絡します。' },
    formQ: { en: 'Your question', ko: '문의 내용', ja: 'ご相談内容' },
    formC: { en: 'Email or phone', ko: '휴대폰 번호 또는 이메일', ja: 'メールまたは電話番号' },
    send: { en: 'Send', ko: '보내기', ja: '送信' },
    sent: { en: 'Thanks! We got your message and will reply soon.', ko: '접수됐어요! 확인하는 대로 남겨 주신 연락처로 답해 드릴게요.', ja: '受け付けました。確認しだい、ご連絡先へお返事します。' },
    fail: { en: "Couldn't send it. Please email us instead.", ko: '전송이 안 됐어요. 이메일로 보내 주세요.', ja: '送信できませんでした。メールでお送りください。' },
    needC: { en: 'Please add an email or phone so we can reply.', ko: '답을 드릴 연락처를 적어 주세요.', ja: 'ご返信先の連絡先をご記入ください。' },
    type: { en: 'Type a question', ko: '궁금한 걸 적어 주세요', ja: '質問を入力' },
    close: { en: 'Close', ko: '닫기', ja: '閉じる' }
  };

  var root = document.createElement('div');
  root.className = 'osc';
  document.body.appendChild(root);
  var fab, panel, log, form, input, started = false, lastLang = '';

  var ICON = {
    chat: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/></svg>',
    x: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    send: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    kk: '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3C6.5 3 2 6.6 2 11c0 2.8 1.9 5.3 4.7 6.7l-1 3.6c-.1.3.3.6.6.4l4.2-2.8c.5.1 1 .1 1.5.1 5.5 0 10-3.6 10-8S17.5 3 12 3Z"/></svg>'
  };

  function build() {
    lastLang = lang(); started = false;
    root.innerHTML =
      '<button class="osc-fab" type="button" aria-expanded="false" aria-controls="oscPanel">' +
        '<span class="i-open">' + ICON.chat + '</span><span class="i-close">' + ICON.x + '</span>' +
        '<span class="osc-fl">' + L(T.fab) + '</span></button>' +
      '<div class="osc-panel" id="oscPanel" role="dialog" aria-label="' + L(T.title) + '" hidden>' +
        '<div class="osc-hd"><i aria-hidden="true">os</i><div><b>' + L(T.title) + '</b><small>' + L(T.sub) + '</small></div>' +
          '<button type="button" class="osc-x" aria-label="' + L(T.close) + '">' + ICON.x + '</button></div>' +
        '<div class="osc-log" aria-live="polite"></div>' +
        '<form class="osc-in"><input type="text" name="q" autocomplete="off" maxlength="300" placeholder="' + L(T.type) + '" aria-label="' + L(T.type) + '">' +
          '<button type="submit" aria-label="' + L(T.send) + '">' + ICON.send + '</button></form>' +
      '</div>';
    fab = root.querySelector('.osc-fab'); panel = root.querySelector('.osc-panel'); log = root.querySelector('.osc-log');
    form = root.querySelector('.osc-in'); input = form.q;
    fab.onclick = function () { open(panel.hidden); };
    root.querySelector('.osc-x').onclick = function () { open(false); fab.focus(); };
    form.onsubmit = function (e) {
      e.preventDefault();
      var q = input.value.trim(); if (!q) return;
      input.value = ''; ask(q);
    };
  }

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function add(cls, html) { var d = document.createElement('div'); d.className = 'osc-m ' + cls; d.innerHTML = html; log.appendChild(d); return d; }
  function clearChips() { log.querySelectorAll('.osc-chips, .osc-next').forEach(function (c) { c.remove(); }); }

  function humanButtons(w) {
    var leave = document.createElement('button'); leave.type = 'button'; leave.className = 'osc-human'; leave.textContent = L(T.leave);
    leave.onclick = function () { clearChips(); contactForm(''); };
    w.appendChild(leave);
    if (KAKAO && lang() === 'ko') {
      var k = document.createElement('a'); k.className = 'osc-human kk'; k.href = KAKAO; k.target = '_blank'; k.rel = 'noopener';
      k.innerHTML = ICON.kk + L(T.kakao); w.appendChild(k);
    }
  }
  function chips() {
    var w = add('osc-chips', '');
    QA.forEach(function (x) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = L(x.q);
      b.onclick = function () { ask(L(x.q), x); }; w.appendChild(b);
    });
    humanButtons(w);
  }
  function match(q) {
    var s = q.toLowerCase(), best = null, n = 0;
    QA.forEach(function (x) { var c = x.k.filter(function (k) { return s.indexOf(k) > -1; }).length; if (c > n) { n = c; best = x; } });
    return best;
  }
  function ask(q, x) {
    clearChips();
    var me = add('me', esc(q));
    x = x || match(q);
    setTimeout(function () {
      if (x) {
        var more = x.go ? '<br><a class="osc-go" href="' + x.go + '">' + L(T.more) + ' →</a>' : '';
        add('bot', L(x.a) + more);
        add('bot osc-next', L(T.next));
        chips();
      } else {
        add('bot', L(T.unknown));
        contactForm(q);
      }
      log.scrollTop = me.offsetTop - log.offsetTop - 12;
    }, 260);
  }

  /* 1:1 상담 남기기 — Apps Script 'chat' 으로 보내 구글 시트 '상담' 탭에 저장 */
  function contactForm(q) {
    var f = document.createElement('form'); f.className = 'osc-m bot osc-form';
    f.innerHTML =
      '<label>' + L(T.formQ) + '<textarea name="q" rows="3" maxlength="600" required>' + esc(q) + '</textarea></label>' +
      '<label>' + L(T.formC) + '<input name="c" maxlength="120" autocomplete="email" required></label>' +
      '<div class="osc-row"><button type="submit" class="osc-human">' + L(T.send) + '</button>' +
      '<a class="osc-mail" href="mailto:' + EMAIL + '">' + L(T.mail) + '</a></div>';
    log.appendChild(f);
    log.scrollTop = log.scrollHeight;
    f.onsubmit = function (e) {
      e.preventDefault();
      var question = f.q.value.trim(), contact = f.c.value.trim();
      if (!question) return;
      if (!contact) { f.c.focus(); f.c.setCustomValidity(L(T.needC)); f.c.reportValidity(); return; }
      var btn = f.querySelector('button'); btn.disabled = true;
      var body = JSON.stringify({ action: 'chat', question: question, contact: contact, lang: lang(), page: location.href });
      fetch(API, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: body })
        .then(function (r) { return r.json(); })
        .then(function (r) { if (!r || !r.ok) throw new Error('fail'); f.remove(); add('bot', L(T.sent)); chips(); log.scrollTop = log.scrollHeight; })
        .catch(function () {
          btn.disabled = false;
          add('bot', L(T.fail) + '<br><a class="osc-go" href="mailto:' + EMAIL + '?subject=' + encodeURIComponent('Olive Skin') + '&body=' + encodeURIComponent(question + '\n\n' + contact) + '">' + EMAIL + '</a>');
          log.scrollTop = log.scrollHeight;
        });
    };
    f.c.oninput = function () { f.c.setCustomValidity(''); };
  }

  function open(v) {
    if (v && lastLang !== lang()) { build(); }
    panel.hidden = !v; fab.setAttribute('aria-expanded', v); root.classList.toggle('on', v);
    if (v && !started) { started = true; add('bot', L(T.hi)); chips(); }
    if (v && window.matchMedia('(min-width:681px)').matches) input.focus();
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && panel && !panel.hidden) { open(false); fab.focus(); } });
  /* 언어(EN/JA) 를 바꾸면 버튼 글씨도 바꿈 */
  new MutationObserver(function () { if (panel.hidden && lastLang !== lang()) build(); }).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });

  build();
})();
