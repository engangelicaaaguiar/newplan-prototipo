"""Ergos/NR1 calculation tables and utilities."""

# NR1 Risk Levels based on scores
RISK_LEVELS = {
    "baixo": (0, 25),
    "medio": (25, 50),
    "alto": (50, 75),
    "critico": (75, 100),
}

# Ergos questionnaire mapping
ERGOS_FACTORS = {
    "carga_mental": {"weight": 0.25, "questions": [1, 2, 3, 4, 5]},
    "ritmo_trabalho": {"weight": 0.20, "questions": [6, 7, 8]},
    "pressao_temporal": {"weight": 0.15, "questions": [9, 10]},
    "autonomia": {"weight": 0.15, "questions": [11, 12]},
    "relacionamento": {"weight": 0.15, "questions": [13, 14, 15]},
    "ambiente_fisico": {"weight": 0.10, "questions": [16, 17, 18]},
}


def calculate_score(responses: dict) -> float:
    """Calculate psychosocial score from responses."""
    # TODO: Implement score calculation based on Ergos methodology
    return sum(responses.values()) / len(responses) if responses else 0.0


def get_risk_level(score: float) -> str:
    """Get risk level based on score."""
    for level, (min_score, max_score) in RISK_LEVELS.items():
        if min_score <= score < max_score:
            return level
    return "critico"
