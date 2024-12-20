# Import necessary libraries
import plotly.express as px
import os
import plotly.graph_objects as go
import pandas as pd
import bar_chart_race as bcr

# Define the class StyleAnalysis
class StyleAnalysis:
    def __init__(self, df_beers, df_breweries, df_users, df_ratings_no_text, save_folder):
        self.df_beers = df_beers
        self.df_breweries = df_breweries
        self.df_users = df_users
        self.df_ratings_no_text = df_ratings_no_text
        self.save_folder = save_folder
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
            
    def plot_pie_chart(self):
        # Choose the number of elements to display
        number_of_elements_displayed = 19

        # Do the styling computations
        styles_counted = self.df_ratings_no_text['style'].value_counts().reset_index()
        top_styles = styles_counted.head(number_of_elements_displayed).copy()
        top_styles.loc[len(top_styles)] = {'style': 'Other', 'count': styles_counted['count'][number_of_elements_displayed:].sum()}

        # Display a pie chart with gradient colors
        fig = px.pie(top_styles, values='count', names='style', title='Distribution of the styles of beers', color_discrete_sequence=px.colors.sequential.Viridis, hole=0.6)
        fig.update_traces(textinfo='label+percent', textfont_size=14)
        
        # Prepare the plot for saving
        fig.update_layout(height=600, width=800, autosize=False, title_x=0.5)
        fig.show()

        # Set the background as (245, 245, 245)
        fig.update_layout(plot_bgcolor='rgb(255, 255, 255)', paper_bgcolor='rgb(255, 255, 255)')
        fig.update_layout(autosize=True, width=None, height=None)
        fig.write_html(f"{self.save_folder}/styles_pie_chart.html")

        fig.write_html(f"docs/notebook_fallback/styles_pie_chart.html")

    def plot_favourite_beer_style_country(self):
        # Find the countries style preferences
        countries_style_preferences = {}
        unique_styles = set()
        for country in self.df_ratings_no_text['country_user'].unique():
            # Filter the data
            df_country = self.df_ratings_no_text[self.df_ratings_no_text['country_user'] == country]
            
            # Compute the style preferences
            style_preferences = df_country['style'].value_counts().reset_index().head(1).iloc[0]['style']

            # Add into countries_style_preferences the data
            countries_style_preferences[country] = style_preferences
            unique_styles.add(style_preferences)

        # Prepare data for the chord diagram
        countries = list(countries_style_preferences.keys())
        styles = list(unique_styles)

        # Combine countries and styles for all_nodes
        all_nodes = countries + styles
        node_indices = {node: idx for idx, node in enumerate(all_nodes)}

        # Create the source and target lists for the chord diagram
        sources = []
        targets = []
        values = []

        for country, style in countries_style_preferences.items():
            sources.append(node_indices[country])
            targets.append(node_indices[style])
            values.append(1)  # Set weight for each connection

        # Create a color palette for nodes
        num_countries = len(countries)
        num_styles = len(styles)
        colors = [f"rgba(0, 128, 255, 0.8)" for _ in range(num_countries)] + [f"rgba(255, 128, 0, 0.8)" for _ in range(num_styles)]

        # Assign unique colors to each cluster of connections
        link_colors = []
        style_color_map = {style: f"rgba({max(0, 255 - i * 30)}, {min(255, 100 + i * 30)}, {min(255, 150 + i * 20)}, 0.6)" for i, style in enumerate(styles)}
        for source, target in zip(sources, targets):
            link_colors.append(style_color_map[all_nodes[target]])

        # Create the chord diagram using Plotly
        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=20,
                        thickness=30,
                        line=dict(color="black", width=1),
                        label=all_nodes,
                        color=colors,
                    ),
                    link=dict(
                        source=sources,  # Indices of source nodes
                        target=targets,  # Indices of target nodes
                        value=values,    # Values for connections
                        color=link_colors,
                        hovertemplate='%{source.label} → %{target.label}<extra></extra>',
                    ),
                )
            ]
        )

        # Update layout for better visualization
        fig.update_layout(
            title_text="User Countries and Their Preferred Beer Styles",
            font_size=12,
            title_font_size=18,
            title_x=0.5,
            height=1020,
            width=800,
        )

        # Show the plot
        fig.show()

        # Set autosize to True
        fig.update_layout(autosize=True,width=None, height=None)
        fig.write_html(f"{self.save_folder}/favourite_beer_style_country.html")

        fig.write_html(f"docs/notebook_fallback/favourite_beer_style_country.html")
        
    def plot_abv_style_evolution(self):
        # Create a dataframe with the top_10_styles_list elements as columns
        row = []
        for year in sorted(self.df_ratings_no_text['date'].dt.year.unique()):
            # Get the data for the year
            df_year = self.df_ratings_no_text[self.df_ratings_no_text['date'].dt.year == year]

            # Compute the style preferences
            style_preferences = df_year['style'].value_counts().reset_index().head(10)

            # Compute the ABV for the top 10 styles
            for style in style_preferences['style'].values:
                # Get the data
                df_style = df_year[df_year['style'] == style]

                # Compute the average ABV
                avg_abv = df_style['abv'].mean()

                # Append the data
                row.append({'year': year, 'style': style, 'avg_abv': avg_abv, 'count': style_preferences[style_preferences['style'] == style]['count'].values[0]})

        # Create the dataframe
        df_style_avg_abv = pd.DataFrame(row)

        # Create the plot with the slider for the years
        fig = px.bar(df_style_avg_abv, x='style', y='count', animation_frame='year', title='Top 10 styles over the years', range_y=[0, 100000], color='avg_abv', range_color=[0, 10], color_continuous_scale='Blues')

        # Set the width and the height
        fig.update_layout(height=600, width=800, title_x=0.5)

        # Use log scale for the y-axis
        fig.update_xaxes(title_text='Style')
        fig.update_yaxes(title_text='Number of ratings')

        fig.show()

        fig.write_html(f"docs/notebook_fallback/abv_style_evolution.html")
        
    def plot_style_race(self):
        # Prepare the data
        all_styles = self.df_ratings_no_text['style'].unique()

        # Create a dataframe with the top_10_styles_list elements as columns
        nbr_ratings_per_style = pd.DataFrame(columns=['year'] + all_styles)
        for year in sorted(self.df_ratings_no_text['date'].dt.year.unique()):
            # Get the data for the year
            df_year = self.df_ratings_no_text[self.df_ratings_no_text['date'].dt.year <= year]

            # Compute the number of ratings per style
            styles_counted = df_year['style'].value_counts().reset_index()

            # Create the dictionary
            row = {style: count for style, count in zip(styles_counted['style'], styles_counted['count'])}
            row['year'] = year

            # Add the row to the dataframe
            nbr_ratings_per_style = pd.concat([nbr_ratings_per_style, pd.DataFrame([row])])

        # Fill the missing values and set the index
        nbr_ratings_per_style = nbr_ratings_per_style.fillna(0).set_index('year')

        # Set to integer the types
        nbr_ratings_per_style = nbr_ratings_per_style.astype(int)

        # Display the race plot     
        return bcr.bar_chart_race(
            nbr_ratings_per_style,
            period_length=1000,
            title='Total number of ratings per beer style',
            n_bars=10,
            steps_per_period=50,
            cmap='tab20',
            period_fmt='Year: {x}',
            bar_kwargs={'alpha': 0.8},
            filename=f"{self.save_folder}/race_video.mp4"
        )