TASKS = [
    {
        "name": "easy_ticket",
        "description": "Classify and respond to simple ticket",
        "target": {
            "priority": "high",
            "response_contains": "refund"
        }
    },
    {
        "name": "medium_ticket",
        "description": "Assign correct department and respond",
        "target": {
            "department": "billing",
            "response_contains": "resolved"
        }
    },
    {
        "name": "hard_ticket",
        "description": "Multi-step resolution with correct actions",
        "target": {
            "priority": "high",
            "department": "billing",
            "response_contains": "refund processed"
        }
    }
]