/* Google Analytics 4 — 방문자 수 · 나라별 통계
   GA 에서 받은 측정 ID(G-로 시작)를 아래 따옴표 안에 넣으면 모든 페이지에서 수집 시작.
   비어 있으면 아무것도 하지 않음. */
(function () {
  var GA_ID = 'G-QE0Y0H5B37';
  if (!GA_ID || /[?&]notrack=1/.test(location.search)) return;
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', GA_ID);
})();
