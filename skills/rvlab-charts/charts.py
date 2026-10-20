"""꾸밈 차트 레시피(멀티 프리셋 및 RVLAB 호환). 복사해 DATA만 고치거나 모듈로 import한다.

uv run python skills/rvlab-charts/charts.py demo OUT_DIR   # 합성 예시 전부 생성
각 함수는 PNG(300dpi)+SVG를 `out` 경로(확장자 제외)에 저장한다. 색은 선택된 프리셋(`set_preset(...)`) 또는 DESIGN.md 팔레트와 그 옅은 단계만 쓴다.
상자 안 라벨이 18pt로 들어가지 않으면 ValueError를 낸다(빌드의 넘침 검사는 그림 내부를 보지 못한다).
"""
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# 설치된 폰트만 리스트로 넘겨야 findfont 경고 없이 글자별 대체가 된다(한글은 Malgun Gothic → Noto Sans CJK KR).
_installed = {f.name for f in font_manager.fontManager.ttflist}
FONTS = [f for f in ("Arial", "Malgun Gothic", "Liberation Sans", "Noto Sans CJK KR") if f in _installed]
plt.rcParams.update({"font.family": FONTS, "font.size": 18})


def _tint(hex_color, factor=0.86):
    s = hex_color.lstrip("#")
    r, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    tr = round(r + (255 - r) * factor)
    tg = round(g + (255 - g) * factor)
    tb = round(b + (255 - b) * factor)
    return f"#{tr:02X}{tg:02X}{tb:02X}"


def set_preset(preset="rvlab"):
    """Load palette colors from a preset (e.g. rvlab, modern-16x9, academic-16x9, executive-16x9, minimal-4x3)."""
    global BLUE, BAND, SKY, TINT, GRAY, INK, SHADES
    from rvppt.template import semantic_palette
    pal = semantic_palette(preset)
    BLUE, BAND, SKY = pal["accent"], pal["band"], pal["secondary"]
    TINT, GRAY, INK = pal["tint"], pal["neutral"], pal["ink"]
    SHADES = [BAND, BLUE, SKY, _tint(SKY, 0.4), GRAY]
    return {"preset": preset, "palette": pal}


set_preset()


def _fit(text, w, h, size):
    """폭 w·높이 h(인치) 안에 들어가게 공백에서 줄을 나눈다. 글자 폭은 한글 1em·그 밖 0.6em으로 어림한다."""
    em = size / 72
    width = lambda t: sum(em if ord(c) > 0x2E80 else 0.6 * em for c in t)
    lines = []
    for word in text.split():
        cand = f"{lines[-1]} {word}" if lines else word
        if lines and width(cand) <= w:
            lines[-1] = cand
        else:
            lines.append(word)
    if any(width(l) > w for l in lines) or len(lines) * em * 1.3 > h:
        raise ValueError(f"라벨이 {w:.1f}×{h:.1f}in 상자에 {size}pt로 들어가지 않는다: {text!r}. 라벨을 줄인다.")
    return "\n".join(lines)


def _save(fig, out):
    for ext in ("png", "svg"):
        fig.savefig(f"{out}.{ext}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    return fig, ax


def _box(ax, x, y, w, h, text, fc=None, tc="white", size=18, bold=False):
    fc = BLUE if fc is None else fc
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc=fc, ec="none"))
    ax.text(x + w / 2, y + h / 2, _fit(text, w - .4, h - .1, size) if text else "", ha="center", va="center",
            color=tc, fontsize=size, fontweight="bold" if bold else "normal")


def _arrow(ax, p, q, color=None, rad=0.0):
    color = INK if color is None else color
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=18, lw=2, color=color,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))


def donut(out, parts, center=None, hole=0.55):
    """parts: [(라벨, 값)]. 3~5조각. 값 단위는 center나 캡션에 밝힌다. 범례 대신 조각 옆 직접 라벨."""
    fig, ax = plt.subplots(figsize=(7, 5.5))
    vals = [v for _, v in parts]
    total = sum(vals)
    wedges, _ = ax.pie(vals, colors=SHADES[:len(vals)], startangle=90, counterclock=False,
                       wedgeprops=dict(width=1 - hole, edgecolor="white", linewidth=3))
    for w, (name, v) in zip(wedges, parts):
        a = math.radians((w.theta1 + w.theta2) / 2)
        ax.annotate(f"{name}\n{v / total:.0%}", (math.cos(a) * .95, math.sin(a) * .95),
                    (math.cos(a) * 1.35, math.sin(a) * 1.35), ha="center", va="center", fontsize=18,
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=1.2))
    if center:
        ax.text(0, 0, center, ha="center", va="center", fontsize=22, fontweight="bold", color=BAND)
    ax.set_aspect("equal")
    _save(fig, out)


def flow(out, steps, loop_back=False, highlight=None):
    """steps: [라벨] 3~5개 가로 흐름. highlight: 강조할 index(BAND). loop_back: 마지막→처음 되돌림 화살표."""
    n = len(steps); bw, gap, bh = 2.0, 0.7, 1.2
    w = n * bw + (n - 1) * gap
    fig, ax = _canvas(w, 3.0 if loop_back else 1.4)
    y = 0.1 if not loop_back else 1.5
    for i, s in enumerate(steps):
        x = i * (bw + gap)
        _box(ax, x, y, bw, bh, s, fc=BAND if i == highlight else BLUE)
        if i < n - 1:
            _arrow(ax, (x + bw + .08, y + bh / 2), (x + bw + gap - .08, y + bh / 2))
    if loop_back:
        _arrow(ax, (w - bw / 2, y), (bw / 2, y), color=SKY, rad=-0.35)
    _save(fig, out)


