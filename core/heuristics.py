# import re

# SENSATIONAL = [
#     "leaked", "shocking", "urgent", "secret",
#     "exposed", "miracle", "deepfake", "hoax"
# ]

# # def detect_red_flags(text: str) -> list:
# #     flags = []
# #     t = text.lower()

# #     for w in SENSATIONAL:
# #         if w in t:
# #             flags.append(f"Sensational phrase: '{w}'")

# #     if len(text.split()) < 30:
# #         flags.append("Very short claim")

# #     if text.count("!") >= 3:
# #         flags.append("Excessive emotional punctuation")

# #     if re.search(r"\d+%", text):
# #         flags.append("Numeric claim without citation")

# #     return flags
def detect_red_flags(text: str):
    flags = []

    if len(text.split()) < 6:
        flags.append("Very short claim")

    if any(x in text.lower() for x in ["killed", "dies", "dead", "plane crash"]):
        flags.append("High-risk event claim")

    if any(c.isdigit() for c in text):
        flags.append("Numeric claim without citation")

    return flags
