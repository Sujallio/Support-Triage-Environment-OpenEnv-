from fastapi import FastAPI
from env.environment import SupportEnv

app = FastAPI()
env = SupportEnv()

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: dict):
    return env.step(action)