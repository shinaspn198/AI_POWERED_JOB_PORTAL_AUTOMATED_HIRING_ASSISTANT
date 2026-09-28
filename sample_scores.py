from communication_score import calculate_communication_score
from score_normalizer import normalize_score


samples = [
    {
        "candidate": "Candidate A",
        "fluency": 50,
        "grammar": 45,
        "vocabulary": 40,
        "clarity": 50,
        "filler_words": 60,
        "structure": 45
    },
    {
        "candidate": "Candidate B",
        "fluency": 70,
        "grammar": 65,
        "vocabulary": 60,
        "clarity": 70,
        "filler_words": 80,
        "structure": 65
    },
    {
        "candidate": "Candidate C",
        "fluency": 90,
        "grammar": 88,
        "vocabulary": 85,
        "clarity": 92,
        "filler_words": 95,
        "structure": 90
    }
]


print("===== SAMPLE COMMUNICATION SCORES =====")

for candidate in samples:

    score = calculate_communication_score(
        candidate["fluency"],
        candidate["grammar"],
        candidate["vocabulary"],
        candidate["clarity"],
        candidate["filler_words"],
        candidate["structure"]
    )

    score = normalize_score(score)

    print(f"\n{candidate['candidate']}")
    print("Communication Score:", score, "/ 100")