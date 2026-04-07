"""
Graders for Support Triage Environment

Three difficulty levels: easy, medium, hard
Scores range from 0.0 to 1.0
Based on action history and task completion
"""

def grade_easy(history, state_data=None):
    """
    Easy Task Grader
    Objective: Classify and respond to a ticket
    
    Scoring: Between 0.01 and 0.99
    - Base: 0.01 (always > 0)
    - Correct classification: +0.35
    - Correct response: +0.35
    - Accuracy bonus: +0.28
    """
    score = 0.01  # Baseline (always > 0)
    message = (state_data.get("message", "") if state_data else "").lower()
    
    # Check for correct classification (0.35)
    if any("classify" in h and "high" in h for h in history):
        if any(cat in message for cat in ["payment", "refund", "crash", "error"]):
            score += 0.35
    
    # Check for correct response (0.35)
    if any("respond" in h for h in history):
        if any(keyword in h.lower() for h in history for keyword in ["refund", "resolved", "fixed", "reset"]):
            score += 0.35
    
    # Bonus for efficiency (0.28)
    if len(history) <= 3:
        score += 0.28
    
    return min(score, 0.99)  # Cap at 0.99 (always < 1)


def grade_medium(history, state_data=None):
    """
    Medium Task Grader
    Objective: Classify, assign to correct department, and respond
    
    Scoring: Between 0.01 and 0.99
    - Base: 0.01 (always > 0)
    - Correct classification: +0.28
    - Correct assignment: +0.28
    - Appropriate response: +0.24
    - Explanation bonus: +0.18
    
    Max score: 0.99
    """
    score = 0.01  # Baseline (always > 0)
    message = (state_data.get("message", "") if state_data else "").lower()
    category = state_data.get("category", "general") if state_data else "general"
    
    # Classification (0.28)
    if any("classify" in h and ("high" in h or "medium" in h) for h in history):
        score += 0.28
    
    # Assignment (0.28) - check correct department
    correct_assignments = {
        "billing": ["billing", "payment", "finance"],
        "technical": ["tech", "engineering", "dev"],
        "general": ["support", "customer"]
    }
    
    target_depts = correct_assignments.get(category, ["support"])
    if any("assign" in h and any(dept in h.lower() for dept in target_depts) for h in history):
        score += 0.28
    
    # Response (0.24)
    if any("respond" in h and len(h) > 10 for h in history):
        score += 0.24
    
    # Explanation bonus (0.18)
    if any(len(h) > 15 for h in history):
        score += 0.18
    
    return min(score, 0.99)  # Cap at 0.99 (always < 1)


def grade_hard(history, state_data=None):
    """
    Hard Task Grader
    Objective: Multi-step resolution with noisy input handling and speed
    
    Scoring: Between 0.01 and 0.99
    - Base: 0.01 (always > 0)
    - Correct classification with noisy input: +0.24
    - Correct assignment to department: +0.24
    - Complete appropriate resolution: +0.20
    - Efficiency bonus (<=3 steps): +0.12
    - Additional efficiency: +0.08
    
    Max score: 0.99
    """
    score = 0.01  # Baseline (always > 0)
    message = (state_data.get("message", "") if state_data else "").lower()
    category = state_data.get("category", "general") if state_data else "general"
    steps_taken = len(history)
    
    # Classification (0.24) - must handle noise
    if any("classify" in h and "high" in h for h in history):
        if any(cat in message for cat in ["payment", "charged", "deducted", "crash", "error", "app"]):
            score += 0.24
    
    # Assignment (0.24) - must route correctly
    correct_assignments = {
        "billing": ["billing", "payment", "finance"],
        "technical": ["tech", "engineering", "dev", "escalat"],
        "general": ["support", "customer"]
    }
    
    target_depts = correct_assignments.get(category, ["support"])
    if any("assign" in h and any(dept in h.lower() for dept in target_depts) for h in history):
        score += 0.24
    
    # Resolution (0.20) - appropriate response type
    if any("respond" in h for h in history):
        response_quality = 0
        for h in history:
            if "respond" in h:
                if "refund" in h.lower() or "credit" in h.lower():
                    response_quality = max(response_quality, 0.20)
                elif "escalat" in h.lower() or "engineer" in h.lower():
                    response_quality = max(response_quality, 0.20)
                elif len(h) > 15:
                    response_quality = max(response_quality, 0.12)
        score += response_quality
    
    # Efficiency bonus (0.20 total across tiers) - encourage fast resolution
    if steps_taken <= 3:
        score += 0.12
    elif steps_taken <= 5:
        score += 0.08
    elif steps_taken <= 7:
        score += 0.03
    
    return min(score, 0.99)  # Cap at 0.99 (always < 1)