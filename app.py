import streamlit as sl
import pandas as pd
import os
from io import BytesIO
import openpyxl

sl.set_page_config(
    page_title="🐱‍👓 Data Sweeper",
    page_icon="🔥",
    layout="wide",
)

sl.title("📊 DATA SWEEPER")
sl.write(
    "Transform your files between CSV and Excel formats with built-in data cleaning and visualizations!."
)

uploaded_files = sl.file_uploader(
    "Upload your CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=False
)

if uploaded_files:
    file = uploaded_files
    file_extension = os.path.splitext(file.name)[-1].lower()
    if file_extension == ".csv":
        data_frame = pd.read_csv(file , encoding='Latin1' )
    elif file_extension == ".xlsx":
        data_frame =  pd.read_excel(file , engine='openpyxl' )
    else:
        sl.error(
            f"Invalid File Uploaded {file_extension}. Please either upload a CSV file or Excel file."
        )

    sl.write(f"**File Name** : {file.name}")
    sl.write(f"**File Size** : {round(file.size/1024,2)}")
    sl.write("Preview the head of the data Frame.")
    sl.dataframe(data_frame.head(10))

    sl.subheader("Data Cleaning Options.")
    if sl.checkbox(f"Clean Data for {file.name}"):
        col1, col2 = sl.columns(2)
        with col1:
            if sl.button(f"Remove Duplicates from {file.name}"):
                data_frame.drop_duplicates(inplace=True)
                sl.write("Duplicates Removed")
        with col2:
            if sl.button(f"fill Missing Values for {file.name}"):
                numeric_cols = data_frame.select_dtypes(include=["number"]).columns
                data_frame[numeric_cols] = data_frame[numeric_cols].fillna(
                    data_frame[numeric_cols].mean()
                )
                sl.write("Missing Values have been filled.")

    sl.subheader("Select Columns to Convert.")
    cols = sl.multiselect(
        f"Choose Columns for {file.name}", data_frame.columns, default=data_frame.columns
    )
    data_frame = data_frame[cols]

    # Creating Some Visualizations
    sl.subheader("Create Some Visualizations")
    if sl.checkbox(f"Show Visualizations for {file.name}"):
        sl.line_chart(data_frame.select_dtypes(include="number").iloc[:, :2])

    # Converting CSV into Excel Format and vice versa
    sl.subheader("Covert CSV into Excel or Vice Versa.")
    convert_to = sl.radio(
        f"🔄 Convert {file.name} to: ", ["CSV", "Excel"], key=file.name
    )
    buffer = BytesIO()
    if convert_to == "CSV":
        data_frame.to_csv(buffer, index=False)
        file_name = file.name.replace(file_extension, ".csv")
        mime_type = "text/csv"
    elif convert_to == "Excel":
        data_frame.to_excel(buffer, index=False)
        file_name = file.name.replace(file_extension, ".xlsx")
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    buffer.seek(0)
    sl.download_button(
        label=f"Get {file_name} as {convert_to} :",
        mime=mime_type,
        data=buffer,
        file_name=file_name,
    )
