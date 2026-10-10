# slides.md 한국어 윤문

한국어 발표의 Stage 4 초안에 `humanize-korean`(im-not-ai, `skills/im-not-ai/`)을 적용하고 RVLAB 구조·사실 보존을 `rvppt polish-check`로 확인한다. 영어 발표(`review.language: en`)는 건너뛴다. 사용자가 윤문을 원하지 않으면 생략한다.

## 절차

1. 윤문 전 원본을 보존한다.

   ```bash
   mkdir -p tasks/<task>/.build/editorial
   cp tasks/<task>/slides.md tasks/<task>/.build/editorial/before.md
   ```

2. `humanize-korean`을 실행하되 작업 폴더(cwd)를 `tasks/<task>/.build/editorial/`로 둔다. 그 스킬의 `_workspace/`는 그 안에 생기고 Git에서 제외된다. 입력은 frontmatter를 뺀 `slides.md` 본문이며 장르는 `report`다. 다음은 바꾸지 말라고 함께 전달한다.
   - `#`·`##`·`###` 제목 줄 전체(섹션·토픽·핵심 문장은 승인된 목차다)
   - `:::`/`::::` 블록 표시, 표의 `|` 구조, 목록 기호와 들여쓰기
   - `$…$`·`$$…$$` 수식, 코드 블록, `![…](경로 "요청")`의 경로, 링크 URL, `[@key]` 인용
   - 모든 숫자·단위·고유명사·영문 전문용어
3. 결과(`_workspace/<run>/final.md`)에서 `<!-- HUMANIZE-SUMMARY -->` 블록을 지우고 `slides.md`의 frontmatter 뒤 본문만 교체한다.
4. 보존 검사를 실행한다.

   ```bash
   uv run rvppt polish-check tasks/<task> --before tasks/<task>/.build/editorial/before.md
   ```

   `errors`가 있으면 종료 코드 2다. 숫자·구조·수식·경로·제목 변화는 받아들이지 않는다. 해당 부분만 `before.md`의 원문으로 되돌리고 다시 검사한다. `warnings`의 영문 용어 변화는 하나씩 보고 의미가 같은지 판단한다.
5. `git diff --no-index tasks/<task>/.build/editorial/before.md tasks/<task>/slides.md`로 바뀐 문장을 사용자에게 보여 준다. `similarity`가 낮으면(대략 0.7 미만) 과윤문을 의심하고 이유를 설명한다. 그다음 Stage 4 승인을 받는다.

핵심 문장(`###`)의 표현을 다듬고 싶으면 먼저 `plan/outline.md`의 headline을 고쳐 Stage 3을 다시 승인받은 뒤 `slides.md`에 반영한다. 윤문은 내용 승인을 대신하지 않는다.
