import os
from pathlib import Path

import pandas as pd

from functions import run_company_S_02_01_02, run_company_S_23_01_01, run_company_S_25_01_21


def _get_api_key() -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("Missing MISTRAL_API_KEY environment variable.")
    return api_key


def _run_table_for_companies(table: str, runner, companies, api_key: str, master_list: pd.DataFrame):
    frames = []
    for company in companies:
        company_frame = runner(company, api_key, master_list)
        if company_frame is not None and not company_frame.empty:
            frames.append(company_frame)
        print(f"Finished table {table} for company: {company}")
    if not frames:
        return None
    return pd.concat(frames, axis=1)


def main():
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "Output"
    output_dir.mkdir(parents=True, exist_ok=True)

    api_key = _get_api_key()
    master_list = pd.read_excel(
        base_dir / "master_list_partial.xlsx",
        sheet_name="ITALY_2025",
        header=0,
        index_col=0,
    )

    company_list = master_list.loc[:, "company"].unique().flatten()
    table_list = master_list.loc[:, "table_category"].unique().flatten()

    table_runners = {
        "S_02_01_02": run_company_S_02_01_02,
        "S_23_01_01": run_company_S_23_01_01,
        "S_25_01_21": run_company_S_25_01_21,
    }
    output_names = {
        "S_02_01_02": "S020102.csv",
        "S_23_01_01": "S230101.csv",
        "S_25_01_21": "S250121.csv",
    }

    for table in table_list:
        runner = table_runners.get(table)
        if runner is None:
            print(f"Skipping unsupported table category: {table}")
            continue
        combined = _run_table_for_companies(table, runner, company_list, api_key, master_list)
        if combined is not None:
            combined.to_csv(output_dir / output_names[table])


if __name__ == "__main__":
    main()