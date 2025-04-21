import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title = "Data Sweeper", layout='wide' )


#custom css

st.markdown(
    """
<style>
.stApp
background-color: black;
color: white;
}
</style>
""",
unsafe_allow_html=True
)

#title and description
st.title("Datasweepering Integrator By Tooba Yameen" )
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization Creating the project for Quarter 3!")

#file uploader
uploader_files = st.file_uploader("Upload your files (accepts CSV or Excel):" , type=["csv","xlsx"], accept_multiple_files=(True))

if uploader_files:
    for files in uploader_files:
        files_ext = os.path.splitext(files.name)[-1].lower()

        if files_ext == ".csv":
            df = pd.read_csv(files)
        elif files_ext == "xlsx":
            df = pd.read_excel(files)
        else:
            st.error(f"Unsupported file type: {files_ext}")
            continue

        #file details
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())

        #data cleaning
        st.subheader ("Data Claning Options")
        if st.checkbox(f"Clean data for {files.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file: {files.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")

                    with col2:
                        if st.button(f"Fill missing values for {files.name}"):
                            numeric_cols = df.select_dtypes(includes=['number']).columns
                            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                            st.write("Missing values have been filled!")

                            st.subheader("Select columns to Keep")
                            columns = st.multiselect(f"Choose columns for {files.name}", df.columns, default=df.columns)
                            df = df[columns]

            #data visualization
            st.subheader("Data Visualization")
            if st.checkbox(f"Show Visualisation for {files.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #Conversation Options

        st.subheader("Conversation Options")
        conversation_type = st.radio(f"Convert {files.name} to:" , ["CSV" , "Excel"], key=files.name)
        if st.button(f"Convert{files.name}"):
            buffer = BytesIo()
            if conversation_type == "CSV":
                df.to.csv(buffer, index=False)
                file_name = files.name.replace(files_ext, ".csv")
                mime_type = "text/csv"

            elif conversation_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = files.name.replace(files_ext, "xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheethtml.sheet"
                buffer.seek(0)

        st.download_button(
            label=f"Dowload {files.name} as {conversation_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

        st.success("All files processed sucessfully!!")