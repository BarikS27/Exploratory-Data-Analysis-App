import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Summary & Visualization App", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: #1E90FF;'>Data Summary & Visualization App</h1>
    <p style='text-align: center; color: #FFFFFF;'>Quickly Gain Key Insights</p>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Please Upload a CSV File With Numeric Data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="cp1252")

    st.markdown("### Preview of Data")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        st.error("This dataset has no numeric columns, so summary statistics and plots cannot be generated.")
    else:
        plot_column = st.selectbox("Please Select a Numeric Column to Plot", numeric_cols)
        plot_type = st.selectbox("Select Plot Type", ["Histogram", "KDE Plot", "Scatter Plot"])

        st.markdown("### Summary Statistics")
        st.dataframe(df[numeric_cols].describe())

        if plot_type == "Scatter Plot":
            if len(numeric_cols) < 2:
                st.error("Scatter plots require at least two numeric columns.")
            else:
                scatter_y = st.selectbox(
                    "Select a Second Numeric Column",
                    [col for col in numeric_cols if col != plot_column]
                )
                st.markdown(f"### Scatter Plot: {plot_column} vs {scatter_y}")
                fig, ax = plt.subplots()
                sns.set_style("whitegrid")
                sns.scatterplot(x=df[plot_column], y=df[scatter_y], ax=ax, color="#3498DB")
                st.pyplot(fig)

        else:
            st.markdown(f"### {plot_type} of {plot_column}")
            fig, ax = plt.subplots()
            sns.set_style("whitegrid")

            if plot_type == "Histogram":
                sns.histplot(df[plot_column], kde=True, ax=ax, color="#3498DB")
            else:
                sns.kdeplot(df[plot_column], fill=True, ax=ax, color="#3498DB")

            st.pyplot(fig)