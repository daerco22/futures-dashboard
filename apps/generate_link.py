# %%
import streamlit as st
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module
from .now_time import file_time

# %% DOWNLOADS
def generate_excel_download_link(df, filename):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding='utf-8', index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}-{file_time}.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)


def generate_html_download_link(fig, filename):
    # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs='cdn')
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="{filename}-{file_time}.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)


# %%
if __name__ == '__main__':
    generate_excel_download_link()
    generate_html_download_link()
