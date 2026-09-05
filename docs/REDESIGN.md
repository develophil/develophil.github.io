# develophil.github.io 개편 설계 — 개인 개발자 브랜드 홈페이지

- 작성일: 2026-09-05
- 상태: **확정 (2026-09-05, 사용자 결정 반영)** — 구현 진행. push는 별도 승인
- 원칙: Minimal Footprint(빌드 도구 없음, 순수 HTML/CSS), 기존 Actions 파이프라인 무중단

---

## 1. 왜 만드나 — 이 사이트에 오는 사람 5부류

| 방문자 | 오는 이유 | 사이트가 해야 할 일 |
|---|---|---|
| **① 스토어·광고 심사자** (Google Play, AdMob/AdSense) | 개발자 실체 확인, 방침·연락처·app-ads.txt | 첫 화면에서 "누가, 무엇을 만들고, 어떻게 연락하나"가 즉시 보일 것 |
| **② 앱 사용자** | 지원 문의, 개인정보처리방침 | 앱별 방침 페이지 + 연락 이메일 |
| **③ B2B 잠재 고객·파트너** | AI 기업교육(도화엔지니어링 류), 마케팅 자동화 | 개인 취미 사이트가 아닌 **신뢰할 수 있는 1인 스튜디오**로 보일 것 |
| **④ 개발자·채용 담당** | GitHub 프로필에서 유입 | 기술 스택·실제 출시물 |
| **⑤ 2027 예비창업패키지 심사위원** | 사업계획서의 포트폴리오 링크 | "7개 제품을 혼자 기획·출시·운영" 증빙이 한 페이지에 |

→ 공통분모: **"실제로 출시된 제품이 있는 신뢰할 수 있는 1인 개발 스튜디오"**. 블로그 대시보드가 첫 화면인 지금은 이 다섯 부류 모두에게 실패한다.

## 2. 브랜드 정의

- **이름**: develophil (develop + Phil, 홍광필). 스토어 퍼블리셔명·GitHub·Ko-fi·패키지명(`com.develophil.*`)과 동일
- **정체**: 기획·디자인·개발·운영을 혼자 하는 인디 개발 스튜디오. AI 에이전트 주도 개발이 작업 방식의 특징
- **태그라인 후보** (§9-①에서 선택)
  - "혼자 만들고, 끝까지 운영합니다."
  - "작은 문제를 실제로 쓰이는 제품으로."
  - "Indie apps & web, built end-to-end."
- **톤**: 담담하고 구체적. 과장·마케팅 문구 배제. 숫자와 링크로 말함

## 3. 정보 구조 (사이트맵)

```
/                         랜딩 (단일 페이지, 아래 섹션 순서)
├─ Hero                   이름 · 태그라인 · 한 줄 소개 · [GitHub] [이메일]
├─ Products               제품 카드 (라이브 → 출시 준비 → 개발 중 순)
├─ Services  (§9-④)       AI 기업교육 · 업무 자동화 — B2B 문의 유도
├─ About                  누구인가 (§9-③ 노출 수준) · 작업 방식 · 스택
└─ Contact                develophil.apps@gmail.com · GitHub · Ko-fi · 블로그

/privacy/pianori/         pianori 개인정보처리방침 (기존 pianori-privacy 리포에서 통합)
/privacy/<app>/           이후 앱 추가 시 동일 패턴
/blog/                    기존 티스토리 RSS 대시보드 이동 (nav에는 "블로그"로 티스토리 직링크, 대시보드는 푸터 소링크)
/app-ads.txt              AdMob 퍼블리셔 ID 수령 후 생성 (빈 파일 금지)
/sitemap.xml, /robots.txt, /favicon.svg, /og.png
```

- v1은 **단일 페이지**. 제품별 상세 페이지는 제품 자체 사이트가 있으므로 만들지 않음
- 영어 대응은 §9-② 결정에 따라 `/en/` 미러 또는 단일 언어

## 4. 콘텐츠 인벤토리 (실데이터 기준)

### Products

