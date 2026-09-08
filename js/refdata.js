document.addEventListener('DOMContentLoaded', async () => {
  const prefixEl = document.getElementById('prefix-list');
  const uniqueEl = document.getElementById('unique-list');
  if (!prefixEl) return;

  const [prefixes, uniques] = await Promise.all([
    EterCommon.loadJSON('data/armor_prefixes.json'),
    EterCommon.loadJSON('data/weapon_unique_modifiers.json'),
  ]);

  prefixEl.innerHTML = prefixes.map(p => `
    <div style="border-bottom:1px solid var(--line); padding-bottom:6px;">
      <b style="color:var(--paper);">${EterCommon.escapeHtml(p.prefix)}</b>
      ${p.clOnly ? '<span class="badge badge--cl" style="margin-left:6px;">CL전용</span>' : ''}
      <span style="color:var(--muted); font-size:11px;"> · ${EterCommon.escapeHtml(p.target)}</span>
      <div>${EterCommon.escapeHtml(p.effect)}</div>
      <div style="color:var(--muted); font-size:11px;">수치: ${EterCommon.escapeHtml(p.valueStatus)}${p.note ? ' · ' + EterCommon.escapeHtml(p.note) : ''}</div>
    </div>
  `).join('');

  uniqueEl.innerHTML = uniques.map(u => `
    <div style="border-bottom:1px solid var(--line); padding-bottom:6px;">
      <b style="color:var(--paper);">${EterCommon.escapeHtml(u.modifier)}</b>
      <div>${EterCommon.escapeHtml(u.effect)}</div>
      <div style="color:var(--muted); font-size:11px;">적용: ${EterCommon.escapeHtml(u.appliesTo)} · 수치: ${EterCommon.escapeHtml(u.valueStatus)}</div>
    </div>
  `).join('');
});
