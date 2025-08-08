"""FastAPI server for the LinkedIn Automation Platform.

This module exposes the public API used to orchestrate investor
workflows. The implementation intentionally keeps state in memory and
focuses on demonstrating the request/response contract described in the
project documentation.
"""

from __future__ import annotations

import asyncio
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI(title="LinkedIn Automation Platform")

# ----------------------------------------------------------------------------
# In-memory storage used for the demo implementation. A real deployment would
# persist this information in a database and coordinate with the agent system.
# ----------------------------------------------------------------------------
workflows: Dict[str, Dict] = {}
progress_updates: Dict[str, int] = {}
budget_config: Dict[str, float] = {}

AVAILABLE_PROVIDERS = ["claude", "openai", "gemini", "grok"]
TEMPLATES = {
    "claude": "investor_search_claude",
    "openai": "investor_search_openai",
    "gemini": "investor_search_gemini",
    "grok": "investor_search_grok",
}


class WorkflowRequest(BaseModel):
    """Request body for starting a workflow."""

    startup_url: str
    budget_cap: Optional[float] = None
    providers: List[str] = []
    max_investors: Optional[int] = None


@app.post("/start_workflow")
async def start_workflow(
    request: WorkflowRequest, background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """Create a new investor discovery workflow.

    The heavy lifting would normally be delegated to the coordinator agent
    through a background task. Here we only register a stub workflow entry.
    """

    workflow_id = f"wf_{uuid4().hex}"
    workflows[workflow_id] = {
        "id": workflow_id,
        "status": "running",
        "stage": "initialized",
        "progress": 0,
        "cost_used": 0.0,
        "investors_found": 0,
    }
    progress_updates[workflow_id] = 0
    # background_tasks.add_task(coordinator.start_workflow, workflow_id, request)
    return {"id": workflow_id}


@app.get("/workflow/{workflow_id}/status")
async def workflow_status(workflow_id: str) -> Dict:
    """Return the status of a workflow."""

    wf = workflows.get(workflow_id)
    if wf is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return wf


@app.post("/workflow/{workflow_id}/stop")
async def stop_workflow(workflow_id: str) -> Dict:
    """Stop a running workflow."""

    wf = workflows.get(workflow_id)
    if wf is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    wf["status"] = "stopped"
    return wf


class ExpansionRequest(BaseModel):
    """Simple body for an expansion request."""

    query: str


@app.post("/expansion/start")
async def expansion_start(request: ExpansionRequest) -> Dict[str, str]:
    expansion_id = f"ex_{uuid4().hex}"
    workflows[expansion_id] = {
        "id": expansion_id,
        "status": "running",
        "stage": "expansion",
        "progress": 0,
    }
    return {"id": expansion_id, "status": "started"}


@app.get("/expansion/{expansion_id}/status")
async def expansion_status(expansion_id: str) -> Dict[str, str]:
    wf = workflows.get(expansion_id)
    if wf is None:
        raise HTTPException(status_code=404, detail="Expansion not found")
    return wf


@app.get("/expansion/{expansion_id}/results")
async def expansion_results(expansion_id: str) -> Dict:
    if expansion_id not in workflows:
        raise HTTPException(status_code=404, detail="Expansion not found")
    return {"id": expansion_id, "results": []}


@app.get("/progress/{job_id}")
async def get_progress(job_id: str) -> Dict[str, int]:
    progress = progress_updates.get(job_id, 0)
    return {"job_id": job_id, "progress": progress}


@app.websocket("/ws/progress/{job_id}")
async def websocket_progress(websocket: WebSocket, job_id: str) -> None:
    await websocket.accept()
    try:
        while True:
            progress = progress_updates.get(job_id, 0)
            await websocket.send_json({"job_id": job_id, "progress": progress})
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass


@app.get("/config/providers")
async def config_providers() -> Dict[str, List[str]]:
    return {"providers": AVAILABLE_PROVIDERS}


class BudgetConfig(BaseModel):
    budget: float


@app.post("/config/budget")
async def set_budget(config: BudgetConfig) -> Dict[str, float]:
    budget_config["budget"] = config.budget
    return {"budget": config.budget}


@app.get("/config/templates")
async def get_templates() -> Dict[str, Dict]:
    return {"templates": TEMPLATES}
