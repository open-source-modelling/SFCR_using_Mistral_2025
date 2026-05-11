import os
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Callable
from functions import run_company_S_02_01_02, run_company_S_23_01_01, run_company_S_25_01_21

def _get_api_key() -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set. Please set it before running.")
    return api_key

def _run_table_for_companies(table: str, runner: Callable[[str, str, pd.DataFrame], pd.DataFrame], companies: np.ndarray, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for company in companies:
        company_frame = runner(company = company, 
                               api_key = api_key, 
                               master_list = master_list)
        if company_frame is not None and not company_frame.empty:
            frames.append(company_frame)    
            print(f"Finished table {table} for company: {company}")
        else:
            print(f"Table {table} for company: {company} was not processed.")
    if not frames:
        # If there are no correctly defined and processed tables then return None
        return None
    return pd.concat(frames, axis=1)


def main():
    code_dir = Path(__file__).resolve().parent
    project_dir = code_dir.parent
    output_dir = project_dir / "Output_aggregated"
    output_dir.mkdir(parents=True, exist_ok=True)
    

    print(f"✓ Project directory set to: {project_dir}")
    print(f"✓ Output directory set to: {output_dir}")

    api_key = _get_api_key()
    master_list = pd.read_csv(
        project_dir / "master_list_partial.csv",
        header=0,
        index_col=0
    )

    company_list = master_list.loc[:, "company"].unique().flatten()
    print("✓ Unique companies inside the list identified")
    table_list = master_list.loc[:, "table_category"].unique().flatten()
    print("✓ Unique tables inside the list identified")

    # Functions that run individual tables:
    table_runners = {
        "S_02_01_02": run_company_S_02_01_02,
        "S_23_01_01": run_company_S_23_01_01,
        "S_25_01_21": run_company_S_25_01_21,
    }
    # Name of csv file that contains aggregated table values for all companies
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
        combined = _run_table_for_companies(table = table,
                                             runner = runner, 
                                             companies = company_list, 
                                             api_key = api_key, 
                                             master_list = master_list)
                
        
        if combined is not None:
            combined.to_csv(output_dir / output_names[table])
        else:
            raise ValueError("The run did not produce a single value.")   

if __name__ == "__main__":
    main()