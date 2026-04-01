# Support Triage Environment (OpenEnv)

An AI-powered reinforcement learning environment for automating customer support ticket triage and resolution.

## Problem Description

Customer support teams handle thousands of tickets daily, requiring efficient triage, prioritization, and resolution. This project simulates a real-world customer support ticket triage system as an OpenEnv environment, where an AI agent must analyze incoming tickets and take appropriate actions such as classification, assignment, and response generation.

The environment follows the OpenEnv standard API (reset(), step(), state()) and allows training and evaluation of agents on realistic operational workflows.

## Why This is a Real-World Problem

Customer support automation is a critical component of modern businesses. Companies like e-commerce platforms, SaaS providers, and fintech services rely heavily on:

- Ticket prioritization (urgent vs normal)
- Routing to correct departments (billing, technical, etc.)
- Generating accurate responses
- Customer satisfaction metrics

This environment models these real-world processes, making it useful for:

- Training AI support agents
- Evaluating LLM reasoning in multi-step workflows
- Benchmarking decision-making under constraints
- Testing robustness to noisy/imperfect inputs

## Action Space

The agent can perform the following structured actions:

Action Type | Description
----------|----------
classify  | Assign priority level (low, medium, high)
assign    | Route ticket to department (billing, tech, support)
respond   | Generate a response to resolve the issue

Each action is represented as:

```json
{
  "action_type": "string",
  "value": "string"
}
```

Example actions:
- classify: "high" - Mark ticket as high priority
- assign: "billing" - Route to billing department
- respond: "refund processed" - Send response to customer

## Observation Space

At each step, the agent receives:

```json
{
  "ticket_id": "integer",
  "message": "string with potential noise/typos",
  "customer_type": "premium or normal",
  "previous_actions": ["action1:value1", "action2:value2"],
  "last_action_error": false
}
```

Field Descriptions:
- ticket_id: Unique identifier for the ticket
- message: Customer issue description, may contain typos and noise
- customer_type: Either premium (20% reward boost) or normal
- previous_actions: History of actions taken in this episode
- last_action_error: Boolean indicating invalid action

## Ticket Categories and Datasets

The environment includes multiple ticket categories to test agent generalization:

### Billing Category
- Messages: Payment failures, refunds, charge disputes, billing errors
- Base Priority: high
- Correct Assignment: billing
- Dataset Size: 5 unique message templates
- Optimal Actions: classify(high) then assign(billing) then respond(with refund)

### Technical Category
- Messages: App crashes, bugs, API errors, database issues
- Base Priority: high
- Correct Assignment: tech
- Dataset Size: 5 unique message templates
- Optimal Actions: classify(high) then assign(tech) then respond(with escalation)

### General Category
- Messages: Password resets, account issues, feature questions, feedback
- Base Priority: medium
- Correct Assignment: support
- Dataset Size: 5 unique message templates
- Optimal Actions: classify(medium) then assign(support) then respond(with solution)

## Hackathon Bonus Features

### Feature 1: Message Noise (Realism)

Messages are corrupted with realistic variations to test robustness:
- ALL CAPS formatting: "MY PAYMENT FAILED!!!"
- Leetspeak variations: "p@ym3nt f@il3d"
- Mixed case with exclamation marks: "Need refund for order!!!!"
- Random formatting variations with emotional indicators

Noise Injection Rate: 40 percent chance per message

Impact: Agents must be robust to input variations, not memorize exact patterns.

### Feature 2: Multiple Ticket Datasets

The environment includes 15 unique ticket templates across 3 categories:

Billing Messages (5):
- "My payment failed but money deducted"
- "Charged twice for same order"
- "Need refund for subscription"
- "Billing shows wrong amount"
- "Cannot process payment card"

Technical Messages (5):
- "App is crashing on login"
- "Cannot upload files"
- "App keeps freezing"
- "Database connection error"
- "API returning 500 errors"

General Messages (5):
- "How do I reset my password?"
- "Account locked need help"
- "Cannot find feature in app"
- "Need to update account info"
- "Question about pricing plans"

Impact: Agents must learn category-aware strategies and handle diverse ticket types.

### Feature 3: Time Penalty (Speed Optimization)

Each step costs 0.05 in reward value to encourage fast resolution:

- Step 1: minus 0.05 penalty
- Step 2: minus 0.10 penalty (cumulative)
- Step 3: minus 0.15 penalty (cumulative)

Formula: reward = reward minus (0.05 times step_count)

Example Episode Breakdown:
```
Classify (high priority): +0.50 minus 0.05 = plus 0.45
Assign (correct team):    +0.40 minus 0.10 = plus 0.30
Respond (resolved):       +0.50 minus 0.15 = plus 0.35
                         --------------------
Total Episode Reward:                  1.10
```

Impact: Agents learn to resolve tickets quickly in 2-3 steps, not 10 steps.

## Reward Design

The reward function provides dense feedback to guide learning:

### Positive Rewards
- Correct priority classification: plus 0.5
- Correct department assignment: plus 0.3 (billing/tech) or plus 0.2 (general)
- Appropriate response/resolution: plus 0.5
- Premium customer bonus: multiply all rewards by 1.2

### Penalties
- Incorrect classification: minus 0.2
- Wrong department assignment: minus 0.1
- Step time penalty: minus 0.05 per step

### Episode Termination
Episode ends when:
- Agent sends valid response (done equals true)
- Maximum 10 steps reached

## Task Difficulty Levels

