"""index.html 로 한국어 사이트 kr/index.html 을 만든다.

index.html 을 고친 뒤 이 파일을 다시 실행하면 kr/ 도 같이 바뀜:
    python3 tools/build_kr.py

한국어 사이트는 한국어로 고정, 가격은 원화, 구매는 페이앱 링크로 연결.
"""
from pathlib import Path


RETAIL_URL = ""  # 국내 소매용 페이앱 결제 링크 — 만들면 여기에 넣고 다시 실행 (비어 있으면 구매 버튼은 메일 문의로)
WHOLESALE_URL = "https://www.payapp.kr/L/z4lfT3"  # 국내 도매용(네일샵) 페이앱 결제 링크
PRICE_KRW = "16,000"
SITE = "https://www.theoliveskin.com"

BUY_URL = RETAIL_URL or "mailto:hello@theoliveskin.com?subject=%EA%B8%80%EB%A1%9C%EC%9A%B0%20%EB%93%9C%EB%A1%AD%20%EA%B5%AC%EB%A7%A4%20%EB%AC%B8%EC%9D%98"

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
rep('<div class="qty-row">', '<div class="qty-row" style="display:none">')  # 수량은 페이앱 결제창에서 고름
rep('<button type="button" class="pill" id="add-bag" data-i18n="addBag">Add to bag</button>',
    '<button type="button" class="pill" id="add-bag" data-i18n="addBag" style="display:none">Add to bag</button>')
rep("buy.href = 'checkout.html?qty=' + qty + '&lang=' + current;", "buy.href = BUY_URL;")
if not RETAIL_URL:
    rep('buyNow:"바로 구매하기"', 'buyNow:"구매 문의하기"')
# 푸터 '도매 문의' → 도매 결제 링크
rep('<a href="mailto:hello@theoliveskin.com?subject=Wholesale" data-i18n="wholesale">Wholesale inquiries</a>',
    f'<a href="{WHOLESALE_URL}" data-i18n="wholesale">Wholesale inquiries</a>')
rep('wholesale:"도매 문의"', 'wholesale:"도매 주문 (네일샵·살롱)"')
rep('<a href="checkout.html" data-i18n="checkout">Checkout</a>', f'<a href="{BUY_URL}" data-i18n="checkout">Checkout</a>')
rep("var current = 'en';", f"var current = 'en', BUY_URL = '{BUY_URL}';")

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
