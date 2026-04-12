from pydantic import BaseModel, Field

##### Schema for the S.23.01.01 table ######
class OwnFundsBasic(BaseModel):
    """Table S.23.01.01 fields values. Only values in column C0010."""

    R0010: float = Field(..., description="Value in row with description Ordinary share capital (gross of own shares) and code R0010")
    R0030: float = Field(..., description="Value in row with description Share premium account related to ordinary share capital and code R0030")
    R0040: float = Field(..., description="Value in row with description Initial funds, members' contributions or the equivalent basic own - fund item for mutual and mutual-type undertakings and code R0040")
    R0050: float = Field(..., description="Value in row with description Subordinated mutual member accounts and code R0050")
    R0070: float = Field(..., description="Value in row with description Surplus funds and code R0070")
    R0090: float = Field(..., description="Value in row with description Preference shares and code R0090")
    R0110: float = Field(..., description="Value in row with description Share premium account related to preference shares and code R0110")
    R0130: float = Field(..., description="Value in row with description Reconciliation reserve and code R0130")
    R0140: float = Field(..., description="Value in row with description Subordinated liabilities and code R0140")
    R0160: float = Field(..., description="Value in row with description An amount equal to the value of net deferred tax assets and code R0160")
    R0180: float = Field(..., description="Value in row with description Other own fund items approved by the supervisory authority as basic own funds not specified above and code R0180")

class OwnFundsBasicIta(BaseModel):
    """Table S.23.01.01 fields values. Only values in column C0010."""

    R0010: float = Field(..., description="Value in row with description Capitale sociale ordinario (al lordo delle azioni proprie) and code R0010")
    R0030: float = Field(..., description="Value in row with description Sovrapprezzo di emissione relativo al capitale sociale ordinario and code R0030")
    R0040: float = Field(..., description="Value in row with description Fondi iniziali, contributi dei membri o elemento equivalente dei fondi propri di base per le mutue e le imprese a forma mutualistica and code R0040")
    R0050: float = Field(..., description="Value in row with description Conti subordinati dei membri delle mutue and code R0050")
    R0070: float = Field(..., description="Value in row with description Riserve di utili and code R0070")
    R0090: float = Field(..., description="Value in row with description Azioni privilegiate and code R0090")
    R0110: float = Field(..., description="Value in row with description Sovrapprezzo di emissione relativo alle azioni privilegiate and code R0110")
    R0130: float = Field(..., description="Value in row with description Riserva di riconciliazione and code R0130")
    R0140: float = Field(..., description="Value in row with description Passività subordinate and code R0140")
    R0160: float = Field(..., description="Value in row with description Importo pari al valore delle attività fiscali differite nette and code R0160")
    R0180: float = Field(..., description="Value in row with description Altri elementi dei fondi propri approvati dall'autorità di vigilanza come fondi propri di base non specificati in precedenza and code R0180")


class OwnFundsDeductions(BaseModel):
    """Table S.23.01.01 fields values. Only values in column C0010."""

    R0220: float = Field(..., description="Value in row with description Own funds from the financial statements that should not be represented by the reconciliation reserve and do not meet the criteria to be classified as Solvency II own funds and code R0220")
    R0230: float = Field(..., description="Value in row with description Deductions for participations in financial and credit institutions and code R0230")
    R0290: float = Field(..., description="Value in row with description Total basic own funds after deductions and code R0290")


class OwnFundsDeductionsIta(BaseModel):
    """Table S.23.01.01 fields values. Only values in column C0010."""

    R0220: float = Field(..., description="Value in row with description Fondi propri in bilancio che non sono rappresentati dalla riserva di riconciliazione e che non soddisfano i criteri per essere classificati come fondi propri ai fini di solvibilità II and code R0220")
    R0230: float = Field(..., description="Value in row with description Deduzioni per partecipazioni in enti creditizi e finanziari and code R0230")
    R0290: float = Field(..., description="Value in row with description Totale dei fondi propri di base dopo le deduzioni and code R0290")

