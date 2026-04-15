print("🔥 ranker.py LOADED")
def rank_candidates(results):
    print("🔥 ranker function called", results)
    return sorted(results, key=lambda x: x.get("score", 0), reverse=True)
