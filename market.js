document.addEventListener('DOMContentLoaded', async () => {
  const ringGroup = document.getElementById('rm-ring');
  const handEl = document.getElementById('rm-hand');
  const noteEl = document.getElementById('rm-note');
  const thead = document.getElementById('rm-thead');
  const tbody = document.getElementById('rm-tbody');

  const data = await EterCommon.loadJSON('data/ring_materials.json');
  const rings = (data && data.rings) || [];
  const colA = (data && data.columnGroups && data.columnGroups.a) || [1, 2, 3, 4, 5];
  const colB = (data && data.columnGroups && data.columnGroups.b) || [0, 1, 2, 3, 4, 5, 6];

  handEl.textContent = data.hand ? `착용 부위: ${data.hand}` : '';

  let active = rings[0];

  rings.forEach((ring, idx) => {
    const btn = document.createElement('button');
    btn.className = 'chip' + (idx === 0 ? ' is-active' : '');
    btn.textContent = `${ring.name} (${ring.variant})`;
    btn.addEventListener('click', () => {
      ringGroup.querySelectorAll('.chip').forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      active = ring;
      render();
    });
    ringGroup.appendChild(btn);
  });

  function render() {
    if (!active) return;

    if (active.note) {
      noteEl.style.display = '';
      noteEl.innerHTML = `<div class="placeholder__mark">DATA MAY BE INCOMPLETE</div><p style="margin:0;">${EterCommon.escapeHtml(active.note)}</p>`;
    } else {
      noteEl.style.display = 'none';
    }

    thead.innerHTML = `
      <tr>
        <th rowspan="2" style="text-align:left; padding:9px 12px; background:var(--panel-raised); border-bottom:1px solid var(--line); font-family:var(--font-mono); font-size:12px; color:var(--muted); vertical-align:bottom;">구분</th>
        <th colspan="${colA.length}" style="padding:6px 12px; background:var(--amber); color:#1a1608; font-family:var(--font-mono); font-size:12px; text-align:center;">A 단계</th>
        <th colspan="${colB.length}" style="padding:6px 12px; background:var(--olive); color:#0d150a; font-family:var(--font-mono); font-size:12px; text-align:center;">B 단계</th>
      </tr>
      <tr>
        ${colA.map(c => `<th style="padding:7px 10px; background:var(--panel-raised); border-bottom:1px solid var(--line); font-family:var(--font-mono); font-size:12px; color:var(--paper-dim); text-align:right;">${c}</th>`).join('')}
        ${colB.map(c => `<th style="padding:7px 10px; background:var(--panel-raised); border-bottom:1px solid var(--line); font-family:var(--font-mono); font-size:12px; color:var(--paper-dim); text-align:right;">${c}</th>`).join('')}
      </tr>
    `;

    function cell(v) {
      return `<td style="padding:6px 10px; text-align:right; font-family:var(--font-mono); color:${v == null ? 'var(--line-bright)' : 'var(--paper-dim)'};">${v == null ? '·' : EterCommon.fmt(v)}</td>`;
    }

    tbody.innerHTML = active.materials.map((m, i) => `
      <tr style="border-top:1px solid var(--line); ${i % 2 === 1 ? 'background:rgba(255,255,255,0.015);' : ''}">
        <td style="padding:6px 12px; color:var(--paper); white-space:nowrap;">${EterCommon.escapeHtml(m.name)}</td>
        ${m.a.map(cell).join('')}
        ${m.b.map(cell).join('')}
      </tr>
    `).join('');
  }

  render();
});
