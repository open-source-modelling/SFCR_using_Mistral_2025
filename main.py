import pandas as pd

from functions import run_company_S_02_01_02, run_company_S_23_01_01

api_key = "MarK4Hz2nWqZKNCItzeJtpSR6e6LBpwH"

master_list_ita = pd.read_excel("master_list_only_23.xlsx", sheet_name = "ITALY_2025", header=0, index_col=0)

S020102 = None
S230101 = None

company_list = master_list_ita.loc[:,"company"].unique().flatten()
table_list = master_list_ita.loc[:,"table_category"].unique().flatten()

for table in table_list:

    if table == "S_02_01_02":
        for company in company_list:
            if S020102 is None:
                S020102 =  run_company_S_02_01_02(company, api_key, master_list_ita)
            else:
                S020102_single =  run_company_S_02_01_02(company, api_key, master_list_ita)
                S020102 = pd.concat([S020102,S020102_single], axis = 1)
            print("Table S.02.01.02 finished for company: "+company+" and table: "+table)
    elif table == "S_23_01_01":
        for company in company_list:
            if S230101 is None:
                S230101 =  run_company_S_23_01_01(company, api_key, master_list_ita)
            else:
                S230101_single =  run_company_S_23_01_01(company, api_key, master_list_ita)
                S230101 = pd.concat([S230101,S230101_single], axis = 1)
            print("Table S.23.01.01 finished for company: "+company+" and table: "+table)


if S020102 is not None:
    S020102.to_csv("Output/S020102.csv")
if S230101 is not None:
        S230101.to_csv("Output/S230101.csv")