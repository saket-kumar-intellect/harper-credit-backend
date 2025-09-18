from core.models import Applicant


def compute_application_score(applicant: Applicant) -> int:
    """Return a credit score between 300 and 900 based on income and employment.

    Very simple heuristic:
    - Base 300
    - Income contribution: min(500, income / 1000) added
    - Employment bump: +80 for SALARIED, +50 for SELF_EMPLOYED, +10 for STUDENT, 0 otherwise
    - Clamp to [300, 900]
    """
    base_score = 300
    try:
        income_value = float(applicant.annual_income or 0)
    except Exception:
        income_value = 0.0

    income_component = min(500.0, income_value / 1000.0)

    employment_bump_map = {
        "SALARIED": 80.0,
        "SELF_EMPLOYED": 50.0,
        "STUDENT": 10.0,
        "UNEMPLOYED": 0.0,
    }
    bump = employment_bump_map.get(applicant.employment_status, 0.0)

    raw_score = base_score + income_component + bump
    final_score = int(max(300, min(900, round(raw_score))))
    return final_score


