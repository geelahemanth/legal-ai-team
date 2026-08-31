MIN_PRPORT_LENGHT = 10

def validate_final_report(report:str):
    """ Validate the final report before sending it to the user."""

    # ----------------- Rule 1 -----------------
    if not report:
        return False, "Final report cannot be empty."
    
    report = report.strip()

    # ----------------- Rule 2 -----------------
    if len(report) < MIN_PRPORT_LENGHT:
        return False, f"Final report is too short. Minimum length is {MIN_PRPORT_LENGHT} characters."
    
    #----------------- Rule 3 -----------------
    invalid_responses = [
        "I dont know",
        "I cannot answer",
        "I am unable to answer",
        "Error generating report",
    ]
    report_lower = report.lower()
    for invalid_response in invalid_responses:
        if invalid_response in report_lower:
            return False, f"Final report contains an invalid response: '{invalid_response}'"
    
    return True, "Valid final report."

