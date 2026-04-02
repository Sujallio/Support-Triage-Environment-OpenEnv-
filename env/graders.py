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
    
    Scoring:
    - Correct classification: 0.5 points
    - Correct response (with refund/resolution): 0.5 points
    
    Max score: 1.0
    """
    score = 0.0
    message = (state_data.get("message", "") if state_data else "").lower()
    
    # Check for correct classification (0.5)
    if any("classify" in h and "high" in h for h in history):
        if any(cat in message for cat in ["payment", "refund", "crash", "error"]):
            score += 0.5
    
    # Check for correct response (0.5)
    if any("respond" in h for h in history):
        if any(keyword in h.lower() for h in history for keyword in ["refund", "resolved", "fixed", "reset"]):
            score += 0.5
    
    return min(score, 1.0)


def grade_medium(history, state_data=None):
    """
    Medium Task Grader
    Objective: Classify, assign to correct department, and respond
    
    Scoring:
    - Correct classification: 0.35 points
    - Correct assignment: 0.35 points
    - Appropriate response: 0.30 points
    
    Max score: 1.0
    """
    score = 0.0
    message = (state_data.get("message", "") if state_data else "").lower()
    category = state_data.get("category", "general") if state_data else "general"
    
    # Classification (0.35)
    if any("classify" in h and ("high" in h or "medium" in h) for h in history):
        score += 0.35
    
    # Assignment (0.35) - check correct department
    correct_assignments = {
        "billing": ["billing", "payment", "finance"],
        "technical": ["tech", "engineering", "dev"],
        "general": ["support", "customer"]
    }
    
    target_depts = correct_assignments.get(category, ["support"])
    if any("assign" in h and any(dept in h.lower() for dept in target_depts) for h in history):
        score += 0.35
    
    # Response (0.30)
    if any("respond" in h for h in history):
        if len(h) > 10 for h in history if "respond" in h:
            score += 0.30
    
    return min(score, 1.0)


def grade_hard(history, state_data=None):
    """
    Hard Task Grader
    Objective: Multi-step resolution with noisy input handling and speed
    
    Scoring:
    - Correct classification with noisy input: 0.30 points
    - Correct assignment to department: 0.30 points
    - Complete appropriate resolution: 0.25 points
    - Efficiency bonus (<=3 steps): 0.15 points
    
    Max score: 1.0
    """
    score = 0.0
    message = (state_data.get("message", "") if state_data else "").lower()
    category = state_data.get("category", "general") if state_data else "general"
    steps_taken = len(history)
    
    # Classification (0.30) - must handle noise
    if any("classify" in h and "high" in h for h in history):
        if any(cat in message for cat in ["payment", "charged", "deducted", "crash", "error", "app"]):
            score += 0.30
    
    # Assignment (0.30) - must route correctly
    correct_assignments = {
        "billing": ["billing", "payment", "finance"],
        "technical": ["tech", "engineering", "dev", "escalat"],
        "general": ["support", "customer"]
    }
    
    target_depts = correct_assignments.get(category, ["support"])
    if any("assign" in h and any(dept in h.lower() for dept in target_depts) for h in history):
        score += 0.30
    
    # Resolution (0.25) - appropriate response type
    if any("respond" in h for h in history):
        response_quality = 0
        for h in history:
            if "respond" in h:
                if "refund" in h.lower() or "credit" in h.lower():
                    response_quality = max(response_quality, 0.25)
                elif "escalat" in h.lower() or "engineer" in h.lower():
                    response_quality = max(response_quality, 0.25)
                elif len(h) > 15:
                    response_quality = max(response_quality, 0.15)
        score += response_quality
    
    # Efficiency bonus (0.15) - encourage fast resolution
    if steps_taken <= 3:
        score += 0.15
    elif steps_taken <= 5:
        score += 0.10
    elif steps_taken <= 7:
        score += 0.05
    
    return min(score, 1.0)