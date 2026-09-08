import re, os, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # .../eterpedia/tools
ROOT_DIR = os.path.dirname(BASE_DIR)                      # .../eterpedia

# 캐시 무력화용 버전 문자열. 배포할 때마다 값이 바뀌어 브라우저가 새 파일을 받아가도록 함.
CACHE_VERSION = str(int(time.time()))

with open(os.path.join(BASE_DIR, '_shell.html'), encoding='utf-8') as f:
    SHELL = f.read()

def shell_for(active_href):
    """rail 링크 중 active_href와 일치하는 항목에 is-active 클래스를 부여."""
    s = SHELL.replace('rail__link is-active', 'rail__link')  # 홈의 기본 active 제거
    # href="X" 를 가진 링크에 is-active 부여 (is-soon 항목 제외)
    pattern = re.compile(r'(<a class="rail__link)( is-soon)?(")( href="' + re.escape(active_href) + r'")')
    s = pattern.sub(lambda m: f'{m.group(1)} is-active{m.group(2) or ""}{m.group(3)}{m.group(4)}', s)
    return s

def bust(html):
    """로컬 css/js 참조에 ?v=CACHE_VERSION 을 붙여 캐시를 무력화 (외부 CDN 링크는 건드리지 않음).
    이미 버전 쿼리가 붙어있으면 먼저 제거한 뒤 새로 붙여서 재실행해도 항상 최신 버전이 되게 함."""
    html = re.sub(r'((?:href|src)="(?:css|js)/[\w\-./]+\.(?:css|js))\?v=\d+"', r'\1"', html)
    html = re.sub(r'(href="css/[\w\-./]+\.css)"', rf'\1?v={CACHE_VERSION}"', html)
    html = re.sub(r'(src="js/[\w\-./]+\.js)"', rf'\1?v={CACHE_VERSION}"', html)
    return html

PAGE_HEAD = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — EterPedia</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
{shell}
  <!-- ============ 본문 ============ -->
  <main class="main">
{body}
  </main>
</div>

<script src="js/nav.js"></script>
<script src="js/common.js"></script>
<script src="js/firebase-config.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-firestore-compat.js"></script>
<script src="js/auth.js"></script>
<script src="js/globalauth.js"></script>
{scripts}
</body>
</html>
"""

def write_page(filename, title, desc, active_href, body, scripts=""):
    html = PAGE_HEAD.format(
        title=title, desc=desc, shell=shell_for(active_href), body=body, scripts=scripts
    )
    html = bust(html)
    out_path = os.path.join(ROOT_DIR, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', out_path)

# ---------------------------------------------------------------------------
# 무기 정보
# ---------------------------------------------------------------------------
weapons_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">ITEM DATABASE / WEAPONS</div>
      <h1>무기 정보</h1>
      <p>이터널시티 CL 무기 전체 목록입니다. 타입 탭과 검색/필터로 원하는 무기를 빠르게 찾아보세요. (출처: eterinfo.kr)</p>
    </div>

    <div class="chip-group" id="w-tabs" style="margin-bottom:16px;"></div>

    <div class="toolbar">
      <div class="toolbar__search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
        <input type="text" id="w-search" placeholder="무기 이름으로 검색...">
      </div>
      <select id="w-cat1"><option value="">전체 분류</option></select>
      <select id="w-grade"><option value="">전체 등급</option></select>
      <select id="w-range"><option value="">근거리/원거리 전체</option></select>
      <span class="toolbar__count" id="w-count"></span>
    </div>

    <div class="grid" id="w-grid">
      <div class="empty-state"><strong>불러오는 중...</strong></div>
    </div>

    <div class="section-title" style="margin-top:44px;">
      <h2>유니크 개조 정보</h2>
      <span class="section-title__note">정확한 수치 미확인 — 효과 방향만 표시</span>
    </div>
    <div id="unique-list" class="cat-grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 20px;"></div>
"""
write_page('weapons.html', '무기 정보', '이터널시티 무기 등급별·타입별 스펙과 강화 정보.',
           'weapons.html', weapons_body,
           '<script src="js/itemgrid.js"></script>\n<script src="js/weapons.js"></script>\n<script src="js/weaponunique.js"></script>')

