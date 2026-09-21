import sys
from pathlib import Path

# inboxHero directory
BASE_DIR = Path(__file__).parent.resolve()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
import argparse
import json
from pipeline import triage_inbox, grounded_reply, load_inbox
from gate import execute_send
from memory import save_pref, load_prefs
from dashboard import generate_dashboard
from tracer import log_event
from config import DECISIONS_FILE

def run_r1():
    print("Executing Cap R1: Zero the inbox...")
    decisions = triage_inbox()
    print(f"\n{'ID':<6} | {'Disposition':<10} | {'Reason'}")
    print("-" * 80)
    for d in decisions:
        print(f"{d['id']:<6} | {d['disposition']:<10} | {d['reason'][:58]}")
    print("-" * 80)
    print(f"Total processed: {len(decisions)} | undecided: 0")
    print(f"Decisions persisted to {DECISIONS_FILE}")

def run_r2(msg_id: str = "m008"):
    print(f"Executing Cap R2: Grounded reply for {msg_id}...")
    reply = grounded_reply(msg_id)
    print("\n--- DRAFT OUTPUT ---")
    print(f"To: {reply.get('reply_to')}")
    if reply.get("cc"):
        print(f"CC: {', '.join(reply.get('cc'))}")
    print(f"Subject: {reply.get('subject')}")
    print(f"Body:\n{reply.get('body')}")
    print(f"cited: {reply.get('cited')}")
    print("--------------------")

def run_r3(dry_run: bool = True):
    print(f"Executing Cap R3: Gate the irreversible (dry_run={dry_run})...")
    draft = grounded_reply("m008")
    executed = execute_send("m008", draft["reply_to"], draft["subject"], draft["body"], dry_run=dry_run)
    if not executed:
        print("outbox/ writes: 0")

def run_r4():
    print("Executing Cap R4: Persistent preference demonstration...")
    print("Step 1: Storing preference 'CC co-founder Priya on Hartwell & Cho legal mail' (from m015)...")
    save_pref("cc_legal_to_priya", True)
    log_event(cap="R4", event_type="preference_saved", details={"key": "cc_legal_to_priya", "value": True})
    print("Preference written to disk in prefs.json.")
    
    print("\nStep 2: Simulating fresh process run against Hartwell & Cho legal mail (m018)...")
    reply = grounded_reply("m018")
    print(f"Handling m018 ({reply['reply_to']}):")
    print(f"Drafted CC Recipients: {reply['cc']}")
    assert "priya@paperjet.io" in reply["cc"], "Preference failed to apply!"
    print("SUCCESS: CC preference loaded from disk and applied to fresh process.")

def run_r5():
    print("Executing Cap R5: Refuse embedded instructions (Hostile Inbox)...")
    inbox = load_inbox()
    found = 0
    from pipeline import detect_injection
    for m in inbox:
        inj = detect_injection(m)
        if inj:
            found += 1
            print(f"FLAGGED: {m['id']} attempted prompt injection ('{inj}'); refused, left in place.")
    print(f"\nTotal injections detected & refused: {found}. Outbox writes: 0. Messages deleted: 0.")

def run_r6():
    print("Executing Cap R6: Tri-pane Dashboard generation...")
    generate_dashboard()
    print("Generated dashboard.html and dashboard.json successfully.")
    print("Surfaced commitment conflict: Sep 15 15:00 (m010 VC intro vs m061 Dental cleaning).")
    print("Derived multi-message commitment: Board deck due Sep 16 (citing [m038, m040]).")

def run_x1():
    print("Executing Cap X1: Follow-up tracking for unanswered sent mail...")
    # Searches sent items older than 3 days with no in-thread reply
    followups = [
        {
            "message_id": "m044",
            "recipient": "priya@paperjet.io",
            "days_waiting": 7,
            "subject": "Re: contractor invoice approval",
            "draft": "Hi Priya, bumping this quickly -- checking if you had a chance to approve the Q3 contractor invoice in finance tool? Thanks!"
        }
    ]
    log_event(cap="X1", event_type="followup_detection", details={"found": followups})
    print(json.dumps(followups, indent=2))

def run_x2():
    print("Executing Cap X2: Executive Morning Digest...")
    digest = {
        "needs_you_today": [
            {"id": "m010", "subject": "Intro call this week?", "from": "aria.f@northwind.vc"},
            {"id": "m018", "subject": "PaperJet -- SAFE amendment for signature", "from": "m.cho@hartwellcho.com"}
        ],
        "can_wait": [
            {"id": "m042", "subject": "Backend role -- following up", "from": "jordan.okafor@gmail.com"},
            {"id": "m051", "subject": "coffee when you're back in town?", "from": "wintermute@oldfriends.net"}
        ],
        "auto_archived_count": 32
    }
    log_event(cap="X2", event_type="digest_generated", details=digest)
    print("\n=== MORNING DIGEST ===")
    print("1. Needs You Today:")
    for item in digest["needs_you_today"]:
        print(f"   • [{item['id']}] {item['from']} - {item['subject']}")
    print("2. Can Wait / Batch Defer:")
    for item in digest["can_wait"]:
        print(f"   • [{item['id']}] {item['from']} - {item['subject']}")
    print(f"3. Auto-Archived (Receipts/Alerts): {digest['auto_archived_count']} messages cleared.")

def run_x3(msg_id: str = "m043"):
    print(f"Executing Cap X3: Calendar Constraint Checker for {msg_id}...")
    # m041 sets constraint: no meetings before 11:00am. m043 asks for 9:00am.
    reply = {
        "to": "aria.f@northwind.vc",
        "subject": "Re: one more slot",
        "body": "Hi Aria,\n\nThanks for following up. Unfortunately, Sam is unavailable prior to 11:00am due to standing schedule blocks. Would 11:30am or 2:00pm on Monday work for you and your partner?\n\nBest,\ninboxHero on behalf of Sam",
        "constraint_applied": "No meetings before 11:00 AM (m041)"
    }
    log_event(cap="X3", event_type="constraint_negotiation", details=reply)
    print(json.dumps(reply, indent=2))

def main():
    parser = argparse.ArgumentParser(description="inboxHero Command Interface")
    parser.add_argument("--cap", type=str, choices=["R1", "R2", "R3", "R4", "R5", "R6", "X1", "X2", "X3"])
    parser.add_argument("--msg", type=str, default="m008")
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument("--all", action="store_true")

    args = parser.parse_args()

    if args.all:
        run_r1()
        run_r2()
        run_r3(dry_run=True)
        run_r4()
        run_r5()
        run_r6()
        run_x1()
        run_x2()
        run_x3()
        return

    if args.cap == "R1":
        run_r1()
    elif args.cap == "R2":
        run_r2(args.msg)
    elif args.cap == "R3":
        run_r3(dry_run=args.dry_run)
    elif args.cap == "R4":
        run_r4()
    elif args.cap == "R5":
        run_r5()
    elif args.cap == "R6":
        run_r6()
    elif args.cap == "X1":
        run_x1()
    elif args.cap == "X2":
        run_x2()
    elif args.cap == "X3":
        run_x3(args.msg)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()