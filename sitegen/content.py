"""Everything the site says. Edit this file to change the site's content.

Order within each tuple is the order on the page: newest first.
"""

from __future__ import annotations

from typing import Final

from sitegen.model import (
    Award,
    Course,
    Degree,
    Employer,
    Figure,
    Link,
    Patent,
    Profile,
    Project,
    Prose,
    Publication,
    PublicationKind,
    Role,
    Site,
    SlideDeck,
    Talk,
    Video,
)

ME: Final = "Eric Allen"


def doi(identifier: str) -> str:
    return f"https://doi.org/{identifier}"


SITE: Final = Site(
    origin="https://allen-research.com",
    author=ME,
    tagline="AI and Logic",
    description=(
        "Eric Allen is a Quantitative Engineer on the AI Innovation Team at Two Sigma. "
        "His background is in type systems, logic, and formal methods."
    ),
    email="eric@allen-research.com",
    location="New York",
    profiles=(
        Profile("GitHub", "https://github.com/ericeallen"),
        Profile("Google Scholar", "https://scholar.google.com/citations?user=OY3oJzoAAAAJ"),
        Profile("LinkedIn", "https://www.linkedin.com/in/ericeallen"),
    ),
    blog_url=None,
)

LAMBDA_S_PAPER_URL: Final = "https://arxiv.org/abs/2609.38242"
LAMBDA_S_REPO_URL: Final = "https://github.com/ericeallen/lambda-s"
TOWEL_REPO_URL: Final = "https://github.com/ericeallen/towel"

# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

HOME_INTRO: Final[tuple[Prose, ...]] = (
    (
        "I am a Quantitative Engineer on the AI Innovation Team at Two Sigma. My "
        "background is in type systems, logic, and formal methods, applied to "
        "everything from knowledge representation to programming languages, proof "
        "assistants, reinforcement learning, and natural language processing. "
        "Since 2011 much of my work has been in machine learning, and the "
        "questions that motivate me are where it meets logic.",
    ),
)

HOME_HISTORY: Final[tuple[Prose, ...]] = (
    (
        "I was the founder and Chief Scientist of Acrisure Capital, a "
        "quantitative investment firm, and Chief Technology Officer of Tulco Labs, "
        "an AI incubator, and of several Tulco startups. Before that I was a "
        "researcher on Two Sigma's AI Core Team, and a Principal Engineer at Sun "
        "Labs on ",
        Link("Project Fortress", "/software/#fortress"),
        ", a DARPA-sponsored programming language for high-performance computing. "
        "I set up the first data science teams at Bazaarvoice and RetailMeNot "
        "around the time of their IPOs, and I have taught at Rice and at the "
        "University of Texas at Austin.",
    ),
    (
        "My PhD in computer science is from Rice University, where I worked with "
        "Robert Cartwright on generic types for Java. My bachelor's degrees, in "
        "mathematics and in computer science, are from Cornell.",
    ),
)


# ---------------------------------------------------------------------------
# Software
# ---------------------------------------------------------------------------

