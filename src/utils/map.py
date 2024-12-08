import plotly.graph_objects as go

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
    "Wisconsin": "WI", "Wyoming": "WY"
}


def plot_map(df_no_US, df_US, options, save_path=None):
    # Initialize figure
    fig = go.Figure()

    # Ratings
    counter = 0
    for counter in range(len(options['plots'])):
        plot = options['plots'][counter]
        dfNoUS = df_no_US[counter] if len(options['plots']) > 1 else df_no_US
        fig.add_trace(go.Choropleth(
            locations=dfNoUS[plot['location_label']],
            locationmode="country names",
            z=dfNoUS[plot['z_label']],
            colorscale=plot['colorscale'],
            showscale=False,  # Suppress legend for countries
            hovertemplate="<b>%{location}</b><br>Count: %{z}<extra></extra>",  # Customized hover
            visible=counter == 0
        ))
        dfUS = df_US[counter] if len(options['plots']) > 1 else df_US    
        dfUS[plot['location_label']] = dfUS[plot['location_label']].map(us_remapping)
        minZ = min(dfUS[plot['z_label']].min(), dfNoUS[plot['z_label']].min())
        maxZ = max(dfUS[plot['z_label']].max(), dfNoUS[plot['z_label']].max())
        fig.add_trace(go.Choropleth(
            locations=dfUS[plot['location_label']],
            locationmode="USA-states",
            z=dfUS[plot['z_label']],
            colorscale=plot['colorscale'],
            zmin=minZ,  # Set min value for colorbar
            zmax=maxZ,  # Set max value for colorbar
            colorbar=dict(title="Scale", tickformat=".1s", len=1),
            hovertemplate="<b>%{location}</b><br>Count: %{z}<extra></extra>",  # Customized hover
            visible=counter == 0
        ))

    # Dropdown menu
    if len(options['plots']) > 1:
        buttons = []
        for counter in range(len(options['plots'])):
            buttons.append(dict(
                args=[{"visible": [False, False] * counter + [True, True] + [False, False] * (len(options['plots']) - counter - 1)}],
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
        title=options["title"],
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular"
        ),
        height=600,
        width=800
    )

    # Show the plot
    fig.show()

    # Save the plot
    if save_path:
        fig.write_html(save_path)