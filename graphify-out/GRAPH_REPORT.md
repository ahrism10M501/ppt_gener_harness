# Graph Report - rvlab-ppt-generator  (2026-10-11)

## Corpus Check
- Corpus is ~26,102 words - fits in a single context window. You may not need a graph.

## Summary
- 673 nodes · 1326 edges · 41 communities (25 shown, 16 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 62 edges (avg confidence: 0.86)
- Token cost: unavailable (host subagent usage is not exposed; zero counters are placeholders, not measured usage)

## Community Hubs (Navigation)
- Build and Markdown Pipeline
- Workflow and Stage Approval
- Build Regression Tests
- PPT Production and QA
- Interview and Planning Skill
- State Regression Tests
- Project Usage and Setup
- Agent Rules and Constraints
- State and Approval Logic
- Research Interview Guide
- RVLAB Design and Layout
- Node Rendering Dependencies
- Doctor and Environment Checks
- Test Fixtures and Imports
- Reference Template Generation
- Editorial and Document Skills
- Outline and Figure Planning
- Python Production Toolchain
- Project Creation and CLI Tests
- Math and Rendering Support
- Graph Snapshot Validation
- Integrity and Ignore Tests
- Template Regression Tests
- Vendored Skill Dependencies
- CLI Entry Points
- Approval Hash Schema
- Slide Syntax and Lint
- Task Folder Structure
- Graph Privacy and Exclusions
- Source and Profile Example
- Build Output Preservation
- Content Approval Meaning
- Read Only Doctor
- Fixed Design Tokens
- Editable Math and Fallback
- Topic and Core Sentence
- Korean Polish Preservation
- Cover Profile and Creation
- Claude Agent Entry
- Codex Agent Entry
- Project Package

## God Nodes (most connected - your core abstractions)
1. `BuildTests` - 46 edges
2. `StateTests` - 39 edges
3. `approve()` - 26 edges
4. `status()` - 23 edges
5. `DESIGN.md: RVLAB 디자인 명세` - 19 edges
6. `doctor()` - 17 edges
7. `assemble()` - 17 edges
8. `build()` - 17 edges
9. `plain()` - 15 edges
10. `StateError` - 13 edges

## Surprising Connections (you probably didn't know these)
- `실제 task 자료의 Graphify 제외` --semantically_similar_to--> `sources/ 원자료 읽기 전용`  [INFERRED] [semantically similar]
  AGENTS.md → docs/workflow.md
- `사람이 고친 PPTX 빌드 중단·덮어쓰기 금지` --semantically_similar_to--> `실패 빌드에서 이전 성공 산출물 보존`  [INFERRED] [semantically similar]
  skills/rvlab-ppt/SKILL.md → AGENTS.md
- `좋은 슬라이드의 조건` --semantically_similar_to--> `본문 제한 (불릿 5·깊이 2·표 8행×6열)`  [INFERRED] [semantically similar]
  skills/rvlab-ppt/references/lab-meeting.md → DESIGN.md
- `3~5개 항목·2~3개 선택지·자유 입력` --semantically_similar_to--> `미확인 항목 3~5개 질문 묶음`  [INFERRED] [semantically similar]
  skills/rvlab-interview/references/interview-guide.md → AGENTS.md
- `사실·요구·추정·미해결 구분` --semantically_similar_to--> `자료 사실·근거 파일·위치·주장 범위`  [INFERRED] [semantically similar]
  AGENTS.md → skills/rvlab-interview/SKILL.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Four-stage research presentation workflow** — docs_workflow_stage1, docs_workflow_stage2, docs_workflow_stage3, docs_workflow_stage4 [EXTRACTED 1.00]
- **4단계 승인 문서 체인 (interview→brief→outline→slides, review_hash·approve)** — docs_schemas_stage1_interview, docs_schemas_stage2_brief, docs_schemas_stage3_outline, docs_schemas_stage4_slides_md, docs_schemas_review_hash [EXTRACTED 1.00]
- **한국어 윤문·보존 검사 흐름** — skills_rvlab_ppt_references_polish, skills_dependencies_im_not_ai, skills_rvlab_ppt_references_polish_editorial_workspace, skills_rvlab_ppt_references_polish_preservation_rules [EXTRACTED 1.00]
- **Markdown→PPTX 제작·렌더 QA 파이프라인** — docs_toolchain_production_pipeline, docs_toolchain_pandoc, docs_toolchain_python_deps, docs_toolchain_node_deps, docs_toolchain_libreoffice [EXTRACTED 1.00]
- **Distinguish facts, requirements, assumptions, and unresolved items** — skills_rvlab_interview_skill_facts, skills_rvlab_interview_skill_requirements, skills_rvlab_interview_skill_assumptions, skills_rvlab_interview_skill_open_items [EXTRACTED 1.00]
- **Presentation production and verification** — skills_rvlab_ppt_skill_slides, skills_rvlab_ppt_skill_lint, skills_rvlab_ppt_skill_build, skills_rvlab_ppt_skill_preview, skills_rvlab_ppt_skill_report [EXTRACTED 1.00]
- **한국어 윤문 흐름 (humanize-korean·editorial 격리·polish-check)** — docs_skills_im_not_ai, docs_skills_editorial_isolation, docs_skills_polish_check, skills_rvlab_ppt_references_polish [INFERRED 0.85]

## Communities (41 total, 16 thin omitted)

### Community 0 - "Build and Markdown Pipeline"
Cohesion: 0.05
Nodes (47): add_text(), assemble(), box_of(), build(), compose(), copy_fragment(), deck_findings(), equation() (+39 more)

### Community 1 - "Workflow and Stage Approval"
Cohesion: 0.05
Nodes (56): docs/workflow.md, 명시적 승인 후 rvppt approve --expected-hash, superpowers brainstorming 고정 커밋 bb92a77741419a4ab5f06e711a283343f1ada0c3, plan/brief.md, rvppt build 언제든 실행 / 승인 전 최종 전달 금지, .build/ PNG·리포트·중간 파일, 근거 있는 메시지·스토리라인 후보 2~3개, 추가 확인 두 차례 후 후보·추천 제시 (+48 more)

### Community 3 - "PPT Production and QA"
Cohesion: 0.07
Nodes (42): skills/rvlab-ppt/SKILL.md, AGENTS.md, 명시적 승인 뒤 Stage 4 approve --expected-hash, 빌드가 표지·목차·감사합니다 생성, rvppt build 언제든 / 승인 전 최종 전달 금지, 같이 만들기에서 섹션마다 3~5개 질문, DESIGN.md, rvppt doctor 도구·폰트·외부 스킬 해시 읽기 전용 (+34 more)

### Community 4 - "Interview and Planning Skill"
Cohesion: 0.07
Nodes (40): 사실·요구·추정·미해결 구분, skills/rvlab-interview/SKILL.md, rvlab-interview 스킬, AGENTS.md, rvppt approve --stage --expected-hash, 에이전트 추정·동의 전 요구로 기록 금지, plan/brief.md, 2~3개 메시지·스토리라인 후보 (+32 more)

### Community 5 - "State Regression Tests"
Cohesion: 0.15
Nodes (3): StateTests, approve(), status()

### Community 6 - "Project Usage and Setup"
Cohesion: 0.09
Nodes (33): skills/dependencies.yaml 출처·라이선스·해시, README.md 문서 안내, AGENTS.md, docs/architecture.md, superpowers / brainstorming 의도 탐색·MIT, rvppt build → 날짜_제목.pptx/.pdf, skills/dependencies.yaml 고정 커밋·파일 해시, DESIGN.md (+25 more)

### Community 7 - "Agent Rules and Constraints"
Cohesion: 0.07
Nodes (26): docs/architecture.md, 같이 만들기 / 핵심만, docs/document-tools.md, task/.build/editorial/ 격리, Arial·맑은 고딕 / Liberation Sans·Noto Sans CJK KR, 입력 수정 후 재생성, rvppt lint, 수치·인용·결과 생성 금지 (+18 more)

### Community 8 - "State and Approval Logic"
Cohesion: 0.15
Nodes (14): _digest(), Document, _inspect(), _mapping(), read_document(), review_issues(), slide_headings(), StateError (+6 more)

### Community 9 - "Research Interview Guide"
Cohesion: 0.15
Nodes (20): 미확인 항목 3~5개 질문 묶음, 중요 근거 부족 시 주장 축소 또는 blocking, 실제 참석자·ACT/BC 사전 지식, 3~5개 항목·2~3개 선택지·자유 입력, 근거 없으면 후보 추천·주장 축소·blocking, 구체 사례·위치 확인 최대 두 차례, 같이 만들기 단계별 지속 질문, 시간·유형·필수/제외·우선순위 (+12 more)

### Community 10 - "RVLAB Design and Layout"
Cohesion: 0.17
Nodes (15): DESIGN.md: RVLAB 디자인 명세, 표지·목차·마무리 자동 생성, 그림 슬롯 그리드 (1·2·3·2×2, 간격 0.24in·캡션 0.36in), templates/examples/ 연구실 발표 예시, 레이아웃 매핑 (cover·toc·section·content·columns·figure_2/3/4), RVLAB_PPT양식.pptx 원본 (10×7.5in·4:3·마스터 1·레이아웃 4), 금지 스타일과 실제 렌더 검사, RVLAB_reference.pptx 파생 양식 (+7 more)

### Community 11 - "Node Rendering Dependencies"
Cohesion: 0.11
Nodes (17): dependencies, mathjax-full, @mermaid-js/mermaid-cli, @resvg/resvg-js, description, engines, node, name (+9 more)

### Community 12 - "Doctor and Environment Checks"
Cohesion: 0.16
Nodes (10): doctor(), fonts(), libreoffice(), skills(), template(), skill_integrity(), libreoffice_binary(), render_pdf() (+2 more)

### Community 14 - "Reference Template Generation"
Cohesion: 0.26
Nodes (12): build_reference(), content_layout(), extract_manifest(), main(), parse(), placeholder(), set_box(), set_text_style() (+4 more)

### Community 15 - "Editorial and Document Skills"
Cohesion: 0.19
Nodes (10): 수식·PDF·문서 포맷 도구 안내, 수식 OCR 후보 (Mathpix·Nougat·Marker), 도구 라이선스 구분 (PyMuPDF AGPL·Pandoc GPL·Typst Apache-2.0 등), 포함한 외부 스킬, superpowers / brainstorming, im-not-ai (humanize-korean), gstack / office-hours, rvppt polish-check (Pandoc AST 보존 검사) (+2 more)

### Community 16 - "Outline and Figure Planning"
Cohesion: 0.17
Nodes (14): LibreOffice 렌더 QA (누락·잘림·오버플로 검사), rvppt build, rvppt preview, Task 문서 스키마 v1, 공통 frontmatter (schema_version·task_id·stage·status·approval_hash·upstream_hashes), content_approved, content_hash (approval_hash에 저장), effective_status (missing·draft·approved·stale·invalid) (+6 more)

### Community 17 - "Python Production Toolchain"
Cohesion: 0.21
Nodes (11): 폰트 대체 (Liberation Sans·Noto Sans CJK KR), 포맷별 도구 선택 표, minimax-docx 스킬 (Open XML SDK·.NET 8 미설치), minimax-xlsx 스킬 (formula_check.py 정적 검사), pdf 스킬 (PyMuPDF·pdfplumber·pypdf·ReportLab), pptx-generator (참고용·발견 경로 미등록), typst 스킬 (Typst CLI 미설치), 도구 구성과 제약 (+3 more)

### Community 18 - "Project Creation and CLI Tests"
Cohesion: 0.24
Nodes (4): CliIntegrationTests, run_cli_smoke(), load_profile(), new_project()

### Community 19 - "Math and Rendering Support"
Cohesion: 0.27
Nodes (8): MathJax 수식 이미지 fallback, 설치와 환경 점검, 처음 설치 (uv sync --frozen·npm ci·profile.yaml·doctor), Mermaid 브라우저 (Chrome/Chromium·Puppeteer), OS별 도구 설치 표 (Ubuntu·macOS·Windows), rvppt doctor (읽기 전용 환경 점검), LibreOffice 렌더 QA, Node 의존성 (MathJax·Mermaid CLI·resvg)

### Community 20 - "Graph Snapshot Validation"
Cohesion: 0.35
Nodes (5): _candidates(), graph_check(), _graph_sources(), ignored(), _patterns()

### Community 21 - "Integrity and Ignore Tests"
Cohesion: 0.18
Nodes (3): GraphCheckTests, IgnoreTests, SkillIntegrityTests

### Community 23 - "Vendored Skill Dependencies"
Cohesion: 0.22
Nodes (9): skills/dependencies.yaml 외부 스킬 고정 버전·해시 목록, superpowers brainstorming (reference_only), im-not-ai (humanize-korean 한국어 윤문, MIT), minimax-docx 스킬, minimax-xlsx 스킬, gstack office-hours (reference_only), pdf 스킬 (openai/skills, Apache-2.0), pptx-generator (reference_only) (+1 more)

### Community 25 - "Approval Hash Schema"
Cohesion: 0.40
Nodes (4): rvppt approve --expected-hash, 명시적 사용자 승인, review_hash 문서·상위 입력 해시, review_hash 문서·상위 자료 동시 검증

### Community 26 - "Slide Syntax and Lint"
Cohesion: 0.40
Nodes (5): Markdown 제작과 QA, deck frontmatter (표지 정보), 그림 요청 상자 (missing_figures), rvppt lint, # 섹션 / ## 토픽 / ### 핵심 문장 문법

### Community 27 - "Task Folder Structure"
Cohesion: 0.50
Nodes (4): 연구자 그림 figures/, 승인 문서 plan/, 읽기 전용 sources/, Overleaf식 task 프로젝트

### Community 29 - "Source and Profile Example"
Cohesion: 0.67
Nodes (3): 재생성 가능한 PPTX, slides.md 발표 원본, profile.example.yaml (표지 인적사항 견본)

## Knowledge Gaps
- **106 isolated node(s):** `rvlab-ppt-generator`, `mathjax-full`, `@mermaid-js/mermaid-cli`, `@resvg/resvg-js`, `description` (+101 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 201 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `profile.yaml 표지 인적사항` connect `Cover Profile and Creation` to `RVLAB Design and Layout`, `Math and Rendering Support`, `Agent Rules and Constraints`?**
  _High betweenness centrality (0.227) - this node is a cross-community bridge._
- **What connects `rvlab-ppt-generator`, `mathjax-full`, `@mermaid-js/mermaid-cli` to the rest of the system?**
  _106 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Build and Markdown Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.05421686746987952 - nodes in this community are weakly interconnected._
- **Why does `slides.md 한국어 윤문 절차` connect `Editorial and Document Skills` to `RVLAB Design and Layout`, `Source and Profile Example`, `Vendored Skill Dependencies`?**
  _High betweenness centrality (0.225) - this node is a cross-community bridge._
- **Should `Workflow and Stage Approval` be split into smaller, more focused modules?**
  _Cohesion score 0.05202661826981246 - nodes in this community are weakly interconnected._
- **Why does `slides.md 발표 원본` connect `Source and Profile Example` to `Editorial and Document Skills`, `Agent Rules and Constraints`?**
  _High betweenness centrality (0.221) - this node is a cross-community bridge._
- **Should `Build Regression Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.05939716312056738 - nodes in this community are weakly interconnected._
## Incremental Update Integrity

- Updated 5 code files and 6 documents; unchanged source nodes were verified preserved.
- No dangling or missing endpoints in the merged graph.
- Graph health warning: 5 pre-existing self-loop edges remain (same count as before this update).
- Semantic subagent token usage was not exposed by the host. Zero counters in cost.json are placeholders, not measured token usage.
