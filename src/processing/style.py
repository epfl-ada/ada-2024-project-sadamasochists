# Import necessary libraries
import plotly.express as px
import os
import plotly.graph_objects as go
import pandas as pd

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
        fig.update_layout(autosize=True)
        fig.write_html(f"{self.save_folder}/styles_pie_chart.html")
        
        # Prepare the plot for saving
        fig.update_layout(height=600, width=800, autosize=False)
        fig.show()
        
    def favourite_beer_style_country(self):
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
            title_text="Countries and Their Preferred Beer Styles",
            font_size=12,
            title_font_size=18,
            title_font_color="darkblue",
            title_x=0.5,
            height=900,
            width=1000,
            plot_bgcolor="rgba(240, 240, 240, 0.9)",
        )

        # Save the plot to an HTML file
        #fig.write_html("docs/plots/beer_styles_chord_diagram.html")

        # Show the plot
        fig.show()