# ---------------------------------------------------------------------------
# 코스튬 · 날개
# ---------------------------------------------------------------------------
costumes_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">ITEM DATABASE / COSTUMES</div>
      <h1>코스튬 · 날개</h1>
      <p>날개의상 강화단계별 방어력·부가 스탯·회피도 수치를 한눈에 비교하세요. 카드의 탭을 눌러 공격형/치명형/체력형을 전환할 수 있습니다.</p>
    </div>

    <div class="toolbar">
      <div class="toolbar__search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
        <input type="text" id="c-search" placeholder="코스튬 이름으로 검색...">
      </div>
      <select id="c-category2"><option value="">전체 분류</option></select>
      <div class="chip-group" id="c-variant">
        <button class="chip is-active" data-variant="">전체</button>
        <button class="chip" data-variant="공격형">공격형</button>
        <button class="chip" data-variant="치명형">치명형</button>
        <button class="chip" data-variant="체력형">체력형</button>
      </div>
      <span class="toolbar__count" id="c-count"></span>
    </div>

    <div class="grid" id="c-grid" style="grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));">
      <div class="empty-state"><strong>불러오는 중...</strong></div>
    </div>

    <div class="section-title" style="margin-top:44px;">
      <h2>전체 코스튬 · 날개 아이템 목록</h2>
      <span class="section-title__note">출처: eterinfo.kr</span>
    </div>

    <div class="chip-group" id="ci-tabs" style="margin-bottom:16px;"></div>

    <div class="toolbar">
      <div class="toolbar__search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
        <input type="text" id="ci-search" placeholder="이름으로 검색...">
      </div>
      <select id="ci-grade"><option value="">전체 등급</option></select>
      <span class="toolbar__count" id="ci-count"></span>
    </div>

    <div class="grid" id="ci-grid">
      <div class="empty-state"><strong>불러오는 중...</strong></div>
    </div>
"""
write_page('costumes.html', '코스튬 · 날개', '이터널시티 날개의상 강화단계별 방어력/스탯/회피도 정보.',
           'costumes.html', costumes_body,
           '<script src="js/costumes.js"></script>\n'
           '<script src="js/itemgrid.js"></script>\n<script src="js/costume-items.js"></script>')

# ---------------------------------------------------------------------------
# 제작 재료 (리마스터 반지 재료)
# ---------------------------------------------------------------------------
ring_materials_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">ITEM DATABASE / CRAFTING MATERIALS</div>
      <h1>제작 재료</h1>
      <p>리마스터 반지 제작에 필요한 단계별 재료 수량을 확인하세요. 반지마다 재료 이름은 다르지만 같은 위치의 재료는 같은 등급의 소재입니다.</p>
    </div>

    <div class="toolbar" style="border-bottom:none; padding-bottom:0; margin-bottom:18px;">
      <div class="chip-group" id="rm-ring"></div>
      <span class="toolbar__count" id="rm-hand"></span>
    </div>

    <div id="rm-note" class="placeholder" style="display:none; padding:20px; text-align:left; margin-bottom:20px;"></div>

    <div style="overflow-x:auto; border:1px solid var(--line);">
      <table style="width:100%; border-collapse:collapse; font-size:12.5px;">
        <thead id="rm-thead"></thead>
        <tbody id="rm-tbody"></tbody>
      </table>
    </div>
"""
write_page('ring-materials.html', '제작 재료', '이터널시티 리마스터 반지 제작 재료 단계별 수량표.',
           'ring-materials.html', ring_materials_body, '<script src="js/ring-materials.js"></script>')

