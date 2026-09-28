from edge_case_handler import (
    handle_edge_case,
    detect_language_mixing,
    handle_audio_quality,
    process_answer,
    handle_background_noise
)


print("EDGE CASE TESTS")

print(handle_edge_case(""))
print(handle_edge_case("uh"))
print(handle_edge_case("Python is a programming language"))


print("\nLANGUAGE TESTS")

print(detect_language_mixing("I worked on Python project"))
print(detect_language_mixing("എനിക്ക് Python അറിയാം"))
print(detect_language_mixing("I worked on Python project ആണ്"))


print("\nAUDIO QUALITY TESTS")

print(handle_audio_quality("", 0.2))

print(handle_audio_quality(
    "I know Python",
    0.4
))

print(handle_audio_quality(
    "I know Python",
    0.6
))

print(handle_audio_quality(
    "I know Python",
    0.9
))


print("\nCOMPLETE AI FLOW")

print(process_answer(
    "I know Python and machine learning",
    0.9
))

print(process_answer(
    "",
    0.2
))

print(process_answer(
    "I worked on Python project ആണ്",
    0.8
))


print("\nBACKGROUND NOISE TESTS")

print(handle_background_noise("", 0.2))

print(handle_background_noise(
    "I know Python",
    0.3
))

print(handle_background_noise(
    "I know Python",
    0.6
))

print(handle_background_noise(
    "I know Python",
    0.9
))
print("\nRETRY TESTS")

print(handle_edge_case("", 0))
print(handle_edge_case("", 1))
print(handle_edge_case("", 2))
print(handle_edge_case("", 3))

print(handle_edge_case("uh", 0))
print(handle_edge_case("uh", 1))
print(handle_edge_case("uh", 2))
print(handle_edge_case("uh", 3))