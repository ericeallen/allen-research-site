"""The site's pages as pure functions from content to HTML."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Final

from sitegen import content
from sitegen.markup import anchor, href, name_list, paragraphs, prose, text
from sitegen.model import (
    Award,
    Course,
    Degree,
    Employer,
    Figure,
    Link,
    Patent,
    Project,
    Publication,
    PublicationKind,
    Role,
    Site,
    SlideDeck,
    Talk,
    Video,
)

HEADSHOT_SMALL: Final = "img/eric-allen-360.jpg"
HEADSHOT_LARGE: Final = "img/eric-allen-720.jpg"
HEADSHOT_WIDTH: Final = 360
HEADSHOT_HEIGHT: Final = 606


@dataclass(frozen=True)
class Page:
    path: str
    """Path under the site root: "" for the home page, "cv/" for a section."""
    file: str
    """Output file, relative to the site root."""
    root: str
    """Prefix that takes a link on this page back to the site root."""
    title: str
    description: str
    body: str
    nav_label: str | None = None
    head_extra: str = ""
    listed: bool = True
    """Whether the page belongs in the sitemap."""


# ---------------------------------------------------------------------------
# Shared pieces
# ---------------------------------------------------------------------------


def _entry(when: str, body: str, *, continued: bool = False) -> str:
    classes = "entry continued" if continued else "entry"
    return (
        f'<li class="{classes}">'
        f'<div class="entry-when">{text(when)}</div>'
        f'<div class="entry-body">{body}</div>'
        "</li>"
    )


def _entries(items: list[str]) -> str:
    return '<ul class="entries">\n' + "\n".join(items) + "\n</ul>"


def _link_row(links: tuple[Link, ...], root: str, *, rel: str | None = None) -> str:
    if not links:
        return ""
    items = "".join(f"<li>{anchor(link, root, rel=rel)}</li>" for link in links)
    return f'<ul class="links">{items}</ul>'


def _titled(title: str, url: str | None, root: str) -> str:
    return anchor(Link(title, url), root) if url else text(title)


def _badge(label: str | None) -> str:
    return f' <span class="badge">{text(label)}</span>' if label else ""


def _section_id(heading: str) -> str:
    return heading.lower().replace(" ", "-")


def _toc(headings: tuple[str, ...]) -> str:
    items = "".join(f'<li><a href="#{_section_id(heading)}">{text(heading)}</a></li>' for heading in headings)
    return f'<nav class="toc" aria-label="On this page"><ul>{items}</ul></nav>'


def _section(heading: str, body: str) -> str:
    return f'<section>\n<h2 id="{_section_id(heading)}">{text(heading)}</h2>\n{body}\n</section>'


# ---------------------------------------------------------------------------
# Publications
# ---------------------------------------------------------------------------


def _publication(pub: Publication, root: str) -> str:
    body = (
        f'<p class="entry-title">{_titled(pub.title, pub.url, root)}{_badge(pub.note)}</p>'
        f'<p class="entry-meta">{text(name_list(pub.authors))}</p>'
        f'<p class="entry-meta">{text(pub.venue)}</p>'
        f"{_link_row(pub.links, root)}"
    )
    return _entry(pub.date, body)


def publications_body(root: str) -> str:
    kinds = tuple(PublicationKind)
    sections = "\n".join(
        _section(
            kind.value,
            _entries([_publication(p, root) for p in content.PUBLICATIONS if p.kind is kind]),
        )
        for kind in kinds
    )
    scholar = next(p for p in content.SITE.profiles if p.label == "Google Scholar")
    return (
        "<h1>Publications</h1>\n"
        '<p class="lede">Citation counts and an always-current list are on '
        f"{anchor(Link('Google Scholar', scholar.url), root)}. "
        f'Patents are on the <a href="{href("/cv/#patents", root)}">CV</a>.</p>\n'
        f"{_toc(tuple(kind.value for kind in kinds))}\n"
        f"{sections}"
    )


def selected_publications() -> tuple[Publication, ...]:
    """The publications named in SELECTED_TITLES, in that order. Fails on an unknown title."""
    papers = {p.title: p for p in content.PUBLICATIONS if p.kind is PublicationKind.PAPER}
    missing = [title for title in content.SELECTED_TITLES if title not in papers]
    if missing:
        raise ValueError(f"SELECTED_TITLES names no paper in PUBLICATIONS: {missing}")
    return tuple(papers[title] for title in content.SELECTED_TITLES)


# ---------------------------------------------------------------------------
# Software
# ---------------------------------------------------------------------------


def _media(media: Figure | Video | None, root: str) -> str:
    if media is None:
        return ""
    if isinstance(media, Figure):
        return (
            "<figure>"
            f'<img src="{href("/img/" + media.file, root)}" alt="{text(media.alt)}" '
            f'width="{media.width}" height="{media.height}" loading="lazy">'
            f"<figcaption>{text(media.caption)}</figcaption>"
            "</figure>\n"
        )
    transcript = anchor(Link("Transcript", "/demo/" + media.transcript), root)
    return (
        "<figure>"
        f'<video controls playsinline preload="none" width="{media.width}" height="{media.height}" '
        f'poster="{href("/demo/" + media.poster, root)}" aria-label="{text(media.label)}">'
        f'<source src="{href("/demo/" + media.file, root)}" type="video/mp4">'
        "</video>"
        f"<figcaption>{text(media.caption)} {transcript}.</figcaption>"
        "</figure>\n"
    )


def _project(project: Project, root: str) -> str:
    return (
        f'<article class="project" id="{project.slug}">\n'
        f"<h2>{text(project.name)}</h2>\n"
        f'<p class="tagline">{text(project.tagline)} · {text(project.context)}</p>\n'
        f"{_link_row(project.links, root)}\n"
        f"{_media(project.media, root)}"
        f"{paragraphs(project.paragraphs, root)}\n"
        "</article>"
    )


def software_body(root: str) -> str:
    return f'<h1>Software</h1>\n<p class="lede">{prose(content.SOFTWARE_INTRO, root)}</p>\n' + "\n".join(
        _project(project, root) for project in content.PROJECTS
    )


# ---------------------------------------------------------------------------
# Talks
# ---------------------------------------------------------------------------


def _talk(talk: Talk, root: str) -> str:
    year = talk.date.rsplit(" ", 1)[-1]
    event = _titled(talk.event, talk.url, root)
    body = (
        f'<p class="entry-title">{text(talk.title)}{_badge(talk.note)}</p>'
        f'<p class="entry-meta">{event}. {text(talk.place)}, {text(talk.date)}.</p>'
    )
    return _entry(year, body)


def _deck(deck: SlideDeck, root: str) -> str:
    link = anchor(Link(deck.title, "/slides/" + deck.file), root)
    body = (
        f'<p class="entry-title">{link}</p>'
        f'<p class="entry-meta">{text(deck.description)} {deck.pages} slides.</p>'
    )
    return _entry(str(deck.year), body)


def _course(course: Course, root: str) -> str:
    body = (
        f'<p class="entry-title">{_titled(course.name, course.url, root)}</p>'
        f'<p class="entry-meta">{text(course.institution)}, {text(course.terms)}. '
        f"{prose(course.detail, root)}</p>"
    )
    return _entry(course.code, body)


def talks_body(root: str) -> str:
    headings = ("Selected talks", "Slides", "Courses")
    return (
        "<h1>Talks</h1>\n"
        f"{_toc(headings)}\n"
        + _section(headings[0], _entries([_talk(t, root) for t in content.TALKS]))
        + "\n"
        + _section(headings[1], _entries([_deck(d, root) for d in content.SLIDE_DECKS]))
        + "\n"
        + _section(headings[2], _entries([_course(c, root) for c in content.COURSES]))
    )


# ---------------------------------------------------------------------------
# CV
# ---------------------------------------------------------------------------


def _years(start: int, end: int | None) -> str:
    if end is None:
        return f"{start}–present"
    return str(start) if start == end else f"{start}–{end}"


def _role(employer: Employer, role: Role, *, first: bool, root: str) -> str:
    org = f'<p class="entry-org">{text(employer.name)}</p>' if first else ""
    summary = f"<p>{prose(role.summary, root)}</p>" if role.summary else ""
    body = f'{org}<p class="entry-title">{text(role.title)}</p>{summary}'
    return _entry(_years(role.start, role.end), body, continued=not first)


def _employers(employers: tuple[Employer, ...], root: str) -> str:
    return _entries(
        [
            _role(employer, role, first=index == 0, root=root)
            for employer in employers
            for index, role in enumerate(employer.roles)
        ]
    )


def _degree(degree: Degree, root: str) -> str:
    body = (
        f'<p class="entry-org">{text(degree.institution)}</p>'
        f'<p class="entry-title">{text(degree.degree)}</p>'
        f"<p>{prose(degree.detail, root)}</p>"
    )
    return _entry(_years(degree.start, degree.end), body)


def _patent(patent: Patent, root: str) -> str:
    body = (
        f'<p class="entry-title">{anchor(Link(patent.title, patent.url), root)}</p>'
        f'<p class="entry-meta">{text(patent.number)}. {text(name_list(patent.inventors))}.</p>'
    )
    return _entry(str(patent.granted), body)


def _award(award: Award) -> str:
    body = f'<p class="entry-title">{text(award.title)}</p><p class="entry-meta">{text(award.detail)}</p>'
    return _entry(str(award.year), body)


def cv_body(root: str) -> str:
    headings = ("Experience", "Teaching", "Education", "Patents", "Awards")
    sections = (
        _employers(content.EXPERIENCE, root),
        _employers(content.TEACHING, root),
        _entries([_degree(d, root) for d in content.EDUCATION]),
        _entries([_patent(p, root) for p in content.PATENTS]),
        _entries([_award(a) for a in content.AWARDS]),
    )
    return (
        "<h1>Curriculum vitae</h1>\n"
        f'<p class="lede">Publications are listed '
        f'<a href="{href("/publications/", root)}">separately</a>.</p>\n'
        f"{_toc(headings)}\n" + "\n".join(_section(h, s) for h, s in zip(headings, sections, strict=True))
    )


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------


def _current_work(root: str) -> str:
    def item(project: Project) -> str:
        name = anchor(Link(project.name, f"/software/#{project.slug}"), root)
        return _entry(
            project.context,
            f'<p class="entry-title">{name}</p>'
            f'<p class="entry-meta">{text(project.tagline)}.</p>'
            f"{_link_row(project.links, root)}",
        )

    featured = [p for p in content.PROJECTS if p.slug in content.FEATURED_PROJECTS]
    return _entries([item(p) for p in featured])


def home_body(root: str) -> str:
    site = content.SITE
    contact = (
        Link("Email", f"mailto:{site.email}"),
        *tuple(Link(profile.label, profile.url) for profile in site.profiles),
    )
    portrait = (
        f'<img src="{href("/" + HEADSHOT_SMALL, root)}" '
        f'srcset="{href("/" + HEADSHOT_SMALL, root)} {HEADSHOT_WIDTH}w, {href("/" + HEADSHOT_LARGE, root)} {2 * HEADSHOT_WIDTH}w" '
        'sizes="(max-width: 36rem) 7.5rem, 10.5rem" '
        f'width="{HEADSHOT_WIDTH}" height="{HEADSHOT_HEIGHT}" alt="Portrait of {text(site.author)}">'
    )
    return (
        '<div class="intro">\n<div>\n'
        f"<h1>{text(site.author)}</h1>\n"
        f'<p class="tagline">{text(site.tagline)}</p>\n'
        f"{paragraphs(content.HOME_INTRO, root)}\n"
        f"{_link_row(contact, root, rel='me')}\n"
        f"</div>\n{portrait}\n</div>\n"
        + _section("Current work", _current_work(root))
        + "\n"
        + _section(
            "Selected publications",
            _entries([_publication(p, root) for p in selected_publications()])
            + f'\n<p class="more"><a href="{href("/publications/", root)}">All publications</a></p>',
        )
        + "\n"
        + _section(
            "Background",
            paragraphs(content.HOME_HISTORY, root)
            + f'\n<p class="more"><a href="{href("/cv/", root)}">Full CV</a></p>',
        )
    )


def current_employer() -> str | None:
    """The employer of the first role with no end date, if any."""
    return next(
        (e.name for e in content.EXPERIENCE for role in e.roles if role.end is None),
        None,
    )


def person_json_ld(site: Site) -> str:
    """schema.org Person, so search engines attach the site to the right Eric Allen."""
    employer = current_employer()
    person: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": site.author,
        "url": f"{site.origin}/",
        "image": f"{site.origin}/{HEADSHOT_LARGE}",
        "description": site.description,
        "sameAs": [profile.url for profile in site.profiles],
        "alumniOf": [
            {"@type": "CollegeOrUniversity", "name": name}
            for name in dict.fromkeys(degree.institution for degree in content.EDUCATION)
        ],
    }
    if employer:
        person["worksFor"] = {"@type": "Organization", "name": employer}
    # "</" cannot end the script element early once the slash is escaped.
    payload = json.dumps(person, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{payload}\n</script>'


# ---------------------------------------------------------------------------
# The page list and the frame around each page
# ---------------------------------------------------------------------------


def _section_page(slug: str, label: str, description: str, body: str) -> Page:
    return Page(
        path=f"{slug}/",
        file=f"{slug}/index.html",
        root="../",
        title=label,
        description=description,
        body=body,
        nav_label=label,
    )


def all_pages() -> tuple[Page, ...]:
    site = content.SITE
    not_found = (
        "<h1>Page not found</h1>\n"
        "<p>There is nothing at this address. The site moved in 2026, so an old link "
        'may have brought you here. Try the <a href="/">home page</a>, the '
        '<a href="/publications/">publications</a>, or the <a href="/cv/">CV</a>.</p>'
    )
    return (
        Page(
            path="",
            file="index.html",
            root="",
            title=site.author,
            description=site.description,
            body=home_body(""),
            head_extra=person_json_ld(site),
        ),
        _section_page(
            "publications",
            "Publications",
            "Papers, books, technical reports, and articles by Eric Allen, from DrJava and "
            "Generic Java through Project Fortress to units of measure in Lean 4.",
            publications_body("../"),
        ),
        _section_page(
            "software",
            "Software",
            "Open source software by Eric Allen: Λs, a calculus for units of measure "
            "mechanized in Lean 4; Towel, a Python refactoring tool; Project Fortress; and DrJava.",
            software_body("../"),
        ),
        _section_page(
            "talks",
            "Talks",
            "Talks, slides, and courses by Eric Allen on programming languages and machine learning.",
            talks_body("../"),
        ),
        _section_page(
            "cv",
            "CV",
            "Curriculum vitae of Eric Allen: experience, teaching, education, patents, and awards.",
            cv_body("../"),
        ),
        Page(
            path="404.html",
            file="404.html",
            root="/",
            title="Page not found",
            description="There is nothing at this address.",
            body=not_found,
            listed=False,
        ),
    )


def _nav(pages: tuple[Page, ...], current: Page) -> str:
    def item(page: Page) -> str:
        here = ' aria-current="page"' if page.path == current.path else ""
        return (
            f'<li><a href="{href("/" + page.path, current.root)}"{here}>{text(page.nav_label or "")}</a></li>'
        )

    items = [item(page) for page in pages if page.nav_label]
    if content.SITE.blog_url:
        items.append(f'<li><a href="{href(content.SITE.blog_url, current.root)}">Blog</a></li>')
    return '<nav aria-label="Primary"><ul>' + "".join(items) + "</ul></nav>"


def render(page: Page, pages: tuple[Page, ...]) -> str:
    """The complete HTML document for one page."""
    site = content.SITE
    is_home = page.path == ""
    title = f"{site.author} · {site.tagline}" if is_home else f"{page.title} · {site.author}"
    canonical = f"{site.origin}/{page.path}"
    robots = "" if page.listed else '<meta name="robots" content="noindex">\n'
    canonical_tags = (
        f'<link rel="canonical" href="{text(canonical)}">\n'
        f'<meta property="og:url" content="{text(canonical)}">\n'
        if page.listed
        else ""
    )
    contact = (
        Link("Email", f"mailto:{site.email}"),
        *tuple(Link(profile.label, profile.url) for profile in site.profiles),
    )
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{text(title)}</title>\n"
        f'<meta name="description" content="{text(page.description)}">\n'
        f'<meta name="author" content="{text(site.author)}">\n'
        f"{robots}{canonical_tags}"
        f'<meta property="og:type" content="{"profile" if is_home else "website"}">\n'
        f'<meta property="og:site_name" content="{text(site.author)}">\n'
        f'<meta property="og:title" content="{text(title)}">\n'
        f'<meta property="og:description" content="{text(page.description)}">\n'
        f'<meta property="og:image" content="{text(site.origin)}/{HEADSHOT_LARGE}">\n'
        '<meta name="twitter:card" content="summary">\n'
        f'<link rel="icon" href="{href("/favicon.svg", page.root)}" type="image/svg+xml">\n'
        f'<link rel="stylesheet" href="{href("/style.css", page.root)}">\n'
        f"{page.head_extra}{chr(10) if page.head_extra else ''}"
        "</head>\n"
        "<body>\n"
        '<a class="skip" href="#main">Skip to content</a>\n'
        '<header class="site-header">\n'
        f'<a class="site-name" href="{href("/", page.root)}">{text(site.author)}</a>\n'
        f"{_nav(pages, page)}\n"
        "</header>\n"
        '<main id="main">\n'
        f"{page.body}\n"
        "</main>\n"
        '<footer class="site-footer">\n'
        f"<p>{text(site.author)} · {text(site.location)}</p>\n"
        f"{_link_row(contact, page.root)}\n"
        "<p>The views expressed on this site are my own.</p>\n"
        "</footer>\n"
        "</body>\n"
        "</html>\n"
    )
