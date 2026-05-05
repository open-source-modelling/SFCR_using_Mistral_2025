from pydantic import BaseModel, Field

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetAssets(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010"""

    R0010: float = Field(..., description="Number in row with description Goodwill of the company and code R0010")
    R0030: float = Field(..., description="Number in row with description Intangible assets and code R0030")
    R0040: float = Field(..., description="Number in row with description Deferred tax assets and code R0040")
    R0050: float = Field(..., description="Number in row with description Pension benefit surplus and code R0050")
    R0060: float = Field(..., description="Number in row with description Property, plant & equipment held for own use and code R0060")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetEquityInvestments(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010"""

    R0070: float = Field(..., description="Number in row with description Investments (other than assets held for index-linked and unit-linked contracts) and code R0070")
    R0080: float = Field(..., description="Number in row with description Property (other than for own use) and code R0080")
    R0090: float = Field(..., description="Number in row with description Holdings in related undertakings, including participations and code R0090")
    R0100: float = Field(..., description="Number in row with description Equities and code R0100")
    R0110: float = Field(..., description="Number in row with description Equities - listed and code R0110")
    R0120: float = Field(..., description="Number in row with description Equities - unlisted and code R0120")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetBondInvestments(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010."""

    R0130: float = Field(..., description="Number in row with description Bonds and code R0130")
    R0140: float = Field(..., description="Number in row with description Government Bonds and code R0140")
    R0150: float = Field(..., description="Number in row with description Corporate Bonds and code R0150")
    R0160: float = Field(..., description="Number in row with description Structured notes and code R0160")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetLoanInvestments(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010."""
    
    R0170: float = Field(..., description="Number in row with description Collateralised securities and code R0170")
    R0180: float = Field(..., description="Number in row with description Collective Investments Undertakings and code R0180")
    R0190: float = Field(..., description="Number in row with description Derivatives and code R0190")
    R0200: float = Field(..., description="Number in row with description Deposits other than cash equivalents and code R0200")
    R0210: float = Field(..., description="Number in row with description Other investments and code R0210")
    R0220: float = Field(..., description="Number in row with description Assets held for index-linked and unit-linked contracts and code R0220")


# Schema for the S.02.01.02 asset table
class AssetBalanceSheetLoansAndRecoverables(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010."""
    
    R0230: float = Field(..., description="Number in row with description Loans and mortgages and code R0230")
    R0240: float = Field(..., description="Number in row with description Loans on policies and code R0240")
    R0250: float = Field(..., description="Number in row with description Loans and mortgages to individuals and code R0250")
    R0260: float = Field(..., description="Number in row with description Other loans and mortgages and code R0260")
    R0270: float = Field(..., description="Number in row with description Reinsurance recoverables from and code R02 R029070")
    R0280: float = Field(..., description="Number in row with description Non-life and alth similar to non-life and code R0280")
    R0290: float = Field(..., description="Value in row with description Non-life excluding health and code R0290")
    R0300: float = Field(..., description="Value in row with description Health similar to non-life and code R0300")
    R0310: float = Field(..., description="Value in row with description Life and health similar to life, excluding health and index-linked and unit-linked and code R0310")
    R0320: float = Field(..., description="Value in row with description Health similar to life and code R0320")
    R0330: float = Field(..., description="Value in row with description Life excluding health and index-linked and unit-linked and code R0330")
    R0340: float = Field(..., description="Value in row with description Life index-linked and unit-linked and code R0340")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetRest(BaseModel):
    """Table S.02.01.02 fields values. Only values in column C0010."""
    
    R0350: float = Field(..., description="Value in row with description Deposits to cedants and code  R0350")
    R0360: float = Field(..., description="Value in row with description Insurance and intermediaries receivables and code R0360")
    R0370: float = Field(..., description="Value in row with description Reinsurance receivables and code R0370")
    R0380: float = Field(..., description="Value in row with description Receivables (trade, not insurance) and code R0380")
    R0390: float = Field(..., description="Value in row with description Own shares (held directly) and code R0390")
    R0400: float = Field(..., description="Value in row with description Amounts due in respect of own fund items or initial fund called up but not yet paid in and code R0400")
    R0410: float = Field(..., description="Value in row with description Cash and cash equivalents and code R0410")
    R0420: float = Field(..., description="Value in row with description Any other assets, not elsewhere shown and code R0420")
    R0500: float = Field(..., description="Value in row with description Total assets and code R0500")

# Schema for the S.02.01.02 asset table
class LiabilityBalanceSheetNonLife(BaseModel):
    """Table S.02.01.02 fields values associated with non-life technical provisions. Only values in column C0010."""

    R0510: float = Field(..., description="Value associated with description Technical provisions - non-life and code R0510")
    R0520: float = Field(..., description="Value in row with description Technical provisions - non-life (excluding health) and code R0520")
    R0530: float = Field(..., description="Value in row with description TP calculated as a whole and code R0530")
    R0540: float = Field(..., description="Value in row with description Best Estimate and code R0540")
    R0550: float = Field(..., description="Value in row with description Risk margin and code R0550")

class LiabilityBalanceSheetHealth(BaseModel):    
    """Table S.02.01.02 fields values associated with health technical provisions. Only values in column C0010."""
    
    R0560: float = Field(..., description="Value in row with description Technical provisions - health (similar to non-life) and code R0560")
    R0570: float = Field(..., description="Value in row with description TP calculated as a whole and code R0570")
    R0580: float = Field(..., description="Value in row with description Best Estimate and code R0580")
    R0590: float = Field(..., description="Value in row with description Risk margin and code R0590")

# Schema for the S.02.01.02 asset table
class LiabilityBalanceSheetLife(BaseModel):
    """Table S.02.01.02 fields values associated with Life provisions. Only values in column C0010."""
    
    R0600: float = Field(..., description="Value in row with description technical provisions - life (excluding index-linked and unit-linked) and code R0600")
    R0610: float = Field(..., description="Value in row with description technical provisions - health (similar to life) and code R0610")
    R0620: float = Field(..., description="Value in row with description TP calculated as a whole and code R0620")
    R0630: float = Field(..., description="Value in row with description Best Estimate and code R0630")
    R0640: float = Field(..., description="Value in row with description Risk margin and code R0640")
    R0650: float = Field(..., description="Value in row with description technical provisions - life (excluding health and index-linked and unit-linked) and code R0650")
    R0660: float = Field(..., description="Value in row with description TP calculated as a whole and code R0660")
    R0670: float = Field(..., description="Value in row with description Best Estimate and code R0670")
    R0680: float = Field(..., description="Value in row with description Risk margin and code R0680")
    R0690: float = Field(..., description="Value in row with description technical provisions - index-linked and unit-linked and code R0690")
    R0700: float = Field(..., description="Value in row with description TP calculated as a whole and code R0700")
    R0710: float = Field(..., description="Value in row with description Best Estimate and code R0710")
    R0720: float = Field(..., description="Value in row with description Risk margin and code R0720")

# Schema for the S.02.01.02 asset table
class LiabilityBalanceSheetDebt(BaseModel):
    """Table S.02.01.02 fields values. Only values in column C0010."""
    
    R0730: float = Field(..., description="Value in row with description Other technical provisions and code R0730")
    R0740: float = Field(..., description="Value in row with description Contingent liabilities and code R0740")
    R0750: float = Field(..., description="Value in row with description Provisions other than technical provisions and code R0750")
    R0760: float = Field(..., description="Value in row with description Pension benefit obligations and code R0760")
    R0770: float = Field(..., description="Value in row with description Deposits from reinsurers and code R0770")
    R0780: float = Field(..., description="Value in row with description Deferred tax liabilities and code R0780")
    R0790: float = Field(..., description="Value in row with description Derivatives and code R0790")
    R0800: float = Field(..., description="Value in row with description Debts owed to credit institutions and code R0800")
    R0810: float = Field(..., description="Value in row with description Financial liabilities other than debts owed to credit institutions and code R0810")


class LiabilityBalanceSheetPayables(BaseModel):
    """Table S.02.01.02 fields values.Only values in column C0010."""
    
    R0820: float = Field(..., description="Value in row with description Insurance & intermediaries payables and code R0820")
    R0830: float = Field(..., description="Value in row with description Reinsurance payables and code R0830")
    R0840: float = Field(..., description="Value in row with description Payables (trade, not insurance) and code R0840")
    R0850: float = Field(..., description="Value in row with description Subordinated liabilities and code R0850")
    R0860: float = Field(..., description="Value in row with description Subordinated liabilities not in BOF and code R0860")
    R0870: float = Field(..., description="Value in row with description Subordinated liabilities in BOF and code R0870")
    R0880: float = Field(..., description="Value in row with description Any other liabilities, not elsewhere shown and code R0880")
    R0890: float = Field(..., description="Value in row with code R0890")
    R0900: float = Field(..., description="Value in row with description Total liabilities and code R0900")
    R1000: float = Field(..., description="Value in row with description Excess of assets over liabilities and code R1000")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetAssetsIta(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010"""
    
    R0010: float = Field(..., description="Number in row with description Goodwill of the company and code R0010. ")
    R0030: float = Field(..., description="Number in row with description Attività immateriali and code R0030")
    R0040: float = Field(..., description="Number in row with description Attività fiscali differite and code R0040")
    R0050: float = Field(..., description="Number in row with description Utili da prestazioni pensionistiche and code R0050")
    R0060: float = Field(..., description="Number in row with description Immobili, impianti e attrezzature posseduti per uso proprio and code R0060")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetEquityInvestmentsIta(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010"""
    
    R0070: float = Field(..., description="Number in row with description Investimenti (diversi da attività detenute per contratti collegati a un indice e collegati a quote) and code R0070")
    R0080: float = Field(..., description="Number in row with description Immobili (diversi da quelli per uso proprio) and code R0080")
    R0090: float = Field(..., description="Number in row with description Quote detenute in imprese partecipate, incluse le partecipazioni and code R0090 ")
    R0100: float = Field(..., description="Number in row with description Strumenti di capitale and code R0100")
    R0110: float = Field(..., description="Number in row with description Strumenti di capitale - Quotati and code R0110")
    R0120: float = Field(..., description="Number in row with description Strumenti di capitale - Non quotati and code R0120")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetBondInvestmentsIta(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010."""
    
    R0130: float = Field(..., description="Number in row with description Obbligazioni and code R0130")
    R0140: float = Field(..., description="Number in row with description Obbligazioni and code R0140")
    R0150: float = Field(..., description="Number in row with description Obbligazioni societarie and code R0150")
    R0160: float = Field(..., description="Number in row with description Obbligazioni strutturate and code R0160")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetLoanInvestmentsIta(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010."""
    
    R0170: float = Field(..., description="Number in row with description Titoli garantiti and code R0170")
    R0180: float = Field(..., description="Number in row with description Organismi di investimento collettivo and code R0180")
    R0190: float = Field(..., description="Number in row with description Derivati and code R0190")
    R0200: float = Field(..., description="Number in row with description Depositi diversi da equivalenti a contante and code R0200")
    R0210: float = Field(..., description="Number in row with description Altri investimenti and code R0210")
    R0220: float = Field(..., description="Number in row with description Attività detenute per contratti collegati a un indice e collegati a quote and code R0220")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetLoansAndRecoverablesIta(BaseModel):
    """Table of selected field values in table S.02.01.02. Only values in column C0010."""
    
    R0230: float = Field(..., description="Number in row with description Mutui ipotecari e prestiti and code R0230")
    R0240: float = Field(..., description="Number in row with description Prestiti su polizze and code R0240")
    R0250: float = Field(..., description="Number in row with description Mutui ipotecari e prestiti a persone fisiche and code R0250")
    R0260: float = Field(..., description="Number in row with description Altri mutui ipotecari e prestiti and code R0260")
    R0270: float = Field(..., description="Number in row with description Importi recuperabili da riassicurazione da and code R02 R029070")
    R0280: float = Field(..., description="Number in row with description Non vita e malattia simile a non vita and code R0280")
    R0290: float = Field(..., description="Value in row with description Non vita esclusa malattia and code R0290")
    R0300: float = Field(..., description="Value in row with description Malattia simile a non vita and code R0300")
    R0310: float = Field(..., description="Value in row with description Vita e malattia simile a vita, escluse malattia, collegata a un indice e collegata a quote and code R0310")
    R0320: float = Field(..., description="Value in row with description Malattia simile a vita and code R0320")
    R0330: float = Field(..., description="Value in row with description Vita, escluse malattia, collegata a un indice e collegata a quote and code R0330")
    R0340: float = Field(..., description="Value in row with description Vita collegata a un indice e collegata a quote and code R0340")

# Schema for the S.02.01.02 asset table
class AssetBalanceSheetRestIta(BaseModel):
    """Table S.02.01.02 fields values. Only values in column C0010."""
    
    R0350: float = Field(..., description="Value in row with description Depositi presso imprese cedenti and code R0350")
    R0360: float = Field(..., description="Value in row with description Crediti assicurativi e verso intermediari and code R0360")
    R0370: float = Field(..., description="Value in row with description Crediti riassicurativi and code R0370")
    R0380: float = Field(..., description="Value in row with description Crediti (commerciali, non assicurativi) and code R0380")
    R0390: float = Field(..., description="Value in row with description Azioni proprie (detenute direttamente) and code R0390")
    R0400: float = Field(..., description="Value in row with description Importi dovuti per elementi dei fondi propri o fondi iniziali richiamati ma non ancora versati and code R0400")
    R0410: float = Field(..., description="Value in row with description Contante ed equivalenti a contante and code R0410")
    R0420: float = Field(..., description="Value in row with description Tutte le altre attività non indicate altrove and code R0420")
    R0500: float = Field(..., description="Value in row with description Totale delle attività and code R0500")

# Schema for the S.02.01.02 asset table
class LiabilityBalanceSheetNonLifeIta(BaseModel):
    """Table S.02.01.02 fields values associated with non-life technical provisions. Only values in column C0010."""

    R0510: float = Field(..., description="Value associated with description Riserve tecniche - Non vita and code R0510")
    R0520: float = Field(..., description="Value in row with description Riserve tecniche - Non vita (esclusa malattia) and code R0520")
    R0530: float = Field(..., description="Value in row with description Riserve tecniche calcolate come un elemento unico and code R0530")
    R0540: float = Field(..., description="Value in row with description Migliore stima and code R0540")
    R0550: float = Field(..., description="Value in row with description Margine di rischio and code R0550")

class LiabilityBalanceSheetHealthIta(BaseModel):    
    """Table S.02.01.02 fields values associated with health technical provisions. Only values in column C0010."""
    
    R0560: float = Field(..., description="Value in row with description Riserve tecniche - Malattia (simile a non vita) and code R0560")
    R0570: float = Field(..., description="Value in row with description Riserve tecniche calcolate come un elemento unico and code R0570")
    R0580: float = Field(..., description="Value in row with description Migliore stima and code R0580")
    R0590: float = Field(..., description="Value in row with description Margine di rischio and code R0590")

# Schema for the S.02.01.02 asset table
class LiabilityBalanceSheetLifeIta(BaseModel):
    """Table S.02.01.02 fields values associated with Life provisions. Only values in column C0010."""
    
    R0600: float = Field(..., description="Value in row with description Riserve tecniche - Vita (escluse collegata a un indice e collegata a quote) and code R0600")
    R0610: float = Field(..., description="Value in row with description Riserve tecniche - Malattia (simile a vita) and code R0610")
    R0620: float = Field(..., description="Value in row with description Riserve tecniche calcolate come un elemento unico and code R0620")
    R0630: float = Field(..., description="Value in row with description Migliore stima and code R0630")
    R0640: float = Field(..., description="Value in row with description Margine di rischio and code R0640")
    R0650: float = Field(..., description="Value in row with description Riserve tecniche - Vita (escluse malattia, collegata a un indice e collegata a quote) and code R0650")
    R0660: float = Field(..., description="Value in row with description Riserve tecniche calcolate come un elemento unico and code R0660")
    R0670: float = Field(..., description="Value in row with description Migliore stima and code R0670")
    R0680: float = Field(..., description="Value in row with description Margine di rischio and code R0680")
    R0690: float = Field(..., description="Value in row with description Riserve tecniche - Collegata a un indice e collegata a quote and code R0690")
    R0700: float = Field(..., description="Value in row with description Riserve tecniche calcolate come un elemento unico and code R0700")
    R0710: float = Field(..., description="Value in row with description Migliore stima and code R0710")
    R0720: float = Field(..., description="Value in row with description Margine di rischio and code R0720")


# Schema for the S.02.01.02 asset table
class LiabilityBalanceSheetDebtIta(BaseModel):
    """Table S.02.01.02 fields values. Only values in column C0010."""

    R0730: float = Field(..., description="Value in row with description Other technical provisions and code R0730")
    R0740: float = Field(..., description="Value in row with description Passività potenziali and code R0740")
    R0750: float = Field(..., description="Value in row with description Riserve diverse dalle riserve tecniche and code R0750")
    R0760: float = Field(..., description="Value in row with description Obbligazioni da prestazioni pensionistiche and code R0760")
    R0770: float = Field(..., description="Value in row with description Depositi dai riassicuratori and code R0770")
    R0780: float = Field(..., description="Value in row with description Passività fiscali differite and code R0780")
    R0790: float = Field(..., description="Value in row with description Derivati and code R0790")
    R0800: float = Field(..., description="Value in row with description Debiti verso enti creditizi and code R0800")
    R0810: float = Field(..., description="Value in row with description Passività finanziarie diverse da debiti verso enti creditizi and code R0810")

class LiabilityBalanceSheetPayablesIta(BaseModel):
    """Table S.02.01.02 fields values.Only values in column C0010."""
    
    R0820: float = Field(..., description="Value in row with description Debiti assicurativi e verso intermediari and code R0820")
    R0830: float = Field(..., description="Value in row with description Debiti riassicurativi and code R0830")
    R0840: float = Field(..., description="Value in row with description Debiti (commerciali, non assicurativi) and code R0840")
    R0850: float = Field(..., description="Value in row with description Passività subordinate and code R0850")
    R0860: float = Field(..., description="Value in row with description Passività subordinate non incluse nei fondi propri di base and code R0860")
    R0870: float = Field(..., description="Value in row with description Passività subordinate incluse nei fondi propri di base and code R0870")
    R0880: float = Field(..., description="Value in row with description Tutte le altre passività non segnalate altrove and code R0880")
    R0890: float = Field(..., description="Value in row with code R0890")
    R0900: float = Field(..., description="Value in row with description Totale delle passività and code R0900")
    R1000: float = Field(..., description="Value in row with description Eccedenza delle attività rispetto alle passività and code R1000")
