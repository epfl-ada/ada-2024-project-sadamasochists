import numpy as np
import pandas as pd
import plotly.express as px
from src.utils.plots import plot_map_time
import os
import plotly.graph_objects as go

class ABV:
    def __init__(self, df_beers, df_breweries, df_users, df_ratings_no_text, save_folder):
        self.df_beers = df_beers
        self.df_breweries = df_breweries
        self.df_users = df_users
        self.df_ratings_no_text = df_ratings_no_text
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        self.save_folder = save_folder
    
    def plot_abv_vs_ratings(self):
        # Define some useful variables
        MAX_ABV = 20
        NUMBER_OF_SAMPLES_ABV = 201
        MIN_NUMBER_OF_RATING = 250

        # Process the data
        beer_ratings = []
        linspace = np.linspace(0, MAX_ABV, NUMBER_OF_SAMPLES_ABV)
        for year in sorted(self.df_ratings_no_text['date'].dt.year.unique()):
            # Filter the data by the year
            df_year = self.df_ratings_no_text[self.df_ratings_no_text['year'] == year]
            
            # Iterate within the ABV range
            for i in range(len(linspace) - 1):
                # Filter the data
                min_abv = round(linspace[i], 2)
                max_abv = round(linspace[i + 1], 2)

                # Compute the matrics
                filtered = df_year[(df_year['abv'] >= min_abv) & (df_year['abv'] < max_abv)]
                ratings = filtered['rating'].mean()
                nbr_ratings = filtered['rating'].count()

                # Append the data
                if nbr_ratings > MIN_NUMBER_OF_RATING:
                    beer_ratings.append({'year': year, 'abv': (min_abv+max_abv)/2, 'rating': ratings, 'nbr_ratings': nbr_ratings})

        # Convert to DataFrame
        beer_ratings = pd.DataFrame(beer_ratings)

        # Do the plot
        fig = px.scatter(beer_ratings, x='abv', y='rating', size='nbr_ratings', hover_name='abv',animation_frame='year', labels={'abv': 'ABV:', 'rating': 'Average Rating:', 'nbr_ratings': 'Number of ratings:'},range_x=[0, 20], range_y=[2.25, 4.75])
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig.update_layout(showlegend=False,title_x=0.5, title='ABV vs. Average Rating Over Time', xaxis_title='ABV', yaxis_title='Average Rating')

        # Make the background and the plot in general transparent
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        
        # Save the plot
        fig.write_html(f'{self.save_folder}/abv_ratings.html')
        
        # Display the plot
        fig.update_layout(width=800, height=600, title_x=0.5)
        fig.update_layout({'plot_bgcolor': 'rgb(255,255,255)', 'paper_bgcolor': 'rgb(255,255,255)'})
        fig.show()
        
        # Save the fallback plot
        fig.write_html('docs/notebook_fallback/abv_ratings.html')

        return beer_ratings
    
    def plot_corr_abv_ratings(self, beer_ratings):
        # Compute the linear correlation between abv and rating for each year
        correlation = []
        for year in sorted(beer_ratings['year'].unique()):
            filtered = beer_ratings[beer_ratings['year'] == year]
            corr = filtered[['abv', 'rating']].corr().iloc[0, 1]
            correlation.append(corr)
        # Plot the correlation 
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sorted(beer_ratings['year'].unique()), y=correlation, mode='lines+markers'))
        fig.update_layout(title='Correlation between ABV and Rating over time', xaxis_title='Year', yaxis_title='Correlation', height=600, width=800, title_x=0.5)
        fig.update_layout({'plot_bgcolor': 'rgb(255,255,255)', 'paper_bgcolor': 'rgb(255,255,255)'})
        fig.show()

        fig.write_html(f'docs/notebook_fallback/corr_abv_ratings.html')
    
    def plot_abv_evolution_map(self):
        # Create the variables
        row_no_US = []
        row_US = []

        # Iterate over the years
        for year in self.df_ratings_no_text['date'].dt.year.unique():
            df_state_US = self.df_ratings_no_text[(self.df_ratings_no_text['date'].dt.year == year) & (self.df_ratings_no_text['country_user'] == 'United States')].groupby('state_user').agg({'abv': 'mean'}).reset_index()
            row_US += [{'year': year, 'location': state, 'avg_abv': abv} for state, abv in zip(df_state_US['state_user'], df_state_US['abv'])]

            df_state_no_US = self.df_ratings_no_text[(self.df_ratings_no_text['date'].dt.year == year) & (self.df_ratings_no_text['country_user'] != 'United States')].groupby('country_user').agg({'abv': 'mean'}).reset_index()
            row_no_US += [{'year': year, 'location': state, 'avg_abv': abv} for state, abv in zip(df_state_no_US['country_user'], df_state_no_US['abv'])]
        df_states_no_US = pd.DataFrame(row_no_US)
        df_states_US = pd.DataFrame(row_US)

        # Filter the data
        nbr_years_considered = df_states_no_US.groupby('location').agg({'year': 'count'}).reset_index()
        nbr_years_considered = nbr_years_considered[nbr_years_considered['year'] == nbr_years_considered['year'].max()]
        df_states_no_US = df_states_no_US[df_states_no_US['location'].isin(nbr_years_considered['location'])]

        # Filter the data
        nbr_years_considered = df_states_US.groupby('location').agg({'year': 'count'}).reset_index()
        nbr_years_considered = nbr_years_considered[nbr_years_considered['year'] == nbr_years_considered['year'].max()]
        df_states_US = df_states_US[df_states_US['location'].isin(nbr_years_considered['location'])]

        # Define the options
        options = {
            'title': 'Average ABV by users country over the years',
            'time_range': range(self.df_ratings_no_text['date'].dt.year.min(), self.df_ratings_no_text['date'].dt.year.max() + 1),
            'time_label': 'year',
            'location_label': 'location',
            'value_label': 'avg_abv',
            'range_color': [4, 8],
            'color_scale': 'Viridis'
        }
        # Display the plot
        plot_map_time(df_states_no_US, df_states_US, options, self.save_folder + '/abv_evolution_map.html', 'abv_evolution_map', is_bg_white=False)
    
    def plot_abv_evolution(self):
        # Compute the metrics
        avg_abv = self.df_ratings_no_text.groupby(self.df_ratings_no_text['date'].dt.year).agg({'abv': 'mean'}).reset_index().rename(columns={'date': 'year'})

        # Plot the data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=avg_abv['year'], y=avg_abv['abv'], mode='lines+markers'))
        fig.update_layout(title='Average ABV over time', xaxis_title='Year', yaxis_title='ABV',title_x=0.5)
        
        # Set the background color to transparent
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        fig.write_html(f'{self.save_folder}/abv_evolution.html')
        
        # Set the background color to white
        fig.update_layout({'plot_bgcolor': 'rgb(255,255,255)', 'paper_bgcolor': 'rgb(255,255,255)'}, width=800, height=600)     
        fig.show()

        fig.write_html('docs/notebook_fallback/abv_evolution.html')