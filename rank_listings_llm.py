
def rank_listings(listings, required_terms=None):
    def score(listing):
        score = 0
        if required_terms:
            for term in required_terms:
                if term.lower() in listing["title"].lower():
                    score += 2
                if term.lower() in listing["description"].lower():
                    score += 1
        score += len(listing["description"]) / 100
        return score

    return max(listings, key=score)
