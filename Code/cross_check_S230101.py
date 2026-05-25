"""
Cross-validation for Italian S.23.01.01 Own Funds table (Phase 4).

Port of Cross_check_SII_Italy_2025.ipynb: runs 17 internal consistency checks per
company column and prints an overview plus diagnostics for failed checks.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

import pandas as pd

DEFAULT_EPS_SUM = 1.5
DEFAULT_EPS_DIV = 0.5
DEFAULT_INPUT = "Output_final/S230101_final.csv"

CHECK_DESCRIPTIONS = {
    "TEST_1": "R0290 = R0010 + R0030 + R0130 + R0140 + R0160",
    "TEST_2": "R0620 = R0540 / R0580",
    "TEST_3": "R0640 = R0550 / R0600",
    "TEST_4": "R0290 = R0500"
}


def _compare(
    data: pd.DataFrame,
    eps: float,
    col: str,
    lhs_row: str,
    rhs_rows: list[str],
    rhs_signs: list[int] | None,
    test_name: str,
    diag_index: list[str] | None = None,
) -> tuple[bool, pd.DataFrame | None, float]:
    """Compare one row to a signed sum of other rows for a single company column."""
    lhs = data.loc[lhs_row, col]
    signs = rhs_signs if rhs_signs is not None else [1] * len(rhs_rows)
    rhs = sum(sign * data.loc[row, col] for row, sign in zip(rhs_rows, signs))
    diff = abs(lhs - rhs)
    if diff < eps:
        return True, None, diff


    if diag_index is None:
        diag_index = rhs_rows + [lhs_row]
    diagnostics = [data.loc[row, col] for row in diag_index]
    return False, pd.DataFrame(diagnostics, index=diag_index, columns=[test_name]), diff


def _compare_division(
    data: pd.DataFrame,
    eps: float,
    col: str,
    lhs_row: str,
    divisor_row: str,
    dividend_row: str,
    test_name: str,
    diag_index: list[str] | None = None,
) -> tuple[bool, pd.DataFrame | None, float]:
    """Compare one row to ``100 * dividend / divisor`` for a single company column."""
    lhs = data.loc[lhs_row, col]
    divisor = data.loc[divisor_row, col]
    dividend = data.loc[dividend_row, col]
    if divisor == 0:
        raise ZeroDivisionError(
            f"Division by zero in test {test_name}: {divisor_row} is zero for company {col}"
        )
    rhs = 100*dividend / divisor
    diff = abs(lhs - rhs)
    if diff < eps:
        return True, None, diff

    if diag_index is None:
        diag_index = [divisor_row, dividend_row, lhs_row]
    diagnostics = [data.loc[row, col] for row in diag_index]
    return False, pd.DataFrame(diagnostics, index=diag_index, columns=[test_name]), diff


def check_23_01_01_1(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_1: R0290 = R0010 + R0030 + R0130 + R0140 + R0160."""
    return _compare(data, eps, col, "R0290", ["R0010", "R0030", "R0130", "R0140", "R0160"], None, "TEST_1")


