import pandas as pd
import os

def load_fi_data(file_path):
    """
    Loads both sheets from the Ethiopia Financial Inclusion dataset.
    Returns: A dictionary of DataFrames.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Loading both sheets as a dictionary
    xls = pd.ExcelFile(file_path)
    data_dict = {
        'unified_data': pd.read_excel(xls, sheet_name="ethiopia_fi_unified_data"),
        'impact_links': pd.read_excel(xls, sheet_name="Impact_sheet")
    }
    return data_dict

def explore_impact_mechanics(data_dict):
    """
    Explains the connection between Impact_sheet and the unified data.
    """
    df_main = data_dict['unified_data']
    df_impact = data_dict['impact_links']
    
    # Task 1 Requirement: Understand how impact_link connects via parent_id
    # We look for 'event' records in the main sheet and link them to Impact_sheet
    events = df_main[df_main['record_type'] == 'event'][['record_id', 'indicator', 'notes']]
    
    # Merging to see the relationship: Event -> Impact Link -> Target Indicator
    connection_map = df_impact.merge(
        events, 
        left_on='parent_id', 
        right_on='record_id', 
        suffixes=('_link', '_event')
    )
    
    return connection_map

def summarize_pillars(df):
    """Analyzes the challenge of events not being pre-assigned to pillars."""
    event_counts = df[df['record_type'] == 'event']['pillar'].isna().sum()
    return f"Events without pre-assigned pillars: {event_counts} (Enables unbiased modeling)"

def load_reference_codes(file_path):
    """Loads valid field values and descriptions."""
    return pd.read_excel(file_path)

def validate_records(df, ref_df):
    """
    Checks if 'pillar', 'indicator_code', and 'category' 
    match the valid values in reference_codes.csv.
    """
    # Extract valid sets from reference codes
    valid_pillars = set(ref_df[ref_df['field'] == 'pillar']['code'])
    valid_indicators = set(ref_df[ref_df['field'] == 'indicator_code']['code'])
    
    # Identify invalid rows (ignoring NaNs for events as discussed)
    invalid_pillars = df[~df['pillar'].isin(valid_pillars) & df['pillar'].notna()]
    invalid_indicators = df[~df['indicator_code'].isin(valid_indicators)]
    
    return {
        "invalid_pillar_count": len(invalid_pillars),
        "invalid_indicator_count": len(invalid_indicators),
        "flagged_indicator_codes": invalid_indicators['indicator_code'].unique().tolist()
    }
def analyze_impact_links(data_dict):
    """
    Relates events in the main sheet to their impacts in the Impact_sheet.
    The Impact_sheet uses 'parent_id' to reference the 'record_id' of an event.
    """
    df_main = data_dict['data']
    df_impact = data_dict['impact']
    
    events = df_main[df_main['record_type'] == 'event']
    
    # Merge events with their modeled impacts
    relationship_df = df_impact.merge(
        events[['record_id', 'indicator', 'notes']], 
        left_on='parent_id', 
        right_on='record_id', 
        suffixes=('_target', '_source_event')
    )
    return relationship_df

def get_record_counts(df):
    """Returns counts for key dimensions to understand data density."""
    dimensions = ['record_type', 'pillar', 'source_type', 'confidence']
    counts = {dim: df[dim].value_counts(dropna=False).to_dict() for dim in dimensions}
    return counts
def get_temporal_coverage(df):
    """Identifies the start and end of actual measured data."""
    obs = df[df['record_type'] == 'observation']
    # Ensure observation_date is datetime
    obs_dates = pd.to_datetime(obs['observation_date'])
    return obs_dates.min(), obs_dates.max()

def list_unique_indicators(df):
    """Lists unique indicators and how many data points exist for each."""
    return df.groupby('indicator_code').agg(
        record_count=('record_id', 'count'),
        latest_value=('value_numeric', 'last'),
        unit=('unit', 'first')
    )
def get_temporal_coverage(df):
    """Identifies the start and end of actual measured data."""
    obs = df[df['record_type'] == 'observation']
    # Ensure observation_date is datetime
    obs_dates = pd.to_datetime(obs['observation_date'])
    return obs_dates.min(), obs_dates.max()

def list_unique_indicators(df):
    """Lists unique indicators and how many data points exist for each."""
    return df.groupby('indicator_code').agg(
        record_count=('record_id', 'count'),
        latest_value=('value_numeric', 'last'),
        unit=('unit', 'first')
    )