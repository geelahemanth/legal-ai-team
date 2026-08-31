MIN_ANALYSIS_LENGTH = 100


def validate_contract_analysis(analysis: str):
    """Validate contract analysis before generating the final report."""

    if not analysis:
        return False, "Contract analysis is empty."

    analysis = analysis.strip()

    if len(analysis) < MIN_ANALYSIS_LENGTH:
        return False, "Contract analysis is too short."

    normalized = analysis.lower()

    if "i don't know" in normalized or "i dont know" in normalized:
        return False, "Contract analysis should not contain 'I don't know'."

    return True, "Valid contract analysis."