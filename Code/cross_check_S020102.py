"""
Cross-validation for Italian S.02.01.02 balance-sheet tables (Phase 4).

Port of Cross_check_SII_Italy_2025.ipynb: runs 17 internal consistency checks per
company column and prints an overview plus diagnostics for failed checks.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

import pandas as pd

DEFAULT_EPS = 1.5
DEFAULT_INPUT = "Final_output/S020102_final.csv"

CHECK_DESCRIPTIONS = {
    "TEST_1": "R0100 = R0110 + R0120",
    "TEST_2": "R0130 = R0140 + R0150 + R0160 + R0170",
    "TEST_3": "R0070 = R0080 + R0090 + R0100 + R0130 + R0180 + R0190 + R0200 + R0210",
    "TEST_4": "R0230 = R0240 + R0250 + R0260",
    "TEST_5": "R0270 = R0280 + R0310 + R0340",
    "TEST_6": "R0310 = R0320 + R0330",
    "TEST_7": "R0280 = R0290 + R0300",
    "TEST_8": "R0500 = R0030 + R0040 + R0050 + R0060 + R0070 + R0220 + R0230 + R0270 + R0350 + R0360 + R0370 + R0380 + R0390 + R0400 + R0410 + R0420",
    "TEST_9": "R0510 = R0520 + R0560",
    "TEST_10": "R0520 = R0530 + R0540 + R0550",
    "TEST_11": "R0560 = R0570 + R0580 + R0590",
    "TEST_12": "R0600 = R0610 + R0650",
    "TEST_13": "R0610 = R0620 + R0630 + R0640",
    "TEST_14": "R0650 = R0660 + R0670 + R0680",
    "TEST_15": "R0690 = R0700 + R0710 + R0720",
    "TEST_16": "R0850 = R0860 + R0870",
    "TEST_17": "R1000 = R0500 - R0900",
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


def check_02_01_02_1(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_1: R0100 = R0110 + R0120."""
    return _compare(data, eps, col, "R0100", ["R0110", "R0120"], None, "TEST_1")


