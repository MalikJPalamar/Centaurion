import uuid
from datetime import datetime
from typing import List, Dict, Any

mock_ai_operations = [
    {
        "id": "op-001",
        "name": "Market Analysis - Tech Sector",
        "type": "market_analysis",
        "status": "completed",
        "created_at": "2026-03-13T10:30:00Z",
        "completed_at": "2026-03-13T10:45:00Z",
        "result": "Analysis complete - 47 opportunities identified"
    },
    {
        "id": "op-002",
        "name": "Competitor Monitoring",
        "type": "monitoring",
        "status": "running",
        "created_at": "2026-03-13T11:00:00Z",
        "progress": 65
    },
    {
        "id": "op-003",
        "name": "Content Generation - Q1 Report",
        "type": "content_generation",
        "status": "queued",
        "created_at": "2026-03-13T11:30:00Z"
    },
    {
        "id": "op-004",
        "name": "Data Processing Pipeline",
        "type": "data_processing",
        "status": "completed",
        "created_at": "2026-03-12T14:00:00Z",
        "completed_at": "2026-03-12T14:30:00Z",
        "result": "Processed 15,000 records"
    },
    {
        "id": "op-005",
        "name": "Sentiment Analysis",
        "type": "nlp_analysis",
        "status": "failed",
        "created_at": "2026-03-12T09:00:00Z",
        "error": "API rate limit exceeded"
    }
]

mock_pipelines = [
    {
        "id": "pipe-001",
        "name": "Production Deploy",
        "status": "success",
        "last_run": "2026-03-13T08:00:00Z",
        "duration": "4m 32s",
        "branch": "main"
    },
    {
        "id": "pipe-002",
        "name": "Staging Deploy",
        "status": "running",
        "last_run": "2026-03-13T11:00:00Z",
        "progress": 78,
        "branch": "develop"
    },
    {
        "id": "pipe-003",
        "name": "Integration Tests",
        "status": "success",
        "last_run": "2026-03-13T07:30:00Z",
        "duration": "12m 15s",
        "branch": "main"
    },
    {
        "id": "pipe-004",
        "name": "Security Scan",
        "status": "failed",
        "last_run": "2026-03-12T22:00:00Z",
        "duration": "8m 45s",
        "error": "2 medium vulnerabilities found"
    }
]

mock_health = {
    "api": {"status": "healthy", "latency": "12ms"},
    "database": {"status": "healthy", "latency": "8ms"},
    "cache": {"status": "healthy", "latency": "2ms"},
    "ai_service": {"status": "healthy", "latency": "145ms"},
    "external_apis": {"status": "degraded", "latency": "320ms"}
}

mock_settings = {
    "api_keys": {
        "openai": "",
        "anthropic": "",
        "market_data": ""
    },
    "notifications": {
        "email": True,
        "slack": False,
        "discord": False
    },
    "preferences": {
        "theme": "dark",
        "auto_refresh": True,
        "refresh_interval": 30
    }
}


def get_dashboard_stats():
    return {
        "total_operations": 127,
        "active_operations": 3,
        "completed_today": 12,
        "success_rate": 94.5,
        "system_health": 98,
        "active_pipelines": 2,
        "recent_activity": [
            {"type": "operation", "message": "Market Analysis completed", "time": "10m ago"},
            {"type": "pipeline", "message": "Production Deploy succeeded", "time": "2h ago"},
            {"type": "system", "message": "Health check passed", "time": "5m ago"}
        ]
    }


def get_ai_operations():
    return {"operations": mock_ai_operations, "total": len(mock_ai_operations)}


def create_ai_operation(operation: Dict[str, Any]):
    new_op = {
        "id": f"op-{uuid.uuid4().hex[:6]}",
        "name": operation.get("name", "Untitled Operation"),
        "type": operation.get("type", "general"),
        "status": "queued",
        "created_at": datetime.now().isoformat() + "Z"
    }
    mock_ai_operations.insert(0, new_op)
    return new_op


def get_operation_by_id(operation_id: str):
    for op in mock_ai_operations:
        if op["id"] == operation_id:
            return op
    return {"error": "Operation not found"}


def get_market_intelligence():
    return {
        "sectors": [
            {"name": "Technology", "sentiment": "bullish", "change": 2.4},
            {"name": "Healthcare", "sentiment": "neutral", "change": 0.8},
            {"name": "Finance", "sentiment": "bullish", "change": 1.2},
            {"name": "Energy", "sentiment": "bearish", "change": -1.5}
        ],
        "trends": [
            {"topic": "AI Automation", "volume": 15420, "sentiment": 0.78},
            {"topic": "Cloud Computing", "volume": 12300, "sentiment": 0.65},
            {"topic": "Cybersecurity", "volume": 9800, "sentiment": 0.82}
        ],
        "competitors": [
            {"name": "TechCorp Inc", "mention_volume": 450, "sentiment": 0.62},
            {"name": "DataSystems", "mention_volume": 320, "sentiment": 0.71},
            {"name": "CloudNine", "mention_volume": 280, "sentiment": 0.55}
        ]
    }


def generate_report(request: Dict[str, Any]):
    return {
        "id": f"report-{uuid.uuid4().hex[:8]}",
        "status": "generating",
        "type": request.get("type", "summary"),
        "estimated_time": "2 minutes"
    }


def get_pipelines():
    return {"pipelines": mock_pipelines, "total": len(mock_pipelines)}


def trigger_pipeline(request: Dict[str, Any]):
    return {
        "id": f"pipe-{uuid.uuid4().hex[:6]}",
        "name": request.get("name", "Manual Trigger"),
        "status": "running",
        "started_at": datetime.now().isoformat() + "Z",
        "branch": request.get("branch", "main")
    }


def get_health_status():
    return {
        "status": "operational",
        "services": mock_health,
        "last_check": datetime.now().isoformat() + "Z"
    }


def get_settings():
    return mock_settings


def update_settings(settings_data: Dict[str, Any]):
    mock_settings.update(settings_data)
    return {"status": "saved", "settings": mock_settings}
