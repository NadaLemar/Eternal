# EterPedia — 이터널시티 통합 기록보관소

이터널시티(Eternal City)의 무기, 퀘스트, 업적 등 게임 정보를 한곳에 정리하기 위한
정적(static) 웹사이트 뼈대입니다. 서버나 빌드 도구 없이 파일을 그대로 아무 웹 호스팅
(GitHub Pages, Netlify, Vercel, 카페24 등)에 올리면 바로 동작합니다.

## 폴더 구조

```
eterpedia/
├── index.html            홈 대시보드 (전체 카테고리 진입점)
├── weapons.html           무기 정보 — 완성된 페이지 (검색/필터 포함)
├── quests.html             퀘스트 — 완성된 페이지 (검색/카테고리 필터 포함)
├── achievements.html       업적·도전과제 — 완성된 페이지
├── armors.html / accessories.html / characters.html / regions.html
│                            아직 데이터가 없는 "준비중" 자리표시 페이지
├── css/style.css           전체 사이트 공통 스타일 (디자인 토큰 포함)
├── js/
│   ├── common.js           공통 유틸 (JSON 로드, 검색 디바운스 등)
│   ├── nav.js               모바일 메뉴 토글
│   ├── home.js               홈 통계/최근 업데이트 렌더링
│   ├── weapons.js             무기 목록 렌더링 및 필터
│   ├── quests.js               퀘스트 목록 렌더링 및 필터
│   └── achievements.js         업적 목록 렌더링 및 필터
├── data/
│   ├── weapons.json         무기 데이터 (실제 게임 수치 샘플 10종 포함)
│   ├── quests.json           퀘스트 데이터 ([예시] 표시된 자리표시 데이터)
│   └── achievements.json     업적 데이터 ([예시] 표시된 자리표시 데이터)
└── tools/                    페이지를 다시 생성할 때 쓰는 빌드 스크립트 (선택사항)
```

## 지금 상태

- **완성**: 홈페이지, 전체 메뉴 구조(좌측 레일 네비게이션), **무기(171종)·방어구(415종)·
  악세서리(77종)·코스튬(80종+강화표)** 전체 아이템 데이터베이스(출처: eterinfo.kr,
  이미지 포함), 퀘스트·업적 검색/필터, **제작 재료**(리마스터 반지 4종 재료표), **거래 게시판**
  (El 전용 판매/구매 게시판, Firebase 연동), **시세**(거래 게시판 데이터를 자동 집계한
  아이템별 시세표), **무기 강화/튜닝 계산기**와 **방어구 플러스업 효과 계산기**
  (확정 공식 기반, 사용자 제공 자료), **접두사·유니크 개조 참고 정보**,
  **아이템 상세페이지**(eterinfo.kr 스타일 강화/튜닝 실시간 계산), **사이트 전체
  공통 로그인**(아이디+비밀번호, 어느 페이지에서든 동일한 로그인 상태 유지)과
  **마이 캐릭터**(부위별 장비 슬롯, 실시간 합산 요약 — Firebase Auth 설정 필요)
- **실제 데이터 반영됨**:
  - `weapons.json` — eterinfo.kr 아이템 통합 목록 기반 CL 무기 전체 171종 (6~12등급,
    합법/불법 포함). 그중 mgame 공식 DB로 먼저 확인했던 31종은 명중/탄착/탄환/특수
    옵션 등 추가 정보가 함께 들어있습니다.
  - `armors.json` — 방어구·의류·방패 전체 415종 (일반/CL, 부위별 세부분류 포함)
  - `accessories.json` — 반지·목걸이·귀걸이·팔찌·벨트 등 악세서리 전체 77종
  - `costumes.json` — 날개의상 16종 × 공격형/치명형/체력형 = 48건의 강화단계 표
  - `costume_items.json` — 코스튬·날개 아이템 전체 목록 80종 (기본 스펙, 강화표와는
    별도로 코스튬 페이지 하단에 전체 목록으로 표시됩니다)
  - `plusup.json` — eterinfo.kr 기반 "일반" 종류 플러스업 확률표(+1~+15) 실제 반영,
    나머지 14종(원피스/변이/장인/명인/O.T/3~11급)은 탭 구조만 만들어두고 데이터 대기 중
  - `ring_materials.json` — 리마스터 반지 4종(거미/좀비/별/개미) 제작 단계별 재료
    수량표. 개미(껍질) 반지는 원본 스크린샷이 잘려 마지막 고유 재료 행이 없을 수
    있습니다.

  무기·방어구·악세서리·코스튬 데이터는 eterinfo.kr에서 제공받은 통합 아이템 목록을
  바탕으로 합니다. **아이템 이미지는 736개가 `images/` 폴더에 로컬로 저장되어 있어**
  더 이상 eterinfo.kr 서버에 핫링크하지 않습니다(사용자가 직접 원본 이미지를 모아
  제공). 이미지가 없는 7개 무기(CLW008401, CLW017001~017006)만 예외적으로
  eterinfo.kr 이미지를 그대로 참조합니다. 각 카드의 "원본 보기" 링크로 eterinfo.kr
  상세페이지로 이동할 수 있습니다.
