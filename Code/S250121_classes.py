from pydantic import BaseModel, Field

##### Schema for the S.25.01.21 Solvency Capital Requirement – for undertakings on Standard Formula table. Values R0010 to R0100. ######
class SCRRisk(BaseModel):
    """Table S.25.01.21 fields values. Only values in column C0110."""

    R0010: float = Field(..., description="Value in row with description Market risk and code R0010")
    R0020: float = Field(..., description="Value in row with description Counterparty default risk and code R0020")
    R0030: float = Field(..., description="Value in row with description Life underwriting risk and code R0030")
    R0040: float = Field(..., description="Value in row with description Health underwriting risk and code R0040")
    R0050: float = Field(..., description="Value in row with description Non-life underwriting risk and code R0050")
    R0060: float = Field(..., description="Value in row with description Diversification and code R0060")
    R0070: float = Field(..., description="Value in row with description Intangible asset risk and code R0070")
    R0100: float = Field(..., description="Value in row with description Basic Solvency Capital Requirement and code R0100")

##### Schema for the S.25.01.21 Solvency Capital Requirement – for undertakings on Standard Formula table. Values R0010 to R0100, if table in Italian ######
class SCRRiskIta(BaseModel):
    """Table S.25.01.21 fields values. Only values in column C0110."""

    R0010: float = Field(..., description="Value in row with description Rischio di mercato and code R0010")
    R0020: float = Field(..., description="Value in row with description Rischio di inadempimento della controparte and code R0020")
    R0030: float = Field(..., description="Value in row with description Rischio di sottoscrizione per l'assicurazione vita and code R0030")
    R0040: float = Field(..., description="Value in row with description Rischio di sottoscrizione per l'assicurazione malattia and code R0040")
    R0050: float = Field(..., description="Value in row with description Rischio di sottoscrizione per l'assicurazione non vita and code R0050")
    R0060: float = Field(..., description="Value in row with description Diversificazione and code R0060")
    R0070: float = Field(..., description="Value in row with description Rischio relativo alle attività immateriali and code R0070")
    R0100: float = Field(..., description="Value in row with description Requisito patrimoniale di solvibilità di base and code R0100")

