import re


def extract_score(text):
    patterns = [
        r"总分[:：]\s*(\d{1,3})",
        r"综合评分[:：]\s*(\d{1,3})",
        r"评分[:：]\s*(\d{1,3})"
    ]

    for pat in patterns:
        match = re.search(pat, text)
        if match:
            score = int(match.group(1))
            return max(0, min(100, score))

    return 60
