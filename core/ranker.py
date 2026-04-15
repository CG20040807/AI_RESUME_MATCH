def rank(results):
    return sorted(results, key=lambda x: x["score"], reverse=True)
