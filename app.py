import streamlit as st
import pandas as pd
import json
from io import BytesIO
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Border, Side

# Define allowed fields with aliases
allowed_fields = {
    "(AOP001)Fixed assets": ["Fixed assets"],
    "(AOP002)Intangible assets": ["I. Intangible assets", "Intangible assets", "Intangible fixed assets", "Total Intangible assets"],
    "(AOP004)Concessions,patents,licenses and similar rights and other intangible assets":["Concessions,industrial rights,licences","Concessions, patents, licenses, trade marks etc.", "Service marks,software and other intangible assets","Concessions,patents,licenses and similar rights and other intangible assets","Concessions, patents, licenses, trademarks, service marks, software and other intangible assets"],
    "(AOP005)Goodwill":["Goodwill"],
    "(AOP006)Advances for intangible assets and intangible assets in preparation":["Advances for intangible assets and intangible assets in preparation"],
    "(AOP008)Other intangible fixed assets":["Other intangible fixed assets"],
    "(AOP009)Tangible fixed assets": ["II. Tangible assets","Tangible fixed assets", "Total tangible assets" , "Property,plants, equipment and biological assets", "Immovables,plants and equipment","Immovables, plants and equipment"],
    "(AOP010)Land and buildings":["Land and buildings"],
    "(AOP011)Land":["Land"],
    "(AOP012)Buildings":["Buildings"],
    "(AOP013)Machinery and equipment": ["Machinery and equipment", "Plant and Machinery", "Technical equipment and machinery", "Property,plant and equipment","Plant and equipment"],
    "(AOP014)Other equipment, furniture, fittings, tools, fixtures, vehicles": ["Other equipment, furniture, fittings, tools, fixtures, vehicles"],
    "(AOP016)Biological property":["Biological property"],
    "(AOP017)Advance payments for tangible assets": ["Advance payments for tangible assets", "Advences in property,plant,equipment and biological assets and property,biological asset in preparation"],
    "(AOP018)Tangible assets in progress": ["Tangible assets in progress", "Payments and fixed goods under construction","Immovables, plant  and equipment under construction"],
    "(AOP019)Other tangible assets": ["Other tangible assets","Other tangible fixed assets", "Other equipment" ,"Other Immovables,plants and equipment","Other immovables, plant and equipment and investment in third-party immovables, plant and equipment"],
    "(AOP020)Investments in real estate": ["Investments in real estate"],
    "(AOP021)Financial fixed assets": ["Financial fixed assets", "Long term investments","Long term financial investments and long term receivables Financial fixed assets","LONG-TERM FINANCIAL INVESTMENTS AND LONG-TERM RECEIVABLES"],
    "(AOP024)Loans to Group":["Loans to Group"],
    "(AOP025)Long term loans":["Long term loans"],
    "(AOP031)Long-term receivables": ["Long-term receivables", "Other long term investments and receivables"],
    "(AOP035)Deferred tax assets": ["DEFERRED TAX ASSETS", "Deferred tax assets"],
    "(AOP030)Other financial fixed assets":["Other financial fixed assets"],
    "(AOP034)Other long term receivables":["Other long term receivables","Other long-term receivables"],
    "(AOP036)Short-term assets": ["Short term assets", "Current assets", "Total Current assets", "Short term assets"],
    "(AOP037)Inventory": ["Inventory", "Total inventories", "Inventories"],
    "(AOP038)Raw materials, consumabeles and supplies":["Raw materials, consumabeles and supplies", "Inventory-raw materials, consumabeles and supplies","Inventory - raw materials, consumables, working inventory", "Inventory of materials(fabrication material, spare parts)"],
    "(AOP039)Inventory of materials":["Inventory of materials(fabricationmaterial, spare parts)"],
    "(AOP040)Work in progress":["Work in progress"],
    "(AOP041)Finished products and goods":["Finished products and goods", "Finished products/merchandise", "Finished goods", "Goods"],
    "(AOP042)Traiding Goods":["Traiding Goods","Inventory-Trading Goods","Inventory - Trading Goods"],
    "(AOP048)Prepayments":["Prepayments","Payments in advance for stock"],
    "(AOP045)Short-term receivables": ["Short-term receivables", "SHORT-TERM RECEIVABLES", "Total receivables", "Receivables", "Receivables and other assets"],
    "(AOP046)Short-term intercompany receivables": ["Short-term intercompany receivables", "Receivables from parent companies and subsidiaries", "Receivables from affiliated companies", "Intercompany Receivables","Receivables from foreign parent companies, subsidiaries and other associated companies"],
    "(AOP047)Short-term trade receivables": ["Short-term trade receivables", "Receivables from buyer", "Trade debtor" , "Trade receivables"],
    "(AOP050)Short-term receivables from employees": ["Short-term receivables from employees"],
    "(AOP049)Receivables from the state and other institutions": ["Prepaid corporate income tax","Receivables from the state and other institutions"],
    "(AOP051)Other short-term receivables": ["Other short-term receivables","Other short term receivables", "Other receivables", "Miscellaneous receivables"],
    "(AOP052)Short-term financial assets": ["SHORT TERM FINANCIAL ASSETS","short-term financial assets", "Financial investment", "Short term financial assets"],
    "(AOP058)Other short-term financial investments":["other short-term financial investments","Other short term financial assets"],
    "(AOP059_060)Cash": ["Cash","Cash and cash equivalents", "Cash assets", "Bank balance cheques and cash on hand", "Cash and cash equivalent", "Cash"],
    "(AOP062)Prepaid expenses": ["Prepaid expenses"],
    "(AOP063)Total assets": ["TOTAL ASSETS", "Total assets", "Balance sheet total"],
    "(AOP064)Off balance sheet items": ["Off balance sheet items"],
    "(AOP065)Equity capital": ["Equity capital", "Owners equity"],
    "(AOP066)Subscribed and paid capital": ["Subscribed and paid capital", "Basic capital", "Shareholders equity","Called capital", "Share capital", "Called and share capital","Subscribed capital"],
    "(AOP067)Emission premium":["Emission premium","Share premium"],
    "(AOP068)Own shares":["Own shares","Called up share capital","Called up share capital (issued capital stock)"],
    "(AOP069)Subscribed unpaid capital":["Subscribed unpaid capital","Unpaid issued capital"],
    "(AOP071)Capital reserves": ["CAPITAL RESERVES", "Capital reserves", "Reserves", "Revenue"],
    "(AOP070)Revaluation reserves": ["Revaluation reserves","POSITIVE REVALUATION RESERVES AND UNREALIZED PROFIT FROM FINANCIAL ASSETS AND OTHER ELEMENTS OF OTHER COMPREHENSIVE INCOME"],
    "(AOP072)Legal reserves":["Legal reserves"],
    "(AOP074)Other reserves":["Other reserves"],
    "(AOP075+/AOP076-)Profit or loss carried forward": ["Profit or loss carried forward","Retained profit (earnings) of the year (net profits)","Accumulated retained earnings from previous periods","Retained profit", "Retained earnings brought forward", "Net retained profit/net acumalted loss", "Net profit or loss from previos years"],
    "(AOP077+/AOP078-)Net profit or loss for the year": ["Net profit or loss for the year","Current period profit", "Loss from previos years", "Net profit for the period" , "Profit of the year","Net profit or loss for the year", "Net profit for the period"],
    "(AOP081)Liabilities": ["Liabilities", "Total liabilities","Total debt"],
    "(AOP082)Provision for risks and charges":["Provision for risks and charges"],
    "(AOP083)Provisions for pensions and similar obligations":["Provisions for pensions and similar obligations"],
    "(AOP084)Other provisions":["Other provisions"],
    "(AOP085)Long-term liabilities": ["Long-term liabilities", "Long term liabilities", "Total Long term liabilities"],
    "(AOP086)Long-term liabilities to affiliates": ["Long-term liabilities to affiliates", "Group payables due after 1 year", "Long term liabilities to affiliates"],
    "(AOP087)Trade liabilities":["Trade liabilities"],
    "(AOP090)Long-term liabilities for loans": ["Long-term liabilities for loans", "Long term liabilities to financial institutions","Long term creditis", "loans and lizing liabilities","Long term loans","Bank liabilites due after 1 year","Long term financial liabilities","Long term liabilities to credit institutions"],
    "(AOP092)Other loans/finance due after 1 year":["Other loans/finance due after 1 year"],
    "(AOP093)Other long-term liabilities": ["Other long-term liabilities", "Other long term liabilities"],
    "(AOP095)Short-term liabilities": ["Short-term liabilities","IV. SHORT-TERM LIABILITIES","Short- term liabilities","Short term liabilities","SHORT- TERM LIABILITIES", "TOTAL CURRENT LIABILITIES", "Total current liabilities","Short- term liabilities and short term provisions"," Short- term financial and operating liabilities"],
    "(AOP096)Short-term liabilities to affiliates": ["Short-term liabilities to affiliates","Liabilities of disposal groups", " Trade payables-foreing parent company, subsidiares and other associated companies", " Liabilities to affiliated companies","Group payables"],
    "(AOP098)Prepayments, deposits and gurantee":["Prepayments, deposits and gurantee","Liabilities for securities","Prepayments, deposits and guarantees"],
    "(AOP103)Liabilities for loans, deposits, etc. to companies within the group": ["Liabilities for loans, deposits, etc. to companies within the group"],
    "(AOP097)Short-term trade creditors": ["Short-term trade creditors", "Liabilities to suppliers","Trade Payables","Trade creditors(acounts payable)", " Trade payables"],
    "(AOP100)Short-term liabilities to employees": ["Short-term liabilities to employees","Liabilities towards employees"],
    "(AOP099)Short-term liabilities for taxes, contributions and other fees": ["Short-term liabilities for taxes, contributions and other fees"],
    "(AOP101)Liability for income tax":["Liability for income tax","S-term Liabilities for tax,contributions and other fees"],
    "(AOP104)Obligations for taken loans and credits":["Obligations for taken loans and credits","Short Term Bank Debt","Short liabilities for loans","Short term loans","Short term financial liabilities","Obligation for taken loans","BANK LOANS AND OVERDRAFT","Liabilities to bank","Loans liabilities from credit institutions","Short-term liabilities for loans","Short-term financial liabilities"],
    "(AOP108)Other short-term liabilities": ["Other short term liabilities", "Other operating and liabilities and other short term liabilities", "Other short-term liabilities ",  "Other  liabilities  including accruals",  "Other  liabilities"],
    "(AOP109)Accruals and deferred income": ["Accruals and deferred income"],
    "(AOP111)Total liabilities and funds": ["Total liabilities and funds", "TOTAL EQUITY AND LIABILITIES "," TOTAL LIABILITIES","BALANCE SHEET TOTAL"],
    "(AOP112)Off balance sheet items": ["Off balance sheet items"],
    "(AOP201)Turnover, sales revenue": ["Turnover, sales revenue","Revenues from contracts with customers","Operating income"],
    "(AOP202)Revenues from sales": ["Revenues from sales","Income from sales","Income from sales (outside group)","Income from goods sold"],
    "(AOP203)Other income(other revenues)": ["Other income(other revenues)","Other operating income (outside the group)","Other operating income","OTHER OPERATING REVENUE"],
    "(AOP206)Own work capitalized": ["Own work capitalized"],
    "(AOP207)Operating expenses": ["Operating expenses"],
    "(AOP208)Material costs": ["Material costs","Cost of raw materials and consumables","RAW MATERIAL COSTS, FUEL AND ENERGY COSTS"],
    "(AOP209)Cost of goods sold": ["Cost of goods sold"],
    "(AOP213)Staff costs": ["Staff costs (employee costs)"],
    "(AOP218)Depreciation on fixed assets": ["Depreciation on fixed assets","Depreciation"],
    "(AOP222)Other operating expenses": ["Other operating expenses","Other expenses"],
    "(AOP223)Income from financial transactions": ["Income from financial transactions (financial income)","III. FINANCIAL INCOME"],
    "(AOP234)Financial costs": ["Financial costs"],
    "(AOP250+/AOP251-)Profit or loss before taxation": ["Profit or loss before taxation","Profit before taxation","Loss before taxation"],
    "(AOP252)Profit tax": ["Profit tax","Income tax"],
    "(AOP255+/AOP256-)Profit or loss after taxation": ["Profit or loss after taxation","Profit after taxation","Loss after taxation","TOTAL RESULT"],
}
# ------------------------------
# Streamlit page config
# ------------------------------
st.set_page_config(page_title="Coface JSON", layout="wide")
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
st.title("Convert COFACE JSON fields to Excel")

uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

# ------------------------------
# Helper functions
# ------------------------------
def convert_date(value):
    value = str(value)
    if value.endswith("0000"):  # year only
        return value[:4]
    if len(value) == 8:  # full date YYYYMMDD -> DD.MM.YYYY
        return f"{value[6:8]}.{value[4:6]}.{value[:4]}"
    return value

def format_amount_list(lst):
    """Format amounts into German style, e.g. 102.261.587,00"""
    formatted = []
    for a in lst:
        if a is None:
            continue

        num = float(a)

        # First format as US: 102,261,587.00
        s = f"{num:,.2f}"

        # Convert to German: 102.261.587,00
        s = s.replace(",", "X")  # temporary placeholder
        s = s.replace(".", ",")  # decimal separator becomes comma
        s = s.replace("X", ".")  # thousands separators become dots

        formatted.append(s)

    return "; ".join(formatted)


def dedupe(seq):
    seen = set()
    result = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result

# Recursive extraction
def extract_values(obj, parent_dates=None, parent_amounts=None):
    if parent_dates is None:
        parent_dates = []
    if parent_amounts is None:
        parent_amounts = []

    if isinstance(obj, dict):
        current_dates = parent_dates.copy()
        current_amounts = parent_amounts.copy()

        if "date" in obj:
            current_dates.append(obj["date"])
        if "fromAmount" in obj:
            current_amounts.append(obj["fromAmount"])

        if "name" in obj and "value" in obj:
            name = str(obj["name"]).strip()
            value = obj.get("value")

            for field, aliases in allowed_fields.items():
                if any(name.lower() == alias.lower() for alias in aliases):

                    if extracted[field]["value"] is None and value is not None:
                        extracted[field]["value"] = value

                    extracted[field]["date"].extend(current_dates)
                    extracted[field]["fromAmount"].extend(current_amounts)
                    break

        for k, v in obj.items():
            extract_values(v, current_dates, current_amounts)

    elif isinstance(obj, list):
        for item in obj:
            extract_values(item, parent_dates, parent_amounts)


