import plotly.graph_objects as go

def plots_values_over_time(items, time_label, value_label, xaxis_title, yaxis_title, title, filename=None):
    fig = go.Figure()
    for state, elem in items.items():
        fig.add_trace(go.Scatter(x=elem[time_label], y=elem[value_label], mode='lines+markers', name=state, marker=dict(size=4)))
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        xaxis=dict(tickmode='linear', tick0=2002, dtick=2),
        height=600,
        width=800,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig.show()

    if filename:
        fig.update_layout(autosize=True, height=None, width=None, title=None)
        fig.write_html(filename)