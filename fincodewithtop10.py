import os
import platform
import streamlit as st

# Set the page configuration with the browser tab name
st.set_page_config(page_title="Directory Size", page_icon="📁")

def get_temp_dir_path():
    """Returns the temporary directory path based on the operating system."""
    try:
        if platform.system() == "Windows":
            return os.getenv('TEMP')
        elif platform.system() == "Darwin":  # macOS
            return '/tmp'
        else:
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_folder_size(folder_path):
    """Returns the size of a folder in bytes."""
    try:
        total_size = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                total_size += os.path.getsize(os.path.join(root, file))
        return total_size
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_top_10_folders(root_folder_path):
    """Returns a list of the top 10 folders that consume the most memory under the given root folder path."""
    try:
        folder_sizes = {}
        for folder in os.listdir(root_folder_path):
            folder_path = os.path.join(root_folder_path, folder)
            if os.path.isdir(folder_path):
                folder_size = get_folder_size(folder_path)
                if folder_size is not None:
                    folder_sizes[folder] = folder_size

        sorted_folder_sizes = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)
        return sorted_folder_sizes[:10]
    except Exception as e:
        st.error(f"Error: {e}")
        return []

def delete_files_in_temp_folder(temp_dir_path):
    """Deletes all files and folders in the temporary directory."""
    try:
        for root, dirs, files in os.walk(temp_dir_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except PermissionError:
                    # Skip if file is being used by another process
                    continue
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                except OSError:
                    # Skip if directory is not empty or being used by another process
                    continue
        st.success("Congrats! you have successfully freed the memory")
        st.snow()
    except Exception as e:
        st.error(f"Error: {e}")

# Streamlit app
st.title("Directory Size Information")

# Sidebar
option = st.sidebar.selectbox("Select Folder", ("Temporary Folder", "Box Folder"))

# Loading icon
with st.spinner(f"Loading {option} Information..."):
    if option == "Temporary Folder":
        # Get temporary directory information
        temp_dir_path = get_temp_dir_path()

        if temp_dir_path:
            st.write("## Temporary Directory Information")
            st.markdown(f"**Temporary directory path:** {temp_dir_path}")

            folder_size_in_mb = get_folder_size(temp_dir_path) / 1024 / 1024
            folder_size_in_gb = folder_size_in_mb / 1024

            if folder_size_in_mb is not None and folder_size_in_gb is not None:
                # Determine the color for MB and GB values
                color_mb = "green" if folder_size_in_mb < 300 else "red"
                color_gb = "green" if folder_size_in_gb < 1 else "red"

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        f"<h3>Folder Size (MB): <span style='color:{color_mb};'>{folder_size_in_mb:.2f}</span></h3>",
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown(
                        f"<h3>Folder Size (GB): <span style='color:{color_gb};'>{folder_size_in_gb:.2f}</span></h3>",
                        unsafe_allow_html=True
                    )

                # Delete files and folders in temporary folder option
                if st.button("Delete Files and Folders in Temporary Folder"):
                    with st.spinner("Deleting files and folders..."):
                        delete_files_in_temp_folder(temp_dir_path)
        else:
            st.error("Temporary directory path not found.")
    elif option == "Box Folder":
        def get_box_folder_path():
            """Returns the Box folder path based on the operating system."""
            try:
                home_dir = os.path.expanduser("~")
                if platform.system() == "Windows":
                    box_sync_path = os.path.join(home_dir, "Box Sync")
                    box_path = os.path.join(home_dir, "Box")
                    if os.path.exists(box_sync_path):
                        return box_sync_path
                    elif os.path.exists(box_path):
                        return box_path
                elif platform.system() == "Darwin":  # macOS
                    box_sync_path = os.path.join(home_dir, "Box Sync")
                    if os.path.exists(box_sync_path):
                        return box_sync_path
                    else:
                        return None
                else:
                    return None
            except Exception as e:
                st.error(f"Error: {e}")
                return None

        box_folder_path = get_box_folder_path()

        if box_folder_path and os.path.exists(box_folder_path):
            st.write("## Box Folder Information")
            st.markdown(f"**Box folder path:** {box_folder_path}")

            top_10_folders = get_top_10_folders(box_folder_path)
            st.write("### Top 10 Folders by Size in Box")
            for folder, size in top_10_folders:
                size_in_mb = size / 1024 / 1024
                color = "green" if size_in_mb < 300 else "red"
                st.markdown(f"<h4>{folder}: <span style='color:{color};'>{size_in_mb:.2f} MB</span></h4>", unsafe_allow_html=True)
        else:
            st.error("Box folder path not found.")
