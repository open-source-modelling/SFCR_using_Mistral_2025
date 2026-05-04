import pandas as pd

from functions import run_company_S_02_01_02, run_company_S_23_01_01, run_company_S_25_01_21

api_key = "[YOUR API KEY HERE]"

# MASTER LIST OF COMPANIES, TABLES AND PAGES TO BE SCRAPED
master_list = pd.read_excel("master_list_partial.xlsx", sheet_name = "ITALY_2025", header=0, index_col=0)

# INITIALIZE THE DATAFRAMES TO STORE THE RESULTS
S020102 = None
S230101 = None
S250121 = None

# GET THE UNIQUE COMPANIES AND TABLES TO BE SCRAPED
company_list = master_list.loc[:,"company"].unique().flatten()
table_list = master_list.loc[:,"table_category"].unique().flatten()

# LOOP THROUGH THE TABLES AND COMPANIES TO SCRAPE THE DATA AND STORE IT IN THE DATAFRAMES
for table in table_list:
    if table == "S_02_01_02": # TABLE S.02.01.02
        for company in company_list:
            if S020102 is None:
                S020102 =  run_company_S_02_01_02(company, api_key, master_list)
            else:
                S020102_single =  run_company_S_02_01_02(company, api_key, master_list)
                S020102 = pd.concat([S020102,S020102_single], axis = 1)
            print("Table S.02.01.02 finished for company: "+company+" and table: "+table)
    elif table == "S_23_01_01": # TABLE S.23.01.01
        for company in company_list:
            if S230101 is None:
                S230101 =  run_company_S_23_01_01(company, api_key, master_list)
            else:
                S230101_single =  run_company_S_23_01_01(company, api_key, master_list)
                S230101 = pd.concat([S230101,S230101_single], axis = 1)
            print("Table S.23.01.01 finished for company: "+company+" and table: "+table)
    elif table == "S_25_01_21": # TABLE S.25.01.21
        for company in company_list:
            if S250121 is None:
                S250121 =  run_company_S_25_01_21(company, api_key, master_list)
            else:
                S250121_single =  run_company_S_25_01_21(company, api_key, master_list)
                S250121 = pd.concat([S250121,S250121_single], axis = 1)
            print("Table S.25.01.21 finished for company: "+company+" and table: "+table)

# SAVE THE DATAFRAMES AS CSV FILES IN THE OUTPUT FOLDER
if S020102 is not None:
    S020102.to_csv("Output/S020102.csv")
if S230101 is not None:
        S230101.to_csv("Output/S230101.csv")
if S250121 is not None:
        S250121.to_csv("Output/S250121.csv")