def rank_candidates(results):
    """
    按 score 降序排序
    """
    if not results:
        return []

    return sorted(
        results,
        key=lambda x: x.get("score", 0),
        reverse=True
    )