def check_02_01_02_2(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_2: R0130 = R0140 + R0150 + R0160 + R0170."""
    return _compare(
        data, eps, col, "R0130", ["R0140", "R0150", "R0160", "R0170"], None, "TEST_2"
    )


def check_02_01_02_3(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_3: R0070 equals the sum of investment sub-rows R0080 through R0210."""
    return _compare(
        data,
        eps,
        col,
        "R0070",
        ["R0080", "R0090", "R0100", "R0130", "R0180", "R0190", "R0200", "R0210"],
        None,
        "TEST_3",
    )


def check_02_01_02_4(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_4: R0230 = R0240 + R0250 + R0260."""
    return _compare(data, eps, col, "R0230", ["R0240", "R0250", "R0260"], None, "TEST_4")


def check_02_01_02_5(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_5: R0270 = R0280 + R0310 + R0340."""
    return _compare(data, eps, col, "R0270", ["R0280", "R0310", "R0340"], None, "TEST_5")


def check_02_01_02_6(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_6: R0310 = R0320 + R0330."""
    return _compare(data, eps, col, "R0310", ["R0320", "R0330"], None, "TEST_6")


def check_02_01_02_7(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_7: R0280 = R0290 + R0300."""
    return _compare(data, eps, col, "R0280", ["R0290", "R0300"], None, "TEST_7")


def check_02_01_02_8(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_8: R0500 equals the sum of selected asset rows."""
    return _compare(
        data,
        eps,
        col,
        "R0500",
        [
            "R0030",
            "R0040",
            "R0050",
            "R0060",
            "R0070",
            "R0220",
            "R0230",
            "R0270",
            "R0350",
            "R0360",
            "R0370",
            "R0380",
            "R0390",
            "R0400",
            "R0410",
            "R0420",
        ],
        None,
        "TEST_8",
    )


def check_02_01_02_9(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_9: R0510 = R0520 + R0560."""
    return _compare(data, eps, col, "R0510", ["R0520", "R0560"], None, "TEST_9")


def check_02_01_02_10(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_10: R0520 = R0530 + R0540 + R0550."""
    return _compare(data, eps, col, "R0520", ["R0530", "R0540", "R0550"], None, "TEST_10")


def check_02_01_02_11(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_11: R0560 = R0570 + R0580 + R0590."""
    return _compare(data, eps, col, "R0560", ["R0570", "R0580", "R0590"], None, "TEST_11")


def check_02_01_02_12(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_12: R0600 = R0610 + R0650."""
    return _compare(data, eps, col, "R0600", ["R0610", "R0650"], None, "TEST_12")


def check_02_01_02_13(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_13: R0610 = R0620 + R0630 + R0640."""
    return _compare(data, eps, col, "R0610", ["R0620", "R0630", "R0640"], None, "TEST_13")


def check_02_01_02_14(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_14: R0650 = R0660 + R0670 + R0680."""
    return _compare(data, eps, col, "R0650", ["R0660", "R0670", "R0680"], None, "TEST_14")


def check_02_01_02_15(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_15: R0690 = R0700 + R0710 + R0720."""
    return _compare(data, eps, col, "R0690", ["R0700", "R0710", "R0720"], None, "TEST_15")


def check_02_01_02_16(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_16: R0850 = R0860 + R0870."""
    return _compare(data, eps, col, "R0850", ["R0860", "R0870"], None, "TEST_16")


def check_02_01_02_17(data: pd.DataFrame, eps: float, col: str):
    """Run TEST_17: R1000 = R0500 - R0900."""
    return _compare(
        data,
        eps,
        col,
        "R1000",
        ["R0500", "R0900"],
        [1, -1],
        "TEST_17",
        diag_index=["R0500", "R0900", "R1000"],
    )


CHECK_FUNCTIONS: list[tuple[str, Callable]] = [
    ("TEST_1", check_02_01_02_1),
    ("TEST_2", check_02_01_02_2),
    ("TEST_3", check_02_01_02_3),
    ("TEST_4", check_02_01_02_4),
    ("TEST_5", check_02_01_02_5),
    ("TEST_6", check_02_01_02_6),
    ("TEST_7", check_02_01_02_7),
    ("TEST_8", check_02_01_02_8),
    ("TEST_9", check_02_01_02_9),
    ("TEST_10", check_02_01_02_10),
    ("TEST_11", check_02_01_02_11),
    ("TEST_12", check_02_01_02_12),
    ("TEST_13", check_02_01_02_13),
    ("TEST_14", check_02_01_02_14),
    ("TEST_15", check_02_01_02_15),
    ("TEST_16", check_02_01_02_16),
    ("TEST_17", check_02_01_02_17),
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


def build_overall_summary(table: pd.DataFrame, eps: float) -> pd.DataFrame:
    """Build a tests-by-companies matrix with empty cells for passes and ``False`` for failures."""
    data: dict[str, dict[str, str | bool]] = {}
    for test_name, check_fn in CHECK_FUNCTIONS:
        results: dict[str, str | bool] = {}
        for company in table.columns:
            passed, _, _ = check_fn(table, eps=eps, col=company)
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
    """Write the S.02.01.02 validation summary CSV and return its path."""
    validation_dir = ensure_validation_dir(project_dir)
    out_path = validation_dir / "validation_summary_S020102.csv"
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
    eps: float,
) -> list[dict]:
    """Collect structured failure records for every company and failed test."""
    failures: list[dict] = []
    for company in table.columns:
        for test_name, check_fn in CHECK_FUNCTIONS:
            passed, diagnostics, diff = check_fn(table, eps=eps, col=company)
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
    """Resolve the input CSV from ``--input`` or known project fallback locations."""
    if input_arg:
        candidate = Path(input_arg)
        if not candidate.is_absolute():
            candidate = project_dir / candidate
        if not candidate.exists():
            raise FileNotFoundError(f"Input file not found: {candidate}")
        return candidate

    fallbacks = [
        project_dir / DEFAULT_INPUT,
        project_dir / "Final_output/S020102_final.csv",
        project_dir / "Output_aggregated/S020102.csv",
        project_dir / "Comparison/S020102_partial_2025.csv",
    ]
    for path in fallbacks:
        if path.exists():
            return path
    raise FileNotFoundError(
        "No input table found. Pass --input or place data at "
        f"{project_dir / DEFAULT_INPUT}"
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
    """CLI entry point for S.02.01.02 cross-validation."""
    parser = argparse.ArgumentParser(
        description="Cross-validate S.02.01.02 Italian SFCR table consistency."
    )
    parser.add_argument(
        "--input",
        help="Path to aggregated S.02.01.02 CSV (default: Final_output/S020102_partial_final.csv)",
    )
    parser.add_argument(
        "--eps",
        type=float,
        default=DEFAULT_EPS,
        help=f"Numerical tolerance (default: {DEFAULT_EPS})",
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

    if not args.quiet:
        print(f"Input: {input_path}")
        print(f"Companies: {len(table.columns)}, rows: {len(table)}, eps: {args.eps}")

    overall_summary = build_overall_summary(table, args.eps)
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
        for f in collect_failure_details(table, args.eps)
        if f["company"] in companies
    ]
    diagnostics_paths = save_failure_diagnostics(failures, project_dir) if failures else []
    if not args.quiet and diagnostics_paths:
        print(f"Saved {len(diagnostics_paths)} diagnostics file(s) to: {project_dir / 'Validation'}")
    print_failure_report(failures)
    return 1 if failures else 0


if __name__ == "__main__":
    main()
