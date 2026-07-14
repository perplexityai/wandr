ROLE_CATEGORIES = (
    "environmental_health_director",
    "environmental_health_manager",
    "environmental_health_supervisor",
    "health_director",
    "public_health_director",
    "community_health_administrator",
    "health_department_executive",
    "public_health_environment_director",
    "external_provider_environmental_health_manager",
    "environmental_health_unit_no_named_lead",
    "unclear_equivalent_counterpart",
)

ROLE_CATEGORIES_TEXT = "\n".join(f"- `{category}`" for category in ROLE_CATEGORIES)
ROLE_CATEGORIES_INLINE = ", ".join(f"`{category}`" for category in ROLE_CATEGORIES)

JURISDICTION_ENTITY_TYPES = (
    "city_or_municipal",
    "county_or_county_department",
    "multi_jurisdiction_or_community_health_provider",
    "tribal_or_other_official_local_authority",
)

JURISDICTION_ENTITY_TYPES_TEXT = "\n".join(
    f"- `{entity_type}`" for entity_type in JURISDICTION_ENTITY_TYPES
)
JURISDICTION_ENTITY_TYPES_INLINE = ", ".join(
    f"`{entity_type}`" for entity_type in JURISDICTION_ENTITY_TYPES
)

MDH_ARTIFACT_NAME = "Minnesota State and Local Food, Pools, and Lodging Contacts"
MDH_ARTIFACT_URL = "https://www.health.state.mn.us/communities/environment/food/docs/license/locals.pdf"
MDH_ARTIFACT_VISIBLE_DATE = "02/04/2026"
MDH_ARTIFACT_CHECKED_DATE = "2026-06-26"
MDH_ARTIFACT_HTTP_METADATA = (
    'Last-Modified: Wed, 04 Feb 2026 17:06:54 GMT; ETag: "1770224814"; '
    "Content-Length: 688425"
)
MDH_ARTIFACT_XMP_METADATA = (
    "CreateDate 2026-02-04T10:46:00-06:00; ModifyDate 2026-02-04T11:01:33-06:00"
)
MDH_ARTIFACT_METADATA_TEXT = "\n".join(
    (
        f"- Source name: `{MDH_ARTIFACT_NAME}`",
        f"- Live URL: `{MDH_ARTIFACT_URL}`",
        f"- Visible artifact date: `{MDH_ARTIFACT_VISIBLE_DATE}`",
        f"- Checked date: `{MDH_ARTIFACT_CHECKED_DATE}`",
        f"- HTTP metadata: `{MDH_ARTIFACT_HTTP_METADATA}`",
        f"- PDF XMP metadata: `{MDH_ARTIFACT_XMP_METADATA}`",
    )
)
