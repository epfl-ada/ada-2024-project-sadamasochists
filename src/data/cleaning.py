# Import all the needed libraries
import pandas as pd
import os

# Define a function to process the states
def clean_states(df, loc_column_name, suffix):
    # Do the cleaning
    split = df[loc_column_name].str.split(', ', expand=True)
    split.columns = [f'country_{suffix}', f'state_{suffix}']
    df = df.drop(loc_column_name, axis=1)
    df = pd.concat([df, split], axis=1)

    # Do any remapping
    mapping = {
        "Wales": "United Kingdom",
        "England": "United Kingdom",
        "Scotland": "United Kingdom",
        "Northern Ireland": "United Kingdom"
    }
    df[f'country_{suffix}'] = df[f'country_{suffix}'].replace(mapping)

    # Return the cleaned dataframe
    return df

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
df_breweries = clean_states(df_breweries, 'location_brewery', 'brewery')

# Clean the users
df_users = df_users[['user_id', 'user_name', 'location', 'joined']]
df_users.columns = ['user_id', 'user_name', 'location_user', 'joined']
df_users['joined'] = pd.to_datetime(df_users['joined'], unit='s')
df_users = df_users.dropna()
df_users = clean_states(df_users, 'location_user', 'user')

# Remove the ratings that have elements that have been cleaned before
df_ratings = df_ratings[df_ratings['beer_id'].isin(df_ratings['beer_id'].unique())]
df_ratings = df_ratings[df_ratings['brewery_id'].isin(df_ratings['brewery_id'].unique())]
df_ratings = df_ratings[df_ratings['user_id'].isin(df_ratings['user_id'].unique())]
df_ratings = df_ratings[['date', 'beer_id', 'user_id', 'brewery_id', 'abv', 'style', 'rating', 'palate', 'taste', 'appearance', 'aroma', 'overall', 'text']]
df_ratings['year'] = df_ratings['date'].dt.year

# Add location information to the ratings
df_ratings = df_ratings.join(df_breweries.set_index('brewery_id'), on='brewery_id')
df_ratings = df_ratings.join(df_users[['user_id', 'country_user', 'state_user']].set_index('user_id'), on='user_id')

# Data clearning
df_ratings = df_ratings[(df_ratings['date'].dt.year>=2002) & (df_ratings['date'].dt.year<=2016)]

# Define the countries where the breweries have more than 250 reviews
countries_min_number_reviews_breweries = df_ratings.groupby('country_brewery').size().sort_values(ascending=False).reset_index().rename(columns={0:'number_reviews'})
countries_min_number_reviews_breweries = list(countries_min_number_reviews_breweries[countries_min_number_reviews_breweries['number_reviews']>=250]['country_brewery'])

# Define the countries where the users from that country have more than 250 reviews
countries_min_number_reviews_users = df_ratings.groupby('country_user').size().sort_values(ascending=False).reset_index().rename(columns={0:'number_reviews'})
countries_min_number_reviews_users = list(countries_min_number_reviews_users[countries_min_number_reviews_users['number_reviews']>=250]['country_user'])

# For country user consider only countries with at least 5 users
countries_min_number_users = df_ratings.groupby('country_user')['user_id'].nunique().reset_index().rename(columns={'user_id':'number_users'})
countries_min_number_users = list(countries_min_number_users[countries_min_number_users['number_users']>=5]['country_user'])

# Define the countries to keep and filter the data
df_ratings = df_ratings[df_ratings['country_brewery'].isin(countries_min_number_reviews_breweries)]
df_ratings = df_ratings[df_ratings['country_user'].isin(countries_min_number_reviews_users)]
df_ratings = df_ratings[df_ratings['country_user'].isin(countries_min_number_users)]
df_ratings = df_ratings.rename(columns={'palete': 'mouthfeel'})

# Remove the beers that are not in the ratings
df_beers = df_beers[df_beers['beer_id'].isin(df_ratings['beer_id'])]

# Remove the breweries that are not in the ratings
df_breweries = df_breweries[df_breweries['brewery_id'].isin(df_ratings['brewery_id'])]

# Remove the users that are not in the ratings
df_users = df_users[df_users['user_id'].isin(df_ratings['user_id'])]

# Rename the column palate into mouthfeel
df_ratings = df_ratings.rename(columns={'palate': 'mouthfeel'})

# Save the processed data
if not os.path.exists(DATA_PROCESSED_FOLDER):
    os.makedirs(DATA_PROCESSED_FOLDER)
df_ratings.drop(columns=['text']).to_parquet(f'{DATA_PROCESSED_FOLDER}/ratings_no_text.pq')
df_ratings[['text']].to_parquet(f'{DATA_PROCESSED_FOLDER}/ratings_only_text.pq')
df_beers.to_parquet(f'{DATA_PROCESSED_FOLDER}/beers.pq')
df_breweries.to_parquet(f'{DATA_PROCESSED_FOLDER}/breweries.pq')
df_users.to_parquet(f'{DATA_PROCESSED_FOLDER}/users.pq')