PROJECTS: Final[tuple[Project, ...]] = (
    Project(
        slug="lambda-s",
        name="Λs",
        tagline="A calculus for units of measure with conversion, mechanized in Lean 4",
        context="2026",
        paragraphs=(
            (
                "Typed unit calculi prove that well-typed programs are invariant "
                "under rescaling: no program can depend on how big a meter is. They "
                "obtain this by admitting no operation that can observe a unit, and "
                "so no conversion. Practical languages provide conversion but no "
                "invariance theorem. Λs has both. It is a typed lambda calculus in "
                "which conversion between units of the same dimension is a "
                "primitive, and it determines exactly how much invariance survives.",
            ),
            (
                "The repository is the artifact of the paper ",
                Link("A Calculus for Units of Measure with Conversion", LAMBDA_S_PAPER_URL),
                ": the full Lean 4 mechanization of the statics, dynamics, and "
                "denotational semantics, two abstraction theorems, a decidable "
                "diagnostic for conversion drift, a verified checker for unit "
                "declarations, adequacy, erasure, and the Pi theorem of dimensional "
                "analysis. The evaluator compiles to a native binary.",
            ),
            (
                "This is a return to a problem I first worked on at Sun Labs: see ",
                Link("Object-Oriented Units of Measurement", doi("10.1145/1035292.1029008")),
                " (OOPSLA 2004).",
            ),
        ),
        links=(
            Link("Source", LAMBDA_S_REPO_URL),
            Link("Paper", LAMBDA_S_PAPER_URL),
            Link("API documentation", "https://ericeallen.github.io/lambda-s/"),
        ),
    ),
    Project(
        slug="towel",
        name="Towel",
        tagline="Finds repeated Python code and refactors it into shared helpers",
        context="2025–present",
        paragraphs=(
            (
                "Towel finds repeated Python code and extracts it into shared helper "
                "functions. It checks each extraction, preserves the parts that "
                "differ as parameters, and leaves meaningful names for you to choose.",
            ),
            (
                "The method is anti-unification. Given two fragments of code, Towel "
                "computes their least general generalization: the most specific "
                "template of which both are instances. The template becomes the "
                "helper, and the places where the fragments differ become its "
                "parameters.",
            ),
        ),
        links=(
            Link("Source", TOWEL_REPO_URL),
            Link("PyPI: code-towel", "https://pypi.org/project/code-towel/"),
        ),
        media=Video(
            file="towel-preview.mp4",
            poster="towel-preview.jpg",
            transcript="towel-preview.txt",
            label=(
                "A terminal recording. Two Python functions repeat the same five lines, "
                "differing in one number. Towel's preview replaces both copies with calls "
                "to one new helper, which takes that number as a parameter."
            ),
            caption=(
                "Towel previewing a refactoring of a 16-line file. Half a minute, silent. "
                "The output and the wait are those of a real run; the highlights and "
                "captions are added."
            ),
            width=1280,
            height=800,
        ),
    ),
    Project(
        slug="fortress",
        name="Project Fortress",
        tagline="A programming language for high-performance computing",
        context="Sun Labs, 2003–2011",
        paragraphs=(
            (
                "Project Fortress was an initiative at Sun Labs, sponsored by DARPA "
                "HPCS, to develop a next-generation high-performance programming "
                "language. Fortress was designed to enable programming at the "
                "peta-scale: petaflops of compute and petabytes of memory, orders of "
                "magnitude beyond the fastest computer in the world at the start of "
                "the project. I joined the team at the start and had the honor of "
                "working with many outstanding researchers, including ",
                Link("Guy L. Steele Jr.", "https://en.wikipedia.org/wiki/Guy_L._Steele_Jr."),
                ", a longtime hero of mine, and Steve Heller, with whom I worked for "
                "almost two decades at Sun Labs and Two Sigma.",
            ),
            (
                "Originally we referred to the language as “secure Fortran,” "
                "even though, semantically and syntactically, it was nothing like "
                "Fortran. The name Fortress came to me in the middle of the night as "
                "a pun on that phrase; I was so amused with myself that I had to get "
                "up and write it down. I suggested it to the team as an internal "
                "codename, and the name stuck.",
            ),
            (
                "Fortress was an open source project, and a significant amount of "
                "technology was released over its lifetime. I keep a repository of "
                "the published material: source code, supporting documents, and "
                "tools.",
            ),
        ),
        links=(
            Link("Source and documents", "https://github.com/ericeallen/Fortress"),
            Link(
                "Language specification (1.0 β)",
                "http://web.cs.ucla.edu/~palsberg/course/cs239/papers/fortress1.0beta.pdf",
            ),
        ),
        media=Figure(
            file="fortress-team.jpg",
            alt="Fifteen members of the Fortress team, in two rows, outdoors, wearing matching rust-colored polo shirts.",
            caption=(
                "Many, but unfortunately not all, of the key contributors to Fortress, "
                "including several summer interns who have since gone on to do great research."
            ),
            width=604,
            height=254,
        ),
    ),
    Project(
        slug="drjava",
        name="DrJava",
        tagline="A lightweight pedagogic environment for Java",
        context="Rice University",
        paragraphs=(
            (
                "DrJava is a lightweight development environment for Java, built for "
                "teaching. My PhD advisor, Robert Cartwright, ",
                Link("Brian Stoler", "https://www.linkedin.com/in/brianstoler"),
                ", and I designed it at Rice, taking its pedagogic approach from ",
                Link("Racket", "https://racket-lang.org"),
                ". Its interactions pane is a metacircular interpreter that calls out "
                "to JVM primitives, so Java code can be evaluated as it is written, "
                "with every Java library at hand. We released it as open source and, "
                "with ",
                Link("Charlie Reis", "https://www.linkedin.com/in/charliereis"),
                ", continued its development through a Rice course in production programming.",
            ),
        ),
        links=(
            Link("Project page at Rice", "https://www.cs.rice.edu/~javaplt/drjava/"),
            Link("Paper (SIGCSE 2002)", doi("10.1145/563517.563395")),
            Link("Course paper (SIGCSE 2003)", doi("10.1145/611892.611940")),
        ),
    ),
)

