# Graph Report - ppt-gener  (2026-10-25)

## Corpus Check
- Corpus is ~48,455 words - fits in a single context window. You may not need a graph.

## Summary
- 849 nodes · 2018 edges · 48 communities (36 shown, 12 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 136 edges (avg confidence: 0.87)
- Token cost: 436,047 tokens spent by the two semantic subagents (combined input and output, as reported by the harness); AST extraction and the merge run locally. No external LLM API calls.

## Graph Freshness
- Built from commit: `d9d7a7a0`
- Run `uv run pptgen graph-check` to verify recorded input and output hashes, freshness and source exclusions.
- Rebuild with the Graphify skill after source changes, then record with `uv run pptgen graph-check --record`. Semantic extraction token usage depends on the active session or configured backend.

## Community Hubs (Navigation)
- Slide Building and Markdown
- Stage Approval Tests
- Anatomy Bridge and Palettes
- Test Fixtures and Shared Imports
- Node Packages and Renderers
- Chart Recipe Library
- Approval State and Hashing
- Template Catalog and RVLAB Design
- Slide Rule Tests
- Workflow and Revision Procedure
- Template Package Tests
- Pinned External Skills
- Animation Skill and Storyboard
- Visual Planning and External Figures
- Graph Check and Diagram Rendering
- Template Layout Builders
- Document Schemas and Profile
- Overview and Toolchain
- Doctor and Binary Detection
- Layout and Overflow Tests
- Project Skills and Roles
- Template Registry and Tokens
- Skill Entrypoint Tests
- Shared Harness Rules
- Source Format and Rendering
- Setup and Environment Guide
- Talk Types and Plan Documents
- Animation Tests
- Interview Question Guide
- PPTX Library Imports
- Plan Contracts and Polish Check
- Charts Skill and Preset Palette
- Local Diagram Rendering
- CLI Entry and Argument Parsing
- Korean Polish Procedure
- Modern Minimal Design
- Neo City Design
- Retro Editorial Design
- General Harness Tests
- Paper Extraction Tests
- Document Extraction Tools
- Python Package Dependencies
- Skill Integrity Tests
- CLI Integration Tests
- Diagram Tests

## God Nodes (most connected - your core abstractions)
1. `StateError` - 56 edges
2. `BuildTests` - 51 edges
3. `StateTests` - 43 edges
4. `Presentation production workflow and approval rules` - 34 edges
5. `status()` - 33 edges
6. `approve()` - 33 edges
7. ``slides.md` authoring syntax and render QA` - 29 edges
8. `Template folder structure and DESIGN.md contract` - 28 edges
9. `resolve_fonts()` - 27 edges
10. `assemble()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `TOC skeleton from sections and topics` --semantically_similar_to--> `RVLAB 4:3 lab template design specification`  [INFERRED] [semantically similar]
  skills/ppt-maker/references/talk-types.md → templates/rvlab/DESIGN.md
- `Discovery entrypoints for agents` --semantically_similar_to--> `Common agent guidelines for PPT-Gener`  [INFERRED] [semantically similar]
  docs/skills.md → AGENTS.md
- `Template-specific style rules live in DESIGN.md` --semantically_similar_to--> `Common agent guidelines for PPT-Gener`  [INFERRED] [semantically similar]
  docs/skills.md → AGENTS.md
- `Hand-edited PPTX overwrite guard` --conceptually_related_to--> `Common agent guidelines for PPT-Gener`  [INFERRED]
  docs/rendering.md → AGENTS.md
- `License URL and preserved license file per skill` --shares_data_with--> `Project overview and quick start`  [INFERRED]
  skills/dependencies.yaml → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Code, preset, and agent responsibility split** — agents_code_enforced_limits, agents_preset_decided_form, agents_agent_judged_content [EXTRACTED 1.00]
- **Four pinned external skills** — skills_dependencies_im_not_ai, skills_dependencies_manimce_best_practices, skills_dependencies_scientific_visualization, skills_dependencies_anatomy [EXTRACTED 1.00]
- **Four-stage presentation approval pipeline** — docs_workflow_stage_1, docs_workflow_stage_2, docs_workflow_stage_3, docs_workflow_stage_4 [EXTRACTED 1.00]
- **ppt skill suite from planning to visuals** — skills_ppt_interview_skill_document, skills_ppt_maker_skill_document, skills_ppt_charts_skill_document, skills_ppt_animation_skill_document, skills_ppt_tutorial_skill_document [INFERRED 0.85]
- **Skills reading deck.preset DESIGN.md before work** — skills_ppt_animation_skill_design_read_first, skills_ppt_charts_skill_design_read_first, skills_ppt_maker_skill_design_read_first, skills_ppt_interview_skill_preset_recommendation, templates_readme_template_specific_rules_in_design_md [INFERRED 0.95]
- **Presets following the five-section DESIGN.md convention** — templates_readme_five_section_convention, templates_modern_minimal_design_character_tech_talk, templates_neo_city_design_character_dark_keynote, templates_retro_design_character_storytelling, templates_rvlab_design_character_lab_meeting [INFERRED 0.95]

## Communities (48 total, 12 thin omitted)

### Community 0 - "Slide Building and Markdown"
Cohesion: 0.06
Nodes (60): add_text(), assemble(), audit(), bold_cell(), _border(), box_of(), build(), column_widths() (+52 more)

### Community 1 - "Stage Approval Tests"
Cohesion: 0.11
Nodes (5): PlanTests, StateTests, write_plan(), approve(), status()

### Community 2 - "Anatomy Bridge and Palettes"
Cohesion: 0.08
Nodes (14): ChartTests, PaletteTests, build_anatomy_figure(), _channels(), _gif(), _localized(), _mix(), _resolve_vars() (+6 more)

### Community 4 - "Node Packages and Renderers"
Cohesion: 0.07
Nodes (25): dependencies, beautiful-mermaid, mathjax-full, @mermaid-js/mermaid-cli, @resvg/resvg-js, description, engines, node (+17 more)

### Community 5 - "Chart Recipe Library"
Cohesion: 0.14
Nodes (14): _arrow(), _box(), _canvas(), cards(), demo(), donut(), _fit(), flow() (+6 more)

### Community 6 - "Approval State and Hashing"
Cohesion: 0.13
Nodes (15): _digest(), Document, _inspect(), _mapping(), _names(), _outline(), review_issues(), review_warnings() (+7 more)

### Community 7 - "Template Catalog and RVLAB Design"
Cohesion: 0.10
Nodes (18): Slide kinds: statement, number, quote, Build, preview, audit inspection loop, Four-step new template procedure, DESIGN.md YAML token keys, Template folder structure and DESIGN.md contract, templates/examples/ local reference talks, Five-section character and conventions, templates/<id>/ folder layout (+10 more)

### Community 9 - "Workflow and Revision Procedure"
Cohesion: 0.13
Nodes (20): Six-step agent revision procedure, Handling broad requests like 'make it cleaner', `plan/contracts.md` snapshot via `pptgen plan`, Presentation revision procedure, Change type to re-review stage table, Natural-language revision requests by page, topic, or ID, `plan/` documents and their writers, Revision IDs (R001) in `plan/revisions.md` (+12 more)

### Community 10 - "Template Package Tests"
Cohesion: 0.15
Nodes (7): TemplateTests, template(), build_reference(), extract_manifest(), parse(), sha256(), validate_package()

### Community 11 - "Pinned External Skills"
Cohesion: 0.15
Nodes (19): Skill discovery links to `skills/`, `pptgen anatomy` run in editorial workdir, Discovery entrypoints for agents, Skill composition and external skills guide, External skills table with source and scope, Pinned external skills with preserved licenses, Removed reference-only and document-format skills, Retired `rvlab-*` skills and compatibility links (+11 more)

### Community 12 - "Animation Skill and Storyboard"
Cohesion: 0.12
Nodes (16): Optional `visual` extra: Manim, Matplotlib, SciencePlots, default_prompt for preset-matched animation, display_name: educational animation, OpenAI agent interface metadata for ppt-animation, short_description for GIF and static alternatives, Beats: state, change, explanation, hold, Iterative optimization calculation record, Animation storyboard pre-production checklist (+8 more)

### Community 13 - "Visual Planning and External Figures"
Cohesion: 0.12
Nodes (14): Pinned PyMuPDF4LLM 0.2.9 paper extraction, Guide to sourcing external photos and paper figures, pptgen extract-paper PDF to Markdown, Caption-driven figure selection procedure, Source line, notes, and slot checks, figures/visual-sources.yaml provenance record, Web photo sourcing from official pages, Visual design and production routing guide (+6 more)

### Community 14 - "Graph Check and Diagram Rendering"
Cohesion: 0.18
Nodes (9): main(), render(), validate_source(), GraphCheckTests, _candidates(), graph_check(), _graph_sources(), ignored() (+1 more)

### Community 15 - "Template Layout Builders"
Cohesion: 0.21
Nodes (14): apply_layout_style(), build_preset_reference(), content_layout(), _decor(), placeholder(), _run_style(), set_background(), set_box() (+6 more)

### Community 16 - "Document Schemas and Profile"
Cohesion: 0.20
Nodes (16): Common frontmatter fields for stage documents, Task document schema v1, Effective status values: missing, draft, approved, stale, invalid, `content_hash` versus `review_hash`, Input hashing of `sources/` and `figures/`, `issues` block approval, `warnings` only advise, Stage 1 `plan/interview.md` review fields, Stage 2 `plan/brief.md` message candidates (+8 more)

### Community 17 - "Overview and Toolchain"
Cohesion: 0.15
Nodes (14): Pinned Python and Node dependencies, Toolchain choices and rendering constraints, Markdown to Pandoc AST to PPTX to LibreOffice QA, RVLAB master, logo, and theme preservation, 16:9 themes styled by DESIGN.md `style` blocks, `pptgen anatomy` isometric diagram build, `pptgen audit` 4x close-up critic loop, Up-front sizing with `--budget` (+6 more)

### Community 18 - "Doctor and Binary Detection"
Cohesion: 0.17
Nodes (6): doctor(), browser(), libreoffice(), chrome_binary(), libreoffice_binary(), render_pdf()

### Community 20 - "Project Skills and Roles"
Cohesion: 0.25
Nodes (11): Task-to-skill starting point table, Project skills and their roles table, Five project skills and `pptgen` command, Per-stage questions in collaborative mode, ppt-interview skill for Stage 1~3 planning, Handoff to ppt-tutorial for follow-along, ppt-maker skill for Stage 4 writing and building, Resume via status and PROGRESS.md (+3 more)

### Community 21 - "Template Registry and Tokens"
Cohesion: 0.14
Nodes (9): fonts(), preset_fonts(), design_path(), _fill(), load_tokens(), read_design(), register_template(), rescale() (+1 more)

### Community 22 - "Skill Entrypoint Tests"
Cohesion: 0.21
Nodes (3): SkillEntrypointTests, entrypoints(), skill_entrypoints()

### Community 23 - "Shared Harness Rules"
Cohesion: 0.19
Nodes (10): Agent-judged wording, structure, and emphasis, Code-enforced limits on unrenderable input and overflow, `templates/<id>/DESIGN.md` style contract, Common agent guidelines for PPT-Gener, Approval only via `pptgen approve` after user consent, `graphify-out/` as non-authoritative structure reference, Preset-decided layout, fonts, and base colors, Protected originals: `sources/`, RVLAB template, external skills (+2 more)

### Community 24 - "Source Format and Rendering"
Cohesion: 0.20
Nodes (12): Build pipeline with LibreOffice render QA, Two-column and figure grid layouts, `slides.md` authoring syntax and render QA, Missing-figure request placeholders, GIF with representative PNG pair, Section, topic, key-sentence heading hierarchy, `lint`, `build`, `preview` commands, LaTeX math as OMML plus image fallback (+4 more)

### Community 25 - "Setup and Environment Guide"
Cohesion: 0.19
Nodes (11): Installation and environment check guide, Initial install with `uv sync` and `npm ci`, Local diagrams via `beautiful-mermaid` and resvg, Mermaid Chrome or Chromium requirement, OS-specific tool installation table, `pptgen doctor` read-only environment check, Preset-specific font requirements, Personal `profile.yaml` copied from example (+3 more)

### Community 26 - "Talk Types and Plan Documents"
Cohesion: 0.14
Nodes (13): brief.md message and storyline candidates, outline.md per-slide plan fields, plan/ documents: interview, brief, outline, PROGRESS, Truth Model in plan/PROGRESS.md, Talk-type section structures and slide quality, Figure request flow to researchers, Good slide conditions checklist, Post-build verification checklist (+5 more)

### Community 28 - "Interview Question Guide"
Cohesion: 0.17
Nodes (10): Question modes: co-create, essentials, instant draft, Answer-driven follow-up branching, Audience, purpose, material, success, constraints, Interview question guide for unconfirmed intent, Bundles of three to five questions, Handling unsupported claims and hidden premises, Budget levels: quick, standard, thorough, First question bundle: mode, preset, budget (+2 more)

### Community 30 - "Plan Contracts and Polish Check"
Cohesion: 0.24
Nodes (5): _cell(), render_contracts(), difference(), polish_check(), read_document()

### Community 31 - "Charts Skill and Preset Palette"
Cohesion: 0.20
Nodes (8): Mermaid flowcharts with preset styling, Preset palette with non-color encoding, charts.py decorative chart recipes, ppt-charts skill for diagrams and decorative charts, figures/make_charts.py reproducible script, Preset auto-detected from task deck.preset, semantic_palette color role keys, Statement, number, quote slide kinds for rhythm

### Community 32 - "Local Diagram Rendering"
Cohesion: 0.18
Nodes (7): beautiful-mermaid and ELK local layout, Local automatic diagram rendering guide, In-slide mermaid blocks render separately, Four-step diagram production workflow, Relation to diagram composition mapping, Local Mermaid rendering via diagrams.py, Equations in LaTeX, 16pt code, Mermaid

### Community 33 - "CLI Entry and Argument Parsing"
Cohesion: 0.38
Nodes (4): main(), _task_path(), list_presets(), main()

### Community 34 - "Korean Polish Procedure"
Cohesion: 0.22
Nodes (6): Korean polish before approval request, before.md snapshot of slides.md, Korean slides.md polishing procedure, humanize-korean run in .build/editorial, pptgen polish-check preservation gate, Pre-approval lint, polish, warnings

### Community 35 - "Modern Minimal Design"
Cohesion: 0.22
Nodes (9): Avoids: paragraphs, many accents, decoration, Character: conference and tech-talk audience, Modern Minimal 16:9 design document, Figure impression: gray baseline, blue protagonist, Fits: one big message per slide, Lint limits and font sizes, Electric blue 2B59FF single-accent palette, Post-build checks: whitespace, single blue, gray text (+1 more)

### Community 36 - "Neo City Design"
Cohesion: 0.24
Nodes (8): Character: dark-venue tech demo keynote, Neo City 16:9 dark neon design document, Dark-canvas figures with thin neon strokes, Fits: demos with fixed neon color meanings, Narrow heavy heading fonts, Neon cyan, magenta, violet on 0B1020, Post-build checks: white remnants, contrast, fonts, HUD grid lines and corner brackets

### Community 37 - "Retro Editorial Design"
Cohesion: 0.24
Nodes (9): Avoids: neon, dense tables, sans-serif titles, Character: storytelling, history, lecture talks, Retro Editorial 16:9 design document, Paper-style figures: thick lines, cream background, Fits: narrative, timelines, case cards, quotes, Cream paper, terracotta, teal, mustard palette, Post-build checks: serif legibility and contrast, Serif fonts for Latin and Korean (+1 more)

### Community 40 - "Document Extraction Tools"
Cohesion: 0.46
Nodes (7): Input material reading tools guide, `pptgen extract-paper` PDF to Markdown, Formula-in-image OCR candidates, Microsoft MarkItDown draft text extraction, Pandoc (pypandoc-binary) document conversion, PDF page rendering and crop fallback, Material-type to tool mapping table

### Community 41 - "Python Package Dependencies"
Cohesion: 0.25
Nodes (8): lxml, Pillow, ppt-gener, PyMuPDF, pymupdf4llm, pypandoc-binary, python-pptx, PyYAML

### Community 42 - "Skill Integrity Tests"
Cohesion: 0.29
Nodes (4): SkillIntegrityTests, skills(), link_stand_in(), skill_integrity()

## Ambiguous Edges - Review These
- `Local automatic diagram rendering guide` → `Equations in LaTeX, 16pt code, Mermaid`  [AMBIGUOUS]
  templates/rvlab/DESIGN.md · relation: conceptually_related_to

## Knowledge Gaps
- **70 isolated node(s):** `Claude agent entry point`, `Gemini agent entry point`, `name`, `private`, `version` (+65 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 244 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Local automatic diagram rendering guide` and `Equations in LaTeX, 16pt code, Mermaid`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Skill composition and external skills guide` connect `Pinned External Skills` to `Setup and Environment Guide`, `Anatomy Bridge and Palettes`, `Project Skills and Roles`, `Node Packages and Renderers`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `StateError` (e.g. with `AnimationTests` and `BuildTests`) actually correct?**
  _`StateError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Claude agent entry point`, `Gemini agent entry point`, `name` to the rest of the system?**
  _70 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Slide Building and Markdown` be split into smaller, more focused modules?**
  _Cohesion score 0.05666293393057111 - nodes in this community are weakly interconnected._
- **Why does `ppt-charts skill for diagrams and decorative charts` connect `Charts Skill and Preset Palette` to `Local Diagram Rendering`, `Modern Minimal Design`, `Neo City Design`, `Chart Recipe Library`, `Retro Editorial Design`, `Visual Planning and External Figures`, `Graph Check and Diagram Rendering`, `Project Skills and Roles`, `Setup and Environment Guide`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Presentation production workflow and approval rules` (e.g. with `Microsoft MarkItDown draft text extraction` and ``plan/contracts.md` snapshot via `pptgen plan``) actually correct?**
  _`Presentation production workflow and approval rules` has 7 INFERRED edges - model-reasoned connections that need verification._
## Extraction audit

Incremental update on 2026-10-25 from commit `d9d7a7a0` plus uncommitted working-tree changes. Re-extracted all 36 code files by AST (deterministic; untouched files reproduced the earlier graph exactly) and 30 changed project documents with two local-session semantic agents; 2 unchanged documents kept their earlier extraction and 13 deleted files were pruned. No external LLM API was called.

The JSON preserves 2091 original relationships across 849 nodes. Clustering and the HTML view use a simple undirected projection with 2018 edges; reciprocal and parallel relationships therefore share one projected edge. The JSON retains the original directions and relation types.

Graphify diagnostics (raw extraction): 307 dangling-endpoint edges, 0 missing-endpoint edges, 7 self-loops, 69 same-endpoint projection collisions. Structural extraction can reference imported external symbols, which Graphify represents with external stubs when applicable.

Corpus exclusions follow `.graphifyignore`; actual tasks, templates, profile.yaml, vendored skill originals, discovery symlinks, and generated output are excluded. This run additionally left out `skills/rvlab-charts/charts.py` (symlink alias of skills/ppt-charts/charts.py); `skills/rvlab-charts/diagrams.py` (symlink alias of skills/ppt-charts/diagrams.py); `skills/system/run-workflow/SKILL.md` (untracked system-injected skill, not project content). `docs/architecture.md` remains excluded by the existing policy. No task data was read or published.
