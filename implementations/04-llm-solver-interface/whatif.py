"""
LLM as the interface, solver as the engine (the OptiGuide pattern).

A small network: 3 plants ship to 4 distribution centres. A linear program
(OR-Tools, GLOP solver) finds the cheapest plan. A planner asks "what if" questions in plain
words. The translator turns each question into a structured change, the
solver re-optimizes, and the answer explains the difference.

The translator below is a few rules so the demo runs offline. Set
ANTHROPIC_API_KEY and ANTHROPIC_MODEL to let an LLM do the translation instead;
the solver part does not change. The LLM never produces the plan itself.

Run: python whatif.py
"""

import copy
import json
import os
import re

from ortools.linear_solver import pywraplp

BASE = {
    "capacity": {"Chennai": 500, "Pune": 400, "Delhi": 500},
    "demand": {"Mumbai": 300, "Bengaluru": 250, "Kolkata": 200, "Hyderabad": 220},
    "cost": {  # cost per unit shipped
        "Chennai": {"Mumbai": 9, "Bengaluru": 3, "Kolkata": 10, "Hyderabad": 5},
        "Pune": {"Mumbai": 2, "Bengaluru": 6, "Kolkata": 12, "Hyderabad": 5},
        "Delhi": {"Mumbai": 11, "Bengaluru": 13, "Kolkata": 7, "Hyderabad": 10},
    },
}


def solve(net):
    s = pywraplp.Solver.CreateSolver("GLOP")
    x = {(p, d): s.NumVar(0, s.infinity(), f"x_{p}_{d}") for p in net["capacity"] for d in net["demand"]}
    for p, cap in net["capacity"].items():
        s.Add(sum(x[p, d] for d in net["demand"]) <= cap)
    for d, dem in net["demand"].items():
        s.Add(sum(x[p, d] for p in net["capacity"]) >= dem)
    s.Minimize(sum(net["cost"][p][d] * x[p, d] for p, d in x))
    if s.Solve() != pywraplp.Solver.OPTIMAL:
        return None
    flows = {k: v.solution_value() for k, v in x.items() if v.solution_value() > 1e-6}
    return {"cost": s.Objective().Value(), "flows": flows}


def rule_translator(q):
    """Stand-in for an LLM: maps a question to a structured change."""
    q = q.lower()
    if m := re.search(r"(\w+) (?:plant )?(?:shuts|closes|goes down)", q):
        return {"op": "capacity", "node": m.group(1).title(), "value": 0}
    if m := re.search(r"demand (?:in|at) (\w+) (?:rises|increases|grows) (?:by )?(\d+)%", q):
        return {"op": "demand_pct", "node": m.group(1).title(), "value": int(m.group(2))}
    if m := re.search(r"(\w+) to (\w+) (?:costs?|freight) (?:rises|doubles)", q):
        return {"op": "cost_mult", "node": [m.group(1).title(), m.group(2).title()], "value": 2}
    return None


def llm_translator(q):
    import anthropic  # pip install anthropic
    client = anthropic.Anthropic()
    prompt = ("Turn the planner's question into ONE JSON object with keys op, node, value. "
              "op is one of capacity (node=plant, value=new capacity), demand_pct (node=DC, value=percent), "
              "cost_mult (node=[plant, DC], value=multiplier). Plants: Chennai, Pune, Delhi. "
              "DCs: Mumbai, Bengaluru, Kolkata, Hyderabad. Reply with JSON only.\nQuestion: " + q)
    msg = client.messages.create(model=os.environ["ANTHROPIC_MODEL"], max_tokens=200,
                                 messages=[{"role": "user", "content": prompt}])
    return json.loads(msg.content[0].text)


def apply(net, ch):
    net = copy.deepcopy(net)
    if ch["op"] == "capacity":
        net["capacity"][ch["node"]] = ch["value"]
    elif ch["op"] == "demand_pct":
        net["demand"][ch["node"]] = round(net["demand"][ch["node"]] * (1 + ch["value"] / 100))
    elif ch["op"] == "cost_mult":
        p, d = ch["node"]
        net["cost"][p][d] *= ch["value"]
    return net


def explain(base, new):
    if new is None:
        return "No feasible plan: demand can't be met with the remaining capacity."
    delta = new["cost"] - base["cost"]
    lanes = sorted(set(base["flows"]) | set(new["flows"]))
    changes = []
    for lane in lanes:
        a, b = base["flows"].get(lane, 0), new["flows"].get(lane, 0)
        if abs(a - b) > 0.5:
            changes.append(f"{lane[0]}->{lane[1]} {a:.0f}->{b:.0f}")
    return (f"Total cost {base['cost']:,.0f} -> {new['cost']:,.0f} ({delta:+,.0f}).\n"
            f"   Volume changes: {'; '.join(changes) or 'none'}.")


def main():
    use_llm = bool(os.environ.get("ANTHROPIC_API_KEY") and os.environ.get("ANTHROPIC_MODEL"))
    translate = llm_translator if use_llm else rule_translator
    base = solve(BASE)
    print(f"Baseline plan cost: {base['cost']:,.0f}")
    for p, d in base["flows"]:
        print(f"  {p:>8} -> {d:<10} {base['flows'][p, d]:>5.0f} units")
    questions = [
        "What if the Pune plant shuts for a week?",
        "What if demand in Mumbai rises 20%?",
        "What if Chennai to Bengaluru freight doubles?",
        "What if we hire more drivers?",
    ]
    for q in questions:
        ch = translate(q)
        print(f"\nQ: {q}\n   change: {ch}")
        print("   " + (explain(base, solve(apply(BASE, ch))) if ch else "Couldn't translate; asking the planner to rephrase."))


if __name__ == "__main__":
    main()