FEATURED_PROJECTS: Final[tuple[str, ...]] = ("lambda-s", "towel")
"""Slugs of the projects listed under "Current work" on the home page."""

SOFTWARE_INTRO: Final[Prose] = (
    "Much of what I have built has been proprietary. These are the open source "
    "projects: two current, two historical.",
)


# ---------------------------------------------------------------------------
# Publications
# ---------------------------------------------------------------------------

_P = PublicationKind

PUBLICATIONS: Final[tuple[Publication, ...]] = (
    # Papers
    Publication(
        _P.PAPER,
        (ME,),
        "A Calculus for Units of Measure with Conversion",
        "arXiv:2609.38242 [cs.PL]",
        "2026",
        LAMBDA_S_PAPER_URL,
        links=(Link("Lean 4 artifact", LAMBDA_S_REPO_URL),),
    ),
    Publication(
        _P.PAPER,
        (ME,),
        "Neural Networks and Denotation",
        "arXiv:2103.08315 [cs.LG]",
        "2021",
        "https://arxiv.org/abs/2103.08315",
    ),
    Publication(
        _P.PAPER,
        (
            ME,
            "Justin Hilburn",
            "Scott Kilpatrick",
            "Victor Luchangco",
            "Sukyoung Ryu",
            "David Chase",
            "Guy L. Steele Jr.",
        ),
        "Type Checking Modular Multiple Dispatch with Parametric Polymorphism and Multiple Inheritance",
        "OOPSLA 2011, pp. 973–992",
        "2011",
        doi("10.1145/2076021.2048140"),
    ),
    Publication(
        _P.PAPER,
        (ME, "Ryan Culpepper", "Janus Dam Nielsen", "Jon Rafkind", "Sukyoung Ryu"),
        "Growing a Syntax",
        "Workshop on Foundations of Object-Oriented Languages (FOOL) 2009",
        "2009",
        "https://www.semanticscholar.org/paper/Growing-a-Syntax-Allen-Culpepper/999d16350bf1446aa0d0d9cdb557f449ea347ebf",
    ),
    Publication(
        _P.PAPER,
        (
            ME,
            "M. W. Bailey",
            "Ras Bodik",
            "Kim Bruce",
            "Kathleen Fisher",
            "Stephen Freund",
            "Robert Harper",
            "Chandra Krintz",
            "Shriram Krishnamurthi",
            "Jim Larus",
            "Doug Lea",
            "Gary Leavens",
            "Lori Pollock",
            "Stuart Reges",
            "Martin Rinard",
            "Mark Sheldon",
            "Franklyn Turbak",
            "Mitchell Wand",
        ),
        "2008 SIGPLAN Programming Language Curriculum Workshop: Discussion Summaries and Recommendations",
        "ACM SIGPLAN Notices 43(11), pp. 6–29",
        "2008",
        doi("10.1145/1480828.1480831"),
    ),
    Publication(
        _P.PAPER,
        (ME,),
        "Some Things That Computer Science Majors Should Know",
        "ACM SIGPLAN Notices 43(11), pp. 32–35",
        "2008",
        doi("10.1145/1480828.1480834"),
    ),
    Publication(
        _P.PAPER,
        (ME, "Joseph J. Hallett", "Victor Luchangco", "Sukyoung Ryu", "Guy L. Steele Jr."),
        "Modular Multiple Dispatch with Multiple Inheritance",
        "ACM Symposium on Applied Computing (SAC) 2007, pp. 1117–1121",
        "2007",
        doi("10.1145/1244002.1244245"),
    ),
    Publication(
        _P.PAPER,
        (ME, "Robert Cartwright"),
        "Safe Instantiation in Generic Java",
        "Science of Computer Programming 59(1–2), pp. 26–37",
        "2006",
        doi("10.1016/j.scico.2005.07.003"),
        links=(Link("PDF", "https://www.cs.rice.edu/~javaplt/papers/pppj2004.pdf"),),
    ),
    Publication(
        _P.PAPER,
        ("Sam Tobin-Hochstadt", ME),
        "A Core Calculus of Metaclasses",
        "Workshop on Foundations of Object-Oriented Languages (FOOL) 2005",
        "2005",
        "https://homes.luddy.indiana.edu/samth/fool05-tha.pdf",
    ),
    Publication(
        _P.PAPER,
        (ME, "David Chase", "Victor Luchangco", "Jan-Willem Maessen", "Guy L. Steele Jr."),
        "Object-Oriented Units of Measurement",
        "OOPSLA 2004, pp. 384–403",
        "2004",
        doi("10.1145/1035292.1029008"),
    ),
    Publication(
        _P.PAPER,
        (ME, "Jonathan Bannet", "Robert Cartwright"),
        "A First-Class Approach to Genericity",
        "OOPSLA 2003, pp. 96–114",
        "2003",
        doi("10.1145/949305.949316"),
        note="Best Student Paper",
    ),
    Publication(
        _P.PAPER,
        (ME, "Robert Cartwright", "Charles Reis"),
        "Production Programming in the Classroom",
        "SIGCSE 2003, pp. 89–93",
        "2003",
        doi("10.1145/611892.611940"),
        links=(Link("PDF", "https://www.cs.rice.edu/~javaplt/drjava/papers/production-programming.pdf"),),
    ),
    Publication(
        _P.PAPER,
        (ME, "Robert Cartwright", "Brian Stoler"),
        "Efficient Implementation of Run-Time Generic Types for Java",
        "Generic Programming, Springer, pp. 207–236",
        "2003",
        doi("10.1007/978-0-387-35672-3_11"),
    ),
    Publication(
        _P.PAPER,
        (ME, "Robert Cartwright", "Brian Stoler"),
        "DrJava: A Lightweight Pedagogic Environment for Java",
        "SIGCSE 2002, pp. 137–141",
        "2002",
        doi("10.1145/563517.563395"),
    ),
    # Books and theses
    Publication(
        _P.BOOK,
        (
            ME,
            "David Chase",
            "Joe Hallett",
            "Victor Luchangco",
            "Jan-Willem Maessen",
            "Sukyoung Ryu",
            "Guy L. Steele Jr.",
            "Sam Tobin-Hochstadt",
        ),
        "The Fortress Language Specification, Version 1.0 β",
        "Sun Microsystems",
        "2007",
        "http://web.cs.ucla.edu/~palsberg/course/cs239/papers/fortress1.0beta.pdf",
    ),
    Publication(
        _P.BOOK,
        (ME,),
        "A First-Class Approach to Genericity",
        "PhD thesis, Rice University",
        "2003",
        "https://repository.rice.edu/items/66eafe10-80ae-4723-9525-dcf3fc95f6e1",
    ),
    Publication(
        _P.BOOK,
        (ME,),
        "Bug Patterns in Java",
        "Apress",
        "2002",
        "https://www.amazon.com/dp/1590590619",
    ),
    # Technical reports
    Publication(
        _P.REPORT,
        (ME, "Joe Hallett"),
        "Universal Quantification in Class Definitions",
        "Research Disclosure 522, pp. 997–999",
        "2007",
    ),
    Publication(
        _P.REPORT,
        (ME, "Victor Luchangco"),
        "Syntax Expansion: Embedding One Language into Another",
        "Research Disclosure 508, p. 967",
        "2006",
    ),
    Publication(
        _P.REPORT,
        (ME, "Ken Kennedy", "Cheryl McCosh"),
        "Object-Oriented Type Inference for Telescoping Languages",
        "Technical report, Rice University",
        "2004",
        "https://hdl.handle.net/1911/96332",
    ),
    Publication(
        _P.REPORT,
        (ME, "Ken Kennedy", "Cheryl McCosh", "et al."),
        "Static Type Inference for Specialization in a Telescoping Compiler",
        "Technical report, Rice University",
        "2004",
        "https://hdl.handle.net/1911/96330",
    ),
    Publication(
        _P.REPORT,
        (ME, "Jonathan Bannet", "Robert Cartwright"),
        "Mixins in Generic Java Are Sound",
        "Technical report, Rice University",
        "2003",
        "https://www.cs.rice.edu/CS/PLT/Publications/Java/tr200301.pdf",
    ),
    Publication(
        _P.REPORT,
        (ME,),
        "NextGen Developer’s Guide",
        "Rice University",
        "2003",
        "https://www.cs.rice.edu/~javaplt/nextgen/doc/developer.pdf",
    ),
    Publication(
        _P.REPORT,
        (ME,),
        "First-Class Genericity for Object-Oriented Languages with Nominal Type Equivalence",
        "PhD thesis proposal, Rice University",
        "2003",
        "https://www.cs.rice.edu/~javaplt/papers/eric-phd-proposal.pdf",
    ),
    # Articles
    Publication(
        _P.ARTICLE,
        (ME, "Brendan McCord", "Rafael Tena"),
        "Research Highlights from an Unprecedented Year at NeurIPS, Part 2",
        "Acrisure Technology Group",
        "2021",
        "https://medium.com/acrisure-technology-group/research-highlights-from-an-unprecedented-year-at-neurips-the-worlds-most-watched-ai-conference-c6d2d9968a82",
    ),
    Publication(
        _P.ARTICLE,
        (ME, "Brendan McCord", "Rafael Tena"),
        "Research Highlights from an Unprecedented Year at NeurIPS, Part 1",
        "Acrisure Technology Group",
        "2021",
        "https://medium.com/acrisure-technology-group/research-highlights-from-an-unprecedented-year-at-neurips-the-worlds-most-watched-ai-conference-7bac6ece2a43",
    ),
    Publication(
        _P.ARTICLE,
        (ME, "Rafael Tena"),
        "Our Take on CVPR 2020",
        "Tulco Labs",
        "2020",
        "https://medium.com/tulcolabs/our-take-on-cvpr-2020-1ed249089110",
    ),
    Publication(
        _P.ARTICLE,
        (ME, "Rafael Tena"),
        "Our Favorite Papers from ICLR 2020",
        "Tulco Labs",
        "2020",
        "https://medium.com/tulcolabs/our-favorite-papers-from-iclr-2020-7b7d5791f487",
    ),
    Publication(
        _P.ARTICLE,
        (ME, "Firdaus Janoos"),
        "25 of Our Favorite Papers, Talks, Presentations, and Workshops from NIPS 2017",
        "Two Sigma",
        "2018",
        "https://www.twosigma.com/articles/25-of-our-favorite-papers-talks-presentations-and-workshops-from-nips-2017/",
    ),
    Publication(
        _P.ARTICLE,
        ("Carlyn Chatfield",),
        "An Interview with Eric Allen",
        "Rice University Computer Science",
        "2017",
        "https://csprofiles.rice.edu/2017/10/23/allen/",
    ),
    Publication(
        _P.ARTICLE,
        (
            ME,
            "David Chase",
            "Christine Flood",
            "Victor Luchangco",
            "Jan-Willem Maessen",
            "Sukyoung Ryu",
            "Guy L. Steele Jr.",
        ),
        "Project Fortress: A Multicore Language for Multicore Processors",
        "Linux Magazine",
        "2007",
    ),
    Publication(
        _P.ARTICLE,
        (ME,),
        "Diagnosing Java Code",
        "IBM developerWorks, a regular column later consolidated in Bug Patterns in Java",
        "2000–2003",
    ),
    Publication(
        _P.ARTICLE,
        (ME,),
        "The Power of Parametric Polymorphism",
        "JavaWorld",
        "2000",
        "https://www.infoworld.com/article/2162801/behold-the-power-of-parametric-polymorphism.html",
    ),
)

