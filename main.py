from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from agents import StudyPlannerAgent, simulate_miss_and_replan
from memory import create_user

app = FastAPI()
planner = StudyPlannerAgent()

class PlanRequest(BaseModel):
    user_id: str
    goal: str
    deadline_str: str
    hours_per_day: float
    topics: List[str]
    preferred_times: str = "18:00-21:00"

class AdaptRequest(BaseModel):
    user_id: str
    plan: List[dict]
    miss_index: int

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/plan")
def generate_plan(req: PlanRequest):
    create_user(req.user_id, {"preferred_times":[req.preferred_times]})
    plan = planner.plan(
        req.user_id,
        req.goal,
        req.deadline_str,
        req.hours_per_day,
        req.topics,
        req.preferred_times
    )
    return {"plan": plan}

@app.post("/adapt")
def adapt(req: AdaptRequest):
    updated = simulate_miss_and_replan(req.user_id, req.plan, req.miss_index)
    return {"updated_plan": updated}
