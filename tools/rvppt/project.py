"""Create an Overleaf-style presentation project: slides.md, figures/, sources/, plan/."""

from datetime import date
import re

import yaml

from .state import StateError
from .template import ROOT

SKELETON = """
<!-- # 섹션 | 부제 → 섹션 슬라이드와 목차의 Chapter
     ## 토픽 → 상단 바 제목(한글 10자·영문 20자 이내 한 줄), 목차의 항목
     ### 핵심 문장 → 슬라이드 한 장. 본문 첫 줄 ▪ 24pt
     표지·목차·감사합니다는 빌드가 만든다. 문법: docs/rendering.md -->

# 연구 배경 | Background

## 주제 이름

### 이 슬라이드에서 전할 한 문장을 쓴다

- 자료에서 확인한 근거
  - 조건이나 수치

![그림 캡션](figures/example.png "연구자에게 요청할 그림: 무엇을 어떤 축·비교로, 어느 자료로")

::: notes
발표할 때 말할 내용과 출처의 전체 서지를 적는다.
:::

# 결과 | Results

## 실험 결과

### 결과가 말해 주는 한 문장을 쓴다

- 비교 기준과 조건
"""


def load_profile(path=ROOT / "profile.yaml"):
    if not path.is_file():
        raise StateError("profile.yaml is missing: copy profile.example.yaml to profile.yaml and fill in your details")
    profile = yaml.safe_load(path.read_text(encoding="utf-8"))
    affiliation = profile.get("affiliation") if isinstance(profile, dict) else None
    if not all(isinstance(profile.get(k), str) and profile[k].strip() for k in ("name", "name_en")) or not isinstance(affiliation, list) or not 1 <= len(affiliation) <= 2:
        raise StateError("profile.yaml needs name, name_en and one or two affiliation lines")
    return profile


def new_project(slug, title, subtitle="", day=None, language="ko", profile_path=ROOT / "profile.yaml", tasks=ROOT / "tasks"):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,40}", slug):
        raise StateError("slug uses lowercase letters, digits and hyphens")
    try:
        day = date.fromisoformat(day).isoformat() if day else date.today().isoformat()
    except ValueError as error:
        raise StateError("--date must be YYYY-MM-DD") from error
    profile = load_profile(profile_path)
    task = tasks / f"{day[2:4]}{day[5:7]}{day[8:10]}-{slug}"
    if task.exists():
        raise StateError(f"Task already exists: {task.name}")
    deck = {"title": title, "subtitle": subtitle, "date": day,
            "presenter": f"{profile['name']} ({profile['name_en']})", "affiliation": profile["affiliation"]}
    metadata = {"schema_version": 1, "task_id": task.name, "stage": 4, "status": "draft", "approval_hash": None,
                "upstream_hashes": {}, "deck": deck, "review": {"language": language}}
    for folder in ("figures", "sources", "plan"):
        (task / folder).mkdir(parents=True)
    (task / "slides.md").write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + "---\n" + SKELETON, encoding="utf-8", newline="\n")
    return {"task": str(task), "slides": str(task / "slides.md"), "next": "Put papers, data and draft PPTs in sources/, figures in figures/, then ask the agent to start the rvlab-interview skill or edit slides.md and run rvppt build."}