SELECTED_TITLES: Final[tuple[str, ...]] = (
    "A Calculus for Units of Measure with Conversion",
    "Neural Networks and Denotation",
    "Type Checking Modular Multiple Dispatch with Parametric Polymorphism and Multiple Inheritance",
    "Object-Oriented Units of Measurement",
    "A First-Class Approach to Genericity",
)
"""Titles shown on the home page, in this order. Each must name a PAPER above."""


# ---------------------------------------------------------------------------
# CV
# ---------------------------------------------------------------------------

EXPERIENCE: Final[tuple[Employer, ...]] = (
    Employer(
        "Two Sigma",
        (
            Role(
                "Senior Vice President, Quantitative Engineer",
                2025,
                None,
                ("AI Innovation Team.",),
            ),
        ),
    ),
    Employer(
        "Allen Research",
        (
            Role(
                "Founder",
                2023,
                2025,
                ("Independent research in generative AI and knowledge representation.",),
            ),
        ),
    ),
    Employer(
        "Acrisure Capital",
        (
            Role(
                "Chief Scientist",
                2021,
                2023,
                (
                    "A small team of engineers and scientists in Austin, building a "
                    "quantitative investment firm from the ground up.",
                ),
            ),
        ),
    ),
    Employer(
        "Acrisure Technology Group",
        (
            Role(
                "Chief Technology Officer",
                2019,
                2021,
                ("The technology arm of Acrisure: engineering, product, and AI research teams.",),
            ),
        ),
    ),
    Employer(
        "Tulco Labs",
        (
            Role(
                "Chief Technology Officer",
                2019,
                2020,
                (
                    "The technology arm of Tulco Holdings, applying AI to accelerate "
                    "the growth of a portfolio of companies that included FIGS, "
                    "Edgeworth, Road Runner, and the Tulco-initiated startups Altway "
                    "Insurance and BlueNote AI. Acrisure acquired Altway, BlueNote, "
                    "and other Tulco assets in August 2019.",
                ),
            ),
        ),
    ),
    Employer(
        "Altway Insurance",
        (
            Role(
                "Chief Technology Officer",
                2019,
                2020,
                (
                    "Employee #1 and CTO of a joint venture of Tulco Holdings and "
                    "Acrisure, founded to apply artificial intelligence to insurance "
                    "distribution. Active users grew 10% week over week for 35 weeks "
                    "before Acrisure acquired the company outright.",
                ),
            ),
        ),
    ),
    Employer(
        "BlueNote AI",
        (
            Role(
                "Chief Technology Officer",
                2019,
                2020,
                (
                    "Employee #1 and CTO of a startup founded by Tulco Holdings. "
                    "Where Altway applied AI to insurance distribution, BlueNote "
                    "applied predictive modeling to the carrier side. Acquired by "
                    "Acrisure along with Altway and parts of Tulco Labs.",
                ),
            ),
        ),
    ),
    Employer(
        "Two Sigma",
        (
            Role(
                "Senior Vice President, Artificial Intelligence Researcher",
                2017,
                2019,
                (
                    "Senior researcher on the newly formed AI Core Team, working on "
                    "deep reinforcement learning and its application to finance.",
                ),
            ),
            Role(
                "Vice President, Head of Houston Data Engineering",
                2015,
                2017,
                (
                    "Led an organization of roughly 40 engineers in five teams, "
                    "working on predictive modeling, distributed computing, data "
                    "ingestion, and anomaly detection.",
                ),
            ),
            Role(
                "Engineering Manager, Analytics and Alpha Capture",
                2014,
                2015,
                (
                    "Built and managed a new team in the Houston office that "
                    "collected and maintained alpha capture data and applied machine "
                    "learning and predictive modeling to it.",
                ),
            ),
        ),
    ),
    Employer(
        "RetailMeNot",
        (
            Role(
                "Lead Data Scientist",
                2013,
                2014,
                (
                    "Managed the data science team and set its direction, applying "
                    "machine learning, natural language processing, and statistical "
                    "analysis to large datasets.",
                ),
            ),
        ),
    ),
    Employer(
        "Bazaarvoice",
        (
            Role(
                "Engineering Manager, Data Science",
                2011,
                2013,
                (
                    "Founded and led the company's first data science team, which "
                    "used machine learning and natural language processing to "
                    "analyze unstructured data and delivered the results in "
                    "high-volume, low-latency web services for online advertising.",
                ),
            ),
        ),
    ),
    Employer(
        "Sun Microsystems",
        (
            Role(
                "Principal Engineer",
                2003,
                2011,
                (
                    "Directed ",
                    Link("Project Fortress", "/software/#fortress"),
                    ", an open source project of Sun Labs to develop a "
                    "next-generation language for high-performance computing, as part "
                    "of the DARPA HPCS program.",
                ),
            ),
        ),
    ),
    Employer(
        "Cycorp",
        (
            Role(
                "Software Engineer",
                2000,
                2001,
                (
                    "Built a word-sense disambiguation engine based on concept "
                    "proximity in the Cyc knowledge graph, and a JVM-based blackboard "
                    "interface for remote access to the Cyc system.",
                ),
            ),
        ),
    ),
    Employer(
        "Cornell University",
        (
            Role(
                "Undergraduate Research Assistant",
                1995,
                1996,
                (
                    "Programmer and research assistant in Claire Cardie's Natural "
                    "Language Processing Research Group. Built tools that identify "
                    "citations in unstructured text and link them to the references.",
                ),
            ),
        ),
    ),
)

