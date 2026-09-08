document.addEventListener('DOMContentLoaded', async () => {
  const setupNotice = document.getElementById('mp-setup-notice');
  const appRoot = document.getElementById('mp-app');

  if (!window.ETER_FIREBASE_CONFIGURED) {
    setupNotice.style.display = '';
    appRoot.style.display = 'none';
    return;
  }
  setupNotice.style.display = 'none';
  appRoot.style.display = '';

  EterAuth.ensureInit();
  const db = firebase.firestore();

  const authBox = document.getElementById('mp-auth-box');
  const charBox = document.getElementById('mp-character-box');
  const usernameEl = document.getElementById('mp-username');

  // ---- 로그인은 전역 위젯/모달을 사용 ----
  document.getElementById('mp-open-login').addEventListener('click', () => {
    if (window.EterAuthModal) window.EterAuthModal.open();
  });
  document.getElementById('mp-logout').addEventListener('click', () => EterAuth.logOut());

  // ---- 데이터 카탈로그 로드 ----
  const [weapons, armors, accessories, achievements] = await Promise.all([
    EterCommon.loadJSON('data/weapons.json'),
    EterCommon.loadJSON('data/armors.json'),
    EterCommon.loadJSON('data/accessories.json'),
    EterCommon.loadJSON('data/achievements.json'),
  ]);

  const armorsBySlot = {};
  EterSlots.ARMOR_SLOT_ORDER.forEach(s => armorsBySlot[s] = []);
  armors.forEach(it => {
    const slot = EterSlots.armorSlotOf(it.type);
    if (slot && armorsBySlot[slot]) armorsBySlot[slot].push(it);
  });

  const accessoriesBySlot = {};
  EterSlots.ACCESSORY_SLOT_ORDER.forEach(s => accessoriesBySlot[s] = []);
  accessories.forEach(it => {
    if (accessoriesBySlot[it.type]) accessoriesBySlot[it.type].push(it);
  });

  // ---- 상태 ----
  let character = defaultCharacter();
  let currentUid = null;

  function defaultCharacter() {
    return {
      name: '', level: 1, trait: '휴먼',
      hp: 0, skill: 0, itemAtk: 0, itemCrit: 0, achAtk: 0, releaseAtk: 0,
      weapon: null, // { itemId, bodyTuning, stage }
      armorSlots: {}, // slotKey -> { itemId, material, plusLevel }
      accessorySlots: {}, // slotKey -> itemId
      achievements: [], // ids
    };
  }

  // ---- 무기 선택 UI ----
  const weaponSelect = document.getElementById('mp-weapon-select');
  const weaponOptionsBox = document.getElementById('mp-weapon-options');
  const weaponBodyGroup = document.getElementById('mp-weapon-body');
  const weaponStageGroup = document.getElementById('mp-weapon-stage');

  weapons.filter(w => w.power).forEach(w => {
    weaponSelect.insertAdjacentHTML('beforeend', `<option value="${w.id}">${EterCommon.escapeHtml(w.name)} (기초 ${EterCommon.fmt(w.power)})</option>`);
  });

  function buildChipGroup(containerEl, options, activeValue, onChange) {
    containerEl.innerHTML = options.map(opt =>
      `<button type="button" class="chip${opt.value === activeValue ? ' is-active' : ''}" data-value="${opt.value}">${opt.label}</button>`
    ).join('');
    containerEl.querySelectorAll('.chip').forEach(btn => {
      btn.addEventListener('click', () => {
        containerEl.querySelectorAll('.chip').forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        onChange(btn.dataset.value);
      });
    });
  }

  weaponSelect.addEventListener('change', () => {
    if (!character.weapon) character.weapon = {};
    character.weapon.itemId = weaponSelect.value || null;
    if (!weaponSelect.value) {
      weaponOptionsBox.style.display = 'none';
      character.weapon = null;
    } else {
      weaponOptionsBox.style.display = '';
      character.weapon.bodyTuning = character.weapon.bodyTuning || '기본';
      character.weapon.stage = character.weapon.stage || '노강';
      renderWeaponChips();
    }
    renderSummary();
  });

  function renderWeaponChips() {
    buildChipGroup(weaponBodyGroup, EterCalc.PART_TUNING_ORDER.map(l => ({ value: l, label: `${l} (×${EterCalc.PART_TUNING_MULT[l]})` })),
      character.weapon.bodyTuning, (v) => { character.weapon.bodyTuning = v; renderSummary(); });
    buildChipGroup(weaponStageGroup, EterCalc.ENHANCEMENT_STAGES.map(s => ({ value: s, label: s })),
      character.weapon.stage, (v) => { character.weapon.stage = v; renderSummary(); });
  }

  // ---- 방어구 슬롯 UI ----
  const armorSlotsContainer = document.getElementById('mp-armor-slots');
  EterSlots.ARMOR_SLOT_ORDER.forEach(slot => {
    const items = armorsBySlot[slot];
    if (!items.length) return;
    const card = document.createElement('div');
    card.className = 'cat-card';
    card.style.minHeight = 'auto';
    card.innerHTML = `
      <h3 style="margin-bottom:8px;">${slot}</h3>
      <select data-slot="${slot}" class="mp-armor-select" style="width:100%; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr); margin-bottom:8px;">
        <option value="">장착 안 함</option>
        ${items.map(it => `<option value="${it.id}">${EterCommon.escapeHtml(it.name)} (등급${it.grade}${it.defense != null ? ', 방어력 ' + it.defense : ''})</option>`).join('')}
      </select>
      <div class="mp-armor-plusup" data-slot="${slot}" style="display:none;">
        <div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:6px;">
          <select class="mp-armor-material" style="background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:5px 7px; font-size:12px;">
            <option value="장인">장인</option><option value="명인">명인</option><option value="O.T">O.T</option>
          </select>
          <select class="mp-armor-level" style="background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:5px 7px; font-size:12px;"></select>
        </div>
      </div>
    `;
    armorSlotsContainer.appendChild(card);

    const select = card.querySelector('.mp-armor-select');
    const plusupBox = card.querySelector('.mp-armor-plusup');
    const materialSelect = card.querySelector('.mp-armor-material');
    const levelSelect = card.querySelector('.mp-armor-level');
    for (let i = 0; i <= 15; i++) levelSelect.insertAdjacentHTML('beforeend', `<option value="${i}">${i}플</option>`);

    select.addEventListener('change', () => {
      if (!select.value) {
        delete character.armorSlots[slot];
        plusupBox.style.display = 'none';
      } else {
        character.armorSlots[slot] = { itemId: select.value, material: materialSelect.value, plusLevel: parseInt(levelSelect.value, 10) };
        plusupBox.style.display = '';
      }
      renderSummary();
    });
    materialSelect.addEventListener('change', () => {
      if (character.armorSlots[slot]) { character.armorSlots[slot].material = materialSelect.value; renderSummary(); }
    });
    levelSelect.addEventListener('change', () => {
      if (character.armorSlots[slot]) { character.armorSlots[slot].plusLevel = parseInt(levelSelect.value, 10); renderSummary(); }
    });
  });

  // ---- 악세서리 슬롯 UI ----
  const accessorySlotsContainer = document.getElementById('mp-accessory-slots');
  EterSlots.ACCESSORY_SLOT_ORDER.forEach(slot => {
    const items = accessoriesBySlot[slot];
    if (!items.length) return;
    const card = document.createElement('div');
    card.className = 'cat-card';
    card.style.minHeight = 'auto';
    card.innerHTML = `
      <h3 style="margin-bottom:8px;">${slot}</h3>
      <select data-slot="${slot}" class="mp-accessory-select" style="width:100%; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);">
        <option value="">장착 안 함</option>
        ${items.map(it => `<option value="${it.id}">${EterCommon.escapeHtml(it.name)}</option>`).join('')}
      </select>
    `;
    accessorySlotsContainer.appendChild(card);
    const select = card.querySelector('.mp-accessory-select');
    select.addEventListener('change', () => {
      if (!select.value) delete character.accessorySlots[slot];
      else character.accessorySlots[slot] = select.value;
      renderSummary();
    });
  });

  // ---- 업적 체크리스트 ----
  const achBox = document.getElementById('mp-achievements');
  achievements.forEach(a => {
    achBox.insertAdjacentHTML('beforeend', `
      <label style="display:flex; align-items:center; gap:8px;">
        <input type="checkbox" class="mp-ach-check" value="${a.id}">
        <span>${EterCommon.escapeHtml(a.name)}</span>
      </label>
    `);
  });
  achBox.querySelectorAll('.mp-ach-check').forEach(cb => {
    cb.addEventListener('change', () => {
      character.achievements = [...achBox.querySelectorAll('.mp-ach-check:checked')].map(c => c.value);
    });
  });

  // ---- 기본 스탯 입력 바인딩 ----
  const statInputs = {
    name: document.getElementById('mp-name'),
    level: document.getElementById('mp-level'),
    trait: document.getElementById('mp-trait'),
    hp: document.getElementById('mp-hp'),
    skill: document.getElementById('mp-skill'),
    itemAtk: document.getElementById('mp-itematk'),
    itemCrit: document.getElementById('mp-itemcrit'),
    achAtk: document.getElementById('mp-achatk'),
    releaseAtk: document.getElementById('mp-releaseatk'),
  };
  Object.entries(statInputs).forEach(([key, el]) => {
    el.addEventListener('input', () => {
      character[key] = el.type === 'number' ? parseFloat(el.value || '0') : el.value;
    });
  });

  // ---- 요약 계산 ----
  function renderSummary() {
    // 무기
    let weaponAttack = null;
    if (character.weapon && character.weapon.itemId) {
      const w = weapons.find(x => x.id === character.weapon.itemId);
      if (w) {
        const result = EterCalc.calculateWeaponEnhancement({
          basePower: w.power, bodyTuning: character.weapon.bodyTuning, enhancementStage: character.weapon.stage,
        });
        weaponAttack = result.attack;
      }
    }
    document.getElementById('mp-sum-weapon').textContent = weaponAttack != null ? EterCommon.fmt(weaponAttack) : '미장착';

    // 방어구
    let totalDefense = 0;
    let totalArmorPct = 0;
    Object.entries(character.armorSlots).forEach(([slot, cfg]) => {
      const it = armorsBySlot[slot].find(x => x.id === cfg.itemId);
      if (!it) return;
      if (it.defense) totalDefense += it.defense;
      const r = EterCalc.calculateArmorPlusUp({
        grade: it.grade, material: cfg.material, isCL: it.category1 === 'CL', pieceType: '일반', plusLevel: cfg.plusLevel,
      });
      if (r.attackBonusPct) totalArmorPct += r.attackBonusPct;
    });
    document.getElementById('mp-sum-defense').textContent = EterCommon.fmt(totalDefense);
    document.getElementById('mp-sum-armorpct').textContent = `+${Math.round(totalArmorPct * 100) / 100}%`;

    // 악세서리
    const accTotals = {};
    Object.entries(character.accessorySlots).forEach(([slot, itemId]) => {
      const it = accessoriesBySlot[slot].find(x => x.id === itemId);
      if (!it) return;
      ['atkPct', 'defense', 'hp', 'crit', 'evasion', 'stamina', 'speed', 'action', 'numb'].forEach(k => {
        if (it[k]) accTotals[k] = (accTotals[k] || 0) + it[k];
      });
    });
    const labels = { atkPct: '공격력%', defense: '방어력', hp: '체력', crit: '치명', evasion: '회피', stamina: '지구', speed: '속도', action: '행동', numb: '무감' };
    const accStr = Object.entries(accTotals).map(([k, v]) => `${labels[k]} +${EterCommon.fmt(v)}`).join(' · ');
    document.getElementById('mp-sum-accessory').textContent = accStr || '장착 없음';
  }

  // ---- Firestore 저장/불러오기 ----
  function loadCharacterIntoForm() {
    statInputs.name.value = character.name || '';
    statInputs.level.value = character.level || 1;
    statInputs.trait.value = character.trait || '휴먼';
    statInputs.hp.value = character.hp || 0;
    statInputs.skill.value = character.skill || 0;
    statInputs.itemAtk.value = character.itemAtk || 0;
    statInputs.itemCrit.value = character.itemCrit || 0;
    statInputs.achAtk.value = character.achAtk || 0;
    statInputs.releaseAtk.value = character.releaseAtk || 0;

    weaponSelect.value = character.weapon ? character.weapon.itemId : '';
    if (character.weapon && character.weapon.itemId) {
      weaponOptionsBox.style.display = '';
      renderWeaponChips();
    }

    document.querySelectorAll('.mp-armor-select').forEach(sel => {
      const slot = sel.dataset.slot;
      const cfg = character.armorSlots[slot];
      if (cfg) {
        sel.value = cfg.itemId;
        const card = sel.closest('.cat-card');
        card.querySelector('.mp-armor-plusup').style.display = '';
        card.querySelector('.mp-armor-material').value = cfg.material || 'O.T';
        card.querySelector('.mp-armor-level').value = cfg.plusLevel || 0;
      }
    });
    document.querySelectorAll('.mp-accessory-select').forEach(sel => {
      const slot = sel.dataset.slot;
      if (character.accessorySlots[slot]) sel.value = character.accessorySlots[slot];
    });
    achBox.querySelectorAll('.mp-ach-check').forEach(cb => {
      cb.checked = (character.achievements || []).includes(cb.value);
    });

    renderSummary();
  }

  document.getElementById('mp-save').addEventListener('click', async () => {
    if (!currentUid) return;
    const statusEl = document.getElementById('mp-save-status');
    statusEl.textContent = '저장 중...';
    try {
      await db.collection('characters').doc(currentUid).set({
        ...character,
        updatedAt: firebase.firestore.FieldValue.serverTimestamp(),
      });
      statusEl.textContent = '저장 완료';
      setTimeout(() => { statusEl.textContent = ''; }, 2000);
    } catch (err) {
      statusEl.textContent = '저장 실패: ' + err.message;
    }
  });

  // ---- 로그인 상태 감지 ----
  EterAuth.onAuthChange(async (user) => {
    if (user) {
      currentUid = user.uid;
      authBox.style.display = 'none';
      charBox.style.display = '';
      const userDoc = await db.collection('users').doc(user.uid).get();
      usernameEl.textContent = userDoc.exists ? userDoc.data().username : user.email.split('@')[0];

      const charDoc = await db.collection('characters').doc(user.uid).get();
      character = charDoc.exists ? { ...defaultCharacter(), ...charDoc.data() } : defaultCharacter();
      loadCharacterIntoForm();
    } else {
      currentUid = null;
      authBox.style.display = '';
      charBox.style.display = 'none';
    }
  });
});
