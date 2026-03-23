"""
src/config.py
-------------
Defines the stocks
"""

# sector -> region -> list of tickers
SECTOR_UNIVERSE = {
    "Technology": {
        "US": [
            "NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "AVGO", "ORCL", "CRM", "ADBE",
            "AMD", "INTC", "QCOM", "IBM", "TXN", "NOW", "INTU", "UBER", "ABNB", "PANW",
            "PLTR", "SNOW", "CRWD", "MDB", "SQ", "SHOP", "ZM", "TEAM", "WDAY", "ADSK"
        ],
        "Germany": [
            "SAP.DE", "IFX.DE", "AIXA.DE", "NEM.DE", "GFT.DE", "S92.DE", "UTDI.DE",
            "DTE.DE", "DRW3.DE", "AFX.DE", "JEN.DE", "NDX1.DE", "QIA.DE"
        ],
        "UK": [
            "REL.L", "SGE.L", "AUTO.L", "HLMA.L", "AV.L", "KAY.L", "TRN.L", "SGRO.L",
            "SBRY.L", "EXPN.L", "RMV.L", "WTB.L", "OCDO.L"
        ],
        "Japan": [
            "6758.T", "8035.T", "6861.T", "6501.T", "7974.T", "6981.T", "6954.T", "6702.T",
            "6701.T", "6503.T", "6723.T", "6920.T", "7751.T", "7733.T", "6902.T"
        ],
        "Europe": [
            "ASML.AS", "SAP.DE", "CAP.PA", "DSY.PA", "STMPA.PA", "NOKIA.HE", "ERIC-B.ST", "ADYEN.AS",
            "ASM.AS", "LOGN.SW", "TEMN.SW", "AMS.SW", "BESI.AS", "SOON.SW", "ATO.PA"
        ],
        "South Korea": [
            "005930.KS", "000660.KS", "035420.KS", "035720.KS", "006400.KS",
            "066570.KS", "028260.KS"
        ]
    },
    "Healthcare": {
        "US": [
            "LLY", "UNH", "JNJ", "ABBV", "MRK", "TMO", "AMGN", "PFE", "ISRG", "DHR",
            "BMY", "GILD", "CVS", "CI", "VRTX", "REGN", "ZTS", "SYK", "BDX", "BSX"
        ],
        "Germany": [
            "SIE.DE", "BAYN.DE", "MRK.DE", "FME.DE", "SHL.DE", "FRE.DE", "SRT.DE", "EVT.DE",
            "COK.DE", "AFX.DE", "M12.DE", "DRW3.DE", "PFV.DE"
        ],
        "UK": [
            "AZN.L", "GSK.L", "SN.L", "HIK.L", "HLN.L", "CTEC.L", "SDR.L",
            "LMP.L", "GNS.L"
        ],
        "Japan": [
            "4568.T", "4519.T", "4503.T", "4502.T", "4523.T", "4543.T", "4507.T", "4578.T",
            "4506.T", "4528.T", "4536.T", "4516.T"
        ],
        "Europe": [
            "NVO", "ROG.SW", "NOVN.SW", "SAN.PA", "LONN.SW", "ALC.SW", "UCB.BR", "ARGX.BR",
            "OR.PA", "ERF.PA", "DIM.PA", "IPN.PA", "GN.CO"
        ],
        "South Korea": [
            "207940.KS", "068270.KS", "000100.KS", "128940.KS", "326030.KS"
        ]
    },
    "Finance": {
        "US": [
            "JPM", "V", "MA", "BAC", "WFC", "MS", "GS", "AXP", "BLK", "C",
            "SCHW", "PGR", "CB", "MMC", "USB", "PNC", "TFC", "COF", "BK", "SPGI"
        ],
        "Germany": [
            "ALV.DE", "MUV2.DE", "DBK.DE", "CBK.DE", "HNR1.DE", "DB1.DE", "TLX.DE", "GKB.DE",
            "HYQ.DE"
        ],
        "UK": [
            "HSBA.L", "LLOY.L", "BARC.L", "NWG.L", "LGEN.L", "STAN.L", "PRU.L", "LSEG.L",
            "ABDN.L", "III.L", "IGG.L", "PHNX.L", "MNG.L"
        ],
        "Japan": [
            "8306.T", "8316.T", "8411.T", "8766.T", "8591.T", "8725.T", "8750.T", "8604.T",
            "8601.T", "8253.T", "8309.T", "7182.T", "8308.T"
        ],
        "Europe": [
            "BNP.PA", "SAN.MC", "INGA.AS", "ISP.MI", "UBSG.SW", "CS.PA", "ACA.PA", "GLE.PA",
            "KBC.BR", "NDA-FI.HE", "DNB.OL", "SEB-A.ST", "SHB-A.ST", "SWED-A.ST"
        ],
        "South Korea": [
            "105560.KS", "055550.KS", "086790.KS", "316140.KS", "032830.KS", "323410.KS"
        ]
    },
    "Consumer": {
        "US": [
            "AMZN", "TSLA", "WMT", "HD", "COST", "PG", "KO", "PEP", "MCD", "NKE",
            "PM", "DIS", "SBUX", "LOW", "TGT", "EL", "LULU", "MAR", "BKNG", "CMG"
        ],
        "Germany": [
            "VOW3.DE", "MBG.DE", "BMW.DE", "ADS.DE", "PAH3.DE", "ZAL.DE", "CON.DE", "PUM.DE",
            "HFG.DE", "BOSS.DE", "HOT.DE", "DUE.DE", "FIE.DE", "B4B.DE", "CEC.DE"
        ],
        "UK": [
            "ULVR.L", "DGE.L", "BATS.L", "TSCO.L", "RR.L", "IMB.L", "RKT.L", "CPG.L",
            "ABF.L", "MKS.L", "SBRY.L", "NXT.L", "KGF.L", "BRBY.L", "IHG.L"
        ],
        "Japan": [
            "7203.T", "7267.T", "9983.T", "9984.T", "7201.T", "6758.T", "7269.T", "7270.T",
            "7202.T", "7211.T", "2502.T", "2503.T", "4911.T", "8267.T", "3382.T"
        ],
        "Europe": [
            "MC.PA", "OR.PA", "RMS.PA", "KER.PA", "ITX.MC", "STLAM.MI", "RACE.MI", "AD.AS",
            "HEIA.AS", "ABI.BR", "RI.PA", "CFR.SW", "NESN.SW", "AIR.PA"
        ],
        "South Korea": [
            "005380.KS", "000270.KS", "012330.KS", "090430.KS", "097950.KS", "139480.KS"
        ]
    },
    "Energy & Ind.": {
        "US": [
            "XOM", "CVX", "GE", "CAT", "COP", "SLB", "EOG", "HON", "UPS", "LMT",
            "RTX", "BA", "DE", "MMM", "ETN", "WM", "UNP", "CSX", "NSC", "GD"
        ],
        "Germany": [
            "SIE.DE", "AIR.DE", "BAS.DE", "DHER.DE", "EOAN.DE", "RWE.DE", "MTX.DE", "HEI.DE",
            "DTG.DE", "LHA.DE", "DHL.DE", "KRN.DE", "FRA.DE", "HO.PA", "VNA.DE"
        ],
        "UK": [
            "SHEL.L", "BP.L", "RIO.L", "GLEN.L", "NG.L", "BA.L", "AAL.L", "ANTO.L",
            "DCC.L", "MNDI.L", "CRDA.L", "JMAT.L", "SVT.L", "IAG.L"
        ],
        "Japan": [
            "8031.T", "8058.T", "6301.T", "8001.T", "8002.T", "5401.T", "7011.T", "6367.T",
            "6326.T", "6594.T", "7012.T", "7013.T", "9101.T", "9104.T"
        ],
        "Europe": [
            "TTE.PA", "SU.PA", "ENEL.MI", "IBE.MC", "DG.PA", "SAF.PA", "ENI.MI", "EQNR.OL",
            "VOW3.DE", "STMPA.PA", "ASM.AS", "MT.AS", "LHA.DE", "ADP.PA"
        ],
        "South Korea": [
            "373220.KS", "096770.KS", "034020.KS", "329180.KS", "011200.KS", "028670.KS"
        ]
    },
    "Real Estate": {
        "US": ["PLD", "AMT", "EQIX", "CCI", "PSA", "O", "SPG", "WELL", "DLR", "VICI"],
        "Germany": ["VNA.DE", "LEG.DE", "TEG.DE", "GYC.DE"],
        "UK": ["LAND.L", "BLND.L", "SGRO.L", "UTG.L"],
        "Japan": ["8801.T", "8802.T", "3289.T", "8830.T"],
        "Europe": ["URW.PA", "VNA.DE", "LEG.DE", "PSPN.SW"],
        "South Korea": ["395400.KS", "365550.KS", "330590.KS", "293940.KS"]
    },
    "Utilities": {
        "US": ["NEE", "DUK", "SO", "AEP", "SRE", "D", "PEG", "ED"],
        "Germany": ["EOAN.DE", "RWE.DE", "ENR.DE"],
        "UK": ["NG.L", "SSE.L", "UU.L", "SVT.L"],
        "Japan": ["9503.T", "9501.T", "9502.T", "9531.T"],
        "Europe": ["IBE.MC", "ENEL.MI", "ENGI.PA", "ORSTED.CO"],
        "South Korea": ["015760.KS", "036460.KS", "017390.KS"]
    },
    "Telecom & Media": {
        "US": ["T", "VZ", "TMUS", "CMCSA", "CHTR", "NFLX", "DIS"],
        "Germany": ["DTE.DE", "1U1.DE"],
        "UK": ["VOD.L", "BT-A.L", "WPP.L"],
        "Japan": ["9432.T", "9433.T", "9984.T", "9434.T"],
        "Europe": ["ORA.PA", "TEF.MC", "KPN.AS", "LBTYA"],
        "South Korea": ["017670.KS", "030200.KS", "032640.KS", "035760.KQ", "352820.KS"]
    },
    "Materials": {
        "US": ["LIN", "SHW", "FCX", "NEM", "DOW", "CTVA", "DD"],
        "Germany": ["BAS.DE", "BAYN.DE", "HEI.DE", "SY1.DE", "KWS.DE"],
        "UK": ["RIO.L", "GLEN.L", "AAL.L", "CRDA.L", "JMAT.L"],
        "Japan": ["5401.T", "4063.T", "3407.T", "5713.T"],
        "Europe": ["AI.PA", "BAS.DE", "UPM.HE", "DSFIR.AS", "AKE.PA"],
        "South Korea": ["005490.KS", "051910.KS", "010130.KS", "011170.KS", "004020.KS"]
    }
}

START_DATE = "2020-01-01"
END_DATE = "2024-01-01"
APP_TITLE = "Advisor Bot"
APP_ICON = ""
REGIONS = ["US", "Germany", "UK", "Japan", "Europe", "South Korea"]
SECTORS = list(SECTOR_UNIVERSE.keys())
DATA_FILE = "market_data.csv"
