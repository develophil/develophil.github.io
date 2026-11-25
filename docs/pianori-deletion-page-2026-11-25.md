# 피아노리 공개 삭제 화면 준비 — 2026-11-25

Supabase 기본 도메인의 HTML 응답 제한으로 기존 공개 삭제 주소가 브라우저에서
소스로 표시됐다. 피아노리 리포의 `web/account-deletion/` 정본 세 파일을
`account-deletion/pianori/`로 복사해 공개 적용 후보를 만들었다.

- 신규 주소 후보: `https://develophil.github.io/account-deletion/pianori/`
- 기존 앱/스토어 주소는 Supabase 함수의 고정 302 연결로 유지한다.
- 화면: 한/영 삭제·보유 범위, Google/Kakao 본인 인증, 확인 체크, 삭제 및 영수증.
- 공개 publishable key만 포함한다. access token은 메모리, verifier는 sessionStorage,
  삭제 요청 ID와 subject만 localStorage에 보관한다. refresh token은 저장하지 않는다.
- source SHA-256은 피아노리 `docs/verification/2026-11-25/deletion-pages-files.json`과 일치한다.
- 피아노리 관련 테스트 44건, Node 런타임, 회귀 검출, 정적 분석, 로컬 Chrome 표시와
  미인증 삭제 차단을 주실행자가 확인했다. 360px/공개 OAuth/삭제는 아직 미검증이다.
- Pages는 임의 HTTP 헤더를 지원하지 않아 CSP meta와 iframe 실행 차단을 사용한다.
  최종 삭제 권한 검사는 Supabase의 소유자·최근 세션 검증이 담당한다.
- 기존 Pages checkout의 뒤처진 브랜치·다른 개인정보처리방침 수정과 섞지 않기 위해
  origin/master `85a4a5d`에서 별도 `codex/pianori-deletion-web` worktree를 만들었다.
- 이 커밋은 로컬 준비다. 사용자 공개 승인 후 Pages→Auth callback 추가→Kakao CORS/반환→
  기존 URL 연결을 적용하고 공개 브라우저에서 검증한다. 아직 푸시/배포하지 않았다.

정본 운영 문서: 피아노리 `docs/public-deletion-web-fix-2026-11-25.md`.
