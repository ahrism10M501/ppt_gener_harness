"""Plot the synthetic example data with the RVLAB style.

uv run --with matplotlib python tasks/261011-example-il-progress/sources/plot_synthetic.py
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

TASK = Path(__file__).resolve().parents[1]
plt.style.use(TASK.parents[1] / "docs/design/rvlab.mplstyle")
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Malgun Gothic", "Liberation Sans", "Arial"]


def rows(name):
    with open(TASK / "sources" / name, encoding="utf-8") as file:
        return list(csv.DictReader(line for line in file if not line.startswith("#")))


evaluation = rows("eval.csv")
rates = [100 * int(r["successes"]) / int(r["trials"]) for r in evaluation]
best = rates.index(max(rates))
fig, ax = plt.subplots(figsize=(8, 4.2))
bars = ax.bar([r["condition"] for r in evaluation], rates, color=["#0070C0" if i == best else "#5B9BD5" for i in range(len(rates))])
for bar, r in zip(bars, evaluation):
    ax.annotate(f"{r['successes']}/{r['trials']}", (bar.get_x() + bar.get_width() / 2, bar.get_height()), ha="center", va="bottom", xytext=(0, 4), textcoords="offset points")
ax.set_ylabel("성공률 (%)")
ax.set_ylim(0, 100)
ax.set_xlabel("조건 (청크 길이)")
fig.savefig(TASK / "figures/success-by-chunk.png")

failures = rows("failures.csv")
fig, ax = plt.subplots(figsize=(6, 4.2))
ax.barh([r["failure_type"] for r in failures][::-1], [int(r["count"]) for r in failures][::-1], color="#0070C0")
ax.set_xlabel("횟수 (ACT-8, 실패 11회)")
fig.savefig(TASK / "figures/failure-types.png")
