document.addEventListener('DOMContentLoaded', async () => {
  const grid = document.getElementById('c-grid');
  const searchInput = document.getElementById('c-search');
  const cat2Select = document.getElementById('c-category2');
  const variantButtons = document.querySelectorAll('#c-variant .chip');
  const countEl = document.getElementById('c-count');

  const raw = await EterCommon.loadJSON('data/costumes.json');

  // baseName 기준으로 variant(공격형/치명형/체력형)를 하나로 묶는다
  const groups = new Map();
  raw.forEach(item => {
    if (!groups.has(item.baseName)) {
      groups.set(item.baseName, {
        baseName: item.baseName,
        category1: item.category1,
        category2: item.category2,
        gender: item.gender,
        weight: item.weight,
        variants: {},
      });
    }
    groups.get(item.baseName).variants[item.variant] = item;
  });
  const items = [...groups.values()];

  const cat2List = [...new Set(items.map(g => g.category2))].sort();
  cat2List.forEach(c => cat2Select.insertAdjacentHTML('beforeend', `<option value="${c}">${c}</option>`));

  const state = { q: '', cat2: '', variant: '' };
  const VARIANT_ORDER = ['공격형', '치명형', '체력형'];

  function matches(g) {
    if (state.cat2 && g.category2 !== state.cat2) return false;
    if (state.variant && !g.variants[state.variant]) return false;
    if (state.q && !g.baseName.toLowerCase().includes(state.q)) return false;
    return true;
  }

  function statTable(item) {
    return `
      <table style="width:100%; border-collapse:collapse; font-family:var(--font-mono); font-size:12px;">
        <thead>
          <tr style="color:var(--muted); text-align:right;">
            <th style="text-align:left; padding:4px 0; border-bottom:1px solid var(--line);">강화</th>
            <th style="padding:4px 0; border-bottom:1px solid var(--line);">방어력%</th>
            <th style="padding:4px 0; border-bottom:1px solid var(--line);">${EterCommon.escapeHtml(item.statLabel)}</th>
            <th style="padding:4px 0; border-bottom:1px solid var(--line);">회피도</th>
          </tr>
        </thead>
        <tbody>
          ${item.levels.map(lv => `
            <tr style="color:var(--paper-dim); text-align:right;">
              <td style="text-align:left; padding:3px 0;">+${lv.stage}</td>
              <td style="padding:3px 0;">${EterCommon.fmt(lv.defensePct)}%</td>
              <td style="padding:3px 0;">${EterCommon.fmt(lv.statValue)}</td>
              <td style="padding:3px 0;">${EterCommon.fmt(lv.evasion)}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  }

  function card(g, idx) {
    const availableVariants = VARIANT_ORDER.filter(v => g.variants[v]);
    const activeVariant = state.variant && g.variants[state.variant] ? state.variant : availableVariants[0];

    const tabs = availableVariants.map(v => `
      <button class="chip ${v === activeVariant ? 'is-active' : ''}" data-group="${idx}" data-tab="${v}" style="font-size:11px; padding:4px 9px;">${v}</button>
    `).join('');

    return `
      <article class="card" data-group-card="${idx}">
        <div class="card__head">
          <div>
            <div class="card__title">${EterCommon.escapeHtml(g.baseName)}</div>
            <div class="card__meta">${EterCommon.escapeHtml(g.category2)} · ${EterCommon.escapeHtml(g.gender)} · 무게 ${g.weight}</div>
          </div>
        </div>
        <div class="card__badges">
          <span class="badge badge--cl">${EterCommon.escapeHtml(g.category1)}</span>
        </div>
        <div class="chip-group" data-tabgroup="${idx}">${tabs}</div>
        <div data-table="${idx}">${statTable(g.variants[activeVariant])}</div>
      </article>
    `;
  }

  function render() {
    const filtered = items.filter(matches);
    countEl.textContent = `${filtered.length} / ${items.length}종`;
    grid.innerHTML = filtered.length
      ? filtered.map((g, i) => card(g, i)).join('')
      : `<div class="empty-state"><strong>조건에 맞는 코스튬이 없습니다</strong>검색어나 필터를 조정해보세요.</div>`;

    // 탭 클릭 이벤트 바인딩 (그룹별 로컬 상태)
    filtered.forEach((g, i) => {
      const tabGroup = grid.querySelector(`[data-tabgroup="${i}"]`);
      if (!tabGroup) return;
      tabGroup.querySelectorAll('.chip').forEach(btn => {
        btn.addEventListener('click', () => {
          tabGroup.querySelectorAll('.chip').forEach(b => b.classList.remove('is-active'));
          btn.classList.add('is-active');
          const variant = btn.dataset.tab;
          grid.querySelector(`[data-table="${i}"]`).innerHTML = statTable(g.variants[variant]);
        });
      });
    });
  }

  searchInput.addEventListener('input', EterCommon.debounce((e) => {
    state.q = e.target.value.trim().toLowerCase();
    render();
  }));
  cat2Select.addEventListener('change', (e) => { state.cat2 = e.target.value; render(); });
  variantButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      variantButtons.forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      state.variant = btn.dataset.variant;
      render();
    });
  });

  render();
});