# ---------------------------------------------------------------------------
# 거래 게시판
# ---------------------------------------------------------------------------
trade_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">COMMUNITY / TRADE BOARD</div>
      <h1>거래 게시판</h1>
      <p>El(게임 내 화폐) 기준으로 판다/삽니다 글을 올리고, 댓글로 연락을 주고받으세요. 현금(RMT) 거래는 취급하지 않습니다.</p>
    </div>

    <div id="tr-setup-notice" class="setup-notice" style="display:none;">
      <strong style="color:var(--paper); display:block; margin-bottom:8px;">거래 게시판을 사용하려면 Firebase 설정이 필요합니다</strong>
      아직 <code>js/firebase-config.js</code>가 기본값 그대로예요. README.md의
      "거래 게시판(Firebase) 설정하기" 섹션을 따라 무료 Firebase 프로젝트를 만들고
      설정값을 붙여넣으면 이 페이지가 바로 동작합니다.
    </div>

    <div id="tr-app">
      <div class="toolbar">
        <div class="chip-group" id="tr-type">
          <button class="chip is-active" data-type="">전체</button>
          <button class="chip" data-type="sell">판매</button>
          <button class="chip" data-type="buy">구매</button>
        </div>
        <select id="tr-category">
          <option value="">전체 카테고리</option>
          <option value="무기">무기</option>
          <option value="코스튬">코스튬·날개</option>
          <option value="방어구">방어구</option>
          <option value="악세서리">악세서리</option>
          <option value="제작재료">제작 재료</option>
          <option value="기타">기타</option>
        </select>
        <div class="toolbar__search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
          <input type="text" id="tr-search" placeholder="아이템 이름으로 검색...">
        </div>
        <label style="display:flex; align-items:center; gap:6px; font-size:12.5px; color:var(--muted);">
          <input type="checkbox" id="tr-hide-done"> 거래완료 숨기기
        </label>
        <span class="toolbar__count" id="tr-count"></span>
      </div>

      <div id="tr-login-required" class="login-required" style="display:none; margin-bottom:20px;">
        <p>글을 쓰려면 로그인이 필요합니다.</p>
        <button class="btn" id="tr-open-login">로그인 / 회원가입</button>
      </div>

      <button class="btn" id="tr-form-toggle" style="margin-bottom:16px; display:none;">+ 새 글 작성</button>

      <div id="tr-form-box" style="display:none; border:1px solid var(--line); padding:18px; margin-bottom:28px;">
        <form id="tr-form">
          <div class="form-grid">
            <div class="form-field">
              <label>구분</label>
              <select name="type" required>
                <option value="sell">판매</option>
                <option value="buy">구매</option>
              </select>
            </div>
            <div class="form-field">
              <label>카테고리</label>
              <select name="category" required>
                <option value="무기">무기</option>
                <option value="코스튬">코스튬·날개</option>
                <option value="방어구">방어구</option>
                <option value="악세서리">악세서리</option>
                <option value="제작재료">제작 재료</option>
                <option value="기타">기타</option>
              </select>
            </div>
            <div class="form-field">
              <label>아이템명</label>
              <input type="text" name="itemName" id="tr-itemname" maxlength="60" required list="tr-item-catalog" placeholder="입력 시 등록된 아이템명이 자동완성됩니다" autocomplete="off">
              <datalist id="tr-item-catalog"></datalist>
            </div>
            <div class="form-field">
              <label>가격 (El)</label>
              <input type="number" name="price" min="0" required>
            </div>
            <div class="form-field">
              <label>연락 방법 (게임 닉네임/디스코드 등)</label>
              <input type="text" name="contact" maxlength="80" required>
            </div>
            <div class="form-field full">
              <label>상세 설명</label>
              <textarea name="description" rows="3" maxlength="1000"></textarea>
            </div>
          </div>
          <button type="submit" class="btn">등록하기</button>
        </form>
      </div>

      <div id="tr-list">
        <div class="empty-state"><strong>불러오는 중...</strong></div>
      </div>
    </div>
"""
write_page('trade.html', '거래 게시판', 'El 기준 이터널시티 아이템 판매/구매 게시판.',
           'trade.html', trade_body,
                                                       '<script src="js/trade.js"></script>')

# ---------------------------------------------------------------------------
# 시세
# ---------------------------------------------------------------------------
market_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">COMMUNITY / MARKET PRICE</div>
      <h1>시세</h1>
      <p>거래 게시판에 등록된 실제 판매글과 거래완료 기록을 집계한 아이템별 시세입니다. 별도로 입력하는 값이 아니라, 게시판 데이터가 쌓일수록 자동으로 정확해집니다.</p>
    </div>

    <div id="mk-setup-notice" class="setup-notice" style="display:none;">
      <strong style="color:var(--paper); display:block; margin-bottom:8px;">시세 페이지를 사용하려면 Firebase 설정이 필요합니다</strong>
      거래 게시판과 같은 데이터베이스를 사용합니다. README.md의
      "거래 게시판(Firebase) 설정하기"를 먼저 완료해주세요.
    </div>

    <div id="mk-app">
      <div class="toolbar">
        <div class="toolbar__search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
          <input type="text" id="mk-search" placeholder="아이템 이름으로 검색...">
        </div>
        <select id="mk-category">
          <option value="">전체 카테고리</option>
          <option value="무기">무기</option>
          <option value="코스튬">코스튬·날개</option>
          <option value="방어구">방어구</option>
          <option value="악세서리">악세서리</option>
          <option value="제작재료">제작 재료</option>
          <option value="기타">기타</option>
        </select>
        <select id="mk-sort">
          <option value="recent">최근 등록순</option>
          <option value="priceHigh">가격 높은순</option>
          <option value="priceLow">가격 낮은순</option>
          <option value="active">매물 많은순</option>
        </select>
        <span class="toolbar__count" id="mk-count"></span>
      </div>

      <div style="overflow-x:auto; border:1px solid var(--line);">
        <table style="width:100%; border-collapse:collapse; font-size:13px;">
          <thead>
            <tr style="background:var(--panel-raised); text-align:right; font-family:var(--font-mono); font-size:12px; color:var(--muted);">
              <th style="text-align:left; padding:10px 12px;">아이템</th>
              <th style="padding:10px 12px;">기준가</th>
              <th style="padding:10px 12px;">등록 평균가</th>
              <th style="padding:10px 12px;">판매중</th>
              <th style="padding:10px 12px;">누적 거래완료</th>
              <th style="padding:10px 12px;">최근 체결</th>
              <th style="padding:10px 12px;"></th>
            </tr>
          </thead>
          <tbody id="mk-list">
            <tr><td colspan="7"><div class="empty-state"><strong>불러오는 중...</strong></div></td></tr>
          </tbody>
        </table>
      </div>
    </div>
"""
write_page('market.html', '시세', '거래 게시판 데이터를 집계한 이터널시티 아이템 시세.',
           'market.html', market_body,
                                                       '<script src="js/market.js"></script>')

