import json
from typing import Dict, Any
from config import OUTBOX_DIR
from tracer import log_event

def require_approval(action: str, target_id: str, details: Dict[str, Any], dry_run: bool = False) -> bool:
    print(f"\n[GATE PROPOSAL] Action: {action.upper()} | Target: {target_id}")
    print(f"Details: {json.dumps(details, indent=2)}")

    if dry_run:
        print("[GATE RESULT] Dry-run enabled: Action suppressed. (0 outbox writes)")
        log_event(cap="R3", event_type="gate", details={
            "action": action, "target_id": target_id, "approved": False, "mode": "dry_run"
        })
        return False

    choice = input("Approve this irreversible action? (y/N): ").strip().lower()
    approved = choice in ["y", "yes"]
    log_event(cap="R3", event_type="gate", details={
        "action": action, "target_id": target_id, "approved": approved, "mode": "interactive"
    })
    return approved

def execute_send(msg_id: str, recipient: str, subject: str, body: str, dry_run: bool = False) -> bool:
    details = {"to": recipient, "subject": subject, "body_preview": body[:120]}
    if not require_approval("send", msg_id, details, dry_run=dry_run):
        return False

    out_path = OUTBOX_DIR / f"{msg_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"to": recipient, "subject": subject, "body": body}, f, indent=2)
    print(f"[EXECUTED] Message written to {out_path}")
    return True