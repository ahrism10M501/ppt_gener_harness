# Graph Report - harness-review  (2026-10-12)

## Corpus Check
- Corpus is ~33,086 words - fits in a single context window. You may not need a graph.

## Summary
- 521 nodes · 1314 edges · 22 communities (19 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 70 edges (avg confidence: 0.86)
- Token cost: 237,747 input · 0 output

## Community Hubs (Navigation)
- PPTX Build and Render QA
- Markdown Parsing and Build Tests
- Animation and Math Build Tests
- Stage Approval State
- CLI, Fonts and Document Tools
- Chart Recipes
- Vendored External Skills
- Agent Guide and Approval Flow
- Paper Extraction
- Node Renderers
- External Figures and Polishing
- Template and Content Rules
- Graphify Snapshot Check
- Environment Doctor
- Template Tests
- Reference Template Generator
- Preview and Publish
- Interview Method
- Skill Integrity Checks
- Ignore and Tracking Rules
- Chart Tests
- Project Root

## God Nodes (most connected - your core abstractions)
1. `BuildTests` - 48 edges
2. `StateError` - 47 edges
3. `StateTests` - 42 edges
4. `approve()` - 29 edges
5. `status()` - 28 edges
6. `sha256()` - 23 edges
7. `assemble()` - 22 edges
8. `build()` - 21 edges
9. `resolve_fonts()` - 20 edges
10. `doctor()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Hand-edited PPTX Overwrite Guard` --semantically_similar_to--> `Original Template Immutability`  [INFERRED] [semantically similar]
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
- **Markdown to PPTX build and QA** — docs_toolchain_pipeline, docs_rendering_build_qa, design_fixed_tokens, design_derived_reference, docs_rendering_layout_inference [INFERRED 0.85]
- **Pinned external skill governance** — docs_skills_pinned_external_skills, docs_setup_doctor, docs_setup_lf_line_endings, docs_document_tools_license_policy, docs_skills_editorial_isolation [INFERRED 0.85]
- **Visual planning routes figures to charts, animation, scientific-visualization and external visuals** — skills_rvlab_ppt_references_visual_planning, skills_rvlab_charts_skill, skills_rvlab_animation_skill, skills_dependencies_scientific_visualization, skills_rvlab_ppt_references_external_visuals, skills_dependencies_scientific_slides [EXTRACTED 1.00]
- **Stage 1-4 planning, polish and hash-gated approval flow** — skills_rvlab_interview_skill_stage_documents, skills_rvlab_interview_skill_hash_approval, skills_rvlab_ppt_references_polish_polish_check, skills_rvlab_ppt_skill_build_preview_qa, tools_rvppt_state [INFERRED 0.85]
- **Paper figure extraction, selection and provenance pipeline** — skills_rvlab_ppt_references_external_visuals_extract_paper, skills_rvlab_ppt_references_external_visuals_caption_based_selection, skills_rvlab_ppt_references_external_visuals_visual_sources_yaml, skills_rvlab_ppt_references_external_visuals_figures_external_vs_sources [EXTRACTED 1.00]

## Communities (22 total, 3 thin omitted)

### Community 0 - "PPTX Build and Render QA"
Cohesion: 0.07
Nodes (50): add_text(), assemble(), box_of(), build(), compose(), copy_fragment(), deck_findings(), equation() (+42 more)

### Community 1 - "Markdown Parsing and Build Tests"
Cohesion: 0.07
Nodes (18): make_task(), slides_body(), CliIntegrationTests, run_cli_smoke(), _digest(), Document, _inspect(), _mapping() (+10 more)

### Community 2 - "Animation and Math Build Tests"
Cohesion: 0.05
Nodes (3): AnimationTests, BuildTests, resolve_fonts()

### Community 3 - "Stage Approval State"
Cohesion: 0.14
Nodes (3): StateTests, approve(), status()

### Community 4 - "CLI, Fonts and Document Tools"
Cohesion: 0.11
Nodes (19): rvppt CLI (new/status/approve/lint/build/preview/polish-check/extract-paper/doctor/graph-check), Auto-generated Cover/TOC/Closing Slides, Font Fallback (Arial/Malgun Gothic -> Liberation Sans/Noto Sans CJK KR), Formula OCR Candidates (Mathpix, Nougat, Marker), PyMuPDF4LLM 0.2.9 Paper Extraction, Equations (LaTeX -> OMML + _수식호환.pptx images), rvppt doctor Environment Check, Skill Entrypoint Symlinks (.claude/skills, .agents/skills) (+11 more)

### Community 5 - "Chart Recipes"
Cohesion: 0.16
Nodes (13): _arrow(), _box(), _canvas(), cards(), demo(), donut(), _fit(), flow() (+5 more)

### Community 6 - "Vendored External Skills"
Cohesion: 0.11
Nodes (20): GIF Animation with Representative PNG, dependencies.yaml (external skill pins), manim-composer (reference_only), manimce-best-practices, minimax-docx skill, minimax-xlsx skill, pdf skill (openai/skills, Apache-2.0), pptx-generator (reference_only) (+12 more)

### Community 7 - "Agent Guide and Approval Flow"
Cohesion: 0.16
Nodes (13): Task Folder (Overleaf-like: slides.md, figures, sources, plan), Format-to-Tool Selection Matrix, Common Stage Frontmatter (schema_version, task_id, stage, status, hashes), content_approved Flag, Effective Status (missing/draft/approved/stale/invalid), Input Hashes (sources/, prior stages, figures/), review_hash (content_hash + upstream hashes), Stage 1 plan/interview.md (+5 more)

### Community 8 - "Paper Extraction"
Cohesion: 0.15
Nodes (6): PaperTests, main(), _task_path(), extract_paper(), load_profile(), new_project()

### Community 9 - "Node Renderers"
Cohesion: 0.11
Nodes (17): dependencies, mathjax-full, @mermaid-js/mermaid-cli, @resvg/resvg-js, description, engines, node, name (+9 more)

### Community 10 - "External Figures and Polishing"
Cohesion: 0.15
Nodes (19): im-not-ai (humanize-korean, MIT, available), Explicit approval via rvppt approve --expected-hash review_hash, External photos & paper figures procedure, Caption/body-based figure selection, rvppt extract-paper (PyMuPDF4LLM -> paper.md, pages.json, media/), figures/visual-sources.yaml provenance record, Lab meeting presentation guide, Good slide conditions (+11 more)

### Community 11 - "Template and Content Rules"
Cohesion: 0.17
Nodes (9): Derived Reference Template (RVLAB_reference.pptx), Figure Slot Grid (1/2/3/4 slots, 0.24in gap, 0.36in caption), Fixed Design Tokens YAML (palette, fonts, sizes, geometry, limits, layouts), Slide Grammar (# section | subtitle, ## topic, ### headline), pptx-generator (reference only), Build Pipeline and LibreOffice Render QA, Figure Request Placeholder (missing_figures), Layout Inferred From Content (columns, figure grid, body) (+1 more)

### Community 12 - "Graphify Snapshot Check"
Cohesion: 0.23
Nodes (7): GraphCheckTests, _candidates(), graph_check(), _graph_sources(), ignored(), _patterns(), render_pdf()

### Community 13 - "Environment Doctor"
Cohesion: 0.17
Nodes (5): doctor(), browser(), libreoffice(), chrome_binary(), libreoffice_binary()

### Community 14 - "Template Tests"
Cohesion: 0.18
Nodes (3): TemplateTests, parse(), validate_package()

### Community 15 - "Reference Template Generator"
Cohesion: 0.35
Nodes (9): build_reference(), content_layout(), extract_manifest(), main(), placeholder(), set_box(), set_text_style(), slots() (+1 more)

### Community 16 - "Preview and Publish"
Cohesion: 0.24
Nodes (6): fingerprint(), preview(), fonts(), template(), load_tokens(), sha256()

### Community 17 - "Interview Method"
Cohesion: 0.29
Nodes (8): brainstorming (superpowers, reference_only), office-hours (gstack, reference_only), Interview question guide, Answer-driven branching table, Co-creation mode (같이 만들기) per-stage questions, Question bundle (3-5 questions with options + free input), rvlab-interview SKILL, Fact / user requirement / agent assumption / unresolved classification

### Community 18 - "Skill Integrity Checks"
Cohesion: 0.29
Nodes (4): SkillIntegrityTests, skills(), link_stand_in(), skill_integrity()

## Ambiguous Edges - Review These
- `office-hours (gstack, reference_only)` → `rvlab-interview SKILL`  [AMBIGUOUS]
  skills/dependencies.yaml · relation: conceptually_related_to
- `brainstorming (superpowers, reference_only)` → `rvlab-interview SKILL`  [AMBIGUOUS]
  skills/dependencies.yaml · relation: conceptually_related_to

## Knowledge Gaps
- **25 isolated node(s):** `name`, `private`, `version`, `description`, `node` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 137 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `office-hours (gstack, reference_only)` and `rvlab-interview SKILL`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `rvlab-interview SKILL` connect `Interview Method` to `Markdown Parsing and Build Tests`, `External Figures and Polishing`, `Vendored External Skills`, `Agent Guide and Approval Flow`?**
  _High betweenness centrality (0.291) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `StateError` (e.g. with `AnimationTests` and `BuildTests`) actually correct?**
  _`StateError` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _25 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `PPTX Build and Render QA` be split into smaller, more focused modules?**
  _Cohesion score 0.0691333982473223 - nodes in this community are weakly interconnected._
- **What is the exact relationship between `brainstorming (superpowers, reference_only)` and `rvlab-interview SKILL`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `StateError` connect `PPTX Build and Render QA` to `Markdown Parsing and Build Tests`, `Animation and Math Build Tests`, `Stage Approval State`, `Paper Extraction`, `Graphify Snapshot Check`, `Preview and Publish`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._