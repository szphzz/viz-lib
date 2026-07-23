"""szviz core: a tiny, love-themed matplotlib wrapper.

Built to explore the Speed Dating dataset, so the defaults lean romantic:
a rose-red primary colour, a validated warm palette, soft pastel fills and
heart-shaped scatter markers. Every helper returns the ``(fig, ax)`` pair so
you can keep tweaking with plain matplotlib afterwards.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path

# --- palette ---------------------------------------------------------------
# ROSE is the default single-series colour. PALETTE is the categorical cycle
# (rose, plum, coral, "something blue", gold, berry): colourblind-checked and
# legible on both light and dark surfaces. PASTELS are soft tints for fills and
# backgrounds -- they are intentionally light, so use them for area/fill, not
# to tell series apart. MATCH / NO_MATCH label the dataset's binary outcome.
ROSE = "#E23A6D"
PALETTE = ["#E23A6D", "#8E56A6", "#DA6C2E", "#2F9E8E", "#AF8A24", "#BE2A86"]
PASTELS = ["#F9C9D6", "#E7D3F0", "#F7D9BE", "#C6E6DF", "#EFE3B0", "#F3C4DE"]
MATCH, NO_MATCH = "#E23A6D", "#B9AEB4"

_LIGHT = {"surface": "#FDE7EC", "ink": "#3A2530", "grid": "#F1CCD7"}
_DARK = {"surface": "#1F1A1E", "ink": "#F5E6EC", "grid": "#3E3238"}


def _heart_path() -> Path:
    """A unit-scaled heart, used as the default scatter marker."""
    t = np.linspace(0, 2 * np.pi, 100)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    v = np.column_stack([x, y])
    v = v - v.mean(axis=0)
    return Path(v / np.abs(v).max())


HEART = _heart_path()


def set_theme(dark: bool = False) -> None:
    """Apply the szviz love theme to every subsequent matplotlib figure.

    Sets the rose colour cycle, a soft blush (or plum-dark) surface, a
    recessive grid, thin marks and clean spines. Call once near the top of a
    script or notebook.
    """
    c = _DARK if dark else _LIGHT
    plt.rcParams.update(
        {
            "axes.prop_cycle": plt.cycler(color=PALETTE),
            "figure.facecolor": c["surface"],
            "axes.facecolor": c["surface"],
            "savefig.facecolor": c["surface"],
            "axes.edgecolor": c["grid"],
            "axes.labelcolor": c["ink"],
            "axes.titlecolor": c["ink"],
            "text.color": c["ink"],
            "xtick.color": c["ink"],
            "ytick.color": c["ink"],
            "axes.grid": True,
            "axes.grid.axis": "y",
            "axes.axisbelow": True,
            "grid.color": c["grid"],
            "grid.linewidth": 1.0,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "lines.linewidth": 2.0,
            "lines.markersize": 9,
            "figure.figsize": (8, 5),
            "figure.dpi": 110,
        }
    )


def _prepare(ax, title, xlabel, ylabel):
    """Create an axes if one was not supplied, then apply shared labels."""
    if ax is None:
        _, ax = plt.subplots()
    if title:
        ax.set_title(title, loc="left", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    return ax, ax.figure


def line(x, y, *, label=None, color=ROSE, title=None, xlabel=None,
         ylabel=None, ax=None, **kwargs):
    """Line chart. ``color`` defaults to rose for a single series."""
    ax, fig = _prepare(ax, title, xlabel, ylabel)
    ax.plot(x, y, color=color, label=label, **kwargs)
    if label:
        ax.legend(frameon=False)
    return fig, ax


def scatter(x, y, *, label=None, color=ROSE, marker=HEART, title=None,
            xlabel=None, ylabel=None, ax=None, **kwargs):
    """Scatter plot drawn with heart markers. ``color`` defaults to rose."""
    ax, fig = _prepare(ax, title, xlabel, ylabel)
    kwargs.setdefault("s", 120)
    kwargs.setdefault("alpha", 0.85)
    ax.scatter(x, y, color=color, marker=marker, label=label, **kwargs)
    if label:
        ax.legend(frameon=False)
    return fig, ax


def bar(labels: Sequence, values: Sequence, *, color=ROSE, title=None,
        xlabel=None, ylabel=None, ax=None, **kwargs):
    """Vertical bar chart with gap-separated bars."""
    ax, fig = _prepare(ax, title, xlabel, ylabel)
    surface = plt.rcParams["axes.facecolor"]
    ax.bar(labels, values, color=color, edgecolor=surface, linewidth=2,
           **kwargs)
    ax.grid(axis="x", visible=False)
    return fig, ax


def barh(labels: Sequence, values: Sequence, *, color=ROSE, title=None,
         xlabel=None, ylabel=None, ax=None, **kwargs):
    """Horizontal bar chart, handy for long category names."""
    ax, fig = _prepare(ax, title, xlabel, ylabel)
    surface = plt.rcParams["axes.facecolor"]
    ax.barh(labels, values, color=color, edgecolor=surface, linewidth=2,
            **kwargs)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.invert_yaxis()
    return fig, ax


def hist(data, *, bins=20, color=ROSE, title=None, xlabel=None,
         ylabel="Count", ax=None, **kwargs):
    """Histogram of a single distribution."""
    ax, fig = _prepare(ax, title, xlabel, ylabel)
    surface = plt.rcParams["axes.facecolor"]
    ax.hist(data, bins=bins, color=color, edgecolor=surface, linewidth=1,
            **kwargs)
    return fig, ax


def pie(labels: Sequence, values: Sequence, *, colors: Optional[Sequence] = None,
        title=None, ax=None, **kwargs):
    """Pie chart cycling through the szviz palette."""
    ax, fig = _prepare(ax, title, None, None)
    colors = colors or PALETTE
    surface = plt.rcParams["axes.facecolor"]
    ax.pie(values, labels=labels, colors=colors, autopct="%1.0f%%",
           wedgeprops={"edgecolor": surface, "linewidth": 2}, **kwargs)
    ax.set_aspect("equal")
    ax.grid(False)
    return fig, ax


def show() -> None:
    """Convenience wrapper around ``matplotlib.pyplot.show``."""
    plt.tight_layout()
    plt.show()


def save(path: str, *, fig=None, dpi: int = 200) -> None:
    """Save the current (or given) figure with a tight bounding box."""
    fig = fig or plt.gcf()
    fig.tight_layout()
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
