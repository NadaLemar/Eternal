document.addEventListener('DOMContentLoaded', async () => {
  const catGroup = document.getElementById('pu-category');
  const emptyBox = document.getElementById('pu-empty');
  const emptyLabel = document.getElementById('pu-empty-label');
  const content = document.getElementById('pu-content');
  const tableBody = document.getElementById('pu-table-body');
  const costNote = document.getElementById('pu-cost-note');
  const fromSelect = document.getElementById('pu-from');
  const toSelect = document.getElementById('pu-to');
  const costInput = document.getElementById('pu-cost-input');
  const expAttemptsEl = document.getElementById('pu-expected-attempts');
  const expCostEl = document.getElementById('pu-expected-cost');

  const simLevelEl = document.getElementById('pu-sim-level');
  const simAttemptsEl = document.getElementById('pu-sim-attempts');
  const simCostEl = document.getElementById('pu-sim-cost');
  const simResetsEl = document.getElementById('pu-sim-resets');
  const simLogEl = document.getElementById('pu-sim-log');
  const simAttemptBtn = document.getElementById('pu-sim-attempt');
  const simAutoBtn = document.getElementById('pu-sim-auto');
  const simResetBtn = document.getElementById('pu-sim-reset');

  const data = await EterCommon.loadJSON('data/plusup.json');
  const categories = (data && data.categories) || [];

  let activeCat = categories[0];
  let sim = { level: 0, attempts: 0, cost: 0, resets: 0, log: [] };
  let autoRunning = false;

  // ---- 카테고리 탭 ----
  categories.forEach((cat, idx) => {
    const btn = document.createElement('button');
    btn.className = 'chip' + (idx === 0 ? ' is-active' : '');
    btn.textContent = cat.label;
    btn.addEventListener('click', () => {
      catGroup.querySelectorAll('.chip').forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      activeCat = cat;
      resetSim();
      render();
    });
    catGroup.appendChild(btn);
  });

  // ---- 기대값 계산 (마르코프 체인: 초기화 시 0단계로 복귀) ----
  // e[i] = i단계에서 목표(target) 단계까지 도달하는 데 필요한 기대 시도 횟수
  function expectedAttempts(levels, fromLevel, target) {
    if (fromLevel >= target) return 0;
    // A[i], B[i] : e[i] = A[i] + B[i] * e[0]  (i = target-1 .. fromLevel)
    const A = new Array(target + 1).fill(0);
    const B = new Array(target + 1).fill(0);
    for (let i = target - 1; i >= fromLevel; i--) {
      const lv = levels[i]; // i단계에서 (i+1)단계로 가는 시도의 확률 정보
      const p = lv.success / 100;
      const f = lv.fail / 100;
      const r = lv.reset / 100;
      const nextA = i + 1 <= target ? (i + 1 === target ? 0 : A[i + 1]) : 0;
      const nextB = i + 1 <= target ? (i + 1 === target ? 0 : B[i + 1]) : 0;
      const denom = 1 - f;
      A[i] = (1 + p * nextA) / denom;
      B[i] = (p * nextB + r) / denom;
    }
    if (fromLevel === 0) {
      // e0 = A[0] + B[0] * e0  =>  e0 = A[0] / (1 - B[0])
      const e0 = A[0] / (1 - B[0]);
      return e0;
    }
    // fromLevel > 0 인 경우, 먼저 e0을 구한 뒤 e[fromLevel] = A[fromLevel] + B[fromLevel]*e0
    const A0 = new Array(target + 1).fill(0);
    const B0 = new Array(target + 1).fill(0);
    for (let i = target - 1; i >= 0; i--) {
      const lv = levels[i];
      const p = lv.success / 100;
      const f = lv.fail / 100;
      const r = lv.reset / 100;
      const nextA = i + 1 === target ? 0 : A0[i + 1];
      const nextB = i + 1 === target ? 0 : B0[i + 1];
      const denom = 1 - f;
      A0[i] = (1 + p * nextA) / denom;
      B0[i] = (p * nextB + r) / denom;
    }
    const e0 = A0[0] / (1 - B0[0]);
    return A0[fromLevel] + B0[fromLevel] * e0;
  }

  // ---- 렌더링 ----
  function render() {
    const hasData = activeCat && activeCat.levels && activeCat.levels.length;
    emptyBox.style.display = hasData ? 'none' : '';
    content.style.display = hasData ? '' : 'none';
    if (!hasData) {
      emptyLabel.textContent = `"${activeCat.label}" 강화 데이터는 아직 준비되지 않았습니다`;
      return;
    }

    costNote.textContent = activeCat.costPerAttempt
      ? `재료 1회 비용 기본값: ${EterCommon.fmt(activeCat.costPerAttempt)} ${activeCat.costUnit || ''}`
      : '';

    tableBody.innerHTML = activeCat.levels.map(lv => `
      <tr style="border-top:1px solid var(--line); text-align:right;">
        <td style="text-align:left; padding:8px 12px; font-family:var(--font-mono); color:var(--paper);">+${lv.level}</td>
        <td style="padding:8px 12px; color:var(--olive);">${lv.success}%</td>
        <td style="padding:8px 12px; color:var(--paper-dim);">${lv.fail}%</td>
        <td style="padding:8px 12px; color:var(--rust);">${lv.reset}%</td>
        <td style="padding:8px 12px; font-family:var(--font-mono);">${lv.atkPct != null ? lv.atkPct + '%' : '—'}</td>
        <td style="padding:8px 12px; font-family:var(--font-mono); color:var(--muted);">${lv.atkPctCL != null ? lv.atkPctCL + '%' : '—'}</td>
      </tr>
    `).join('');

    // 현재/목표 단계 셀렉트 옵션
    const maxLevel = activeCat.levels.length;
    fromSelect.innerHTML = '';
    toSelect.innerHTML = '';
    for (let i = 0; i < maxLevel; i++) {
      fromSelect.insertAdjacentHTML('beforeend', `<option value="${i}">+${i}</option>`);
    }
    for (let i = 1; i <= maxLevel; i++) {
      toSelect.insertAdjacentHTML('beforeend', `<option value="${i}" ${i === maxLevel ? 'selected' : ''}>+${i}</option>`);
    }
    costInput.value = activeCat.costPerAttempt || 0;

    updateExpectation();
    renderSim();
  }

  function updateExpectation() {
    if (!activeCat || !activeCat.levels.length) return;
    const from = parseInt(fromSelect.value || '0', 10);
    const to = parseInt(toSelect.value || String(activeCat.levels.length), 10);
    const cost = parseFloat(costInput.value || '0');
    if (to <= from) {
      expAttemptsEl.textContent = '0회';
      expCostEl.textContent = `0 ${activeCat.costUnit || ''}`;
      return;
    }
    const attempts = expectedAttempts(activeCat.levels, from, to);
    expAttemptsEl.textContent = `${EterCommon.fmt(Math.round(attempts))}회`;
    expCostEl.textContent = `${EterCommon.fmt(Math.round(attempts * cost))} ${activeCat.costUnit || ''}`;
  }

  fromSelect.addEventListener('change', updateExpectation);
  toSelect.addEventListener('change', updateExpectation);
  costInput.addEventListener('input', EterCommon.debounce(updateExpectation, 150));

  // ---- 실전 시뮬레이터 ----
  function resetSim() {
    sim = { level: 0, attempts: 0, cost: 0, resets: 0, log: [] };
    autoRunning = false;
    renderSim();
  }

  function renderSim() {
    simLevelEl.textContent = `+${sim.level}`;
    simAttemptsEl.textContent = EterCommon.fmt(sim.attempts);
    simCostEl.textContent = EterCommon.fmt(sim.cost);
    simResetsEl.textContent = EterCommon.fmt(sim.resets);
    simLogEl.innerHTML = sim.log.slice(-30).map(l => `<div>${l}</div>`).join('');
  }

  function doAttempt() {
    if (!activeCat || !activeCat.levels.length) return false;
    if (sim.level >= activeCat.levels.length) return false;

    const lv = activeCat.levels[sim.level]; // 다음 단계로 가는 확률
    const cost = activeCat.costPerAttempt || 0;
    const roll = Math.random() * 100;

    sim.attempts += 1;
    sim.cost += cost;

    let outcome;
    if (roll < lv.success) {
      sim.level += 1;
      outcome = `#${sim.attempts} +${lv.level} 강화 <span style="color:var(--olive)">성공</span> → 현재 +${sim.level}`;
    } else if (roll < lv.success + lv.fail) {
      outcome = `#${sim.attempts} +${lv.level} 강화 <span style="color:var(--paper-dim)">실패</span> (유지 +${sim.level})`;
    } else {
      sim.resets += 1;
      sim.level = 0;
      outcome = `#${sim.attempts} +${lv.level} 강화 <span style="color:var(--rust)">초기화</span> → +0으로 복귀`;
    }
    sim.log.push(outcome);
    return true;
  }

  simAttemptBtn.addEventListener('click', () => {
    doAttempt();
    renderSim();
  });

  simResetBtn.addEventListener('click', () => {
    resetSim();
  });

  simAutoBtn.addEventListener('click', () => {
    if (autoRunning) {
      autoRunning = false;
      simAutoBtn.textContent = '목표까지 자동 시도';
      return;
    }
    if (!activeCat || !activeCat.levels.length) return;
    const target = parseInt(toSelect.value || String(activeCat.levels.length), 10);
    autoRunning = true;
    simAutoBtn.textContent = '중지';

    const step = () => {
      if (!autoRunning) return;
      if (sim.level >= target || sim.attempts > 200000) {
        autoRunning = false;
        simAutoBtn.textContent = '목표까지 자동 시도';
        renderSim();
        return;
      }
      // 화면 업데이트 부담을 줄이기 위해 한 프레임에 여러 번 시도
      for (let k = 0; k < 25 && sim.level < target; k++) {
        doAttempt();
      }
      renderSim();
      requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });

  render();
});
