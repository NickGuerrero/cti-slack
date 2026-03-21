from typing import Any, Dict, Optional

from .logging_schema import Flow, LogPhase


def log_trigger_start(
    logger,
    *,
    flow: Flow,
    trigger_type: str,
    trigger_name: str,
    user_id: str,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    payload = {
        "phase": LogPhase.START.value,
        "trigger_type": trigger_type,
        "trigger_name": trigger_name,
        "user_id": user_id,
        **flow.base_fields(),
    }
    if extra:
        payload.update(extra)
    logger.info(payload)


def log_done(logger, *, flow: Flow, extra: Optional[Dict[str, Any]] = None) -> None:
    payload = {
        "phase": LogPhase.DONE.value,
        "duration_ms": flow.duration_ms(),
        **flow.base_fields(),
    }
    if extra:
        payload.update(extra)
    logger.info(payload)


def log_error(logger, *, flow: Flow, err: Exception, extra: Optional[Dict[str, Any]] = None) -> None:
    payload = {
        "phase": LogPhase.ERROR.value,
        "duration_ms": flow.duration_ms(),
        "error_type": type(err).__name__,
        "error": str(err),
        **flow.base_fields(),
    }
    if extra:
        payload.update(extra)
    logger.error(payload)
