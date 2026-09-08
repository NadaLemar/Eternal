document.addEventListener('DOMContentLoaded', async () => {
  const setupNotice = document.getElementById('mk-setup-notice');
  const appRoot = document.getElementById('mk-app');

  if (!window.ETER_FIREBASE_CONFIGURED) {
    setupNotice.style.display = '';
    appRoot.style.display = 'none';
    return;
  }
  setupNotice.style.display = 'none';
  appRoot.style.display = '';

  // trade.html과 같은 Firebase 프로젝트/컬렉션을 사용합니다.
  if (!firebase.apps.length) {
    firebase.initializeApp(window.ETER_FIREBASE_CONFIG);
  }
  const db = firebase.firestore();
  const postsRef = db.collection('trade_posts');

  const listEl = document.getElementById('mk-list');
  const countEl = document.getElementById('mk-count');
  const searchInput = document.getElementById('mk-search');
  const categorySelect = document.getElementById('mk-category');
  const sortSelect = document.getElementById('mk-sort');

  const state = { q: '', category: '', sort: 'recent' };
  let allPosts = [];

  postsRef.orderBy('createdAt', 'desc').limit(500).onSnapshot((snapshot) => {
    allPosts = snapshot.docs.map(doc => doc.data());
    render();
  }, (err) => {
    console.error(err);
    listEl.innerHTML = `<div class="empty-state"><strong>시세 데이터를 불러오지 못했습니다</strong>Firebase 설정 또는 보안 규칙을 확인해주세요.</div>`;
  });

  function tsMillis(ts) {
    return ts && ts.toMillis ? ts.toMillis() : 0;
  }

  function timeAgo(ts) {
    if (!ts || !ts.toDate) return '-';
    const diff = Date.now() - ts.toDate().getTime();
    const m = Math.floor(diff / 60000);
    if (m < 1) return '방금 전';
    if (m < 60) return `${m}분 전`;
    const h = Math.floor(m / 60);
    if (h < 24) return `${h}시간 전`;
    return `${Math.floor(h / 24)}일 전`;
  }

  // ---- 아이템명 기준 집계 ----
  function aggregate(posts) {
    const groups = new Map();
    posts.forEach(p => {
      if (p.type !== 'sell' || !p.itemName) return;
      const key = p.itemName.trim();
      if (!key) return;
      if (!groups.has(key)) {
        groups.set(key, {
          itemName: key,
          category: p.category || '기타',
          activePrices: [],
          completedPrices: [], // { price, doneAt }
          latestListingAt: 0,
        });
      }
      const g = groups.get(key);
      g.latestListingAt = Math.max(g.latestListingAt, tsMillis(p.createdAt));
      if (p.status === 'done') {
        g.completedPrices.push({ price: p.price, doneAt: p.doneAt });
      } else {
        g.activePrices.push(p.price);
      }
    });

    return [...groups.values()].map(g => {
      const active = g.activePrices.filter(v => typeof v === 'number');
      const completed = g.completedPrices
        .filter(c => typeof c.price === 'number')
        .sort((a, b) => tsMillis(b.doneAt) - tsMillis(a.doneAt));

      const activeMin = active.length ? Math.min(...active) : null;
      const activeAvg = active.length ? Math.round(active.reduce((a, b) => a + b, 0) / active.length) : null;
      const lastDone = completed[0] || null;
      const completedAvg = completed.length
        ? Math.round(completed.reduce((a, c) => a + c.price, 0) / completed.length)
        : null;

      return {
        itemName: g.itemName,
        category: g.category,
        activeCount: active.length,
        activeMin,
        activeAvg,
        completedCount: completed.length,
        completedAvg,
        lastDonePrice: lastDone ? lastDone.price : null,
        lastDoneAt: lastDone ? lastDone.doneAt : null,
        latestListingAt: g.latestListingAt,
      };
    });
  }

  function matches(row) {
    if (state.category && row.category !== state.category) return false;
    if (state.q && !row.itemName.toLowerCase().includes(state.q)) return false;
    return true;
  }

  function sortRows(rows) {
    const arr = [...rows];
    switch (state.sort) {
      case 'priceHigh':
        arr.sort((a, b) => (b.lastDonePrice ?? b.activeMin ?? 0) - (a.lastDonePrice ?? a.activeMin ?? 0));
        break;
      case 'priceLow':
        arr.sort((a, b) => (a.lastDonePrice ?? a.activeMin ?? Infinity) - (b.lastDonePrice ?? b.activeMin ?? Infinity));
        break;
      case 'active':
        arr.sort((a, b) => b.activeCount - a.activeCount);
        break;
      default:
        arr.sort((a, b) => b.latestListingAt - a.latestListingAt);
    }
    return arr;
  }

  function row(r) {
    const refPrice = r.lastDonePrice != null ? r.lastDonePrice : r.activeMin;
    const refLabel = r.lastDonePrice != null ? '최근 체결가' : '최저 등록가';
    return `
      <tr style="border-top:1px solid var(--line);">
        <td style="padding:10px 12px; color:var(--paper);">
          ${EterCommon.escapeHtml(r.itemName)}
          <div class="card__meta" style="margin-top:2px;">${EterCommon.escapeHtml(r.category)}</div>
        </td>
        <td style="padding:10px 12px; text-align:right; font-family:var(--font-mono); color:var(--amber);">
          ${refPrice != null ? EterCommon.fmt(refPrice) + ' El' : '—'}
          <div class="card__meta" style="margin-top:2px;">${refLabel}</div>
        </td>
        <td style="padding:10px 12px; text-align:right; font-family:var(--font-mono); color:var(--paper-dim);">
          ${r.activeAvg != null ? EterCommon.fmt(r.activeAvg) + ' El' : '—'}
        </td>
        <td style="padding:10px 12px; text-align:right; font-family:var(--font-mono); color:var(--paper-dim);">
          ${r.activeCount}건
        </td>
        <td style="padding:10px 12px; text-align:right; font-family:var(--font-mono); color:var(--muted);">
          ${r.completedCount}건
        </td>
        <td style="padding:10px 12px; text-align:right; font-size:12px; color:var(--muted);">
          ${r.lastDoneAt ? timeAgo(r.lastDoneAt) : '-'}
        </td>
        <td style="padding:10px 12px; text-align:right;">
          <a class="btn btn--ghost btn--sm" href="trade.html?item=${encodeURIComponent(r.itemName)}">매물 보기</a>
        </td>
      </tr>
    `;
  }

  function render() {
    const rows = sortRows(aggregate(allPosts).filter(matches));
    countEl.textContent = `${rows.length}개 아이템`;
    listEl.innerHTML = rows.length
      ? rows.map(row).join('')
      : `<tr><td colspan="7"><div class="empty-state"><strong>집계할 판매글이 없습니다</strong>거래 게시판에 판매 글이 등록되면 여기에 시세가 표시됩니다.</div></td></tr>`;
  }

  searchInput.addEventListener('input', EterCommon.debounce((e) => {
    state.q = e.target.value.trim().toLowerCase();
    render();
  }));
  categorySelect.addEventListener('change', (e) => { state.category = e.target.value; render(); });
  sortSelect.addEventListener('change', (e) => { state.sort = e.target.value; render(); });
});