| 제품 | 한 줄 | 상태 | 링크 | 비고 |
|---|---|---|---|---|
| **Rankorea** | 한국을 데이터로만 랭킹하는 지수 발행 플랫폼 | 🟢 라이브 | rankorea.com | 영문 서비스 |
| **보드게임메이트** | 보드게임 점수 계산 + 118종 규칙·영상 카탈로그 | 🟢 라이브 | boardgame-master.pages.dev | ⚠️ 라이브 `<title>`은 아직 "보드게임 마스터" — 배포 동기화 확인 필요. 도메인 구매 후 URL 교체 |
| **모임스팟** (meetup-spot) | 참석자 위치 기준 중간지점 모임 장소 추천 | 🟡 확인 필요 | meetup-spot.vercel.app | 라이브 여부 구현 단계에서 curl 확인 후 노출 결정 |
| **피아노리** (pianori) | 실시간 음정 감지 어린이 피아노 학습 앱 | 🟠 출시 준비 | (Play 링크 출시 후) | "Coming soon" 배지, 방침 링크 |
| **세계정복 퀴즈** (nara_quiz) | 2~4인 패스앤플레이 나라 맞히기 | ⚪ 개발 중 | — | 노출 여부 §9 후속 |
| **라운딩메이트** / **티끌갓생** | 골프 모임 플래너 / 커플 습관 앱 | ⚪ 개발 중 | — | v1 비노출 권고 (미완 제품 나열은 신뢰 감소) |
| **kakao-supabase-auth** | Kakao↔Supabase 인증 라이브러리 | 🔧 OSS | GitHub (private 상태 확인 필요) | 공개 전환 시 노출 |

### About (사실만)
- GitHub 2015~ · 성남 · 현직: StayManagement Inc. CTO (GitHub bio 공개 중 — 노출 여부 §9-③)
- 스택: Flutter/Riverpod/Supabase · Next.js/React/Tailwind · Cloudflare/Vercel · AI 에이전트 주도 개발
- 블로그: androphil.tistory.com (AI 트렌드) · Ko-fi: ko-fi.com/develophil

## 5. 비주얼 방향 3안 (§9-① 선택)

| | A. 타이포 미니멀 | B. 프로덕트 스튜디오 ⭐ | C. 포트폴리오 매거진 |
|---|---|---|---|
| 인상 | 개발자 개인 사이트. 텍스트 중심, 모노톤 + 포인트 1색 | 작은 소프트웨어 회사. 제품 카드·아이콘·상태 배지 | 에디토리얼. 큰 이미지, 프로젝트 스토리 |
| 강점 | 가장 빠르고 유지 쉬움 | ①③⑤ 방문자에게 신뢰. 제품이 주인공 | 개성 |
| 약점 | B2B·심사자에게 "취미"로 읽힐 수 있음 | 제품 아이콘·스크린샷 준비 필요 | 콘텐츠 유지 부담, 1인에겐 과함 |
| 참고 느낌 | 개인 개발자 블로그 | 인디 스튜디오 랜딩 (Sindre Sorhus, Panic 축소판) | 디자인 에이전시 |

**권고 B** — 방문자 5부류 중 4부류가 "제품과 신뢰"를 보러 오기 때문. 다크/라이트 자동 대응, 시스템 폰트 + Noto Sans KR.

## 6. 기술 결정

- **순수 HTML + CSS + 최소 JS** (다크모드·언어 토글 정도). 프레임워크·빌드 없음 → Actions와 충돌 0, 유지비 0
- 반응형: 모바일 우선, 카드 그리드 1→2→3열
- 접근성: 시맨틱 마크업, 대비 AA, 키보드 포커스
- SEO: `<title>`·description·OG 태그·`og.png`(1200×630)·JSON-LD `Person`+`Organization`·`sitemap.xml`·`robots.txt`
- 성능: 외부 요청은 폰트(Noto Sans KR) 1건만. 이미지는 SVG/WebP
- 기존 대시보드(`/blog/`)는 코드 그대로 이동, `fetch('data.json')` → `fetch('../data.json')` 1줄만 수정

## 7. 마이그레이션 계획

