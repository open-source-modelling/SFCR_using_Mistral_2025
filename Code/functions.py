import base64
import json
from pathlib import Path
from typing import Sequence, Type

import pandas as pd
from mistralai import Mistral
from mistralai.extra import response_format_from_pydantic_model
from PyPDF2 import PdfReader, PdfWriter
from pydantic import BaseModel

from S020102_classes import (
    AssetBalanceSheetAssets,
    AssetBalanceSheetAssetsIta,
    AssetBalanceSheetBondInvestments,
    AssetBalanceSheetBondInvestmentsIta,
    AssetBalanceSheetEquityInvestments,
    AssetBalanceSheetEquityInvestmentsIta,
    AssetBalanceSheetLoanInvestments,
    AssetBalanceSheetLoanInvestmentsIta,
    AssetBalanceSheetLoansAndRecoverables,
    AssetBalanceSheetLoansAndRecoverablesIta,
    AssetBalanceSheetRest,
    AssetBalanceSheetRestIta,
    LiabilityBalanceSheetDebt,
    LiabilityBalanceSheetDebtIta,
    LiabilityBalanceSheetHealth,
    LiabilityBalanceSheetHealthIta,
    LiabilityBalanceSheetLife,
    LiabilityBalanceSheetLifeIta,
    LiabilityBalanceSheetNonLife,
    LiabilityBalanceSheetNonLifeIta,
    LiabilityBalanceSheetPayables,
    LiabilityBalanceSheetPayablesIta,
)
from S230101_classes import (
    OwnFundsAuxiliaryOwnFunds,
    OwnFundsAuxiliaryOwnFundsIta,
    OwnFundsBasic,
    OwnFundsBasicIta,
    OwnFundsDeductions,
    OwnFundsDeductionsIta,
    OwnFundsRest,
    OwnFundsRestIta,
)
from S250121_classes import SCRRisk, SCRRiskIta


CODE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CODE_DIR.parent
INPUT_DIR = PROJECT_DIR / "Input"
SINGLE_PDF_DIR = PROJECT_DIR / "Single_pdf"
OUTPUT_DIR = PROJECT_DIR / "Output"


def extract_page(input_pdf_path, output_pdf_path, page_number, password: str = ""):
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()

    if pdf_reader.is_encrypted:
        if password:
            pdf_reader.decrypt(password)
        else:
            pdf_reader.decrypt("")

    pdf_writer.add_page(pdf_reader.pages[page_number - 1])

    with open(output_pdf_path, "wb") as output_pdf_file:
        pdf_writer.write(output_pdf_file)


def encode_pdf_str(pdf_path: str) -> str:
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode("utf-8")


def extract_paths(master_list: pd.DataFrame, unique_id: str):
    document_name, table_name, company, page_number, table_type = master_list.loc[
        unique_id, ["document_name", "table_name", "company", "page_number", "type"]
    ]

    page_number = int(page_number)
    pdf_path = INPUT_DIR / document_name
    output_pdf_path = SINGLE_PDF_DIR / f"{company}_{table_name}.pdf"
    output_final_path = OUTPUT_DIR / f"{company}_{table_name}.csv"
    return str(pdf_path), page_number, str(output_pdf_path), str(output_final_path), table_type


def call_mistral(client: Mistral, output_pdf_path: str, pydantic_model: Type[BaseModel]):
    base64_pdf = encode_pdf_str(output_pdf_path)
    annotations_response = client.ocr.process(
        model="mistral-ocr-latest",
        pages=list(range(3)),
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{base64_pdf}",
        },
        document_annotation_format=response_format_from_pydantic_model(pydantic_model),
        include_image_base64=True,
    )
    return annotations_response


def extracted_to_df(extracted_data: BaseModel, company: str) -> pd.DataFrame:
    data_tmp = pd.DataFrame(data=[], columns=[company])
    for attr, value in extracted_data:
        data_tmp.loc[attr, company] = value
    return data_tmp


def _ensure_output_dirs() -> None:
    SINGLE_PDF_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _run_single_model(client: Mistral, output_pdf_path: str, model_cls: Type[BaseModel], company: str) -> pd.DataFrame:
    annotations_response = call_mistral(
        client=client, output_pdf_path=output_pdf_path, pydantic_model=model_cls
    )
    extracted_data = model_cls(**json.loads(annotations_response.document_annotation))
    return extracted_to_df(extracted_data, company)


def _run_models_and_save(
    company: str,
    unique_id: str,
    api_key: str,
    master_list: pd.DataFrame,
    model_classes: Sequence[Type[BaseModel]],
) -> pd.DataFrame:
    _ensure_output_dirs()
    pdf_path, page_number, output_pdf_path, output_final_path, _ = extract_paths(master_list, unique_id)
    extract_page(pdf_path, output_pdf_path, page_number)

    client = Mistral(api_key=api_key)
    frames = [_run_single_model(client, output_pdf_path, model_cls, company) for model_cls in model_classes]
    output = pd.concat(frames, axis=0) if frames else pd.DataFrame()
    output.to_csv(output_final_path)
    return output


