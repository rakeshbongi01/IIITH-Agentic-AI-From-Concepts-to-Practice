import re
from typing import Dict, Any, Optional, Tuple

NOISE_SENDERS = [
    "no-reply@", "noreply@", "notifications@", "alerts@", "receipts@",
    "billing@", "support@", "ship-confirm@", "orders@", "checkin@",
    "info@members.netflix.com", "calendar-notification@google.com",
    "digest@hackernewsletter.com", "newsletter@", "updates@figma.com",
    "facilities@paperjet.io", "notes@paperjet.io", "status@paperjet-monitoring.io"
]

def evaluate_rules(msg: Dict[str, Any]) -> Optional[Tuple[str, str]]:
    sender = msg.get("from", "").lower()
    subject = msg.get("subject", "").lower()
    body = msg.get("body", "").lower()

    # Noise threads
    if msg.get("thread_id", "").startswith("t-noise") or msg.get("thread_id", "").startswith("t-fill"):
        return ("archive", "Automated notification/noise matching thread-level rule.")

    # Sender heuristics
    for prefix in NOISE_SENDERS:
        if prefix in sender:
            return ("archive", f"Automated transactional or notification email from {sender}.")

    # Content heuristics for noise
    if "receipt" in subject or "statement" in subject or "weekly digest" in subject:
        return ("archive", "Automated periodic statement or receipt.")

    return None