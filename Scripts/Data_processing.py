import pandas as pd
from Data_loading import calculate_missing_aqi

def get_aqi_category(aqi):
    if aqi <= 50:   return 'Good'
    if aqi <= 100:  return 'Satisfactory'
    if aqi <= 200:  return 'Moderate'
    if aqi <= 300:  return 'Poor'
    if aqi <= 400:  return 'Very Poor'
    return 'Severe'

def process_comprehensive_analysis(df):
    """Run full AQI analysis: daily, city, yearly, seasonal summaries."""
    df = calculate_missing_aqi(df)
    df['aqi_category'] = df['aqi'].apply(get_aqi_category)

    daily = df.groupby('date').agg(
        avg_aqi=('aqi','mean'),
        min_aqi=('aqi','min'),
        max_aqi=('aqi','max'),
        days=('aqi','count'),
        avg_pm25=('pm25','mean'),
        avg_pm10=('pm10','mean')
    ).reset_index()

    city = df.groupby('city').agg(
        days=('aqi','count'),
        avg_aqi=('aqi','mean'),
        min_aqi=('aqi','min'),
        max_aqi=('aqi','max'),
        avg_pm25=('pm25','mean'),
        avg_pm10=('pm10','mean')
    ).reset_index()

    yearly = df.groupby(['year','city']).agg(
        days=('aqi','count'),
        avg_aqi=('aqi','mean')
    ).reset_index()

    seasonal = df.groupby(['season','city']).agg(
        days=('aqi','count'),
        avg_aqi=('aqi','mean')
    ).reset_index()

    return {'daily': daily, 'city': city, 'yearly': yearly, 'seasonal': seasonal}
