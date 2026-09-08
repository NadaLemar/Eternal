// 아이디+비밀번호 로그인 래퍼
// Firebase Auth는 이메일 형식이 필요하므로, 내부적으로 "아이디@eterpedia.local" 형태의
// 합성 이메일을 사용합니다. 사용자에게는 항상 "아이디"만 보이고 입력받습니다.
const EterAuth = (() => {
  let auth = null;

  function ensureInit() {
    if (!auth) {
      if (!firebase.apps.length) firebase.initializeApp(window.ETER_FIREBASE_CONFIG);
      auth = firebase.auth();
    }
    return auth;
  }

  function usernameToEmail(username) {
    const clean = username.trim().toLowerCase();
    return `${clean}@eterpedia.local`;
  }

  function validUsername(username) {
    return /^[a-z0-9_]{4,20}$/i.test(username.trim());
  }

  async function signUp(username, password) {
    if (!validUsername(username)) {
      throw new Error('아이디는 영문/숫자/밑줄 4~20자로 입력해주세요.');
    }
    if (password.length < 6) {
      throw new Error('비밀번호는 6자 이상이어야 합니다.');
    }
    const a = ensureInit();
    const cred = await a.createUserWithEmailAndPassword(usernameToEmail(username), password);
    const db = firebase.firestore();
    await db.collection('users').doc(cred.user.uid).set({
      username: username.trim(),
      createdAt: firebase.firestore.FieldValue.serverTimestamp(),
    });
    return cred.user;
  }

  async function logIn(username, password) {
    const a = ensureInit();
    const cred = await a.signInWithEmailAndPassword(usernameToEmail(username), password);
    return cred.user;
  }

  async function logOut() {
    const a = ensureInit();
    await a.signOut();
  }

  function onAuthChange(callback) {
    const a = ensureInit();
    return a.onAuthStateChanged(callback);
  }

  function friendlyError(err) {
    const map = {
      'auth/email-already-in-use': '이미 사용 중인 아이디입니다.',
      'auth/invalid-email': '아이디 형식이 올바르지 않습니다.',
      'auth/weak-password': '비밀번호가 너무 약합니다 (6자 이상).',
      'auth/user-not-found': '존재하지 않는 아이디입니다.',
      'auth/wrong-password': '비밀번호가 일치하지 않습니다.',
      'auth/invalid-credential': '아이디 또는 비밀번호가 일치하지 않습니다.',
      'auth/too-many-requests': '시도가 너무 많습니다. 잠시 후 다시 시도해주세요.',
    };
    return map[err.code] || err.message || '알 수 없는 오류가 발생했습니다.';
  }

  return { signUp, logIn, logOut, onAuthChange, friendlyError, ensureInit };
})();
