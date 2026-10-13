"""Rebuild data plots, paper crops and earlier conceptual diagrams.
AI illustrations are saved assets; see illustration-prompts.md.
Run: uv run python tasks/261011-example-il-progress/figures/make_charts.py
"""
import csv
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pymupdf
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
TASK = HERE.parent
sys.path.insert(0, str(TASK.parents[1] / 'skills/rvlab-charts'))
import charts


def rows(name):
    with (TASK / 'sources' / name).open(encoding='utf-8') as f:
        return list(csv.DictReader(line for line in f if not line.startswith('#')))


def wilson(successes, trials):
    assert trials > 0 and 0 <= successes <= trials
    z = 1.959963984540054
    p = successes / trials
    divisor = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / divisor
    half = z * math.sqrt(p * (1-p) / trials + z*z / (4*trials*trials)) / divisor
    return max(0, center-half), min(1, center+half)


def save(fig, name):
    for ext in ('png', 'svg'):
        fig.savefig(HERE / f'{name}.{ext}', dpi=300, facecolor='white')
    plt.close(fig)


# Teaching diagrams encode relationships only; no measured trajectories or values.
charts.flow(HERE / 'bc-pipeline', ['시연 수집', '관측·행동 쌍', '정책 학습', '로봇 실행'], highlight=2)
charts.flow(HERE / 'distribution-shift', ['작은 행동 오차', '달라진 관측', '낯선 입력', '추가 오차'], loop_back=True)
charts.flow(HERE / 'dagger-loop', ['정책 실행', '방문 상태 수집', '전문가 행동', '누적·재학습'], loop_back=True, highlight=2)
charts.timeline(HERE / 'next-experiment', [('1단계', '파지 시연 보강'), ('2단계', '앙상블 비교'), ('3단계', '평가 확대')])

# Redraw ACT Fig. 5 as a teaching grid, k=4 purely for legibility.
fig, ax = plt.subplots(figsize=(9.3, 3.7))
ax.set(xlim=(-1.6, 7.4), ylim=(-1.3, 4.8)); ax.axis('off')
for t in range(7):
    ax.text(t+.4, 4.3, f't={t}', ha='center', fontsize=18)
for start in range(4):
    y = 3-start
    ax.text(-.2, y+.35, f'관측 {start}', ha='right', va='center', fontsize=18)
    for t in range(start, start+4):
        current = t == 3
        ax.add_patch(Rectangle((t, y), .8, .7, facecolor=charts.BAND if current else charts.TINT,
                               edgecolor=charts.BAND, linewidth=1.4))
        ax.text(t+.4, y+.35, 'a₃' if current else 'a', ha='center', va='center',
                fontsize=18, color='white' if current else charts.BAND)
ax.annotate('같은 t=3의 네 예측 → 가중 평균 → 실행', xy=(3.4, .0), xytext=(3.4, -.9),
            ha='center', fontsize=18, arrowprops={'arrowstyle':'->','color':charts.BAND})
fig.subplots_adjust(left=.02, right=.98, top=.96, bottom=.04)
save(fig, 'temporal-ensemble')

# Preserve original paper colors; crop artwork only, caption recorded in provenance.
with pymupdf.open(HERE / 'external/act-2023.pdf') as doc:
    doc[3].get_pixmap(dpi=300, clip=pymupdf.Rect(48, 50, 565, 180)).save(HERE / 'act-architecture.png')
    doc[0].get_pixmap(dpi=300, clip=pymupdf.Rect(48, 162, 256, 324)).save(HERE / 'aloha-teleoperation.png')

evaluation = rows('eval.csv')
failures = rows('failures.csv')
assert [int(r['trials']) for r in evaluation] == [40]*4
assert sum(int(r['count']) for r in failures) == 40 - int(evaluation[2]['successes'])
assert math.isclose(wilson(0,40)[1], 0.08762160119728664)
assert math.isclose(wilson(40,40)[0], 1-wilson(0,40)[1])
rates = [100*int(r['successes'])/int(r['trials']) for r in evaluation]
intervals = [wilson(int(r['successes']), int(r['trials'])) for r in evaluation]
with plt.rc_context({'font.family': charts.FONTS, 'font.size':18, 'axes.spines.top':False,
                     'axes.spines.right':False, 'axes.labelcolor':charts.INK}):
    fig, ax = plt.subplots(figsize=(9.3, 4.2), layout='constrained')
    ax.bar(range(4), rates, color=[charts.BLUE]*4, width=.58, edgecolor=charts.BAND)
    ax.errorbar(range(4), rates, yerr=([v-100*lo for v,(lo,hi) in zip(rates,intervals)],
                                     [100*hi-v for v,(lo,hi) in zip(rates,intervals)]),
                fmt='none', color=charts.INK, capsize=7, linewidth=1.7)
    for i,(r,(lo,hi)) in enumerate(zip(evaluation,intervals)):
        ax.text(i, 100*hi+3, f"{rates[i]:g}%\n{r['successes']}/{r['trials']}", ha='center', fontsize=18)
    ax.set(ylim=(0,105), yticks=[0,25,50,75,100], ylabel='성공률 (%)',
           xticks=range(4), xticklabels=[r['condition'] for r in evaluation])
    ax.set_title('합성 예제 · 95% Wilson 구간 · 조건별 40회', fontsize=18, pad=15)
    ax.grid(axis='y', alpha=.18); ax.set_axisbelow(True)
    save(fig, 'success-by-chunk')
    fig, ax = plt.subplots(figsize=(9.3, 3.4), layout='constrained')
    labels = [r['failure_type'] for r in failures][::-1]
    counts = [int(r['count']) for r in failures][::-1]
    ax.barh(labels, counts, color=charts.BLUE, edgecolor=charts.BAND, height=.58)
    for i,v in enumerate(counts):
        ax.text(v+.12, i, f'{v}회', va='center', fontsize=18)
    ax.set(xlim=(0,7.3), xticks=range(8), xlabel='실패 횟수 (합성 자료 · ACT-8 실패 11회)')
    ax.grid(axis='x', alpha=.18); ax.set_axisbelow(True)
    save(fig, 'failure-types')
print('chart fonts:', charts.FONTS)
print('Synthetic-data checks and Wilson boundary checks passed.')