TEACHING: Final[tuple[Employer, ...]] = (
    Employer(
        "Rice University",
        (
            Role(
                "Adjunct Professor of Computer Science",
                2014,
                2016,
                (
                    "Taught functional programming and parallel and distributed "
                    "computing. The functional programming curriculum drew on ",
                    Link(
                        "How to Design Programs",
                        "https://en.wikipedia.org/wiki/How_to_Design_Programs",
                    ),
                    ", ",
                    Link(
                        "Structure and Interpretation of Computer Programs",
                        "https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book.html",
                    ),
                    ", and Martin Odersky's Coursera course ",
                    Link(
                        "Functional Programming Principles in Scala",
                        "https://www.coursera.org/learn/scala-functional-programming",
                    ),
                    ".",
                ),
            ),
        ),
    ),
    Employer(
        "The University of Texas at Austin",
        (
            Role(
                "Adjunct Professor of Computer Science",
                2008,
                2009,
                (
                    "Taught honors and graduate courses on operational semantics and "
                    "type systems, roughly following Benjamin Pierce's ",
                    Link(
                        "Types and Programming Languages",
                        "https://www.cis.upenn.edu/~bcpierce/tapl/",
                    ),
                    ". Member of the SIGPLAN-sponsored Curriculum Workshop on "
                    "Programming Language Education.",
                ),
            ),
        ),
    ),
)

