import math


def normalize_score(score):
    """
    Safely normalizes scores to the [0.0, 100.0] range.
    Handles None, strings, negative values, values > 100, and NaN/inf values gracefully.
    """
    if score is None:
        return 0.0

    try:
        val = float(score)
        if math.isnan(val) or math.isinf(val):
            return 0.0
        if val < 0:
            return 0.0
        if val > 100:
            return 100.0
        return round(val, 2)
    except (ValueError, TypeError):
        return 0.0


if __name__ == "__main__":
    test_scores = [-10, 45, 80.5, 110, None, "92.5", float("nan")]
    print("===== SCORE NORMALIZATION =====")
    for score in test_scores:
        normalized = normalize_score(score)
        print(f"Original Score: {score} -> Normalized Score: {normalized}")