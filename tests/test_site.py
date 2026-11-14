"""Checks on the built site. Run with: python -m unittest discover tests"""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urlsplit

from sitegen import content
from sitegen.build import build
from sitegen.markup import href, name_list, text
from sitegen.model import Publication, PublicationKind
from sitegen.pages import _publication, all_pages, current_employer, selected_publications


@dataclass
class Parsed:
    """What the checks need to know about one HTML page."""

    links: list[str] = field(default_factory=list)
    ids: list[str] = field(default_factory=list)
    headings: list[int] = field(default_factory=list)
    images: list[dict[str, str | None]] = field(default_factory=list)
    meta: dict[str, str] = field(default_factory=dict)
    canonical: str | None = None
    title: str = ""
    json_ld: list[str] = field(default_factory=list)


class _Reader(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.page = Parsed()
        self._capture: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        page = self.page
        if identifier := a.get("id"):
            page.ids.append(identifier)
        if tag in ("a", "link") and a.get("href"):
            page.links.append(a["href"] or "")
        if tag == "link" and a.get("rel") == "canonical":
            page.canonical = a.get("href")
        if tag == "img":
            page.images.append(a)
            page.links.append(a.get("src") or "")
            page.links.extend(part.split()[0] for part in (a.get("srcset") or "").split(",") if part)
        if tag in ("video", "source"):
            page.links.extend(a[name] or "" for name in ("src", "poster") if a.get(name))
        if tag == "meta" and (key := a.get("name") or a.get("property")):
            page.meta[key] = a.get("content") or ""
        if re.fullmatch(r"h[1-6]", tag):
            page.headings.append(int(tag[1]))
        if tag == "title":
            self._capture = "title"
        if tag == "script" and a.get("type") == "application/ld+json":
            self._capture = "json_ld"
            page.json_ld.append("")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("title", "script"):
            self._capture = None

    def handle_data(self, data: str) -> None:
        if self._capture == "title":
            self.page.title += data
        elif self._capture == "json_ld":
            self.page.json_ld[-1] += data


def parse(path: Path) -> Parsed:
    reader = _Reader()
    reader.feed(path.read_text(encoding="utf-8"))
    return reader.page


class BuiltSite(unittest.TestCase):
    out: Path
    pages: dict[str, Parsed]
    _tmp: tempfile.TemporaryDirectory[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name) / "site"
        build(cls.out)
        cls.pages = {page.file: parse(cls.out / page.file) for page in all_pages()}

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def _target(self, page_file: str, url: str) -> tuple[Path, str]:
        """The output file and fragment an internal link on `page_file` points at."""
        path, fragment = urldefrag(url)
        base = self.out if path.startswith("/") else (self.out / page_file).parent
        target = (base / path.lstrip("/")).resolve() if path else self.out / page_file
        return (target / "index.html" if target.is_dir() else target), fragment

    def test_every_internal_link_resolves(self) -> None:
        for page_file, page in self.pages.items():
            for url in page.links:
                if urlsplit(url).scheme:
                    continue
                target, fragment = self._target(page_file, url)
                with self.subTest(page=page_file, url=url):
                    self.assertTrue(target.is_file(), f"{url} -> {target} does not exist")
                    self.assertTrue(target.resolve().is_relative_to(self.out.resolve()))
                    if fragment:
                        self.assertIn(fragment, parse(target).ids)

    def test_external_links_are_absolute_https_or_known_http(self) -> None:
        plain_http = {url for page in self.pages.values() for url in page.links if url.startswith("http://")}
        # The only host that still serves this document does not offer HTTPS.
        self.assertEqual(
            plain_http, {"http://web.cs.ucla.edu/~palsberg/course/cs239/papers/fortress1.0beta.pdf"}
        )

    def test_each_page_has_one_h1_and_no_skipped_heading_level(self) -> None:
        for page_file, page in self.pages.items():
            with self.subTest(page=page_file):
                self.assertEqual(page.headings.count(1), 1)
                self.assertEqual(page.headings[0], 1)
                for previous, current in zip(page.headings, page.headings[1:], strict=False):
                    self.assertLessEqual(current, previous + 1)

    def test_ids_are_unique_within_a_page(self) -> None:
        for page_file, page in self.pages.items():
            with self.subTest(page=page_file):
                self.assertEqual(len(page.ids), len(set(page.ids)))

    def test_titles_and_descriptions_are_present_and_distinct(self) -> None:
        titles = [page.title for page in self.pages.values()]
        descriptions = [page.meta.get("description", "") for page in self.pages.values()]
        self.assertTrue(all(titles) and all(descriptions))
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))
        for description in descriptions:
            self.assertLessEqual(len(description), 170, description)

    def test_listed_pages_are_canonical_and_in_the_sitemap(self) -> None:
        sitemap = (self.out / "sitemap.xml").read_text(encoding="utf-8")
        for page in all_pages():
            parsed = self.pages[page.file]
            expected = f"{content.SITE.origin}/{page.path}"
            with self.subTest(page=page.file):
                if page.listed:
                    self.assertEqual(parsed.canonical, expected)
                    self.assertIn(f"<loc>{expected}</loc>", sitemap)
                else:
                    self.assertIsNone(parsed.canonical)
                    self.assertNotIn(expected, sitemap)
                    self.assertEqual(parsed.meta.get("robots"), "noindex")

    def test_images_declare_alt_text_and_dimensions(self) -> None:
        images = [image for page in self.pages.values() for image in page.images]
        self.assertTrue(images)
        for image in images:
            with self.subTest(src=image.get("src")):
                self.assertTrue(image.get("alt"))
                self.assertTrue(image.get("width") and image.get("height"))

    def test_person_metadata_matches_the_cv(self) -> None:
        (raw,) = self.pages["index.html"].json_ld
        person = json.loads(raw)
        self.assertEqual(person["@type"], "Person")
        self.assertEqual(person["name"], content.SITE.author)
        employer = current_employer()
        self.assertEqual(person.get("worksFor", {}).get("name"), employer)

    def test_no_page_loads_scripts_or_third_party_resources(self) -> None:
        for page in all_pages():
            source = (self.out / page.file).read_text(encoding="utf-8")
            with self.subTest(page=page.file):
                self.assertNotRegex(source, r"<script(?! type=\"application/ld\+json\")")
                self.assertNotRegex(
                    source, r"<(?:img|iframe|script|video|source)[^>]+(?:src|poster)=\"https?://"
                )
                self.assertNotRegex(source, r"<link rel=\"(?:stylesheet|icon)\" href=\"https?://")

    def test_build_is_deterministic(self) -> None:
        again = Path(self._tmp.name) / "again"
        build(again)
        first = {p.relative_to(self.out): p.read_bytes() for p in self.out.rglob("*") if p.is_file()}
        second = {p.relative_to(again): p.read_bytes() for p in again.rglob("*") if p.is_file()}
        self.assertEqual(first, second)

    def test_build_refuses_to_replace_a_directory_it_did_not_write(self) -> None:
        foreign = Path(self._tmp.name) / "foreign"
        foreign.mkdir()
        (foreign / "keep.txt").write_text("not ours")
        with self.assertRaises(FileExistsError):
            build(foreign)
        self.assertEqual((foreign / "keep.txt").read_text(), "not ours")


