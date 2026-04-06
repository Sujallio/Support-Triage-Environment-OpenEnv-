from fastapi import FastAPI, Body
from env.environment import SupportEnv
from env.models import Action

app = FastAPI()
env = SupportEnv()

@app.get("/reset")
@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs}

@app.post("/step")
def step(action: dict = Body(..., example={"action_type": "classify", "value": "high"})):
    try:
        # Convert dict to Action object
        action_obj = Action(
            action_type=action.get("action_type", "respond"),
            value=action.get("value", "")
        )
        # Step the environment
        result = env.step(action_obj)
        return result
    except Exception as e:
        return {"error": str(e), "observation": None, "reward": 0.0, "done": True, "info": {}}