import os
import streamlit as st
# Get the path of the user's directory
user_dir = os.path.expanduser("~")

# Assuming "box" is a subfolder within the user's directory
box_folder = os.path.join(user_dir, "box")

# Print the full path of the "box" folder
print("Full path of the 'box' folder:", box_folder)
st.write (box_folder)
