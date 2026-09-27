"""index.html 로 한국어 사이트 kr/index.html 을 만든다.

index.html 을 고친 뒤 이 파일을 다시 실행하면 kr/ 도 같이 바뀜:
    python3 tools/build_kr.py

한국어 사이트는 한국어로 고정, 가격은 원화, 구매는 페이앱 링크로 연결.
"""
from pathlib import Path


PAYAPP_USERID = "krawn"  # 페이앱 판매자 아이디 — 구매 버튼이 페이앱 결제창을 바로 띄움
PAYAPP_SHOP = "Olive Skin 올리브스킨"
PRICE_WON = 16000
WHOLESALE_URL = "https://www.payapp.kr/L/z4lfT3"  # 국내 도매용(네일샵) 페이앱 결제 링크
PRICE_KRW = f"{PRICE_WON:,}"
SITE = "https://www.theoliveskin.com"


root = Path(__file__).resolve().parent.parent
s = (root / "index.html").read_text(encoding="utf-8")


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"index.html 에서 {old[:60]!r} 를 {count}번 찾아야 하는데 {n}번 찾음 — 스크립트를 index.html 에 맞게 고쳐 주세요")
    s = s.replace(old, new)


# 영어 페이지에만 필요한 줄 빼기
rep('\n<link rel="alternate" hreflang="en" href="https://www.theoliveskin.com/">\n<link rel="alternate" hreflang="ko" href="https://www.theoliveskin.com/kr/">', '')  # 영어 페이지용 줄은 빼고 위에서 새로 넣음
rep("  if(start === 'ko'){ location.replace('kr/'); return; }  // 한국어는 /kr 사이트로\n", "")
rep("if(b.dataset.lang === 'ko'){ location.href = 'kr/'; return; } setLang(b.dataset.lang);", "setLang(b.dataset.lang);")

# 문서 언어 · 검색엔진용 주소
rep('<html lang="en">', '<html lang="ko">')
rep('<meta name="description" content="Olive Skin Glow Drop — a healing daily care oil with cold-pressed olive and avocado, inspired by Napa Valley.">',
    '<meta name="description" content="올리브 스킨 글로우 드롭 — 콜드프레스 올리브 오일과 아보카도 오일을 담은 네일 & 바디 케어 오일. 나파 밸리의 올리브 숲에서 영감을 받은 한 방울의 힐링.">\n'
    f'<link rel="canonical" href="{SITE}/kr/">\n'
    f'<link rel="alternate" hreflang="en" href="{SITE}/">\n'
    f'<link rel="alternate" hreflang="ko" href="{SITE}/kr/">')

# kr/ 폴더에서 이미지·영상 경로가 맞도록
for attr, n in (("src", 14), ("data-src", 4), ("poster", 1)):
    rep(f' {attr}="images/', f' {attr}="../images/', n)

# 가격 · 구매 — 원화, 페이앱
rep('<p class="price">$18<small>USD</small></p>', f'<p class="price">{PRICE_KRW}<small>원</small></p>')
rep('btnShop:"글로우 드롭 구매하기 — $18"', f'btnShop:"글로우 드롭 구매하기 — {PRICE_KRW}원"')
rep('announce:"전 세계 배송"', 'announce:"국내 배송 · 간편결제"')
rep('<span class="total" id="total">$18.00</span>', f'<span class="total" id="total">{PRICE_KRW}원</span>')
rep("tEl.textContent = '$' + (qty*PRICE).toFixed(2);", "tEl.textContent = (qty*PRICE_WON).toLocaleString('ko-KR') + '원';")
rep('<button type="button" class="pill" id="add-bag" data-i18n="addBag">Add to bag</button>',
    '<button type="button" class="pill" id="add-bag" data-i18n="addBag" style="display:none">Add to bag</button>')
