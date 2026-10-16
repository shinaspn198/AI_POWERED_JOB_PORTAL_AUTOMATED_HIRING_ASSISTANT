from scoring.score_engine import final_score


print("===== DAY 42 SCORING ENGINE =====")

print("Normal score:")
print(final_score(80, 90))

print("\nMinimum score:")
print(final_score(0, 0))

print("\nMaximum score:")
print(final_score(100, 100))

print("\nInvalid score test:")

try:
    print(final_score(100, 120))
except ValueError as e:
    print("Error:", e)