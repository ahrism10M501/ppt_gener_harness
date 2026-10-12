# slides.md 한국어 윤문

한국어 발표는 요청이 없어도 Stage 4 승인 요청 전에 `humanize-korean`(im-not-ai, `skills/im-not-ai/`)으로 윤문하고, RVLAB 구조·사실 보존을 `rvppt polish-check`로 확인한다. 영어 발표(`review.language: en`)는 건너뛴다. 사용자가 원하지 않으면 생략한다.

## 절차

1. 윤문 전 원본을 보존한다.

   ```bash
   mkdir -p tasks/<task>/.build/editorial
   cp tasks/<task>/slides.md tasks/<task>/.build/editorial/before.md
   ```

2. `humanize-korean`을 실행하되 작업 폴더(cwd)를 `tasks/<task>/.build/editorial/`로 둔다. 그 스킬의 `_workspace/`는 그 안에 생기고 Git에서 제외된다. 입력은 frontmatter를 뺀 `slides.md` 본문이고 장르는 `report`다. 다음은 바꾸지 말라고 함께 전달한다.
   - `#` 섹션·`##` 토픽 줄(목차·상단 바 이름)
   - `:::`/`::::` 블록 표시, 표의 `|` 구조, 목록 기호와 들여쓰기
   - `$…$`·`$$…$$` 수식, 코드 블록, `![…](경로 "요청")`의 경로, 링크 URL, `[@key]` 인용
   - 모든 숫자·단위·고유명사·영문 전문용어

   `###` 핵심 문장은 다듬어도 된다. 다만 주장의 범위와 숫자는 바꾸지 않는다.
3. 결과(`_workspace/<run>/final.md`)에서 `<!-- HUMANIZE-SUMMARY -->` 블록을 지우고 `slides.md`의 frontmatter 뒤 본문만 교체한다.
4. 보존 검사를 실행한다.

   ```bash
   uv run rvppt polish-check tasks/<task> --before tasks/<task>/.build/editorial/before.md
   ```

   `errors`가 있으면 종료 코드 2다. 숫자·구조·수식·경로·섹션/토픽 이름 변화는 받아들이지 않고, 해당 부분만 `before.md`의 원문으로 되돌린 뒤 다시 검사한다. `warnings`의 영문 용어 변화는 하나씩 보고 의미가 같은지 판단한다.
5. `git diff --no-index tasks/<task>/.build/editorial/before.md tasks/<task>/slides.md`로 바뀐 문장을 Stage 4 보고에 요약한다. `similarity`가 대략 0.7 미만이면 과윤문을 의심하고 이유를 설명한다.

윤문은 내용 승인을 대신하지 않는다.
