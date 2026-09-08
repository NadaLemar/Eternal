document.addEventListener('DOMContentLoaded', async () => {
  const params = new URLSearchParams(location.search);
  const cat = params.get('cat') || 'weapons';
  const id = params.get('id');

  const CAT_FILES = {
    weapons: 'data/weapons.json',
    armors: 'data/armors.json',
    accessories: 'data/accessories.json',
    costume_items: 'data/costume_items.json',
  };
  const CAT_LABELS = {
    weapons: 'WEAPON',
    armors: 'ARMOR',
    accessories: 'ACCESSORY',
    costume_items: 'COSTUME',
  };
  const CAT_BACK = {
    weapons: 'weapons.html',
    armors: 'armors.html',
    accessories: 'accessories.html',
    costume_items: 'costumes.html',
  };

  const notFoundEl = document.getElementById('id-notfound');
  const contentEl = document.getElementById('id-content');

  const path = CAT_FILES[cat];
  if (!path || !id) {
    notFoundEl.style.display = '';
    document.getElementById('id-name').textContent = '아이템을 찾을 수 없습니다';
    return;
  }

  const items = await EterCommon.loadJSON(path);
  const item = items.find(it => it.id === id);
  if (!item) {
    notFoundEl.style.display = '';
    document.getElementById('id-name').textContent = '아이템을 찾을 수 없습니다';
    return;
  }
  contentEl.style.display = '';

  document.getElementById('id-eyebrow').textContent = `ITEM DETAIL / ${CAT_LABELS[cat]}`;
  document.title = `${item.name} — EterPedia`;
  document.getElementById('id-name').textContent = item.name;
  document.getElementById('id-meta').textContent = `${item.type || ''}${item.grade != null ? ' · 등급 ' + item.grade : ''}${item.category1 ? ' · ' + item.category1 : ''}`;

  const imgEl = document.getElementById('id-image');
  const imgFallback = document.getElementById('id-image-fallback');
  if (item.imageUrl) {
    imgEl.onload = () => { imgEl.style.display = ''; imgFallback.style.display = 'none'; };
    imgEl.onerror = () => { imgEl.style.display = 'none'; imgFallback.textContent = '이미지를 불러올 수 없습니다'; imgFallback.style.display = ''; };
    imgEl.src = item.imageUrl;
  } else {
    imgFallback.textContent = '이미지 없음';
  }

  const badges = [
    item.category1 ? `<span class="badge badge--cl">${EterCommon.escapeHtml(item.category1)}</span>` : '',
    item.illegal ? `<span class="badge badge--illegal">불법</span>` : '',
    item.grade != null ? `<span class="badge badge--grade">등급 ${item.grade}</span>` : '',
    item.type ? `<span class="badge">${EterCommon.escapeHtml(item.type)}</span>` : '',
    item.rangeType ? `<span class="badge badge--olive">${EterCommon.escapeHtml(item.rangeType)}</span>` : '',
  ].filter(Boolean).join('');
  document.getElementById('id-badges').innerHTML = badges;

  const STAT_LABELS = {
    power: '파괴력', atkPct: '공격력%', defense: '방어력', defensePct: '방어력%', hp: '체력',
    crit: '치명', evasion: '회피', stamina: '지구', speed: '속도', action: '행동', numb: '무감',
    loadRate: '탄착', accuracy: '명중', shotCount: '발수', weight: '무게', holdCount: '보유개수',
  };
  const statRows = Object.keys(STAT_LABELS)
    .filter(k => item[k] !== undefined && item[k] !== null)
    .map(k => `<div class="stat-row"><dt>${STAT_LABELS[k]}</dt><dd>${EterCommon.fmt(item[k])}${k.includes('Pct') ? '%' : ''}</dd></div>`);
  if (item.fireRate) statRows.push(`<div class="stat-row"><dt>발사속도</dt><dd>${EterCommon.escapeHtml(item.fireRate)}</dd></div>`);
  if (item.size) statRows.push(`<div class="stat-row"><dt>크기</dt><dd>${EterCommon.escapeHtml(item.size)}</dd></div>`);
  document.getElementById('id-basestats').innerHTML = statRows.join('');

  document.getElementById('id-link').innerHTML = `<a href="${CAT_BACK[cat]}" style="color:var(--olive);">목록으로</a>`;

  // 버튼형 선택 그룹 생성 헬퍼: 옵션을 직접 채우고 클릭 시 is-active 토글 + 콜백
  function buildChipGroup(containerEl, options, activeValue, onChange) {
    containerEl.innerHTML = options.map(opt =>
      `<button class="chip${opt.value === activeValue ? ' is-active' : ''}" data-value="${opt.value}">${opt.label}</button>`
    ).join('');
    containerEl.querySelectorAll('.chip').forEach(btn => {
      btn.addEventListener('click', () => {
        containerEl.querySelectorAll('.chip').forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        onChange(btn.dataset.value);
      });
    });
  }

  // 이미 마크업에 버튼이 있는 그룹(방어구 재질/부위)은 클릭 핸들러만 연결
  function wireExistingChipGroup(containerEl, onChange) {
    containerEl.querySelectorAll('.chip').forEach(btn => {
      btn.addEventListener('click', () => {
        containerEl.querySelectorAll('.chip').forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        onChange(btn.dataset.value);
      });
    });
  }

  // ---- 무기: 강화/튜닝 계산기 ----
  if (cat === 'weapons' && item.power) {
    const calcBox = document.getElementById('id-weapon-calc');
    calcBox.style.display = '';
    const bodyGroup = document.getElementById('id-body');
    const stageGroup = document.getElementById('id-stage');
    const resultEl = document.getElementById('id-attack-result');
    const breakdownEl = document.getElementById('id-breakdown');

    const state = { body: '기본', stage: '노강' };

    function renderCalc() {
      const result = EterCalc.calculateWeaponEnhancement({
        basePower: item.power,
        bodyTuning: state.body,
        enhancementStage: state.stage,
      });
      resultEl.textContent = EterCommon.fmt(result.attack);
      breakdownEl.innerHTML = result.breakdown.map(b =>
        `<div>${b.step}${b.input != null ? `: ${EterCommon.fmt(b.input)}` : ''}${b.multiplier != null ? ` → ×${b.multiplier}` : ''}${b.note ? ` (${b.note})` : ''}</div>`
      ).join('');
    }

    buildChipGroup(
      bodyGroup,
      EterCalc.PART_TUNING_ORDER.map(level => ({ value: level, label: `${level} (×${EterCalc.PART_TUNING_MULT[level]})` })),
      state.body,
      (v) => { state.body = v; renderCalc(); }
    );
    buildChipGroup(
      stageGroup,
      EterCalc.ENHANCEMENT_STAGES.map(stage => ({ value: stage, label: stage })),
      state.stage,
      (v) => { state.stage = v; renderCalc(); }
    );
    renderCalc();

    // ---- 데미지 레인지 계산 ----
    const invAttackInput = document.getElementById('id-inv-attack');
    const multSize = document.getElementById('id-mult-size');
    const multAmmo = document.getElementById('id-mult-ammo');
    const multSpecial = document.getElementById('id-mult-special');
    const multSkill = document.getElementById('id-mult-skill');
    const damageTableEl = document.getElementById('id-damage-table');

    const DAMAGE_ROWS = [
      { key: 'normal', label: '일반' },
      { key: 'fire', label: '일반 발화' },
      { key: 'critical', label: '크리티컬' },
      { key: 'headshot', label: '헤드샷' },
      { key: 'criticalFire', label: '크리티컬 발화' },
      { key: 'headshotFire', label: '헤드샷 발화' },
    ];

    let userOverrodeInvAttack = false;
    invAttackInput.addEventListener('input', () => { userOverrodeInvAttack = true; renderDamage(); });
    [multSize, multAmmo, multSpecial, multSkill].forEach(el => el.addEventListener('input', renderDamage));

    function renderDamage() {
      if (!userOverrodeInvAttack) {
        const enhResult = EterCalc.calculateWeaponEnhancement({
          basePower: item.power, bodyTuning: state.body, enhancementStage: state.stage,
        });
        invAttackInput.value = enhResult.attack;
      }
      const inventoryAttack = parseFloat(invAttackInput.value || '0');
      const dmg = EterCalc.calculateDamageRange({
        inventoryAttack,
        sizeMultiplier: parseFloat(multSize.value || '1'),
        ammoSkinMultiplier: parseFloat(multAmmo.value || '1'),
        specialMultiplier: parseFloat(multSpecial.value || '1'),
        skillMultiplier: parseFloat(multSkill.value || '1'),
      });
      damageTableEl.innerHTML = DAMAGE_ROWS.map(row => `
        <tr style="border-top:1px solid var(--line);">
          <td style="padding:7px 10px; color:var(--paper);">${row.label}</td>
          <td style="padding:7px 10px; text-align:right; font-family:var(--font-mono); color:var(--paper-dim);">${EterCommon.fmt(dmg[row.key][0])}</td>
          <td style="padding:7px 10px; text-align:right; font-family:var(--font-mono); color:var(--amber);">${EterCommon.fmt(dmg[row.key][1])}</td>
        </tr>
      `).join('');
    }
    // 강화/튜닝 변경 시 데미지도 함께 갱신 (사용자가 직접 인벤창 공격력을 입력하지 않은 경우에만 자동 추적)
    const originalRenderCalc = renderCalc;
    renderCalc = function () {
      originalRenderCalc();
      renderDamage();
    };
    renderDamage();
  }

  // ---- 방어구/방패: 플러스업 효과 계산기 ----
  if (cat === 'armors' && item.grade != null) {
    const calcBox = document.getElementById('id-armor-calc');
    calcBox.style.display = '';
    const materialGroup = document.getElementById('id-material');
    const pieceGroup = document.getElementById('id-piece');
    const levelGroup = document.getElementById('id-level');
    const resultEl = document.getElementById('id-armor-result');
    const breakdownEl = document.getElementById('id-armor-breakdown');

    const state = { material: 'O.T', piece: '일반', level: 7 };

    function renderArmorCalc() {
      const result = EterCalc.calculateArmorPlusUp({
        grade: item.grade,
        material: state.material,
        isCL: item.category1 === 'CL',
        pieceType: state.piece,
        plusLevel: state.level,
      });
      resultEl.textContent = result.attackBonusPct != null ? `+${result.attackBonusPct}%` : '계산 불가';
      breakdownEl.innerHTML = result.breakdown.map(b =>
        `<div>${b.step}: ${b.value != null ? b.value : ''}${b.note ? ` (${b.note})` : ''}</div>`
      ).join('');
    }

    wireExistingChipGroup(materialGroup, (v) => { state.material = v; renderArmorCalc(); });
    wireExistingChipGroup(pieceGroup, (v) => { state.piece = v; renderArmorCalc(); });
    buildChipGroup(
      levelGroup,
      Array.from({ length: 16 }, (_, i) => ({ value: String(i), label: `${i}플` })),
      String(state.level),
      (v) => { state.level = parseInt(v, 10); renderArmorCalc(); }
    );
    renderArmorCalc();
  }
});
