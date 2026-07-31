# szviz 💕

A tiny, **love-themed** data-visualization library built on top of
[matplotlib](https://matplotlib.org/). It was made to explore the
[Speed Dating dataset](https://www.kaggle.com/datasets/annavictoria/speed-dating-experiment),
so the defaults lean romantic: a rose-red primary color, a warm validated
palette, soft pastel fills, and **heart-shaped scatter markers**.

The whole library is a single ~200-line module — small enough to read in one
sitting.

## Install

```bash
pip install -e .
```

## Quickstart

The two figures below are the heart of the demo — both come straight from
[`examples/speed_dating.py`](examples/speed_dating.py), which runs with
**zero setup** on a bundled data sample:

```bash
python examples/speed_dating.py
```

```python
import szviz

szviz.set_theme()  # apply the love theme to every following figure

# ── Visual 1: grouped bars by gender, sorted high → low ───────────────
szviz.grouped_bar(
    ["Attractive", "Sincere", "Intelligent", "Fun", "Ambitious", "Shared int."],
    {"Women": women_means, "Men": men_means},   # no colors= → plum + gold default
    sort="desc", ylabel="mean rating",
    title="Average rating received, by gender (1-10)",
)
szviz.save("ratings_by_gender.png")

# ── Visual 2: age histogram with the modal bin highlighted ────────────
fig, ax = szviz.hist(ages, bins=25, xlabel="age", title="Age of participants")
peak = max(ax.patches, key=lambda b: b.get_height())   # the tallest bin
peak.set_facecolor("#AF8A24")                          # recolor the mode gold
center = peak.get_x() + peak.get_width() / 2
ax.annotate(f"mode ≈ {center:.0f}  (n={int(peak.get_height())})",
            xy=(center, peak.get_height()), xytext=(0, 8),
            textcoords="offset points", ha="center",
            fontweight="bold", color="#AF8A24")
szviz.save("age_histogram.png")
```

Every helper returns the `(fig, ax)` pair, so — as with the mode highlight above
— you can keep customizing with plain matplotlib afterwards.

## What you get

| Helper | Chart |
|--------|-------|
| `set_theme(dark=False)` | Apply the love theme (blush or plum-dark surface) |
| `line(x, y, ...)` | Line chart |
| `scatter(x, y, ...)` | Scatter plot with heart markers |
| `bar(labels, values, ...)` | Vertical bars |
| `grouped_bar(labels, groups, ...)` | Grouped bars, one series per group |
| `barh(labels, values, ...)` | Horizontal bars |
| `hist(data, ...)` | Histogram |
| `pie(labels, values, ...)` | Pie chart |
| `show()` / `save(path)` | Display or export the figure |

Pass `marker=...` to `scatter` to opt out of hearts, or `szviz.HEART` to bring
them anywhere else.

## The palette

`szviz.ROSE` is the default single-series color (`#E23A6D`). `szviz.PALETTE` is
the categorical cycle used when a chart holds several series — a
colorblind-checked, romantic set (rose · plum · coral · *something blue* · gold
· berry) that reads cleanly on both light and dark backgrounds:

`#E23A6D` · `#8E56A6` · `#DA6C2E` · `#2F9E8E` · `#AF8A24` · `#BE2A86`

Extras for this dataset:

- `szviz.GROUPED` — the default cycle for `grouped_bar`, leading with plum and
  gold (`#8E56A6`, `#AF8A24`) then teal/coral/berry; colorblind-checked as
  adjacent pairs so grouped series stay distinct without leaning on the
  pink/blue gender cliché.
- `szviz.PASTELS` — soft blush/lavender/peach tints for fills and backgrounds
  (intentionally light, so use them for area fills, not to tell series apart).
- `szviz.MATCH` / `szviz.NO_MATCH` — a rose/muted-gray pair for the dataset's
  binary `match` outcome.
- `szviz.HEART` — the heart-shaped marker `Path`, reusable in any matplotlib call.

## Examples

[`examples/speed_dating.py`](examples/speed_dating.py) is a runnable tour of the
library on the Speed Dating dataset — it produces the two visuals from the
Quickstart (the grouped by-gender chart and the mode-highlighted age
histogram). With no arguments it runs on the bundled sample
([`examples/sample_speed_dating.csv`](examples/sample_speed_dating.csv), a
~250-row excerpt) so it works out of the box:

```bash
python examples/speed_dating.py
```

For the full picture, download "Speed Dating Data.csv" from
[Kaggle](https://www.kaggle.com/datasets/annavictoria/speed-dating-experiment)
and pass its path:

```bash
python examples/speed_dating.py path/to/Speed_Dating_Data.csv
```

## License

MIT — see [LICENSE](LICENSE).