- **[예시] 데이터**: `quests.json`, `achievements.json`은 구조를 보여주기 위한 자리표시
  데이터이므로 실제 게임 DB 내용으로 교체해야 합니다.
- **준비중 페이지**: 캐릭터·용병, 지역·어썰트는 자리표시 페이지만 만들어 두었습니다.
  데이터가 준비되면 `weapons.html`과 같은 방식으로
  채울 수 있습니다.

## 데이터 추가/수정 방법

이 사이트는 각 카테고리마다 `data/*.json` 파일 하나를 "데이터베이스"로 사용합니다.
새 항목을 추가하려면 해당 JSON 파일에 객체를 하나 더 넣기만 하면 됩니다. 코드 수정은
필요 없습니다.

### 무기 추가 예시 (`data/weapons.json`)

`primary`는 필수, `secondary`는 유탄런처 등 2차 공격 모드가 있는 무기에만 넣습니다
(없으면 `null`).

```json
{
  "id": "n032",
  "name": "[CL]New Weapon",
  "category1": "CL불법무기",
  "grade": 12,
  "type": "돌격소총",
  "size": "중형",
  "weight": 200,
  "primary": {
    "type": "돌격소총",
    "power": 20000,
    "fireRate": "300발/1분",
    "crit": 15,
    "accuracy": 30,
    "loadRate": 60,
    "ammo": ["일반탄", "철갑탄"],
    "shotCount": null,
    "features": []
  },
  "secondary": null,
  "updatedAt": "2026-09-07"
}
```

### 퀘스트 추가 예시 (`data/quests.json`)

```json
{
  "id": "q005",
  "name": "퀘스트 이름",
  "category": "메인",
  "levelReq": 25,
  "region": "지역명",
  "giver": "NPC 이름",
  "description": "퀘스트 설명",
  "objectives": ["진행 조건 1", "진행 조건 2"],
  "rewards": { "exp": 1000, "el": 500, "items": ["아이템명"] },
  "updatedAt": "2026-09-07"
}
```

### 코스튬(날개) 추가 예시 (`data/costumes.json`)

날개의상처럼 강화단계별 표를 갖는 장비는 다음 구조를 씁니다. `baseName`이 같은
항목끼리 `costumes.html`에서 자동으로 하나의 카드로 묶여 탭(공격형/치명형/체력형)으로
전환됩니다.

```json
{
  "id": "c049",
  "name": "[CL] 새 날개 (공격형)",
  "baseName": "[CL] 새 날개",
  "variant": "공격형",
  "category1": "CL",
  "gender": "여성",
  "category2": "날개의상",
  "weight": 1,
  "statLabel": "공격력",
  "levels": [
    { "stage": 0, "defensePct": 12, "statValue": 2, "evasion": 10 },
    { "stage": 1, "defensePct": 13, "statValue": 3, "evasion": 11 }
  ]
}
```

### 반지 제작 재료 추가 예시 (`data/ring_materials.json`)

`columnGroups`에 정의된 두 단계 구간(A: 1~5, B: 0~6)에 맞춰 각 재료의 수량을
배열로 넣습니다. 빈 칸은 `null`로 표시합니다.

```json
{
  "id": "newring",
  "name": "새 반지",
  "variant": "종류",
  "materials": [
    { "name": "재료 이름", "a": [30, 60, 100, 150, 210], "b": [10, 20, 30, 40, 50, 60, 70] }
  ]
}
```

### 업적 추가 예시 (`data/achievements.json`)

```json
{
  "id": "a005",
  "name": "업적 이름",
  "category": "전투",
  "description": "업적 설명",
  "condition": "달성 조건",
  "reward": "보상 내용",
  "points": 20,
  "updatedAt": "2026-09-07"
}
```

