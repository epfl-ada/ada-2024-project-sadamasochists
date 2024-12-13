class DataPresentation:
    def __init__(self, df_beers, df_breweries, df_users, df_ratings_no_text):
        self.df_users = df_users
        self.df_breweries = df_breweries
        self.df_beers = df_beers
        self.df_ratings_no_text = df_ratings_no_text
    
    def get_spatial_aggregated(self):
        # Compute the aggregated value for countries outside the US
        beers_per_country_no_US = self.df_beers[self.df_beers['country_beer'] != 'United States'].groupby('country_beer').size().reset_index(name='count').rename(columns={'country_beer': 'location'})
        users_per_country_no_US = self.df_users[self.df_users['country_user'] != 'United States'].groupby('country_user').size().reset_index(name='count').rename(columns={'country_user': 'location'})
        breweries_per_country_no_US = self.df_breweries[self.df_breweries['country_brewery'] != 'United States'].groupby('country_brewery').size().reset_index(name='count').rename(columns={'country_brewery': 'location'})
        ratings_in_country_no_US = self.df_ratings_no_text[self.df_ratings_no_text['country_brewery'] != 'United States'].groupby('country_brewery').size().reset_index(name='count').rename(columns={'country_brewery': 'location'})
        ratings_users_country_no_US = self.df_ratings_no_text[self.df_ratings_no_text['country_user'] != 'United States'].groupby('country_user').size().reset_index(name='count').rename(columns={'country_user': 'location'})
        df_no_US = [beers_per_country_no_US, users_per_country_no_US, breweries_per_country_no_US, ratings_in_country_no_US, ratings_users_country_no_US]

        # Compute the aggregated value for the states of the US
        beers_per_country_US = self.df_beers[self.df_beers['country_beer'] == 'United States'].groupby('state_beer').size().reset_index(name='count').rename(columns={'state_beer': 'location'})
        users_per_country_US = self.df_users[self.df_users['country_user'] == 'United States'].groupby('state_user').size().reset_index(name='count').rename(columns={'state_user': 'location'})
        breweries_per_country_US = self.df_breweries[self.df_breweries['country_brewery'] == 'United States'].groupby('state_brewery').size().reset_index(name='count').rename(columns={'state_brewery': 'location'})
        ratings_in_country_US = self.df_ratings_no_text[self.df_ratings_no_text['country_brewery'] == 'United States'].groupby('state_brewery').size().reset_index(name='count').rename(columns={'state_brewery': 'location'})
        ratings_users_country_US = self.df_ratings_no_text[self.df_ratings_no_text['country_user'] == 'United States'].groupby('state_user').size().reset_index(name='count').rename(columns={'state_user': 'location'})
        df_US = [beers_per_country_US, users_per_country_US, breweries_per_country_US, ratings_in_country_US, ratings_users_country_US]

        # Return the dataframes
        return df_no_US, df_US
    
    def get_temporal_aggregated(self):
        # Compute the ratings grouping by year
        ratings_grouping = self.df_ratings_no_text.groupby(self.df_ratings_no_text['date'].dt.year).size().reset_index(name='count').rename(columns={'date': 'Year', 'count': 'Number of ratings'})

        # Compute the users grouping by year
        users_grouping = self.df_users.groupby(self.df_users['joined'].dt.year).size().reset_index(name='count').rename(columns={'joined': 'Year', 'count': 'Number of users'})

        # Return the dataframes
        return ratings_grouping, users_grouping

