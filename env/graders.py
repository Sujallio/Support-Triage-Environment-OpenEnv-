def grade_easy(history):
    score = 0.0
    for h in history:
        if "classify:high" in h:
            score += 0.5
        if "respond" in h and "refund" in h:
            score += 0.5
    return min(score, 1.0)


def grade_medium(history):
    score = 0.0
    if any("assign:billing" in h for h in history):
        score += 0.5
    if any("respond" in h for h in history):
        score += 0.5
    return score


def grade_hard(history):
    score = 0.0
    if any("classify:high" in h for h in history):
        score += 0.3
    if any("assign:billing" in h for h in history):
        score += 0.3
    if any("refund" in h for h in history):
        score += 0.4
    return score