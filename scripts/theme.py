"""Shared palette for the profile SVGs (dark and light GitHub themes)."""

FONT = "ui-monospace, 'Cascadia Mono', Consolas, Menlo, 'DejaVu Sans Mono', monospace"

THEMES = {
    "dark": {
        "bg": "#28261d",
        "text": "#f6edd9",
        "accent": "#f3a284",
        "muted": "#d7cbb1",
        "line": "#645841",
        "panel": "#333125",
        "series": ["#b9cf9e", "#f3a284", "#a6c6ca", "#e5c386", "#dab3c4"],
    },
    "light": {
        "bg": "#f6edd9",
        "text": "#29281f",
        "accent": "#9b3d26",
        "muted": "#675d48",
        "line": "#c9b79a",
        "panel": "#fcf5e4",
        "series": ["#475735", "#9b3d26", "#3e5b66", "#76522e", "#694458"],
    },
}
