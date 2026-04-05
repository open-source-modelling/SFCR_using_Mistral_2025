import os
import json
import base64
from anthropic import BaseModel
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from mistralai import Mistral
from mistralai.extra import response_format_from_pydantic_model
from pydantic import BaseModel
from S020102_classes import AssetBalanceSheetAssets, AssetBalanceSheetEquityInvestments, AssetBalanceSheetBondInvestments, AssetBalanceSheetLoanInvestments, AssetBalanceSheetLoansAndRecoverables, AssetBalanceSheetRest, AssetBalanceSheetAssetsIta, AssetBalanceSheetEquityInvestmentsIta, AssetBalanceSheetBondInvestmentsIta, AssetBalanceSheetLoanInvestmentsIta, AssetBalanceSheetLoansAndRecoverablesIta, AssetBalanceSheetRestIta, LiabilityBalanceSheetNonLife, LiabilityBalanceSheetHealth, LiabilityBalanceSheetLife, LiabilityBalanceSheetDebt, LiabilityBalanceSheetPayables, LiabilityBalanceSheetNonLifeIta, LiabilityBalanceSheetHealthIta, LiabilityBalanceSheetLifeIta, LiabilityBalanceSheetDebtIta, LiabilityBalanceSheetPayablesIta

def extract_page(input_pdf_path, output_pdf_path, page_number, password: str = ""):
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()

    # Decrypt if necessary
    if pdf_reader.is_encrypted:
        if password:
            pdf_reader.decrypt(password)
        else:
            pdf_reader.decrypt("")  # try empty password
    
    # Add the specified page to the PdfWriter object
    pdf_writer.add_page(pdf_reader.pages[page_number - 1])

    # Write the selected page to a new PDF file
    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

def encode_pdf_str(pdf_path: str) -> str:
    """Encode PDF file to base64 string.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Base64 encoded string of the PDF
    """
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    except Exception as e:
        raise Exception(f"Error encoding PDF: {str(e)}")


def extract_paths(master_list:pd.DataFrame, unique_id:str) -> dict:
    """
    Extract file paths and page number from master_list for a given unique_id.
    
    Parameters:
        master_list (pd.DataFrame): DataFrame containing metadata.
        unique_id: Index or identifier in the DataFrame.
    
    Returns:
        dict: Dictionary with keys 'pdf_path', 'page_number', 
              'output_pdf_path', 'output_final_path', 'codes_path'.
    """
    document_name, table_name, company, page_number, table_type = master_list.loc[unique_id, ["document_name", "table_name", "company", "page_number", "type"]]

    page_number = int(page_number)
    
    path_to_main = os.getcwd()
    path_to_Input = os.path.join(path_to_main, "Input")
    path_to_Single_pdf = os.path.join(path_to_main, "Single_pdf")
    path_to_output = os.path.join(path_to_main,"Output") 

    pdf_path = os.path.join(path_to_Input, document_name)
    output_pdf_path	= os.path.join(path_to_Single_pdf, company+"_"+table_name+".pdf")
    output_final_path = os.path.join(path_to_output, company+"_"+table_name+".csv")
    
    return pdf_path, page_number, output_pdf_path, output_final_path, table_type

def call_mistral(client:Mistral, output_pdf_path:str, pydantic_model:BaseModel):
    base64_pdf = encode_pdf_str(output_pdf_path)
    annotations_response = client.ocr.process(
        model="mistral-ocr-latest",
        pages=list(range(3)),  # Document Annotations limited to 8 pages
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{base64_pdf}"
        },
        document_annotation_format=response_format_from_pydantic_model(pydantic_model),
        include_image_base64=True
    )
    return annotations_response
#print(f"   ✓ OCR completed - {len(annotations_response.pages)} pages processed")
#print("   ✓ Structured data extracted successfully")

def extracted_to_df(extracted_data:pd.DataFrame, company:str)->pd.DataFrame:
    data_tmp = pd.DataFrame(data = [], columns = [company])
    for attr, value in extracted_data:
        data_tmp.loc[attr,company] = value 
    return data_tmp


def run_assets_by_sections(company:str, unique_id:str, api_key:str, master_list:pd.DataFrame)->pd.DataFrame:
    ### V funkcijo za bolj granularno

    pdf_path, page_number, output_pdf_path, output_final_path, table_type =  extract_paths(master_list, unique_id)
    extract_page(pdf_path, output_pdf_path, page_number)
    
    client = Mistral(api_key=api_key)
    class_output = AssetBalanceSheetAssets    
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    
    output_02_A_1 = extracted_to_df(extracted_data, company)
    
    class_output = AssetBalanceSheetEquityInvestments
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_2 = extracted_to_df(extracted_data, company)

    class_output = AssetBalanceSheetBondInvestments
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_3 = extracted_to_df(extracted_data, company)
    
    class_output = AssetBalanceSheetLoanInvestments
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_4 = extracted_to_df(extracted_data, company)
    
    class_output = AssetBalanceSheetLoansAndRecoverables
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_5 = extracted_to_df(extracted_data, company)
        
    class_output = AssetBalanceSheetLoansAndRecoverables
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_6 = extracted_to_df(extracted_data, company)
      
    class_output = AssetBalanceSheetRest
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_7 = extracted_to_df(extracted_data, company)
    
    output = pd.concat([output_02_A_1, output_02_A_2, output_02_A_3, output_02_A_4, output_02_A_5, output_02_A_6, output_02_A_7], axis=0)
    output.to_csv(output_final_path)
    return output