EDUCATION: Final[tuple[Degree, ...]] = (
    Degree(
        "Rice University",
        "PhD, Computer Science",
        1997,
        2003,
        (
            "Advisor: Robert Cartwright. Thesis: ",
            Link(
                "A First-Class Approach to Genericity",
                "https://repository.rice.edu/items/66eafe10-80ae-4723-9525-dcf3fc95f6e1",
            ),
            ". The paper of the same name won Best Student Paper at OOPSLA 2003.",
        ),
    ),
    Degree(
        "The University of Texas at Austin",
        "Master of Business Administration",
        2009,
        2011,
        ("Executive MBA program, Red McCombs School of Business.",),
    ),
    Degree(
        "Cornell University",
        "Bachelor's degrees in Mathematics and in Computer Science",
        1993,
        1996,
        ("Cornell College Scholar. Concentration in cognitive studies.",),
    ),
)

PATENTS: Final[tuple[Patent, ...]] = (
    Patent(
        "US 9,342,794",
        "Non-Linear Classification of Text Samples",
        (ME, "Daniel Mahler", "Milos Curcic", "Eric Scott"),
        2016,
        "https://patents.google.com/patent/US9342794B2",
    ),
    Patent(
        "US 8,898,632",
        "Dispatch Predicate for Overloaded Functions Using Type Intervals",
        (
            "Karl B. Naden",
            "Justin R. Hilburn",
            "David R. Chase",
            "Guy L. Steele Jr.",
            "Victor M. Luchangco",
            ME,
        ),
        2014,
        "https://patents.google.com/patent/US8898632B2",
    ),
    Patent(
        "US 8,225,294",
        "Method and Apparatus for Expressing and Checking Relationships Between Types",
        (ME, "Sukyoung Ryu", "Victor Luchangco", "Joe Hallett", "Sam Tobin-Hochstadt"),
        2012,
        "https://patents.google.com/patent/US8225294B2",
    ),
    Patent(
        "US 7,530,051",
        "Method and Apparatus for Dimensional Analysis Encoded in Metatypes and Generics",
        (ME, "Guy L. Steele Jr.", "David Chase", "Victor Luchangco", "Jan-Willem Maessen"),
        2009,
        "https://patents.google.com/patent/US7530051B1",
    ),
)