class Content(unittest.TestCase):
    def test_selected_publications_resolve_in_order(self) -> None:
        self.assertEqual(tuple(p.title for p in selected_publications()), content.SELECTED_TITLES)

    def test_featured_projects_exist(self) -> None:
        slugs = {project.slug for project in content.PROJECTS}
        self.assertLessEqual(set(content.FEATURED_PROJECTS), slugs)

    def test_at_most_one_current_role(self) -> None:
        current = [r for e in content.EXPERIENCE for r in e.roles if r.end is None]
        self.assertLessEqual(len(current), 1)

    def test_roles_are_listed_newest_first(self) -> None:
        starts = [role.start for employer in content.EXPERIENCE for role in employer.roles]
        self.assertEqual(starts, sorted(starts, reverse=True))


class Markup(unittest.TestCase):
    def test_text_is_escaped(self) -> None:
        self.assertEqual(text('<b> & "q"'), "&lt;b&gt; &amp; &quot;q&quot;")

    def test_apostrophes_are_typeset(self) -> None:
        self.assertEqual(text("Sigma's teams' work"), "Sigma’s teams’ work")

    def test_content_cannot_inject_markup(self) -> None:
        hostile = Publication(
            PublicationKind.PAPER,
            ("<i>A</i>",),
            "<script>x</script>",
            "v",
            "2000",
            'https://example.org/"onmouseover="x',
        )
        rendered = _publication(hostile, "")
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("<i>", rendered)
        self.assertNotIn('"onmouseover', rendered)

    def test_internal_links_are_relative_to_the_page(self) -> None:
        self.assertEqual(href("/cv/#patents", "../"), "../cv/#patents")
        self.assertEqual(href("/cv/", ""), "cv/")
        self.assertEqual(href("/", ""), "./")
        self.assertEqual(href("/", "/"), "/")
        self.assertEqual(href("https://example.org/?a=1&b=2", "../"), "https://example.org/?a=1&amp;b=2")

    def test_name_lists_read_as_prose(self) -> None:
        self.assertEqual(name_list(("A",)), "A")
        self.assertEqual(name_list(("A", "B")), "A and B")
        self.assertEqual(name_list(("A", "B", "C")), "A, B, and C")
        self.assertEqual(name_list(("A", "B", "et al.")), "A, B, et al.")


if __name__ == "__main__":
    unittest.main()
