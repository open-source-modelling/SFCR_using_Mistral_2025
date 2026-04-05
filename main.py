import pandas as pd

from functions import run_company_S_02_01_02

api_key = "upP6NWLMzeR4oRGPHkRUt00sCxffXmS5"

master_list_ita = pd.read_excel("master_list.xlsx", sheet_name = "ITALY_2024", header=0, index_col=0)

S020102 = None
for company in master_list_ita.loc[:,"company"].unique().flatten():
    if S020102 is None:
        S020102 =  run_company_S_02_01_02(company, api_key, master_list_ita)
    else:
        S020102_single =  run_company_S_02_01_02(company, api_key, master_list_ita)
        S020102 = pd.concat([S020102,S020102_single], axis = 1)
    print("Table S.02.01.02 finished for company: "+company)

S020102.to_csv("Output/S020102.csv")
