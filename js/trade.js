document.addEventListener('DOMContentLoaded', async () => {
  const setupNotice = document.getElementById('tr-setup-notice');
  const appRoot = document.getElementById('tr-app');

  if (!window.ETER_FIREBASE_CONFIGURED) {
    setupNotice.style.display = '';
    appRoot.style.display = 'none';
    return;
  }
  setupNotice.style.display = 'none';
  appRoot.style.display = '';

  // ---- Firebase 초기화 (compat SDK, 스크립트 태그로 로드됨) ----
  firebase.initializeApp(window.ETER_FIREBASE_CONFIG);
  const db = firebase.firestore();
  const postsRef = db.collection('trade_posts');

  const listEl = document.getElementById('tr-list');
  const countEl = document.getElementById('tr-count');
  const searchInput = document.getElementById('tr-search');
  const typeButtons = document.querySelectorAll('#tr-type .chip');
  const categorySelect = document.getElementById('tr-category');
  const hideDoneCheckbox = document.getElementById('tr-hide-done');
  const form = document.getElementById('tr-form');
  const formToggleBtn = document.getElementById('tr-form-toggle');
  const formBox = document.getElementById('tr-form-box');

  const state = { q: '', type: '', category: '', hideDone: false };
  let allPosts = [];

  formToggleBtn.addEventListener('click', () => {
    formBox.style.display = formBox.style.display === 'none' ? '' : 'none';
  });

  // ---- 글 목록 실시간 구독 ----
  postsRef.orderBy('createdAt', 'desc').limit(200).onSnapshot((snapshot) => {
    allPosts = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    render();
  }, (err) => {
    console.error(err);
    listEl.innerHTML = `<div class="empty-state"><strong>게시글을 불러오지 못했습니다</strong>Firebase 설정 또는 보안 규칙을 확인해주세요.</div>`;
  });

  function matches(p) {
    if (state.type && p.type !== state.type) return false;
    if (state.category && p.category !== state.category) return false;
    if (state.hideDone && p.status === 'done') return false;
    if (state.q) {
      const hay = `${p.itemName} ${p.description || ''}`.toLowerCase();
      if (!hay.includes(state.q)) return false;
    }
    return true;
  }

  function timeAgo(ts) {
    if (!ts || !ts.toDate) return '';
    const diff = Date.now() - ts.toDate().getTime();
    const m = Math.floor(diff / 60000);
    if (m < 1) return '방금 전';
    if (m < 60) return `${m}분 전`;
    const h = Math.floor(m / 60);
    if (h < 24) return `${h}시간 전`;
    return `${Math.floor(h / 24)}일 전`;
  }

  function render() {
    const filtered = allPosts.filter(matches);
    countEl.textContent = `${filtered.length} / ${allPosts.length}건`;
    listEl.innerHTML = filtered.length
      ? filtered.map(postRow).join('')
      : `<div class="empty-state"><strong>조건에 맞는 게시글이 없습니다</strong>첫 글을 올려보세요.</div>`;

    filtered.forEach(p => {
      const titleEl = document.getElementById(`tr-title-${p.id}`);
      const bodyEl = document.getElementById(`tr-body-${p.id}`);
      if (titleEl && bodyEl) {
        titleEl.addEventListener('click', () => {
          const wasOpen = bodyEl.classList.contains('is-open');
          bodyEl.classList.toggle('is-open', !wasOpen);
          if (!wasOpen) loadComments(p.id);
        });
      }
      const doneBtn = document.getElementById(`tr-done-${p.id}`);
      if (doneBtn) doneBtn.addEventListener('click', () => markDone(p));
      const delBtn = document.getElementById(`tr-del-${p.id}`);
      if (delBtn) delBtn.addEventListener('click', () => deletePost(p));
      const cForm = document.getElementById(`tr-cform-${p.id}`);
      if (cForm) cForm.addEventListener('submit', (e) => submitComment(e, p.id));
    });
  }

  function postRow(p) {
    const typeLabel = p.type === 'sell' ? '판매' : '구매';
    const typeBadge = p.type === 'sell' ? 'badge--olive' : 'badge--illegal';
    return `
      <div class="trade-post ${p.status === 'done' ? 'is-done' : ''}">
        <div class="trade-post__top">
          <span class="badge ${typeBadge}">${typeLabel}</span>
          <span class="badge">${EterCommon.escapeHtml(p.category || '기타')}</span>
          <span class="trade-post__title" id="tr-title-${p.id}">${EterCommon.escapeHtml(p.itemName)}</span>
          <span class="trade-post__price">${EterCommon.fmt(p.price)} El</span>
        </div>
        <div class="trade-post__meta">${EterCommon.escapeHtml(p.nickname)} · ${timeAgo(p.createdAt)}</div>
        <div class="trade-post__body" id="tr-body-${p.id}">
          <div class="trade-post__desc">${EterCommon.escapeHtml(p.description || '')}</div>
          <div class="trade-post__meta" style="margin-bottom:10px;">연락 방법: ${EterCommon.escapeHtml(p.contact || '-')}</div>
          <div style="display:flex; gap:8px; margin-bottom:14px;">
            ${p.status !== 'done' ? `<button class="btn btn--ghost btn--sm" id="tr-done-${p.id}">거래완료 처리</button>` : ''}
            <button class="btn btn--danger btn--sm" id="tr-del-${p.id}">삭제</button>
          </div>
          <div class="comment-list" id="tr-comments-${p.id}"><div class="card__meta">댓글 불러오는 중...</div></div>
          <form class="comment-form" id="tr-cform-${p.id}">
            <input type="text" name="nickname" placeholder="닉네임" maxlength="20" required style="flex:0 0 100px;">
            <input type="text" name="content" placeholder="댓글 (연락 방법 등)" maxlength="300" required>
            <button type="submit" class="btn btn--sm">등록</button>
          </form>
        </div>
      </div>
    `;
  }

  function loadComments(postId) {
    const box = document.getElementById(`tr-comments-${postId}`);
    if (!box) return;
    postsRef.doc(postId).collection('comments').orderBy('createdAt', 'asc').limit(100)
      .onSnapshot((snap) => {
        if (snap.empty) {
          box.innerHTML = `<div class="card__meta">아직 댓글이 없습니다.</div>`;
          return;
        }
        box.innerHTML = snap.docs.map(d => {
          const c = d.data();
          return `<div class="comment-item"><b>${EterCommon.escapeHtml(c.nickname)}</b> ${EterCommon.escapeHtml(c.content)}<time>${timeAgo(c.createdAt)}</time></div>`;
        }).join('');
      });
  }

  async function submitComment(e, postId) {
    e.preventDefault();
    const f = e.target;
    const nickname = f.nickname.value.trim();
    const content = f.content.value.trim();
    if (!nickname || !content) return;
    try {
      await postsRef.doc(postId).collection('comments').add({
        nickname, content, createdAt: firebase.firestore.FieldValue.serverTimestamp(),
      });
      f.reset();
    } catch (err) {
      alert('댓글 등록에 실패했습니다: ' + err.message);
    }
  }

  async function markDone(p) {
    const pw = prompt('삭제/수정 비밀번호를 입력하세요.');
    if (pw == null) return;
    if (pw !== p.editKey) { alert('비밀번호가 일치하지 않습니다.'); return; }
    await postsRef.doc(p.id).update({ status: 'done', doneAt: firebase.firestore.FieldValue.serverTimestamp() });
  }

  async function deletePost(p) {
    const pw = prompt('삭제 비밀번호를 입력하세요.');
    if (pw == null) return;
    if (pw !== p.editKey) { alert('비밀번호가 일치하지 않습니다.'); return; }
    if (!confirm('정말 삭제하시겠어요?')) return;
    await postsRef.doc(p.id).delete();
  }

  // ---- 글쓰기 ----
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.target;
    const data = {
      type: f.type.value,
      category: f.category.value,
      itemName: f.itemName.value.trim(),
      price: parseInt(f.price.value || '0', 10),
      description: f.description.value.trim(),
      nickname: f.nickname.value.trim(),
      contact: f.contact.value.trim(),
      editKey: f.editKey.value,
      status: 'open',
      createdAt: firebase.firestore.FieldValue.serverTimestamp(),
    };
    if (!data.itemName || !data.nickname || !data.editKey) {
      alert('아이템명, 닉네임, 비밀번호는 필수입니다.');
      return;
    }
    try {
      await postsRef.add(data);
      f.reset();
      formBox.style.display = 'none';
    } catch (err) {
      alert('등록에 실패했습니다: ' + err.message);
    }
  });

  // ---- 필터 이벤트 ----
  searchInput.addEventListener('input', EterCommon.debounce((e) => {
    state.q = e.target.value.trim().toLowerCase();
    render();
  }));
  typeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      typeButtons.forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      state.type = btn.dataset.type;
      render();
    });
  });
  categorySelect.addEventListener('change', (e) => { state.category = e.target.value; render(); });
  hideDoneCheckbox.addEventListener('change', (e) => { state.hideDone = e.target.checked; render(); });

  // ---- 시세 페이지에서 넘어온 딥링크 지원 (?item=이름) ----
  const params = new URLSearchParams(location.search);
  const itemParam = params.get('item');
  if (itemParam) {
    searchInput.value = itemParam;
    state.q = itemParam.trim().toLowerCase();
  }
});
