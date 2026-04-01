import random
from env.models import Observation, Action

class SupportEnv:
    # Multiple ticket datasets by category
    TICKET_DATASETS = {
        "billing": {
            "category": "billing",
            "base_priority": "high",
            "agent": "billing",
            "messages": [
                "My payment failed but money deducted",
                "Charged twice for same order",
                "Need refund for subscription",
                "Billing shows wrong amount",
                "Cannot process payment card",
            ]
        },
        "technical": {
            "category": "technical",
            "base_priority": "high",
            "agent": "tech",
            "messages": [
                "App is crashing on login",
                "Cannot upload files",
                "App keeps freezing",
                "Database connection error",
                "API returning 500 errors",
            ]
        },
        "general": {
            "category": "general",
            "base_priority": "medium",
            "agent": "support",
            "messages": [
                "How do I reset my password?",
                "Account locked need help",
                "Can't find feature in app",
                "Need to update account info",
                "Question about pricing plans",
            ]
        }
    }
    
    # Typos and noise patterns
    NOISE_PATTERNS = [
        lambda s: s.upper(),  # ALL CAPS
        lambda s: s.lower() + "!!!",  # Lowercase with exclamation
        lambda s: s.replace("a", "@").replace("e", "3"),  # L33T speak
        lambda s: random.choice([s[:-1], s, s + " :("]),  # Variations
    ]

    def __init__(self):
        self.state_data = None
        self.step_count = 0
        self.category = None

    def _add_noise(self, message):
        """Add realistic typos and formatting noise to messages"""
        if random.random() < 0.4:  # 40% chance of noise
            return random.choice(self.NOISE_PATTERNS)(message)
        return message

    def reset(self):
        self.step_count = 0
        # Select a random category
        self.category = random.choice(list(self.TICKET_DATASETS.keys()))
        dataset = self.TICKET_DATASETS[self.category]
        
        # Select a raw message from the category
        raw_message = random.choice(dataset["messages"])
        
        # Add noise for realism
        message_with_noise = self._add_noise(raw_message)
        
        self.state_data = {
            "ticket_id": random.randint(1, 10000),
            "message": message_with_noise,
            "category": self.category,
            "base_priority": dataset["base_priority"],
            "correct_agent": dataset["agent"],
            "customer_type": random.choice(["premium", "normal"]),
            "history": []
        }
        return self._get_obs()

    def _get_obs(self):
        return Observation(
            ticket_id=self.state_data["ticket_id"],
            message=self.state_data["message"],
            customer_type=self.state_data["customer_type"],
            previous_actions=self.state_data["history"],
            last_action_error=False
        )

    def step(self, action: Action):
        self.step_count += 1
        reward = 0.0
        done = False
        message = self.state_data["message"].lower()

        # Reward shaping with category-aware logic
        if action.action_type == "classify":
            # Correct priority classification
            if self.state_data["base_priority"] == "high" and action.value.lower() in ["high", "critical"]:
                reward += 0.5
            elif self.state_data["base_priority"] == "medium" and action.value.lower() in ["medium"]:
                reward += 0.3
            else:
                reward -= 0.2

        elif action.action_type == "assign":
            # Correct team assignment
            if action.value.lower() in ["billing", "billing team"] and self.category == "billing":
                reward += 0.4
            elif action.value.lower() in ["tech", "technical", "engineering"] and self.category == "technical":
                reward += 0.4
            elif action.value.lower() in ["support", "general", "customer support"] and self.category == "general":
                reward += 0.3
            else:
                reward -= 0.1

        elif action.action_type == "respond":
            # Reward for appropriate responses
            if ("refund" in action.value.lower() or "credit" in action.value.lower()) and self.category == "billing":
                reward += 0.5
                done = True
            elif ("escalat" in action.value.lower() or "engineer" in action.value.lower()) and self.category == "technical":
                reward += 0.4
                done = True
            elif len(action.value) > 10:  # Meaningful response
                reward += 0.2
                done = True

        # TIME PENALTY: Encourage quick resolution
        time_penalty = 0.05 * self.step_count
        reward -= time_penalty

        # Premium customer bonus
        if self.state_data["customer_type"] == "premium":
            reward *= 1.2  # 20% bonus for premium customers

        self.state_data["history"].append(f"{action.action_type}:{action.value}")

        return {
            "observation": self._get_obs(),
            "reward": reward,
            "done": done,
            "info": {
                "category": self.category,
                "time_penalty": time_penalty,
                "step": self.step_count
            }
        }

    def state(self):
        return self.state_data