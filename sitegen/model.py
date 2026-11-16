"""The shapes of the site's content.

Every value here is immutable. Prose is a tuple of inline pieces rather than a
string of HTML, so text is escaped in exactly one place (the renderer) and
content can never smuggle markup into a page.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Link:
    text: str
    url: str


type Inline = str | Link
type Prose = tuple[Inline, ...]


class PublicationKind(Enum):
    PAPER = "Papers"
    BOOK = "Books and theses"
    REPORT = "Technical reports"
    ARTICLE = "Articles"


@dataclass(frozen=True)
class Publication:
    kind: PublicationKind
    authors: tuple[str, ...]
    title: str
    venue: str
    date: str
    """A year or a range of years, shown in the date column."""
    url: str | None = None
    note: str | None = None
    links: tuple[Link, ...] = ()


@dataclass(frozen=True)
class Patent:
    number: str
    title: str
    inventors: tuple[str, ...]
    granted: int
    url: str


@dataclass(frozen=True)
class Figure:
    file: str
    """A file in static/img/."""
    alt: str
    caption: str
    width: int
    height: int


@dataclass(frozen=True)
class Video:
    """A silent recording, shown with controls and never played automatically."""

    file: str
    """A file in static/demo/, as are the poster and the transcript."""
    poster: str
    transcript: str
    label: str
    """What the video shows, for a reader who cannot see it."""
    caption: str
    width: int
    height: int


@dataclass(frozen=True)
class Project:
    slug: str
    name: str
    tagline: str
    context: str
    """Where and when, e.g. "Sun Labs, 2003–2011"."""
    paragraphs: tuple[Prose, ...]
    links: tuple[Link, ...]
    media: Figure | Video | None = None


@dataclass(frozen=True)
class Role:
    title: str
    start: int
    end: int | None
    """None means the role is current."""
    summary: Prose = ()


@dataclass(frozen=True)
class Employer:
    name: str
    roles: tuple[Role, ...]


@dataclass(frozen=True)
class Degree:
    institution: str
    degree: str
    start: int
    end: int
    detail: Prose


@dataclass(frozen=True)
class Award:
    title: str
    year: int
    detail: str


@dataclass(frozen=True)
class Talk:
    title: str
    event: str
    place: str
    date: str
    """A full date ending in the year, e.g. "January 20, 2007"."""
    url: str | None = None
    note: str | None = None


@dataclass(frozen=True)
class Course:
    code: str
    name: str
    institution: str
    terms: str
    detail: Prose
    url: str | None = None


@dataclass(frozen=True)
class SlideDeck:
    title: str
    file: str
    year: int
    pages: int
    description: str


@dataclass(frozen=True)
class Profile:
    """A place Eric can be found elsewhere; rendered with rel="me"."""

    label: str
    url: str


@dataclass(frozen=True)
class Site:
    origin: str
    """Scheme and host with no trailing slash, e.g. https://allen-research.com."""
    author: str
    tagline: str
    description: str
    email: str
    profiles: tuple[Profile, ...]
    blog_url: str | None
    """None until the blog is live; the navigation shows it only when set."""
