# Import necessary libraries
import plotly.graph_objects as go
import plotly.express as px
import os

# Define the US remapping
us_remapping = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "Washington DC": "DC"
}
us_remapping_inverse = {v: k for k, v in us_remapping.items()}

# Define the map to plot the data
def plot_map(df_no_US, df_US, options, save_dir, save_prefix, fallback_title, is_bg_white=True):
    # Initialize figure
    fig = go.Figure()

    # Ratings
    counter = 0
    for counter in range(len(options['plots'])):
        # Create a new figure for each plot
        newFig = go.Figure()

        # Add the data to the figure
        plot = options['plots'][counter]
        
        # Do the plotting for non-US countries
        dfNoUS = df_no_US[counter] if len(options['plots']) > 1 else df_no_US
        goMapNoUS = go.Choropleth(
            locations=dfNoUS[plot['location_label']],
            locationmode="country names",
            z=dfNoUS[plot['z_label']],
            colorscale=plot['colorscale'],
            showscale=False,  # Suppress legend for countries
            hovertemplate="<b>%{location}</b><br>Count: %{z}<extra></extra>",  # Customized hover
        )
        
        # Do the plotting for US states
        dfUS = df_US[counter] if len(options['plots']) > 1 else df_US    
        minZ = min(dfUS[plot['z_label']].min(), dfNoUS[plot['z_label']].min())
        maxZ = max(dfUS[plot['z_label']].max(), dfNoUS[plot['z_label']].max())
        goMapUs = go.Choropleth(
            locations=dfUS[plot['location_label']].map(us_remapping),
            locationmode="USA-states",
            z=dfUS[plot['z_label']],
            colorscale=plot['colorscale'],
            zmin=minZ,  # Set min value for colorbar
            zmax=maxZ,  # Set max value for colorbar
            colorbar=dict(title="Scale", len=1),
            hovertemplate="<b>%{location}</b><br>Count: %{z}<extra></extra>",  # Customized hover
        )

        # Append the traces to the new figure
        newFig.add_traces([goMapNoUS, goMapUs])

        # Appent the traces to the main figure but set all but the first plot to invisible
        goMapNoUS.visible = counter == 0
        goMapUs.visible = counter == 0
        fig.add_traces([goMapNoUS, goMapUs])
        fig.update_layout(title_text=plot['label'])

        # Create the directory if it does not exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Define some visualization options
        newFig.update_layout(
            title_text=plot['label'],
            title_x=0.5,  # Center the title
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection=dict(type="equirectangular"),  # Correct usage
                bgcolor="rgb(255, 255, 255)" if is_bg_white else "rgb(245, 245, 245)"
            ),
        )

        # Make the background transparent
        newFig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

        # Save the plot
        prepare_label = lambda label: label.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(",", "")
        newFig.write_html(f"{save_dir}/{save_prefix}_{prepare_label(plot['label'])}.html")

    # Dropdown menu
    if len(options['plots']) > 1:
        buttons = []
        for counter in range(len(options['plots'])):
            buttons.append(dict(
                args=[{"visible": [False, False] * counter + [True, True] + [False, False] * (len(options['plots']) - counter - 1)}, {"title": options['plots'][counter]['label']}],
                label=options['plots'][counter]['label'],
                method="update"
            ))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=buttons,
                    direction="down",
                    x=0.1,
                    y=1,  # Dropdown below title
                    xanchor="left",
                    yanchor="top"
                )
            ]
        )
    
    # Update general layout
    fig.update_layout(
        title_text=options['plots'][0]['label'],
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular"
        ),
        height=600,
        width=800,
        title_x=0.5
    )

    # Show the plot
    fig.show()

    # Save the fallback plot
    fig.write_html(f"docs/notebook_fallback/{fallback_title}.html")


def plot_map_time(df_no_US, df_US, options, save_path, fallback_title, is_bg_white=True):
    df_US_copy = df_US.copy()
    df_US_copy[options['location_label']] = df_US_copy[options['location_label']].map(us_remapping)

    # Create frames for the animation
    frames = [
        {
            "data": [
                go.Choropleth(
                    locations=df_no_US[df_no_US[options['time_label']] == year][options['location_label']],
                    locationmode='country names',
                    z=df_no_US[df_no_US[options['time_label']] == year][options['value_label']],
                    colorscale=options['color_scale'],
                    zmin=options['range_color'][0],
                    zmax=options['range_color'][1]
                ),
                go.Choropleth(
                    locations=df_US_copy[df_US_copy[options['time_label']] == year][options['location_label']],
                    locationmode='USA-states',
                    z=df_US_copy[df_US_copy[options['time_label']] == year][options['value_label']],
                    colorscale=options['color_scale'],
                    zmin=options['range_color'][0],
                    zmax=options['range_color'][1]
                )
            ],
            "name": str(year),
        }
        for year in options['time_range']
    ]

    # Create a figure
    fig = go.Figure()

    # Define the figure with animation
    fig.add_trace(
        go.Choropleth(
            locations=df_no_US[df_no_US[options['time_label']] == df_no_US[options['time_label']].min()][options['location_label']],
            locationmode='country names',
            z=df_no_US[df_no_US[options['time_label']] == df_no_US[options['time_label']].min()][options['value_label']],
            colorscale=options['color_scale'],
            zmin=options['range_color'][0],
            zmax=options['range_color'][1]
    ))
    fig.add_trace(
        go.Choropleth(
            locations=df_US_copy[df_US_copy[options['time_label']] == df_US_copy[options['time_label']].min()][options['location_label']],
            locationmode='USA-states',
            z=df_US_copy[df_US_copy[options['time_label']] == df_US_copy[options['time_label']].min()][options['value_label']],
            colorscale=options['color_scale'],
            zmin=options['range_color'][0],
            zmax=options['range_color'][1]
        )
    )

    fig.frames = frames

    # Add slider to the layout
    fig.update_layout(
        sliders=[{
            "steps": [
                {"args": [[str(year)], {"frame": {"duration": 300, "redraw": True}, "mode": "immediate"}],
                "label": str(year), "method": "animate"}
                for year in options['time_range']
            ],
            "transition": {"duration": 300},
            "x": 0.1,
            "xanchor": "left",
            "y": 0,
            "yanchor": "top"
        }],
        updatemenus=[{
            "buttons": [
                {"args": [None, {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True}],
                "label": "Play", "method": "animate"},
                {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                "label": "Pause", "method": "animate"}
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }]
    )

    # Update the layout
    fig.update_layout(
        title_text=options['title'] if 'title' in options else None,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular"
        ),
        geo_scope='world',
        height=600,
        width=800,
        title_x=0.5
    )

    fig.show()
    
    # Update the background color
    fig.update_layout(
        geo=dict(
            bgcolor="rgb(255, 255, 255)" if is_bg_white else "rgb(245, 245, 245)",
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular"
        ),
    )

    # Set the background as transparent and set the sea color to #f5f5f5
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    

    fig.update_layout(width=None, height=None, autosize=True)
    fig.write_html(save_path)

    # Save the fallback plot
    fig.write_html(f"docs/notebook_fallback/{fallback_title}.html")