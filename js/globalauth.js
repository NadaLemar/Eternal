// 사이트 전체 공통 로그인 상태 위젯 + 로그인/회원가입 모달
// 다른 페이지 스크립트(mypage.js, trade.js 등)는 아래 이벤트/API를 사용합니다:
//   - window.addEventListener('eterauth:change', (e) => { e.detail.user, e.detail.profile })
//   - window.EterAuthModal.open()
document.addEventListener('DOMContentLoaded', () => {
  if (!window.ETER_FIREBASE_CONFIGURED) return; // Firebase 미설정 시 위젯 숨김

  EterAuth.ensureInit();
  const db = firebase.firestore();

  // ---- 모달 마크업 주입 ----
  const modalHtml = `
    <div class="auth-modal-backdrop" id="ga-backdrop">
      <div class="auth-modal">
        <button class="auth-modal__close" id="ga-close" aria-label="닫기">×</button>
        <div class="chip-group" id="ga-tabs" style="margin-bottom:16px;">
          <button class="chip is-active" data-tab="login">로그인</button>
          <button class="chip" data-tab="signup">회원가입</button>
        </div>
        <form id="ga-login-form">
          <h2>로그인</h2>
          <div class="form-grid" style="grid-template-columns: 1fr;">
            <div class="form-field"><label>아이디</label><input type="text" name="username" maxlength="20" required autocomplete="username"></div>
            <div class="form-field"><label>비밀번호</label><input type="password" name="password" required autocomplete="current-password"></div>
          </div>
          <button type="submit" class="btn" style="width:100%;">로그인</button>
          <div id="ga-login-error" style="color:var(--rust); font-size:12.5px; margin-top:8px;"></div>
        </form>
        <form id="ga-signup-form" style="display:none;">
          <h2>회원가입</h2>
          <div class="form-grid" style="grid-template-columns: 1fr;">
            <div class="form-field"><label>아이디 (영문/숫자/밑줄 4~20자)</label><input type="text" name="username" maxlength="20" required autocomplete="username"></div>
            <div class="form-field"><label>비밀번호 (6자 이상)</label><input type="password" name="password" required autocomplete="new-password"></div>
          </div>
          <button type="submit" class="btn" style="width:100%;">회원가입</button>
          <div id="ga-signup-error" style="color:var(--rust); font-size:12.5px; margin-top:8px;"></div>
        </form>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);

  const backdrop = document.getElementById('ga-backdrop');
  const closeBtn = document.getElementById('ga-close');
  const tabs = document.querySelectorAll('#ga-tabs .chip');
  const loginForm = document.getElementById('ga-login-form');
  const signupForm = document.getElementById('ga-signup-form');

  function openModal() { backdrop.classList.add('is-open'); }
  function closeModal() { backdrop.classList.remove('is-open'); }
  closeBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', (e) => { if (e.target === backdrop) closeModal(); });

  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      tabs.forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      const isLogin = btn.dataset.tab === 'login';
      loginForm.style.display = isLogin ? '' : 'none';
      signupForm.style.display = isLogin ? 'none' : '';
    });
  });

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.target;
    const errEl = document.getElementById('ga-login-error');
    errEl.textContent = '';
    try {
      await EterAuth.logIn(f.username.value, f.password.value);
      closeModal();
      f.reset();
    } catch (err) {
      errEl.textContent = EterAuth.friendlyError(err);
    }
  });

  signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.target;
    const errEl = document.getElementById('ga-signup-error');
    errEl.textContent = '';
    try {
      await EterAuth.signUp(f.username.value, f.password.value);
      closeModal();
      f.reset();
    } catch (err) {
      errEl.textContent = EterAuth.friendlyError(err);
    }
  });

  window.EterAuthModal = { open: openModal, close: closeModal };

  // ---- 레일 상단 위젯 ----
  const slot = document.getElementById('global-auth-slot');

  function renderLoggedOut() {
    if (!slot) return;
    slot.innerHTML = `
      <div class="auth-widget">
        <button class="auth-widget__login-btn" id="ga-open-btn">로그인 / 회원가입</button>
      </div>
    `;
    document.getElementById('ga-open-btn').addEventListener('click', openModal);
  }

  function renderLoggedIn(username) {
    if (!slot) return;
    slot.innerHTML = `
      <div class="auth-widget">
        <div class="auth-widget__user">
          <span><span class="auth-widget__name">${EterCommon.escapeHtml(username)}</span>님</span>
          <button class="auth-widget__logout" id="ga-logout-btn">로그아웃</button>
        </div>
      </div>
    `;
    document.getElementById('ga-logout-btn').addEventListener('click', () => EterAuth.logOut());
  }

  renderLoggedOut(); // 초기 상태(확인 전)

  EterAuth.onAuthChange(async (user) => {
    if (user) {
      let username = user.email ? user.email.split('@')[0] : '회원';
      try {
        const doc = await db.collection('users').doc(user.uid).get();
        if (doc.exists && doc.data().username) username = doc.data().username;
      } catch (e) { /* 무시 */ }
      renderLoggedIn(username);
      window.dispatchEvent(new CustomEvent('eterauth:change', { detail: { user, username } }));
    } else {
      renderLoggedOut();
      window.dispatchEvent(new CustomEvent('eterauth:change', { detail: { user: null, username: null } }));
    }
  });
});
