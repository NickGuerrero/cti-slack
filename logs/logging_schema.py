import time
import uuid

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class LogPhase(str, Enum):
    START = "start"
    DONE = "done"
    ERROR = "error"


def create_correlation_id() -> str:
    return str(uuid.uuid4())


def extract_slack_meta(*, context: Optional[dict] = None, body: Optional[dict] = None) -> Dict[str, Any]:
    """
    Extracts stable-ish identifiers that help:
    - group retries (retry_num/retry_reason)
    - dedupe (event_id)
    - identify interaction source (action_id/view_id/callback_id)
    """
    meta: Dict[str, Any] = {}

    if context:
        # Events API (best dedupe key for events)
        if context.get("event_id"):
            meta["slack_event_id"] = context["event_id"]

        # Slack retries (Bolt often exposes these on context)
        # Depending on adapter/version, these may or may not exist.
        if context.get("retry_num") is not None:
            meta["slack_retry_num"] = context["retry_num"]
        if context.get("retry_reason"):
            meta["slack_retry_reason"] = context["retry_reason"]

    if body:
        # Actions payload
        actions = body.get("actions") or []
        if actions and isinstance(actions, list):
            action0 = actions[0] or {}
            if action0.get("action_id"):
                meta["slack_action_id"] = action0["action_id"]
            if action0.get("block_id"):
                meta["slack_block_id"] = action0["block_id"]
            # Often present for interactivity; can help trace duplicates
            if action0.get("action_ts"):
                meta["slack_action_ts"] = action0["action_ts"]

        view = body.get("view") or {}
        if view.get("id"):
            meta["slack_view_id"] = view["id"]
        if view.get("callback_id"):
            meta["slack_callback_id"] = view["callback_id"]
        if body.get("type"):
            meta["slack_body_type"] = body["type"]

    return meta


@dataclass
class Flow:
    """
    A small helper that:
    - generates correlation_id
    - holds slack metadata
    - tracks timings
    """
    correlation_id: str
    start_ms: int
    slack_meta: Dict[str, Any]

    ack_latency_ms: Optional[int] = None

    @staticmethod
    def start(*, context: Optional[dict] = None, body: Optional[dict] = None) -> Flow:
        return Flow(
            correlation_id=create_correlation_id(),
            start_ms=int(time.time() * 1000),
            slack_meta=extract_slack_meta(context=context, body=body),
        )

    def mark_acked(self, ack_start_ms: int) -> None:
        """
        Call this when ack() is called to track ack latency separately from total duration.

        This is useful because ack latency is often a proxy for Slack retries (if ack is slow, Slack may retry the event, causing duplicate processing).
        """
        self.ack_latency_ms = int(time.time() * 1000) - ack_start_ms

    def duration_ms(self) -> int:
        return int(time.time() * 1000) - self.start_ms

    def base_fields(self) -> Dict[str, Any]:
        fields: Dict[str, Any] = {
            "correlation_id": self.correlation_id,
            **self.slack_meta,
        }
        if self.ack_latency_ms is not None:
            fields["ack_latency_ms"] = self.ack_latency_ms
        return fields