def timeline(out, events):
    """events: [(시점, 제목)] 3~6개. 시점은 짧게(2025.03, Q2 등). 간격은 균등(비례 시간축이 아님)."""
    n = len(events); w = max(8, n * 2.2)
    fig, ax = _canvas(w, 3.2)
    ax.plot([0.3, w - 0.3], [1.6, 1.6], color=GRAY, lw=3, solid_capstyle="round")
    for i, (when, title) in enumerate(events):
        x = 0.3 + (w - .6) * (i + .5) / n
        up = i % 2 == 0
        ax.plot([x, x], [1.6, 2.1 if up else 1.1], color=GRAY, lw=1.5)
        ax.scatter([x], [1.6], s=260, color=BLUE, zorder=3, edgecolor="white", linewidth=3)
        ax.text(x, 2.2 if up else 1.0, when, ha="center", va="bottom" if up else "top",
                fontsize=18, fontweight="bold", color=BAND)
        ax.text(x, 2.65 if up else 0.55, title, ha="center", va="bottom" if up else "top", fontsize=18)
    _save(fig, out)


def matrix2x2(out, x_label, y_label, cells, points=()):
    """cells: [좌상, 우상, 좌하, 우하] 사분면 이름. points: [(라벨, x, y)] 0~1 위치(개념 배치임을 캡션에 밝힌다)."""
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    for (x, y), name, fc in zip([(0, .5), (.5, .5), (0, 0), (.5, 0)], cells, [TINT, _tint(BLUE, 0.72), "white", TINT]):
        ax.add_patch(plt.Rectangle((x, y), .5, .5, fc=fc, ec="white", lw=3))
        ax.text(x + .25, y + .45, name, ha="center", va="top", fontsize=18, color=BAND, fontweight="bold")
    for name, px, py in points:
        ax.scatter([px], [py], s=220, color=BLUE, zorder=3)
        ax.text(px + .03, py, name, va="center", fontsize=18)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.annotate("", (1.02, 0), (0, 0), arrowprops=dict(arrowstyle="-|>", lw=2), annotation_clip=False)
    ax.annotate("", (0, 1.02), (0, 0), arrowprops=dict(arrowstyle="-|>", lw=2), annotation_clip=False)
    ax.set_xlabel(x_label, fontsize=18, loc="right"); ax.set_ylabel(y_label, fontsize=18, loc="top", labelpad=14)
    _save(fig, out)


def funnel(out, stages):
    """stages: [(라벨, 값)] 큰 값부터 3~5단. 막대 폭이 값에 비례한다(실제 값 필요). 라벨은 왼쪽, 값은 막대 오른쪽."""
    fig, ax = _canvas(10, len(stages) * 1.05)
    top = max(v for _, v in stages)
    for i, (name, v) in enumerate(stages):
        bw = 6.0 * v / top; y = (len(stages) - 1 - i) * 1.05
        _box(ax, 2.6 + (6.0 - bw) / 2, y, bw, .85, "", fc=SHADES[i % 5])
        ax.text(2.4, y + .42, name, ha="right", va="center", fontsize=18)
        ax.text(2.6 + (6.0 + bw) / 2 + .15, y + .42, f"{v:,}", ha="left", va="center", fontsize=18, fontweight="bold", color=BAND)
    _save(fig, out)


def cards(out, items, title_size=20):
    """items: [(제목, 설명)] 2~4개 나란한 비교/요약 카드. 설명은 18pt로 두 줄까지 들어간다."""
    n = len(items); cw, g = 3.0, 0.3
    fig, ax = _canvas(n * cw + (n - 1) * g, 2.6)
    for i, (t, d) in enumerate(items):
        x = i * (cw + g)
        ax.add_patch(plt.Rectangle((x, 0), cw, 2.6, fc=TINT, ec="none"))
        _box(ax, x, 1.8, cw, .8, t, fc=BLUE, size=title_size, bold=True)
        ax.text(x + cw / 2, .85, _fit(d, cw - .5, 1.5, 18), ha="center", va="center", fontsize=18)
    _save(fig, out)


def demo(d, preset="rvlab"):
    set_preset(preset)
    d = Path(d); d.mkdir(parents=True, exist_ok=True)
    donut(d / "donut", [("A 모듈", 45), ("B 모듈", 30), ("C 모듈", 15), ("기타", 10)], center="합성 예시")
    flow(d / "flow", ["입력", "인코더", "정책", "행동"], highlight=2)
    flow(d / "flow-loop", ["관측", "추론", "행동"], loop_back=True)
    timeline(d / "timeline", [("1단계", "문제 정의"), ("2단계", "데이터 수집"), ("3단계", "학습"), ("4단계", "평가")])
    matrix2x2(d / "matrix", "구현 난이도", "기대 효과", ["우선 검토", "도전", "빠른 적용", "보류"],
              [("방법 A", .25, .75), ("방법 B", .7, .8), ("방법 C", .3, .25)])
    funnel(d / "funnel", [("후보", 1000), ("1차 통과", 400), ("2차 통과", 120), ("최종", 30)])
    cards(d / "cards", [("방법 A", "빠르지만 정확도 낮음"), ("방법 B", "느리지만 안정적"), ("제안", "둘의 장점 결합")])


if __name__ == "__main__":
    if len(sys.argv) in (3, 4) and sys.argv[1] == "demo":
        demo(sys.argv[2], preset=sys.argv[3] if len(sys.argv) == 4 else "rvlab")
    else:
        sys.exit(__doc__)
