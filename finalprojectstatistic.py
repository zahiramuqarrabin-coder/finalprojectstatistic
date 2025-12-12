import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Survey Data Analysis App",
    layout="wide",
)

# ---------------------------
# CUSTOM THEME (TEXT COLORS & LIGHTER INPUT BOX)
# ---------------------------
custom_css = """
<style>
/* Main titles */
h1, h2, h3, h4 {
    color: #ff79b0 !important;   /* pink pastel */
    font-weight: 700;
}

/* General text */
body, p, label, span {
    color: #eaeaea !important;
}

/* Sidebar text */
.sidebar .sidebar-content h2, .sidebar .sidebar-content h3 {
    color: #ff79b0 !important;
}

/* Input file uploader lighter */
[data-testid="stFileUploader"] > div {
    background-color: #2f2f2f !important; 
    border: 1px solid #ff79b0 !important;
    border-radius: 12px !important;
}

/* Buttons */
.stButton>button {
    color: white !important;
    background-color: #ff79b0 !important;
    border-radius: 12px;
    padding: 8px 20px;
}

/* Improve selectbox & radio visibility */
.stSelectbox, .stRadio {
    color: #ffffff !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------
# SIDEBAR - ABOUT CREATOR
# ---------------------------
st.sidebar.title("About The Creator")
st.sidebar.write("**IG:** @ziramqn")
st.sidebar.write("**Email:** zahira.muqarrabin@student.president.ac.id")

# ---------------------------
# MAIN TITLE
# ---------------------------
st.title("Survey Data Analysis App")
st.write("Upload your Excel survey data and run descriptive or association analysis.")

# ---------------------------
# FILE UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Data Preview")
    st.dataframe(df)

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) == 0:
        st.error("No numeric columns found in the dataset.")
    else:
        st.success("Numeric columns detected: " + ", ".join(numeric_cols))

        # ---------------------------
        # DESCRIPTIVE ANALYSIS
        # ---------------------------
        st.header("Descriptive Statistics")

        col = st.selectbox("Choose variable:", numeric_cols)

        if col:
            st.write("### Summary Statistics")
            st.write(df[col].describe())

            st.write("### Histogram")
            st.bar_chart(df[col])

        # ---------------------------
        # ASSOCIATION ANALYSIS
        # ---------------------------
        st.header("Association Analysis (Two Numeric Variables)")

        col1 = st.selectbox("Variable 1:", numeric_cols, key="var1")
        col2 = st.selectbox("Variable 2:", numeric_cols, key="var2")

        method = st.radio(
            "Choose correlation method:",
            ["Pearson", "Spearman"],
            horizontal=True
        )

        if col1 and col2:
            if method == "Pearson":
                corr, p_value = stats.pearsonr(df[col1], df[col2])
            else:
                corr, p_value = stats.spearmanr(df[col1], df[col2])

            st.write(f"### {method} Correlation Result")
            st.write(f"**Correlation Coefficient:** {corr:.4f}")
            st.write(f"**P-value:** {p_value:.4f}")

            if p_value < 0.05:
                st.success("There is a significant relationship between the two variables.")
            else:
                st.info("There is no significant relationship between the two variables.")
else:
    st.info("Please upload an Excel (.xlsx) file to start analysis.")
