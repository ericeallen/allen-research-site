"""Write the site to disk. All file-system effects live in this module."""

from __future__ import annotations

import shutil
from pathlib import Path
from urllib.parse import urlsplit

from sitegen import content
from sitegen.model import Figure, Video
from sitegen.pages import Page, all_pages, render

REPOSITORY: Path = Path(__file__).resolve().parent.parent
STATIC: Path = REPOSITORY / "static"
DEFAULT_OUT: Path = REPOSITORY / "_site"
OUTPUT_MARKER = ".sitegen-output"
"""A build only replaces a directory that holds this file, or is empty."""


def sitemap(pages: tuple[Page, ...], origin: str) -> str:
    urls = "\n".join(f"  <url><loc>{origin}/{page.path}</loc></url>" for page in pages if page.listed)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )


def robots(origin: str) -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {origin}/sitemap.xml\n"


def missing_static_files() -> list[str]:
    """Static files the content refers to that are not in static/."""
    media = [project.media for project in content.PROJECTS]
    referenced = (
        [f"slides/{deck.file}" for deck in content.SLIDE_DECKS]
        + [f"img/{m.file}" for m in media if isinstance(m, Figure)]
        + [f"demo/{name}" for m in media if isinstance(m, Video) for name in (m.file, m.poster, m.transcript)]
    )
    return [name for name in referenced if not (STATIC / name).is_file()]


def build(out: Path = DEFAULT_OUT) -> tuple[Path, ...]:
    """Build the whole site into `out`, replacing what was there. Returns the files written."""
    missing = missing_static_files()
    if missing:
        raise FileNotFoundError(f"content refers to files missing from static/: {missing}")

    pages = all_pages()
    origin = content.SITE.origin
    generated = {
        **{page.file: render(page, pages) for page in pages},
        "sitemap.xml": sitemap(pages, origin),
        "robots.txt": robots(origin),
        # GitHub Pages reads the custom domain from this file.
        "CNAME": f"{urlsplit(origin).hostname}\n",
        # Tells GitHub Pages to serve the files as they are, without Jekyll.
        ".nojekyll": "",
        OUTPUT_MARKER: "Written by sitegen. The next build replaces this directory.\n",
    }

    if out.exists():
        if any(out.iterdir()) and not (out / OUTPUT_MARKER).is_file():
            raise FileExistsError(
                f"{out} is not empty and was not written by this build; refusing to replace it"
            )
        shutil.rmtree(out)
    shutil.copytree(STATIC, out)
    for name, body in generated.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    return tuple(sorted(path for path in out.rglob("*") if path.is_file()))
