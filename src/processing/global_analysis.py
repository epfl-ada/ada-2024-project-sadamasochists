# Do all the importings
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import os
import pandas as pd
from scipy.stats import skew, kurtosis, normaltest
from great_tables import GT
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from src.utils.plots import plot_map, plot_map_time

# Define the class
class GlobalAnalysis:
    def __init__(self, df_beers, df_breweries, df_users, df_ratings_no_text, save_folder):
        self.df_users = df_users
        self.df_breweries = df_breweries
        self.df_beers = df_beers
        self.df_ratings_no_text = df_ratings_no_text
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        self.save_folder = save_folder

    def display_ratings_distribution(self):
        # Select the rating elements
        df_ratings_only_ratings = self.df_ratings_no_text[['mouthfeel','taste','appearance','aroma','overall', 'rating']]

        # Create a figure to save and one to display
        fig = make_subplots(rows=2, cols=3, subplot_titles=('Mouthfeel', 'Taste', 'Appearance', 'Aroma', 'Overall', 'Rating'))
        fig_display = make_subplots(rows=2, cols=3, subplot_titles=('Mouthfeel', 'Taste', 'Appearance', 'Aroma', 'Overall', 'Rating'))

        # Create the histograms
        for i, column in enumerate(df_ratings_only_ratings.columns):
            value_counts = df_ratings_only_ratings[column].value_counts().sort_index()
            fig.add_trace(go.Bar(x=value_counts.index, y=value_counts.values, name=column), row=(i//3)+1, col=(i%3)+1)
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
            fig_display.add_trace(go.Bar(x=value_counts.index, y=value_counts.values, name=column), row=(i//3)+1, col=(i%3)+1)
            fig_display.update_layout({'plot_bgcolor': 'rgb(255,255,255)', 'paper_bgcolor': 'rgb(255,255,255)'})

        
        # Add the title
        fig.update_layout(title_text='Ratings Distribution')
        
        # Save the figure
        fig.write_html(f'{self.save_folder}/raw_ratings_distribution.html')

        # Set the size to 800x800
        fig_display.update_layout(width=1000, height=600, title_text='Ratings Distribution')

        # Display the figure
        fig_display.show()
    
    def display_ratings_statistics(self):
        # Select the rating elements
        df_ratings_only_ratings = self.df_ratings_no_text[['mouthfeel','taste','appearance','aroma','overall', 'rating']]

        # Get the analysis
        mean = df_ratings_only_ratings.mean().round(2)
        std = df_ratings_only_ratings.std().round(2)
        median = df_ratings_only_ratings.median().round(2)
        skewness = df_ratings_only_ratings.apply(skew).round(2)
        kurtosis_result = df_ratings_only_ratings.apply(kurtosis).round(2)
        normaltest_results = df_ratings_only_ratings.apply(lambda x: normaltest(x).pvalue)

        # Wrap the results into a dataframe
        df_results = pd.DataFrame({
            'Mean': mean,
            'Std': std,
            'Median': median,
            'Skewness': skewness,
            'Kurtosis': kurtosis_result,
            'Can reject H0 (95%)': normaltest_results < 0.05
        }, index=df_ratings_only_ratings.columns).reset_index().rename(columns={'index': 'Rating'})

        # Show the results
        (
            GT(df_results)
            .tab_header(title='Statistics of the ratings')
        ).show()

    def plot_correlation_matrix(self):
        df = self.df_ratings_no_text[['mouthfeel','taste','appearance','aroma','overall','abv']]
        corr = df.corr()

        # Mask the upper triangle and flatten to remove blanks
        mask = np.triu(np.ones_like(corr, dtype=bool))
        lower_triangle_corr = corr.where(~mask)  # Keep only the lower triangle

        # Extract the lower triangle values and the corresponding labels
        lower_triangle_corr = lower_triangle_corr.stack()
        labels_x = lower_triangle_corr.index.get_level_values(1)
        labels_y = lower_triangle_corr.index.get_level_values(0)
        values = lower_triangle_corr.values

        # Determine the dynamic color scale range
        z_min, z_max = values.min(), values.max()

        # Create a heatmap with only the lower triangle
        fig = go.Figure(
            data=go.Heatmap(
                z=values,
                x=labels_x,
                y=labels_y,
                text=[f"{x} vs {y}: {val:.2f}" for x, y, val in zip(labels_x, labels_y, values)],
                hoverinfo="text",  
                colorscale=['pink','red'],  # Set the color scale
                zmin=z_min,  # Set minimum value for color scale
                zmax=z_max,  # Set maximum value for color scale
                showscale=True
            )
        )

        # Add annotations for the correlation values
        annotations = []
        for x, y, val in zip(labels_x, labels_y, values):
            annotations.append(
                dict(
                    x=x,
                    y=y,
                    text=f"{val:.2f}",
                    showarrow=False,
                    font=dict(color="black", size=14),
                )
            )

        fig.update_layout(
            xaxis=dict(
                tickfont=dict(size=14),
            ),
            yaxis=dict(
                tickfont=dict(size=14),
                tickmode='linear'
            ),
            annotations=annotations,
            autosize=True,
            plot_bgcolor='white',  # Set the plot background color to white
            paper_bgcolor='white'  # Set the paper background color to white
        )

        # Set the background color as transparent
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'}, title_text='Correlation Matrix')
        fig.write_html(self.save_folder + "correlation_matrix.html")

        # Revert the background color to white
        fig.update_layout({'plot_bgcolor': 'white', 'paper_bgcolor': 'white'})

        # Set the size to 800x800
        fig.update_layout(width=800, height=600)

        # Show the plot
        fig.show()

    def regression_analysis(self, df_ratings_no_text):
        # Define the train / test split
        random_number = np.random.rand(df_ratings_no_text.shape[0])
        df_ratings_regression = df_ratings_no_text.copy()
        df_ratings_regression['is_train'] = random_number < 0.8

        # Define the train and test set
        df_ratings_regression_train = df_ratings_regression.loc[df_ratings_regression['is_train']]
        df_ratings_regression_test = df_ratings_regression.loc[~df_ratings_regression['is_train']]

        # Normalize the data
        scaler = StandardScaler()
        df_ratings_regression_train.loc[:, ['aroma','taste','mouthfeel','appearance']] = scaler.fit_transform(df_ratings_regression_train[['aroma','taste','mouthfeel','appearance']])
        df_ratings_regression_test.loc[:, ['aroma','taste','mouthfeel','appearance']] = scaler.transform(df_ratings_regression_test[['aroma','taste','mouthfeel','appearance']])

        # Get the X and the y
        X_train = df_ratings_regression_train[['aroma','taste','mouthfeel','appearance']]
        y_train = df_ratings_regression_train['overall']
        X_test = df_ratings_regression_test[['aroma','taste','mouthfeel','appearance']]
        y_test = df_ratings_regression_test['overall']

        # Define the model
        model = sm.OLS(y_train, sm.add_constant(X_train))
        results = model.fit()

        # Compute the R^2 and RMSE for the test set
        y_pred = results.predict(sm.add_constant(X_test))
        r_squared = results.rsquared
        rmse = np.sqrt(((y_test - y_pred) ** 2).mean())

        # Return everything
        return results, r_squared, rmse

    def plot_median_mean_ratings_evolution(self):
        # Define the categories (including 'rating')
        columns = ['overall', 'aroma', 'taste', 'appearance', 'mouthfeel', 'rating']

        # Create subplots with 3 rows and 2 columns
        fig = make_subplots(rows=2, cols=3, shared_xaxes=True, vertical_spacing=0.25, subplot_titles=[f'{col}' for col in columns])

        # Initialize dictionaries for mean and median values
        means = {column: [] for column in columns}
        medians = {column: [] for column in columns}
        year_list = sorted(self.df_ratings_no_text['year'].unique())

        # Calculate mean and median for each year and category
        for year in year_list:
            df_year = self.df_ratings_no_text[self.df_ratings_no_text['year'] == year]
            for column in columns:
                means[column].append(df_year[column].mean())
                medians[column].append(df_year[column].median())

        # Add traces for mean and median of each category to respective subplots
        ranges = {
            "overall": [12.25, 14.25],
            "aroma": [5.5, 7.5],
            "taste": [5.5, 7.5],
            "appearance": [2.75, 4.75],
            "mouthfeel": [2.75, 4.75],
            "rating": [2.74, 4.75]
        }
        for i, column in enumerate(columns):
            row = (i // 3) + 1  # Determine the row (1, 2, or 3)
            col = (i % 3) + 1  # Determine the column (1 or 2)
            
            # Add mean trace (in red) with markers (dots) and lines - show legend only for the first mean
            fig.add_trace(go.Scatter(x=year_list, y=means[column], mode='lines+markers', name='Mean', 
                                    line=dict(color='red'), marker=dict(color='red', size=4), showlegend=(i == 0)),
                        row=row, col=col)
            min_y = min(means[column])
            fig.update_yaxes(range=ranges[column], row=row, col=col)
            
            # Add median trace (in blue) with markers (dots) and lines - show legend only for the first median
            if column != 'rating':
                fig.add_trace(go.Scatter(x=year_list, y=medians[column], mode='markers', name='Median', 
                                        line=dict(color='blue'), marker=dict(color='blue', size=6), showlegend=(i == 0)),
                            row=row, col=col)
            else:
                fig.add_trace(go.Scatter(x=year_list, y=medians[column], mode='lines+markers', name='Median', 
                                        line=dict(color='blue'), marker=dict(color='blue', size=4), showlegend=(i == 0)),
                            row=row, col=col)

        # Update layout to set white background and title
        fig.update_layout(
            showlegend=True,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)'
        )

        fig.write_html(self.save_folder + '/mean_median_over_time.html')

        fig.update_layout(
            title='Mean and Median Ratings Over Time',
            xaxis_title='Year',
            yaxis_title='Rating',
            width=1000,
            height=600,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        fig.show()

    def ratings_world_map(self):
        # Compute the average rating per country
        average_rating_no_US = self.df_ratings_no_text[self.df_ratings_no_text['country_brewery'] != 'United States'].groupby('country_brewery')['rating'].mean().reset_index().rename(columns={'country_brewery':'location', 'rating':'count'})
        average_rating_US = self.df_ratings_no_text[self.df_ratings_no_text['country_brewery'] == 'United States'].groupby('state_brewery')['rating'].mean().reset_index().rename(columns={'state_brewery':'location', 'rating':'count'})

        # Plot everything
        options = {
            "title": "Average Ratings by Country and US State",
            "plots": [{
                'label': 'Beers per country',
                'location_label': 'location',
                'z_label': 'count',
                'colorscale': 'Blues'
            }]
        }
        plot_map(average_rating_no_US, average_rating_US, options, self.save_folder, 'world_ratings')

        # Return the data
        return average_rating_no_US, average_rating_US
    
    def ratings_evolution_map(self):
        # Create the variables
        row_US = []
        row_no_US = []

        # Prepare the data
        for year in self.df_ratings_no_text['date'].dt.year.unique():
            df_state_no_US = self.df_ratings_no_text[(self.df_ratings_no_text['date'].dt.year == year) & (self.df_ratings_no_text['country_brewery'] != 'United States')].groupby('country_brewery').agg({'rating': 'mean'}).reset_index()
            row_no_US += [{'year': year, 'location': state, 'count': abv} for state, abv in zip(df_state_no_US['country_brewery'], df_state_no_US['rating'])]

            df_state_US = self.df_ratings_no_text[(self.df_ratings_no_text['date'].dt.year == year) & (self.df_ratings_no_text['country_brewery'] == 'United States')].groupby('state_brewery').agg({'rating': 'mean'}).reset_index()
            row_US += [{'year': year, 'location': state, 'count': abv} for state, abv in zip(df_state_US['state_brewery'], df_state_US['rating'])]

        # Create the dataframes
        df_states_no_US = pd.DataFrame(row_no_US)
        df_states_US = pd.DataFrame(row_US)

        # Filter the data for a more clean plot (No US)
        number_of_years_per_state_no_US = df_states_no_US.groupby('location').size().reset_index().rename(columns={0:'count'})
        number_of_years_per_state_no_US = number_of_years_per_state_no_US[number_of_years_per_state_no_US['count'] == len(self.df_ratings_no_text['date'].dt.year.unique())]
        df_states_no_US = df_states_no_US[df_states_no_US['location'].isin(number_of_years_per_state_no_US['location'])]

        # Filter the data for a more clean plot (US)
        number_of_years_per_state_US = df_states_US.groupby('location').size().reset_index().rename(columns={0:'count'})
        number_of_years_per_state_US = number_of_years_per_state_US[number_of_years_per_state_US['count'] == len(self.df_ratings_no_text['date'].dt.year.unique())]
        df_states_US = df_states_US[df_states_US['location'].isin(number_of_years_per_state_US['location'])]

        # Define the options for the plot
        options = {
            'title': 'Average Ratings by State Over the Years',
            'time_range': range(self.df_ratings_no_text['date'].dt.year.min(), self.df_ratings_no_text['date'].dt.year.max() + 1),
            'time_label': 'year',
            'location_label': 'location',
            'value_label': 'count',
            'range_color': [1, 4],
            'color_scale': 'Viridis'
        }

        # Display the plot
        plot_map_time(df_states_no_US, df_states_US, options, self.save_folder + '/ratings_evolution_map.html', is_bg_white=True)
