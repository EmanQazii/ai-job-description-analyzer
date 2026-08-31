"""
SentinelJD — AI Job Description Analyzer — Streamlit frontend.

This file contains ONLY presentation logic. The AI/analysis backend
(src/analyzer.py, src/schemas.py, src/prompts.py) is untouched.

Interface preserved exactly as before:

    from src.analyzer import analyze_job_description
    analysis, overall_score = analyze_job_description(job_description)

    analysis.score_breakdown   -> .clarity / .completeness / .specificity
                                   .professionalism / .inclusivity
    analysis.summary           -> str
    analysis.issues            -> list[.title, .severity, .category,
                                        .explanation, .suggestion]
    analysis.bias_flags        -> list[.phrase, .concern, .alternative]
    analysis.checklist         -> list[.item, .present, .priority, .comment]
    analysis.recommendations   -> list[str]
    analysis.improved_jd       -> str

Field-name fallbacks: a couple of field names shifted during this
refinement (issue.issue -> issue.title, flag.suggested_alternative ->
flag.alternative). Helpers below read either name so this file keeps
working whichever the backend currently returns.

---------------------------------------------------------------------
Layout fix (2026): several sections used to open a raw
`<div class="jda-card">` in one st.markdown() call, render content in
further separate st.markdown()/st.expander()/st.columns() calls, then
close the div in a final st.markdown() call. Streamlit renders every
top-level call as its own isolated DOM node, so the opening <div> was
rendering completely alone (an empty bordered/padded box) and never
actually wrapping the content beneath it — hence the blank white bars.

Fix: every "card" section now uses `with st.container(border=True):`
instead of a hand-rolled div. A Streamlit container is a real DOM node,
so everything written inside the `with` block (markdown, expanders,
columns, components.html, buttons, text areas) is genuinely nested
inside one visual box, no matter how many calls it takes.
---------------------------------------------------------------------
"""

from html import escape
from types import SimpleNamespace

import streamlit as st
import streamlit.components.v1 as components

from src.analyzer import analyze_job_description


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

APP_NAME = "SentinelJD"
APP_TAGLINE = "AI-powered analysis for stronger, more inclusive cybersecurity job descriptions."

# Flip to True to preview/demo the UI without spending Gemini API quota.
# Never enable this in production — it returns a fixed, fake analysis.
DEMO_MODE = False

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
TOP_FINDINGS_COUNT = 3
TOP_RECOMMENDATIONS_COUNT = 5


