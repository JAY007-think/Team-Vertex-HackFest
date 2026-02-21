import streamlit as st
import pandas as pd

st.success("Badhai ho! Aapka setup sahi se kaam kar raha hai.")
st.write("Ye dekhiye ek sample table:")
df = pd.DataFrame({'Col1': [1, 2], 'Col2': [3, 4]})
st.table(df)