// 이터널시티 장비 강화/튜닝 계산 엔진
// 출처: 사용자 제공 "이터널시티_강화계산식_Claude전달용" 자료
// 신뢰도 원칙: '확정'된 공식만 계산에 사용. '미확인' 수치는 절대 임의로 채우지 않고 null + confidence 표시.

const EterCalc = (() => {

  // ---- 부품 튜닝 배율 (확정) ----
  const PART_TUNING_MULT = {
    '기본': 1.0, '초보': 1.1, '숙련': 1.3, '전문': 1.5,
    '장인': 2.0, '명인': 3.0, 'O.T': 4.0,
  };
  const PART_TUNING_ORDER = ['기본', '초보', '숙련', '전문', '장인', '명인', 'O.T'];

  // ---- 무기 강화 20단계 누적 배율 (확정, 노강 대비) ----
  const ENHANCEMENT_STAGES = ['노강', '1강', '2강', '3강', '4강', '5강', '6강', '7강', '8강', '9강',
    '맥강', '맥1강', '맥2강', '맥3강', '맥4강', '맥5강', '맥6강', '맥7강', '맥8강', '맥9강'];
  const ENHANCEMENT_CUMULATIVE = {
    '노강': 1.0, '1강': 1.01, '2강': 1.0302, '3강': 1.061106, '4강': 1.1035502400000001,
    '5강': 1.158727752, '6강': 1.22825141712, '7강': 1.3142290163184, '8강': 1.4193673376238722,
    '9강': 1.547110398010021, '맥강': 1.5625815019901212, '맥1강': 1.5782073170100224,
    '맥2강': 1.5939893901801225, '맥3강': 1.6418090718855263, '맥4강': 1.6910633440420921,
    '맥5강': 1.7417952443633549, '맥6강': 1.8463029590251563, '맥7강': 1.9570811365666658,
    '맥8강': 2.074506004760666, '맥9강': 2.281956605236733,
  };

  // ---- 무기 강화 계산 (확정 공식. 사이트와 완전히 같은 정수 반올림 규칙은 미확정) ----
  // roundingNote: 실측 검증 결과 "기초값 × 부품배율 × 누적배율"을 한 번만 반올림하는 방식이
  // 실제 사이트 값과 오차 ±2 이내로 거의 일치함 (완전 일치는 아님 — 중간 단계별 반올림 규칙 미확정).
  function calculateWeaponEnhancement({ basePower, bodyTuning = '기본', enhancementStage = '노강' }) {
    const breakdown = [];
    const bodyMult = PART_TUNING_MULT[bodyTuning] ?? 1.0;
    breakdown.push({ step: 'baseAttack', input: basePower });
    breakdown.push({ step: `몸체(${bodyTuning})`, multiplier: bodyMult });

    const cumMult = ENHANCEMENT_CUMULATIVE[enhancementStage] ?? 1.0;
    breakdown.push({ step: `강화(${enhancementStage})`, multiplier: cumMult, note: '노강 대비 누적배율' });

    const raw = basePower * bodyMult * cumMult;
    const attack = Math.round(raw);

    return {
      attack,
      breakdown,
      roundingMode: 'single_final_round',
      confidence: 'partially_verified',
      note: '사이트 값과 오차 ±2 이내로 근사 (중간 단계 반올림 규칙 미확정)',
    };
  }

  function calculateWeaponPartStat(baseValue, tuningLevel) {
    if (baseValue == null) return null;
    const mult = PART_TUNING_MULT[tuningLevel] ?? 1.0;
    return { value: baseValue * mult, multiplier: mult, confidence: 'confirmed_effect_only' };
  }

  // ---- 방어구 플러스업 (확정 공식) ----
  const GRADE_COEFF = { 1: 0.5, 2: 0.6, 3: 0.7, 4: 0.8, 5: 0.9, 6: 1.0, 7: 1.1, 8: 1.2, 9: 1.3, 10: 1.4, 11: 1.5 };
  const MATERIAL_COEFF = { '장인': 1.11, '명인': 1.66, 'O.T': 2.5 };
  const PIECE_MULT = { '일반': 1.0, '원피스': 2.0, '전신의상': 6.0 };

  function weightedSteps(p) {
    return Math.min(p, 5) * 1 + Math.max(Math.min(p, 10) - 5, 0) * 2 + Math.max(p - 10, 0) * 3;
  }

  function calculateArmorPlusUp({ grade, material, isCL = false, pieceType = '일반', plusLevel = 0 }) {
    const breakdown = [];
    if (!MATERIAL_COEFF[material]) {
      return {
        attackBonusPct: 0,
        breakdown: [{ step: '재질', note: `${material}은(는) 플러스업 불가 — 장인 이상 재질만 가능` }],
        confidence: 'confirmed',
      };
    }
    const gradeCoeff = GRADE_COEFF[grade] ?? null;
    if (gradeCoeff == null) {
      return { attackBonusPct: null, breakdown: [], confidence: 'unknown', note: '등급 범위(1~11) 밖' };
    }
    const materialCoeff = MATERIAL_COEFF[material];
    const clMult = isCL ? 1.1 : 1.0;
    const pieceMult = PIECE_MULT[pieceType] ?? 1.0;
    const steps = weightedSteps(plusLevel);

    breakdown.push({ step: '등급계수', value: gradeCoeff });
    breakdown.push({ step: '재질계수', value: materialCoeff });
    breakdown.push({ step: 'CL보정', value: clMult });
    breakdown.push({ step: '부위보정', value: pieceMult });
    breakdown.push({ step: '누적가중스텝', value: steps, note: `${plusLevel}플 기준` });

    const attackBonusPct = gradeCoeff * materialCoeff * clMult * pieceMult * steps;

    return { attackBonusPct: Math.round(attackBonusPct * 100) / 100, breakdown, confidence: 'confirmed' };
  }

  // ---- 데미지 레인지 계산 (확정 배율. 캐릭터 스탯→인벤창 공격력 변환식은 미확인) ----
  // 검증: [CL] 처형자의 검 (인벤창 공격력 52,604) 실측값과 오차 ±1 이내로 완전히 일치.
  function calculateDamageRange({ inventoryAttack, sizeMultiplier = 1, ammoSkinMultiplier = 1, specialMultiplier = 1, skillMultiplier = 1 }) {
    const normalMin = inventoryAttack * 0.88 * sizeMultiplier * ammoSkinMultiplier * specialMultiplier * skillMultiplier;
    const normalMax = normalMin * 1.5;
    const fireMin = normalMin * 1.5;
    const fireMax = normalMax * 1.5;
    const criticalMin = normalMin * 1.55;
    const criticalMax = normalMax * 1.55;
    const headshotMin = normalMin * 3.10;
    const headshotMax = normalMax * 3.10;
    const criticalFireMin = criticalMin * 1.5;
    const criticalFireMax = criticalMax * 1.5;
    const headshotFireMin = headshotMin * 1.5;
    const headshotFireMax = headshotMax * 1.5;

    const r = (v) => Math.round(v);
    return {
      normal: [r(normalMin), r(normalMax)],
      fire: [r(fireMin), r(fireMax)],
      critical: [r(criticalMin), r(criticalMax)],
      headshot: [r(headshotMin), r(headshotMax)],
      criticalFire: [r(criticalFireMin), r(criticalFireMax)],
      headshotFire: [r(headshotFireMin), r(headshotFireMax)],
      confidence: 'confirmed',
      note: '기본 배율(0.88, 1.5, 1.55, 3.10)은 확정. 크기/탄종/특수/스킬 보정값은 아이템별로 다를 수 있으며 기본값 1로 계산됩니다.',
    };
  }

  // ---- 캐릭터 스탯 → 인벤창 공격력 (공식 미확인, 임의 추정 금지) ----
  function calculateCharacterAttack() {
    return {
      value: null,
      confidence: 'unknown',
      note: 'NEEDS_VERIFICATION — 무기 파괴력에 체력/기술/템공합/업적공/해방공/무기타입이 어떻게 반영되는지 정확한 공식이 아직 확인되지 않았습니다. 실제 게임 화면에 표시된 공격력 값을 직접 입력해서 사용하세요.',
    };
  }

  return {
    PART_TUNING_MULT, PART_TUNING_ORDER,
    ENHANCEMENT_STAGES, ENHANCEMENT_CUMULATIVE,
    GRADE_COEFF, MATERIAL_COEFF, PIECE_MULT,
    calculateWeaponEnhancement, calculateWeaponPartStat,
    calculateArmorPlusUp, weightedSteps,
    calculateDamageRange, calculateCharacterAttack,
  };
})();
