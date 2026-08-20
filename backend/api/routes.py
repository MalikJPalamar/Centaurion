from dataclasses import asdict
from typing import Optional

from fastapi import APIRouter, Query
from api.mock_data import (
    get_dashboard_stats,
    get_ai_operations,
    create_ai_operation,
    get_operation_by_id,
    get_market_intelligence,
    generate_report,
    get_pipelines,
    trigger_pipeline,
    get_health_status,
    get_settings,
    update_settings
)

router = APIRouter()

@router.get("/dashboard/stats")
async def dashboard_stats():
    return get_dashboard_stats()

@router.get("/ai-operations")
async def list_ai_operations():
    return get_ai_operations()

@router.post("/ai-operations")
async def create_operation(operation: dict):
    return create_ai_operation(operation)

@router.get("/ai-operations/{operation_id}")
async def get_operation(operation_id: str):
    return get_operation_by_id(operation_id)

@router.get("/market/intelligence")
async def market_intelligence():
    return get_market_intelligence()

@router.post("/market/generate")
async def create_report(request: dict):
    return generate_report(request)

@router.get("/cicd/pipelines")
async def list_pipelines():
    return get_pipelines()

@router.post("/cicd/trigger")
async def trigger_cicd(request: dict):
    return trigger_pipeline(request)

@router.get("/cicd/health")
async def health():
    return get_health_status()

@router.get("/settings")
async def settings():
    return get_settings()

@router.put("/settings")
async def save_settings(settings_data: dict):
    return update_settings(settings_data)


# ---------------------------------------------------------------------------
# /doctor/trajectory — provenance query routes (WO-025)
# ---------------------------------------------------------------------------

from lib.trajectory import TrajectoryReader

_trajectory_reader = TrajectoryReader()


@router.get("/doctor/trajectory/files")
async def trajectory_files(wo: Optional[str] = Query(None)):
    """List trajectory log files, optionally filtered by WO."""
    return [str(f.name) for f in _trajectory_reader.list_files(wo=wo)]


@router.get("/doctor/trajectory/query")
async def trajectory_query(
    wo: Optional[str] = Query(None),
    phase: Optional[str] = Query(None),
    after: Optional[str] = Query(None),
    before: Optional[str] = Query(None),
):
    """Query trajectory entries with optional filters."""
    entries = _trajectory_reader.query(wo=wo, phase=phase, after=after, before=before)
    return [asdict(e) for e in entries]


@router.get("/doctor/trajectory/provenance")
async def trajectory_provenance(
    wo: str = Query(...),
    action_index: int = Query(...),
):
    """Answer: 'which skill/policy caused action N in WO-xxx?'"""
    entry = _trajectory_reader.provenance(wo, action_index)
    if entry is None:
        return {"error": f"No action at index {action_index} for {wo}"}
    return asdict(entry)
