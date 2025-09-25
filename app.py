import streamlit as st
import pandas as pd
import json
from io import BytesIO

# ✅ Define allowed fields with aliases
allowed_fields = {
    "Fixed assets": ["Fixed assets"],
    "Intangible assets": ["I. Intangible assets", "Intangible assets"],
    "Tangible fixed assets": ["II. Tangible assets","Tangible fixed assets"],
    "Machinery and equipment": ["Machinery and equipment"],
    "Other equipment, furniture, fittings, tools, fixtures, vehicles": [
        "Other equipment, furniture, fittings, tools, fixtures, vehicles"
    ],
    "Advance payments for tangible assets": ["Advance payments for tangible assets"],
    "Tangible assets in progress": ["Tangible assets in progress"],
    "Other tangible assets": ["Other tangible assets"],
    "Investments in real estate": ["Investments in real estate"],
    "Financial fixed assets": ["Financial fixed assets"],
    "Long-term receivables": ["Long-term receivables"],
    "Deferred tax assets": ["DEFERRED TAX ASSETS", "Deferred tax assets"],
    "Short-term assets": ["Short term assets"],
    "Inventory": ["Inventory"],
    "Short-term receivables": ["Short-term receivables", "SHORT-TERM RECEIVABLES"],
    "Short-term intercompany receivables": ["Short-term intercompany receivables"],
    "Short-term trade receivables": ["Short-term trade receivables"],
    "Short-term receivables from employees": ["Short-term receivables from employees"],
    "Receivables from the state and other institutions": [
        "Receivables from the state and other institutions"
    ],
    "Other short-term receivables": ["Other short-term receivables","Other short term receivables"],
    "Short-term financial assets": [
        "SHORT TERM FINANCIAL ASSETS",
        "short-term financial assets",
    ],
    "Cash": ["Cash","Cash and cash equivalents"],
    "Prepaid expenses": ["Prepaid expenses"],
    "Total assets": ["TOTAL ASSETS", "Total assets"],
    "Off balance sheet items": ["Off balance sheet items"],
    "Equity capital": ["Equity capital"],
    "Subscribed and paid capital": ["Subscribed and paid capital"],
    "Capital reserves": ["CAPITAL RESERVES", "Capital reserves"],
    "Revaluation reserves": ["Revaluation reserves"],
    "Profit or loss carried forward": ["Profit or loss carried forward"],
    "Net profit or loss for the year": ["Net profit or loss for the year"],
    "Liabilities": ["Liabilities"],
    "Long-term liabilities": ["Long-term liabilities"],
    "Long-term liabilities to affiliates": ["Long-term liabilities to affiliates"],
    "Long-term liabilities for loans": ["Long-term liabilities for loans"],
    "Other long-term liabilities": ["Other long-term liabilities"],
    "Short-term liabilities": ["Short-term liabilities","IV. SHORT-TERM LIABILITIES"],
    "Short-term liabilities to affiliates": ["Short-term liabilities to affiliates"],
    "Liabilities for loans, deposits, etc. to companies within the group": [
        "Liabilities for loans, deposits, etc. to companies within the group"
    ],
    "Short-term trade creditors": ["Short-term trade creditors"],
    "Short-term liabilities to employees": ["Short-term liabilities to employees","Liabilities towards employees"],
    "Short-term liabilities for taxes, contributions and other fees": [
        "Short-term liabilities for taxes, contributions and other fees"
    ],
    "Other short-term liabilities": ["Other short term liabilities"],
    "Accruals and deferred income": ["Accruals and deferred income"],
    "Total liabilities and funds": ["Total liabilities and funds"],
    "Turnover, sales revenue": ["Turnover, sales revenue"],
    "Own work capitalized": ["Own work capitalized"],
    "Operating expenses": ["Operating expenses"],
    "Material costs": ["Material costs"],
    "Cost of goods sold": ["Cost of goods sold"],
    "Staff costs": ["Staff costs (employee costs)"],
    "Depreciation on fixed assets": ["Depreciation on fixed assets"],
    "Other operating expenses": ["Other operating expenses"],
    "Income from financial transactions": [
        "Income from financial transactions (financial income)","III. FINANCIAL INCOME"
    ],
    "Financial costs": ["Financial costs"],
    "Profit or loss before taxation": ["Profit or loss before taxation","Profit before taxation","Loss before taxation"],
    "Profit tax": ["Profit tax","Income tax"],
    "Profit or loss after taxation": ["Profit or loss after taxation","Profit after taxation","Loss after taxation"],
}
# Hide default Streamlit elements
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}        /* Hides hamburger menu */
    header {visibility: hidden;}           /* Hides GitHub repo link */
    footer {visibility: hidden;}           /* Hides footer */
    .stAppDeployButton {display: none;}    /* Hides 'Deploy' button if shown */
    .viewerBadge_link__qRIco {display: none !important;}  /* Hides 'Made with Streamlit' badge */
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Add your own footer
custom_footer = """
    <div style="position: fixed; bottom: 0; width: 100%; 
                background-color: #f5f5f5; padding: 10px; 
                text-align: center; font-size: 14px; color: #444;">
        🚀 Developed by <b>Gorgi Kokinovski</b>  
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)
st.title("Convert COFACE JSON fields to Excel")

uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

if uploaded_file:
    try:
        data = json.load(uploaded_file)

        # Initialize extracted dictionary with empty strings
        extracted = {field: "" for field in allowed_fields}
        found_names = []

        def extract_values(obj):
            """Recursively search for 'name' and 'value' in JSON"""
            if isinstance(obj, dict):
                if "name" in obj and "value" in obj:
                    name = str(obj["name"]).strip()
                    value = obj["value"]
                    found_names.append(name)

                    # ✅ Check against all aliases
                    for field, aliases in allowed_fields.items():
                        if extracted[field] == "" and any(
                            name.lower() == alias.lower() for alias in aliases
                        ):
                            extracted[field] = value
                            break  # stop after first match

                for v in obj.values():
                    extract_values(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract_values(item)

        extract_values(data)

        df = pd.DataFrame([extracted])
        st.dataframe(df)

        # Save to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        st.download_button(
            label="📥 Download Excel",
            data=output,
            file_name="mapped_values.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        st.error(f"Error: {e}")