rep("buy.href = 'checkout.html?qty=' + qty + '&lang=' + current;", "buy.href = '#shop';")
# 구매 버튼 → 주문 확인 창(수량·금액·휴대폰 번호) → 페이앱 결제창 (배송지 요청)
ORDER_DIALOG = """
<dialog id="order" class="order-sheet" aria-labelledby="order-h">
  <form method="dialog" id="order-form" novalidate>
    <p class="tag">Olive Skin · 주문 확인</p>
    <h3 id="order-h">Glow Drop 15ml</h3>
    <dl class="order-sum">
      <div><dt>수량</dt><dd id="o-qty">1개</dd></div>
      <div><dt>결제 금액</dt><dd id="o-total">PRICE_KRW원</dd></div>
    </dl>
    <label class="o-field">휴대폰 번호
      <input id="buyer-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="010-0000-0000" required>
      <small>결제 안내와 배송 연락에만 사용합니다.</small>
    </label>
    <p class="o-err" id="o-err" role="alert" hidden>휴대폰 번호를 정확히 입력해 주세요.</p>
    <div class="o-actions">
      <button type="button" class="pill ghost" id="o-cancel">닫기</button>
      <button type="submit" class="pill primary" id="o-pay">결제하기</button>
    </div>
    <p class="o-note">다음 화면(페이앱)에서 배송지와 결제 수단을 입력합니다.</p>
  </form>
</dialog>
<style>
.order-sheet{border:0;padding:0;border-radius:20px;width:min(420px,calc(100vw - 32px));background:var(--bg);color:var(--ink);box-shadow:0 30px 80px -20px rgba(20,20,14,.45)}
.order-sheet::backdrop{background:rgba(20,20,14,.45);backdrop-filter:blur(2px)}
.order-sheet form{padding:28px 28px 22px;display:grid;gap:16px}
.order-sheet .tag{font-size:12px;font-weight:500;letter-spacing:.12em;color:var(--ink-soft)}
.order-sheet h3{font-family:var(--display);font-weight:400;font-size:34px;line-height:1;margin:-6px 0 0}
.order-sum{margin:0;border-block:1px solid var(--line);padding:12px 0;display:grid;gap:6px;font-size:15px}
.order-sum div{display:flex;justify-content:space-between}
.order-sum dt{color:var(--ink-soft)}
.order-sum dd{margin:0;font-variant-numeric:tabular-nums}
#o-total{font-weight:500;color:var(--olive)}
.o-field{display:grid;gap:8px;font-size:15px;font-weight:500}
.o-field input{font:inherit;font-weight:400;padding:13px 18px;border:1px solid var(--line);border-radius:999px;background:#fff}
.o-field input:focus{outline:2px solid var(--olive);outline-offset:1px}
.o-field small{font-size:13px;font-weight:400;color:var(--ink-soft)}
.o-err{font-size:14px;color:#9B3B2E;margin:-6px 0 0}
.o-actions{display:grid;grid-template-columns:1fr 2fr;gap:10px}
.o-actions .pill{min-height:52px;width:100%}
.o-note{font-size:13px;color:var(--ink-soft);text-align:center}
</style>
"""
rep("  var toast = document.getElementById('toast'), timer;", """  var dlg = document.getElementById('order'), ph = document.getElementById('buyer-phone'), oErr = document.getElementById('o-err');
  buy.addEventListener('click', function(ev){
    ev.preventDefault();
    document.getElementById('o-qty').textContent = qty + '개';
    document.getElementById('o-total').textContent = (qty*PRICE_WON).toLocaleString('ko-KR') + '원';
    oErr.hidden = true;
    if(dlg.showModal) dlg.showModal(); else dlg.setAttribute('open','');
    setTimeout(function(){ ph.focus(); }, 50);
  });
  document.getElementById('o-cancel').addEventListener('click', function(){ dlg.close(); });
  ph.addEventListener('input', function(){ oErr.hidden = true; });
  document.getElementById('order-form').addEventListener('submit', function(ev){
    ev.preventDefault();
    var num = ph.value.replace(/[^0-9]/g, '');
    if(!/^01[0-9]{8,9}$/.test(num)){ oErr.hidden = false; ph.focus(); return; }
    if(!window.PayApp){ oErr.textContent = '결제창을 불러오지 못했어요. 새로고침 후 다시 시도해 주세요.'; oErr.hidden = false; return; }
    dlg.close();
    PayApp.setDefault('userid', PAYAPP_USERID);
    PayApp.setDefault('shopname', PAYAPP_SHOP);
    PayApp.setParam('goodname', 'Glow Drop 글로우드롭 15ml x ' + qty)
      .setParam('price', String(qty * PRICE_WON))
      .setParam('recvphone', num)
      .setParam('reqaddr', '1')
      .setParam('smsuse', 'n')
      .payrequest();
  });

  var toast = document.getElementById('toast'), timer;""")
rep('<footer', ORDER_DIALOG.replace('PRICE_KRW', PRICE_KRW) + '<footer')
rep('</body>', '<script src="https://lite.payapp.kr/public/api/v2/payapp-lite.js"></script>\n</body>')
rep('m4:"PayPal · 카드 결제"', 'm4:"페이앱 · 카드 · 계좌이체 · 간편결제"')
# 푸터 '도매 문의' → 도매 결제 링크
rep('<a href="mailto:hello@theoliveskin.com?subject=Wholesale" data-i18n="wholesale">Wholesale inquiries</a>',
    f'<a href="{WHOLESALE_URL}" data-i18n="wholesale">Wholesale inquiries</a>')
rep('wholesale:"도매 문의"', 'wholesale:"도매 주문 (네일샵·살롱)"')
rep('<a href="checkout.html" data-i18n="checkout">Checkout</a>', '<a href="#shop" data-i18n="checkout">Checkout</a>')
rep("var current = 'en';", f"var current = 'en', PAYAPP_USERID = '{PAYAPP_USERID}', PAYAPP_SHOP = '{PAYAPP_SHOP}', PRICE_WON = {PRICE_WON};")

# 언어: 한국어 고정, EN/JA 는 영어 사이트로 이동
rep("document.querySelectorAll('.lang button').forEach(function(b){ b.addEventListener('click', function(){ setLang(b.dataset.lang); }); });",
    "document.querySelectorAll('.lang button').forEach(function(b){ b.addEventListener('click', function(){ if(b.dataset.lang !== 'ko') location.href = '../?lang=' + b.dataset.lang; }); });")
rep("""  var start = 'en';
  try{ start = localStorage.getItem('os-lang') || 'en'; }catch(e){}
  var q = new URLSearchParams(location.search).get('lang');
  if(q) start = q;""", "  var start = 'ko';")

out = root / "kr" / "index.html"
rep("<!DOCTYPE html>\n", "<!DOCTYPE html>\n<!-- 자동 생성 파일: 직접 고치지 말고 index.html 을 고친 뒤 python3 tools/build_kr.py 실행 -->\n")
out.write_text(s, encoding="utf-8")
print("wrote", out.relative_to(root))