# ---------------------------------------------------------------------------
# 퀘스트
# ---------------------------------------------------------------------------
quests_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">PROGRESSION / QUESTS</div>
      <h1>퀘스트</h1>
      <p>메인·서브·일일·이벤트 퀘스트의 진행 조건과 보상을 정리했습니다.</p>
    </div>

    <div class="toolbar">
      <div class="toolbar__search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
        <input type="text" id="q-search" placeholder="퀘스트 이름/지역으로 검색...">
      </div>
      <div class="chip-group" id="q-category">
        <button class="chip is-active" data-cat="">전체</button>
        <button class="chip" data-cat="메인">메인</button>
        <button class="chip" data-cat="서브">서브</button>
        <button class="chip" data-cat="일일">일일</button>
        <button class="chip" data-cat="이벤트">이벤트</button>
      </div>
      <span class="toolbar__count" id="q-count"></span>
    </div>

    <div id="q-list">
      <div class="empty-state"><strong>불러오는 중...</strong></div>
    </div>
"""
write_page('quests.html', '퀘스트', '이터널시티 메인/서브/일일/이벤트 퀘스트 진행 조건과 보상 정리.',
           'quests.html', quests_body, '<script src="js/quests.js"></script>')

# ---------------------------------------------------------------------------
# 업적
# ---------------------------------------------------------------------------
achievements_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">PROGRESSION / ACHIEVEMENTS</div>
      <h1>업적 · 도전과제</h1>
      <p>달성 조건, 보상, 획득 팁을 카테고리별로 정리했습니다.</p>
    </div>

    <div class="toolbar">
      <div class="toolbar__search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
        <input type="text" id="a-search" placeholder="업적 이름으로 검색...">
      </div>
      <select id="a-category"><option value="">전체 카테고리</option></select>
      <span class="toolbar__count" id="a-count"></span>
    </div>

    <div id="a-list">
      <div class="empty-state"><strong>불러오는 중...</strong></div>
    </div>
"""
write_page('achievements.html', '업적 · 도전과제', '이터널시티 업적/도전과제 달성 조건과 보상 정리.',
           'achievements.html', achievements_body, '<script src="js/achievements.js"></script>')

# ---------------------------------------------------------------------------
# 방어구
# ---------------------------------------------------------------------------
armors_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">ITEM DATABASE / ARMORS</div>
      <h1>방어구</h1>
      <p>부위별 탭으로 방어구·의류·방패를 확인하세요. (출처: eterinfo.kr)</p>
    </div>

    <div class="chip-group" id="ar-tabs" style="margin-bottom:16px; flex-wrap:wrap;"></div>

    <div class="toolbar">
      <div class="toolbar__search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
        <input type="text" id="ar-search" placeholder="이름으로 검색...">
      </div>
      <select id="ar-cat1"><option value="">전체 분류</option></select>
      <select id="ar-grade"><option value="">전체 등급</option></select>
      <span class="toolbar__count" id="ar-count"></span>
    </div>

    <div class="grid" id="ar-grid">
      <div class="empty-state"><strong>불러오는 중...</strong></div>
    </div>

    <div class="section-title" style="margin-top:44px;">
      <h2>접두사 정보</h2>
      <span class="section-title__note">정확한 수치 미확인 — 효과 방향만 표시</span>
    </div>
    <div class="chip-group" id="prefix-tabs" style="margin-bottom:16px;"></div>
    <div id="prefix-list" class="cat-grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 20px;"></div>
