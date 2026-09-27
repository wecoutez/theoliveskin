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
rep('<div class="buy">', '<label class="phone-row" style="display:flex;align-items:center;gap:14px;font-size:13px;margin:14px 0">휴대폰 번호'
    ' <input id="buyer-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="010-0000-0000" required'
    ' style="flex:1;max-width:220px;font:inherit;padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:#fff"></label>\n        <div class="buy">')
rep('<button type="button" class="pill" id="add-bag" data-i18n="addBag">Add to bag</button>',
    '<button type="button" class="pill" id="add-bag" data-i18n="addBag" style="display:none">Add to bag</button>')
rep("buy.href = 'checkout.html?qty=' + qty + '&lang=' + current;", "buy.href = '#shop';")
# 구매 버튼 → 페이앱 결제창 (수량만큼 금액, 배송지 요청)
rep("  var toast = document.getElementById('toast'), timer;", '''  buy.addEventListener('click', function(ev){
    ev.preventDefault();
    var ph = document.getElementById('buyer-phone'), num = ph.value.replace(/[^0-9]/g, '');
    if(!/^01[0-9]{8,9}$/.test(num)){ ph.focus(); ph.setCustomValidity('휴대폰 번호를 정확히 입력해 주세요'); ph.reportValidity(); return; }
    ph.setCustomValidity('');
    if(!window.PayApp){ alert('결제창을 불러오지 못했어요. 새로고침 후 다시 시도해 주세요.'); return; }
    PayApp.setDefault('userid', PAYAPP_USERID);
    PayApp.setDefault('shopname', PAYAPP_SHOP);
    PayApp.setParam('goodname', 'Glow Drop 글로우드롭 15ml x ' + qty)
      .setParam('price', String(qty * PRICE_WON))
      .setParam('recvphone', num)
      .setParam('reqaddr', '1')
      .setParam('smsuse', 'n')
      .payrequest();
  });
  document.getElementById('buyer-phone').addEventListener('input', function(){ this.setCustomValidity(''); });

  var toast = document.getElementById('toast'), timer;''')
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
