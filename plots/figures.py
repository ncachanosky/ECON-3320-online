"""
Regression Theorem Timeline
Money, Institutions, and Markets — Chapter 1

Illustrates the logical regress underlying the regression theorem:
monetary value today is anchored by yesterday's value, traced back
to an originating non-monetary commodity use.

Two branches show how the chain was extended in practice:
  1. Fiat money inherited value from gold-linked predecessors
  2. Bitcoin faces a bootstrapping problem — no commodity anchor

Economic Order color palette:
  Sky Blue    #5B9BD5  — main timeline nodes
  Copper      #B87333  — node highlights / commodity anchor
  Sage Green  #87A96B  — fiat money branch
  Terracotta  #D4745E  — Bitcoin branch
  Charcoal    #36454F  — text and arrows
  Lavender    #8E7AB5  — accent / question mark node
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# ── EO palette ────────────────────────────────────────────────────────────────
SKY_BLUE   = "#5B9BD5"
COPPER     = "#B87333"
SAGE       = "#87A96B"
TERRACOTTA = "#D4745E"
CHARCOAL   = "#36454F"
LAVENDER   = "#8E7AB5"
WHITE      = "#FFFFFF"
LIGHT_GRAY = "#F5F5F5"

# ── Figure setup ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 6))
ax.set_xlim(0, 14)
ax.set_ylim(0, 6)
ax.axis("off")
fig.patch.set_facecolor(WHITE)

# ── Helper functions ──────────────────────────────────────────────────────────

def draw_node(ax, x, y, label, sublabel=None,
              facecolor=SKY_BLUE, textcolor=WHITE,
              width=1.8, height=0.75, fontsize=9.5):
    """Draw a rounded rectangle node with label."""
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width, height,
        boxstyle="round,pad=0.08",
        facecolor=facecolor,
        edgecolor=CHARCOAL,
        linewidth=1.2,
        zorder=3
    )
    ax.add_patch(box)
    if sublabel:
        ax.text(x, y + 0.13, label,
                ha="center", va="center",
                fontsize=fontsize, fontweight="bold",
                color=textcolor, zorder=4)
        ax.text(x, y - 0.18, sublabel,
                ha="center", va="center",
                fontsize=fontsize - 1.5,
                color=textcolor, zorder=4,
                style="italic")
    else:
        ax.text(x, y, label,
                ha="center", va="center",
                fontsize=fontsize, fontweight="bold",
                color=textcolor, zorder=4)


def draw_arrow(ax, x1, y1, x2, y2, color=CHARCOAL,
               label=None, label_offset=(0, 0.22)):
    """Draw a horizontal/straight arrow between two points."""
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=1.6,
            mutation_scale=16
        ),
        zorder=2
    )
    if label:
        mx = (x1 + x2) / 2 + label_offset[0]
        my = (y1 + y2) / 2 + label_offset[1]
        ax.text(mx, my, label,
                ha="center", va="center",
                fontsize=8, color=color,
                style="italic")


def draw_dashed_arrow(ax, x1, y1, x2, y2, color=CHARCOAL):
    """Draw a dashed diagonal arrow for branches."""
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=1.4,
            linestyle="dashed",
            mutation_scale=14
        ),
        zorder=2
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TIMELINE  (y = 3.8)
# ═══════════════════════════════════════════════════════════════════════════════
Y_MAIN = 3.8

# Node x-positions
xs = [1.2, 3.4, 5.6, 7.8, 10.0]

node_data = [
    (xs[0], "Commodity\nValue",      None,                COPPER),
    (xs[1], "Early Monetary\nUse",   None,                SKY_BLUE),
    (xs[2], "Established\nMoney",    None,                SKY_BLUE),
    (xs[3], "Gold Standard /\nBretton Woods", None,       SKY_BLUE),
    (xs[4], "Present\nValue",        None,                SKY_BLUE),
]

for (x, lbl, sub, fc) in node_data:
    draw_node(ax, x, Y_MAIN, lbl, sub, facecolor=fc)

# Arrows between main nodes
arrow_labels = ["anchors →", "anchors →", "anchors →", "anchors →"]
for i in range(len(xs) - 1):
    x1 = xs[i] + 0.9
    x2 = xs[i + 1] - 0.9
    draw_arrow(ax, x1, Y_MAIN, x2, Y_MAIN,
               label=arrow_labels[i])

# Section label above timeline
ax.text(5.6, 5.35, "The Regression Theorem",
        ha="center", va="center",
        fontsize=13, fontweight="bold", color=CHARCOAL)
ax.text(5.6, 4.95,
        "Monetary value today is anchored by value yesterday — "
        "traced back to an originating non-monetary commodity use.",
        ha="center", va="center",
        fontsize=9, color=CHARCOAL, style="italic")

# Origin label under first node
ax.text(xs[0], Y_MAIN - 0.72,
        "Non-monetary\norigin",
        ha="center", va="top",
        fontsize=8, color=COPPER, fontweight="bold")


# ═══════════════════════════════════════════════════════════════════════════════
# BRANCH: "The Chain Continues…" from Bretton Woods node
# ═══════════════════════════════════════════════════════════════════════════════

BRANCH_X  = xs[3]   # x of "Gold Standard / Bretton Woods"
BRANCH_Y  = Y_MAIN  # same height

# ── Branch header ──────────────────────────────────────────────────────────────
ax.text(11.5, 4.78, "How the Chain\nContinues…",
        ha="center", va="center",
        fontsize=9.5, fontweight="bold", color=CHARCOAL)

# ── Branch 1: Fiat money (upper) ───────────────────────────────────────────────
Y_FIAT = 2.65
X_FIAT = 12.2

draw_dashed_arrow(ax,
                  BRANCH_X + 0.9, BRANCH_Y - 0.25,
                  X_FIAT - 0.9,   Y_FIAT + 0.35,
                  color=SAGE)

draw_node(ax, X_FIAT, Y_FIAT,
          "Fiat Money",
          sublabel="inherits from gold predecessor",
          facecolor=SAGE, textcolor=WHITE,
          width=2.4, height=0.72, fontsize=8.8)

# ── Branch 2: Bitcoin (lower) ──────────────────────────────────────────────────
Y_BTC = 1.45
X_BTC = 12.2

draw_dashed_arrow(ax,
                  BRANCH_X + 0.9, BRANCH_Y - 0.38,
                  X_BTC - 0.9,    Y_BTC + 0.35,
                  color=TERRACOTTA)

draw_node(ax, X_BTC, Y_BTC,
          "Bitcoin / Crypto",
          sublabel="no commodity anchor — value\nfrom expectations alone?",
          facecolor=TERRACOTTA, textcolor=WHITE,
          width=2.4, height=0.80, fontsize=8.8)

# Question mark in lavender circle next to Bitcoin node
circle = plt.Circle((X_BTC + 1.42, Y_BTC + 0.02), 0.22,
                     color=LAVENDER, zorder=5)
ax.add_patch(circle)
ax.text(X_BTC + 1.42, Y_BTC + 0.02, "?",
        ha="center", va="center",
        fontsize=12, fontweight="bold",
        color=WHITE, zorder=6)


# ═══════════════════════════════════════════════════════════════════════════════
# BOTTOM NOTE
# ═══════════════════════════════════════════════════════════════════════════════
ax.text(0.3, 0.28,
        "Mises (1912): money's value cannot be explained without reference to its prior value — "
        "the regress terminates only at a commodity origin.",
        ha="left", va="center",
        fontsize=7.8, color=CHARCOAL, style="italic",
        wrap=True)

# ── Save ───────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.4)
plt.savefig("regression_theorem.png", dpi=150, bbox_inches="tight",
            facecolor=WHITE)
plt.show()
print("Saved: regression_theorem.png")