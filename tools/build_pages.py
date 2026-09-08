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
"""
write_page('weapons.html', '무기 정보', '이터널시티 무기 등급별·타입별 스펙과 강화 정보.',
           'weapons.html', weapons_body,
           '<script src="js/itemgrid.js"></script>\n<script src="js/weapons.js"></script>')

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
# 강화 시뮬레이터 (플러스업)
# ---------------------------------------------------------------------------
calculators_body = """
    <div class="page-header">
      <div class="page-header__eyebrow">TOOLS / ENHANCEMENT SIMULATOR</div>
      <h1>강화 시뮬레이터</h1>
      <p>아이템 종류별 플러스업 성공·실패·초기화 확률로 기대 비용을 계산하고, 실제 강화 과정을 직접 시뮬레이션해보세요.</p>
    </div>

    <div class="toolbar" style="border-bottom:none; padding-bottom:0; margin-bottom:18px;">
      <div class="chip-group" id="pu-category"></div>
    </div>

    <div id="pu-empty" class="placeholder" style="display:none;">
      <div class="placeholder__mark">DATA NOT YET LINKED</div>
      <h2 id="pu-empty-label"></h2>
      <p>이 종류의 강화 확률표는 아직 등록되지 않았습니다. eterinfo.kr 등에서 해당 종류의 확률표를 붙여넣어 주시면 반영해 드릴게요.</p>
    </div>

    <div id="pu-content">
      <div class="section-title">
        <h2>강화 확률표</h2>
        <span class="section-title__note" id="pu-cost-note"></span>
      </div>
      <div style="overflow-x:auto; margin-bottom:36px; border:1px solid var(--line);">
        <table style="width:100%; border-collapse:collapse; font-size:13px;">
          <thead>
            <tr style="background:var(--panel-raised); text-align:right; font-family:var(--font-mono); font-size:12px; color:var(--muted);">
              <th style="text-align:left; padding:9px 12px;">강화</th>
              <th style="padding:9px 12px;">성공</th>
              <th style="padding:9px 12px;">실패</th>
              <th style="padding:9px 12px;">초기화</th>
              <th style="padding:9px 12px;">누적 공격력 증가</th>
              <th style="padding:9px 12px;">누적 증가 (CL)</th>
            </tr>
          </thead>
          <tbody id="pu-table-body"></tbody>
        </table>
      </div>

      <div class="cat-grid" style="grid-template-columns: 1fr 1fr; margin-bottom: 36px;">
        <div class="cat-card" style="min-height:auto;">
          <h3>기대값 계산기</h3>
          <p>이론적으로 평균 몇 번 시도해야 목표 강화 단계에 도달하는지 계산합니다.</p>
          <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-top:6px;">
            <label style="font-size:12.5px; color:var(--muted);">현재 단계
              <select id="pu-from" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);"></select>
            </label>
            <label style="font-size:12.5px; color:var(--muted);">목표 단계
              <select id="pu-to" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);"></select>
            </label>
            <label style="font-size:12.5px; color:var(--muted);">재료 1회 비용
              <input id="pu-cost-input" type="number" style="display:block; margin-top:4px; width:110px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-mono);">
            </label>
          </div>
          <div style="margin-top:16px; border-top:1px solid var(--line); padding-top:14px;">
            <div class="hero__stat" style="border:none; padding:0;">
              <div class="hero__stat-num" id="pu-expected-attempts">–</div>
              <div class="hero__stat-label">평균 예상 시도 횟수</div>
            </div>
            <div class="hero__stat" style="border:none; padding:12px 0 0;">
              <div class="hero__stat-num" id="pu-expected-cost">–</div>
              <div class="hero__stat-label">평균 예상 비용</div>
            </div>
          </div>
        </div>

        <div class="cat-card" style="min-height:auto;">
          <h3>실전 시뮬레이터</h3>
          <p>버튼을 눌러 실제로 강화를 시도해보세요. 확률에 따라 성공·실패·초기화가 무작위로 결정됩니다.</p>
          <div style="display:flex; align-items:baseline; gap:10px; margin-top:10px;">
            <div class="hero__stat-num" id="pu-sim-level" style="font-size:40px;">+0</div>
            <div class="card__meta">현재 강화 단계</div>
          </div>
          <dl class="card__stats" style="grid-template-columns: repeat(3, 1fr); margin-top:6px;">
            <div class="stat-row" style="flex-direction:column; align-items:flex-start; gap:2px;"><dt>총 시도</dt><dd id="pu-sim-attempts">0</dd></div>
            <div class="stat-row" style="flex-direction:column; align-items:flex-start; gap:2px;"><dt>총 비용</dt><dd id="pu-sim-cost">0</dd></div>
            <div class="stat-row" style="flex-direction:column; align-items:flex-start; gap:2px;"><dt>초기화 횟수</dt><dd id="pu-sim-resets">0</dd></div>
          </dl>
          <div style="display:flex; gap:8px; margin-top:14px; flex-wrap:wrap;">
            <button class="chip" id="pu-sim-attempt" style="background:var(--olive-dim); border-color:var(--olive); color:var(--paper); font-size:13px; padding:9px 16px;">강화 시도</button>
            <button class="chip" id="pu-sim-auto" style="font-size:13px; padding:9px 16px;">목표까지 자동 시도</button>
            <button class="chip" id="pu-sim-reset" style="font-size:13px; padding:9px 16px;">초기화</button>
          </div>
          <div id="pu-sim-log" style="margin-top:14px; max-height:180px; overflow-y:auto; font-family:var(--font-mono); font-size:11.5px; color:var(--muted); border-top:1px solid var(--line); padding-top:10px; display:flex; flex-direction:column-reverse; gap:3px;"></div>
        </div>
      </div>
    </div>

    <div class="section-title" style="margin-top:44px;">
      <h2>아이템 등급 착용 제한</h2>
      <span class="section-title__note">출처: 나무위키</span>
    </div>
    <div class="cat-grid" style="grid-template-columns: 1fr 1fr; margin-bottom: 36px;">
      <div class="cat-card" style="min-height:auto;">
        <h3>착용 레벨 계산기</h3>
        <p>9등급 이하 아이템은 <code style="color:var(--amber);">(등급-2)×10</code> 레벨부터 페널티 없이 착용할 수 있고,
        그보다 낮은 레벨로 착용하면 부족한 레벨 1당 성능이 10%씩 깎입니다. 10등급은 90레벨,
        11등급은 101레벨 + 특정 퀘스트가 반드시 필요합니다(부분 착용 불가).</p>
        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-top:10px;">
          <label style="font-size:12.5px; color:var(--muted);">아이템 등급
            <select id="lv-grade" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);">
              <option value="1">1등급</option><option value="2">2등급</option><option value="3">3등급</option>
              <option value="4">4등급</option><option value="5">5등급</option><option value="6">6등급</option>
              <option value="7">7등급</option><option value="8">8등급</option><option value="9">9등급</option>
              <option value="10">10등급</option><option value="11">11등급</option>
            </select>
          </label>
          <label style="font-size:12.5px; color:var(--muted);">내 캐릭터 레벨
            <input id="lv-char" type="number" min="1" value="60" style="display:block; margin-top:4px; width:100px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-mono);">
          </label>
        </div>
        <div style="margin-top:16px; border-top:1px solid var(--line); padding-top:14px;">
          <div class="hero__stat" style="border:none; padding:0;">
            <div class="hero__stat-num" id="lv-required">–</div>
            <div class="hero__stat-label">권장 착용 레벨</div>
          </div>
          <div class="hero__stat" style="border:none; padding:12px 0 0;">
            <div class="hero__stat-num" id="lv-penalty">–</div>
            <div class="hero__stat-label">현재 레벨 기준 성능 적용률</div>
          </div>
        </div>
      </div>

      <div class="cat-card" style="min-height:auto;">
        <h3>명인 업그레이드 승급 확률</h3>
        <p>일반/CL 무기를 <b style="color:var(--paper);">명인 등급</b>으로 승급시키는 별도 확률 시스템입니다.
        위의 플러스업(+1~+15)과는 다른 콘텐츠이며, 현재 알려진 값은 다음과 같습니다.</p>
        <dl class="card__stats" style="grid-template-columns: 1fr; margin-top:10px;">
          <div class="stat-row"><dt>8등급 이상 기본 성공률</dt><dd>0.5%</dd></div>
          <div class="stat-row"><dt>특수가공 부품 사용 시</dt><dd>0.75% (1.5배)</dd></div>
        </dl>
        <div class="card__foot" style="margin-top:12px;">7등급 이하 성공률 및 실패 시 페널티(재료 소모/등급 유지 여부)는
        아직 확인되지 않았습니다. 정보를 알고 계시면 알려주세요 — 바로 반영해 드릴게요.</div>
      </div>
    </div>

    <div class="section-title" style="margin-top:44px;">
      <h2>무기 강화 · 튜닝 계산기</h2>
      <span class="section-title__note">몸체 튜닝 × 강화단계 누적배율 (확정 공식)</span>
    </div>
    <div class="cat-card" style="min-height:auto; margin-bottom:36px;">
      <p>우리 DB에 등록된 무기를 골라 몸체 튜닝과 강화 단계를 선택하면, 확정된 배율 공식으로
      최종 파괴력을 계산합니다. 총열/손잡이/조준경(치명·탄착률·명중률)은 영향을 주는 스탯은
      확인됐지만 정확한 상한·반올림 규칙이 아직 미확인이라 이번 계산기에는 포함하지 않았습니다.</p>
      <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:flex-end; margin-top:12px;">
        <label style="font-size:12.5px; color:var(--muted); flex:1 1 260px;">무기 선택
          <select id="wc-weapon" style="display:block; width:100%; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);"></select>
        </label>
        <label style="font-size:12.5px; color:var(--muted);">몸체 튜닝
          <select id="wc-body" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);"></select>
        </label>
        <label style="font-size:12.5px; color:var(--muted);">강화 단계
          <select id="wc-stage" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);"></select>
        </label>
      </div>
      <div style="margin-top:16px; border-top:1px solid var(--line); padding-top:14px;">
        <div class="hero__stat" style="border:none; padding:0;">
          <div class="hero__stat-num" id="wc-result">–</div>
          <div class="hero__stat-label">계산된 파괴력 (기초 <span id="wc-base">–</span>)</div>
        </div>
      </div>
      <div id="wc-breakdown" style="margin-top:12px; font-family:var(--font-mono); font-size:12px; color:var(--muted); display:flex; flex-direction:column; gap:3px;"></div>
      <div class="card__foot" style="margin-top:10px;">오차 안내: 사이트와 완전히 동일한 정수 반올림 규칙은 미확정이라, 실제 값과 ±2 정도 차이가 날 수 있습니다.</div>
    </div>

    <div class="section-title">
      <h2>방어구 플러스업 효과 계산기</h2>
      <span class="section-title__note">등급 × 재질 × CL × 부위 × 플러스업 단계 (확정 공식)</span>
    </div>
    <div class="cat-card" style="min-height:auto;">
      <p>강화(플러스업) <b style="color:var(--paper);">확률</b>은 위쪽 시뮬레이터에서, 플러스업을 완료했을 때
      실제로 얻는 <b style="color:var(--paper);">공격력 증가율(%)</b>은 이 계산기에서 확인하세요. 별개의 두 시스템입니다.</p>
      <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:flex-end; margin-top:12px;">
        <label style="font-size:12.5px; color:var(--muted);">아이템 등급
          <select id="ac-grade-calc" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);">
            <option value="1">1등급</option><option value="2">2등급</option><option value="3">3등급</option>
            <option value="4">4등급</option><option value="5">5등급</option><option value="6" selected>6등급</option>
            <option value="7">7등급</option><option value="8">8등급</option><option value="9">9등급</option>
            <option value="10">10등급</option><option value="11">11등급</option>
          </select>
        </label>
        <label style="font-size:12.5px; color:var(--muted);">재질
          <select id="ac-material" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);">
            <option value="장인">장인 (1.11)</option>
            <option value="명인">명인 (1.66)</option>
            <option value="O.T" selected>O.T (2.5)</option>
          </select>
        </label>
        <label style="font-size:12.5px; color:var(--muted);">CL 여부
          <select id="ac-cl" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);">
            <option value="0" selected>일반 (×1.0)</option>
            <option value="1">CL (×1.1)</option>
          </select>
        </label>
        <label style="font-size:12.5px; color:var(--muted);">부위
          <select id="ac-piece" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);">
            <option value="일반" selected>일반 (×1)</option>
            <option value="원피스">원피스 (×2)</option>
            <option value="전신의상">전신의상 (×6)</option>
          </select>
        </label>
        <label style="font-size:12.5px; color:var(--muted);">플러스업 단계
          <select id="ac-level" style="display:block; margin-top:4px; background:var(--panel); border:1px solid var(--line-bright); color:var(--paper); padding:7px 9px; font-family:var(--font-kr);"></select>
        </label>
      </div>
      <div style="margin-top:16px; border-top:1px solid var(--line); padding-top:14px;">
        <div class="hero__stat" style="border:none; padding:0;">
          <div class="hero__stat-num" id="ac-result">–</div>
          <div class="hero__stat-label">공격력 증가율</div>
        </div>
      </div>
      <div id="ac-breakdown" style="margin-top:12px; font-family:var(--font-mono); font-size:12px; color:var(--muted); display:flex; flex-direction:column; gap:3px;"></div>
    </div>

    <div class="section-title" style="margin-top:44px;">
      <h2>접두사 · 유니크 개조 (정성적 정보)</h2>
      <span class="section-title__note">정확한 수치 미확인 — 효과 방향만 표시</span>
    </div>
    <div class="cat-grid" style="grid-template-columns: 1fr 1fr; margin-bottom: 20px;">
      <div class="cat-card" style="min-height:auto;">
        <h3>방어구 접두사</h3>
        <div id="prefix-list" style="font-size:12.5px; color:var(--paper-dim); display:flex; flex-direction:column; gap:6px; margin-top:8px;"></div>
      </div>
      <div class="cat-card" style="min-height:auto;">
        <h3>무기 유니크 개조</h3>
        <div id="unique-list" style="font-size:12.5px; color:var(--paper-dim); display:flex; flex-direction:column; gap:6px; margin-top:8px;"></div>
      </div>
    </div>
"""
write_page('calculators.html', '강화 시뮬레이터', '이터널시티 아이템 종류별 플러스업 강화 확률/기대비용/시뮬레이터.',
           'calculators.html', calculators_body,
           '<script src="js/plusup.js"></script>\n<script src="js/itemlevel.js"></script>\n<script src="js/calcengine.js"></script>\n<script src="js/weaponcalc.js"></script>\n<script src="js/armorpluscalc.js"></script>\n<script src="js/refdata.js"></script>')

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
"""
write_page('armors.html', '방어구', '이터널시티 방어구·의류·방패 부위별 전체 목록.',
           'armors.html', armors_body,
           '<script src="js/itemgrid.js"></script>\n<script src="js/armors.js"></script>')

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
            <img id="id-image" src="" alt="" referrerpolicy="no-referrer" style="max-width:75%; max-height:75%; object-fit:contain; image-rendering:pixelated;" onerror="this.style.display='none'; document.getElementById('id-image-fallback').style.display='';">
            <div id="id-image-fallback" style="display:none; font-size:11px; color:var(--muted); text-align:center; padding:16px; font-family:var(--font-mono);">이미지를 불러올 수 없습니다</div>
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
