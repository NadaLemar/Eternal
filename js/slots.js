// 방어구/악세서리 세부분류(type)를 캐릭터 장비 슬롯으로 매핑
const EterSlots = (() => {
  // 방어구: 남성/여성 접두어를 떼어 공용 슬롯으로 묶음
  function armorSlotOf(type) {
    if (!type) return null;
    if (type.includes('방패')) return '방패';
    return type.replace(/^(남성|여성)/, '');
  }

  const ARMOR_SLOT_ORDER = ['모자', '가발', '상의', '자켓상의', '하의', '신발', '코트', '스타킹', '감염체전용의상', '방패'];
  const ACCESSORY_SLOT_ORDER = ['벨트', '귀걸이', '목걸이', '팔찌', '반지', '왼손반지', '환생악세', '토이'];

  return { armorSlotOf, ARMOR_SLOT_ORDER, ACCESSORY_SLOT_ORDER };
})();
