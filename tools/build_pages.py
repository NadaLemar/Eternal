import re, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # .../eterpedia/tools
ROOT_DIR = os.path.dirname(BASE_DIR)                      # .../eterpedia

with open(os.path.join(BASE_DIR, '_shell.html'), encoding='utf-8') as f:
    SHELL = f.read()

def shell_for(active_href):
    """rail 링크 중 active_href와 일치하는 항목에 is-active 클래스를 부여."""
    s = SHELL.replace('rail__link is-active', 'rail__link')  # 홈의 기본 active 제거
    # href="X" 를 가진 링크에 is-active 부여 (is-soon 항목 제외)
    pattern = re.compile(r'(<a class="rail__link)( is-soon)?(")( href="' + re.escape(active_href) + r'")')
    s = pattern.sub(lambda m: f'{m.group(1)} is-active{m.group(2) or ""}{m.group(3)}{m.group(4)}', s)
    return s

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
{scripts}
</body>
</html>
"""

def write_page(filename, title, desc, active_href, body, scripts=""):
    html = PAGE_HEAD.format(
        title=title, desc=desc, shell=shell_for(active_href), body=body, scripts=scripts
    )
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
      <span class="toolbar__count" id="w-count"></span>
    </div>

    <div class="grid" id="w-grid">
      <div class="empty-state"><strong>불러오는 중...</strong></div>
    </div>
"""
write_page('weapons.html', '무기 정보', '이터널시티 무기 등급별·타입별 스펙과 강화 정보.',
           'weapons.html', weapons_body,
           '<script src="js/common.js"></script>\n<script src="js/itemgrid.js"></script>\n<script src="js/weapons.js"></script>')

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
           '<script src="js/common.js"></script>\n<script src="js/costumes.js"></script>\n'
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
           'ring-materials.html', ring_materials_body, '<script src="js/common.js"></script>\n<script src="js/ring-materials.js"></script>')

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

      <button class="btn" id="tr-form-toggle" style="margin-bottom:16px;">+ 새 글 작성</button>

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
              <input type="text" name="itemName" maxlength="60" required>
            </div>
            <div class="form-field">
              <label>가격 (El)</label>
              <input type="number" name="price" min="0" required>
            </div>
            <div class="form-field">
              <label>닉네임</label>
              <input type="text" name="nickname" maxlength="20" required>
            </div>
            <div class="form-field">
              <label>연락 방법 (게임 닉네임/디스코드 등)</label>
              <input type="text" name="contact" maxlength="80" required>
            </div>
            <div class="form-field">
              <label>삭제/수정 비밀번호</label>
              <input type="password" name="editKey" maxlength="20" required>
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
           '<script src="js/common.js"></script>\n'
           '<script src="js/firebase-config.js"></script>\n'
           '<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-app-compat.js"></script>\n'
           '<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-firestore-compat.js"></script>\n'
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
           '<script src="js/common.js"></script>\n'
           '<script src="js/firebase-config.js"></script>\n'
           '<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-app-compat.js"></script>\n'
           '<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-firestore-compat.js"></script>\n'
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
           'quests.html', quests_body, '<script src="js/common.js"></script>\n<script src="js/quests.js"></script>')

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
           'achievements.html', achievements_body, '<script src="js/common.js"></script>\n<script src="js/achievements.js"></script>')

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
"""
write_page('calculators.html', '강화 시뮬레이터', '이터널시티 아이템 종류별 플러스업 강화 확률/기대비용/시뮬레이터.',
           'calculators.html', calculators_body, '<script src="js/common.js"></script>\n<script src="js/plusup.js"></script>')

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
           '<script src="js/common.js"></script>\n<script src="js/itemgrid.js"></script>\n<script src="js/armors.js"></script>')

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
           '<script src="js/common.js"></script>\n<script src="js/itemgrid.js"></script>\n<script src="js/accessories.js"></script>')

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

print('done')
