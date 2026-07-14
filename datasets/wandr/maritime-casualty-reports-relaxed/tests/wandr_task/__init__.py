"""Casual maritime casualty coverage — relaxed variant of `maritime_casualty_reports`.

Same key hierarchy ([vessel, url]) and target_period ("2024 or 2025") as the strict task,
but the source bar drops from "per-incident investigation report on a recognized safety
board's domain" to "any page that clearly names the vessel and describes its 2024-2025
casualty (when, where, what)". News articles, encyclopedic articles, trade-press
write-ups, dive-magazine reportage, legal-blog post-mortems, etc. all admit. The strict
casualty-class enumeration is dropped; any vocabulary works.

See `config.py` for the volume rationale (vessel.required = 80).
"""
