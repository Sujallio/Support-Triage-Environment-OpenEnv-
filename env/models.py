from pydantic import BaseModel
from typing import Optional

class Observation(BaseModel):
    ticket_id: int
    message: str
    customer_type: str
    previous_actions: list[str]
    last_action_error: bool = False

class Action(BaseModel):
    action_type: str  # "classify", "assign", "respond"
    value: str

class Reward(BaseModel):
    score: float