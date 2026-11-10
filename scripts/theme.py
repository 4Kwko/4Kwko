"""Shared palette for the profile SVGs (dark and light GitHub themes)."""

FONT = "ui-monospace, 'Cascadia Mono', Consolas, Menlo, 'DejaVu Sans Mono', monospace"

THEMES = {
    "dark": {
        "bg": "#111b27",
        "text": "#f2f6fa",
        "accent": "#55d8b2",
        "muted": "#a6b7c9",
        "line": "#35475b",
        "series": ["#55d8b2", "#f2bc59", "#75aaf5", "#ed8ca1", "#b2a4e8"],
    },
    "light": {
        "bg": "#f3eee5",
        "text": "#14212c",
        "accent": "#0b6652",
        "muted": "#4d5b68",
        "line": "#c9bfae",
        "series": ["#0b6652", "#8a5a12", "#2d5f9a", "#9c3d5a", "#5b4b9a"],
    },
}
