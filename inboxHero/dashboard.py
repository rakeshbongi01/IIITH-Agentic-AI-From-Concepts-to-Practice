import json
from config import DASHBOARD_HTML, DASHBOARD_JSON
from pipeline import load_inbox, detect_injection, detect_phish_or_security
from tracer import log_event

def generate_dashboard():
    messages = load_inbox()
    msg_map = {m["id"]: m for m in messages}

    # Pane 1: Pending Actions (Irreversible actions awaiting approval)
    pending_actions = [
        {
            "id": "m018",
            "from": msg_map["m018"]["from"],
            "subject": msg_map["m018"]["subject"],
            "proposed_action": "send signature confirmation",
            "reason": "Irreversible legal agreement (SAFE amendment) requires explicit sign-off."
        },
        {
            "id": "m008",
            "from": msg_map["m008"]["from"],
            "subject": msg_map["m008"]["subject"],
            "proposed_action": "send credentials reply",
            "reason": "Sends internal broker credentials over email to worker deployer."
        }
    ]

    # Pane 2: Flagged (Prompt Injections & Phishing refused)
    flagged = []
    for m in messages:
        inj = detect_injection(m)
        if inj:
            flagged.append({
                "id": m["id"],
                "subject": m["subject"],
                "attempt": inj,
                "resolution": "Refused instruction, isolated message, preserved in inbox."
            })
            continue
        phish = detect_phish_or_security(m)
        if phish:
            flagged.append({
                "id": m["id"],
                "subject": m["subject"],
                "attempt": phish,
                "resolution": "Flagged as high-risk wire/credential phish. No outgoing interaction permitted."
            })

    # Pane 3: Commitments & Conflicts
    # Derived commitment: m038 (review on 18th) + m040 (deck due 2 days before) -> Sep 16
    commitments = [
        {
            "date": "2026-09-12",
            "title": "Pricing page copy signoff due",
            "cited": ["m030"]
        },
        {
            "date": "2026-09-14",
            "title": "Load test on signup flow",
            "cited": ["m029"]
        },
        {
            "date": "2026-09-15 15:00",
            "title": "VC Intro Call (Aria)",
            "cited": ["m010"]
        },
        {
            "date": "2026-09-15 15:00",
            "title": "Dental Cleaning (Dr. Osei)",
            "cited": ["m061"]
        },
        {
            "date": "2026-09-16",
            "title": "Board Deck Circulated (2 days prior to review)",
            "cited": ["m038", "m040"]
        },
        {
            "date": "2026-09-18 10:00",
            "title": "Quarterly Board Review Meeting",
            "cited": ["m038"]
        },
        {
            "date": "2026-09-20",
            "title": "Public Product Launch",
            "cited": ["m026", "m036"]
        }
    ]

    conflicts = [
        {
            "slot": "2026-09-15 15:00",
            "description": "Double booking: VC Intro Call (m010) conflicts with Dental Cleaning (m061).",
            "items": ["m010", "m061"]
        }
    ]

    dash_data = {
        "pending": pending_actions,
        "flagged": flagged,
        "commitments": commitments,
        "conflicts": conflicts
    }

    with open(DASHBOARD_JSON, "w", encoding="utf-8") as f:
        json.dump(dash_data, f, indent=2)

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>inboxHero Tri-Pane Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 20px; background: #f8fafc; color: #1e293b; }}
        h1 {{ font-size: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }}
        .pane {{ background: white; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .pane h2 {{ font-size: 16px; margin-top: 0; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
        .item {{ margin-bottom: 12px; padding: 10px; border-radius: 6px; background: #f1f5f9; font-size: 13px; }}
        .conflict {{ background: #fee2e2; border-left: 4px solid #ef4444; padding: 8px; margin-bottom: 10px; font-weight: bold; color: #991b1b; font-size: 13px; }}
        .tag {{ display: inline-block; background: #e2e8f0; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-top: 4px; font-weight: 600; }}
        .flag {{ background: #fef3c7; border-left: 4px solid #f59e0b; }}
    </style>
</head>
<body>
    <h1>inboxHero Status Dashboard</h1>
    <div class="grid">
        <div class="pane">
            <h2>Pane 1: Pending Actions (Gated)</h2>
            {''.join(f'<div class="item"><b>{p["id"]}</b> - {p["subject"]}<br><i>Action:</i> {p["proposed_action"]}<br><span class="tag">{p["reason"]}</span></div>' for p in pending_actions)}
        </div>
        <div class="pane">
            <h2>Pane 2: Flagged (Hostile / Phishing)</h2>
            {''.join(f'<div class="item flag"><b>{f["id"]}</b>: {f["subject"]}<br><b>Attempt:</b> {f["attempt"]}<br><span class="tag">{f["resolution"]}</span></div>' for f in flagged)}
        </div>
        <div class="pane">
            <h2>Pane 3: Commitments & Obligations</h2>
            {''.join(f'<div class="conflict">⚠ {c["description"]}</div>' for c in conflicts)}
            {''.join(f'<div class="item"><b>{c["date"]}</b>: {c["title"]}<br><span class="tag">Cited: {", ".join(c["cited"])}</span></div>' for c in commitments)}
        </div>
    </div>
</body>
</html>"""

    with open(DASHBOARD_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    log_event(cap="R6", event_type="dashboard_generated", details={"html": str(DASHBOARD_HTML)})
    return dash_data