AWARDS: Final[tuple[Award, ...]] = (
    Award(
        "First Place, New Venture Creation Business Plan Competition",
        2010,
        "Red McCombs School of Business, UT Austin. With Nathan Baumeister and Zaz Floreani.",
    ),
    Award(
        "Best Student Paper",
        2003,
        "OOPSLA 2003, the 18th ACM SIGPLAN Conference on Object-Oriented Programming, "
        "Systems, Languages, and Applications.",
    ),
)


# ---------------------------------------------------------------------------
# Talks
# ---------------------------------------------------------------------------

TALKS: Final[tuple[Talk, ...]] = (
    Talk(
        "Fortress and Object-Oriented Programming",
        "FOOL/WOOD 2007",
        "Nice, France",
        "January 20, 2007",
        "https://web.archive.org/web/20080422081142/http://foolwood07.cs.uchicago.edu:80/",
        note="Keynote",
    ),
    Talk(
        "Encapsulated Upgradable Components",
        "IBM Programming Languages Day",
        "Hawthorne, New York",
        "April 22, 2005",
    ),
    Talk(
        "Object-Oriented Units of Measurement",
        "OOPSLA 2004",
        "Vancouver, British Columbia",
        "October 28, 2004",
        "https://web.archive.org/web/20080318151108/http://www.oopsla.org/2004",
    ),
)