| 단계 | 작업 | 검증 |
|---|---|---|
| 1 | `study/` 전체 삭제 (사용자 결정: 하위 포함 불필요) | 트리 확인 |
| 2 | `index.html` → `blog/index.html`, fetch 경로 수정 | 로컬 서버에서 대시보드 렌더 확인 |
| 3 | 새 `index.html` + `assets/style.css` + `favicon.svg` + `og.png` | 모바일/데스크톱 스크린샷, 다크/라이트 |
| 4 | `privacy/pianori/index.html` — pianori 리포의 최신 `privacy_policy.html`(연락처 교체본) 복사 | 200 확인 |
| 5 | `pianori-privacy` 리포 index → 새 URL로 meta refresh 리다이렉트 (구 URL 보호) | 리다이렉트 동작 |
| 6 | `sitemap.xml`·`robots.txt`·README 갱신 | — |
| 7 | 로컬 최종 점검 → **사용자 승인 → push** | GitHub Pages 배포 후 전 URL 200, Actions 다음 실행 green |
| 8 | (후속) AdMob pub ID 수령 시 `app-ads.txt` 추가 / Play Console·pianori `store-listing.md`에 웹사이트·방침 URL 반영 | — |

## 8. 수용 기준

- [ ] `/`, `/blog/`, `/privacy/pianori/` 모두 200, 모바일(375px)·데스크톱(1280px) 레이아웃 정상
- [ ] 다크/라이트 모두 대비 AA
- [ ] 제품 카드의 모든 외부 링크 실제 200 (라이브 미확인 제품은 비노출)
- [ ] 콘솔 에러 0, 외부 요청 폰트 1건
- [ ] Actions `update-blog-data.yml` 변경 없이 다음 주기 정상 커밋
- [ ] 첫 화면 3초 안에 "누구 / 무엇 / 연락처"가 읽힘 (심사자 시나리오)

## 9. 결정 사항 (2026-09-05 확정)

| # | 질문 | **결정** |
|---|---|---|
| ① | 비주얼 방향 | **B. 프로덕트 스튜디오**. 태그라인 "혼자 만들고, 끝까지 운영합니다." / EN "Indie apps & web, built and run end-to-end." |
| ② | 언어 | **한국어 기본 + `/en/` 미러** |
| ③ | 신원 노출 | **핸들만(develophil)** — 실명·사진·현직 표기 없음. JSON-LD는 `Organization`만 |
| ④ | Services | **포함, 절제된 표현** — "함께 할 수 있는 일" 3항목 + 이메일 CTA. 가격·영업 문구 없음 |
| ⑤ | 개발 중 제품 | **라이브·출시준비만 노출** — Rankorea, 보드게임메이트, 모임스팟(라이브 확인 200), 피아노리(Coming soon). nara_quiz·roundingmate·tgodlife·kakao-supabase-auth 비노출 |

### 구현 중 발견·조치
- **`.gitignore`가 `*.html`/`*.css`/`*.js`를 무시**(gitignore.io web 템플릿 잔재) → 최소 `.gitignore`로 교체. 기존 `index.html`은 과거 강제 추가로 추적 중이었음
- pianori 방침에 실명 표기 없음 → 핸들만 원칙과 충돌 없음
- `pianori-privacy` 리포가 `/pianori-privacy/`로 이미 방침을 서빙 중 → 본 사이트 `/privacy/pianori/`로 통합, 구 리포는 리다이렉트로 유지(후속, 별도 리포 push)
- OG 이미지는 PIL로 1200×630 생성(외부 도구 없음)

## 10. 구현 기록 (2026-09-05)

- 완료: `study/` 삭제(53파일) · `.gitignore` 최소화 · `index.html`→`blog/index.html`(fetch `../data.json`) · 새 `index.html`·`en/index.html`·`assets/style.css`·`assets/favicon.svg`·`assets/og.png`(PIL 1200×630) · `privacy/pianori/index.html` · `sitemap.xml`·`robots.txt`·`README.md`
- 로컬 검증: 전 경로 200, 데스크톱 1280 / 모바일 390(iframe) 렌더 정상, 대시보드 데이터 로드 확인, 나브 모바일 축약 동작
- 미검증: 다크모드 스크린샷(CSS는 `prefers-color-scheme`로 구현), Lighthouse 수치 → 배포 후 실측
- 후속: ① push 승인 → GitHub Pages 배포 확인 ② `pianori-privacy` 리포 index를 `/privacy/pianori/`로 meta refresh ③ AdMob pub ID 수령 후 `app-ads.txt` ④ Play Console·pianori `store-listing.md`에 웹사이트 `https://develophil.github.io/`·방침 `https://develophil.github.io/privacy/pianori/` 반영 ⑤ 보드게임메이트 도메인 구매 시 카드 URL 교체
