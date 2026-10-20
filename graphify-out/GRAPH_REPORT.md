# Graph Report - ppt-gener  (2026-10-20)

## Corpus Check
- Corpus is ~43,926 words - fits in a single context window. You may not need a graph.

## Summary
- 705 nodes · 1664 edges · 32 communities (24 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 36 edges (avg confidence: 0.88)
- Token cost: unmetered local-session semantic extraction; no external LLM API calls. Zero counters are placeholders, not measured token usage.

## Graph Freshness
- Built from commit: `f037d422`
- Run `uv run pptgen graph-check` to verify recorded input and output hashes, freshness and source exclusions.
- Rebuild with the Graphify skill after source changes, then record with `uv run pptgen graph-check --record`. Semantic extraction token usage depends on the active session or configured backend.

## Community Hubs (Navigation)
- Slide Building and Markdown
- Templates and Approval State
- Stage Approval Tests
- Figure Planning and Production
- CLI Planning and Environment
- Template Integrity and Papers
- Node Diagram Renderers
- Slide Content Lint Tests
- Chart Recipe Library
- Skill Entrypoint Integrity
- Shared Harness Rules
- Diagram and Graph Integrity
- Vendored Skill Setup
- Pinned External Skill Manifest
- Slide Layout and Typography
- Semantic Palette Tests
- Source Format and Rendering
- Revisions and Document Schemas
- Animation Truth and Storyboards
- Audience Interview and Storyline
- Animation and Math Tests
- Document Extraction and Toolchain
- Slide Authoring and Audit
- Semantic Chart Palette
- Content Approval Workflow
- Python Package Dependencies
- Animation Palette Contract
- Local Diagram Tests
- Animation Agent Interface

## God Nodes (most connected - your core abstractions)
1. `StateError` - 53 edges
2. `BuildTests` - 50 edges
3. `StateTests` - 42 edges
4. `approve()` - 32 edges
5. `status()` - 31 edges
6. `resolve_fonts()` - 24 edges
7. `sha256()` - 24 edges
8. `assemble()` - 23 edges
9. `load_tokens()` - 23 edges
10. `build()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `set_preset()` --calls--> `semantic_palette()`  [INFERRED]
  skills/rvlab-charts/charts.py → tools/rvppt/template.py
- `AnimationTests` --uses--> `StateError`  [INFERRED]
  tests/test_animation.py → tools/rvppt/state.py
- `BuildTests` --uses--> `StateError`  [INFERRED]
  tests/test_build.py → tools/rvppt/state.py
- `PaperTests` --uses--> `StateError`  [INFERRED]
  tests/test_papers.py → tools/rvppt/state.py
- `PlanTests` --uses--> `StateError`  [INFERRED]
  tests/test_plan.py → tools/rvppt/state.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Markdown and native presentation rendering pipeline** — agents_slides_source, docs_rendering_pandoc_ast, docs_toolchain_pipeline, docs_toolchain_libreoffice_qa [EXTRACTED 1.00]
- **Four-stage presentation content workflow** — docs_workflow_interview, docs_workflow_brief, docs_workflow_outline, docs_workflow_slides [EXTRACTED 1.00]
- **Shared semantic palette contract** — skills_ppt_charts_skill_rvppt_template_semantic_palette_preset_, skills_ppt_charts_skill_semantic_palette_keys_accent_band_secondary_tint_neutral_ink_section_accent_background, skills_ppt_charts_skill_hex_rgb_palette_values__rrggbb [EXTRACTED 1.00]
- **Stage 1 to 3 planning artifacts** — skills_ppt_interview_skill_stage_1_plan_interview_md, skills_ppt_interview_skill_stage_2_plan_brief_md, skills_ppt_interview_skill_stage_3_plan_outline_md [EXTRACTED 1.00]
- **4x crop critic loop** — skills_ppt_maker_skill_pptgen_audit___zoom_4, skills_ppt_maker_skill_critic_crops_sheet_png_and_critic_audit_json, skills_ppt_maker_skill_critic_loop_and_4x_crop_audit_log [EXTRACTED 1.00]

## Communities (32 total, 8 thin omitted)

### Community 0 - "Slide Building and Markdown"
Cohesion: 0.06
Nodes (59): build_anatomy_figure(), _resolved_svg_css(), standalone_svg(), add_text(), assemble(), audit(), box_of(), build() (+51 more)

### Community 1 - "Templates and Approval State"
Cohesion: 0.07
Nodes (22): make_task(), slides_body(), CliIntegrationTests, run_cli_smoke(), IgnoreTests, _cell(), render_contracts(), _digest() (+14 more)

### Community 2 - "Stage Approval Tests"
Cohesion: 0.11
Nodes (4): GeneralHarnessTests, StateTests, approve(), status()

### Community 3 - "Figure Planning and Production"
Cohesion: 0.05
Nodes (42): @resvg/resvg-js 300dpi PNG rendering, beautiful-mermaid SVG with ELK layout, Branch group feedback sequence and state diagrams, Local automatic diagrams, npm ci reproducible installation, package.json and package-lock.json dependency pinning, Chart recipes donut flow timeline matrix2x2 funnel cards, figures/make_charts.py reproducibility (+34 more)

### Community 4 - "CLI Planning and Environment"
Cohesion: 0.08
Nodes (16): PlanTests, main(), _task_path(), doctor(), browser(), fonts(), libreoffice(), template() (+8 more)

### Community 5 - "Template Integrity and Papers"
Cohesion: 0.10
Nodes (15): PaperTests, TemplateTests, extract_paper(), build_preset_reference(), build_reference(), content_layout(), extract_manifest(), parse() (+7 more)

### Community 6 - "Node Diagram Renderers"
Cohesion: 0.07
Nodes (25): dependencies, beautiful-mermaid, mathjax-full, @mermaid-js/mermaid-cli, @resvg/resvg-js, description, engines, node (+17 more)

### Community 8 - "Chart Recipe Library"
Cohesion: 0.15
Nodes (14): _arrow(), _box(), _canvas(), cards(), demo(), donut(), _fit(), flow() (+6 more)

### Community 9 - "Skill Entrypoint Integrity"
Cohesion: 0.14
Nodes (7): SkillEntrypointTests, SkillIntegrityTests, entrypoints(), skills(), link_stand_in(), skill_entrypoints(), skill_integrity()

### Community 10 - "Shared Harness Rules"
Cohesion: 0.15
Nodes (15): Shared agent instructions, pptgen audit: 4x crops, margins and contrast, PROGRESS.md: budget, truth model, state and 4x critic log, Claude agent entry point, anatomy_bridge creates task figure PNG and SVG from isolated workspace, Gemini agent entry point, Profile defaults: rvlab preset and standard budget, Public presenter profile example (+7 more)

### Community 11 - "Diagram and Graph Integrity"
Cohesion: 0.18
Nodes (9): main(), render(), validate_source(), GraphCheckTests, _candidates(), graph_check(), _graph_sources(), ignored() (+1 more)

### Community 12 - "Vendored Skill Setup"
Cohesion: 0.20
Nodes (13): skills/ source with agent discovery symlinks, doctor checks environment, fonts, renderer and vendored hashes read-only, Installation and environment checks, beautiful-mermaid/resvg local diagrams need no browser or visual extra, Python 3.11–3.14, uv, Node 22+, LibreOffice and fonts, Windows developer mode and core.symlinks for skill discovery, beautiful-mermaid 1.1.3 local chart renderer, Vendored skills and discovery policy (+5 more)

### Community 13 - "Pinned External Skill Manifest"
Cohesion: 0.26
Nodes (15): anatomy — available, brainstorming — reference_only, Pinned skill dependency manifest, im-not-ai — available, Pinned dependency provenance and per-file integrity records, manim-composer — reference_only, manimce-best-practices — available_requires_dependencies, minimax-docx — available_requires_dependencies (+7 more)

### Community 15 - "Semantic Palette Tests"
Cohesion: 0.14
Nodes (3): ChartTests, PaletteTests, semantic_palette()

### Community 16 - "Source Format and Rendering"
Cohesion: 0.18
Nodes (10): RVLAB design specification, Arial/Malgun Gothic with Liberation Sans/Noto Sans CJK KR fallback, 150 effective DPI minimum; generated PNG target 300 DPI, RVLAB 4:3: 10 × 7.5 inches, One-line topic and at most two-line headline, Markdown authoring and render QA, LaTeX source: editable OMML plus 300 DPI compatibility images, PPTX GIF with same-size representative PNG for PDF and previews (+2 more)

### Community 17 - "Revisions and Document Schemas"
Cohesion: 0.21
Nodes (11): contracts.md is a generated view, not a separate approval system, Presentation revision procedure, Revision impact selects earliest stage to review again, revisions.md: request IDs, changes, review scope and validation, Task document schema v1, Computed status: missing, draft, approved, stale or invalid, Stage frontmatter: schema, task ID, status, approval and upstream hashes, Stage input hashing covers sources and prior stages; Stage 4 adds figures (+3 more)

### Community 18 - "Animation Truth and Storyboards"
Cohesion: 0.16
Nodes (10): GIF and PNG dual artifact contract, Manim CE for transformations and equation geometry, manim-composer scene planning, manimce-best-practices implementation guidance, Matplotlib and Pillow for 2D graphs, rvlab-animation, scientific-visualization quantitative graph guidance, Storyboard beats state change explanation hold poster playback (+2 more)

### Community 19 - "Audience Interview and Storyline"
Cohesion: 0.15
Nodes (11): Explicit approval with review_hash, ppt-interview, Stage 1 plan/interview.md, Stage 1 to 3 presentation planning, Stage 2 plan/brief.md, Stage 3 plan/outline.md, Up-front sizing and budget quick standard thorough, Continue confirmed work while awaiting answers (+3 more)

### Community 21 - "Document Extraction and Toolchain"
Cohesion: 0.23
Nodes (11): Document processing tools and limitations, XLSX formula_check validates references without recalculating values, OCR formulas must be checked against source images, PyMuPDF4LLM: model-free extraction with AGPL/commercial dual licensing, Tool licenses are separate from skill licenses, Pandoc AST validates input and provides native text, tables and OMML, Build toolchain and limitations, extract-paper uses PyMuPDF4LLM 0.2.9 and existing PyMuPDF (+3 more)

### Community 22 - "Slide Authoring and Audit"
Cohesion: 0.20
Nodes (10): pptgen audit --zoom 4, anatomy PNG SVG and interactive HTML artifacts, critic-crops-sheet.png and critic-audit.json, ppt-maker, pptgen audit --zoom 4, pptgen lint and pptgen build, pptgen new --preset --budget, pptgen register-template and deck.preset (+2 more)

### Community 23 - "Semantic Chart Palette"
Cohesion: 0.26
Nodes (11): anatomy hardware and mechanism routing, beautiful-mermaid and ELK automatic layout, Chart recipes donut flow timeline matrix2x2 funnel cards, charts.set_preset, deck.preset, diagrams.py --preset, Hex RGB palette values #RRGGBB, Minimum diagram text size 18pt (+3 more)

### Community 24 - "Content Approval Workflow"
Cohesion: 0.31
Nodes (8): content_approved is separate from render QA, Stage 2 brief: selected message and storyline, Presentation production and approval workflow, Stage 1 interview: audience, purpose, evidence and constraints, Stage 3 outline: ordered claims, evidence, timing and figures, Korean polishing with AST preservation check, Stage 4: slides.md, Korean polish, content and production QA, Four-stage content approval workflow

### Community 25 - "Python Package Dependencies"
Cohesion: 0.25
Nodes (8): lxml, Pillow, ppt-gener, PyMuPDF, pymupdf4llm, pypandoc-binary, python-pptx, PyYAML

### Community 26 - "Animation Palette Contract"
Cohesion: 0.47
Nodes (4): Hex RGB palette values #RRGGBB, ppt-animation, rvppt.template.semantic_palette(preset), Semantic palette keys accent band secondary tint neutral ink section_accent background

## Knowledge Gaps
- **81 isolated node(s):** `name`, `private`, `version`, `description`, `node` (+76 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 224 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Vendored skills and discovery policy` connect `Vendored Skill Setup` to `Slide Building and Markdown`, `Shared Harness Rules`, `Document Extraction and Toolchain`, `Pinned External Skill Manifest`?**
  _High betweenness centrality (0.145) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `StateError` (e.g. with `AnimationTests` and `BuildTests`) actually correct?**
  _`StateError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _81 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Slide Building and Markdown` be split into smaller, more focused modules?**
  _Cohesion score 0.05605670103092784 - nodes in this community are weakly interconnected._
- **Why does `StateError` connect `Slide Building and Markdown` to `Templates and Approval State`, `Stage Approval Tests`, `CLI Planning and Environment`, `Template Integrity and Papers`, `Slide Content Lint Tests`, `Diagram and Graph Integrity`, `Animation and Math Tests`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Should `Templates and Approval State` be split into smaller, more focused modules?**
  _Cohesion score 0.06511761331038439 - nodes in this community are weakly interconnected._
- **Why does `Local automatic diagrams` connect `Figure Planning and Production` to `Diagram and Graph Integrity`, `Node Diagram Renderers`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
## Extraction audit

Rebuilt 36 code files by AST and 30 project documents with two local-session semantic agents. No external LLM API was called. All semantic source documents produced nodes; cache hits: 0.

The JSON preserves 1736 original relationships across 705 nodes. Clustering and the HTML view use a simple undirected projection with 1664 edges; reciprocal and parallel relationships therefore share one projected edge. The JSON retains the original directions and relation types.

Graphify diagnostics (raw extraction): 300 dangling-endpoint edges, 0 missing-endpoint edges, 5 self-loops, 68 same-endpoint projection collisions. Structural extraction can reference imported external symbols, which Graphify represents with external stubs when applicable.

Corpus exclusions follow `.graphifyignore`; actual tasks, templates, profile.yaml, vendored skill originals, discovery symlinks, and generated output are excluded. `.gemini/` is additionally excluded from detection to prevent discovery links from introducing duplicate vendor content. `docs/architecture.md` remains excluded by the existing policy. No task data was read or published.
