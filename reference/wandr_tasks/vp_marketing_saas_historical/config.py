"""Per (company, person) where company is one of a fixed list of enterprise SaaS companies, find evidence the person held a senior marketing-leadership role at that company during 2022-2025.

Structure:
  vp_marketing_saas_historical:    [company, company_person(fields=company,person), url]
      leaf judge: page (LinkedIn profile or equivalent) shows in-scope marketing-leadership
                  role + matching employer + tenure overlapping 2022-2025

Unlike `vp_marketing_saas`, which demands current tenure (`Present` / no end-date), this task accepts tenure overlapping the 2022-2025 window and requires three historically active marketing leaders per company. The work shifts from finding the single current incumbent to discovering multiple leaders across an absolute closed window.

The `COMPANIES` dictionary is duplicated from `vp_marketing_saas` so each task remains self-contained; keep the two lists synchronized when the closed set changes.
"""

from pathlib import Path

from src.config import (
    CanonConfig,
    CanonKeyConfig,
    DedupConfig,
    DedupKeyConfig,
    EvalConfig,
    JudgeConfig,
    KeySpec,
    TaskConfig,
    exact_match,
    url_norm,
)
from schemas.judgment import (
    VPMarketingSaaSHistoricalJudgment,
)

HERE = Path(__file__).parent

# Canonical key → list of accepted aliases. Mirrors `vp_marketing_saas.config.COMPANIES`
# (duplicated for task-isolation; manual sync if the closed list changes).
COMPANIES = {
    # Existing 10 (carried over verbatim from prior config)
    "SAP":         ["SAP SE", "SAP AG"],
    "Sage":        ["Sage Group", "Sage Software", "The Sage Group"],
    "AVEVA":       ["AVEVA Group", "AVEVA Solutions"],
    "Elastic":     ["Elastic NV", "Elasticsearch", "Elastic.co"],
    "Software AG": ["SoftwareAG", "Software AG (now StreamServe / IBM acquisition)"],
    "TeamViewer":  ["TeamViewer Germany", "TeamViewer SE"],
    "Darktrace":   ["Darktrace plc", "Darktrace Limited"],
    "Celonis":     ["Celonis SE", "Celonis Inc", "Make by Celonis"],
    "OutSystems":  ["OutSystems, Inc.", "OutSystems Software"],
    "Onfido":      ["Onfido Ltd", "Onfido (Entrust)"],

    # Mega-cap enterprise SaaS / CRM / cloud platforms
    "Salesforce":         ["Salesforce.com", "Salesforce, Inc.", "salesforce.com"],
    "ServiceNow":         ["ServiceNow, Inc.", "Service Now"],
    "Workday":            ["Workday, Inc."],
    "Adobe":              ["Adobe Inc.", "Adobe Systems", "Adobe Digital Experience"],
    "Atlassian":          ["Atlassian Corporation", "Atlassian Plc"],
    "Intuit":             ["Intuit Inc."],

    # Cloud data / observability / DevOps
    "Snowflake":          ["Snowflake Inc.", "Snowflake Computing"],
    "Datadog":            ["Datadog, Inc."],
    "MongoDB":            ["MongoDB Inc.", "MongoDB, Inc."],
    "Cloudflare":         ["Cloudflare, Inc."],
    "Confluent":          ["Confluent, Inc.", "Confluent Inc"],
    "GitLab":             ["GitLab Inc.", "GitLab Ltd"],
    "Splunk":             ["Splunk Inc.", "Splunk (Cisco)"],
    "Dynatrace":          ["Dynatrace LLC", "Dynatrace, Inc."],
    "New Relic":          ["New Relic, Inc.", "New Relic Inc"],
    "PagerDuty":          ["PagerDuty, Inc."],
    "JFrog":              ["JFrog Ltd"],

    # Cybersecurity / identity
    "Okta":               ["Okta, Inc.", "Auth0 (an Okta company)"],
    "CrowdStrike":        ["CrowdStrike Holdings", "CrowdStrike, Inc."],
    "Palo Alto Networks": ["Palo Alto Networks, Inc.", "PANW"],
    "Zscaler":            ["Zscaler, Inc."],

    # Communications / collaboration / customer experience SaaS
    "Twilio":             ["Twilio Inc.", "Twilio Segment"],
    "HubSpot":            ["HubSpot, Inc.", "Hubspot"],
    "Zendesk":            ["Zendesk, Inc.", "Zendesk Inc"],
    "Slack":              ["Slack Technologies", "Slack (Salesforce)"],
    "Freshworks":         ["Freshworks Inc.", "Freshdesk", "Freshservice"],
    "Sprinklr":           ["Sprinklr, Inc."],
    "DocuSign":           ["DocuSign, Inc.", "Docusign"],

    # Vertical / industry SaaS
    "Bentley Systems":    ["Bentley", "Bentley Systems Incorporated"],
    "Procore":            ["Procore Technologies", "Procore Technologies, Inc."],
    "BlackLine":          ["BlackLine, Inc.", "Blackline"],
    "Coupa":              ["Coupa Software", "Coupa Software, Inc."],
    "Anaplan":            ["Anaplan, Inc."],
    "UiPath":             ["UiPath, Inc.", "UiPath Inc"],
    "Pegasystems":        ["Pega", "Pega Systems", "Pegasystems Inc."],
    "Veeam":              ["Veeam Software", "Veeam Software Group"],

    # Commerce / e-commerce platform / FinTech-platform SaaS
    "Shopify":            ["Shopify Inc.", "Shopify Plus"],
    "Wix":                ["Wix.com", "Wix.com Ltd"],
    "Klaviyo":            ["Klaviyo, Inc."],
    "BILL":               ["Bill.com", "Bill.com Holdings", "BILL Holdings"],
}

COMPANY = KeySpec("company", required=len(COMPANIES))
COMPANY_PERSON = KeySpec(
    "company_person", required=3, fields=("company", "person"))
URL = KeySpec("url", required=1)

_COMPANY_CANON = CanonKeyConfig(
    prompt_section_template=(HERE / "prompts" / "canon_company_section_template.md.jinja").read_text().strip())
_COMPANY_PERSON_DEDUP = DedupKeyConfig(
    prompt_section_template=(HERE / "prompts" / "dedup_company_person_section_template.md.jinja").read_text().strip())
_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)
_COMPANY_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

CONFIG = TaskConfig(
    name="vp_marketing_saas_historical",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    extra_bindings={"companies": COMPANIES, "target_period": "2022-2025"},
    key_hierarchy=[COMPANY, COMPANY_PERSON, URL],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={"company": _COMPANY_CANON, "url": _URL_CANON}),
        judge=JudgeConfig(
            schema=VPMarketingSaaSHistoricalJudgment,
            prompt_section_template=(HERE / "prompts" / "judge_section_template.md.jinja").read_text()),
        dedup=DedupConfig(
            keys={"company": _COMPANY_DEDUP, "company_person": _COMPANY_PERSON_DEDUP, "url": _URL_DEDUP}),
    ),
)
