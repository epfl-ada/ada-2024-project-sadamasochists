import numpy as np
import plotly.graph_objects as go

def plot_correlation_matrix(df, cmap=['pink', 'red'], filename=None):
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
            hoverinfo="text",  # Show custom hover text
            colorscale=cmap,  # Use the two-color scale
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
                font=dict(color="black", size=10)
            )
        )

    fig.update_layout(
        title="Correlation Matrix",
        xaxis=dict(tickangle=45),
        yaxis=dict(tickmode='linear'),
        annotations=annotations,
        autosize=True
    )

    # Save as HTML if a filename is provided
    if filename:
        fig.write_html(filename)

    # Show the plot
    fig.show()
