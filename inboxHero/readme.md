# inboxHero

**GitHub Repository:** https://github.com/rakeshbongi01/IIITH-Agentic-AI-From-Concepts-to-Practice/tree/main/inboxHero


inboxHero is a capability-driven agentic triage system designed to transition an inbox from unread to empty while maintaining defensive boundaries against prompt injection and isolating irreversible actions behind human-in-the-loop gates.

---

## 1. System Architecture

The system operates via a deterministic, modular pipeline consisting of four primary stages:
1. **Security & Injection Scanner (`pipeline.py`):** Inbound message bodies are analyzed for prompt injection patterns (e.g., hidden administrative commands, exfiltration instructions) and business email compromise (BEC) / phishing signatures. Hostile messages are flagged and isolated without deletion.
2. **Rule-Based Triage (`rules.py`):** Routine notifications, newsletters, receipts, and system alerts are matched against deterministic sender patterns and thread metadata. These messages are assigned an `archive` disposition without incurring LLM latency or token usage.
3. **Context Retrieval & Decision Engine (`pipeline.py`, `memory.py`):** High-priority messages are contextualized using thread-walk retrieval to pull verified historical facts (e.g., staging credentials) and check against persistent user preferences.
4. **Execution & Human-in-the-Loop Gate (`gate.py`):** Reversible actions are logged directly. Irreversible actions (`send`, `delete`) must route through an interactive approval gate or an explicit `--dry-run` barrier before writing to the filesystem.

Every stage writes structured audit logs to `trace.jsonl` with capability identifiers (`cap=R1`–`R6`, `X1`–`X3`) to maintain full process observability.

---

## 2. Framework Choice

**Framework: None (Pure Standard Python)**

- **Rationale:** The triage workflow is fundamentally a structured, linear pipeline with distinct conditional branches (rule path vs. model path).
- **Why Avoided Multi-Agent Frameworks:** Orchestration frameworks such as CrewAI, AutoGen, or LangGraph introduce heavy abstraction layers, non-deterministic re-prompt loops, high execution overhead, and potential failure modes in prompt encapsulation. Writing the architecture in standard Python provides direct control over memory persistence, gate enforcement, reproducible CLI invocation, and error handling.

---

## 3. Disposition Vocabulary

Every message in the inbox is assigned exactly one disposition with an explanatory reason:

- `reply`: The inbound message requires outgoing communication, clarification, or answering an explicit query.
- `archive`: Routine notifications, transactional receipts, system alerts, or completed threads requiring no human intervention.
- `defer`: Non-urgent communications, networking outreach, or low-priority reading suitable for later review.
- `delegate`: An actionable task or decision assigned to an external team member or colleague.
- `escalate`: Critical security anomalies, detected prompt injections, wire transfer/phishing attempts, or sensitive legal agreements requiring immediate owner attention.

---

## 4. Reversible vs. Irreversible Classification & The Gate

### Action Classification
- **Irreversible Actions:** `send`, `delete`.
  - *Why:* A sent message cannot be un-sent once transmitted to an external recipient. Deleting is treated as irreversible in this architecture because the mock storage environment lacks a soft-delete/trash recovery buffer.
- **Reversible Actions:** `draft`, `label`, `archive`, `defer`.
  - *Why:* Drafts can be edited or deleted prior to release; archive, defer, and label statuses can be toggled without permanent data loss.

### Gate Implementation
- The boundary is implemented in `gate.py` through the `require_approval()` function.
- No message can be written to `outbox/` without explicitly passing this gate.
- The gate offers two enforcement modes:
  1. **Dry-Run Mode (`--dry-run`):** Intercepts proposed actions, displays the full payload details, logs the proposal to `trace.jsonl`, and guarantees `outbox/ writes: 0`.
  2. **Interactive Mode:** Pauses execution, prints the action metadata, and prompts the operator (`y/N`). Execution proceeds only upon explicit human approval.

### Escalation Line & Trade-offs
- The escalation threshold is set strictly at **money, legal commitments, and external sends**. Routine receipts, status pings, and internal notification archives run automatically to protect the user from approval fatigue. 
- **Trade-off:** If an internal notification or routine email is misclassified as noise and auto-archived, the user might miss a non-critical update; however, this completely prevents the user from rubber-stamping critical financial or legal actions without reading them.

---

## 5. Retrieval Approach

**Method: Thread-Walk Retrieval**

- Inboxes naturally preserve relational conversation structure via `thread_id` and ISO timestamps.
- For any grounded reply (e.g., capability `R2` for message `m008`), the retrieval engine queries the inbox for all messages sharing the target's `thread_id` that precede it in chronological order.
- Thread-walk retrieval guarantees complete extraction precision for exact strings (such as the AMQP staging URL from `m003`) while completely eliminating embedding latency, vector index construction, and semantic retrieval drift.
- If required data is not present in the thread history, the engine refuses to hallucinate facts and leaves the draft empty.

---

## 6. Final Report Answers

### 1. What did you refuse to automate?
We deliberately refused to automate message `m021` (an urgent banking remittance instruction to wire $8,400 to Meridian Trust) and message `m023` (an executive spoofing wire request for $3,200). Autonomous execution of financial disbursements or alterations to banking details creates asymmetric, unrecoverable liabilities that cannot be corrected with an undo operation. Both messages are classified under the `escalate` disposition and isolated for manual verification.

### 2. Where does untrusted text enter your system?
Untrusted text enters through the `body` and `subject` fields of incoming mail items. Our architecture encapsulates raw email text into isolated data structures that are processed strictly as unexecuted parameters by an injection scanner before reaching any drafting or reasoning logic. An attacker attempting to force data exfiltration (e.g., `m024` attempting to forward the inbox, or `m047` requesting revenue copies) would have to defeat both the regex/semantic scanner in `pipeline.py` and the hardcoded programmatic gate in `gate.py` that blocks writing to `outbox/` without interactive terminal input.

### 3. Who is accountable when it sends the wrong thing?
The human operator is ultimately accountable for any communication sent under the owner's name. The system enforces this accountability via the Part 4 gate: the assistant may generate candidate drafts, but cannot deliver them without explicit human approval. If a mistake occurs, `inboxHero` provides full auditability through `trace.jsonl`, which logs the source message IDs cited, the exact draft payload, the gate timestamp, and whether approval was granted.

### 4. Name your own machinery.
In our implementation, the classification and grounded drafting routines in `pipeline.py` serve as **Agents**; citation verification, injection detection, and gate approvals function as **Tasks**; the linear loop in `demo.py` functions as the **Crew**; and `rules.py` operates as the deterministic **Router**. Multi-agent frameworks provide prebuilt message-passing abstractions and agent persona definitions. However, utilizing a framework here would have added unnecessary execution latency, non-deterministic token loops, and opaque state management, whereas our custom pipeline delivers deterministic, transparent CLI capabilities with low latency.

---

## 7. Execution & Verification

Run the full test suite across all capabilities:
python demo.py --all

