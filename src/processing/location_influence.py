from pyvis.network import Network
from src.utils.locationinfluence_utils import get_base64_flag, get_png
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from pyvis.network import Network
from src.utils.locationinfluence_utils import get_base64_flag, get_png
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class LocationInfluence():
    def __init__(self, df_ratings_no_text, save_folder):    
        # Set some variables
        plotFrom = 'country_user'
        plotTo = 'country_brewery'

        # Count the frequencies of location_user -> location_brewery
        freq = df_ratings_no_text[df_ratings_no_text[plotFrom] != df_ratings_no_text[plotTo]].groupby(
            [plotFrom, plotTo]
        ).size().reset_index(name='count')

        # Find the most frequent location_brewery for each location_user
        most_frequent = freq.loc[
            freq.groupby(plotFrom)['count'].idxmax()
        ]

        # Create the directed graph
        self.G = nx.DiGraph()

        for _, row in most_frequent.iterrows():
            self.G.add_edge(row[plotFrom], row[plotTo], weight=row['count'])
        
        self.in_degrees = dict(self.G.in_degree())

        self.save_folder = save_folder

        self.plot_location()

    def print_in_degrees(self):
        # Plot the in-degrees in the map
        fig = go.Figure(go.Choropleth(
            locations=list(self.in_degrees.keys()),
            z=list(self.in_degrees.values()),
            locationmode='country names',
            colorscale='Blues',
            colorbar_title='In-Degree',
        ))

        fig.update_layout(
            title_text='In-Degree of Location Influence',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            autosize=True,
        )
        
        fig.update_layout(height=600, width=800, title_x=0.5)

        fig.show()
        
    def plot_location(self):        
        if self.G.number_of_edges() == 0:
            print("The graph is empty and has no edges to visualize.")
        else:
            # Create PyVis network
            net = Network(height="620px", width="100%", directed=True, bgcolor="#f5f5f5", font_color="black")
            
            # Add nodes with size proportional to their in-degree
            max_in_degree = max(self.in_degrees.values()) if self.in_degrees else 1

            for node in self.G.nodes():
                size = 20 + 30 * (self.in_degrees[node] / max_in_degree)  # Scale size between 10 and 30
                net.add_node(node, shape="image", image=get_base64_flag(node), size=size, title=node, label="")

            # Add edges in visualization
            for edge in self.G.edges(data=True):
                # Make loops curve instead of overlap
                if self.G.has_edge(edge[1], edge[0]):
                    # Ensure one edge is clockwise and the other counterclockwise
                    if (edge[0], edge[1]) in self.G.edges:
                        curvature = {"type": "curvedCW"}
                    else:
                        curvature = {"type": "curvedCCW"}
                else:
                    curvature = False 

                net.add_edge(
                    edge[0],
                    edge[1],
                    width=2,
                    smooth=curvature
                )

            net.set_options("""
            var options = {
            "nodes": {
                "shape": "dot",
                "scaling": {
                "min": 10,
                "max": 30
                },
                "font": {
                "size": 0,
                "face": "Tahoma"
                }
            },
            "edges": {
                "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 1
                }
                },
                "scaling": {
                "min": 1,
                "max": 15
                },
                "color": {
                "inherit": true
                },
                "smooth": {
                "enabled": true
                }
            },
            "interaction": {
                "dragNodes": true,
                "hideEdgesOnDrag": false,
                "hideNodesOnDrag": false,
                "tooltipDelay": 0,
                "hover": true
            },
            "physics": {
                "enabled": true,
                "barnesHut": {
                "gravitationalConstant": -20000,
                "centralGravity": 0.1,
                "springLength": 110,
                "springConstant": 0.05
                },
                "stabilization": {
                "enabled": true
                }
                }
            }
            """)
            
            # Generate the interactive visualization
            path = f"{self.save_folder}/location_influence.html"

            # Set the background to transparent
            net.write_html(path, open_browser=False)
            
