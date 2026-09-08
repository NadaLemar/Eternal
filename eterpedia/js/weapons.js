document.addEventListener('DOMContentLoaded', async () => {
  const grid = document.getElementById('w-grid');
  const searchInput = document.getElementById('w-search');
  const cat1Select = document.getElementById('w-cat1');
  const typeSelect = document.getElementById('w-type');
  const gradeSelect = document.getElementById('w-grade');
  const countEl = document.getElementById('w-count');

  const weapons = await EterCommon.loadJSON('data/weapons.json');

  // 필터 옵션 자동 생성
  const cat1List = [...new Set(weapons.map(w => w.category1).filter(Boolean))].sort();
  const types = [...new Set(weapons.map(w => w.type).filter(Boolean))].sort();
  const grades = [...new Set(weapons.map(w => w.grade).filter(g => g != null))].sort((a, b) => b - a);
  cat1List.forEach(c => cat1Select.insertAdjacentHTML('beforeend', `<option value="${c}">${c}</option>`));
  types.forEach(t => typeSelect.insertAdjacentHTML('beforeend', `<option value="${t}">${t}</option>`));
  grades.forEach(g => gradeSelect.insertAdjacentHTML('beforeend', `<option value="${g}">등급 ${g}</option>`));

  const state = { q: '', cat1: '', type: '', grade: '' };

  function matches(w) {
    if (state.q && !w.name.toLowerCase().includes(state.q)) return false;
    if (state.cat1 && w.category1 !== state.cat1) return false;
    if (state.type && w.type !== state.type) return false;
    if (state.grade && String(w.grade) !== state.grade) return false;
    return true;
  }

  function statBlock(p, label) {
    if (!p) return '';
    const featureHtml = p.features && p.features.length
      ? `<div class="card__foot">${p.features.map(EterCommon.escapeHtml).join(' · ')}</div>`
      : '';
    return `
      <div style="border-top:1px solid var(--line); padding-top:8px; margin-top:2px;">
        ${label ? `<div style="font-family:var(--font-mono); font-size:11px; color:var(--olive); margin-bottom:6px;">${label}</div>` : ''}
        <dl class="card__stats" style="border-top:none; padding-top:0;">
          <div class="stat-row"><dt>공격력</dt><dd>${p.power != null ? EterCommon.fmt(p.power) : '—'}</dd></div>
          <div class="stat-row"><dt>연사속도</dt><dd>${p.fireRate || '—'}</dd></div>
          <div class="stat-row"><dt>치명</dt><dd>${p.crit != null ? p.crit : '—'}</dd></div>
          <div class="stat-row"><dt>명중</dt><dd>${p.accuracy != null ? p.accuracy : '—'}</dd></div>
          <div class="stat-row"><dt>탄착</dt><dd>${p.loadRate != null ? p.loadRate : '—'}</dd></div>
          <div class="stat-row"><dt>탄환</dt><dd>${p.ammo.length ? p.ammo.join(', ') : '—'}</dd></div>
          ${p.shotCount != null ? `<div class="stat-row"><dt>발수</dt><dd>${p.shotCount}</dd></div>` : ''}
        </dl>
        ${featureHtml}
      </div>
    `;
  }

  function card(w) {
    const badges = [
      w.category1 ? `<span class="badge badge--illegal">${EterCommon.escapeHtml(w.category1)}</span>` : '',
      w.grade != null ? `<span class="badge badge--grade">등급 ${w.grade}</span>` : '',
      w.type ? `<span class="badge">${EterCommon.escapeHtml(w.type)}</span>` : '',
      w.size ? `<span class="badge">${EterCommon.escapeHtml(w.size)}</span>` : '',
    ].filter(Boolean).join('');

    return `
      <article class="card">
        <div class="card__head">
          <div>
            <div class="card__title">${EterCommon.escapeHtml(w.name)}</div>
            <div class="card__meta">${w.type || ''}${w.grade != null ? ' · 등급 ' + w.grade : ''}${w.size ? ' · ' + w.size : ''}${w.weight ? ' · 무게 ' + w.weight : ''}</div>
          </div>
        </div>
        <div class="card__badges">${badges}</div>
        ${statBlock(w.primary, w.secondary ? '1차 공격' : '')}
        ${w.secondary ? statBlock(w.secondary, '2차 공격') : ''}
      </article>
    `;
  }

  function render() {
    const filtered = weapons.filter(matches);
    countEl.textContent = `${filtered.length} / ${weapons.length}건`;
    grid.innerHTML = filtered.length
      ? filtered.map(card).join('')
      : `<div class="empty-state"><strong>조건에 맞는 무기가 없습니다</strong>검색어나 필터를 조정해보세요.</div>`;
  }

  searchInput.addEventListener('input', EterCommon.debounce((e) => {
    state.q = e.target.value.trim().toLowerCase();
    render();
  }));
  cat1Select.addEventListener('change', (e) => { state.cat1 = e.target.value; render(); });
  typeSelect.addEventListener('change', (e) => { state.type = e.target.value; render(); });
  gradeSelect.addEventListener('change', (e) => { state.grade = e.target.value; render(); });

  render();
});