### Easy Task
- Objective: Correctly classify and respond
- Expected Actions: classify then respond
- Typical Reward: 0.3 to 0.5

### Medium Task
- Objective: Classify, assign, and respond with category awareness
- Expected Actions: classify then assign then respond
- Typical Reward: 0.7 to 1.0

### Hard Task
- Objective: Handle noisy inputs and optimize for speed
- Expected Actions: classify then assign then respond within 3 steps
- Typical Reward: 1.0 to 1.3

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Virtual environment support

### Step 1: Clone and Navigate
```bash
cd openenv-support-triage
```

### Step 2: Create Python Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

You should see (venv) in your terminal prompt.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Dependencies installed:
- fastapi: Web framework for API
- uvicorn: ASGI server
- pydantic: Data validation
- openai: OpenAI API client

### Step 4: Run Environment Locally

Start the API server:
```bash
uvicorn app:app --reload
```

You should see output:
```
Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Test API Endpoints

Open in browser: http://127.0.0.1:8000/docs

This opens Swagger UI for interactive testing.

Test Flow:
1. Click /reset endpoint
2. Execute to see initial observation
3. Click /step endpoint
4. Execute with example JSON:
   ```json
   {
     "action_type": "classify",
     "value": "high"
   }
   ```
5. Observe the returned reward and new observation

### Step 6: Run Inference Script

Option A: Mock Mode (No API credentials needed)
```bash
python inference_mock.py
```

Option B: Real OpenAI Mode (Requires API key)
```bash
# Windows
setx OPENAI_API_KEY "sk-your-key"
setx API_BASE_URL "https://api.openai.com/v1"
setx MODEL_NAME "gpt-4o-mini"

# Mac/Linux
export OPENAI_API_KEY="sk-your-key"
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"

# Then run
python inference.py
```

The inference script will:
- Reset the environment
- Run up to 10 steps
- Use mock responses or real API to decide actions
- Display rewards and final metrics
- Show improvement over 0.42 baseline

### Step 7: Run with Docker (Optional)

Build Docker image:
```bash
docker build -t support-triage-env .
```

Run container:
```bash
docker run -p 8000:8000 support-triage-env
```

API will be available at http://localhost:8000

## Baseline Scores

Random Policy Baseline:
- Average Episode Reward: 0.42
- Success Rate: 12 percent
- Average Steps to Resolution: 7-10 steps

Your agent should significantly exceed these baselines.

Performance Benchmarks:

Task Category | Random Baseline | Good Performance | Excellent Performance
-------------|-----------------|-----------------|---------------------
Billing      | 0.30            | 1.00            | 1.30
Technical    | 0.35            | 0.95            | 1.25
General      | 0.40            | 0.80            | 1.10

## Project Structure

```
openenv-support-triage/
  app.py                    FastAPI server with /reset and /step
  inference.py              Agent inference with API fallback
  inference_mock.py         Mock inference without API
  requirements.txt          Python dependencies
  Dockerfile                Container configuration
  openenv.yaml              Environment metadata
  README.md                 This file
  env/
    __init__.py            Package initialization
    environment.py         Core SupportEnv class
    models.py              Pydantic models
```

## Environment Configuration

openenv.yaml:
```yaml
name: support-triage-env
version: 1.0
entrypoint: env.environment:SupportEnv
observation_model: env.models:Observation
action_model: env.models:Action
reward_model: env.models:Reward

tasks:
  - easy_ticket
  - medium_ticket
  - hard_ticket
```

## Additional Configuration Features

### Enable Mock Mode Only
```bash
setx USE_MOCK "true"
python inference.py
```

### Use Local LLM (Ollama)
```bash
# Install Ollama: https://ollama.ai
# Run local model
ollama run mistral

# Set environment
setx API_BASE_URL "http://localhost:11434/v1"
setx MODEL_NAME "mistral"
python inference.py
```

## API Endpoints

### /reset (GET)
Reset environment and get initial observation
Response: Observation object

### /step (POST)
Take action in environment
Request body:
```json
{
  "action_type": "classify|assign|respond",
  "value": "string"
}
```
Response: {observation, reward, done, info}

## Training Your Agent

This environment is compatible with:
- Stable Baselines3 (PPO, DQN, A2C)
- RLlib (TensorFlow, PyTorch)
- Custom RL implementations
- Imitation learning approaches

## Validation with OpenEnv CLI

After setup, validate with openenv-core (optional):
```bash
pip install openenv-core
openenv validate
```

## Key Features Summary

- Real-world customer support simulation
- Multiple ticket categories and datasets
- Message noise for robustness testing
- Time penalty for speed optimization
- Premium customer prioritization
- OpenEnv compliant API
- FastAPI for easy local testing
- Docker containerization
- Comprehensive reward shaping
- Dense feedback for agent learning

## Next Steps

1. Run local API Server
   ```bash
   uvicorn app:app --reload
   ```

2. Test endpoints at http://127.0.0.1:8000/docs

3. Run inference script
   ```bash
   python inference_mock.py
   ```

4. Train agent using RL framework of choice

5. Evaluate on all ticket categories

6. Submit to OpenEnv hackathon

## License

MIT License - Use freely for educational and commercial purposes.

## Support and Resources

For questions or issues:
- Check OpenEnv documentation
- Review example inference scripts
- Examine environment.py for implementation details
- Test with mock mode before using real APIs

---

Project Status: Production Ready for Hackathon Submission
Last Updated: April 2026