# Graph Report - rvlab-ppt-generator  (2026-10-13)

## Corpus Check
- Corpus is ~33,123 words - fits in a single context window. You may not need a graph.

## Summary
- 534 nodes · 1328 edges · 22 communities (19 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 65 edges (avg confidence: 0.84)
- Token cost: 63,082 input · 0 output

## Community Hubs (Navigation)
- Markdown Parsing and Build Tests
- Animation and Math Build Tests
- Paper Extraction
- PPTX Build and Render QA 3
- Chart Tests
- Stage Approval State
- Animation and Math Build Tests 2
- Markdown Parsing and Build Tests 2
- PPTX Build and Render QA 4
- PPTX Build and Render QA 5
- Chart Recipes
- PPTX Build and Render QA
- PPTX Build and Render QA 2
- Node Renderers
- Project Root
- Template and Content Rules
- Agent Guide and Approval Flow 2
- Vendored External Skills
- Interview Method
- External Figures and Polishing
- CLI, Fonts and Document Tools
- Agent Guide and Approval Flow

## God Nodes (most connected - your core abstractions)
1. `BuildTests` - 48 edges
2. `StateError` - 47 edges
3. `StateTests` - 42 edges
4. `approve()` - 29 edges
5. `status()` - 28 edges
6. `AGENTS.md (RVLAB PPT 공통 지침)` - 27 edges
7. `sha256()` - 23 edges
8. `assemble()` - 22 edges
9. `build()` - 21 edges
10. `resolve_fonts()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Hand-edited PPTX Overwrite Guard` --semantically_similar_to--> `원본 양식 불변 / RVLAB_reference.pptx 파생 사용`  [INFERRED] [semantically similar]
  docs/rendering.md → AGENTS.md
- `AnimationTests` --uses--> `StateError`  [INFERRED]
  tests/test_animation.py → tools/rvppt/state.py
- `BuildTests` --uses--> `StateError`  [INFERRED]
  tests/test_build.py → tools/rvppt/state.py
- `PaperTests` --uses--> `StateError`  [INFERRED]
  tests/test_papers.py → tools/rvppt/state.py
- `StateTests` --uses--> `StateError`  [INFERRED]
  tests/test_state.py → tools/rvppt/state.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Stage approval hash chain** — docs_schemas_review_hash, docs_schemas_input_hashes, docs_schemas_effective_status, docs_schemas_content_approved, docs_workflow_invalidation [EXTRACTED 1.00]
- **Pinned external skill governance** — docs_skills_pinned_external_skills, docs_setup_doctor, docs_setup_lf_line_endings, docs_document_tools_license_policy, docs_skills_editorial_isolation [INFERRED 0.85]
- **Markdown to PPTX build and QA** — docs_toolchain_pipeline, docs_rendering_build_qa, design_fixed_tokens, design_derived_reference, docs_rendering_layout_inference [INFERRED 0.85]
- **Paper figure extraction, selection and provenance pipeline** — skills_rvlab_ppt_references_external_visuals_extract_paper, skills_rvlab_ppt_references_external_visuals_caption_based_selection, skills_rvlab_ppt_references_external_visuals_visual_sources_yaml, skills_rvlab_ppt_references_external_visuals_figures_external_vs_sources [EXTRACTED 1.00]
- **단계 승인 파이프라인 (stage 문서·review_hash·상태 계산)** — agents_four_stage_approval, agents_review_hash_approval, agents_content_approved, docs_schemas, tools_rvppt_state [INFERRED 0.85]
- **시각 설계 → 표현 선택 → 차트/애니메이션 제작 → 슬라이드 검수** — skills_rvlab_ppt_references_visual_planning_necessity_role, skills_rvlab_ppt_references_visual_planning_representation_table, skills_rvlab_charts_skill_recipe_selection, skills_rvlab_animation_skill, skills_rvlab_ppt_references_visual_planning_slide_figure_qa [EXTRACTED 1.00]
- **그림 확보 정책 (찾아 넣기·구조 도식 직접 제작·요청 상자, 날조 금지)** — skills_rvlab_ppt_skill_figure_paths, skills_rvlab_ppt_skill_figure_request_box, skills_rvlab_charts_skill_numeric_vs_structural_rule, agents_no_fabrication, skills_rvlab_ppt_references_external_visuals [INFERRED 0.85]

## Communities (22 total, 3 thin omitted)

### Community 0 - "Markdown Parsing and Build Tests"
Cohesion: 0.05
Nodes (31): CliIntegrationTests, GraphCheckTests, IgnoreTests, SkillIntegrityTests, TemplateTests, make_task(), slides_body(), run_cli_smoke() (+23 more)

### Community 14 - "Paper Extraction"
Cohesion: 0.18
Nodes (6): PaperTests, main(), _task_path(), extract_paper(), difference(), polish_check()

### Community 15 - "PPTX Build and Render QA 3"
Cohesion: 0.17
Nodes (10): StateError, build(), fingerprint(), _last_report(), preview(), publish(), _workspace(), load_profile() (+2 more)

### Community 2 - "Stage Approval State"
Cohesion: 0.14
Nodes (3): StateTests, approve(), status()

### Community 5 - "Animation and Math Build Tests 2"
Cohesion: 0.08
Nodes (8): AnimationTests, doctor(), browser(), fonts(), libreoffice(), template(), chrome_binary(), load_tokens()

### Community 7 - "Markdown Parsing and Build Tests 2"
Cohesion: 0.15
Nodes (14): Document, UniqueLoader, _digest(), _inspect(), _outline(), read_document(), review_issues(), review_warnings() (+6 more)

### Community 17 - "PPTX Build and Render QA 4"
Cohesion: 0.20
Nodes (6): deck_findings(), lint(), output_stem(), deck_info(), parse_task(), units()

### Community 20 - "PPTX Build and Render QA 5"
Cohesion: 0.40
Nodes (3): render_and_check(), visual_rows(), contact_sheet()

### Community 3 - "Chart Recipes"
Cohesion: 0.12
Nodes (18): _arrow(), _box(), _canvas(), cards(), demo(), donut(), _fit(), flow() (+10 more)

### Community 4 - "PPTX Build and Render QA"
Cohesion: 0.12
Nodes (18): add_text(), assemble(), box_of(), compose(), copy_fragment(), equation(), figure_request(), fill_template() (+10 more)

### Community 9 - "PPTX Build and Render QA 2"
Cohesion: 0.19
Nodes (14): native_fragments(), requested_figures(), animation_metadata(), asset_path(), build_slots(), bullet_items(), image_node(), is_figure() (+6 more)

### Community 10 - "Node Renderers"
Cohesion: 0.11
Nodes (17): dependencies, mathjax-full, @mermaid-js/mermaid-cli, @resvg/resvg-js, description, engines, node, name (+9 more)

### Community 11 - "Template and Content Rules"
Cohesion: 0.16
Nodes (12): Build Pipeline and LibreOffice Render QA, Derived Reference Template (RVLAB_reference.pptx), Figure Slot Grid (1/2/3/4 slots, 0.24in gap, 0.36in caption), Fixed Design Tokens YAML (palette, fonts, sizes, geometry, limits, layouts), Font Fallback (Arial/Malgun Gothic -> Liberation Sans/Noto Sans CJK KR), Slide Grammar (# section | subtitle, ## topic, ### headline), pptx-generator (reference only), Figure Request Placeholder (missing_figures) (+4 more)

### Community 12 - "Agent Guide and Approval Flow 2"
Cohesion: 0.16
Nodes (13): content_approved (내용 승인 상태), 4단계 승인 흐름 (interview→brief→outline→slides), Common Stage Frontmatter (schema_version, task_id, stage, status, hashes), content_approved Flag, Effective Status (missing/draft/approved/stale/invalid), Input Hashes (sources/, prior stages, figures/), review_hash (content_hash + upstream hashes), 제작에 넘길 그림 요약 (outline figure 문자열) (+5 more)

### Community 13 - "Vendored External Skills"
Cohesion: 0.13
Nodes (15): GIF Animation with Representative PNG, im-not-ai (humanize-korean, MIT, available), manim-composer (reference_only), manimce-best-practices, minimax-docx skill, minimax-xlsx skill, pdf skill (openai/skills, Apache-2.0), pptx-generator (reference_only) (+7 more)

### Community 16 - "Interview Method"
Cohesion: 0.16
Nodes (14): brainstorming (superpowers, reference_only), office-hours (gstack, reference_only), Answer-driven branching table, Co-creation mode (같이 만들기) per-stage questions, Question bundle (3-5 questions with options + free input), Fact / user requirement / agent assumption / unresolved classification, Explicit approval via rvppt approve --expected-hash review_hash, Stage 1-3 plan documents (interview.md, brief.md, outline.md) (+6 more)

### Community 18 - "External Figures and Polishing"
Cohesion: 0.25
Nodes (7): Good slide conditions, Post-build visual checklist (contact-sheet, slide-NN.png), Presentation type skeletons (progress report, paper review, study), 시각 자료의 필요성과 역할 판단, 그림 세 경로 (찾아 넣기·직접 만들기·요청하기), 그림 요청 상자 / missing_figures, Lab meeting presentation guide

### Community 6 - "CLI, Fonts and Document Tools"
Cohesion: 0.12
Nodes (17): PyMuPDF4LLM 0.2.9 Paper Extraction, rvppt doctor Environment Check, rvppt polish-check (Pandoc AST preservation), rvppt CLI (new·status·approve·lint·build·preview·polish-check·extract-paper·doctor·graph-check), Auto-generated Cover/TOC/Closing Slides, Formula OCR Candidates (Mathpix, Nougat, Marker), Equations (LaTeX -> OMML + _수식호환.pptx images), Skill Entrypoint Symlinks (.claude/skills, .agents/skills) (+9 more)

### Community 8 - "Agent Guide and Approval Flow"
Cohesion: 0.13
Nodes (16): 금지사항 (양식 변경·해시 조작·PPTX 직접 수정 등), 슬라이드 분량 제약 (메시지 1개·불릿 5·깊이 2·표 8행 6열), Overleaf식 task 폴더 구조 (slides.md·figures·sources·plan), Format-to-Tool Selection Matrix, Draft PPT Intake (markitdown, unzip media), Progress Modes (같이 만들기 / 핵심만), rvppt polish-check preservation gate (before.md, similarity), Polish protected elements (section/topic lines, blocks, math, paths, numbers) (+8 more)

## Ambiguous Edges - Review These
- `office-hours (gstack, reference_only)` → `rvlab-interview SKILL`  [AMBIGUOUS]
  skills/dependencies.yaml · relation: conceptually_related_to
- `brainstorming (superpowers, reference_only)` → `rvlab-interview SKILL`  [AMBIGUOUS]
  skills/dependencies.yaml · relation: conceptually_related_to

## Knowledge Gaps
- **32 isolated node(s):** `name`, `private`, `version`, `description`, `node` (+27 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 145 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `office-hours (gstack, reference_only)` and `rvlab-interview SKILL`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `rvlab-interview SKILL` connect `Interview Method` to `Agent Guide and Approval Flow`, `External Figures and Polishing`, `Agent Guide and Approval Flow 2`, `Markdown Parsing and Build Tests 2`?**
  _High betweenness centrality (0.227) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `StateError` (e.g. with `AnimationTests` and `BuildTests`) actually correct?**
  _`StateError` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _32 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Markdown Parsing and Build Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.05154639175257732 - nodes in this community are weakly interconnected._
- **What is the exact relationship between `brainstorming (superpowers, reference_only)` and `rvlab-interview SKILL`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `StateError` connect `PPTX Build and Render QA 3` to `Markdown Parsing and Build Tests`, `Animation and Math Build Tests`, `Stage Approval State`, `PPTX Build and Render QA`, `Animation and Math Build Tests 2`, `Markdown Parsing and Build Tests 2`, `PPTX Build and Render QA 2`, `Paper Extraction`, `PPTX Build and Render QA 4`, `PPTX Build and Render QA 5`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._