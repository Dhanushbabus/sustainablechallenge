import tempfile
import streamlit as st
temp_directory = tempfile.gettempdir()
print("Temporary directory:", temp_directory)
st.write (temp_directory)