"""
write_page('armors.html', '방어구', '이터널시티 방어구·의류·방패 부위별 전체 목록.',
           'armors.html', armors_body,
           '<script src="js/itemgrid.js"></script>\n<script src="js/armors.js"></script>\n<script src="js/armorprefix.js"></script>')

# ---------------------------------------------------------------------------
# 악세서리
# ---------------------------------------------------------------------------
accessories_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">ITEM DATABASE / ACCESSORIES</div>
      <h1>악세서리</h1>
      <p>반지·목걸이·귀걸이·팔찌·벨트 등 악세서리 전체 목록입니다. (출처: eterinfo.kr)</p>
    </div>

    <div class="chip-group" id="ac-tabs" style="margin-bottom:16px; flex-wrap:wrap;"></div>

    <div class="toolbar">
      <div class="toolbar__search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
        <input type="text" id="ac-search" placeholder="이름으로 검색...">
      </div>
      <select id="ac-cat1"><option value="">전체 분류</option></select>
      <select id="ac-grade"><option value="">전체 등급</option></select>
      <span class="toolbar__count" id="ac-count"></span>
    </div>

    <div class="grid" id="ac-grid">
      <div class="empty-state"><strong>불러오는 중...</strong></div>
    </div>
"""
write_page('accessories.html', '악세서리', '이터널시티 악세서리(반지·목걸이·귀걸이·팔찌·벨트) 전체 목록.',
           'accessories.html', accessories_body,
           '<script src="js/itemgrid.js"></script>\n<script src="js/accessories.js"></script>')

