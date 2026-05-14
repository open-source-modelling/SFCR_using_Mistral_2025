"""
Run all SFCR table cross-validation scripts in one pass.

Usage:
    python Code/run_cross_checks.py
    python Code/run_cross_checks.py --quiet
    python Code/run_cross_checks.py --company AXA
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from cross_check_S020102 import DEFAULT_EPS as DEFAULT_EPS_S020102
from cross_check_S020102 import main as main_s020102
from cross_check_S230101 import DEFAULT_EPS_DIV
from cross_check_S230101 import DEFAULT_EPS_SUM
from cross_check_S230101 import main as main_s230101
from cross_check_S250121 import main as main_s250121


@dataclass(frozen=True)
class CrossCheckJob:
    table_id: str
    label: str
    main_fn: Callable[[], int]
    input_flag: str


JOBS: tuple[CrossCheckJob, ...] = (
    CrossCheckJob("S_02_01_02", "S.02.01.02 balance sheet", main_s020102, "--input-s020102"),
    CrossCheckJob("S_23_01_01", "S.23.01.01 own funds", main_s230101, "--input-s230101"),
    CrossCheckJob("S_25_01_21", "S.25.01.21 SCR standard formula", main_s250121, "--input-s250121"),
)


def _run_with_argv(argv: Sequence[str], main_fn: Callable[[], int]) -> int:
    """Call ``main_fn`` as if it were invoked with ``argv`` and restore ``sys.argv`` afterward."""
    previous_argv = sys.argv
    sys.argv = list(argv)
    try:
        return main_fn()
    finally:
        sys.argv = previous_argv


def _build_argv(
    script_name: str,
    *,
    input_path: str | None,
    quiet: bool,
    company: str | None,
    eps: float,
    eps_sum: float,
    eps_div: float,
    is_balance_sheet: bool,
) -> list[str]:
    """Build a synthetic ``sys.argv`` for one table-specific cross-check script."""
    argv = [script_name]
    if input_path:
        argv.extend(["--input", input_path])
    if quiet:
        argv.append("--quiet")
    if company:
        argv.extend(["--company", company])
    if is_balance_sheet:
        argv.extend(["--eps", str(eps)])
    else:
        argv.extend(["--eps-sum", str(eps_sum), "--eps-div", str(eps_div)])
    return argv


def main() -> int:
    """Run all configured cross-check suites and return a combined process exit code."""
    parser = argparse.ArgumentParser(
        description="Run cross-validation for all supported SFCR tables."
    )
    parser.add_argument(
        "--input-s020102",
        help="CSV for S.02.01.02 (default: resolved by cross_check_S020102.py)",
    )
    parser.add_argument(
        "--input-s230101",
        help="CSV for S.23.01.01 (default: resolved by cross_check_S230101.py)",
    )
    parser.add_argument(
        "--input-s250121",
        help="CSV for S.25.01.21 (default: resolved by cross_check_S250121.py)",
    )
    parser.add_argument(
        "--eps",
        type=float,
        default=DEFAULT_EPS_S020102,
        help=f"Tolerance for S.02.01.02 checks (default: {DEFAULT_EPS_S020102})",
    )
    parser.add_argument(
        "--eps-sum",
        type=float,
        default=DEFAULT_EPS_SUM,
        help=f"Summation tolerance for S.23.01.01 and S.25.01.21 (default: {DEFAULT_EPS_SUM})",
    )
    parser.add_argument(
        "--eps-div",
        type=float,
        default=DEFAULT_EPS_DIV,
        help=f"Division tolerance for S.23.01.01 and S.25.01.21 (default: {DEFAULT_EPS_DIV})",
    )
    parser.add_argument("--company", help="Validate a single company column only")
    parser.add_argument(
        "--tables",
        nargs="+",
        choices=[job.table_id for job in JOBS],
        help="Run only selected tables (default: all)",
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop after the first table that fails checks or raises an error",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce per-table output (forwarded to each cross-check script)",
    )
    args = parser.parse_args()

    code_dir = Path(__file__).resolve().parent
    inputs = {
        "--input-s020102": args.input_s020102,
        "--input-s230101": args.input_s230101,
        "--input-s250121": args.input_s250121,
    }
    selected = set(args.tables) if args.tables else {job.table_id for job in JOBS}
    jobs = [job for job in JOBS if job.table_id in selected]

    if not args.quiet:
        print(f"Running {len(jobs)} cross-check suite(s) from {code_dir.parent}\n")

    results: list[tuple[str, str, int | str]] = []
    exit_code = 0

    for index, job in enumerate(jobs, start=1):
        if not args.quiet:
            separator = "=" * 72
            print(f"{separator}\n[{index}/{len(jobs)}] {job.label} ({job.table_id})\n{separator}")

        argv = _build_argv(
            f"cross_check_{job.table_id.replace('_', '')}.py",
            input_path=inputs[job.input_flag],
            quiet=args.quiet,
            company=args.company,
            eps=args.eps,
            eps_sum=args.eps_sum,
            eps_div=args.eps_div,
            is_balance_sheet=job.table_id == "S_02_01_02",
        )

        try:
            status = _run_with_argv(argv, job.main_fn)
        except Exception as exc:
            status = f"error: {exc}"
            exit_code = 1
            print(f"ERROR running {job.table_id}: {exc}")
            if args.stop_on_error:
                break
            results.append((job.table_id, job.label, status))
            continue

        results.append((job.table_id, job.label, status))
        if status != 0:
            exit_code = 1
            if args.stop_on_error:
                break

    print("\n" + "=" * 72)
    print("Cross-check summary")
    print("=" * 72)
    for table_id, label, status in results:
        if status == 0:
            outcome = "PASS"
        elif status == 1:
            outcome = "FAIL (checks did not pass)"
        else:
            outcome = str(status).upper()
        print(f"  {table_id} ({label}): {outcome}")

    if exit_code == 0:
        print("\nAll selected cross-check suites passed.")
    else:
        print("\nOne or more cross-check suites failed or errored.")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
