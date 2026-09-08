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
    return;
  }

  const items = await EterCommon.loadJSON(path);
  const item = items.find(it => it.id === id);
  if (!item) {
    notFoundEl.style.display = '';
    return;
  }
  contentEl.style.display = '';

  document.getElementById('id-eyebrow').textContent = `ITEM DETAIL / ${CAT_LABELS[cat]}`;
  document.title = `${item.name} — EterPedia`;
  document.getElementById('id-name').textContent = item.name;
  document.getElementById('id-meta').textContent = `${item.type || ''}${item.grade != null ? ' · 등급 ' + item.grade : ''}${item.category1 ? ' · ' + item.category1 : ''}`;

  if (item.imageUrl) {
    document.getElementById('id-image').src = item.imageUrl;
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

  if (item.detailUrl) {
    document.getElementById('id-link').innerHTML = `<a href="${item.detailUrl}" target="_blank" rel="noopener">eterinfo.kr 원본 보기 ↗</a> · <a href="${CAT_BACK[cat]}" style="margin-left:10px; color:var(--olive);">목록으로</a>`;
  } else {
    document.getElementById('id-link').innerHTML = `<a href="${CAT_BACK[cat]}" style="color:var(--olive);">목록으로</a>`;
  }

  // ---- 무기: 강화/튜닝 계산기 ----
  if (cat === 'weapons' && item.power) {
    const calcBox = document.getElementById('id-weapon-calc');
    calcBox.style.display = '';
    const bodySelect = document.getElementById('id-body');
    const stageSelect = document.getElementById('id-stage');
    const resultEl = document.getElementById('id-attack-result');
    const breakdownEl = document.getElementById('id-breakdown');

    EterCalc.PART_TUNING_ORDER.forEach(level => {
      bodySelect.insertAdjacentHTML('beforeend', `<option value="${level}">${level} (×${EterCalc.PART_TUNING_MULT[level]})</option>`);
    });
    EterCalc.ENHANCEMENT_STAGES.forEach(stage => {
      stageSelect.insertAdjacentHTML('beforeend', `<option value="${stage}">${stage}</option>`);
    });
    bodySelect.value = '기본';
    stageSelect.value = '노강';

    function renderCalc() {
      const result = EterCalc.calculateWeaponEnhancement({
        basePower: item.power,
        bodyTuning: bodySelect.value,
        enhancementStage: stageSelect.value,
      });
      resultEl.textContent = EterCommon.fmt(result.attack);
      breakdownEl.innerHTML = result.breakdown.map(b =>
        `<div>${b.step}${b.input != null ? `: ${EterCommon.fmt(b.input)}` : ''}${b.multiplier != null ? ` → ×${b.multiplier}` : ''}${b.note ? ` (${b.note})` : ''}</div>`
      ).join('');
    }
    [bodySelect, stageSelect].forEach(el => el.addEventListener('change', renderCalc));
    renderCalc();
  }

  // ---- 방어구/방패: 플러스업 효과 계산기 ----
  if (cat === 'armors' && item.grade != null) {
    const calcBox = document.getElementById('id-armor-calc');
    calcBox.style.display = '';
    const materialSelect = document.getElementById('id-material');
    const pieceSelect = document.getElementById('id-piece');
    const levelSelect = document.getElementById('id-level');
    const resultEl = document.getElementById('id-armor-result');
    const breakdownEl = document.getElementById('id-armor-breakdown');

    for (let i = 0; i <= 15; i++) {
      levelSelect.insertAdjacentHTML('beforeend', `<option value="${i}">${i}플</option>`);
    }
    levelSelect.value = '7';

    function renderArmorCalc() {
      const result = EterCalc.calculateArmorPlusUp({
        grade: item.grade,
        material: materialSelect.value,
        isCL: item.category1 === 'CL',
        pieceType: pieceSelect.value,
        plusLevel: parseInt(levelSelect.value, 10),
      });
      resultEl.textContent = result.attackBonusPct != null ? `+${result.attackBonusPct}%` : '계산 불가';
      breakdownEl.innerHTML = result.breakdown.map(b =>
        `<div>${b.step}: ${b.value != null ? b.value : ''}${b.note ? ` (${b.note})` : ''}</div>`
      ).join('');
    }
    [materialSelect, pieceSelect, levelSelect].forEach(el => el.addEventListener('change', renderArmorCalc));
    renderArmorCalc();
  }
});
