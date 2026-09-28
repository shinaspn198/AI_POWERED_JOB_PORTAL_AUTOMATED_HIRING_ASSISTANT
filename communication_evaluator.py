from communication_score import calculate_communication_score
from communication_analyzer import calculate_filler_score


def evaluate_communication(
    answer,
    fluency,
    grammar,
    vocabulary,
    clarity,
    structure
):
    filler_score = calculate_filler_score(answer)

    final_score = calculate_communication_score(
        fluency,
        grammar,
        vocabulary,
        clarity,
        filler_score,
        structure
    )

    return {
        "fluency": fluency,
        "grammar": grammar,
        "vocabulary": vocabulary,
        "clarity": clarity,
        "filler_score": filler_score,
        "structure": structure,
        "communication_score": final_score
    }


if __name__ == "__main__":

    answer = input("Enter candidate answer: ")

    result = evaluate_communication(
        answer,
        fluency=80,
        grammar=75,
        vocabulary=70,
        clarity=85,
        structure=80
    )

    print("\n===== COMMUNICATION EVALUATION =====")

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nFinal Communication Score:",
          result["communication_score"], "/ 100")