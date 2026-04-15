import re

def extract_score(text: str) -> float:
    """
    从分析文本中提取分数
    """

    if not text:
        return 0.0

    # 示例：匹配 "评分：85"
    match = re.search(r"(?:评分|score)[:：]\s*(\d+)", text, re.I)

    if match:
        return float(match.group(1))

    # fallback
    return 50.0
