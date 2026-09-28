def normalize_score(score):
    if score < 0:
        return 0

    if score > 100:
        return 100

    return round(score, 2)


if __name__ == "__main__":

    test_scores = [-10, 45, 80.5, 110]

    print("===== SCORE NORMALIZATION =====")

    for score in test_scores:
        normalized = normalize_score(score)

        print(
            f"Original Score: {score} "
            f"-> Normalized Score: {normalized}"
        )