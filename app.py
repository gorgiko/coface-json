import streamlit as st
import pandas as pd
import json
from io import BytesIO
#from openpyxl.utils import get_column_letter

# ✅ Define allowed fields with aliases
allowed_fields = {
    "(AOP001)Fixed assets": ["Fixed assets"],
    "(AOP002)Intangible assets": ["I. Intangible assets", "Intangible assets"],
    "(AOP009)Tangible fixed assets": ["II. Tangible assets","Tangible fixed assets"],
    "(AOP013)Machinery and equipment": ["Machinery and equipment"],
    "(AOP014)Other equipment, furniture, fittings, tools, fixtures, vehicles": [
        "Other equipment, furniture, fittings, tools, fixtures, vehicles"
    ],
    "(AOP017)Advance payments for tangible assets": ["Advance payments for tangible assets"],
    "(AOP018)Tangible assets in progress": ["Tangible assets in progress"],
    "(AOP019)Other tangible assets": ["Other tangible assets"],
    "(AOP020)Investments in real estate": ["Investments in real estate"],
    "(AOP021)Financial fixed assets": ["Financial fixed assets"],
    "(AOP031)Long-term receivables": ["Long-term receivables"],
    "(AOP035)Deferred tax assets": ["DEFERRED TAX ASSETS", "Deferred tax assets"],
    "(AOP036)Short-term assets": ["Short term assets"],
    "(AOP037)Inventory": ["Inventory"],
    "(AOP045)Short-term receivables": ["Short-term receivables", "SHORT-TERM RECEIVABLES"],
    "(AOP046)Short-term intercompany receivables": ["Short-term intercompany receivables"],
    "(AOP047)Short-term trade receivables": ["Short-term trade receivables"],
    "(AOP050)Short-term receivables from employees": ["Short-term receivables from employees"],
    "(AOP049)Receivables from the state and other institutions": [
        "Receivables from the state and other institutions"
    ],
    "(AOP051)Other short-term receivables": ["Other short-term receivables","Other short term receivables"],
    "(AOP052)Short-term financial assets": [
        "SHORT TERM FINANCIAL ASSETS",
        "short-term financial assets",
    ],
    "(AOP059_060)Cash": ["Cash","Cash and cash equivalents"],
    "(AOP062)Prepaid expenses": ["Prepaid expenses"],
    "(AOP063)Total assets": ["TOTAL ASSETS", "Total assets"],
    "(AOP064)Off balance sheet items": ["Off balance sheet items"],
    "(AOP065)Equity capital": ["Equity capital"],
    "(AOP066)Subscribed and paid capital": ["Subscribed and paid capital"],
    "(AOP071)Capital reserves": ["CAPITAL RESERVES", "Capital reserves"],
    "(AOP070)Revaluation reserves": ["Revaluation reserves"],
    "(AOP075+/AOP076-)Profit or loss carried forward": ["Profit or loss carried forward"],
    "(AOP077+/AOP078-)Net profit or loss for the year": ["Net profit or loss for the year"],
    "(AOP081)Liabilities": ["Liabilities"],
    "(AOP085)Long-term liabilities": ["Long-term liabilities"],
    "(AOP086)Long-term liabilities to affiliates": ["Long-term liabilities to affiliates"],
    "(AOP090)Long-term liabilities for loans": ["Long-term liabilities for loans"],
    "(AOP093)Other long-term liabilities": ["Other long-term liabilities"],
    "(AOP095)Short-term liabilities": ["Short-term liabilities","IV. SHORT-TERM LIABILITIES"],
    "(AOP096)Short-term liabilities to affiliates": ["Short-term liabilities to affiliates"],
    "(AOP103)Liabilities for loans, deposits, etc. to companies within the group": [
        "Liabilities for loans, deposits, etc. to companies within the group"
    ],
    "(AOP097)Short-term trade creditors": ["Short-term trade creditors"],
    "(AOP100)Short-term liabilities to employees": ["Short-term liabilities to employees","Liabilities towards employees"],
    "(AOP099)Short-term liabilities for taxes, contributions and other fees": [
        "Short-term liabilities for taxes, contributions and other fees"
    ],
    "(AOP108)Other short-term liabilities": ["Other short term liabilities"],
    "(AOP109)Accruals and deferred income": ["Accruals and deferred income"],
    "(AOP111)Total liabilities and funds": ["Total liabilities and funds"],
    "(AOP112)Off balance sheet items": ["Off balance sheet items"],
    "(AOP201&AOP202)Turnover, sales revenue": ["Turnover, sales revenue"],
    "(AOP206)Own work capitalized": ["Own work capitalized"],
    "(AOP207)Operating expenses": ["Operating expenses"],
    "(AOP208)Material costs": ["Material costs"],
    "(AOP209)Cost of goods sold": ["Cost of goods sold"],
    "(AOP213)Staff costs": ["Staff costs (employee costs)"],
    "(AOP218)Depreciation on fixed assets": ["Depreciation on fixed assets"],
    "(AOP222)Other operating expenses": ["Other operating expenses"],
    "(AOP223)Income from financial transactions": [
        "Income from financial transactions (financial income)","III. FINANCIAL INCOME"
    ],
    "(AOP234)Financial costs": ["Financial costs"],
    "(AOP250+/AOP251-)Profit or loss before taxation": ["Profit or loss before taxation","Profit before taxation","Loss before taxation"],
    "(AOP252)Profit tax": ["Profit tax","Income tax"],
    "(AOP255+/AOP256-)Profit or loss after taxation": ["Profit or loss after taxation","Profit after taxation","Loss after taxation"],
}

# ✅ File uploader
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    # Read Excel file
    df = pd.read_excel(uploaded_file)

    # Normalize column names
    df.columns = df.columns.str.strip().str.replace("\n", " ")

    # ✅ Extract allowed fields
    extracted_data = {}
    for key, aliases in allowed_fields.items():
        found = False
        for alias in aliases:
            # Case-insensitive match
            match = df.columns[df.columns.str.contains(alias, case=False, regex=False)]
            if not match.empty:
                extracted_data[key] = df[match[0]].tolist()
                found = True
                break
        if not found:
            extracted_data[key] = None

    # ✅ Show results in Streamlit
    st.write("### Extracted Data")
    st.json(extracted_data)

    # ✅ Download extracted data as Excel
    output = BytesIO()
    pd.DataFrame([extracted_data]).to_excel(output, index=False, engine="openpyxl")
    st.download_button(
        "Download Extracted Data",
        data=output.getvalue(),
        file_name="extracted_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )



















