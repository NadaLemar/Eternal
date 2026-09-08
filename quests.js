// 공통 네비게이션 동작: 모바일 레일 메뉴 토글
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('[data-nav-toggle]');
  const rail = document.querySelector('.rail');
  if (!toggle || !rail) return;

  toggle.addEventListener('click', () => {
    rail.classList.toggle('is-open');
  });

  document.addEventListener('click', (e) => {
    if (!rail.classList.contains('is-open')) return;
    if (rail.contains(e.target) || toggle.contains(e.target)) return;
    rail.classList.remove('is-open');
  });

  rail.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => rail.classList.remove('is-open'));
  });
});