`id`는 각 파일 안에서 중복되지 않게만 하면 됩니다.

## mgame 공식 게임DB에서 데이터 옮기기

말씀하신 `https://eternalcity.mgame.com/info/gameDB/...` 페이지는 로봇 접근이
차단되어 있어 제가 직접 긁어올 수는 없었습니다. 아래 방법으로 데이터를 옮기는 걸
도와드릴 수 있습니다.

1. 게임DB 페이지에서 원하는 항목의 텍스트(무기명, 스탯, 퀘스트 설명 등)를 복사해서
   대화창에 붙여넣어 주세요.
2. 제가 위 JSON 구조에 맞춰 변환해서 `data/*.json`에 반영해 드릴게요.
3. 항목이 많다면 표/캡처를 여러 번에 나눠 보내주셔도 됩니다.

## 새 카테고리(방어구 등) 페이지를 채우는 법

1. `data/armors.json`처럼 새 JSON 데이터 파일을 만듭니다.
2. `weapons.html` + `js/weapons.js`를 복사해서 필드명만 바꿔줍니다.
3. `armors.html`(현재 자리표시 페이지)을 새로 만든 페이지로 교체합니다.
4. 좌측 레일의 `is-soon` 클래스와 "예정" 배지를 제거해 정식 메뉴로 전환합니다.

이 작업도 원하시면 다음 대화에서 이어서 진행해 드릴 수 있습니다.

## 로그인 시스템(사이트 전체 공통) 설정하기

로그인은 **특정 페이지 전용이 아니라 사이트 어디서나 동작하는 공통 기능**입니다.
왼쪽 레일 맨 위에 있는 "로그인 / 회원가입" 위젯(`js/globalauth.js`)이 모든 페이지에
공통으로 로드되고, 한 번 로그인하면 브라우저에 로그인 상태가 유지되어 다른 페이지로
이동해도 로그인 상태가 그대로 이어집니다. 거래 게시판 글쓰기, 마이 캐릭터 저장 모두
이 로그인 상태를 그대로 가져다 씁니다.

아이디+비밀번호로 가입/로그인하며, 내부적으로는 `아이디@eterpedia.local` 형태의
가짜 이메일을 만들어 Firebase Authentication에 등록합니다(`js/auth.js`). 실제
이메일을 수집하지 않습니다.

### 1. Firebase 프로젝트 만들기 (거래 게시판과 공용)

1. https://console.firebase.google.com 접속 후 구글 계정으로 로그인
2. "프로젝트 추가" → 프로젝트 이름 입력 (예: `eterpedia`) → 생성
3. Google Analytics는 꺼도 됩니다

### 2. Firestore 데이터베이스 만들기

1. 왼쪽 메뉴 **Firestore Database** → "데이터베이스 만들기"
2. 위치는 `asia-northeast3`(서울) 권장
3. 보안 규칙은 아래 3번 내용으로 바로 설정하는 것을 권장합니다

### 3. 이메일/비밀번호 로그인 활성화

1. 왼쪽 메뉴 **Authentication** → "시작하기"
2. **Sign-in method** 탭 → **이메일/비밀번호** 선택 → 사용 설정 → 저장

### 4. 보안 규칙 설정 (전체)

