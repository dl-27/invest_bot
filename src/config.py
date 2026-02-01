"""
src/config.py
-------------
Defines the STATIC stock universe.
Top ~30 companies by capitalization for each Sector & Region.
"""

# SECTOR -> REGION -> List of Tickers
SECTOR_UNIVERSE = {
    "Technology": {
        "US": [
            "NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "AVGO", "ORCL", "CRM", "ADBE",
            "AMD", "QCOM", "TXN", "INTC", "IBM", "AMAT", "NOW", "UBER", "PANW", "MU",
            "SNPS", "CDNS", "KLAC", "LRCX", "ROP", "NXPI", "FTNT", "APH", "ADI", "PLTR"
        ],
        "Germany": [
            "SAP.DE", "IFX.DE", "AIXA.DE", "NEM.DE", "GFT.DE", "S92.DE", "COP.DE", "UTDI.DE",
            "O2D.DE", "DRI.DE", "WAF.DE", "AFX.DE", "DTE.DE" # Telecommunications included in Tech
        ],
        "UK": [
            "REL.L", "SGE.L", "AUTO.L", "HLMA.L", "AV.L", "SPT.L", "KAY.L", "DARK.L",
            "BME.L", "RMV.L", "CNA.L", "TRN.L", "OCT.L", "SOFT.L", "ROO.L"
        ],
        "Japan": [
            "6758.T", "8035.T", "6861.T", "6501.T", "7974.T", "6981.T", "6954.T", "6902.T",
            "6701.T", "6702.T", "6723.T", "6503.T", "6762.T", "6479.T", "7751.T", "6971.T",
            "6857.T", "6920.T", "6752.T", "4901.T", "6963.T", "6976.T", "6841.T", "6724.T"
        ],
        "Europe": [
            "ASML.AS", "SAP.DE", "PROX.BR", "CAP.PA", "DSY.PA", "STM.PA", "NOKIA.HE", "ERIC-B.ST",
            "ADYEN.AS", "AMAD.MC", "HEXA-B.ST", "INVE-B.ST", "LOGN.SW", "TEMN.SW", "ASM.AS"
        ]
    },
    "Healthcare": {
        "US": [
            "LLY", "UNH", "JNJ", "ABBV", "MRK", "TMO", "AMGN", "PFE", "ISRG", "DHR",
            "VRTX", "REGN", "SYK", "BMY", "GILD", "BSX", "ZTS", "MDT", "CVS", "CI",
            "BDX", "HCA", "MCK", "EW", "HUM", "COR", "IDXX", "IQV", "A", "DXCM"
        ],
        "Germany": [
            "SIE.DE", "BAYN.DE", "MRK.DE", "FME.DE", "SHL.DE", "FRE.DE", "SRT.DE", "SRT3.DE",
            "EVT.DE", "PFV.DE", "DRW3.DE", "AFX.DE", "M12.DE", "COP.DE"
        ],
        "UK": [
            "AZN.L", "GSK.L", "SN.L", "HIK.L", "DPH.L", "HLN.L", "CNV.L", "GNS.L", "SDR.L",
            "OXB.L", "PHP.L", "UDG.L", "NMC.L", "MTO.L"
        ],
        "Japan": [
            "4568.T", "4519.T", "4503.T", "4502.T", "4523.T", "4543.T", "4507.T", "4578.T",
            "4528.T", "4506.T", "4151.T", "4536.T", "4569.T", "4555.T", "4587.T", "4516.T"
        ],
        "Europe": [
            "NVO", "ROG.SW", "NOVN.SW", "SAN.PA", "LONN.SW", "ALC.SW", "UCB.BR", "ARGX.BR",
            "IPN.PA", "DIM.PA", "VIFN.SW", "SOON.SW", "GN.CO", "AMBU-B.CO", "COLO-B.CO"
        ]
    },
    "Finance": {
        "US": [
            "JPM", "V", "MA", "BAC", "WFC", "MS", "GS", "AXP", "BLK", "C",
            "SPGI", "PGR", "CB", "MMC", "USB", "SCHW", "AON", "ICE", "PNC", "TFC",
            "BK", "COF", "TRV", "AIG", "MET", "DFS", "HIG", "ALL", "FITB", "MTB"
        ],
        "Germany": [
            "ALV.DE", "MUV2.DE", "DBK.DE", "CBK.DE", "HNR1.DE", "TQA.DE", "HYQ.DE", "DB1.DE",
            "GKB.DE", "ARL.DE", "EVK.DE", "MLP.DE"
        ],
        "UK": [
            "HSBA.L", "LLOY.L", "BARC.L", "NWG.L", "LGEN.L", "STAN.L", "PRU.L", "AV.L",
            "LSEG.L", "SLA.L", "MNG.L", "PHNX.L", "IGG.L", "Hargreaves.L", "STJ.L"
        ],
        "Japan": [
            "8306.T", "8316.T", "8411.T", "8766.T", "8591.T", "8725.T", "8750.T", "8604.T",
            "8601.T", "8253.T", "8309.T", "8308.T", "8354.T", "8331.T", "8355.T"
        ],
        "Europe": [
            "BNP.PA", "SAN.MC", "INGA.AS", "ISP.MI", "UBSG.SW", "CS.PA", "ACA.PA", "KBC.BR",
            "DNB.OL", "NDA-FI.HE", "SEB-A.ST", "SHB-A.ST", "SWED-A.ST", "GLE.PA", "BBVA.MC"
        ]
    },
    "Consumer": {
        "US": [
            "AMZN", "TSLA", "WMT", "HD", "COST", "PG", "KO", "PEP", "MCD", "NKE",
            "SBUX", "LOW", "DIS", "PM", "TGT", "TJX", "BKNG", "ABNB", "MAR", "LULU",
            "F", "GM", "CMG", "YUM", "HLT", "DG", "ROST", "K", "MO", "CL"
        ],
        "Germany": [
            "VOW3.DE", "MBG.DE", "BMW.DE", "ADS.DE", "PAH3.DE", "ZAL.DE", "CON.DE", "HLE.DE",
            "PUM.DE", "BOSS.DE", "FIE.DE", "HFA.DE", "HOT.DE", "DHER.DE", "HFG.DE"
        ],
        "UK": [
            "ULVR.L", "DGE.L", "BATS.L", "TSCO.L", "RR.L", "IMB.L", "RB.L", "CPG.L",
            "SBRY.L", "MKS.L", "NXT.L", "ABF.L", "KGF.L", "WTB.L", "JMAT.L", "ENT.L"
        ],
        "Japan": [
            "7203.T", "7267.T", "9983.T", "9984.T", "7201.T", "6758.T", "7269.T", "7270.T",
            "2914.T", "4911.T", "2503.T", "2502.T", "4452.T", "7202.T", "7211.T", "7261.T"
        ],
        "Europe": [
            "MC.PA", "OR.PA", "RMS.PA", "KER.PA", "ITX.MC", "STLAM.MI", "RACE.MI", "HEIA.AS",
            "ABI.BR", "RI.PA", "EL.PA", "CDI.PA", "PIRC.MI", "MONC.MI", "CPR.MI"
        ]
    },
    "Energy & Ind.": {
        "US": [
            "XOM", "CVX", "GE", "CAT", "COP", "SLB", "EOG", "HON", "UPS", "LMT",
            "RTX", "DE", "UNP", "BA", "MMM", "ETN", "WM", "GD", "EMR", "PH",
            "PSX", "VLO", "MPC", "OXY", "HES", "KMI", "WMB", "HAL", "BKR", "OKE"
        ],
        "Germany": [
            "SIE.DE", "AIR.DE", "BAS.DE", "DHER.DE", "EOAN.DE", "RWE.DE", "MTX.DE", "HEI.DE",
            "DHD.DE", "SY1.DE", "KRN.DE", "LHA.DE", "TKA.DE", "KGX.DE", "WCH.DE"
        ],
        "UK": [
            "SHEL.L", "BP.L", "RIO.L", "GLEN.L", "NG.L", "BA.L", "AAL.L", "ANTO.L",
            "SSE.L", "CNA.L", "DCC.L", "PSON.L", "SMDS.L", "MNDI.L", "WEIR.L", "IMI.L"
        ],
        "Japan": [
            "8031.T", "8058.T", "6301.T", "8001.T", "8002.T", "5401.T", "7011.T", "6367.T",
            "6326.T", "6273.T", "6113.T", "6302.T", "6305.T", "5411.T", "5713.T"
        ],
        "Europe": [
            "TTE.PA", "SU.PA", "ENEL.MI", "IBE.MC", "DG.PA", "SAF.PA", "ENI.MI", "DSV.CO",
            "VOLV-B.ST", "ATCO-A.ST", "SAND.ST", "UPM.HE", "NES1V.HE", "REP.MC", "ENG.PA"
        ]
    }
}

# Config Settings
START_DATE = "2020-01-01"
END_DATE = "2024-01-01"
APP_TITLE = "Project Invest: Global Advisor"
APP_ICON = "🌐"

# Helper for sidebar dropdowns
REGIONS = ["US", "Germany", "UK", "Japan", "Europe"]
SECTORS = list(SECTOR_UNIVERSE.keys())