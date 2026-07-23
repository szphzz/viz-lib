# szviz 💕

A tiny, **love-themed** data-visualization library built on top of
[matplotlib](https://matplotlib.org/). It was made to explore the
[Speed Dating dataset](https://www.kaggle.com/datasets/annavictoria/speed-dating-experiment),
so the defaults lean romantic: a rose-red primary color, a warm validated
palette, soft pastel fills, and **heart-shaped scatter markers**.

The whole library is a single ~180-line module — small enough to read in one
sitting.

## Install

```bash
pip install -e .
```

## Quickstart

```python
import szviz

szviz.set_theme()  # apply the love theme to every following figure

# Single series defaults to rose-red
szviz.line([0, 1, 2, 3], [3, 1, 4, 2], title="Interest over the date")
szviz.show()

# Scatter draws little hearts by default 💗
szviz.scatter(attractiveness, likelihood, title="Attractiveness vs. liking")

# Categorical charts cycle through the szviz palette
szviz.bar(["Attr", "Sinc", "Intel", "Fun", "Amb", "Shar"], prefs,
          title="What people say they want")
szviz.save("prefs.png")
```

## What you get

| Helper | Chart |
|--------|-------|
| `set_theme(dark=False)` | Apply the love theme (blush or plum-dark surface) |
| `line(x, y, ...)` | Line chart |
| `scatter(x, y, ...)` | Scatter plot with heart markers |
| `bar(labels, values, ...)` | Vertical bars |
| `barh(labels, values, ...)` | Horizontal bars |
| `hist(data, ...)` | Histogram |
| `pie(labels, values, ...)` | Pie chart |
| `show()` / `save(path)` | Display or export the figure |

Every helper returns the `(fig, ax)` pair, so you can keep customizing with
plain matplotlib afterwards. Pass `marker=...` to `scatter` to opt out of
hearts, or `szviz.HEART` to bring them anywhere else.

## The palette

`szviz.ROSE` is the default single-series color (`#E23A6D`). `szviz.PALETTE` is
the categorical cycle used when a chart holds several series — a
colorblind-checked, romantic set (rose · plum · coral · *something blue* · gold
· berry) that reads cleanly on both light and dark backgrounds:

`#E23A6D` · `#8E56A6` · `#DA6C2E` · `#2F9E8E` · `#AF8A24` · `#BE2A86`

Extras for this dataset:

- `szviz.PASTELS` — soft blush/lavender/peach tints for fills and backgrounds
  (intentionally light, so use them for area fills, not to tell series apart).
- `szviz.MATCH` / `szviz.NO_MATCH` — a rose/muted-gray pair for the dataset's
  binary `match` outcome.
- `szviz.HEART` — the heart-shaped marker `Path`, reusable in any matplotlib call.

## License

MIT — see [LICENSE](LICENSE).
