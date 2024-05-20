import os
import streamlit as st

def list_files_in_box_folder():
    # Get the path of the user's directory
    user_dir = os.path.expanduser("~")

    # Assuming "box" is a subfolder within the user's directory
    box_folder = os.path.join(user_dir, "box")

    # List all files and directories in the "box" folder
    contents = os.listdir(box_folder)

    return contents

def main():
    st.title("List Files in 'box' Folder")

    # List files and folders
    contents = list_files_in_box_folder()

    if contents:
        st.write("Contents of the 'box' folder:")
        for item in contents:
            st.write(item)
    else:
        st.write("The 'box' folder is empty.")

if __name__ == "__main__":
    main()
