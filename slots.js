// 공통 유틸리티 함수 모음
const EterCommon = (() => {
  async function loadJSON(path) {
    try {
      const res = await fetch(path);
      if (!res.ok) throw new Error(`${path} 로드 실패 (${res.status})`);
      return await res.json();
    } catch (err) {
      console.error(err);
      return [];
    }
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function debounce(fn, wait = 180) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), wait);
    };
  }

  function fmt(num) {
    if (typeof num !== 'number') return num;
    return num.toLocaleString('ko-KR');
  }

  return { loadJSON, escapeHtml, debounce, fmt };
})();
