import streamlit as st
import pandas as pd
import json
from io import BytesIO
from openpyxl.utils import get_column_letter

# Define allowed fields with aliases
allowed_fields = {
    "(AOP001)Fixed assets": ["Fixed assets"],
    "(AOP002)Intangible assets": ["I. Intangible assets", "Intangible assets", "Intangible fixed assets", "Total Intangible assets"],
    "(AOP004)Concessions,patents,licenses and similar rights and other intangible assets":["Concessions,industrial rights,licences"," Concessions,patents,licences,trademarks, service marks,software and ather intangible assets","Concessions,patents,licenses  and similar rights and other intangible assets"],
    "(AOP005)Goodwill":["Goodwill"],
    "(AOP006)Advances for intangible assets and intangible assets in preparation":["Advances for intangible assets and intangible assets in preparation"],
    "(AOP008)Other intangible fixed assets":["Other intangible fixed assets"],
    "(AOP009)Tangible fixed assets": ["II. Tangible assets","Tangible fixed assets", "Total tangible assets" , "Property,plants, equipment and biological assets", "Immovables,plants and equipment"],
    "(AOP010)Land and buildings":["Land and buildings"],
    "(AOP011)Land":["Land"],
    "(AOP012)Buildings":["Buildings"],
    "(AOP013)Machinery and equipment": ["Machinery and equipment", "Plant and Machinery", "Technical equipment and machinery", "Property,plant and equipment"],
    "(AOP014)Other equipment, furniture, fittings, tools, fixtures, vehicles": ["Other equipment, furniture, fittings, tools, fixtures, vehicles"],
    "(AOP016)Biological property":["Biological property"],
    "(AOP017)Advance payments for tangible assets": ["Advance payments for tangible assets", "Advences in property,plant,equipment and biological assets and property,biological asset in preparation"],
    "(AOP018)Tangible assets in progress": ["Tangible assets in progress", "Payments and fixed goods under construction"],
    "(AOP019)Other tangible assets": ["Other tangible assets","Other tangible fixed assets", "Other equipment" ,"Other Immovables,plants and equipment"],
    "(AOP020)Investments in real estate": ["Investments in real estate"],
    "(AOP021)Financial fixed assets": ["Financial fixed assets", "Long term investments","Long term financial investments and long term receivables Financial fixed assets"],
    "(AOP024)Loans to Group":["Loans to Group"],
    "(AOP025)Long term loans":["Long term loans"],
    "(AOP031)Long-term receivables": ["Long term receivables", "Other long term investments and receivables"],
    "(AOP035)Deferred tax assets": ["DEFERRED TAX ASSETS", "Deferred tax assets"],
    "(AOP030)Other financial fixed assets":["Other financial fixed assets"],
    "(AOP034)Other long term receivables":["Other long term receivables"],
    "(AOP036)Short-term assets": ["Short term assets", "Current assets", "Total Current assets", "Short term assets"],
    "(AOP037)Inventory": ["Inventory", "Total inventories", "Inventories"],
    "(AOP038)Raw materials, consumabeles and supplies":["Raw materials, consumabeles and supplies", "Inventory-raw materials, consumabeles and supplies", "Inventory of materials(fabrication material, spare parts)"],
    "(AOP039)Inventory of materials":["Inventory of materials(fabricationmaterial, spare parts)"],
    "(AOP040)Work in progress":["Work in progress"],
    "(AOP041)Finished products and goods":["Finished products and goods", "Finished products/merchandise", "Finished goods", "Goods"],
    "(AOP042)Traiding Goods":["Traiding Goods","Inventory-Trading Goods"],
    "(AOP048)Prepayments":["Prepayments"],
    "(AOP045)Short-term receivables": ["Short-term receivables", "SHORT-TERM RECEIVABLES", "Total receivables", "Receivables", "Receivables and other assets"],
    "(AOP046)Short-term intercompany receivables": ["Short-term intercompany receivables", "Receivables from parent companies and subsidiaries", "Receivables from affiliated companies", "Intercompany Receivables"],
    "(AOP047)Short-term trade receivables": ["Short-term trade receivables", "Receivables from buyer", "Trade debtor" , "Trade receivables"],
    "(AOP050)Short-term receivables from employees": ["Short-term receivables from employees"],
    "(AOP049)Receivables from the state and other institutions": ["Prepaid corporate income tax","Receivables from the state and other institutions"],
    "(AOP051)Other short-term receivables": ["Other short-term receivables","Other short term receivables", "Other receivables", "Miscellaneous receivables"],
    "(AOP052)Short-term financial assets": ["SHORT TERM FINANCIAL ASSETS","short-term financial assets", "Financial investment", "Short term financial assets"],
    "(AOP058)Other short-term financial investments":["other short-term financial investments"],
    "(AOP059_060)Cash": ["Cash","Cash and cash equivalents", "Cash assets", "Bank balance cheques and cash on hand", "Cash and cash equivalent", "Cash"],
    "(AOP062)Prepaid expenses": ["Prepaid expenses"],
    "(AOP063)Total assets": ["TOTAL ASSETS", "Total assets", "Balance sheet total"],
    "(AOP064)Off balance sheet items": ["Off balance sheet items"],
    "(AOP065)Equity capital": ["Equity capital", "Owners equity"],
    "(AOP066)Subscribed and paid capital": ["Subscribed and paid capital", "Basic capital", "Shareholders equity","Called capital", "Share capital", "Called and share capital"],
    "(AOP067)Emission premium":["Emission premium","Share premium"],
    "(AOP068)Own shares":["Own shares","Called up share capital"],
    "(AOP069)Subscribed unpaid capital":["Subscribed unpaid capital","Unpaid issued capital"],
    "(AOP071)Capital reserves": ["CAPITAL RESERVES", "Capital reserves", "Reserves", "Revenue"],
    "(AOP070)Revaluation reserves": ["Revaluation reserves"],
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
    "(AOP098)Prepayments, deposits and gurantee":["Prepayments, deposits and gurantee","Liabilities for securities"],
    "(AOP103)Liabilities for loans, deposits, etc. to companies within the group": ["Liabilities for loans, deposits, etc. to companies within the group"],
    "(AOP097)Short-term trade creditors": ["Short-term trade creditors", "Liabilities to suppliers","Trade Payables","Trade creditors(acounts payable)", " Trade payables"],
    "(AOP100)Short-term liabilities to employees": ["Short-term liabilities to employees","Liabilities towards employees"],
    "(AOP099)Short-term liabilities for taxes, contributions and other fees": ["Short-term liabilities for taxes, contributions and other fees"],
    "(AOP101)Liability for income tax":["Liability for income tax","S-term Liabilities for tax,contributions and other fees"],
    "(AOP104)Obligations for taken loans and credits":["Obligations for taken loans and credits","Short Term Bank Debt","Short liabilities for loans","Short term loans","Short term financial liabilities","Obligation for taken loans","BANK LOANS AND OVERDRAFT","Liabilities to bank","Loans liabilities from credit institutions"],
    "(AOP108)Other short-term liabilities": ["Other short term liabilities", "Other operating and liabilities and other short term liabilities", "Other short-term liabilities ",  "Other  liabilities  including accruals",  "Other  liabilities"],
    "(AOP109)Accruals and deferred income": ["Accruals and deferred income"],
    "(AOP111)Total liabilities and funds": ["Total liabilities and funds", "TOTAL EQUITY AND LIABILITIES "," TOTAL LIABILITIES","BALANCE SHEET TOTAL"],
    "(AOP112)Off balance sheet items": ["Off balance sheet items"],
    "(AOP201)Turnover, sales revenue": ["Turnover, sales revenue","Revenues from contracts with customers"],
    "(AOP202)Revenues from sales": ["Revenues from sales"],
    "(AOP203)Other income(other revenues)": ["Other income(other revenues)"],
    "(AOP206)Own work capitalized": ["Own work capitalized"],
    "(AOP207)Operating expenses": ["Operating expenses"],
    "(AOP208)Material costs": ["Material costs","Cost of raw materials and consumables"],
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
# Streamlit page config
st.set_page_config(
    page_title="Coface JSON",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# Hide Streamlit branding
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.viewerBadge_link__qRIco {display: none !important;}
.stAppDeployButton {display: none !important;}
.stDeployButton {display: none !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom footer
custom_footer = """
<div style="position: fixed; bottom: 0; width: 100%; 
            background-color: #f5f5f5; padding: 10px; 
            text-align: center; font-size: 14px; color: #444;">
    Created by Gorgi Kokinovski  
</div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)

st.title("Convert COFACE JSON fields to Excel")

uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

if uploaded_file:
    try:
        data = json.load(uploaded_file)

        # Initialize extracted dictionary
        extracted = {field: "" for field in allowed_fields}
        found_names = []

        def extract_values(obj):
            """Recursively search for 'name' and 'value' in JSON"""
            if isinstance(obj, dict):
                if "name" in obj and "value" in obj:
                    name = str(obj["name"]).strip()
                    value = obj["value"]
                    found_names.append(name)

                    # Match against aliases
                    for field, aliases in allowed_fields.items():
                        if extracted[field] == "" and any(
                            name.lower() == alias.lower() for alias in aliases
                        ):
                            extracted[field] = value
                            break

                for v in obj.values():
                    extract_values(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract_values(item)

        extract_values(data)

        df = pd.DataFrame([extracted])
        st.dataframe(df)

        # Save to Excel with auto-adjusted columns
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
            ws = writer.sheets["Sheet1"]

            for col in ws.columns:
                max_length = 0
                column_letter = get_column_letter(col[0].column)
                for cell in col:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                ws.column_dimensions[column_letter].width = max_length + 2

        output.seek(0)
        st.download_button(
            label="📥 Download Excel",
            data=output,
            file_name="mapped_values.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        st.error(f"Error: {e}")



















































