POSITIVE_WORDS = [
    "confident",
    "excellent",
    "good",
    "strong",
    "success",
    "enjoy",
    "love",
    "comfortable",
    "achieved"
]

NEGATIVE_WORDS = [
    "worried",
    "nervous",
    "afraid",
    "difficult",
    "confused",
    "problem",
    "fail",
    "stress",
    "uncertain"
]


def analyze_sentiment(text):
    words = text.lower().split()

    positive_count = 0
    negative_count = 0

    for word in words:
        if word in POSITIVE_WORDS:
            positive_count += 1

        if word in NEGATIVE_WORDS:
            negative_count += 1

    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    total_words = len(words)

    if total_words == 0:
        sentiment_score = 50
    else:
        sentiment_score = 50 + (
            (positive_count - negative_count) * 10
        )

    sentiment_score = max(0, min(100, sentiment_score))

    return {
        "positive_words": positive_count,
        "negative_words": negative_count,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score
    }


if __name__ == "__main__":

    answer = input("Enter candidate response: ")

    result = analyze_sentiment(answer)

    print("\n===== SENTIMENT ANALYSIS =====")
    print("Positive Words:", result["positive_words"])
    print("Negative Words:", result["negative_words"])
    print("Sentiment:", result["sentiment"])
    print("Sentiment Score:", result["sentiment_score"], "/ 100")