def run_assets_by_sections_ita(company:str, unique_id:str, api_key:str, master_list:pd.DataFrame)->pd.DataFrame:
    ### V funkcijo za bolj granularno

    pdf_path, page_number, output_pdf_path, output_final_path, table_type =  extract_paths(master_list, unique_id)
    extract_page(pdf_path, output_pdf_path, page_number)
    
    client = Mistral(api_key=api_key)
    class_output = AssetBalanceSheetAssetsIta    
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_1 = extracted_to_df(extracted_data, company)
    
    class_output = AssetBalanceSheetEquityInvestmentsIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_2 = extracted_to_df(extracted_data, company)

    class_output = AssetBalanceSheetBondInvestmentsIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_3 = extracted_to_df(extracted_data, company)
    
    class_output = AssetBalanceSheetLoanInvestmentsIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_4 = extracted_to_df(extracted_data, company)
    
    class_output = AssetBalanceSheetLoansAndRecoverablesIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_5 = extracted_to_df(extracted_data, company)
        
    class_output = AssetBalanceSheetLoansAndRecoverablesIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_6 = extracted_to_df(extracted_data, company)
      
    class_output = AssetBalanceSheetRestIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_A_7 = extracted_to_df(extracted_data, company)
    
    output = pd.concat([output_02_A_1, output_02_A_2, output_02_A_3, output_02_A_4, output_02_A_5, output_02_A_6, output_02_A_7], axis=0)
    output.to_csv(output_final_path)
    return output

def run_liability_by_sections(company:str, unique_id:str, api_key:str, master_list:pd.DataFrame)->pd.DataFrame:
    
    pdf_path, page_number, output_pdf_path, output_final_path, table_type =  extract_paths(master_list, unique_id)
    extract_page(pdf_path, output_pdf_path, page_number)

    client = Mistral(api_key=api_key)
    class_output = LiabilityBalanceSheetNonLife
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_L_1 = extracted_to_df(extracted_data, company)

    class_output = LiabilityBalanceSheetHealth
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_L_2 = extracted_to_df(extracted_data, company)
    
    class_output = LiabilityBalanceSheetLife
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))   
    output_02_L_3 = extracted_to_df(extracted_data, company)
    
    class_output = LiabilityBalanceSheetDebt
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_L_4 = extracted_to_df(extracted_data, company)

    class_output = LiabilityBalanceSheetPayables
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_L_5 = extracted_to_df(extracted_data, company)

    output_02_L = pd.concat([output_02_L_1, output_02_L_2, output_02_L_3, output_02_L_4, output_02_L_5], axis=0)
    output_02_L.to_csv(output_final_path)
    
    return output_02_L

def run_liability_by_sections_ita(company:str, unique_id:str, api_key:str, master_list:pd.DataFrame)->pd.DataFrame:
    
    pdf_path, page_number, output_pdf_path, output_final_path, table_type =  extract_paths(master_list, unique_id)
    extract_page(pdf_path, output_pdf_path, page_number)

    client = Mistral(api_key=api_key)
    class_output = LiabilityBalanceSheetNonLifeIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_L_1 = extracted_to_df(extracted_data, company)

    class_output = LiabilityBalanceSheetHealthIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_L_2 = extracted_to_df(extracted_data, company)
    
    class_output = LiabilityBalanceSheetLifeIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))   
    output_02_L_3 = extracted_to_df(extracted_data, company)
    
    class_output = LiabilityBalanceSheetDebtIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_L_4 = extracted_to_df(extracted_data, company)

    class_output = LiabilityBalanceSheetPayablesIta
    annotations_response = call_mistral(client=client, output_pdf_path = output_pdf_path, pydantic_model = class_output)
    extracted_data = class_output(**json.loads(annotations_response.document_annotation))
    output_02_L_5 = extracted_to_df(extracted_data, company)

    output_02_L = pd.concat([output_02_L_1, output_02_L_2, output_02_L_3, output_02_L_4, output_02_L_5], axis=0)
    output_02_L.to_csv(output_final_path)
    
    return output_02_L

def run_company_S_02_01_02(company:str, api_key:str, master_list:pd.DataFrame)->pd.DataFrame:
    
    relevant_rows = master_list.loc[master_list.loc[:,"company"] == company,:]
    
    for id in relevant_rows.index:    
        if relevant_rows.loc[id,"type"] == "B":
            out_A = run_assets_by_sections(company, id, api_key, master_list)
            out_L = run_liability_by_sections(company, id, api_key, master_list)
        elif relevant_rows.loc[id,"type"] == "B_ITA":
            out_A = run_assets_by_sections_ita(company, id, api_key, master_list)
            out_L = run_liability_by_sections_ita(company, id, api_key, master_list)
        elif relevant_rows.loc[id,"type"] == "A":
            out_A = run_assets_by_sections(company, id, api_key, master_list)     
        elif relevant_rows.loc[id,"type"] == "L":
            out_L = run_liability_by_sections(company, id, api_key, master_list)
        elif relevant_rows.loc[id,"type"] == "A_ITA":
            out_A = run_assets_by_sections_ita(company, id, api_key, master_list)
        elif relevant_rows.loc[id,"type"] == "L_ITA":
            out_L = run_liability_by_sections_ita(company, id, api_key, master_list)

    return pd.concat([out_A, out_L], axis=0)    