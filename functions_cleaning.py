import numpy as np
import pandas as pd
from geopy.point import Point
from geopy.geocoders import Nominatim

def count_na(df: pd.DataFrame) -> pd.DataFrame:
    
    """Returns the sum and percentage of NaN values for each column of a given dataframe"""
    
    return pd.DataFrame({'sum': df.isna().sum(),
                         'perc': df.isna().sum() * 100 / len(df)}).sort_values(by='perc',
                                                                               ascending=False)

def to_point(lat: float,lon: float):
    
    """Transforms the given latitude and longitude into a coordinate system (use Point method
    from geopy"""
    
    return Point(lat, lon)

def get_geo_feature(coord, feature: str, geolocator):
    
    """Get the desired feature from a given geographic coordinate (e.g.,
    country name, country code, etc: please refers to the geopy doc for more informations)"""
    
    try:
        location = geolocator.reverse(coord)
        return location.raw['address'][feature]
    
    except:
        return np.nan
    
def replace_exceptions(row: str) -> str or float:
    
    """This function was made to be applied to a single dataframe string column. Return either 'ocean',
    'sea', or a predefined country name."""
    
    if re.search(r"ocean|sea", row):
        return re.findall(r'ocean|sea', row)[0]
    
    elif re.search(r"brasil", row):
        return "brazil"
    
    elif re.search(r"uk/england", row):
        return "united kingdom of great britain and northern ireland (the)"
    
    elif re.search(r"netherlands", row):
        return "netherlands (the)"
    
    elif re.search(r"bolivia", row):
        return "bolivia (plurinational state of)"
    
    elif re.search(r"australi", row):
        return "australia"
    
    else:
        return np.nan

def print_city_unique():
    return print(len(set(df['city'])))

def clean_city_col(df: pd.DataFrame, col='city') -> pd.DataFrame:
    
    print_city_unique()
    
    # removing parentheses and their content for the column "city"
    df[col] = df[col].str.replace(r"\(.*\)","", regex=True)
    print_city_unique()
    
    # removing non-alphanumeric characters from the strings for the column "city", including numbers
    df[col] = [re.sub('[^\w\s]|\d+', '', x) for x in df[col]]
    print_city_unique()
    
    # turning the first letter of each city name into a capital letter
    df[col] = df[col].str.title()
    print_city_unique()
    
    #If a row contains only one word, suppress all white spaces within it
    #If a row contains 2 words or more, doe nothing
    df['test'] = df[col].str.split().apply(len).value_counts()
    df[col] = np.where(df['test'] > 1, df[col], df[col].str.replace(" ",""))
    
    df = df.drop(['test'], axis=1)
    return df