def check_23_01_01_2(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_2: R0620 = R0540 / R0580."""
    return _compare_division(
        data, eps, col, "R0620", "R0580", "R0540", "TEST_2"
    )


def check_23_01_01_3(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_3: R0640 = R0550 / R0600."""
    return _compare_division(
        data,
        eps,
        col,
        "R0640",
        "R0600",
        "R0550",
        "TEST_3"
    )


def check_23_01_01_4(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_4: R0290 = R0500."""
    return _compare(data, eps, col, "R0500", ["R0290", "R0400"], None, "TEST_4")


CHECK_FUNCTIONS: list[tuple[str, Callable, bool]] = [
    ("TEST_1", check_23_01_01_1, False),
    ("TEST_2", check_23_01_01_2, True),
    ("TEST_3", check_23_01_01_3, True),
    ("TEST_4", check_23_01_01_4, False),
]


def run_check_diagnostics(
    table: pd.DataFrame,
    function: Callable,
    col_name: str,
    eps: float,
) -> pd.DataFrame:
    """Run one check function across all company columns and return pass/fail flags."""
    results = pd.DataFrame(data=[], columns=["COMPANY_NAME", col_name])
    for col in table.columns:
        res, _, _ = function(table, eps=eps, col=col)
        result_tmp = pd.DataFrame(data=[[col, res]], columns=["COMPANY_NAME", col_name])
        results = pd.concat([results, result_tmp])
        results[results == True] = ""
    return results


def build_overall_summary(
    table: pd.DataFrame,
    eps_sum: float,
    eps_div: float,
) -> pd.DataFrame:
    """Build a tests-by-companies matrix using summation or division tolerances."""
    data: dict[str, dict[str, str | bool]] = {}
    for test_name, check_fn, is_division in CHECK_FUNCTIONS:
        eps_to_use = eps_div if is_division else eps_sum
        results: dict[str, str | bool] = {}
        for company in table.columns:
            passed, _, _ = check_fn(table, eps=eps_to_use, col=company)
            results[company] = "" if passed else False
        data[test_name] = results

    summary = pd.DataFrame.from_dict(data, orient="index", columns=table.columns)
    summary.index.name = "TEST_NAME"
    summary.columns.name = "COMPANY_NAME"
    return summary


def ensure_validation_dir(project_dir: Path) -> Path:
    """Create and return the project ``Validation/`` directory."""
    validation_dir = project_dir / "Validation"
    validation_dir.mkdir(parents=True, exist_ok=True)
    return validation_dir


def save_validation_summary(summary: pd.DataFrame, project_dir: Path) -> Path:
    """Write the S.23.01.01 validation summary CSV and return its path."""
    validation_dir = ensure_validation_dir(project_dir)
    out_path = validation_dir / "validation_summary_S230101.csv"
    summary.to_csv(out_path)
    return out_path


def sanitize_filename(value: str) -> str:
    """Replace unsafe filename characters with underscores."""
    return "".join(
        ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in str(value)
    ).strip("_")


def save_failure_diagnostics(failures: list[dict], project_dir: Path) -> list[Path]:
    """Persist per-company diagnostic CSV files for failed checks."""
    validation_dir = ensure_validation_dir(project_dir)
    output_paths: list[Path] = []
    for failure in failures:
        company = sanitize_filename(failure["company"])
        test = sanitize_filename(failure["test"])
        diagnostics = failure["diagnostics"]
        out_path = validation_dir / f"diagnostics_{company}_{test}.csv"
        diagnostics.to_csv(out_path)
        output_paths.append(out_path)
    return output_paths


def collect_failure_details(
    table: pd.DataFrame,
    eps_sum: float,
    eps_div: float,
) -> list[dict]:
    """Collect structured failure records for every company and failed test."""
    failures: list[dict] = []
    for company in table.columns:
        for test_name, check_fn, is_division in CHECK_FUNCTIONS:
            eps_to_use = eps_div if is_division else eps_sum
            passed, diagnostics, diff = check_fn(table, eps=eps_to_use, col=company)
            if not passed:
                failures.append(
                    {
                        "company": company,
                        "test": test_name,
                        "rule": CHECK_DESCRIPTIONS[test_name],
                        "diff": diff,
                        "diagnostics": diagnostics,
                    }
                )
    return failures


def load_table(path: Path) -> pd.DataFrame:
    """Load an aggregated SFCR table CSV with row codes as the index."""
    return pd.read_csv(path, header=0, index_col=0, decimal=".", thousands=",")


def resolve_input_path(project_dir: Path, input_arg: str | None) -> Path:
    """Resolve the input CSV from ``--input`` or the default ``Output_final`` path."""
    if input_arg:
        candidate = Path(input_arg)
        if not candidate.is_absolute():
            candidate = project_dir / candidate
        if not candidate.exists():
            raise FileNotFoundError(f"Input file not found: {candidate}")
        return candidate

    candidate = project_dir / DEFAULT_INPUT
    if candidate.exists():
        return candidate
    raise FileNotFoundError(
        "No input table found. Pass --input or place data at "
        f"{candidate}"
    )


def print_failure_report(failures: list[dict]) -> None:
    """Print a human-readable report for all failed checks."""
    if not failures:
        print("\nAll checks passed for every company.")
        return

    print(f"\n{len(failures)} failed check(s):\n")
    current_company = None
    for item in failures:
        if item["company"] != current_company:
            current_company = item["company"]
            print(f"--- {current_company} ---")
        print(f"  {item['test']}: {item['rule']} (diff={item['diff']:.4f})")
        print(item["diagnostics"].to_string(header=True))
        print()


def main() -> int:
    """CLI entry point for S.23.01.01 cross-validation."""
    parser = argparse.ArgumentParser(
        description="Cross-validate S.23.01.01 Italian SFCR table consistency."
    )
    parser.add_argument(
        "--input",
        help="Path to aggregated S.23.01.01 CSV (default: Output_final/S230101_final.csv)",
    )
    parser.add_argument(
        "--eps-sum",
        type=float,
        default=DEFAULT_EPS_SUM,
        help="Numerical tolerance for summation checks only",
    )
    parser.add_argument(
        "--eps-div",
        type=float,
        default=DEFAULT_EPS_DIV,
        help="Numerical tolerance for division checks only",
    )
    parser.add_argument(
        "--company",
        help="Run detailed diagnostics for a single company column name only",
    )
    parser.add_argument(
        "--output-summary",
        help="Optional path to save the overall summary CSV",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print failures and exit status",
    )
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent.parent
    input_path = resolve_input_path(project_dir, args.input)
    table = load_table(input_path)

    if args.company:
        if args.company not in table.columns:
            available = ", ".join(map(str, table.columns))
            raise ValueError(
                f"Company '{args.company}' not in table columns. Available: {available}"
            )
        companies = [args.company]
    else:
        companies = list(table.columns)

    eps_sum = args.eps_sum if args.eps_sum is not None else DEFAULT_EPS_SUM
    eps_div = args.eps_div if args.eps_div is not None else DEFAULT_EPS_DIV

    if not args.quiet:
        print(f"Input: {input_path}")
        print(
            f"Companies: {len(table.columns)}, rows: {len(table)}, eps_sum: {eps_sum}, eps_div: {eps_div}"
        )

    overall_summary = build_overall_summary(table, eps_sum=eps_sum, eps_div=eps_div)
    validation_summary_path = save_validation_summary(overall_summary, project_dir)

    if args.company:
        overall_summary = overall_summary[[args.company]]

    if not args.quiet:
        print("\nOverall summary (tests in rows, companies in columns; empty cell = pass, False = fail):")
        print(overall_summary.to_string())
        print(f"\nValidation summary written to: {validation_summary_path}")

    if args.output_summary:
        out_path = Path(args.output_summary)
        if not out_path.is_absolute():
            out_path = project_dir / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        overall_summary.to_csv(out_path)
        print(f"Summary written to: {out_path}")

    failures = [
        f
        for f in collect_failure_details(table, eps_sum=eps_sum, eps_div=eps_div)
        if f["company"] in companies
    ]
    diagnostics_paths = save_failure_diagnostics(failures, project_dir) if failures else []
    if not args.quiet and diagnostics_paths:
        print(f"Saved {len(diagnostics_paths)} diagnostics file(s) to: {project_dir / 'Validation'}")
    print_failure_report(failures)
    return 1 if failures else 0


if __name__ == "__main__":
    main()
