# szviz

A tiny data-visualization library built on top of
[matplotlib](https://matplotlib.org/). It ships a **lilac-purple** default
palette and a handful of one-line chart helpers so a plot looks good before you
touch a single style setting.

The whole library is a single ~180-line module — small enough to read in one
sitting.

## Install

```bash
pip install -e .
```

## Quickstart

```python
import szviz

szviz.set_theme()  # apply the lilac look to every following figure

# Single series defaults to lilac purple
szviz.line([0, 1, 2, 3], [3, 1, 4, 2], title="Signal", xlabel="t", ylabel="v")
szviz.show()

# Categorical charts cycle through the szviz palette
szviz.bar(["A", "B", "C"], [10, 7, 13], title="Counts")
szviz.save("counts.png")
```

## What you get

| Helper | Chart |
|--------|-------|
| `set_theme(dark=False)` | Apply the lilac theme (light or dark surface) |
| `line(x, y, ...)` | Line chart |
| `scatter(x, y, ...)` | Scatter plot |
| `bar(labels, values, ...)` | Vertical bars |
| `barh(labels, values, ...)` | Horizontal bars |
| `hist(data, ...)` | Histogram |
| `pie(labels, values, ...)` | Pie chart |
| `show()` / `save(path)` | Display or export the figure |

Every helper returns the `(fig, ax)` pair, so you can keep customizing with
plain matplotlib afterwards.

## The palette

`szviz.LILAC` is the default single-series color (`#9B72CF`). `szviz.PALETTE` is
the categorical cycle used when a chart holds several series — a
colorblind-checked set that reads cleanly on both light and dark backgrounds:

`#9B72CF` · `#CE6B26` · `#2E86C9` · `#4E9E4A` · `#D14D9A` · `#B08A1E`

## License

MIT — see [LICENSE](LICENSE).
