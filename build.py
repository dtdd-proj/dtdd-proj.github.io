#!/usr/bin/env python3
"""Build the static project page using only the Python standard library."""
import argparse
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent
SITE_URL = "https://dtdd-proj.github.io/"
TITLE = "DTDD: Divergence-Triggered Dynamic Distillation for Reliable On-Policy Supervision"
DESCRIPTION = ("DTDD uses segment-level student–teacher divergence to route supervision: "
               "OPD on the student prefix, behavior cloning on the teacher recovery suffix.")
ARXIV = ""  # Set the public paper URL when available.
CODE = ""   # Set the implementation repository URL when available.

FIGURES = {
    "method": ("fig_dtdd_pipeline.png", 2000, 730,
               "Reasoning pipeline: a student rollout is split into segments; the first high-divergence segment marks where the teacher regenerates the suffix; the prefix receives OPD and the suffix behavior cloning.",
               "Reasoning realization of DTDD. The teacher recovers from the retained student prefix.", True),
    "motivation": ("fig_opd_failure_cases.png", 2000, 730,
                   "Illustrations of slow learning from a base student, late instability under long response budgets, and error propagation after a wrong tool call.",
                   "Examples motivating teacher recovery: a large initial policy gap, long reasoning trajectories, and errors that propagate through tool use.", False),
    "stability": ("stability_main.png", 1623, 470,
                  "OPD and DTDD gradient norm and truncated-rollout ratio over training, grouped by 15K and 18K response budgets.",
                  "DTDD suppresses late OPD spikes at 15K and 18K response budgets.", False),
    "efficiency": ("base_efficiency_main.png", 1510, 444,
                   "Held-out math accuracy over training for OPD and DTDD at different window sizes and intervention levels.",
                   "Accuracy on AIME 2024, AIME 2025, and AMC 2023, averaged across benchmarks using average@16 evaluation.", False),
    "agents": ("alfworld_takeover.png", 1943, 755,
               "ALFWorld LoRA takeover dynamics: intervention declines as training progresses and rises again around update 180.",
               "ALFWorld with LoRA: takeover becomes sparse and reactivates near update 180.", False),
    "headroom": ("headroom_gate.png", 1401, 500,
                 "Average DTDD minus OPD performance versus OPD-to-teacher headroom across 23 experimental arms, with boundary cases highlighted.",
                 "Each point is an experimental arm. Gains are averaged over shared checkpoints; they are not the best-observed scores reported above.", False),
}


def figure(key):
    filename, width, height, alt, caption, eager = FIGURES[key]
    src = f"static/images/{filename}"
    priority = ' fetchpriority="high"' if eager else ''
    return f'''<figure>
      <div class="figure-scroll" tabindex="0" role="region" aria-label="{escape(alt, quote=True)}">
        <a class="figure-link" href="{src}" data-lightbox aria-label="Enlarge figure: {escape(alt, quote=True)}">
          <img src="{src}" width="{width}" height="{height}" loading="{'eager' if eager else 'lazy'}" decoding="async"{priority} alt="{escape(alt, quote=True)}">
        </a>
      </div>
      <figcaption>{caption} <a href="{src}" data-lightbox data-alt="{escape(alt, quote=True)}" class="enlarge">View full size ↗</a><span class="swipe-hint">Swipe to explore the plot on mobile.</span></figcaption>
    </figure>'''


def resource(label, url):
    paths = {
        "Paper": "M6 2h9l5 5v15H6zM14 3.5V8h4.5",
        "Code": "M8 5 1 12l7 7 2-2-5-5 5-5zm8 0-2 2 5 5-5 5 2 2 7-7z",
    }
    icon = f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{paths.get(label, paths["Paper"])}"/></svg>'
    if not url:
        return f'<span class="button unavailable" aria-disabled="true">{icon}{label}<span class="resource-status">(coming soon)</span></span>'
    if not url.startswith("https://"):
        raise ValueError(f"{label} URL must be an HTTPS URL")
    return f'<a class="button" href="{escape(url, quote=True)}">{icon}{label}</a>'


def render():
    context = {"title": escape(TITLE), "description": escape(DESCRIPTION, quote=True),
               "site_url": SITE_URL, "paper_button": resource("Paper", ARXIV),
               "code_button": resource("Code", CODE)}
    context.update({f"figure_{key}": figure(key) for key in FIGURES})
    return Template((ROOT / "page.html").read_text()).substitute(context)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check that index.html is up to date")
    args = parser.parse_args()
    page = render()
    if args.check:
        if (ROOT / "index.html").read_text() != page:
            parser.error("index.html is stale; run python3 build.py")
        print("index.html is up to date")
    else:
        for name in ("index.html", "preview.html"):
            (ROOT / name).write_text(page)
        print("Wrote index.html and preview.html")
