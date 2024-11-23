# Importing Libraries
import requests
import psycopg2
import pandas as pd
import json
import http.client
import os
import csv
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import create_engine, String, Float, Text, Integer, Date

pd.set_option('future.no_silent_downcasting', True)

# Scraping the Data using API
conn = http.client.HTTPSConnection("realty-mole-property-api.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "eb615e7b27msh20dba361cc462fep193aefjsnf51bbf461fc4",
    'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com"
}

conn.request("GET", "/randomProperties?limit=10000", headers=headers)
res = conn.getresponse()
data = res.read().decode("utf-8")
dt_res = json.loads(data)

# Load the dataset
prop_df = pd.DataFrame(dt_res)

# Transformation
# converting dictionary column to string
prop_df['features'] = prop_df['features'].apply(json.dumps)
# prop_df['owner'] = prop_df['owner'].apply(json.dumps)
# prop_df['taxAssessment'] = prop_df['taxAssessment'].apply(json.dumps)
# prop_df['propertyTaxes'] = prop_df['propertyTaxes'].apply(json.dumps)


prop_df['lotSize'] = prop_df['lotSize'].astype(str).str.strip().replace({'Single Family': 0, 'Unknown': 0})
prop_df['lotSize'] = pd.to_numeric(prop_df['lotSize'], errors='coerce')
prop_df['lotSize'] = prop_df['lotSize'].fillna(0)
prop_df['lastSaleDate'] = pd.to_datetime(prop_df['lastSaleDate'], errors='coerce').dt.date


# replace NaN values with appropriate defaults or remove rows/columns as necessary
prop_df = prop_df.fillna({
    'assessorID': 'Unknown',                 
    'legalDescription': 'Not available',    
    'squareFootage': 0,                     
    'subdivision': 'Not available',         
    'yearBuilt': 0,                         
    'bathrooms': 0,                         
    'lotSize': 0,                           
    'propertyType': 'Unknown',              
    'lastSalePrice': 0,                     
    'lastSaleDate': 0,        
    'taxAssessment': 'Not available',       
    'owners': 'Unknown',                    
    'propertyTaxes': 'Not available',       
    'bedrooms': 0,                          
    'longitude': 0.0,                       
    'latitude': 0.0, 
    'ownerOccupied': False,
    'zoning': 'Unknown',
    'features': 'Not available',
    'addressLine2': 'Not available',
    'cooling': 'Unknown',
    'owner': 'Unknown',
    'formattedAddress': 'Not available',    
    'county': 'Unknown'               
})

# Step 2: Infer objects to optimize types
prop_df = prop_df.infer_objects(copy=False)

# Dropping all rows containing null values
prop_df = prop_df.dropna(how = 'all')

# Create Fact Table
fct_table = prop_df[['addressLine1', 'city', 'state', 'formattedAddress', 'squareFootage', 'yearBuilt', 'bathrooms', 'bedrooms', 'lotSize', 'propertyType', 'longitude', 'latitude']].drop_duplicates()

# Location Dimension Table
dim_location = prop_df[['addressLine1', 'city', 'state', 'zipCode', 'county', 'longitude', 'latitude']].reset_index(drop = True)
dim_location['location_id'] = dim_location.index + 1

# Sales Dimension Table 
dim_sales = prop_df[['lastSalePrice', 'lastSaleDate']].drop_duplicates().reset_index(drop = True)
dim_sales['sales_id'] = dim_sales.index + 1
dim_sales.head()

# Property Features Dimension tables
dim_feature = prop_df[['zoning', 'features', 'propertyType']].dropna().reset_index(drop = True)
dim_feature['feature_id'] = dim_feature.index + 1

# Save files as csv
fct_table.to_csv('./dataset/fct_table.csv', index = False)
dim_location.to_csv('./dataset/dim_location.csv', index = False)
dim_feature.to_csv('./dataset/dim_feature.csv', index = False)
dim_sales.to_csv('./dataset/dim_sales.csv', index = False)

# Connect to Posgtres Engine
engine = create_engine('postgresql://postgres:omotayo@localhost:5432/postgres')
with engine.connect() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS zipco;"))

# creating Datatypes
fct_table_dtype = {
    'addressLine1': String(255),
    'city': String(100),
    'state': String(50),
    'zipCode': String(255),
    'formattedAddress': String(255),
    'squareFootage': Float,
    'yearBuilt': Float,
    'bathrooms': Float,
    'bedrooms': Float,
    'lotSize': Float,
    'propertyType': String(100),
    'longitude': Float,
    'latitude': Float
}

dim_location_dtype = {
    'addressLine1': String(255),
    'city': String(100),
    'state': String(50),
    'zipCode': Integer,
    'county': String(100),
    'longitude': Float,
    'latitude': Float
}

dim_sales_dtype = {
    'lastSalePrice': Float,
    'lastSaleDate': Date
}

dim_features_dtype = {
    'features': Text,
    'propertyType': String(100),
    'zoning': String(100)
}

# Load Data to PostgreSQL 
fct_table.to_sql('fact_table', con=engine, schema='zipco', if_exists='replace', index=False,)
dim_location.to_sql('dim_location', con=engine, schema='zipco', if_exists='replace', index=False,)
dim_sales.to_sql('dim_sales', con=engine, schema='zipco', if_exists='replace', index=False,)
dim_feature.to_sql('dim_features', con=engine, schema='zipco', if_exists='replace', index=False,)


# Read SQL Queries from analysis.sql
with open("./sql_script/analysis.sql", "r") as file:
    sql_queries = file.read().split(';')  # Split the queries by semicolon

# Execute the first query: Average price
avg_price_query = sql_queries[0].strip()  # Get the first query and remove any surrounding whitespace
avg_price = pd.read_sql(avg_price_query, engine)
print("Average Sale Price:")
print(avg_price)

# Execute the second query: Property count by state
state_count_query = sql_queries[1].strip()  # Get the second query
state_counts = pd.read_sql(state_count_query, engine)
print("\nProperty Count by State:")
print(state_counts)

# Saving the Queries
avg_price.to_json("./savedQueries/average_price.json", orient = "records")
state_counts.to_json("./savedQueries/state_counts.json", orient = "records")