st.set_page_config(
    page_title=f"{APP_NAME} | AI Job Description Analyzer",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------

def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --color-primary: #1D4ED8;
            --color-primary-dark: #1E3A8A;
            --color-primary-soft: #EFF6FF;
            --color-navy: #0F172A;
            --color-text: #1E293B;
            --color-muted: #64748B;
            --color-border: #E2E8F0;
            --color-card: #FFFFFF;
            --color-page: #FFFFFF;
            --color-good-bg: #F0FDF4;
            --color-good-text: #15803D;
            --color-high-bg: #FEF2F2;
            --color-high-text: #B91C1C;
            --color-medium-bg: #FFFBEB;
            --color-medium-text: #B45309;
            --color-low-bg: #F1F5F9;
            --color-low-text: #334155;
        }

        .main .block-container {
            max-width: 880px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        body, .stApp {
            background: linear-gradient(180deg, #FFFFFF 0%, #F9FAFB 52%, #FFFFFF 100%);
            background-attachment: fixed;
            color: var(--color-text);
        }

        /* Header — brand banner */
        .jda-header {
            display: flex;
            align-items: center;
            gap: 1.1rem;
            background: linear-gradient(135deg, var(--color-navy) 0%, #1E3A8A 55%, #1D4ED8 100%);
            border-radius: 14px;
            padding: 1.6rem 1.9rem;
            margin-bottom: 1.75rem;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.22);
        }
        .jda-brand-icon {
            font-size: 2rem;
            line-height: 1;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            padding: 0.55rem 0.7rem;
            flex-shrink: 0;
        }
        .jda-header h1 {
            font-size: 1.55rem;
            font-weight: 800;
            color: #FFFFFF;
            margin: 0 0 0.3rem 0;
            letter-spacing: -0.01em;
        }
        .jda-header p {
            font-size: 0.92rem;
            color: #BFDBFE;
            margin: 0;
        }

        /* Streamlit native bordered container == our "card".
           Everything rendered inside `with st.container(border=True):`
           lands inside this single real DOM node, so mixed content
           (markdown + expanders + columns + widgets) is genuinely
           wrapped — no more empty divs. */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--color-card) !important;
            border: 1px solid var(--color-border) !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
            margin-bottom: 1.25rem;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
            gap: 0.5rem;
            padding: 1.4rem 1.5rem 1.5rem 1.5rem;
        }

        .jda-section-title {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--color-muted);
            border-left: 3px solid var(--accent, var(--color-primary));
            padding-left: 0.65rem;
            margin-bottom: 0.9rem;
        }
        .jda-section-subtitle {
            font-size: 0.85rem;
            color: var(--color-muted);
            margin-top: -0.5rem;
            margin-bottom: 0.9rem;
        }
        .jda-helper-text {
            font-size: 0.85rem;
            color: var(--color-muted);
            margin-top: -0.4rem;
            margin-bottom: 0.75rem;
        }

        /* Score card */
        .jda-score-card {
            background: linear-gradient(180deg, var(--color-navy) 0%, #1E293B 100%);
            border-radius: 12px;
            padding: 2rem 1.5rem;
            text-align: center;
            margin-bottom: 1.25rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.15);
        }
        .jda-score-label {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #94A3B8;
            margin-bottom: 0.5rem;
        }
        .jda-score-value {
            font-size: 3rem;
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1;
        }
        .jda-score-value span {
            font-size: 1.4rem;
            font-weight: 500;
            color: #94A3B8;
        }
        .jda-score-tag {
            display: inline-block;
            margin-top: 0.9rem;
            padding: 0.3rem 0.9rem;
            border-radius: 999px;
            background: rgba(59, 130, 246, 0.18);
            color: #BFDBFE;
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        /* Quick stats */
        .jda-stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.9rem;
            margin-bottom: 1.25rem;
        }
        @media (max-width: 640px) {
            .jda-stats-grid { grid-template-columns: 1fr; }
        }
        .jda-stat-box {
            background: var(--color-card);
            border: 1px solid var(--color-border);
            border-radius: 10px;
            padding: 1rem 1.1rem;
            text-align: center;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        }
        .jda-stat-value {
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--color-navy);
            line-height: 1.1;
        }
        .jda-stat-value.warn { color: var(--color-high-text); }
        .jda-stat-value.ok { color: var(--color-good-text); }
        .jda-stat-label {
            font-size: 0.8rem;
            color: var(--color-muted);
            margin-top: 0.25rem;
        }

        /* Score breakdown bars */
        .jda-bar-row {
            margin-bottom: 1rem;
        }
        .jda-bar-row:last-child { margin-bottom: 0; }
        .jda-bar-top {
            display: flex;
            justify-content: space-between;
            font-size: 0.88rem;
            margin-bottom: 0.35rem;
        }
        .jda-bar-top .name { font-weight: 600; color: var(--color-text); }
        .jda-bar-top .value { color: var(--color-muted); font-weight: 600; }
        .jda-bar-track {
            width: 100%;
            height: 8px;
            border-radius: 999px;
            background: #E2E8F0;
            overflow: hidden;
        }
        .jda-bar-fill {
            height: 100%;
            border-radius: 999px;
        }

        /* Badges */
        .jda-badge {
            display: inline-block;
            padding: 0.15rem 0.6rem;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }
        .jda-badge-high { background: var(--color-high-bg); color: var(--color-high-text); }
        .jda-badge-medium { background: var(--color-medium-bg); color: var(--color-medium-text); }
        .jda-badge-low { background: var(--color-low-bg); color: var(--color-low-text); }

        /* Finding card (compact) */
        .jda-finding {
            border: 1px solid var(--color-border);
            border-radius: 8px;
            padding: 0.9rem 1.05rem;
            margin-bottom: 0.65rem;
            background: #FBFCFE;
        }
        .jda-finding:last-child { margin-bottom: 0; }
        .jda-finding-title {
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--color-navy);
            margin: 0.35rem 0 0.4rem 0;
        }
        .jda-finding-quote {
            font-size: 0.87rem;
            color: var(--color-muted);
            font-style: italic;
            margin-bottom: 0.4rem;
        }
        .jda-finding-fix {
            font-size: 0.88rem;
            color: var(--color-text);
        }
        .jda-finding-fix b {
            color: var(--color-muted);
            font-weight: 600;
        }

        /* Bias table */
        .jda-bias-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.86rem;
        }
        .jda-bias-table th {
            text-align: left;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            color: var(--color-muted);
            padding: 0.5rem 0.7rem;
            border-bottom: 1px solid var(--color-border);
        }
        .jda-bias-table td {
            padding: 0.6rem 0.7rem;
            border-bottom: 1px solid var(--color-border);
            vertical-align: top;
            color: var(--color-text);
        }
        .jda-bias-table tr:last-child td { border-bottom: none; }
        .jda-bias-table tr:nth-child(even) td { background: #FAFBFF; }
        .jda-bias-phrase {
            font-weight: 600;
            color: var(--color-navy);
            white-space: nowrap;
        }
        .jda-bias-alt {
            color: var(--color-good-text);
            font-weight: 600;
        }

        /* Checklist summary */
        .jda-check-summary-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.9rem;
            margin-bottom: 1.1rem;
        }
        @media (max-width: 640px) {
            .jda-check-summary-grid { grid-template-columns: 1fr; }
        }
        .jda-check-summary-box {
            background: var(--color-primary-soft);
            border-radius: 8px;
            padding: 0.8rem 1rem;
        }
        .jda-check-summary-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            color: var(--color-primary-dark);
            margin-bottom: 0.2rem;
        }
        .jda-check-summary-value {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--color-navy);
        }

        /* Checklist items — compact grid */
        .jda-check-row {
            display: flex;
            align-items: flex-start;
            gap: 0.6rem;
            padding: 0.5rem 0;
        }
        .jda-check-icon {
            flex-shrink: 0;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
            margin-top: 0.1rem;
        }
        .jda-check-icon.present { background: var(--color-good-bg); color: var(--color-good-text); }
        .jda-check-icon.missing { background: var(--color-low-bg); color: var(--color-muted); }
        .jda-check-title {
            font-weight: 600;
            font-size: 0.88rem;
            color: var(--color-text);
        }
        .jda-check-priority {
            font-size: 0.72rem;
            color: var(--color-muted);
        }

        /* Priority action cards */
        .jda-action-row {
            display: flex;
            align-items: flex-start;
            gap: 0.9rem;
            padding: 0.7rem 0;
            border-bottom: 1px solid var(--color-border);
        }
        .jda-action-row:last-child { border-bottom: none; }
        .jda-action-number {
            flex-shrink: 0;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: var(--color-primary-soft);
            color: var(--color-primary-dark);
            font-weight: 800;
            font-size: 0.78rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .jda-action-detail {
            font-size: 0.88rem;
            color: var(--color-text);
            line-height: 1.5;
            padding-top: 0.1rem;
        }

        /* Improved JD */
        .jda-improved-box {
            background: #FBFCFE;
            border: 1px solid var(--color-border);
            border-radius: 10px;
            padding: 1.4rem 1.5rem;
            white-space: pre-wrap;
            font-size: 0.9rem;
            line-height: 1.6;
            color: var(--color-text);
            max-height: 560px;
            overflow-y: auto;
        }
        .jda-disclaimer {
            font-size: 0.83rem;
            color: var(--color-muted);
            background: var(--color-primary-soft);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-top: 0.9rem;
            line-height: 1.5;
        }
        .jda-disclaimer b { color: var(--color-navy); }

        /* Empty state */
        .jda-empty-state {
            text-align: center;
            padding: 2.5rem 1.5rem;
            color: var(--color-muted);
            font-size: 0.95rem;
            border: 1px dashed var(--color-border);
            border-radius: 10px;
            background: var(--color-card);
        }

        /* Footer */
        .jda-footer {
            text-align: center;
            font-size: 0.78rem;
            color: var(--color-muted);
            margin-top: 2.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid var(--color-border);
        }

        /* Text area — force light surface + dark text regardless of
           the browser/OS theme, so it never renders dark-on-dark. */
        .stTextArea textarea {
            background-color: #FFFFFF !important;
            color: var(--color-text) !important;
            border: 1px solid var(--color-border) !important;
            border-radius: 8px !important;
            font-size: 0.92rem !important;
        }
        .stTextArea textarea::placeholder {
            color: var(--color-muted) !important;
            opacity: 1 !important;
        }
        .stTextArea textarea:focus {
            border-color: var(--color-primary) !important;
            box-shadow: 0 0 0 1px var(--color-primary) !important;
        }

        /* Primary button */
        div.stButton > button[kind="primary"] {
            background-color: var(--color-primary);
            border: none;
            font-weight: 600;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: var(--color-primary-dark);
        }

        /* Streamlit expander header — quieter default styling */
        .streamlit-expanderHeader {
            font-size: 0.87rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Small pure helpers
# ---------------------------------------------------------------------------

def get_quality_label(score: int) -> str:
    """Python-side quality label — Gemini never determines this."""
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 60:
        return "Fair"
    if score >= 40:
        return "Needs Improvement"
    return "Poor"


def get_friendly_error_message(error: Exception) -> str:
    """Map a raw backend exception to a professional, user-safe message."""
    text = str(error).lower()
    if "429" in text or "resource_exhausted" in text or "quota" in text:
        return (
            "**Analysis temporarily unavailable**\n\n"
            "The AI service has reached its current usage limit. "
            "Please try again later."
        )
    return (
        "**Unable to complete analysis**\n\n"
        "Something went wrong while processing the job description. "
        "Please try again."
    )


def severity_badge_class(severity: str) -> str:
    return {
        "high": "jda-badge-high",
        "medium": "jda-badge-medium",
        "low": "jda-badge-low",
    }.get(str(severity).lower(), "jda-badge-low")


def score_bar_color(value: int) -> str:
    """Color-code score bars so the breakdown isn't a wall of uniform blue."""
    if value >= 75:
        return "#16A34A"   # green
    if value >= 50:
        return "#F59E0B"   # amber
    return "#DC2626"       # red


def get_issue_title(issue) -> str:
    """Supports either .title (current) or .issue (legacy) field name."""
    return getattr(issue, "title", None) or getattr(issue, "issue", "")


def get_bias_alternative(flag) -> str:
    """Supports either .alternative (current) or .suggested_alternative (legacy)."""
    return getattr(flag, "alternative", None) or getattr(flag, "suggested_alternative", "")


def sorted_issues(issues):
    return sorted(
        issues,
        key=lambda i: SEVERITY_ORDER.get(str(i.severity).lower(), 3),
    )


def get_demo_analysis():
    """Fixed sample result used only when DEMO_MODE is True."""
    score_breakdown = SimpleNamespace(
        clarity=88,
        completeness=79,
        specificity=71,
        professionalism=92,
        inclusivity=84,
    )
    issues = [
        SimpleNamespace(
            title="Vague technical requirements",
            severity="High",
            category="Specificity",
            explanation=(
                "The job description does not specify which cybersecurity "
                "technologies or tools the candidate will work with."
            ),
            suggestion=(
                "Mention relevant SIEM, EDR, and security monitoring "
                "technologies used by the team."
            ),
        ),
        SimpleNamespace(
            title="No clear reporting structure",
            severity="Medium",
            category="Completeness",
            explanation="It is unclear who the role reports to.",
            suggestion="Add a line naming the manager or team the role reports into.",
        ),
    ]
    bias_flags = [
        SimpleNamespace(
            phrase="young and energetic",
            concern="This phrasing may discourage older, equally qualified candidates.",
            alternative="motivated and adaptable",
        ),
    ]
    checklist = [
        SimpleNamespace(item="Clear job title", present=True, priority="Essential",
                        comment="The role title clearly identifies the position."),
        SimpleNamespace(item="Role summary", present=True, priority="Essential",
                        comment="A short overview of the role is included."),
        SimpleNamespace(item="Work arrangement", present=False, priority="Recommended",
                        comment="No remote, hybrid, or on-site information is provided."),
    ]
    recommendations = [
        "Add specific cybersecurity technologies used day to day.",
        "Define minimum and preferred years of experience.",
        "Clarify the reporting structure for the role.",
        "Replace subjective language with measurable requirements.",
    ]
    improved_jd = (
        "Junior Cybersecurity Analyst\n\n"
        "Role Summary\n"
        "Support the security operations team by monitoring, investigating, "
        "and responding to security events across the organization's "
        "environment.\n\n"
        "Responsibilities\n"
        "- Monitor security alerts and escalate confirmed incidents.\n"
        "- Assist with log analysis and initial triage of events.\n"
        "- Support documentation of incident response activities.\n\n"
        "Required Qualifications\n"
        "- Foundational knowledge of networking and operating systems.\n"
        "- Willingness to work in a fast-paced security environment.\n\n"
        "[Customize: experience level, specific tools/platforms, work "
        "arrangement, and reporting structure were not specified in the "
        "original JD.]"
    )
    analysis = SimpleNamespace(
        score_breakdown=score_breakdown,
        summary=(
            "This is a solid draft cybersecurity job description with clear "
            "professionalism and inclusive tone. Specificity around required "
            "tools and technologies is the main area to strengthen."
        ),
        issues=issues,
        bias_flags=bias_flags,
        checklist=checklist,
        recommendations=recommendations,
        improved_jd=improved_jd,
    )
    overall_score = 83
    return analysis, overall_score


# ---------------------------------------------------------------------------
# Render functions
# ---------------------------------------------------------------------------

def render_header() -> None:
    st.markdown(
        f"""
        <div class="jda-header">
            <div>
                <h1>{APP_NAME}</h1>
                <p>{APP_TAGLINE}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_input_section():
    with st.container(border=True):
        st.markdown(
            '<div class="jda-section-title" style="--accent:#1D4ED8;">Job Description</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="jda-helper-text">Paste the complete job description you want to evaluate.</div>',
            unsafe_allow_html=True,
        )

        job_description = st.text_area(
            label="Job description input",
            height=280,
            placeholder="Paste a cybersecurity job description here...",
            label_visibility="collapsed",
        )

        analyze_clicked = st.button(
            "Analyze Job Description",
            type="primary",
            use_container_width=True,
        )

    return job_description, analyze_clicked


def render_score_section(overall_score: int, label: str) -> None:
    st.markdown(
        f"""
        <div class="jda-score-card">
            <div class="jda-score-label">Overall Score</div>
            <div class="jda-score-value">{overall_score}<span>/100</span></div>
            <div class="jda-score-tag">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_stats(analysis) -> None:
    issue_count = len(analysis.issues)
    bias_count = len(analysis.bias_flags)
    missing_count = sum(1 for item in analysis.checklist if not item.present)

    issue_class = "warn" if issue_count > 0 else "ok"
    bias_class = "warn" if bias_count > 0 else "ok"
    missing_class = "warn" if missing_count > 0 else "ok"

    st.markdown(
        f"""
        <div class="jda-stats-grid">
            <div class="jda-stat-box">
                <div class="jda-stat-value {issue_class}">{issue_count}</div>
                <div class="jda-stat-label">Issue{'s' if issue_count != 1 else ''}</div>
            </div>
            <div class="jda-stat-box">
                <div class="jda-stat-value {bias_class}">{bias_count}</div>
                <div class="jda-stat-label">Bias Flag{'s' if bias_count != 1 else ''}</div>
            </div>
            <div class="jda-stat-box">
                <div class="jda-stat-value {missing_class}">{missing_count}</div>
                <div class="jda-stat-label">Missing Criteri{'on' if missing_count == 1 else 'a'}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_score_breakdown(score_breakdown) -> None:
    dimensions = [
        ("Clarity", score_breakdown.clarity),
        ("Completeness", score_breakdown.completeness),
        ("Specificity", score_breakdown.specificity),
        ("Professionalism", score_breakdown.professionalism),
        ("Inclusivity", score_breakdown.inclusivity),
    ]

    with st.container(border=True):
        st.markdown(
            '<div class="jda-section-title" style="--accent:#1D4ED8;">Score Breakdown</div>',
            unsafe_allow_html=True,
        )

        rows_html = ""
        for name, value in dimensions:
            width = max(0, min(100, int(value)))
            color = score_bar_color(width)
            rows_html += f"""
            <div class="jda-bar-row">
                <div class="jda-bar-top">
                    <span class="name">{name}</span>
                    <span class="value">{width}/100</span>
                </div>
                <div class="jda-bar-track">
                    <div class="jda-bar-fill" style="width:{width}%; background:{color};"></div>
                </div>
            </div>
            """
        st.markdown(rows_html, unsafe_allow_html=True)


def render_summary(summary: str) -> None:
    with st.container(border=True):
        st.markdown(
            '<div class="jda-section-title" style="--accent:#0F172A;">Summary</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-size: 0.92rem; line-height: 1.6; color: var(--color-text);">{summary}</div>',
            unsafe_allow_html=True,
        )


def render_finding_card(issue) -> None:
    badge_class = severity_badge_class(issue.severity)
    title = get_issue_title(issue)
    st.markdown(
        f"""
        <div class="jda-finding">
            <span class="jda-badge {badge_class}">{issue.severity}</span>
            <div class="jda-finding-title">{title}</div>
            <div class="jda-finding-fix">→ {issue.suggestion}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Why this matters"):
        st.markdown(f"**Category:** {issue.category}")
        st.markdown(issue.explanation)


def render_key_findings(issues) -> None:
    with st.container(border=True):
        st.markdown(
            '<div class="jda-section-title" style="--accent:#B91C1C;">Key Findings</div>',
            unsafe_allow_html=True,
        )

        if not issues:
            st.success("No significant issues were identified.")
            return

        ordered = sorted_issues(issues)
        visible = ordered[:TOP_FINDINGS_COUNT]
        remaining = ordered[TOP_FINDINGS_COUNT:]

        for issue in visible:
            render_finding_card(issue)

        if remaining:
            with st.expander(f"View all {len(ordered)} findings"):
                for issue in remaining:
                    render_finding_card(issue)


def render_bias_section(bias_flags) -> None:
    with st.container(border=True):
        st.markdown(
            '<div class="jda-section-title" style="--accent:#7C3AED;">Bias &amp; Inclusivity</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="jda-section-subtitle">Potentially exclusionary or subjective '
            'language identified in the JD.</div>',
            unsafe_allow_html=True,
        )

        if bias_flags:
            rows = []
            for flag in bias_flags:
                rows.append(
                    {
                        "Phrase": f'"{getattr(flag, "phrase", "")}"',
                        "Concern": getattr(flag, "concern", ""),
                        "Suggested alternative": get_bias_alternative(flag),
                    }
                )
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.success("No potentially biased language identified.")


def render_checklist(checklist) -> None:
    with st.container(border=True):
        st.markdown(
            '<div class="jda-section-title" style="--accent:#15803D;">JD Quality Checklist</div>',
            unsafe_allow_html=True,
        )

        essential = [i for i in checklist if str(i.priority).lower() == "essential"]
        recommended = [i for i in checklist if str(i.priority).lower() != "essential"]
        essential_done = sum(1 for i in essential if i.present)
        recommended_done = sum(1 for i in recommended if i.present)

        st.markdown(
            f"""
            <div class="jda-check-summary-grid">
                <div class="jda-check-summary-box">
                    <div class="jda-check-summary-label">Essential Criteria</div>
                    <div class="jda-check-summary-value">{essential_done} / {len(essential)} complete</div>
                </div>
                <div class="jda-check-summary-box">
                    <div class="jda-check-summary-label">Recommended Criteria</div>
                    <div class="jda-check-summary-value">{recommended_done} / {len(recommended)} complete</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        cols = st.columns(2)
        for index, item in enumerate(checklist):
            icon, icon_class = ("✓", "present") if item.present else ("–", "missing")
            with cols[index % 2]:
                st.markdown(
                    f"""
                    <div class="jda-check-row">
                        <div class="jda-check-icon {icon_class}">{icon}</div>
                        <div>
                            <div class="jda-check-title">{item.item}</div>
                            <div class="jda-check-priority">{item.priority}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                with st.expander("Details", expanded=False):
                    st.markdown(item.comment)


def render_priority_actions(recommendations) -> None:
    with st.container(border=True):
        st.markdown(
            '<div class="jda-section-title" style="--accent:#1E3A8A;">Priority Actions</div>',
            unsafe_allow_html=True,
        )

        if not recommendations:
            st.info("No additional recommendations were generated.")
            return

        visible = recommendations[:TOP_RECOMMENDATIONS_COUNT]
        remaining = recommendations[TOP_RECOMMENDATIONS_COUNT:]

        def action_row(index: int, text: str) -> str:
            return f"""
            <div class="jda-action-row">
                <div class="jda-action-number">{index:02d}</div>
                <div class="jda-action-detail">{text}</div>
            </div>
            """

        rows_html = "".join(action_row(i, text) for i, text in enumerate(visible, start=1))
        st.markdown(rows_html, unsafe_allow_html=True)

        if remaining:
            with st.expander(f"View all {len(recommendations)} recommendations"):
                rows_html = "".join(
                    action_row(i, text)
                    for i, text in enumerate(remaining, start=len(visible) + 1)
                )
                st.markdown(rows_html, unsafe_allow_html=True)


def render_improved_jd(improved_jd: str) -> None:
    if not improved_jd:
        return

    with st.container(border=True):
        st.markdown(
            '<div class="jda-section-title" style="--accent:#0D9488;">Improved Job Description</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="jda-section-subtitle">Example revision based on the identified issues.</div>',
            unsafe_allow_html=True,
        )

        st.markdown(f'<div class="jda-improved-box">{improved_jd}</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="jda-disclaimer">
                <b>Review before publishing:</b> This is an AI-generated example.
                Verify and customize responsibilities, qualifications,
                technologies, work arrangements, and other requirements to match
                your organization's actual needs.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Lightweight copy-to-clipboard button. No extra dependency: uses the
        # browser clipboard API directly via a small embedded component.
        # This is a native iframe element — it now also lives inside the
        # same st.container(border=True) box as everything else above, so
        # it renders visually nested instead of floating below a dead div.
        escaped = (
            improved_jd.replace("\\", "\\\\")
            .replace("`", "\\`")
            .replace("</", "<\\/")
        )
        components.html(
            f"""
            <div style="margin-top: 0.75rem;">
                <button id="jda-copy-btn" style="
                    background: #1D4ED8; color: #fff; border: none;
                    border-radius: 6px; padding: 0.5rem 1rem; font-size: 0.85rem;
                    font-weight: 600; cursor: pointer; font-family: inherit;">
                    Copy Improved JD
                </button>
                <span id="jda-copy-status" style="
                    margin-left: 0.6rem; font-size: 0.82rem; color: #15803D;"></span>
            </div>
            <script>
            const jdText = `{escaped}`;
            const btn = document.getElementById("jda-copy-btn");
            const status = document.getElementById("jda-copy-status");
            btn.addEventListener("click", async () => {{
                try {{
                    await navigator.clipboard.writeText(jdText);
                    status.textContent = "Copied";
                    setTimeout(() => {{ status.textContent = ""; }}, 2000);
                }} catch (err) {{
                    status.textContent = "Copy failed — select and copy manually";
                }}
            }});
            </script>
            """,
            height=50,
        )


def render_empty_state() -> None:
    st.markdown(
        '<div class="jda-empty-state">Paste a job description above to begin your analysis.</div>',
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="jda-footer">
            {APP_NAME}<br />
            AI-assisted analysis for better cybersecurity hiring.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main app flow
# ---------------------------------------------------------------------------

def main() -> None:
    inject_styles()

    if "jda_analysis" not in st.session_state:
        st.session_state.jda_analysis = None
    if "jda_overall_score" not in st.session_state:
        st.session_state.jda_overall_score = None
    if "jda_error" not in st.session_state:
        st.session_state.jda_error = None

    render_header()
    job_description, analyze_clicked = render_input_section()

    if analyze_clicked:
        if not job_description.strip():
            st.warning("Please enter a job description before analyzing.")
        else:
            st.session_state.jda_error = None
            with st.spinner("Analyzing job description..."):
                try:
                    if DEMO_MODE:
                        analysis, overall_score = get_demo_analysis()
                    else:
                        analysis, overall_score = analyze_job_description(job_description)

                    st.session_state.jda_analysis = analysis
                    st.session_state.jda_overall_score = overall_score

                except Exception as error:  # noqa: BLE001 - surfaced safely below
                    st.session_state.jda_error = error

    st.divider()

    if st.session_state.jda_error is not None:
        st.error(get_friendly_error_message(st.session_state.jda_error))
        with st.expander("Technical details (for debugging)"):
            st.code(str(st.session_state.jda_error))

    analysis = st.session_state.jda_analysis
    overall_score = st.session_state.jda_overall_score

    if analysis is not None and overall_score is not None:
        label = get_quality_label(overall_score)
        render_score_section(overall_score, label)
        render_quick_stats(analysis)
        render_score_breakdown(analysis.score_breakdown)
        render_summary(analysis.summary)
        render_key_findings(analysis.issues)
        render_bias_section(analysis.bias_flags)
        render_checklist(analysis.checklist)
        render_priority_actions(analysis.recommendations)
        render_improved_jd(getattr(analysis, "improved_jd", ""))
    elif st.session_state.jda_error is None:
        render_empty_state()

    render_footer()


if __name__ == "__main__":
    main()