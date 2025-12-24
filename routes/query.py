from fastapi import APIRouter, Depends
from fastapi_limiter import FastAPILimiter
from starlette.requests import Request
from starlette.responses import Response

from pydantic_ai.ag_ui import handle_ag_ui_request

from GraphBuilder import State, agents

limiter = FastAPILimiter()

router = APIRouter(prefix="/api/query", tags=["query"])


def _get_last_user_text(payload: dict) -> str:
    for m in reversed(payload.get("messages", [])):
        role = (m.get("role") or m.get("type") or "").lower()
        if role == "user":
            content = m.get("content")
            return content.strip() if isinstance(content, str) else str(content)
    return ""


@router.post("/ag-ui")
@limiter.limit("5/minute")
async def query_ag_ui(request: Request) -> Response:
    payload = await request.json()

    user_text = _get_last_user_text(payload)
    if not user_text:
        return Response(
            '{"error":"No user message found"}',
            media_type="application/json",
            status_code=422,
        )

    state = State(agent_messages=[])
    router_result = await agents["Router"].run(user_text)
    agent_name = router_result.output.agent.value
    agent = agents[agent_name]

    return await handle_ag_ui_request(
        agent,
        request,
    )
