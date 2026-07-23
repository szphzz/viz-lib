"""Explore the Speed Dating dataset with szviz.

Usage:
    python examples/speed_dating.py [path/to/Speed_Dating_Data.csv] [out_dir]

The dataset isn't bundled with the library. Grab "Speed Dating Data.csv" from
https://www.kaggle.com/datasets/annavictoria/speed-dating-experiment and pass
its path as the first argument (default: ./Speed_Dating_Data.csv). Charts are
written as PNGs into the output directory (default: alongside this script).

The file uses Latin-1 encoding and carriage-return line endings; csv.DictReader
handles both. gender is coded 0 = women, 1 = men.
"""

import csv
import os
import sys

import matplotlib.pyplot as plt

import szviz

# Partner-assigned rating columns (the "_o" = "from the other person") and the
# friendly labels we show on charts.
ATTRS = ["attr_o", "sinc_o", "intel_o", "fun_o", "amb_o", "shar_o"]
LABELS = ["Attractive", "Sincere", "Intelligent", "Fun", "Ambitious",
          "Shared int."]


def load(path):
    """Read the CSV into a list of dict rows, or exit with guidance."""
    if not os.path.exists(path):
        sys.exit(
            f"Could not find the dataset at {path!r}.\n"
            "Download 'Speed Dating Data.csv' from Kaggle "
            "(annavictoria/speed-dating-experiment) and pass its path:\n"
            "    python examples/speed_dating.py path/to/Speed_Dating_Data.csv"
        )
    with open(path, newline="", encoding="latin-1") as f:
        return list(csv.DictReader(f))


def numbers(rows, name, where=None):
    """The parseable float values in column ``name``, optionally filtered."""
    out = []
    for r in rows:
        if where and not where(r):
            continue
        try:
            out.append(float(r.get(name, "").strip()))
        except ValueError:
            pass
    return out


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def overview(rows, out_dir):
    """A four-panel tour of the dataset."""
    szviz.set_theme()
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))

    szviz.bar(LABELS, [mean(numbers(rows, a)) for a in ATTRS],
              color=szviz.PALETTE, title="Average rating received (1-10)",
              ax=ax[0][0])
    ax[0][0].tick_params(axis="x", labelrotation=30)

    pairs = [(x, y) for x, y in zip(numbers(rows, "attr_o"),
                                    numbers(rows, "like_o"))][:600]
    szviz.scatter([p[0] for p in pairs], [p[1] for p in pairs], alpha=0.35,
                  title="Attractiveness vs. liking", xlabel="attractive",
                  ylabel="liked", ax=ax[0][1])

    m = numbers(rows, "match")
    hits = sum(m)
    szviz.pie(["Match", "No match"], [hits, len(m) - hits],
              colors=[szviz.MATCH, szviz.NO_MATCH], title="Did sparks fly?",
              ax=ax[1][0])

    szviz.hist(numbers(rows, "age"), bins=25, title="Age of participants",
               xlabel="age", ax=ax[1][1])

    fig.suptitle("szviz  ♥  Speed Dating", fontsize=18,
                 fontweight="bold", x=0.02, ha="left")
    path = os.path.join(out_dir, "overview.png")
    szviz.save(path, fig=fig)
    print(f"wrote {path}  (match rate {hits / len(m):.1%})")


def ratings_by_gender(rows, out_dir):
    """Grouped bars of mean rating received, women vs men, sorted high->low."""
    women = [mean(numbers(rows, a, lambda r: r["gender"].strip() == "0"))
             for a in ATTRS]
    men = [mean(numbers(rows, a, lambda r: r["gender"].strip() == "1"))
           for a in ATTRS]
    # No colors= -> szviz.GROUPED default (plum + gold).
    fig, _ = szviz.grouped_bar(LABELS, {"Women": women, "Men": men},
                               sort="desc", ylabel="mean rating",
                               title="Average rating received, by gender (1-10)")
    path = os.path.join(out_dir, "ratings_by_gender.png")
    szviz.save(path, fig=fig)
    print(f"wrote {path}")


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "Speed_Dating_Data.csv"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(__file__)
    os.makedirs(out_dir, exist_ok=True)
    rows = load(csv_path)
    print(f"loaded {len(rows)} rows from {csv_path}")
    overview(rows, out_dir)
    ratings_by_gender(rows, out_dir)


if __name__ == "__main__":
    main()
