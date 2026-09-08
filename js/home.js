document.addEventListener('DOMContentLoaded', async () => {
  const [weapons, costumes, quests, achievements, ringData, armors, accessories] = await Promise.all([
    EterCommon.loadJSON('data/weapons.json'),
    EterCommon.loadJSON('data/costumes.json'),
    EterCommon.loadJSON('data/quests.json'),
    EterCommon.loadJSON('data/achievements.json'),
    EterCommon.loadJSON('data/ring_materials.json'),
    EterCommon.loadJSON('data/armors.json'),
    EterCommon.loadJSON('data/accessories.json'),
  ]);
  const ringCount = (ringData && ringData.rings) ? ringData.rings.length : 0;

  setText('stat-weapons', EterCommon.fmt(weapons.length));
  setText('stat-costumes', EterCommon.fmt(costumes.length));
  setText('stat-quests', EterCommon.fmt(quests.length));
  setText('stat-achievements', EterCommon.fmt(achievements.length));
  setText('count-weapons', `${weapons.length}건`);
  setText('count-costumes', `${costumes.length}건`);
  setText('count-quests', `${quests.length}건`);
  setText('count-achievements', `${achievements.length}건`);
  setText('count-ringmats', `${ringCount}종`);
  setText('count-armors', `${armors.length}건`);
  setText('count-accessories', `${accessories.length}건`);

  const updates = [
    ...weapons.map(w => ({ date: w.updatedAt || '2026-09-08', type: '무기', badge: 'olive', label: w.name, href: 'weapons.html' })),
    ...costumes.map(c => ({ date: '2026-09-07', type: '코스튬', badge: 'olive', label: c.name, href: 'costumes.html' })),
    ...quests.map(q => ({ date: q.updatedAt, type: '퀘스트', badge: 'main', label: q.name, href: 'quests.html' })),
    ...achievements.map(a => ({ date: a.updatedAt, type: '업적', badge: 'grade', label: a.name, href: 'achievements.html' })),
  ].sort((a, b) => (a.date < b.date ? 1 : -1)).slice(0, 8);

  const list = document.getElementById('update-list');
  if (list) {
    list.innerHTML = updates.map(u => `
      <div class="update-row">
        <time>${u.date}</time>
        <span class="badge badge--${u.badge}">${u.type}</span>
        <span class="desc"><a href="${u.href}">${EterCommon.escapeHtml(u.label)}</a></span>
      </div>
    `).join('');
  }

  function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  }
});
