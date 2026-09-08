document.addEventListener('DOMContentLoaded', async () => {
  const weaponSelect = document.getElementById('wc-weapon');
  const bodySelect = document.getElementById('wc-body');
  const stageSelect = document.getElementById('wc-stage');
  const resultEl = document.getElementById('wc-result');
  const baseEl = document.getElementById('wc-base');
  const breakdownEl = document.getElementById('wc-breakdown');
  if (!weaponSelect) return;

  const weapons = (await EterCommon.loadJSON('data/weapons.json')).filter(w => w.power);

  weapons.forEach((w, i) => {
    weaponSelect.insertAdjacentHTML('beforeend', `<option value="${i}">${EterCommon.escapeHtml(w.name)} (기초 ${EterCommon.fmt(w.power)})</option>`);
  });
  EterCalc.PART_TUNING_ORDER.forEach(level => {
    bodySelect.insertAdjacentHTML('beforeend', `<option value="${level}" ${level === 'O.T' ? 'selected' : ''}>${level} (×${EterCalc.PART_TUNING_MULT[level]})</option>`);
  });
  EterCalc.ENHANCEMENT_STAGES.forEach(stage => {
    stageSelect.insertAdjacentHTML('beforeend', `<option value="${stage}" ${stage === '맥9강' ? 'selected' : ''}>${stage}</option>`);
  });

  function render() {
    const w = weapons[parseInt(weaponSelect.value || '0', 10)];
    if (!w) return;
    baseEl.textContent = EterCommon.fmt(w.power);
    const result = EterCalc.calculateWeaponEnhancement({
      basePower: w.power,
      bodyTuning: bodySelect.value,
      enhancementStage: stageSelect.value,
    });
    resultEl.textContent = EterCommon.fmt(result.attack);
    breakdownEl.innerHTML = result.breakdown.map(b =>
      `<div>${b.step}${b.input != null ? `: ${EterCommon.fmt(b.input)}` : ''}${b.multiplier != null ? ` → ×${b.multiplier}` : ''}${b.note ? ` (${b.note})` : ''}</div>`
    ).join('');
  }

  [weaponSelect, bodySelect, stageSelect].forEach(el => el.addEventListener('change', render));
  render();
});
