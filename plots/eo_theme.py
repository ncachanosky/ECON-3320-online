"""
eo_theme.py
-----------
Shared Economic Order Plotly theme for Money, Institutions, and Markets.
ECON 3320 – Money and Banking | Nicolas Cachanosky | UTEP

Usage
-----
In any chapter plot script:

    from eo_theme import EO, apply_eo_theme, save_plot

    fig = go.Figure(...)
    fig = apply_eo_theme(fig, title="My Chart", source="FRED")
    save_plot(fig, "plots/html/ch01_example.html")
"""

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

class EO:
    """Economic Order color palette."""
    PRIMARY    = "#5B9BD5"   # Sky Blue      — main data series
    SECONDARY  = "#87A96B"   # Sage Green    — secondary series
    HIGHLIGHT  = "#B87333"   # Copper        — highlight / callout
    ACCENT     = "#D4745E"   # Terracotta    — tertiary / accent
    LAVENDER   = "#8E7AB5"   # Lavender      — additional series
    TEXT       = "#36454F"   # Charcoal      — labels, annotations
    BACKGROUND = "#FFFFFF"   # White         — plot background
    GRID       = "#E8E8E8"   # Light gray    — gridlines

    # Ordered list for multi-series plots
    SEQUENCE = [PRIMARY, SECONDARY, HIGHLIGHT, ACCENT, LAVENDER]


# ---------------------------------------------------------------------------
# Base Plotly template
# ---------------------------------------------------------------------------

eo_template = go.layout.Template(
    layout=go.Layout(
        # Fonts
        font=dict(
            family="Georgia, 'Times New Roman', serif",
            size=13,
            color=EO.TEXT,
        ),
        title=dict(
            font=dict(size=16, color=EO.TEXT, family="Georgia, serif"),
            x=0.0,
            xanchor="left",
            pad=dict(l=0, t=10),
        ),

        # Colors
        colorway=EO.SEQUENCE,
        paper_bgcolor=EO.BACKGROUND,
        plot_bgcolor=EO.BACKGROUND,

        # Axes — x
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor=EO.TEXT,
            linewidth=1,
            ticks="outside",
            tickcolor=EO.TEXT,
            tickfont=dict(size=11, color=EO.TEXT),
            title_font=dict(size=12, color=EO.TEXT),
        ),

        # Axes — y
        yaxis=dict(
            showgrid=True,
            gridcolor=EO.GRID,
            gridwidth=1,
            zeroline=False,
            showline=False,
            tickfont=dict(size=11, color=EO.TEXT),
            title_font=dict(size=12, color=EO.TEXT),
        ),

        # Legend
        legend=dict(
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor=EO.GRID,
            borderwidth=1,
            font=dict(size=11, color=EO.TEXT),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),

        # Margins
        margin=dict(l=60, r=30, t=80, b=60),

        # Hover
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=EO.TEXT,
            font=dict(size=12, color=EO.TEXT),
        ),
        hovermode="x unified",
    )
)

# Register the template globally
pio.templates["eo"] = eo_template
pio.templates.default = "eo"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def apply_eo_theme(
    fig: go.Figure,
    title: str = "",
    subtitle: str = "",
    source: str = "",
    yaxis_title: str = "",
    xaxis_title: str = "",
    height: int = 450,
    width: int = 750,
) -> go.Figure:
    """
    Apply the EO theme to a Plotly figure and add standard metadata.

    Parameters
    ----------
    fig         : Plotly Figure object
    title       : Main chart title
    subtitle    : Optional subtitle (appended below title via annotation)
    source      : Data source string shown in bottom-left annotation
    yaxis_title : Y-axis label
    xaxis_title : X-axis label (leave blank for time series — date is implicit)
    height      : Figure height in pixels (default 450)
    width       : Figure width in pixels (default 750)

    Returns
    -------
    fig : Plotly Figure with EO theme applied
    """
    annotations = []

    # Subtitle
    if subtitle:
        annotations.append(dict(
            text=subtitle,
            xref="paper", yref="paper",
            x=0, y=1.08,
            xanchor="left", yanchor="bottom",
            font=dict(size=12, color=EO.TEXT),
            showarrow=False,
        ))

    # Source note
    if source:
        annotations.append(dict(
            text=f"Source: {source}",
            xref="paper", yref="paper",
            x=0, y=-0.12,
            xanchor="left", yanchor="top",
            font=dict(size=10, color=EO.TEXT),
            showarrow=False,
        ))

    fig.update_layout(
        template="eo",
        title_text=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        height=height,
        width=width,
        annotations=annotations,
    )

    return fig


def save_plot(fig: go.Figure, filepath: str) -> None:
    """
    Save a Plotly figure as a self-contained HTML file for embedding in Quarto.

    Parameters
    ----------
    fig      : Plotly Figure object
    filepath : Output path, e.g. "plots/html/ch01_money_supply.html"
    """
    fig.write_html(
        filepath,
        include_plotlyjs="cdn",   # Load Plotly from CDN — keeps file size small
        full_html=False,          # Fragment only — embeds cleanly in Quarto iframe
        config={
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
            "responsive": True,
        },
    )
    print(f"Saved: {filepath}")


def make_dual_axis(title: str = "", source: str = "", height: int = 450) -> go.Figure:
    """
    Create a dual-axis figure with EO theme pre-applied.
    Useful for overlaying two series with different scales (e.g., inflation + interest rate).

    Returns a Figure with two y-axes: yaxis (left) and yaxis2 (right).
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = apply_eo_theme(fig, title=title, source=source, height=height)
    fig.update_layout(
        yaxis2=dict(
            showgrid=False,
            tickfont=dict(size=11, color=EO.TEXT),
            title_font=dict(size=12, color=EO.TEXT),
        )
    )
    return fig


# ---------------------------------------------------------------------------
# Recession shading utility
# ---------------------------------------------------------------------------

# NBER recession dates (add more as needed)
NBER_RECESSIONS = [
    ("1973-11-01", "1975-03-01"),
    ("1980-01-01", "1980-07-01"),
    ("1981-07-01", "1982-11-01"),
    ("1990-07-01", "1991-03-01"),
    ("2001-03-01", "2001-11-01"),
    ("2007-12-01", "2009-06-01"),
    ("2020-02-01", "2020-04-01"),
]


def add_recession_shading(fig: go.Figure, recessions: list = None) -> go.Figure:
    """
    Add NBER recession shading to a time-series figure.

    Parameters
    ----------
    fig        : Plotly Figure object
    recessions : List of (start, end) date string tuples.
                 Defaults to NBER_RECESSIONS defined above.

    Returns
    -------
    fig : Figure with recession bands added
    """
    if recessions is None:
        recessions = NBER_RECESSIONS

    for start, end in recessions:
        fig.add_vrect(
            x0=start, x1=end,
            fillcolor="lightgray",
            opacity=0.25,
            layer="below",
            line_width=0,
        )

    return fig