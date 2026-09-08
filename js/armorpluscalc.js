document.addEventListener('DOMContentLoaded', () => {
  const gradeEl = document.getElementById('ac-grade-calc');
  const materialEl = document.getElementById('ac-material');
  const clEl = document.getElementById('ac-cl');
  const pieceEl = document.getElementById('ac-piece');
  const levelEl = document.getElementById('ac-level');
  const resultEl = document.getElementById('ac-result');
  const breakdownEl = document.getElementById('ac-breakdown');
  if (!gradeEl) return;

  for (let i = 0; i <= 15; i++) {
    levelEl.insertAdjacentHTML('beforeend', `<option value="${i}" ${i === 7 ? 'selected' : ''}>${i}플</option>`);
  }

  function render() {
    const result = EterCalc.calculateArmorPlusUp({
      grade: parseInt(gradeEl.value, 10),
      material: materialEl.value,
      isCL: clEl.value === '1',
      pieceType: pieceEl.value,
      plusLevel: parseInt(levelEl.value, 10),
    });
    resultEl.textContent = result.attackBonusPct != null ? `+${result.attackBonusPct}%` : '계산 불가';
    breakdownEl.innerHTML = result.breakdown.map(b =>
      `<div>${b.step}: ${b.value != null ? b.value : ''}${b.note ? ` (${b.note})` : ''}</div>`
    ).join('');
  }

  [gradeEl, materialEl, clEl, pieceEl, levelEl].forEach(el => el.addEventListener('change', render));
  render();
});
