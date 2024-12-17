import plotly.graph_objects as go
import os

class DataPresentation:
    def __init__(self, df_beers, df_breweries, df_users, df_ratings_no_text, save_root):
        self.df_users = df_users
        self.df_breweries = df_breweries
        self.df_beers = df_beers
        self.df_ratings_no_text = df_ratings_no_text
        if not os.path.exists(save_root):
            os.makedirs(save_root)
        self.save_root = save_root
        
    def get_spatial_data(self):
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
    
    def get_temporal_data(self):
        # Compute the ratings grouping by year
        ratings_grouping = self.df_ratings_no_text.groupby(self.df_ratings_no_text['date'].dt.year).size().reset_index(name='count').rename(columns={'date': 'Year', 'count': 'Number of ratings'})

        # Compute the users grouping by year
        users_grouping = self.df_users.groupby(self.df_users['joined'].dt.year).size().reset_index(name='count').rename(columns={'joined': 'Year', 'count': 'Number of users'})

        # Return the dataframes
        return ratings_grouping, users_grouping
    
    def plot_top_5(self):
        # Define the top 5 countries with the most beers
        df_beers_country = self.df_beers.groupby('country_beer').size().sort_values(ascending=False).reset_index().rename(columns={0:'count', 'country_beer': 'location'})
        df_beers_country = df_beers_country.head(5)

        # Define the top 5 countries with the most users
        df_users_country = self.df_users.groupby('country_user').size().sort_values(ascending=False).reset_index().rename(columns={0:'count', 'country_user': 'location'})
        df_users_country = df_users_country.head(5)

        # Define the top 5 countries with the most breweries
        df_breweries_country = self.df_breweries.groupby('country_brewery').size().sort_values(ascending=False).reset_index().rename(columns={0:'count', 'country_brewery': 'location'})
        df_breweries_country = df_breweries_country.head(5)

        # Define the top 5 states with the most ratings (user origin)
        df_ratings_user_country = self.df_ratings_no_text.groupby('country_user').size().sort_values(ascending=False).reset_index().rename(columns={0:'count', 'country_user': 'location'})
        df_ratings_user_country = df_ratings_user_country.head(5)

        # Define the top 5 states with the most ratings (brewery origin)
        df_ratings_brewery_country = self.df_ratings_no_text.groupby('country_brewery').size().sort_values(ascending=False).reset_index().rename(columns={0:'count', 'country_brewery': 'location'})
        df_ratings_brewery_country = df_ratings_brewery_country.head(5)

        # Create the figure
        fig = go.Figure()
        
        # Add traces
        fig.add_trace(go.Bar(x=df_beers_country['location'], y=df_beers_country['count'], name='Beers'))
        fig.add_trace(go.Bar(x=df_users_country['location'], y=df_users_country['count'], name='Users', visible=False))
        fig.add_trace(go.Bar(x=df_breweries_country['location'], y=df_breweries_country['count'], name='Breweries', visible=False))
        fig.add_trace(go.Bar(x=df_ratings_user_country['location'], y=df_ratings_user_country['count'], name='Ratings by user country', visible=False))
        fig.add_trace(go.Bar(x=df_ratings_brewery_country['location'], y=df_ratings_brewery_country['count'], name='Ratings by brewery country', visible=False))

        # Update the layout
        fig.update_layout(
            updatemenus=[
                dict(
                    active=0,
                    buttons=list([
                        dict(
                            label="Top 5 countries with more beers",
                            method="update",
                            args=[{"visible": [True, False, False, False, False]}, {"title": "Top 5 countries with more beers"}]
                        ),
                        dict(
                            label="Top 5 countries with more users",
                            method="update",
                            args=[{"visible": [False, True, False, False, False]}, {"title": "Top 5 countries with more users"}]
                        ),
                        dict(
                            label="Top 5 countries with more breweries",
                            method="update",
                            args=[{"visible": [False, False, True, False, False]}, {"title": "Top 5 countries with more breweries"}]
                        ),
                        dict(
                            label="Top 5 countries with more ratings based on the user country",
                            method="update",
                            args=[{"visible": [False, False, False, True, False]}, {"title": "Top 5 countries with more ratings based on the user country"}]
                        ),
                        dict(
                            label="Top 5 countries with more ratings based on the brewery country",
                            method="update",
                            args=[{"visible": [False, False, False, False, True]}, {"title": "Top 5 countries with more ratings based on the brewery country"}]
                        )
                    ]),
                    x=0.70,
                    xanchor="center",
                    y=1.1,
                    yanchor="top"
                )
            ],
            height=600,
            width=800
        )

        # Update the layout
        fig.update_layout(barmode='group', title_text='Top 5 countries with more beers')
        fig.show()

    def plot_temporal(self, data, year_label, count_label, title):
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data[year_label], y=data[count_label]))
        fig.update_layout(title=title, xaxis_title=year_label, yaxis_title=count_label, width=800, height=600)
        fig.show()