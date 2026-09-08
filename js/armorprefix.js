document.addEventListener('DOMContentLoaded', async () => {
  const tabsEl = document.getElementById('prefix-tabs');
  const listEl = document.getElementById('prefix-list');
  if (!tabsEl) return;

  const prefixes = await EterCommon.loadJSON('data/armor_prefixes.json');
  const targets = [...new Set(prefixes.map(p => p.target))];

  let activeTarget = targets[0];

  function card(p) {
    return `
      <div class="cat-card" style="min-height:auto;">
        <div class="card__badges" style="margin-bottom:6px;">
          <span class="badge badge--grade">${EterCommon.escapeHtml(p.prefix)}</span>
          ${p.clOnly ? '<span class="badge badge--cl">CL전용</span>' : ''}
        </div>
        <p style="font-size:13px; color:var(--paper-dim); margin:0 0 8px;">${EterCommon.escapeHtml(p.effect)}</p>
        <div class="card__foot">수치: ${EterCommon.escapeHtml(p.valueStatus)}${p.note ? ' · ' + EterCommon.escapeHtml(p.note) : ''}</div>
      </div>
    `;
  }

  function render() {
    listEl.innerHTML = prefixes.filter(p => p.target === activeTarget).map(card).join('');
  }

  targets.forEach((t, i) => {
    tabsEl.insertAdjacentHTML('beforeend', `<button class="chip${i === 0 ? ' is-active' : ''}" data-target="${t}">${t}</button>`);
  });
  tabsEl.querySelectorAll('.chip').forEach(btn => {
    btn.addEventListener('click', () => {
      tabsEl.querySelectorAll('.chip').forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      activeTarget = btn.dataset.target;
      render();
    });
  });

  render();
});