Firestore Database → 규칙(Rules) 탭에서 아래 내용 전체로 교체하고 "게시":

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // 거래 게시판: 글 작성자(uid)만 수정/삭제 가능
    match /trade_posts/{postId} {
      allow read: if true;
      allow create: if request.auth != null
        && request.resource.data.uid == request.auth.uid
        && request.resource.data.keys().hasAll(
            ['nickname','uid','type','category','itemName','price','description','contact','status','createdAt'])
        && request.resource.data.nickname is string && request.resource.data.nickname.size() <= 20
        && request.resource.data.itemName is string && request.resource.data.itemName.size() <= 60
        && request.resource.data.description is string && request.resource.data.description.size() <= 1000
        && request.resource.data.price is number && request.resource.data.price >= 0
        && request.resource.data.type in ['sell', 'buy'];
      allow update, delete: if request.auth != null && resource.data.uid == request.auth.uid;

      match /comments/{commentId} {
        allow read: if true;
        allow create: if request.auth != null
          && request.resource.data.uid == request.auth.uid
          && request.resource.data.keys().hasAll(['nickname','uid','content','createdAt'])
          && request.resource.data.nickname is string && request.resource.data.nickname.size() <= 20
          && request.resource.data.content is string && request.resource.data.content.size() <= 300;
        allow update, delete: if false;
      }
    }

    // 회원 정보: 본인만 생성/수정 가능
    match /users/{uid} {
      allow read: if true;
      allow create, update: if request.auth != null && request.auth.uid == uid;
      allow delete: if false;
    }

    // 캐릭터 저장: 본인만 생성/수정/삭제 가능
    match /characters/{uid} {
      allow read: if true;
      allow create, update: if request.auth != null && request.auth.uid == uid
        && request.resource.data.keys().hasAll(['name','level','trait']);
      allow delete: if request.auth != null && request.auth.uid == uid;
    }
  }
}
```

> **이전 버전과 달라진 점**: 예전에는 거래 게시판 글마다 "삭제 비밀번호"를 따로
> 입력받아 클라이언트에서만 비교했습니다. 이제는 로그인 자체가 소유권 증명이라,
> 글 작성자 본인(`uid` 일치)만 수정/삭제가 가능하도록 **서버(Firestore 규칙)에서
> 직접 검증**합니다. 훨씬 안전합니다.

### 5. 웹 앱 등록 및 설정값 붙여넣기

1. 프로젝트 설정(톱니바퀴) → 일반 탭 → "내 앱" → 웹 아이콘(`</>`) 클릭 → 앱 등록
2. 화면에 나오는 `firebaseConfig` 값을 복사해서 `js/firebase-config.js`에 붙여넣기

```js
window.ETER_FIREBASE_CONFIG = {
  apiKey: "복사한 값",
  authDomain: "복사한 값",
  projectId: "복사한 값",
  storageBucket: "복사한 값",
  messagingSenderId: "복사한 값",
  appId: "복사한 값"
};
```

저장 후 아무 페이지나 열어서 왼쪽 레일 맨 위에 "로그인 / 회원가입" 버튼이
보이는지 확인하세요. 회원가입 → 로그인 후에는 어느 페이지에서든 로그인 상태가
유지됩니다. 거래 게시판 글쓰기와 마이 캐릭터 저장 모두 이 상태를 그대로 사용합니다.


`js/firebase-config.js`는 거래 게시판 설정 때 이미 채워두셨다면 추가 작업이
필요 없습니다. `mypage.html`을 열어 회원가입 → 로그인 → 캐릭터 정보 입력 →
저장하기가 되는지 확인하세요.

## 아이템 상세페이지 (eterinfo.kr 스타일 실시간 계산기)

`item-detail.html?cat=weapons&id=CLW000800` 같은 주소로 접근하는 동적 페이지입니다.
무기/방어구/악세서리/코스튬 목록(`weapons.html` 등)의 카드에서 아이템 이름이나
"상세 · 계산기 열기" 링크를 누르면 자동으로 이동합니다.

- **무기**: 몸체 튜닝(기본~O.T) + 강화단계(노강~맥9강)를 선택하면 그 자리에서
  파괴력이 다시 계산되고, 계산 근거(breakdown)도 함께 보여줍니다.
- **방어구**: 재질(장인/명인/O.T) + 부위(일반/원피스/전신의상) + 플러스업 단계(0~15)를
  선택하면 공격력 증가율이 계산됩니다. CL 여부는 아이템 데이터에서 자동으로 반영됩니다.
- 계산에 쓰는 공식은 모두 `js/calcengine.js`의 확정된 공식이며, eterinfo.kr 원본
  페이지(`몸체선택`/`강화선택` 드롭다운 구조)와 같은 사용 흐름을 재현했습니다.

## 무기 강화/튜닝 · 방어구 플러스업 효과 계산기

사용자가 제공한 "이터널시티_강화계산식_Claude전달용" 자료의 확정 공식을 그대로 구현했습니다
(`js/calcengine.js`). 검증 결과:

- **무기 강화**: `기초 파괴력 × 몸체 튜닝 배율 × 강화단계 누적배율`. 실제 사이트에서
  개별로 가져온 21개 무기 값과 대조한 결과 **오차 ±2 이내**로 일치했습니다. 이 공식
  덕분에 개별 상세페이지를 열지 않고도 **171개 무기 전체**에 "이론상 최대강화피해량"을
  계산해 반영할 수 있었습니다(`maxEnhancedPowerEstimated` 필드, 실측값이 있는 항목은
  `maxEnhancedPower`를 그대로 유지).
- **방어구 플러스업 효과**: `등급계수 × 재질계수 × CL보정 × 부위보정 × 누적가중스텝`.
  스펙에 있는 예시(6등급/O.T/7플 → +22.5%)와 정확히 일치하는 걸 확인했습니다.
- **데미지 레인지**: `인벤창 공격력 × 0.88 × (크기·탄종·특수·스킬 보정)`을 기준으로
  일반/발화(×1.5)/크리티컬(×1.55)/헤드샷(×3.10)/크리티컬발화/헤드샷발화까지 6가지
  구간을 계산합니다. `[CL] 처형자의 검` 실측값(공격력 52,604 → 일반 46,292~69,438 ~
  헤드샷발화 215,256~322,884)과 **오차 없이 정확히 일치**했습니다. 다만 "인벤창
  공격력"(무기 파괴력에 체력/기술/템공합/업적공/해방공이 어떻게 반영되는지)을 구하는
  공식 자체는 아직 미확인이라, 계산기에서는 위 무기 계산 파괴력을 기본값으로 쓰고
  사용자가 실제 게임 화면의 공격력 숫자를 직접 입력해 덮어쓸 수 있게 했습니다
  (`calculateCharacterAttack`은 `NEEDS_VERIFICATION` 상태로 명시).
- 총열/손잡이/조준경(치명·탄착률·명중률에 영향)은 **효과는 확정**이지만 상한이나
  정수처리 규칙이 미확인이라 계산기에 포함하지 않았습니다. 접두사와 유니크 개조도
  정성적 효과만 표시하고 수치는 넣지 않았습니다(`data/armor_prefixes.json`,
  `data/weapon_unique_modifiers.json`) — 나중에 정확한 수치가 확인되면 알려주세요.

> ⚠️ 이 계산기의 "미확인" 표시는 실제로 근거가 없는 값이라는 뜻입니다. 절대 임의로
> 채워 넣지 않았으니, 정확한 수치를 알게 되시면 알려주시는 대로 반영하겠습니다.

## 거래 게시판 아이템명 자동완성

거래 게시판의 "아이템명" 입력란은 `weapons.json`, `armors.json`, `accessories.json`,
`costume_items.json`에 등록된 이름을 자동완성으로 제안합니다. 목록에 있는 이름을
그대로 선택하면 "카테고리" 항목도 자동으로 맞춰집니다. 이렇게 하면 시세 페이지에서
같은 아이템을 정확히 하나로 집계할 수 있습니다. 다만 자동완성은 강제가 아니라
제안일 뿐이라, 카탈로그에 없는 이름(예: 퀘스트 보상 아이템)도 자유롭게 입력할 수
있습니다.

## 시세 페이지는 어떻게 동작하나요

`market.html`은 별도의 데이터 입력 없이, 거래 게시판(`trade_posts` 컬렉션)에
등록된 글을 그대로 읽어서 아이템 이름 기준으로 자동 집계합니다. 그래서
거래 게시판과 **같은 Firebase 설정을 그대로 공유**하며, 위 설정을 한 번만 하면
두 페이지 모두 바로 동작합니다.

- **기준가**: 최근 거래완료 기록이 있으면 그 가격, 없으면 현재 등록된 판매글 중
  최저가를 보여줍니다.
- **등록 평균가**: 현재 판매중(거래완료 처리 전)인 글들의 평균 가격입니다.
- **누적 거래완료**: 지금까지 "거래완료" 처리된 횟수입니다.
- 아이템 이름은 띄어쓰기 등 사소한 차이도 다른 아이템으로 집계되므로, 이용자들이
  같은 이름으로 글을 올리도록 안내하면 시세가 더 정확해집니다.
- "매물 보기" 버튼을 누르면 거래 게시판으로 이동해 해당 아이템으로 자동 검색됩니다.

## 로컬에서 미리보기

별도 서버 없이 파일을 열어도 되지만, 브라우저 보안 정책상 `fetch()`로 JSON을
불러오는 부분이 `file://`에서 막힐 수 있어 아래처럼 간단한 로컬 서버 사용을
권장합니다.

```bash
cd eterpedia
python3 -m http.server 8000
# 브라우저에서 http://localhost:8000 접속
```

## 디자인 컨셉

폐허가 된 세계관에 맞춰 야전 정보 단말기(터미널)를 모티프로 한 다크 톤
디자인입니다. 올리브/러스트 색상, 각진 여백, 괘선 기반 레이아웃을 사용했습니다.
색상·폰트 값은 `css/style.css` 최상단 `:root` 변수에서 한번에 바꿀 수 있습니다.