def run_assets_by_sections(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(
        company,
        unique_id,
        api_key,
        master_list,
        [
            AssetBalanceSheetAssets,
            AssetBalanceSheetEquityInvestments,
            AssetBalanceSheetBondInvestments,
            AssetBalanceSheetLoanInvestments,
            AssetBalanceSheetLoansAndRecoverables,
            AssetBalanceSheetRest,
        ],
    )


def run_assets_by_sections_ita(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(
        company,
        unique_id,
        api_key,
        master_list,
        [
            AssetBalanceSheetAssetsIta,
            AssetBalanceSheetEquityInvestmentsIta,
            AssetBalanceSheetBondInvestmentsIta,
            AssetBalanceSheetLoanInvestmentsIta,
            AssetBalanceSheetLoansAndRecoverablesIta,
            AssetBalanceSheetRestIta,
        ],
    )


def run_liability_by_sections(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(
        company,
        unique_id,
        api_key,
        master_list,
        [
            LiabilityBalanceSheetNonLife,
            LiabilityBalanceSheetHealth,
            LiabilityBalanceSheetLife,
            LiabilityBalanceSheetDebt,
            LiabilityBalanceSheetPayables,
        ],
    )


def run_liability_by_sections_ita(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(
        company,
        unique_id,
        api_key,
        master_list,
        [
            LiabilityBalanceSheetNonLifeIta,
            LiabilityBalanceSheetHealthIta,
            LiabilityBalanceSheetLifeIta,
            LiabilityBalanceSheetDebtIta,
            LiabilityBalanceSheetPayablesIta,
        ],
    )


def run_company_S_02_01_02(company: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    relevant_rows = master_list.loc[
        (master_list.loc[:, "company"] == company) & (master_list.loc[:, "table_category"] == "S_02_01_02"),
        :,
    ]
    if relevant_rows.empty:
        return pd.DataFrame()

    out_a = pd.DataFrame()
    out_l = pd.DataFrame()
    for row_id in relevant_rows.index:
        row_type = relevant_rows.loc[row_id, "type"]
        if row_type == "B":
            out_a = run_assets_by_sections(company, row_id, api_key, master_list)
            out_l = run_liability_by_sections(company, row_id, api_key, master_list)
        elif row_type == "B_ITA":
            out_a = run_assets_by_sections_ita(company, row_id, api_key, master_list)
            out_l = run_liability_by_sections_ita(company, row_id, api_key, master_list)
        elif row_type == "A":
            out_a = run_assets_by_sections(company, row_id, api_key, master_list)
        elif row_type == "L":
            out_l = run_liability_by_sections(company, row_id, api_key, master_list)
        elif row_type == "A_ITA":
            out_a = run_assets_by_sections_ita(company, row_id, api_key, master_list)
        elif row_type == "L_ITA":
            out_l = run_liability_by_sections_ita(company, row_id, api_key, master_list)

    return pd.concat([df for df in [out_a, out_l] if not df.empty], axis=0) if (not out_a.empty or not out_l.empty) else pd.DataFrame()


def run_S230101_first_half(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(
        company, unique_id, api_key, master_list, [OwnFundsBasic, OwnFundsDeductions, OwnFundsAuxiliaryOwnFunds]
    )


def run_S230101_first_half_ita(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(
        company,
        unique_id,
        api_key,
        master_list,
        [OwnFundsBasicIta, OwnFundsDeductionsIta, OwnFundsAuxiliaryOwnFundsIta],
    )


def run_S230101_second_half(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(company, unique_id, api_key, master_list, [OwnFundsRest])


def run_S230101_second_half_ita(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(company, unique_id, api_key, master_list, [OwnFundsRestIta])


def run_S250121(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(company, unique_id, api_key, master_list, [SCRRisk])


def run_S250121_ita(company: str, unique_id: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    return _run_models_and_save(company, unique_id, api_key, master_list, [SCRRiskIta])


def run_company_S_25_01_21(company: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    relevant_rows = master_list.loc[
        (master_list.loc[:, "company"] == company) & (master_list.loc[:, "table_category"] == "S_25_01_21"),
        :,
    ]
    if relevant_rows.empty:
        return pd.DataFrame()

    out = pd.DataFrame()
    for row_id in relevant_rows.index:
        row_type = relevant_rows.loc[row_id, "type"]
        if row_type == "B":
            out = run_S250121(company, row_id, api_key, master_list)
        elif row_type == "B_ITA":
            out = run_S250121_ita(company, row_id, api_key, master_list)
    return out


def run_company_S_23_01_01(company: str, api_key: str, master_list: pd.DataFrame) -> pd.DataFrame:
    relevant_rows = master_list.loc[
        (master_list.loc[:, "company"] == company) & (master_list.loc[:, "table_category"] == "S_23_01_01"),
        :,
    ]
    if relevant_rows.empty:
        return pd.DataFrame()

    out_1 = pd.DataFrame()
    out_2 = pd.DataFrame()
    for row_id in relevant_rows.index:
        row_type = relevant_rows.loc[row_id, "type"]
        if row_type == "B":
            out_1 = run_S230101_first_half(company, row_id, api_key, master_list)
            out_2 = run_S230101_second_half(company, row_id, api_key, master_list)
        elif row_type == "B_ITA":
            out_1 = run_S230101_first_half_ita(company, row_id, api_key, master_list)
            out_2 = run_S230101_second_half_ita(company, row_id, api_key, master_list)
        elif row_type == "A":
            out_1 = run_S230101_first_half(company, row_id, api_key, master_list)
        elif row_type == "L":
            out_2 = run_S230101_second_half(company, row_id, api_key, master_list)
        elif row_type == "A_ITA":
            out_1 = run_S230101_first_half_ita(company, row_id, api_key, master_list)
        elif row_type == "L_ITA":
            out_2 = run_S230101_second_half_ita(company, row_id, api_key, master_list)

    return pd.concat([df for df in [out_1, out_2] if not df.empty], axis=0) if (not out_1.empty or not out_2.empty) else pd.DataFrame()

