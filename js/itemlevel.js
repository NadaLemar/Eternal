document.addEventListener('DOMContentLoaded', () => {
  const gradeEl = document.getElementById('lv-grade');
  const charEl = document.getElementById('lv-char');
  const reqEl = document.getElementById('lv-required');
  const penaltyEl = document.getElementById('lv-penalty');
  if (!gradeEl) return;

  function compute() {
    const grade = parseInt(gradeEl.value, 10);
    const charLevel = parseInt(charEl.value || '0', 10);

    if (grade === 10) {
      reqEl.textContent = '90레벨 (필수)';
      penaltyEl.textContent = charLevel >= 90 ? '착용 가능' : '착용 불가';
      return;
    }
    if (grade === 11) {
      reqEl.textContent = '101레벨 + 특정 퀘스트 (필수)';
      penaltyEl.textContent = charLevel >= 101 ? '착용 가능 (퀘스트 완료 시)' : '착용 불가';
      return;
    }

    // 9등급 이하: (등급-2)*10, 최소 0
    const required = Math.max(0, (grade - 2) * 10);
    reqEl.textContent = `${required}레벨`;

    if (charLevel >= required) {
      penaltyEl.textContent = '100% (정상 적용)';
    } else {
      const shortfall = required - charLevel;
      const applied = Math.max(0, 100 - shortfall * 10);
      penaltyEl.textContent = `${applied}% (레벨 ${shortfall} 부족)`;
    }
  }

  gradeEl.addEventListener('change', compute);
  charEl.addEventListener('input', EterCommon.debounce(compute, 150));
  compute();
});
