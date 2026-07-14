"""CEO and CFO appointments at US publicly-listed companies, with announcement landing in a target period.

Compendium-source (a) flat task. Per (company, appointee) row, an authoritative-source URL
(SEC primary filing, the company's controlled web property, a newswire-distributed authored
release, or directly-attributed first-hand business journalism) carries the full conjunction:
US-public-company identity + appointee + role + announcement-date.

Real-world workflow proxied: ESG / equity-research / IR / executive-recruiting analyst
tracking C-suite transitions across US-public-company watchlists. The volume + source-class
authority bar are the load-bearing discrimination axes; naive aggregator-republication
solvers fail the bar; programmatic SEC-EDGAR + company-IR + press-wire sweep solvers pass.
"""