# ---------------------------------------------------------------------------
# 아이템 상세 (동적 페이지, ?cat=&id= 로 구동)
# ---------------------------------------------------------------------------
item_detail_body = """
    <div class="page-header">
      <div class="page-header__eyebrow" id="id-eyebrow">ITEM DETAIL</div>
      <h1 id="id-name">불러오는 중...</h1>
      <p id="id-meta"></p>
    </div>

    <div id="id-notfound" class="placeholder" style="display:none;">
      <div class="placeholder__mark">NOT FOUND</div>
      <h2>아이템을 찾을 수 없습니다</h2>
      <p>주소에 문제가 있거나 데이터가 아직 없는 아이템입니다. <a href="weapons.html" style="color:var(--olive);">무기 목록으로 돌아가기</a></p>
    </div>

    <div id="id-content" style="display:none;">
      <div class="cat-grid" style="grid-template-columns: 220px 1fr; margin-bottom: 28px;">
        <div class="cat-card" style="min-height:auto; padding:0; overflow:hidden;">
          <div style="aspect-ratio:1/1; width:100%; display:flex; align-items:center; justify-content:center; background:var(--panel-raised);">
            <img id="id-image" alt="" style="display:none; max-width:75%; max-height:75%; object-fit:contain; image-rendering:pixelated;">
            <div id="id-image-fallback" style="font-size:11px; color:var(--muted); text-align:center; padding:16px; font-family:var(--font-mono);">이미지를 불러오는 중...</div>
          </div>
        </div>
        <div class="cat-card" style="min-height:auto;">
          <div class="card__badges" id="id-badges" style="margin-bottom:10px;"></div>
          <dl class="card__stats" id="id-basestats" style="grid-template-columns: repeat(3, 1fr);"></dl>
          <div class="card__foot" id="id-link" style="margin-top:14px;"></div>
        </div>
      </div>

      <!-- 무기 강화 계산기 -->
      <div id="id-weapon-calc" style="display:none;">
        <div class="section-title"><h2>강화 · 튜닝 계산기</h2></div>
        <div class="cat-card" style="min-height:auto; margin-bottom:36px;">
          <div style="font-size:12px; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px;">몸체 튜닝</div>
          <div class="chip-group" id="id-body" style="flex-wrap:wrap; margin-bottom:16px;"></div>
          <div style="font-size:12px; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px;">강화 단계</div>
          <div class="chip-group" id="id-stage" style="flex-wrap:wrap;"></div>
          <div style="margin-top:16px; border-top:1px solid var(--line); padding-top:14px;">
            <div class="hero__stat" style="border:none; padding:0;">
              <div class="hero__stat-num" id="id-attack-result">–</div>
              <div class="hero__stat-label">계산된 파괴력</div>
            </div>
          </div>
          <div id="id-breakdown" style="margin-top:12px; font-family:var(--font-mono); font-size:12px; color:var(--muted); display:flex; flex-direction:column; gap:3px;"></div>
          <div class="card__foot" style="margin-top:10px;">총열/손잡이/조준경(치명·탄착률·명중률)은 영향 스탯은 확정됐지만 상한·반올림 규칙이 미확인이라 계산에서 제외했습니다. 오차 안내: 사이트 값과 ±2 정도 차이가 날 수 있습니다.</div>
        </div>

        <div class="section-title"><h2>데미지 레인지 계산</h2></div>
        <div class="cat-card" style="min-height:auto; margin-bottom:36px;">
          <p>위에서 계산한 파괴력을 캐릭터 스탯(체력/기술/템공합 등)이 반영된 <b style="color:var(--paper);">"인벤창 공격력"</b>으로
          바꾸는 정확한 공식은 아직 확인되지 않았습니다. 기본값은 위 계산 파괴력을 그대로 쓰지만,
          실제 게임 화면에 보이는 공격력 숫자를 알고 있다면 직접 입력해서 더 정확하게 계산할 수 있습니다.</p>
          <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:flex-end; margin:12px 0;">
            <label style="font-size:12.5px; color:var(--muted);">인벤창 공격력
              <input id="id-inv-attack" type="number" style="display:block; margin-top:4px; width:140px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-mono);">
            </label>
            <label style="font-size:12.5px; color:var(--muted);">크기 보정
              <input id="id-mult-size" type="number" step="0.01" value="1" style="display:block; margin-top:4px; width:80px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-mono);">
            </label>
            <label style="font-size:12.5px; color:var(--muted);">탄종 보정
              <input id="id-mult-ammo" type="number" step="0.01" value="1" style="display:block; margin-top:4px; width:80px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-mono);">
            </label>
            <label style="font-size:12.5px; color:var(--muted);">특수 보정</label>
            <input id="id-mult-special" type="number" step="0.01" value="1" style="display:block; margin-top:4px; width:80px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-mono);">
            <label style="font-size:12.5px; color:var(--muted);">스킬 보정
              <input id="id-mult-skill" type="number" step="0.01" value="1" style="display:block; margin-top:4px; width:80px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-mono);">
            </label>
          </div>
          <div style="overflow-x:auto;">
            <table style="width:100%; border-collapse:collapse; font-size:13px;">
              <thead>
                <tr style="background:var(--panel-raised); text-align:right; font-family:var(--font-mono); font-size:12px; color:var(--muted);">
                  <th style="text-align:left; padding:8px 10px;">구분</th>
                  <th style="padding:8px 10px;">최소</th>
                  <th style="padding:8px 10px;">최대</th>
                </tr>
              </thead>
              <tbody id="id-damage-table"></tbody>
            </table>
          </div>
          <div class="card__foot" style="margin-top:10px;">배율(0.88 / 발화·크리티컬 1.5·1.55배 / 헤드샷 3.10배)은 확정된 값이며, 실측 아이템으로
          오차 없이 검증했습니다. 크기·탄종·특수·스킬 보정값은 아이템마다 달라질 수 있어 기본값 1로 계산됩니다.</div>
        </div>
      </div>

      <!-- 방어구 플러스업 계산기 -->
      <div id="id-armor-calc" style="display:none;">
        <div class="section-title"><h2>플러스업 효과 계산기</h2></div>
        <div class="cat-card" style="min-height:auto; margin-bottom:36px;">
          <div style="font-size:12px; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px;">재질</div>
          <div class="chip-group" id="id-material" style="flex-wrap:wrap; margin-bottom:16px;">
            <button class="chip" data-value="장인">장인 (1.11)</button>
            <button class="chip" data-value="명인">명인 (1.66)</button>
            <button class="chip is-active" data-value="O.T">O.T (2.5)</button>
          </div>
          <div style="font-size:12px; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px;">부위</div>
          <div class="chip-group" id="id-piece" style="flex-wrap:wrap; margin-bottom:16px;">
            <button class="chip is-active" data-value="일반">일반 (×1)</button>
            <button class="chip" data-value="원피스">원피스 (×2)</button>
            <button class="chip" data-value="전신의상">전신의상 (×6)</button>
          </div>
          <div style="font-size:12px; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px;">플러스업 단계</div>
          <div class="chip-group" id="id-level" style="flex-wrap:wrap;"></div>
          <div style="margin-top:16px; border-top:1px solid var(--line); padding-top:14px;">
            <div class="hero__stat" style="border:none; padding:0;">
              <div class="hero__stat-num" id="id-armor-result">–</div>
              <div class="hero__stat-label">공격력 증가율</div>
            </div>
          </div>
          <div id="id-armor-breakdown" style="margin-top:12px; font-family:var(--font-mono); font-size:12px; color:var(--muted); display:flex; flex-direction:column; gap:3px;"></div>
        </div>
      </div>
    </div>
"""
write_page('item-detail.html', '아이템 상세', '이터널시티 아이템 상세정보 및 강화/튜닝 계산기.',
           'weapons.html', item_detail_body,
           '<script src="js/calcengine.js"></script>\n<script src="js/itemdetail.js"></script>')

