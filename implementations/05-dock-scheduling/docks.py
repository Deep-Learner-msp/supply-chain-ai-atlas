"""
Dock appointment scheduling with OR-Tools CP-SAT, and a re-plan when a truck runs late.

10 trucks arrive at a DC with 3 dock doors. Each has an ETA and an unload time.
Goal: assign each truck a door and a start time so no two trucks share a door
at once, nobody starts before arriving, and total waiting time is as small as possible.

Then truck T4's ETA slips by 50 minutes. We re-plan twice:
  free re-plan   : best total wait, any truck may move
  stable re-plan : best total wait, but moving a truck to another door or
                   shifting its slot by more than 15 minutes costs a penalty
Planners care about the second one: a schedule that changes every time
nobody can follow.

Run: python docks.py
"""

from ortools.sat.python import cp_model

DOORS = 3
TRUCKS = {  # name: (ETA in minutes from 06:00, unload minutes)
    "T1": (0, 45), "T2": (10, 30), "T3": (15, 60), "T4": (30, 45), "T5": (40, 30),
    "T6": (55, 45), "T7": (60, 30), "T8": (75, 60), "T9": (90, 30), "T10": (95, 45),
}
HORIZON = 600


def schedule(trucks, previous=None, stability_weight=0):
    m = cp_model.CpModel()
    start, door_of, waits = {}, {}, []
    per_door = {d: [] for d in range(DOORS)}
    for name, (eta, dur) in trucks.items():
        s = m.NewIntVar(eta, HORIZON, f"s_{name}")
        start[name] = s
        lits = []
        for d in range(DOORS):
            lit = m.NewBoolVar(f"{name}_d{d}")
            iv = m.NewOptionalIntervalVar(s, dur, s + dur, lit, f"iv_{name}_{d}")
            per_door[d].append(iv)
            lits.append(lit)
        m.AddExactlyOne(lits)
        door_of[name] = lits
        waits.append(s - eta)
    for d in range(DOORS):
        m.AddNoOverlap(per_door[d])
    penalties = []
    if previous and stability_weight:
        for name, (pdoor, pstart) in previous.items():
            moved_door = door_of[name][pdoor].Not()
            shift = m.NewIntVar(0, HORIZON, f"shift_{name}")
            m.AddAbsEquality(shift, start[name] - pstart)
            big_shift = m.NewBoolVar(f"big_{name}")
            m.Add(shift > 15).OnlyEnforceIf(big_shift)
            m.Add(shift <= 15).OnlyEnforceIf(big_shift.Not())
            penalties += [moved_door, big_shift]
    m.Minimize(sum(waits) + stability_weight * sum(penalties))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 7
    solver.Solve(m)
    plan = {}
    for name in trucks:
        d = next(i for i, lit in enumerate(door_of[name]) if solver.Value(lit))
        plan[name] = (d, solver.Value(start[name]))
    return plan


def hhmm(minutes):
    return f"{6 + minutes // 60:02d}:{minutes % 60:02d}"


def show(title, trucks, plan, base=None):
    total_wait = sum(plan[n][1] - trucks[n][0] for n in trucks)
    moved = sum(1 for n in plan if base and (plan[n][0] != base[n][0] or abs(plan[n][1] - base[n][1]) > 15))
    print(f"\n{title}: total wait {total_wait} min" + (f", trucks moved {moved}" if base else ""))
    for d in range(DOORS):
        row = sorted((s, n) for n, (dd, s) in plan.items() if dd == d)
        print(f"  Door {d + 1}: " + "  ".join(f"{n} {hhmm(s)}" for s, n in row))


def main():
    base = schedule(TRUCKS)
    show("Original plan", TRUCKS, base)
    late = dict(TRUCKS)
    late["T4"] = (TRUCKS["T4"][0] + 50, TRUCKS["T4"][1])
    print("\nT4 now arrives 50 minutes late.")
    free = schedule(late)
    show("Free re-plan", late, free, base)
    stable = schedule(late, previous=base, stability_weight=30)
    show("Stable re-plan", late, stable, base)


if __name__ == "__main__":
    main()
