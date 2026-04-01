import pandas as pd

# Mapping of Data Brands (from CSV) to Chain Scale Categories
# Note: Hand-tuned based on the unique values found in both CSVs
BRAND_TO_SCALE = {
    'DAYS INN': 'Economy',
    'HOWARD JOHNSON': 'Economy',
    'SUPER 8': 'Economy',
    'TRAVELODGE': 'Economy',
    'MICROTEL': 'Economy',
    'ECHO': 'Midscale', # Echo Suites
    'WINGATE BY WYNDHAM': 'Midscale',
    'AMERICINN': 'Midscale',
    'BAYMONT': 'Midscale',
    'RAMADA': 'Midscale',
    'HAWTHORN SUITES BY WYNDHAM': 'Upper Midscale',
    'LA QUINTA': 'Upper Midscale',
    'TRYP': 'Upper Midscale',
    'WYNDHAM GARDEN': 'Upper Midscale',
    'TRADEMARK HOTELS': 'Upper Midscale',
    'WATERWALK': 'Upscale',
    'WYNDHAM': 'Upper Upscale',
    'DOLCE': 'Upper Upscale',
    'WYNDHAM GRAND': 'Luxury',
    'REGISTRY COLLECTION': 'Luxury',
    # Others found in data but not in scale CSV (will categorize as Other or map manually)
    'VIENNA HOUSE': 'Upper Upscale',
    'FEN HOTELS': 'Midscale',
    'WYNDHAM ALLTRA': 'Upscale'
}

def get_chain_scale(brand_name):
    return BRAND_TO_SCALE.get(brand_name.upper(), "Other")

def add_scale_info(df):
    df['chain_scale'] = df['property_brand_name'].apply(get_chain_scale)
    return df
