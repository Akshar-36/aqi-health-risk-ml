import pandas as pd
import numpy as np
import tabula

def _get_season(month):
    """Maps a month number to a season."""
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8, 9]:
        return 'Monsoon'
    elif month in [10, 11]:
        return 'Autumn'
    else:
        return 'Unknown'

def load_cpcb_data(file_path):
    """Load raw CPCB CSV file."""
    df = pd.read_csv(file_path)
    return df

def prepare_cpcb_dataframe(df):
    """Clean and prepare the CPCB DataFrame for analysis."""
    # Rename columns to lowercase
    df = df.rename(columns={
        'City': 'city',
        'Date': 'date',
        'PM2.5': 'pm25',
        'PM10': 'pm10',
        'NO': 'no',
        'NO2': 'no2',
        'NH3': 'nh3',
        'CO': 'co',
        'SO2': 'so2',
        'O3': 'o3',
        'Benzene': 'benzene',
        'Toluene': 'toluene',
        'Xylene': 'xylene',
        'AQI': 'aqi',
        'AQI_Bucket': 'aqi_bucket'
    })

    # Parse dates (DD-MM-YYYY)
    df['date_parsed'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    if df['date_parsed'].isna().all():
        df['date_parsed'] = pd.to_datetime(df['date'], infer_datetime_format=True, errors='coerce')
    df = df[df['date_parsed'].notna()]
    df['date'] = df['date_parsed'].dt.date
    df['year'] = df['date_parsed'].dt.year
    df['month'] = df['date_parsed'].dt.month
    df['day'] = df['date_parsed'].dt.day
    df['weekday'] = df['date_parsed'].dt.dayofweek
    df['season'] = df['month'].apply(_get_season)

    # Clean numeric columns (handle '####')
    for col in ['pm25','pm10','no','no2','nh3','co','so2','o3','benzene','toluene','xylene','aqi']:
        if col in df:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('#',''), errors='coerce')

    # Filter out rows missing both PM2.5 and PM10
    df = df.dropna(subset=['pm25','pm10'], how='all')

    # Standardize city names
    df['city'] = df['city'].str.strip().str.title()

    return df

def calculate_missing_aqi(df):
    """Calculate AQI where missing based on PM2.5 and PM10."""
    def _calc(c, bps):
        for lo,hi,alo,ahi in bps:
            if lo<=c<=hi:
                return (ahi-alo)/(hi-lo)*(c-lo)+alo
        return 500

    bp = {
        'pm25': [(0,30,0,50),(30,60,51,100),(60,90,101,200),(90,120,201,300),(120,250,301,400),(250,380,401,500)],
        'pm10': [(0,50,0,50),(50,100,51,100),(100,250,101,200),(250,350,201,300),(350,430,301,400),(430,510,401,500)]
    }

    mask = df['aqi'].isna() & df[['pm25','pm10']].notna().any(axis=1)
    for idx in df[mask].index:
        p25 = df.at[idx,'pm25'] or 0
        p10 = df.at[idx,'pm10'] or 0
        idx25 = _calc(p25, bp['pm25'])
        idx10 = _calc(p10, bp['pm10'])
        df.at[idx,'aqi'] = max(idx25, idx10)
    return df

def load_modis_data(file_path):
    """Load MODIS PM2.5 CSV file."""
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()
    if 'date' in df:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df