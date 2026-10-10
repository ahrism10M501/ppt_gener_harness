# Graph Report - rvlab-ppt-generator  (2026-10-11)

## Corpus Check
- Corpus is ~25,335 words - fits in a single context window. You may not need a graph.

## Summary
- 465 nodes · 1219 edges · 16 communities (14 shown, 2 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 100 edges (avg confidence: 0.88)
- Token cost: 127,441 input · 0 output

## Community Hubs (Navigation)
- State, CLI and Graph Check
- Build and Render Pipeline
- Build Tests
- State Tests
- Toolchain and Format Docs
- Vendored Skills
- Template and Reference
- Design Spec
- Doctor Checks
- Node Renderers
- Project Workflow
- Agent Rules
- Planning Stages
- Approval Schema
- Stage 4 and Polish
- Python Project Metadata

## God Nodes (most connected - your core abstractions)
1. `BuildTests` - 47 edges
2. `StateError` - 42 edges
3. `StateTests` - 39 edges
4. `AGENTS.md: RVLAB PPT 공통 지침` - 31 edges
5. `status()` - 26 edges
6. `approve()` - 26 edges
7. `연구 발표 제작 워크플로우` - 24 edges
8. `DESIGN.md: RVLAB 디자인 명세` - 23 edges
9. `rvlab-ppt 스킬` - 22 edges
10. `build()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `좋은 슬라이드의 조건` --semantically_similar_to--> `본문 제한 (불릿 5·깊이 2·표 8행×6열)`  [INFERRED] [semantically similar]
  skills/rvlab-ppt/references/lab-meeting.md → DESIGN.md
- `Stage 4 승인 절차 (lint→윤문·polish-check→review_hash→approve)` --conceptually_related_to--> `rvppt lint`  [INFERRED]
  skills/rvlab-ppt/SKILL.md → docs/rendering.md
- `답변·관찰별 다음 행동 표` --semantically_similar_to--> `답변에 따른 분기 (근거 없는 주장·숨은 전제·상충 요구·주제 미정)`  [INFERRED] [semantically similar]
  docs/workflow.md → skills/rvlab-interview/references/interview-guide.md
- `발표 유형별 뼈대 (진행 보고·논문 리뷰·스터디)` --conceptually_related_to--> `슬라이드 문법 (# 섹션 | 부제 / ## 토픽 / ### 핵심 문장)`  [INFERRED]
  skills/rvlab-ppt/references/lab-meeting.md → DESIGN.md
- `BuildTests` --uses--> `StateError`  [INFERRED]
  tests/test_build.py → tools/rvppt/state.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **4단계 승인 문서 체인 (interview→brief→outline→slides, review_hash·approve)** — docs_schemas_stage1_interview, docs_schemas_stage2_brief, docs_schemas_stage3_outline, docs_schemas_stage4_slides_md, docs_schemas_review_hash, docs_workflow_rvppt_approve [EXTRACTED 1.00]
- **한국어 윤문·보존 검사 흐름** — skills_rvlab_ppt_references_polish, skills_dependencies_im_not_ai, skills_rvlab_ppt_references_polish_editorial_workspace, skills_rvlab_ppt_references_polish_preservation_rules [EXTRACTED 1.00]
- **Markdown→PPTX 제작·렌더 QA 파이프라인** — docs_toolchain_production_pipeline, docs_toolchain_pandoc, docs_toolchain_python_deps, docs_toolchain_node_deps, docs_toolchain_libreoffice [EXTRACTED 1.00]
- **한국어 윤문 흐름 (humanize-korean·editorial 격리·polish-check)** — docs_skills_im_not_ai, docs_skills_editorial_isolation, docs_skills_polish_check, skills_rvlab_ppt_references_polish, skills_rvlab_ppt_skill_stage4_approval [INFERRED 0.85]

## Communities (16 total, 2 thin omitted)

### Community 0 - "State, CLI and Graph Check"
Cohesion: 0.05
Nodes (30): state.py·cli.py 재사용 (인터뷰 전용 scripts 없음), make_task(), slides_body(), CliIntegrationTests, run_cli_smoke(), GraphCheckTests, IgnoreTests, main() (+22 more)

### Community 1 - "Build and Render Pipeline"
Cohesion: 0.07
Nodes (51): add_text(), assemble(), box_of(), build(), compose(), copy_fragment(), equation(), figure_request() (+43 more)

### Community 3 - "State Tests"
Cohesion: 0.15
Nodes (3): StateTests, approve(), status()

### Community 4 - "Toolchain and Format Docs"
Cohesion: 0.10
Nodes (25): 폰트 대체 (Liberation Sans·Noto Sans CJK KR), RVLAB_reference.pptx 파생 양식, 포맷별 도구 선택 표, minimax-docx 스킬 (Open XML SDK·.NET 8 미설치), minimax-xlsx 스킬 (formula_check.py 정적 검사), pdf 스킬 (PyMuPDF·pdfplumber·pypdf·ReportLab), pptx-generator (참고용·발견 경로 미등록), 도구 라이선스 구분 (PyMuPDF AGPL·Pandoc GPL·Typst Apache-2.0 등) (+17 more)

### Community 5 - "Vendored Skills"
Cohesion: 0.13
Nodes (20): 스킬 발견 진입점 (.agents/skills·.claude/skills → skills/), 수식·PDF·문서 포맷 도구 안내, 수식 OCR 후보 (Mathpix·Nougat·Marker), 포함한 외부 스킬, superpowers / brainstorming, im-not-ai (humanize-korean), gstack / office-hours, rvppt polish-check (Pandoc AST 보존 검사) (+12 more)

### Community 6 - "Template and Reference"
Cohesion: 0.13
Nodes (11): TemplateTests, build_reference(), content_layout(), extract_manifest(), main(), parse(), placeholder(), set_box() (+3 more)

### Community 7 - "Design Spec"
Cohesion: 0.15
Nodes (16): DESIGN.md: RVLAB 디자인 명세, 표지·목차·마무리 자동 생성, 그림 슬롯 그리드 (1·2·3·2×2, 간격 0.24in·캡션 0.36in), templates/examples/ 연구실 발표 예시, 레이아웃 매핑 (cover·toc·section·content·columns·figure_2/3/4), RVLAB_PPT양식.pptx 원본 (10×7.5in·4:3·마스터 1·레이아웃 4), 금지 스타일과 실제 렌더 검사, rvlab.mplstyle (+8 more)

### Community 8 - "Doctor Checks"
Cohesion: 0.13
Nodes (9): SkillIntegrityTests, doctor(), fonts(), libreoffice(), skills(), template(), skill_integrity(), libreoffice_binary() (+1 more)

### Community 9 - "Node Renderers"
Cohesion: 0.11
Nodes (17): dependencies, mathjax-full, @mermaid-js/mermaid-cli, @resvg/resvg-js, description, engines, node, name (+9 more)

### Community 10 - "Project Workflow"
Cohesion: 0.23
Nodes (15): profile.yaml 표지 인적사항, Task 폴더 (slides.md·figures/·sources/·plan/·YYYYMMDD_제목.pptx), 공통 frontmatter (schema_version·task_id·stage·status·approval_hash·upstream_hashes), 연구 발표 제작 워크플로우, 답변·관찰별 다음 행동 표, 초안 PPT 읽기 (markitdown·LibreOffice·unzip), Overleaf형 task 폴더 구조, rvppt new (profile.yaml→deck) (+7 more)

### Community 11 - "Agent Rules"
Cohesion: 0.17
Nodes (10): AGENTS.md: RVLAB PPT 공통 지침, 완성 예제 tasks/261011-example-il-progress, graphify-out 프로젝트 구조 스냅샷, plan/interview.md (Stage 1: 청중·목적·근거·전제), 금지사항 (원본 양식 변경·승인 해시 조작·PPTX 직접 수정·인적사항 추측 등), rvppt 명령 (new·status·approve·lint·build·preview·polish-check·doctor·graph-check), CLAUDE.md (@AGENTS.md 포인터), CODEX.md (@AGENTS.md 포인터) (+2 more)

### Community 12 - "Planning Stages"
Cohesion: 0.18
Nodes (12): plan/brief.md (Stage 2: 핵심 메시지·스토리라인 후보), plan/outline.md (Stage 3: ID·섹션·토픽·핵심 문장·근거·시간·그림 제안), Stage 2 스키마: brief.md candidates, Stage 3 스키마: outline.md slides, Stage 2 핵심 메시지 선택, Stage 3 목차와 주장–근거 연결, 단계별 결과물 (interview·brief·outline), 랩미팅용 RVLAB 발표 가이드 (+4 more)

### Community 13 - "Approval Schema"
Cohesion: 0.36
Nodes (8): Task 문서 스키마 v1, content_approved, content_hash (approval_hash에 저장), effective_status (missing·draft·approved·stale·invalid), 입력 해시 (sources/·이전 단계·figures/), review_hash (content_hash + 상위 입력 해시), 단계 종료와 변경 (재승인 규칙), rvppt approve --expected-hash

### Community 14 - "Stage 4 and Polish"
Cohesion: 0.33
Nodes (7): slides.md (Stage 4: 본문·그림 요청·표·수식·출처·노트), Stage 4 스키마: slides.md deck·language, Stage 4 내용·윤문·제작 QA, profile.example.yaml (표지 인적사항 견본), im-not-ai (humanize-korean 한국어 윤문, MIT), slides.md 한국어 윤문 절차, .build/editorial 격리 작업 폴더

## Knowledge Gaps
- **28 isolated node(s):** `name`, `private`, `version`, `description`, `node` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 101 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `StateError` connect `Build and Render Pipeline` to `State, CLI and Graph Check`, `Build Tests`, `State Tests`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `StateError` (e.g. with `BuildTests` and `StateTests`) actually correct?**
  _`StateError` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _28 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `State, CLI and Graph Check` be split into smaller, more focused modules?**
  _Cohesion score 0.052604698672114404 - nodes in this community are weakly interconnected._
- **Why does `BuildTests` connect `Build Tests` to `State, CLI and Graph Check`, `Doctor Checks`, `Build and Render Pipeline`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Should `Build and Render Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.06848425835767608 - nodes in this community are weakly interconnected._
- **Why does `AGENTS.md: RVLAB PPT 공통 지침` connect `Agent Rules` to `Toolchain and Format Docs`, `Vendored Skills`, `Design Spec`, `Project Workflow`, `Planning Stages`, `Approval Schema`, `Stage 4 and Polish`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._