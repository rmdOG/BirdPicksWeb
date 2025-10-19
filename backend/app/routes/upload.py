from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from ..database import engine # Import the database engine directly
from .. import models
import pandas as pd
import io

# This line creates the router object that main.py needs to import.
router = APIRouter()

@router.post("/data/upload")
async def upload_schedule(file: UploadFile = File(...)):
    """
    This endpoint handles the upload of the NHL schedule file.
    It reads the file, cleans the data types, and saves it to the
    'raw_schedule' table using pandas' to_sql for robust type handling.
    """
    try:
        # --- 1. Read the file into a pandas DataFrame ---
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
        else:
            raise HTTPException(400, "Unsupported file type. Please use CSV or XLSX.")
    except Exception as e:
        raise HTTPException(400, f"Error reading file: {e}")

    # --- 2. Define the mapping from file columns to database columns ---
    column_mapping = {
        'Date': 'date',
        'Time': 'time',
        'Visitor': 'visitor',
        'G': 'visitor_goals',
        'Home': 'home',
        'G.1': 'home_goals',
        'Att.': 'attendance',
        'Notes': 'notes'
    }
    df.rename(columns=column_mapping, inplace=True)
    
    # --- 3. Keep only the columns defined in our database model ---
    model_columns = [c.name for c in models.RawSchedule.__table__.columns if c.name != 'id']
    df_to_upload = df[df.columns.intersection(model_columns)]

    # --- 4. Correct data types to avoid database errors ---
    # This is the key fix for the "integer out of range" error.
    # We convert date/time and explicitly use pandas' nullable integer
    # type for columns that might have missing values.
    
    if 'date' in df_to_upload.columns:
        df_to_upload['date'] = pd.to_datetime(df_to_upload['date'], errors='coerce').dt.date
    if 'time' in df_to_upload.columns:
        # The file has time as a string, so we convert it to a datetime object first, then extract the time
        df_to_upload['time'] = pd.to_datetime(df_to_upload['time'].astype(str), errors='coerce').dt.time

    # Define integer columns
    integer_columns = ['visitor_goals', 'home_goals', 'attendance']
    for col in integer_columns:
        if col in df_to_upload.columns:
            # pd.to_numeric converts values to numbers, making non-numbers NaN
            # astype('Int64') converts the column to a nullable integer type, which handles NaN
            df_to_upload[col] = pd.to_numeric(df_to_upload[col], errors='coerce').astype('Int64')

    # --- 5. Save the cleaned DataFrame to the database ---
    try:
        # Using df.to_sql is robust and handles pandas dtypes (like Int64) correctly.
        # It will convert the special <NA> from Int64 columns to a SQL NULL value.
        df_to_upload.to_sql(
            name=models.RawSchedule.__tablename__,
            con=engine,
            if_exists='append',
            index=False
        )
        return {"status": "success", "records_uploaded": len(df_to_upload)}

    except Exception as e:
        raise HTTPException(500, f"Database error: {e}")