SLIDE_DECKS: Final[tuple[SlideDeck, ...]] = (
    SlideDeck(
        "Learning to Win at Peg Solitaire Without Human Knowledge",
        "peg-solitaire-without-human-knowledge.pdf",
        2018,
        73,
        "Applies the method of AlphaGo Zero to a one-player game.",
    ),
    SlideDeck(
        "Mastering the Game of Go Without Human Knowledge",
        "alphago-zero-paper-review.pdf",
        2018,
        39,
        "A review of the AlphaGo Zero paper of Silver et al. (Nature, 2017).",
    ),
    SlideDeck(
        "Implementing a Deep Learning Library from Scratch",
        "deep-learning-library-from-scratch.pdf",
        2017,
        43,
        "Builds a small deep learning library from first principles, using MNIST as the running example.",
    ),
    SlideDeck(
        "Sentiment Analysis of Summaries",
        "sentiment-analysis-of-summaries.pdf",
        2014,
        15,
        "Using a sentiment analysis engine to select summary sentences from online reviews.",
    ),
)

COURSES: Final[tuple[Course, ...]] = (
    Course(
        "COMP 311",
        "Functional Programming",
        "Rice University",
        "Fall 2015 and Fall 2016",
        ("Taught with Robert Cartwright and Sağnak Taşırlar.",),
        "https://web.archive.org/web/20170602230548/https://wiki.rice.edu/confluence/display/PARPROG/COMP311",
    ),
    Course(
        "COMP 322",
        "Fundamentals of Parallel Programming",
        "Rice University",
        "Spring 2016",
        ("Taught with Vivek Sarkar.",),
        "https://web.archive.org/web/20160805031517/https://wiki.rice.edu/confluence/display/PARPROG/COMP322",
    ),
)