# ------------------------------
# Main processing
# ------------------------------
if uploaded_file:
    try:
        data = json.load(uploaded_file)

        extracted = {field: {"value": None, "date": [], "fromAmount": []} for field in allowed_fields}

        extract_values(data)

        for field in extracted:
            extracted[field]["date"] = dedupe(extracted[field]["date"])
            extracted[field]["fromAmount"] = dedupe(extracted[field]["fromAmount"])

        df = pd.DataFrame(
            [
                (
                    field,
                    extracted[field]["value"] if extracted[field]["value"] is not None else "",
                    "; ".join(convert_date(d) for d in extracted[field]["date"]),
                    format_amount_list(extracted[field]["fromAmount"]),
                )
                for field in allowed_fields
            ],
            columns=["Field", "Value", "Date", "FromAmount"]
        )

        st.dataframe(df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
            ws = writer.sheets["Sheet1"]

            for col in ws.columns:
                max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col)
                ws.column_dimensions[get_column_letter(col[0].column)].width = max_len + 4

            for cell in ws["A"]:
                cell.font = Font(bold=True)

            thin = Side(border_style="thin", color="000000")
            border = Border(left=thin, right=thin, top=thin, bottom=thin)
            for row in ws.iter_rows():
                for cell in row:
                    cell.border = border

        output.seek(0)
        st.download_button(
            label="📥 Download Excel",
            data=output,
            file_name="mapped_values.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        st.error(f"Error: {e}")
















































