# ---------------------------------------------------------------------------
# 마이 캐릭터 (로그인 + 캐릭터/장비 저장)
# ---------------------------------------------------------------------------
mypage_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">ACCOUNT / MY CHARACTER</div>
      <h1>마이 캐릭터</h1>
      <p>로그인하면 캐릭터 스탯과 장비 구성을 저장하고, 강화·플러스업 계산 결과를 한번에 확인할 수 있습니다.</p>
    </div>

    <div id="mp-setup-notice" class="setup-notice" style="display:none;">
      <strong style="color:var(--paper); display:block; margin-bottom:8px;">마이 캐릭터를 사용하려면 Firebase 설정이 필요합니다</strong>
      거래 게시판과 같은 Firebase 프로젝트를 사용합니다. README.md의 "마이 캐릭터(로그인) 설정하기"를
      먼저 완료해주세요 (Firebase Authentication의 이메일/비밀번호 로그인 활성화 필요).
    </div>

    <div id="mp-app" style="display:none;">

      <!-- 로그인 전 -->
      <div id="mp-auth-box" class="login-required">
        <p>캐릭터 정보를 저장하려면 로그인이 필요합니다.</p>
        <button class="btn" id="mp-open-login">로그인 / 회원가입</button>
      </div>

      <!-- 로그인 후 -->
      <div id="mp-character-box" style="display:none;">
        <div class="toolbar" style="border-bottom:none; padding-bottom:0;">
          <span style="font-size:14px; color:var(--paper);"><span id="mp-username" style="color:var(--olive);"></span>님</span>
          <button class="btn btn--ghost btn--sm" id="mp-logout" style="margin-left:auto;">로그아웃</button>
        </div>

        <div class="section-title" style="margin-top:24px;"><h2>기본 스탯</h2></div>
        <div class="cat-card" style="min-height:auto; margin-bottom:28px;">
          <div class="form-grid">
            <div class="form-field"><label>캐릭터명</label><input type="text" id="mp-name" maxlength="20"></div>
            <div class="form-field"><label>레벨</label><input type="number" id="mp-level" min="1" value="1"></div>
            <div class="form-field">
              <label>특성</label>
              <select id="mp-trait"><option value="휴먼">휴먼</option><option value="변이">변이</option><option value="공앰">공앰</option></select>
            </div>
            <div class="form-field"><label>체력</label><input type="number" id="mp-hp" value="0"></div>
            <div class="form-field"><label>기술</label><input type="number" id="mp-skill" value="0"></div>
            <div class="form-field"><label>템공합</label><input type="number" id="mp-itematk" value="0"></div>
            <div class="form-field"><label>템치합</label><input type="number" id="mp-itemcrit" value="0"></div>
            <div class="form-field"><label>업적공</label><input type="number" id="mp-achatk" value="0"></div>
            <div class="form-field"><label>해방공</label><input type="number" id="mp-releaseatk" value="0"></div>
          </div>
          <div class="card__foot">이 값들은 eterinfo.kr 시뮬레이터의 "기본능력" 입력값과 같은 항목입니다.
          다만 이 수치들이 무기 파괴력과 정확히 어떤 공식으로 합산되는지는 아직 확인되지 않아,
          아래 요약에서는 무기/방어구 계산과 별도로 참고용으로만 표시합니다.</div>
        </div>

        <div class="section-title"><h2>무기 장착</h2></div>
        <div class="cat-card" style="min-height:auto; margin-bottom:28px;">
          <select id="mp-weapon-select" style="width:100%; max-width:420px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:8px 10px; font-family:var(--font-kr); margin-bottom:14px;">
            <option value="">장착 안 함</option>
          </select>
          <div id="mp-weapon-options" style="display:none;">
            <div style="font-size:12px; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px;">몸체 튜닝</div>
            <div class="chip-group" id="mp-weapon-body" style="flex-wrap:wrap; margin-bottom:14px;"></div>
            <div style="font-size:12px; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px;">강화 단계</div>
            <div class="chip-group" id="mp-weapon-stage" style="flex-wrap:wrap;"></div>
          </div>
        </div>

        <div class="section-title"><h2>방어구 장착 (부위별)</h2></div>
        <div id="mp-armor-slots" class="cat-grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 28px;"></div>

        <div class="section-title"><h2>악세서리 장착</h2></div>
        <div id="mp-accessory-slots" class="cat-grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 28px;"></div>

        <div class="section-title"><h2>업적 (참고용 체크리스트)</h2></div>
        <div class="cat-card" style="min-height:auto; margin-bottom:28px;">
          <div id="mp-achievements" style="display:flex; flex-direction:column; gap:6px; font-size:13px; max-height:220px; overflow-y:auto;"></div>
          <div class="card__foot">현재 업적별 정확한 스탯 보너스 수치가 확인되지 않아, 체크한 업적은
          기록용으로만 저장되고 아래 합산 계산에는 반영되지 않습니다.</div>
        </div>

        <div class="section-title"><h2>합산 요약</h2></div>
        <div class="cat-grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 20px;">
          <div class="cat-card" style="min-height:auto;">
            <h3>무기 계산 파괴력</h3>
            <div class="hero__stat-num" id="mp-sum-weapon" style="margin-top:6px;">–</div>
          </div>
          <div class="cat-card" style="min-height:auto;">
            <h3>방어구 방어력 합계</h3>
            <div class="hero__stat-num" id="mp-sum-defense" style="margin-top:6px;">–</div>
          </div>
          <div class="cat-card" style="min-height:auto;">
            <h3>방어구 플러스업 공격력 증가율 합계</h3>
            <div class="hero__stat-num" id="mp-sum-armorpct" style="margin-top:6px;">–</div>
            <div class="card__foot">여러 부위 보너스가 게임 내에서 정확히 어떻게 합산되는지 미확인 —
            단순 합산 기준입니다.</div>
          </div>
          <div class="cat-card" style="min-height:auto;">
            <h3>악세서리 고정 옵션 합계</h3>
            <div id="mp-sum-accessory" style="margin-top:6px; font-size:13px; color:var(--paper-dim);">–</div>
          </div>
        </div>

        <button class="btn" id="mp-save">저장하기</button>
        <span id="mp-save-status" style="margin-left:10px; font-size:12.5px; color:var(--muted);"></span>
      </div>
    </div>
