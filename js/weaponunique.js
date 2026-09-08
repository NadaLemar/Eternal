document.addEventListener('DOMContentLoaded', async () => {
  const listEl = document.getElementById('unique-list');
  if (!listEl) return;

  const uniques = await EterCommon.loadJSON('data/weapon_unique_modifiers.json');

  listEl.innerHTML = uniques.map(u => `
    <div class="cat-card" style="min-height:auto;">
      <div class="card__badges" style="margin-bottom:6px;">
        <span class="badge badge--grade">${EterCommon.escapeHtml(u.modifier)}</span>
      </div>
      <p style="font-size:13px; color:var(--paper-dim); margin:0 0 8px;">${EterCommon.escapeHtml(u.effect)}</p>
      <div class="card__foot">적용: ${EterCommon.escapeHtml(u.appliesTo)} · 수치: ${EterCommon.escapeHtml(u.valueStatus)}</div>
    </div>
  `).join('');
});
