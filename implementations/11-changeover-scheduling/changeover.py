"""
Sequencing jobs on a line with sequence-dependent changeovers (OR-Tools CP-SAT).

A paint line runs 12 jobs in one long shift. Switching colour needs a clean:
light to dark is quick, dark to light needs a full wash. The changeover time
depends on the order, so the sequence decides how much of the shift is
spent cleaning instead of making paint.

We compare four sequences:
  FIFO            : the order the jobs arrived
  Due date (EDD)  : earliest due date first, the usual planner rule
  CP-SAT min clean: least total changeover time
  CP-SAT on time  : fewest late jobs first, then least changeover

The line starts clean on White. All data are synthetic and illustrative.

Run: python changeover.py
"""

from ortools.sat.python import cp_model

COLOURS = ["White", "Yellow", "Red", "Blue", "Black"]  # light to dark
# Changeover minutes from row colour to column colour
CHANGE = [
    [0, 10, 20, 25, 30],
    [40, 0, 15, 25, 30],
    [60, 45, 0, 20, 25],
    [70, 60, 40, 0, 20],
    [90, 80, 60, 45, 0],
]
JOBS = [  # name, colour, run minutes, due (minutes after shift start), in arrival order
    ("J1", "Blue", 50, 240), ("J2", "White", 40, 120), ("J3", "Black", 60, 600),
    ("J4", "Yellow", 45, 180), ("J5", "White", 30, 420), ("J6", "Red", 55, 360),
    ("J7", "Black", 40, 720), ("J8", "Yellow", 35, 300), ("J9", "Blue", 45, 540),
    ("J10", "Red", 50, 480), ("J11", "White", 35, 660), ("J12", "Yellow", 40, 780),
]
START_COLOUR = "White"
HORIZON = 2000


def change(a, b):
    return CHANGE[COLOURS.index(a)][COLOURS.index(b)]


def evaluate(order):
    t, colour, total_change, late, tardy = 0, START_COLOUR, 0, 0, 0
    for i in order:
        _, c, run, due = JOBS[i]
        total_change += change(colour, c)
        t += change(colour, c) + run
        late += t > due
        tardy += max(0, t - due)
        colour = c
    return total_change, t, late, tardy


def solve(late_weight):
    m = cp_model.CpModel()
    n = len(JOBS)
    start = [m.NewIntVar(0, HORIZON, f"s{i}") for i in range(n)]
    is_late = [m.NewBoolVar(f"late{i}") for i in range(n)]
    arcs, change_terms, succ = [], [], {}
    for i in range(n):  # node 0 is the shift start/end, job i is node i + 1
        _, ci, run_i, due_i = JOBS[i]
        first = m.NewBoolVar(f"first{i}")
        arcs += [(0, i + 1, first), (i + 1, 0, m.NewBoolVar(f"last{i}"))]
        m.Add(start[i] >= change(START_COLOUR, ci)).OnlyEnforceIf(first)
        change_terms.append(change(START_COLOUR, ci) * first)
        succ[(0, i)] = first
        m.Add(start[i] + run_i <= due_i).OnlyEnforceIf(is_late[i].Not())
        for j in range(n):
            if i == j:
                continue
            lit = m.NewBoolVar(f"{i}to{j}")
            arcs.append((i + 1, j + 1, lit))
            c = change(ci, JOBS[j][1])
            m.Add(start[j] >= start[i] + run_i + c).OnlyEnforceIf(lit)
            change_terms.append(c * lit)
            succ[(i + 1, j)] = lit
    m.AddCircuit(arcs)
    m.Minimize(late_weight * sum(is_late) + sum(change_terms))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 3
    solver.Solve(m)
    order, node = [], 0
    while len(order) < n:
        node = next(j for j in range(n) if (node, j) in succ and solver.Value(succ[(node, j)]))
        order.append(node)
        node += 1
    return order


def main():
    sequences = {
        "FIFO": list(range(len(JOBS))),
        "Due date (EDD)": sorted(range(len(JOBS)), key=lambda i: JOBS[i][3]),
        "CP-SAT min clean": solve(late_weight=0),
        "CP-SAT on time": solve(late_weight=1000),
    }
    print(f"{len(JOBS)} jobs, {len(COLOURS)} colours, line starts on {START_COLOUR}\n")
    print(f"{'Sequence':<17} {'Changeover':>10} {'Makespan':>9} {'Late jobs':>9} {'Tardiness':>9}")
    print("-" * 58)
    rows = {}
    for name, order in sequences.items():
        rows[name] = evaluate(order)
        ch, span, late, tardy = rows[name]
        print(f"{name:<17} {ch:>6} min {span:>5} min {late:>9} {tardy:>5} min")
    for name, order in sequences.items():
        print(f"  {name:<17} " + " ".join(f"{JOBS[i][0]}:{JOBS[i][1][:2]}" for i in order))
    fifo, best = rows["FIFO"], rows["CP-SAT on time"]
    print(f"\nThe on-time sequence cuts cleaning from {fifo[0]} to {best[0]} min and late jobs "
          f"from {fifo[2]} to {best[2]}.")
    print("Sequence by changeover and due date together; pure due-date order wastes the shift on cleaning.")


if __name__ == "__main__":
    main()