"""
write_page('mypage.html', '마이 캐릭터', '내 캐릭터 스탯과 장비를 저장하고 강화 계산 결과를 확인하세요.',
           'mypage.html',
           mypage_body,
                                                                             '<script src="js/slots.js"></script>\n'
           '<script src="js/calcengine.js"></script>\n'
           '<script src="js/mypage.js"></script>')

# ---------------------------------------------------------------------------
# 준비중 placeholder 페이지들
# ---------------------------------------------------------------------------
soon_pages = [
    ('characters.html', '캐릭터 · 용병', '캐릭터/용병 정보 (준비중)',
     '캐릭터 · 용병 정보는 준비 중입니다', '직업 특성, 스탯 분배 가이드, 용병 스킬트리를 정리할 예정입니다.'),
    ('regions.html', '지역 · 어썰트', '지역/어썰트 정보 (준비중)',
     '지역 · 어썰트 정보는 준비 중입니다', '사냥터, 보스 위치, 어썰트/캠페인 공략을 정리할 예정입니다.'),
]

for href, title, desc, headline, body_text in soon_pages:
    body = f"""
    <div class="page-header">
      <div class="page-header__eyebrow">COMING SOON</div>
      <h1>{title}</h1>
    </div>
    <div class="placeholder">
      <div class="placeholder__mark">DATA NOT YET LINKED</div>
      <h2>{headline}</h2>
      <p>{body_text}</p>
    </div>
    """
    write_page(href, title, desc, href, body)

# index.html은 손으로 관리하는 파일이라 write_page를 거치지 않으므로, 여기서 직접
# 캐시 버전을 입혀줌 (재실행해도 항상 최신 버전 번호로 갱신됨).
index_path = os.path.join(ROOT_DIR, 'index.html')
with open(index_path, encoding='utf-8') as f:
    index_html = f.read()
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(bust(index_html))
print('busted index.html cache version ->', CACHE_VERSION)

print('done')
