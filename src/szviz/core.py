"""szviz core: a tiny matplotlib wrapper with a lilac-purple default palette.

Every plotting helper returns the ``(fig, ax)`` pair so you can keep tweaking
the result with plain matplotlib afterwards.
"""

from __future__ import annotations

from typing import Optional, Sequence

import matplotlib.pyplot as plt

# --- palette ---------------------------------------------------------------
# LILAC is the default single-series colour. PALETTE is the categorical cycle
# used when several series share a chart; it is colourblind-checked and works
# on both light and dark surfaces (lilac first, then well-separated hues).
LILAC = "#9B72CF"
PALETTE = ["#9B72CF", "#CE6B26", "#2E86C9", "#4E9E4A", "#D14D9A", "#B08A1E"]

_LIGHT = {"surface": "#FCFCFB", "ink": "#1A1A19", "grid": "#E4E1EA"}
_DARK = {"surface": "#1A1A19", "ink": "#F2F0F5", "grid": "#3A3A42"}


def set_theme(dark: bool = False) -> None:
    """Apply the szviz look to every subsequent matplotlib figure.

    Sets the lilac colour cycle, a recessive grid, thin marks and clean spines.
    Call once near the top of a script or notebook.
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
            "grid.color": c["grid"],
            "grid.linewidth": 1.0,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "lines.linewidth": 2.0,
            "lines.markersize": 8,
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


def line(x, y, *, label=None, color=LILAC, title=None, xlabel=None,
         ylabel=None, ax=None, **kwargs):
    """Line chart. ``color`` defaults to lilac for a single series."""
    ax, fig = _prepare(ax, title, xlabel, ylabel)
    ax.plot(x, y, color=color, label=label, **kwargs)
    if label:
        ax.legend(frameon=False)
    return fig, ax


def scatter(x, y, *, label=None, color=LILAC, title=None, xlabel=None,
            ylabel=None, ax=None, **kwargs):
    """Scatter plot. ``color`` defaults to lilac."""
    ax, fig = _prepare(ax, title, xlabel, ylabel)
    kwargs.setdefault("s", 60)
    kwargs.setdefault("alpha", 0.85)
    ax.scatter(x, y, color=color, label=label, **kwargs)
    if label:
        ax.legend(frameon=False)
    return fig, ax


def bar(labels: Sequence, values: Sequence, *, color=LILAC, title=None,
        xlabel=None, ylabel=None, ax=None, **kwargs):
    """Vertical bar chart with rounded, gap-separated bars."""
    ax, fig = _prepare(ax, title, xlabel, ylabel)
    surface = plt.rcParams["axes.facecolor"]
    ax.bar(labels, values, color=color, edgecolor=surface, linewidth=2,
           **kwargs)
    ax.grid(axis="x", visible=False)
    return fig, ax


def barh(labels: Sequence, values: Sequence, *, color=LILAC, title=None,
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


def hist(data, *, bins=20, color=LILAC, title=None, xlabel=None,
         ylabel="Count", ax=None, **kwargs):
    """Histogram of a single distribution."""
    ax, fig = _prepare(ax, title, xlabel, ylabel)
    surface = plt.rcParams["axes.facecolor"]
    ax.hist(data, bins=bins, color=color, edgecolor=surface, linewidth=1,
            **kwargs)
    return fig, ax


def pie(labels: Sequence, values: Sequence, *, colors: Optional[Sequence] = None,
        title=None, ax=None, **kwargs):
    """Pie chart cycling through the szviz categorical palette."""
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
