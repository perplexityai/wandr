EVIDENCE_SIDE_OPERATOR_OR_PROJECT_CLAIM = "operator_or_project_claim"
EVIDENCE_SIDE_RECIPIENT_OR_PUBLIC_ACKNOWLEDGMENT = "recipient_or_public_acknowledgment"

EVIDENCE_SIDES = {
    EVIDENCE_SIDE_OPERATOR_OR_PROJECT_CLAIM,
    EVIDENCE_SIDE_RECIPIENT_OR_PUBLIC_ACKNOWLEDGMENT,
}

EVIDENCE_SIDE_DESCRIPTIONS = {
    EVIDENCE_SIDE_OPERATOR_OR_PROJECT_CLAIM: (
        "operator, sponsor, project, filing, or official project-controlled source"
    ),
    EVIDENCE_SIDE_RECIPIENT_OR_PUBLIC_ACKNOWLEDGMENT: (
        "recipient, heat utility/network, municipality, public authority, host facility, "
        "or equivalent independent public source"
    ),
}
