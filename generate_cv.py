#!/usr/bin/env python3
"""Generate Julian Henry CV PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

OUTPUT = "Julian Henry CV.pdf"
PAGE_W, PAGE_H = letter

LEFT = 0.55 * inch
RIGHT = 0.55 * inch
TOP = 0.4 * inch
BOTTOM = 0.4 * inch
CONTENT_W = PAGE_W - LEFT - RIGHT

# Professional blue accents
ACCENT = HexColor("#1B4F8A")
LINK = HexColor("#1565C0")
RULE = HexColor("#1B4F8A")
RULE_SOFT = HexColor("#9BB4D0")
LINK_HEX = "1565C0"
ACCENT_HEX = "1B4F8A"


def href(url, text):
    """Blue underlined clickable link."""
    return (
        f'<font color="#{LINK_HEX}"><u><link href="{url}">{text}</link></u></font>'
    )


def accent(text):
    """Bold blue highlight (non-link)."""
    return f'<font color="#{ACCENT_HEX}"><b>{text}</b></font>'


def styles():
    return {
        "name": ParagraphStyle(
            "Name",
            fontName="Times-Bold",
            fontSize=20,
            leading=22,
            alignment=TA_CENTER,
            textColor=ACCENT,
            spaceAfter=2,
        ),
        "contact_line": ParagraphStyle(
            "ContactLine",
            fontName="Times-Roman",
            fontSize=9,
            leading=11,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "section": ParagraphStyle(
            "Section",
            fontName="Times-Bold",
            fontSize=10.5,
            leading=12,
            alignment=TA_CENTER,
            textColor=ACCENT,
            spaceBefore=5,
            spaceAfter=0.5,
        ),
        "role": ParagraphStyle(
            "Role",
            fontName="Times-Bold",
            fontSize=10,
            leading=12,
            alignment=TA_LEFT,
            textColor=ACCENT,
        ),
        "dates": ParagraphStyle(
            "Dates",
            fontName="Times-Bold",
            fontSize=10,
            leading=12,
            alignment=TA_RIGHT,
        ),
        "org": ParagraphStyle(
            "Org",
            fontName="Times-Italic",
            fontSize=9,
            leading=11,
            alignment=TA_LEFT,
            spaceAfter=1,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontName="Times-Roman",
            fontSize=9,
            leading=10.8,
            alignment=TA_LEFT,
            leftIndent=10,
            firstLineIndent=-8,
            spaceBefore=0.5,
            spaceAfter=0.5,
        ),
        "skill": ParagraphStyle(
            "Skill",
            fontName="Times-Roman",
            fontSize=9,
            leading=10.8,
            alignment=TA_LEFT,
            spaceBefore=0.5,
            spaceAfter=0.5,
        ),
        "edu": ParagraphStyle(
            "Edu",
            fontName="Times-Bold",
            fontSize=10,
            leading=12,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=1,
        ),
        "cert": ParagraphStyle(
            "Cert",
            fontName="Times-Roman",
            fontSize=9,
            leading=11,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
        ),
        "portfolio_h": ParagraphStyle(
            "PortfolioH",
            fontName="Times-Bold",
            fontSize=10,
            leading=12,
            alignment=TA_LEFT,
            textColor=ACCENT,
            spaceBefore=0,
            spaceAfter=1,
        ),
    }


def section_rule():
    return HRFlowable(
        width="100%",
        thickness=0.9,
        color=RULE,
        spaceBefore=0,
        spaceAfter=2.5,
    )


def job_block(s, role, org, location, dates, employment, items):
    top = Table(
        [[Paragraph(role, s["role"]), Paragraph(dates, s["dates"])]],
        colWidths=[CONTENT_W * 0.62, CONTENT_W * 0.38],
    )
    top.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    org_line = Paragraph(f"{org} — {location} · {employment}", s["org"])
    require_clean_bullets(s, items)
    body = [top, org_line] + [bullet(s, item) for item in items]
    body.append(Spacer(1, 2.5))
    return KeepTogether(body)


def bullet(s, item):
    return Paragraph(f'<font size="6.5" color="#{ACCENT_HEX}">•</font>&nbsp;&nbsp;{item}', s["bullet"])


def require_clean_bullets(s, items):
    for item in items:
        p = bullet(s, item)
        _, h = p.wrap(CONTENT_W, 1000)
        soft_lines = max(1, int(round(h / s["bullet"].leading)))
        explicit = item.lower().count("<br")
        if explicit:
            if explicit > 1:
                raise SystemExit(f"Bullet has >2 explicit lines:\n  {item}")
            parts = item.replace("<br />", "<br/>").split("<br/>")
            for part in parts:
                q = bullet(s, part.strip())
                _, ph = q.wrap(CONTENT_W, 1000)
                if int(round(ph / s["bullet"].leading)) > 1:
                    raise SystemExit(f"Bullet <br/> segment still wraps:\n  {part}")
        elif soft_lines > 1:
            raise SystemExit(
                f"Bullet soft-wraps to {soft_lines} lines — shorten or insert <br/>:\n  {item}"
            )


def build():
    s = styles()
    story = []

    story.append(Paragraph("Julian Henry", s["name"]))
    story.append(
        Paragraph(
            "Houston, TX USA  ·  (346) 237-6315  ·  "
            f'{href("mailto:juliantx@naver.com", "juliantx@naver.com")}  ·  '
            f'{href("https://github.com/juleshenry", "github.com/juleshenry")}',
            s["contact_line"],
        )
    )
    story.append(Spacer(1, 2))
    story.append(
        HRFlowable(
            width="100%",
            thickness=1.35,
            color=ACCENT,
            spaceBefore=0,
            spaceAfter=1.5,
        )
    )
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.4,
            color=RULE_SOFT,
            spaceBefore=0,
            spaceAfter=2,
        )
    )

    # --- Work Experience ---
    story.append(Paragraph("Work Experience", s["section"]))
    story.append(section_rule())

    story.append(
        job_block(
            s,
            "Senior Full-Stack Engineer",
            "Macquarie Financial Ltd.",
            "Houston, TX",
            "October 2024 – Present",
            "Full-time",
            [
                "Deploy and operate Java servlet services powering high-priority trading workflows<br/>across globally distributed infrastructure in London, São Paulo, and Sydney.",
                "Translate as-dealt deal logic from C++ to Python for ASIC regulatory reporting,<br/>enabling auditable trade exposition and compliance-ready deal state.",
                "Co-author a shared library that adds standardized risk and workflow controls<br/>to trades across 100+ commodities and financial products.",
                "Deliver C++17 enhancements inside a 1M+ line enterprise trading platform,<br/>hardening low-latency, high-availability commodities and markets systems.",
            ],
        )
    )

    story.append(
        job_block(
            s,
            "Software Engineer",
            "Allis-Gleaner Corporation (AGCO)",
            "Atlanta, GA",
            "May 2023 – October 2024",
            "Full-time",
            [
                "Hardened AWS Kafka-based IoT telemetry infrastructure serving a connected<br/>agriculture fleet across 140 countries with improved real-time reliability.",
                "Engineered RESTful APIs for hardware device orchestration that accelerated<br/>integration test cycles by 500%+ across connected farm equipment.",
                "Shipped Angular features for the Fendt.One precision agriculture platform<br/>supporting 10,000+ remote farm operations worldwide.",
            ],
        )
    )

    story.append(
        job_block(
            s,
            "Data Engineer",
            "SimSpace Corporation",
            "Boston, MA",
            "August 2020 – August 2022",
            "Full-time",
            [
                "Evaluated ML-based threat detection models through adversarial red-team<br/>simulations, surfacing failure modes before production exposure.",
                "Built cybersecurity analytics pipelines with NLP that improved threat<br/>detection rates by 72% across enterprise security workloads.",
                "Led performance optimization of a 30,000+ line Python/Pandas ETL pipeline,<br/>delivering 10× throughput gains for cybersecurity data processing.",
            ],
        )
    )

    story.append(
        job_block(
            s,
            "Assets &amp; Liabilities Intern",
            "Transamerica Corporation",
            "Baltimore, MD",
            "June 2019 – May 2020",
            "Internship → part-time",
            [
                "Validated actuarial risk models for variable annuity portfolios using<br/>NumPy, scikit-learn, and pandas across large-scale simulation runs.",
                "Achieved 99.7% simulation accuracy for reconciliation and stress testing<br/>on a $6B+ AUM variable annuity book.",
            ],
        )
    )

    # --- Technical Skills ---
    story.append(Paragraph("Technical Skills", s["section"]))
    story.append(section_rule())
    for line in [
        f'{accent("Languages:")} C++17, Python, Java, TypeScript, JavaScript, SQL, Julia, Rust, WebAssembly',
        f'{accent("Frontend:")} React, Next.js, Angular, HTML5, CSS3',
        f'{accent("Backend:")} Spring Boot, Node.js, Express, REST APIs, Java Servlets',
        f'{accent("Cloud / Infra:")} AWS, Kafka, Docker, Linux, GitHub Actions, CI/CD, Cloudflare',
        f'{accent("Databases:")} PostgreSQL, MongoDB, DynamoDB, Neo4j, SurrealDB, SQLite, FAISS, Vector DBs',
        f'{accent("Data / ML:")} Pandas, NumPy, scikit-learn, TensorFlow, PySpark, RAG, Tableau',
    ]:
        story.append(Paragraph(line, s["skill"]))

    # --- Education ---
    story.append(Paragraph("Education &amp; Certificates", s["section"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            f'{accent("Bachelor’s of Applied Science in Computer Science")}, University of Pennsylvania',
            s["edu"],
        )
    )
    edu_bullets = [
        "Vice President, Artificial Intelligence Society; undergraduate thesis on differential privacy under Rajeev Alur, with distinction",
        f'{accent("DELE B2")} (Instituto Cervantes) — official upper-intermediate Spanish language credential',
    ]
    require_clean_bullets(s, edu_bullets)
    story.extend([bullet(s, item) for item in edu_bullets])

    # --- Open Source & Portfolio ---
    story.append(Paragraph("Open Source &amp; Portfolio", s["section"]))
    story.append(section_rule())
    portfolio_bullets = [
        f'{href("https://1wg.ai", "1wg.ai")} — AI-powered global news gazette using RAG over a vector database<br/>'
        "for retrieval-augmented journalism across world events.",
        f'{href("https://glottosphere.com", "glottosphere.com")} — multilingual dictionary spanning 200+ languages,<br/>'
        "powered by FAISS similarity search and a custom binary lexicon engine.",
        f'{href("https://github.com/juleshenry/ghee", "ghee")} — 616+ fuzzy-searchable shell shortcuts published to PyPI;<br/>'
        f'{href("https://github.com/juleshenry/tatuagem", "tatuagem")} — ASCII code-signature suite; '
        f'{href("https://github.com/juleshenry/readme_rosetta", "readme-rosetta")} — Ollama-powered README translation.',
        f'{href("https://github.com/juleshenry/intersekt", "intersekt")} — WebAssembly Karatsuba vs JS BigInt, demonstrating O(N^1.58) vs schoolbook multiply.',
        f'{href("https://github.com/juleshenry/quantum-plankton-ml", "quantum-plankton-ml")} — quantum machine learning on plankton imagery across architectures.',
        f'{href("https://github.com/juleshenry/laciyo", "laciyo")} — constructed Romance language via simulated annealing (Python prep + Rust optimizer).',
    ]
    require_clean_bullets(s, portfolio_bullets)
    story.extend([bullet(s, item) for item in portfolio_bullets])

    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="Julian Henry CV",
        author="Julian Henry",
    )
    doc.build(story)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
