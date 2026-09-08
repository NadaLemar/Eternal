document.addEventListener('DOMContentLoaded', async () => {
  const list = document.getElementById('a-list');
  const searchInput = document.getElementById('a-search');
  const catSelect = document.getElementById('a-category');
  const countEl = document.getElementById('a-count');

  const achievements = await EterCommon.loadJSON('data/achievements.json');
  const state = { q: '', cat: '' };

  const categories = [...new Set(achievements.map(a => a.category))].sort();
  categories.forEach(c => catSelect.insertAdjacentHTML('beforeend', `<option value="${c}">${c}</option>`));

  function matches(item) {
    if (state.cat && item.category !== state.cat) return false;
    if (state.q && !item.name.toLowerCase().includes(state.q)) return false;
    return true;
  }

  function row(a) {
    return `
      <div class="qa-row">
        <div class="qa-row__top">
          <span class="badge badge--grade">${a.points}P</span>
          <span class="qa-row__title">${EterCommon.escapeHtml(a.name)}</span>
          <span class="badge badge--olive">${EterCommon.escapeHtml(a.category)}</span>
        </div>
        <div class="qa-row__desc">${EterCommon.escapeHtml(a.description)}</div>
        <div class="qa-row__foot">
          <span>달성 조건: ${EterCommon.escapeHtml(a.condition)}</span>
          <span>보상: ${EterCommon.escapeHtml(a.reward)}</span>
        </div>
      </div>
    `;
  }

  function render() {
    const filtered = achievements.filter(matches);
    countEl.textContent = `${filtered.length} / ${achievements.length}건`;
    list.innerHTML = filtered.length
      ? filtered.map(row).join('')
      : `<div class="empty-state"><strong>조건에 맞는 업적이 없습니다</strong>검색어나 카테고리를 조정해보세요.</div>`;
  }

  searchInput.addEventListener('input', EterCommon.debounce((e) => {
    state.q = e.target.value.trim().toLowerCase();
    render();
  }));
  catSelect.addEventListener('change', (e) => { state.cat = e.target.value; render(); });

  render();
});