class OwnFundsAuxiliaryOwnFunds(BaseModel):
    """Table S.23.01.01 fields values. Only values in column C0010."""

    R0300: float = Field(..., description="Value in row with description Unpaid and uncalled ordinary share capital callable on demand and code R0300")
    R0310: float = Field(..., description="Value in row with description Unpaid and uncalled initial funds, members' contributions or the equivalent basic own fund item for mutual and mutual - type undertakings, callable on demand and code R0310")
    R0320: float = Field(..., description="Value in row with description Unpaid and uncalled preference shares callable on demand and code R0320")
    R0330: float = Field(..., description="Value in row with description A legally binding commitment to subscribe and pay for subordinated liabilities on demand and code R0330")
    R0340: float = Field(..., description="Value in row with description Letters of credit and guarantees under Article 96(2) of the Directive 2009/138/EC and code R0340")
    R0350: float = Field(..., description="Value in row with description Letters of credit and guarantees other than under Article 96(2) of the Directive 2009/138/EC and code R0350")
    R0360: float = Field(..., description="Value in row with description Supplementary members calls under first subparagraph of Article 96(3) of the Directive 2009/138/EC and code R0360")
    R0370: float = Field(..., description="Value in row with description Supplementary members calls - other than under first subparagraph of Article 96(3) of the Directive 2009/138/EC and code R0370")
    R0390: float = Field(..., description="Value in row with description Other ancillary own funds and code R0390")
    R0400: float = Field(..., description="Value in row with description Total ancillary own fundsand code R0400")


class OwnFundsAuxiliaryOwnFundsIta(BaseModel):
    """Table S.23.01.01 fields values. Only values in column C0010."""

    R0300: float = Field(..., description="Value in row with description Capitale sociale ordinario non versato e non richiamato richiamabile su richiesta and code R0300")
    R0310: float = Field(..., description="Value in row with description Unpaid and uncalled initial funds, members' contributions or the equivalent basic own fund item for mutual and mutual - type undertakings, callable on demand and code R0310")
    R0320: float = Field(..., description="Value in row with description Unpaid and uncalled preference shares callable on demand and code R0320")
    R0330: float = Field(..., description="Value in row with description A legally binding commitment to subscribe and pay for subordinated liabilities on demand and code R0330")
    R0340: float = Field(..., description="Value in row with description Letters of credit and guarantees under Article 96(2) of the Directive 2009/138/EC and code R0340")
    R0350: float = Field(..., description="Value in row with description Letters of credit and guarantees other than under Article 96(2) of the Directive 2009/138/EC and code R0350")
    R0360: float = Field(..., description="Value in row with description Supplementary members calls under first subparagraph of Article 96(3) of the Directive 2009/138/EC and code R0360")
    R0370: float = Field(..., description="Value in row with description Supplementary members calls - other than under first subparagraph of Article 96(3) of the Directive 2009/138/EC and code R0370")
    R0390: float = Field(..., description="Value in row with description Other ancillary own funds and code R0390")
    R0400: float = Field(..., description="Value in row with description Total ancillary own fundsand code R0400")


class OwnFundsRest(BaseModel):
    """Table S.23.01.01 fields values. Only values in column C0010."""

    R0500: float = Field(..., description="Value in row with description Total available own funds to meet the SCR and code R0500")
    R0510: float = Field(..., description="Value in row with description Total available own funds to meet the MCR and code R0510")
    R0540: float = Field(..., description="Value in row with description Total eligible own funds to meet the SCR and code R0540")
    R0550: float = Field(..., description="Value in row with description Total eligible own funds to meet the MCR and code R0550")
    R0580: float = Field(..., description="Value in row with description SCR and code R0580")
    R0600: float = Field(..., description="Value in row with description MCR and code R0600")
    R0620: float = Field(..., description="Value in row with description Ratio of Eligible own funds to SCR and code R0620")
    R0640: float = Field(..., description="Value in row with description Ratio of Eligible own funds to MCR and code R0640")


class OwnFundsRestIta(BaseModel):
    """Table S.23.01.01 fields values. Only values in column C0010."""

    R0500: float = Field(..., description="Value in row with description Totale dei fondi propri disponibili per soddisfare il requisito patrimoniale di solvibilità (SCR) and code R0500")
    R0510: float = Field(..., description="Value in row with description Totale dei fondi propri disponibili per soddisfare il requisito patrimoniale minimo (MCR) and code R0510")
    R0540: float = Field(..., description="Value in row with description Totale dei fondi propri ammissibili per soddisfare il requisito patrimoniale di solvibilità (SCR) and code R0540")
    R0550: float = Field(..., description="Value in row with description Totale dei fondi propri ammissibili per soddisfare il requisito patrimoniale minimo (MCR) and code R0550")
    R0580: float = Field(..., description="Value in row with description SCR and code R0580")
    R0600: float = Field(..., description="Value in row with description Requisito patrimoniale minimo (MCR) and code R0600")
    R0620: float = Field(..., description="Value in row with description Rapporto tra fondi propri ammissibili e SCR and code R0620")
    R0640: float = Field(..., description="Value in row with description Rapporto tra fondi propri ammissibili e MCR and code R0640")
