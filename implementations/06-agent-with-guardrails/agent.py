"""
An agent with guardrails: chasing a missing proof of delivery (POD).

Load L-1042 was delivered, but no POD arrived, so the customer won't pay the
invoice. The agent's job: get the POD from the carrier and close the case.

The pattern this demo shows (the same with or without an LLM):
  1. The agent may only call tools on an ALLOWED list.
  2. Tools that move money or make promises need a human approval.
  3. Every step is written to an audit log.
  4. The run stops after a fixed number of steps.

The planner below is a small rule-based policy so the demo runs offline.
Swap in an LLM planner that returns the same {"tool": ..., "args": ...}
shape; the guardrail layer does not change.

Run: python agent.py
"""

import json

# ---------- the world (simulated systems) ----------
WORLD = {
    "shipment": {"id": "L-1042", "carrier": "Ravi Transport", "status": "delivered", "pod": None,
                 "invoice": 1850, "customer": "Acme Foods"},
    "inbox": [],
    "carrier_will_reply_after": 2,  # carrier replies on the 2nd inbox check
}


def lookup_shipment(_): return dict(WORLD["shipment"])


def email_carrier(args):
    WORLD["sent"] = WORLD.get("sent", 0) + 1
    return {"sent_to": WORLD["shipment"]["carrier"], "body": args["body"]}


def check_inbox(_):
    WORLD["checks"] = WORLD.get("checks", 0) + 1
    if WORLD.get("sent") and WORLD["checks"] >= WORLD["carrier_will_reply_after"]:
        return {"messages": [{"from": "Ravi Transport", "attachment": "POD_L-1042.pdf"}]}
    return {"messages": []}


def attach_pod(args):
    WORLD["shipment"]["pod"] = args["file"]
    return {"ok": True}


def issue_credit(args): return {"credited": args["amount"]}
def pay_carrier(args): return {"paid": args["amount"]}


TOOLS = {"lookup_shipment": lookup_shipment, "email_carrier": email_carrier, "check_inbox": check_inbox,
         "attach_pod": attach_pod, "issue_credit": issue_credit, "pay_carrier": pay_carrier}

# ---------- guardrails ----------
ALLOWED = {"lookup_shipment", "email_carrier", "check_inbox", "attach_pod", "issue_credit", "close_case"}
NEEDS_APPROVAL = {"issue_credit"}  # anything that moves money
MAX_STEPS = 8


def approver(tool, args):
    """A human in the loop. Here: policy says no credits while a POD may still arrive."""
    return False, "POD is still being chased; no credit yet."


# ---------- the planner (stand-in for an LLM) ----------
def planner(state):
    s = state.get("shipment")
    if s is None:
        return {"tool": "lookup_shipment", "args": {}}
    if s["pod"]:
        return {"tool": "close_case", "args": {"note": "POD attached, invoice can be released"}}
    if state.get("pod_file"):
        return {"tool": "attach_pod", "args": {"file": state["pod_file"]}}
    if state["step"] == 2 and not state.get("tried_credit"):
        state["tried_credit"] = True  # a tempting shortcut the guardrails should stop
        return {"tool": "issue_credit", "args": {"amount": s["invoice"]}}
    if state["step"] == 3 and not state.get("tried_pay"):
        state["tried_pay"] = True  # a tool the agent is not allowed to use at all
        return {"tool": "pay_carrier", "args": {"amount": 500}}
    if not state.get("emailed"):
        state["emailed"] = True
        return {"tool": "email_carrier", "args": {"body": f"Please send the POD for {s['id']}. Thank you."}}
    return {"tool": "check_inbox", "args": {}}


def run():
    state, log = {"step": 0}, []
    while state["step"] < MAX_STEPS:
        state["step"] += 1
        act = planner(state)
        tool, args = act["tool"], act["args"]
        entry = {"step": state["step"], "tool": tool, "args": args}
        if tool not in ALLOWED:
            entry["result"] = "BLOCKED: tool not on the allowed list"
        elif tool in NEEDS_APPROVAL:
            ok, why = approver(tool, args)
            entry["result"] = TOOLS[tool](args) if ok else f"DENIED by approver: {why}"
        elif tool == "close_case":
            entry["result"] = "case closed"
            log.append(entry)
            break
        else:
            out = TOOLS[tool](args)
            entry["result"] = json.loads(json.dumps(out))  # snapshot for the audit log
            if tool == "lookup_shipment":
                state["shipment"] = dict(out)
            if tool == "check_inbox" and out["messages"]:
                state["pod_file"] = out["messages"][0]["attachment"]
            if tool == "attach_pod":
                state["shipment"]["pod"] = args["file"]
        log.append(entry)
    else:
        log.append({"step": state["step"], "tool": None, "result": "STOPPED: step limit reached"})
    return log


def main():
    for e in run():
        res = e["result"] if isinstance(e["result"], str) else json.dumps(e["result"])
        print(f"{e['step']:>2}. {e['tool']!s:<16} -> {res}")
    print("\nThe agent did the coordination. The guardrails blocked one unapproved tool, "
          "held one money action for a human, and logged every step.")


if __name__ == "__main__":
    main()
