// 공용 아이템 그리드: 무기/방어구/악세서리/코스튬 아이템 목록 페이지에서 재사용
const EterItemGrid = (() => {

  const STAT_LABELS = {
    power: '파괴력',
    atkPct: '공격력%',
    defense: '방어력',
    defensePct: '방어력%',
    hp: '체력',
    crit: '치명',
    evasion: '회피',
    stamina: '지구',
    speed: '속도',
    action: '행동',
    numb: '무감',
    loadRate: '탄착',
    accuracy: '명중',
    shotCount: '발수',
    weight: '무게',
    maxEnhancedPower: '최대강화 피해량',
    holdCount: '보유개수',
    dpsPerSecond: '초당 파괴력(추정)',
  };
  const STAT_ORDER = ['power', 'atkPct', 'defense', 'defensePct', 'hp', 'crit', 'evasion',
    'stamina', 'speed', 'action', 'numb', 'accuracy', 'loadRate', 'shotCount',
    'maxEnhancedPower', 'dpsPerSecond', 'weight', 'holdCount'];

  function statList(item) {
    const rows = STAT_ORDER
      .filter(k => item[k] !== undefined && item[k] !== null)
      .map(k => `<div class="stat-row"><dt>${STAT_LABELS[k]}</dt><dd>${EterCommon.fmt(item[k])}${k.includes('Pct') ? '%' : ''}</dd></div>`);
    if (item.size) rows.push(`<div class="stat-row"><dt>크기</dt><dd>${EterCommon.escapeHtml(item.size)}</dd></div>`);
    if (item.fireRate) rows.push(`<div class="stat-row"><dt>발사속도</dt><dd>${EterCommon.escapeHtml(item.fireRate)}</dd></div>`);
    if (item.ammo && item.ammo.length) rows.push(`<div class="stat-row"><dt>탄환</dt><dd>${item.ammo.map(EterCommon.escapeHtml).join(', ')}</dd></div>`);
    return rows.length ? `<dl class="card__stats">${rows.join('')}</dl>` : '';
  }

  function secondaryBlock(item) {
    if (!item.secondary) return '';
    const s = item.secondary;
    return `
      <div style="border-top:1px solid var(--line); padding-top:8px; margin-top:8px;">
        <div style="font-family:var(--font-mono); font-size:11px; color:var(--olive); margin-bottom:6px;">2차 공격</div>
        ${statList(s)}
        ${s.features && s.features.length ? `<div class="card__foot">${s.features.map(EterCommon.escapeHtml).join(' · ')}</div>` : ''}
      </div>
    `;
  }

  function card(item, opts) {
    const badges = [
      item.category1 ? `<span class="badge badge--cl">${EterCommon.escapeHtml(item.category1)}</span>` : '',
      item.illegal ? `<span class="badge badge--illegal">불법</span>` : '',
      item.grade != null ? `<span class="badge badge--grade">등급 ${item.grade}</span>` : '',
      item.type ? `<span class="badge">${EterCommon.escapeHtml(item.type)}</span>` : '',
      item.rangeType ? `<span class="badge badge--olive">${EterCommon.escapeHtml(item.rangeType)}</span>` : '',
    ].filter(Boolean).join('');

    const img = (opts.showImage && item.imageUrl)
      ? `<img src="${item.imageUrl}" alt="" loading="lazy" style="width:40px; height:40px; object-fit:contain; background:var(--panel-raised); border:1px solid var(--line); flex-shrink:0;" onerror="this.style.display='none'">`
      : '';

    return `
      <a class="card card--link" href="item-detail.html?cat=${opts.catKey}&id=${encodeURIComponent(item.id)}">
        <div class="card__head">
          ${img}
          <div>
            <div class="card__title">${EterCommon.escapeHtml(item.name)}</div>
            <div class="card__meta">${item.type || ''}${item.grade != null ? ' · 등급 ' + item.grade : ''}</div>
          </div>
        </div>
        <div class="card__badges">${badges}</div>
        ${statList(item)}
        ${item.features && item.features.length ? `<div class="card__foot">${item.features.map(EterCommon.escapeHtml).join(' · ')}</div>` : ''}
        ${item.weaponSkill ? `<div class="card__foot">무기 스킬: ${EterCommon.escapeHtml(item.weaponSkill)}</div>` : ''}
        ${item.tuningSlots && item.tuningSlots.length ? `<div class="card__foot">튜닝 슬롯: ${item.tuningSlots.map(EterCommon.escapeHtml).join(', ')}</div>` : ''}
        ${item.materialOptions && item.materialOptions.length ? `<div class="card__foot">재질 옵션: ${item.materialOptions.map(EterCommon.escapeHtml).join(', ')}</div>` : ''}
        ${secondaryBlock(item)}
      </a>
    `;
  }

  /**
   * config: {
   *   dataPath, gridId, tabsId, searchId, countId,
   *   tabField, filters: [{id, field, isGrade}], showImage
   * }
   */
  async function mount(config) {
    const grid = document.getElementById(config.gridId);
    const tabsEl = config.tabsId ? document.getElementById(config.tabsId) : null;
    const searchEl = document.getElementById(config.searchId);
    const countEl = document.getElementById(config.countId);
    const filterEls = (config.filters || []).map(f => ({ ...f, el: document.getElementById(f.id) }));

    const items = await EterCommon.loadJSON(config.dataPath);
    const state = { q: '', tab: '', filters: {} };

    // 탭 생성
    if (tabsEl && config.tabField) {
      const values = [...new Set(items.map(it => it[config.tabField]).filter(Boolean))];
      tabsEl.insertAdjacentHTML('beforeend', `<button class="chip is-active" data-tab="">전체</button>`);
      values.forEach(v => tabsEl.insertAdjacentHTML('beforeend', `<button class="chip" data-tab="${v}">${v}</button>`));
      tabsEl.querySelectorAll('.chip').forEach(btn => {
        btn.addEventListener('click', () => {
          tabsEl.querySelectorAll('.chip').forEach(b => b.classList.remove('is-active'));
          btn.classList.add('is-active');
          state.tab = btn.dataset.tab;
          render();
        });
      });
    }

    // 필터 셀렉트 생성
    filterEls.forEach(f => {
      const values = [...new Set(items.map(it => it[f.field]).filter(v => v !== undefined && v !== null))];
      values.sort((a, b) => f.isGrade ? b - a : String(a).localeCompare(String(b)));
      values.forEach(v => f.el.insertAdjacentHTML('beforeend', `<option value="${v}">${f.isGrade ? '등급 ' + v : v}</option>`));
      f.el.addEventListener('change', (e) => { state.filters[f.field] = e.target.value; render(); });
    });

    function matches(it) {
      if (config.tabField && state.tab && it[config.tabField] !== state.tab) return false;
      for (const f of filterEls) {
        const val = state.filters[f.field];
        if (val && String(it[f.field]) !== val) return false;
      }
      if (state.q && !it.name.toLowerCase().includes(state.q)) return false;
      return true;
    }

    function render() {
      const filtered = items.filter(matches);
      if (countEl) countEl.textContent = `${filtered.length} / ${items.length}건`;
      grid.innerHTML = filtered.length
        ? filtered.map(it => card(it, { showImage: config.showImage, catKey: config.catKey })).join('')
        : `<div class="empty-state"><strong>조건에 맞는 항목이 없습니다</strong>검색어나 필터를 조정해보세요.</div>`;
    }

    if (searchEl) {
      searchEl.addEventListener('input', EterCommon.debounce((e) => {
        state.q = e.target.value.trim().toLowerCase();
        render();
      }));
    }

    render();
    return { items, render };
  }

  return { mount, card, statList };
})();
