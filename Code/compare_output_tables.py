"""
Compare extracted tables in ``Output/`` with manually corrected tables in ``Output_final/``.

Reports the percentage of aligned cell values that are equal after numeric parsing.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_TABLE_PAIRS: tuple[tuple[str, str], ...] = (
    ("S020102.csv", "S020102_final.csv"),
    ("S230101.csv", "S230101_final.csv"),
    ("S250121.csv", "S250121_final.csv"),
)


@dataclass(frozen=True)
class TableComparisonResult:
    """Summary of one Output vs Output_final table pair."""

    output_file: str
    final_file: str
    compared_cells: int
    equal_cells: int
    equal_percentage: float
    missing_in_output_rows: int
    missing_in_output_cols: int
    missing_in_final_rows: int
    missing_in_final_cols: int

    @property
    def unequal_cells(self) -> int:
        return self.compared_cells - self.equal_cells


def load_output_table(path: Path) -> pd.DataFrame:
    """Load a raw extraction CSV from ``Output/``."""
    return pd.read_csv(path, header=0, index_col=0)


def load_final_table(path: Path) -> pd.DataFrame:
    """Load a corrected CSV from ``Output_final/`` with thousands separators."""
    return pd.read_csv(path, header=0, index_col=0, thousands=",")


def _to_numeric_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert every cell to float, coercing unparseable values to NaN."""
    numeric = frame.apply(pd.to_numeric, errors="coerce")
    return numeric.astype(float)


def values_equal(left: float, right: float, atol: float) -> bool:
    """Return whether two numeric cells should be treated as equal."""
    if np.isnan(left) and np.isnan(right):
        return True
    if np.isnan(left) or np.isnan(right):
        return False
    if atol == 0:
        return left == right
    return bool(np.isclose(left, right, atol=atol, rtol=0))


def compare_tables(
    output_df: pd.DataFrame,
    final_df: pd.DataFrame,
    atol: float,
) -> tuple[int, int]:
    """
    Compare aligned rows and columns between two tables.

    Returns ``(equal_cells, compared_cells)``.
    """
    common_rows = output_df.index.intersection(final_df.index)
    common_cols = output_df.columns.intersection(final_df.columns)

    if common_rows.empty or common_cols.empty:
        return 0, 0

    output_numeric = _to_numeric_frame(output_df.loc[common_rows, common_cols])
    final_numeric = _to_numeric_frame(final_df.loc[common_rows, common_cols])

    compared_cells = int(output_numeric.size)
    equal_cells = 0

    for row in common_rows:
        for col in common_cols:
            if values_equal(output_numeric.at[row, col], final_numeric.at[row, col], atol):
                equal_cells += 1

    return equal_cells, compared_cells


def compare_table_pair(
    output_path: Path,
    final_path: Path,
    atol: float,
) -> TableComparisonResult:
    """Compare one Output / Output_final file pair and return summary statistics."""
    output_df = load_output_table(output_path)
    final_df = load_final_table(final_path)

    equal_cells, compared_cells = compare_tables(output_df, final_df, atol)
    equal_percentage = (100.0 * equal_cells / compared_cells) if compared_cells else 0.0

    common_rows = output_df.index.intersection(final_df.index)
    common_cols = output_df.columns.intersection(final_df.columns)

    return TableComparisonResult(
        output_file=output_path.name,
        final_file=final_path.name,
        compared_cells=compared_cells,
        equal_cells=equal_cells,
        equal_percentage=equal_percentage,
        missing_in_output_rows=len(final_df.index.difference(output_df.index)),
        missing_in_output_cols=len(final_df.columns.difference(output_df.columns)),
        missing_in_final_rows=len(output_df.index.difference(final_df.index)),
        missing_in_final_cols=len(output_df.columns.difference(final_df.columns)),
    )


def discover_table_pairs(output_dir: Path, final_dir: Path) -> list[tuple[Path, Path]]:
    """Match ``Output/*.csv`` files to ``Output_final/*_final.csv`` counterparts."""
    pairs: list[tuple[Path, Path]] = []

    for output_name, final_name in DEFAULT_TABLE_PAIRS:
        output_path = output_dir / output_name
        final_path = final_dir / final_name
        if output_path.exists() and final_path.exists():
            pairs.append((output_path, final_path))

    return pairs


def print_report(results: list[TableComparisonResult], atol: float) -> None:
    """Print a human-readable comparison report."""
    print(f"Numeric tolerance (atol): {atol}")
    print()

    total_compared = 0
    total_equal = 0

    for result in results:
        print(f"{result.output_file} vs {result.final_file}")
        print(f"  Compared cells: {result.compared_cells}")
        print(f"  Equal cells:    {result.equal_cells}")
        print(f"  Unequal cells:  {result.unequal_cells}")
        print(f"  Equal values:   {result.equal_percentage:.2f}%")

        if (
            result.missing_in_final_rows
            or result.missing_in_final_cols
            or result.missing_in_output_rows
            or result.missing_in_output_cols
        ):
            print(
                "  Alignment note: "
                f"{result.missing_in_final_rows} row(s) only in Output, "
                f"{result.missing_in_output_rows} row(s) only in Output_final, "
                f"{result.missing_in_final_cols} column(s) only in Output, "
                f"{result.missing_in_output_cols} column(s) only in Output_final"
            )
        print()

        total_compared += result.compared_cells
        total_equal += result.equal_cells

    if len(results) > 1:
        overall = (100.0 * total_equal / total_compared) if total_compared else 0.0
        print("Overall")
        print(f"  Compared cells: {total_compared}")
        print(f"  Equal cells:    {total_equal}")
        print(f"  Equal values:   {overall:.2f}%")


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Compare Output/ tables with Output_final/ tables and report match rate."
    )
    parser.add_argument(
        "--output-dir",
        default="Output",
        help="Folder with raw extracted CSV files (default: Output)",
    )
    parser.add_argument(
        "--final-dir",
        default="Output_final",
        help="Folder with corrected CSV files (default: Output_final)",
    )
    parser.add_argument(
        "--atol",
        type=float,
        default=0.0,
        help="Absolute tolerance for numeric equality (default: 0 for exact match)",
    )
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent.parent
    output_dir = Path(args.output_dir)
    final_dir = Path(args.final_dir)
    if not output_dir.is_absolute():
        output_dir = project_dir / output_dir
    if not final_dir.is_absolute():
        final_dir = project_dir / final_dir

    if not output_dir.is_dir():
        raise FileNotFoundError(f"Output directory not found: {output_dir}")
    if not final_dir.is_dir():
        raise FileNotFoundError(f"Output_final directory not found: {final_dir}")

    pairs = discover_table_pairs(output_dir, final_dir)
    if not pairs:
        raise FileNotFoundError(
            f"No matching table pairs found in {output_dir} and {final_dir}"
        )

    results = [compare_table_pair(output_path, final_path, args.atol) for output_path, final_path in pairs]
    print_report(results, args.atol)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
