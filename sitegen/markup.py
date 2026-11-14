"""Turning content values into HTML text. Escaping happens here and nowhere else."""

from __future__ import annotations

import html
import re

from sitegen.model import Inline, Link, Prose

_APOSTROPHE = re.compile(r"(?<=\w)'(?=\w|\s|[.,;:)]|$)")


def text(raw: str) -> str:
    """Escape plain text for HTML, typesetting straight apostrophes as curly ones."""
    return html.escape(_APOSTROPHE.sub("’", raw), quote=True)


def is_internal(url: str) -> bool:
    """Internal links are written site-absolute, e.g. "/software/#fortress"."""
    return url.startswith("/")


def href(url: str, root: str) -> str:
    """Resolve a link for a page whose relative path to the site root is `root`.

    Internal links become relative, so the site works at any base path: the
    custom domain, a GitHub project page, or a local preview server.
    """
    resolved = (root + url[1:] or "./") if is_internal(url) else url
    return html.escape(resolved, quote=True)


def anchor(link: Link, root: str, *, rel: str | None = None) -> str:
    rel_attr = f' rel="{rel}"' if rel else ""
    return f'<a href="{href(link.url, root)}"{rel_attr}>{text(link.text)}</a>'


def inline(piece: Inline, root: str) -> str:
    if isinstance(piece, Link):
        return anchor(piece, root)
    return text(piece)


def prose(pieces: Prose, root: str) -> str:
    return "".join(inline(piece, root) for piece in pieces)


def paragraphs(blocks: tuple[Prose, ...], root: str) -> str:
    return "\n".join(f"<p>{prose(block, root)}</p>" for block in blocks)


def name_list(names: tuple[str, ...]) -> str:
    """Join names as prose: "A", "A and B", "A, B, and C". A trailing "et al." is kept as is."""
    if names and names[-1] == "et al.":
        return ", ".join(names)
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + f", and {names[-1]}"
