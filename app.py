import streamlit as st
import pandas as pd
import psycopg2

# Page config
st.set_page_config(page_title="AGR_CURAJ_Price_List", layout="wide")

# ---- HEADER SECTION ----
col1, col2 = st.columns([1, 5])

with col1:
    st.image("AGR_Logo_New.png", width=120)

with col2:
    st.markdown(
        """
        <h1 style='color:#2EA490; margin-bottom:0;'>AnuGenix Rasayan</h1>
        <p style='font-size:18px; margin-top:2px; color:gray; font-style:italic;'>
        Creating Bonds Beyond Molecules
        </p>
        <h3 style='margin-top:5px;'>CURAJ Price List 2026</h3>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ---- SEARCH SECTION ----
st.subheader("🔍 Search CAS Number for Prices")

# DB connection
conn = psycopg2.connect(st.secrets["DB_URL"])

# Input
user_input = st.text_area("Enter CAS Number (one per line)")

if st.button("Search"):

    cas_list = [c.strip() for c in user_input.split("\n") if c.strip()]

    if len(cas_list) == 0:
        st.warning("Please enter CAS numbers")

    else:
        query = """
        SELECT "CAS_No", "Chemical_Name", "Purity", "Size", "Price"
        FROM price_list
        WHERE "CAS_No" = ANY(%s)
        """

        df = pd.read_sql(query, conn, params=(cas_list,))

        df.index = df.index + 1

        st.success(f"{len(df)} results found")

        st.dataframe(df, use_container_width=True)