class MostLeastPlot():
    def __init__(self, df_ratings_no_text, save_folder):
        # Define some instance variables
        plotPer = 'country_user'
        inequal = 'country_brewery'
        toPlot = 'rating'
        minThresh = 100
        self.save_folder = save_folder

        # Create a new column to indicate whether the rating is domestic or foreign
        df_ratings_no_text["rating_type"] = (
            df_ratings_no_text[plotPer] == df_ratings_no_text[inequal]
        ).map({True: "domestic", False: "foreign"})
        
        # First, select only countries with at least 100 domestic and foreign reviews.
        counts = df_ratings_no_text.groupby([plotPer, "rating_type"]).size().reset_index(name="count")
        counts_pivot = counts.pivot(index=plotPer, columns="rating_type", values="count").fillna(0)
        valid_countries = counts_pivot[(counts_pivot.get("domestic", 0) >= minThresh) & (counts_pivot.get("foreign", 0) >= minThresh)].index

        # Filter the original dataframe to retain only valid countries
        df_ratings_no_text = df_ratings_no_text[df_ratings_no_text[plotPer].isin(valid_countries)]
        self.average_ratings = (
            df_ratings_no_text.groupby([plotPer, "rating_type"])
            .agg(average_rating=(toPlot, "mean"), review_count=(plotPer, "size"))
            .reset_index()
        )

        self.average_ratings.rename(columns={plotPer: "country", toPlot: "average_rating"}, inplace=True)
        
    # Updated function to add flag images beside the bars
    def add_flag_images(self, ax, countries, x_positions, y_positions, offset=0.1):
        # Flags are from the following GitHub repository:
        # https://github.com/HatScripts/circle-flags
        for country, x, y in zip(countries, x_positions, y_positions):
            if country == "":
                continue
            img_path = get_png(country)  # Use local paths
            try:
                img = np.array(Image.open(img_path))
                imagebox = OffsetImage(img, zoom=0.15)
                # Adjust the position based on the bar's sign
                adjusted_x = x + offset if x > 0 else x - offset
                ab = AnnotationBbox(imagebox, (adjusted_x, y), frameon=False, box_alignment=(0.5, 0.5))
                ax.add_artist(ab)
            except Exception as e:
                print(f"Error loading flag for {country}: {e}")
                print("img_path:" + img_path)
        
    def plot(self, n=10):
        # Pivot the DataFrame to get separate columns for domestic and foreign ratings
        pivoted_df = self.average_ratings.pivot(index="country", columns="rating_type", values="average_rating").reset_index()

        # Calculate the deviation between domestic and foreign ratings
        pivoted_df["deviation"] = pivoted_df["foreign"] - pivoted_df["domestic"]

        # Sort the DataFrame by deviation
        largest_positive_deviation = pivoted_df.nlargest(n, "deviation")
        largest_negative_deviation = pivoted_df.nsmallest(n, "deviation")
        
        largest_negative_deviation["type"] = "Negative"
        largest_positive_deviation["type"] = "Positive"
        largest_negative_deviation = largest_negative_deviation.iloc[::-1]
        
        # Add empty row inbetween
        gap_row = pd.DataFrame({
            "country": [""],
            "deviation": [0],
            "type": ["Positive"],
            "domestic": [True],
            "foreign": [True]
        })

        combined_with_gap = pd.concat([largest_positive_deviation, gap_row, largest_negative_deviation], ignore_index=True)

        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot positive deviations in blue
        positive_data = combined_with_gap[combined_with_gap["type"] == "Positive"]
        ax.barh(positive_data["country"], positive_data["deviation"], color="blue", edgecolor="black", label="Positive Deviation")

        # For negative: assign colors based on whether < 0 or > 0
        negative_data = combined_with_gap[combined_with_gap["type"] == "Negative"]
        colors = negative_data["deviation"].apply(lambda x: "red" if x < 0 else "blue")
        ax.barh(negative_data["country"], negative_data["deviation"], color=colors, edgecolor="black", label="Deviation")

        # Add a dashed horizontal line
        separation_index = len(positive_data) - 1 # -1 for the gap row
        ax.axhline(y=separation_index, color="black", linestyle="--", linewidth=1)

        # Add a dashed vertical line at zero
        ax.axvline(0, color="black", linewidth=1.2, linestyle="--")

        # Add flags
        labels = combined_with_gap["country"].tolist()
        deviations = combined_with_gap["deviation"].tolist()
        self.add_flag_images(ax, labels, deviations, range(len(labels)), offset=0.03)

        ax.set_xlabel("Preference for foreign beers (given in deviation in mean rating)")
        ax.set_title("Top {} countries with the highest and lowest preference for foreign beers".format(n))

        # Adjust y-axis labels and invert for proper horizontal bar alignment
        ax.set_yticks(range(len(combined_with_gap)))
        ax.set_yticklabels(combined_with_gap["country"])
        ax.invert_yaxis()

        # Set X and Y axis with a bit of a gap to allow for the flags
        # And color the chart red/blue
        min_deviation = min(deviations)
        max_deviation = max(deviations)
        scale = max(abs(min_deviation), max_deviation)
        min_point = min(min_deviation, 0)
        plt.xlim(min_point - 0.15 * scale, max_deviation + 0.15 * scale)

        y_min, y_max = ax.get_ylim()
        ax.set_ylim(y_min - 0.5, y_max + 0.5)

        x_min, x_max = ax.get_xlim()

        # Shade areas above and below the separation line
        ax.fill_betweenx(
            [separation_index, y_max + 0.5],
            x1=x_min,
            x2=x_max,
            color="lightblue",
            alpha=0.2,
        )
        ax.fill_betweenx(
            [y_min - 0.5, separation_index],
            x1=x_min,
            x2=x_max,
            color="lightcoral",
            alpha=0.2,
        )
        
        ax.xaxis.set_major_locator(plt.MultipleLocator(0.1))  # Adjust step size for granularity
        ax.xaxis.grid(True, linestyle="--", alpha=0.5)

        fig.patch.set_facecolor((245/255, 245/255, 245/255))  # Set background color to rgb(245,245,245)
        # Adjust layout
        plt.tight_layout()
        plt.savefig(f"{self.save_folder}/preferences.png")
        plt.show()
