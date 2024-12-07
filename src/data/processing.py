import pandas as pd
import os

# Define some constants
DATA_FOLDER = os.path.join(os.path.dirname(__file__), '../../data')
DATA_PROCESSED_FOLDER = os.path.join(DATA_FOLDER, 'processed')

# Read the files
df_beers = pd.read_csv(os.path.join(DATA_FOLDER, 'beers.csv'))
df_breweries = pd.read_csv(f'{DATA_FOLDER}/breweries.csv')
df_ratings = pd.read_parquet(f'{DATA_FOLDER}/ratings.pq')
df_users = pd.read_csv(f'{DATA_FOLDER}/users.csv')

# Clean the beers
df_beers = df_beers[['beer_id', 'beer_name', 'brewery_id', 'brewery_name', 'style', 'abv']]
df_beers = df_beers.dropna()

# Clean the breweries
df_breweries = df_breweries[['id', 'name', 'location']]
df_breweries.columns = ['brewery_id', 'brewery_name', 'location_brewery']
df_breweries = df_breweries.dropna()

# Clean the users
df_users = df_users[['user_id', 'user_name', 'location', 'joined']]
df_users.columns = ['user_id', 'user_name', 'location_user', 'joined']
df_users['joined'] = pd.to_datetime(df_users['joined'], unit='s')
df_users = df_users.dropna()

# Remove the ratings that have elements that have been cleaned before
beers_ids = df_ratings['beer_id'].unique()
breweries_ids = df_ratings['brewery_id'].unique()
users_ids = df_ratings['user_id'].unique()

df_ratings = df_ratings[df_ratings['beer_id'].isin(beers_ids)]
df_ratings = df_ratings[df_ratings['brewery_id'].isin(breweries_ids)]
df_ratings = df_ratings[df_ratings['user_id'].isin(users_ids)]
df_ratings = df_ratings[['date', 'beer_id', 'user_id', 'brewery_id', 'abv', 'style', 'rating', 'palate', 'taste', 'appearance', 'aroma', 'overall', 'text']]

# Add location information to the ratings
df_ratings = df_ratings.join(df_breweries.set_index('brewery_id'), on='brewery_id')
df_ratings = df_ratings.join(df_users.set_index('user_id'), on='user_id')

# Save the processed data
if not os.path.exists(DATA_PROCESSED_FOLDER):
    os.makedirs(DATA_PROCESSED_FOLDER)
df_ratings.drop(columns=['text']).to_parquet(f'{DATA_PROCESSED_FOLDER}/ratings_no_text.pq')
df_ratings[['text']].to_parquet(f'{DATA_PROCESSED_FOLDER}/ratings_only_text.pq')
df_beers.to_parquet(f'{DATA_PROCESSED_FOLDER}/beers.pq')
df_breweries.to_parquet(f'{DATA_PROCESSED_FOLDER}/breweries.pq')
df_users.to_parquet(f'{DATA_PROCESSED_FOLDER}/users.pq')