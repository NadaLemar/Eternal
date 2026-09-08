document.addEventListener('DOMContentLoaded', async () => {
  const list = document.getElementById('q-list');
  const searchInput = document.getElementById('q-search');
  const catButtons = document.querySelectorAll('#q-category .chip');
  const countEl = document.getElementById('q-count');

  const quests = await EterCommon.loadJSON('data/quests.json');
  const state = { q: '', cat: '' };

  const badgeClass = { '메인': 'main', '서브': 'olive', '일일': 'daily', '이벤트': 'event' };

  function matches(item) {
    if (state.cat && item.category !== state.cat) return false;
    if (state.q) {
      const hay = `${item.name} ${item.region} ${item.giver}`.toLowerCase();
      if (!hay.includes(state.q)) return false;
    }
    return true;
  }

  function row(q) {
    const rewardBits = [];
    if (q.rewards.exp) rewardBits.push(`경험치 ${EterCommon.fmt(q.rewards.exp)}`);
    if (q.rewards.el) rewardBits.push(`El ${EterCommon.fmt(q.rewards.el)}`);
    if (q.rewards.items && q.rewards.items.length) rewardBits.push(q.rewards.items.join(', '));

    return `
      <div class="qa-row">
        <div class="qa-row__top">
          <span class="badge badge--${badgeClass[q.category] || 'olive'}">${q.category}</span>
          <span class="qa-row__title">${EterCommon.escapeHtml(q.name)}</span>
          <span class="badge">Lv.${q.levelReq}+</span>
        </div>
        <div class="qa-row__desc">${EterCommon.escapeHtml(q.description)}</div>
        <div class="qa-row__desc"><strong style="color:var(--paper-dim)">진행 조건 —</strong> ${q.objectives.map(EterCommon.escapeHtml).join(' → ')}</div>
        <div class="qa-row__foot">
          <span>지역: ${EterCommon.escapeHtml(q.region)}</span>
          <span>의뢰인: ${EterCommon.escapeHtml(q.giver)}</span>
          <span>보상: ${rewardBits.join(' · ') || '—'}</span>
        </div>
      </div>
    `;
  }

  function render() {
    const filtered = quests.filter(matches);
    countEl.textContent = `${filtered.length} / ${quests.length}건`;
    list.innerHTML = filtered.length
      ? filtered.map(row).join('')
      : `<div class="empty-state"><strong>조건에 맞는 퀘스트가 없습니다</strong>검색어나 카테고리를 조정해보세요.</div>`;
  }

  searchInput.addEventListener('input', EterCommon.debounce((e) => {
    state.q = e.target.value.trim().toLowerCase();
    render();
  }));
  catButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      catButtons.forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      state.cat = btn.dataset.cat;
      render();
    });
  });

  render();
});
