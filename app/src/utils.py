from fastapi import UploadFile, HTTPException
import pandas as pd
import numpy as np

def process_uploaded_file(file: UploadFile):
    """
    Checks for the validity of the uploaded file and process it into a pandas dataframe and validates its content
    """

    if not is_csv(file):
        raise HTTPException(
            status_code=400, 
            detail='The uploaded file must be a CSV file'
        )
    try:
        df = pd.read_csv(file.file)
    except:
        raise HTTPException(
            status_code=500,
            detail='We faced an internal error while reading the file. Please try again'
        )

    if not is_file_structure_valid(df):
        raise HTTPException(
            status_code=400,
            detail='The CSV file is either empty or malformated. The file must contain at least one row of products and two columns <product_name>, <customer_avrage_rating>'
        )

    df = remove_duplicates_and_na(df)

    return df


def is_csv(file: UploadFile):
    """
    check if the uploaded file is of type csv (comma separated values)
    """
    file_extension = file.filename.lower().split('.')[-1]
    if not file_extension == 'csv':
        return False
    return True


def remove_duplicates_and_na(dataframe):
    """
    filter out any duplicate rows and rows with all 'na/nan' values
    """
    dataframe.drop_duplicates(subset=['product_name', 'customer_avrage_rating'], inplace=True)
    dataframe.dropna(subset=['product_name', 'customer_avrage_rating'], inplace=True)
    return dataframe


def is_file_structure_valid(dataframe):
    """
    check if the CSV file is not empty and exist the two columns 'product_name', 'customer_avrage_rating' with valid data types in the file
    """
    columns_exist = {'product_name', 'customer_avrage_rating'}.issubset(dataframe.columns)
    if columns_exist:
        valid_columns_type = dataframe.dtypes['product_name'] == np.object and dataframe.dtypes['customer_avrage_rating'] == np.float64
        if not dataframe.empty and valid_columns_type:
            return True
    return False
