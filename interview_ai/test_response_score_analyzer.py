from response_score_analyzer import calculate_response_score


print("=" * 60)
print("DAY 27 - STEP 5 RESPONSE SCORING TEST")
print("=" * 60)


# Test 1 - Excellent Response
confidence = {
    "confidence_level": "high"
}

quality = {
    "quality_level": "good"
}

relevance = {
    "relevance_score": 100.0
}

result = calculate_response_score(
    confidence,
    quality,
    relevance
)

print("\nTest 1 - Excellent Response")
print("Result:", result)


# Test 2 - Good Response
confidence = {
    "confidence_level": "high"
}

quality = {
    "quality_level": "moderate"
}

relevance = {
    "relevance_score": 100.0
}

result = calculate_response_score(
    confidence,
    quality,
    relevance
)

print("\nTest 2 - Good Response")
print("Result:", result)


# Test 3 - Moderate Response
confidence = {
    "confidence_level": "moderate"
}

quality = {
    "quality_level": "moderate"
}

relevance = {
    "relevance_score": 50.0
}

result = calculate_response_score(
    confidence,
    quality,
    relevance
)

print("\nTest 3 - Moderate Response")
print("Result:", result)


# Test 4 - Poor Response
confidence = {
    "confidence_level": "moderate"
}

quality = {
    "quality_level": "poor"
}

relevance = {
    "relevance_score": 0.0
}

result = calculate_response_score(
    confidence,
    quality,
    relevance
)

print("\nTest 4 - Poor Response")
print("Result:", result)


# Test 5 - Empty Response
confidence = {
    "confidence_level": "high"
}

quality = {
    "quality_level": "poor"
}

relevance = {
    "relevance_score": 0
}

result = calculate_response_score(
    confidence,
    quality,
    relevance
)

print("\nTest 5 - Empty Response")
print("Result:", result)


print("\n" + "=" * 60)
print("STEP 5 TEST COMPLETED")
print("=" * 60)