// ⚠️ 이 파일을 Firebase 콘솔에서 발급받은 값으로 채워주세요.
// README.md의 "거래 게시판(Firebase) 설정하기" 섹션을 참고하세요.
//
// Firebase 콘솔 > 프로젝트 설정 > 일반 > "내 앱" > SDK 설정 및 구성 에서
// 아래와 동일한 형태의 객체를 복사해서 그대로 덮어쓰면 됩니다.

window.ETER_FIREBASE_CONFIG = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// 설정이 완료되었는지 자동으로 판별하기 위한 플래그입니다. 수정하지 마세요.
window.ETER_FIREBASE_CONFIGURED = window.ETER_FIREBASE_CONFIG.apiKey !== "YOUR_API_KEY";
