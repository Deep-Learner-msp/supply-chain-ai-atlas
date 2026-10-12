"""Smoke tests: every implementation and the benchmark run and print their key result."""
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMOS = {
    "implementations/01-bullwhip-simulator/simulate.py": "Supplier",
    "implementations/02-scope3-spend-vs-activity/compare.py": "tracks the invoice",
    "implementations/03-forecast-baselines/forecast.py": "Holt-Winters",
    "implementations/04-llm-solver-interface/whatif.py": "Baseline plan cost",
    "implementations/05-dock-scheduling/docks.py": "Stable re-plan",
    "implementations/06-agent-with-guardrails/agent.py": "BLOCKED",
    "implementations/07-federated-forecasting/federated.py": "Personal",
    "implementations/08-scope3-uncertainty/uncertainty.py": "Honest range",
    "implementations/09-safety-stock/safety_stock.py": "Combined SS",
    "implementations/10-dual-sourcing/dual_sourcing.py": "Dual 80/20",
    "implementations/11-changeover-scheduling/changeover.py": "CP-SAT on time",
    "implementations/12-eta-calibration/eta_conformal.py": "Conformal",
    "implementations/13-document-validation/bol_validation.py": "Straight-through rate",
    "implementations/14-returns-disposition/disposition.py": "EV at first touch",
    "benchmark/run.py": "Safe success",
}


def test_demos_run():
    for path, expected in DEMOS.items():
        out = subprocess.run([sys.executable, str(ROOT / path)], capture_output=True, text=True, timeout=120)
        assert out.returncode == 0, f"{path} failed:\n{out.stderr}"
        assert expected in out.stdout, f"{path} did not print '{expected}'"


def test_reference_agent_is_safe():
    bench = runpy.run_path(str(ROOT / "benchmark/run.py"))
    rows = bench["run_agent"](bench["careful"])
    assert all(r["success"] and r["violations"] == 0 for r in rows)
