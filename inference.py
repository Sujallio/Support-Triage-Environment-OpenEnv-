import os
import random
from openai import OpenAI
from env.environment import SupportEnv
from env.models import Action

# Try to initialize real API client, fallback to mock if unavailable
client = None
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

api_key = os.getenv("OPENAI_API_KEY")
api_base_url = os.getenv("API_BASE_URL", "https://api.openai.com/v1")

if api_key and not USE_MOCK:
    try:
        client = OpenAI(api_key=api_key, base_url=api_base_url)
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize OpenAI client: {e}")
        print("🔄 Falling back to mock mode (FREE - no charges)\n")
        client = None

# Mock responses for fallback
MOCK_RESPONSES = {
    "payment": ["classify: high", "assign: billing", "respond: refund processed"],
    "app": ["classify: high", "assign: tech", "respond: escalating to engineering team"],
    "refund": ["classify: medium", "assign: billing", "respond: refund initiated"],
    "default": ["classify: medium", "assign: general", "respond: thank you for contacting support"]
}

def get_mock_action(message):
    """Get a mock action based on ticket message"""
    message_lower = message.lower()
    for keyword, responses in MOCK_RESPONSES.items():
        if keyword in message_lower:
            return random.choice(responses)
    return random.choice(MOCK_RESPONSES["default"])

def get_action_text(message):
    """Get action text from API or mock"""
    if client:
        try:
            prompt = f"Ticket: {message}\nWhat should agent do? (answer as 'action_type: value')"
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️  API call failed: {e}")
            print("🔄 Switching to mock mode\n")
            return get_mock_action(message)
    else:
        return get_mock_action(message)

def main():
    mode = "🤖 OpenAI API" if client else "🤖 Mock Mode (FREE)"
    print(f"Support Triage Agent - {mode}")
    print("=" * 60)
    
    env = SupportEnv()
    obs = env.reset()
    total_reward = 0.0

    for step in range(10):
        print(f"\n📋 Step {step + 1}")
        print(f"   Ticket: {obs.message}")
        
        action_text = get_action_text(obs.message)
        
        try:
            action_type, action_value = action_text.split(": ", 1)
            action = Action(action_type=action_type.strip().lower(), value=action_value.strip())
            print(f"   🎯 Action: {action.action_type} -> {action.value}")
        except:
            print(f"   ⚠️  Could not parse action: {action_text}")
            print(f"   Using default: respond")
            action = Action(action_type="respond", value="Thank you for contacting support")

        result = env.step(action)
        obs = result["observation"]
        reward = result["reward"]
        total_reward += reward
        
        print(f"   💎 Reward: {reward:.2f} (Total: {total_reward:.2f})")

        if result["done"]:
            print(f"\n✅ Episode finished at step {step + 1}")
            break

    print("\n" + "=" * 60)
    print(f"🏆 Final Reward: {total_reward:.2f}")
    print("=" * 60)

if __name__ == "__main__":
    main()