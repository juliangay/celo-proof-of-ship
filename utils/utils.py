import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_mock_data(year):
    """Generate mock activity data for the entire year."""
    start_date = datetime(year, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365)]

    # Generate random activity counts with some patterns
    activities = []
    for _ in dates:
        rand = np.random.random()
        if rand < 0.3:
            activities.append(0)
        elif rand < 0.6:
            activities.append(np.random.randint(1, 4))
        elif rand < 0.8:
            activities.append(np.random.randint(4, 8))
        else:
            activities.append(np.random.randint(8, 15))

    return pd.DataFrame({
        'date': dates,
        'activity': activities
    })

def get_activity_color(count):
    """Return GitHub-style color based on activity count."""
    if count == 0:
        return '#ebedf0'
    elif count < 4:
        return '#9be9a8'
    elif count < 8:
        return '#40c463'
    elif count < 12:
        return '#30a14e'
    else:
        return '#216e39'

def create_activity_grid(data):
    """Create Plotly figure for activity grid."""
    import plotly.graph_objects as go

    # Process data by month
    months = []
    month_labels = []

    for month in range(1, 13):
        month_data = data[data['date'].dt.month == month]
        if not month_data.empty:
            months.append(month_data)
            # Get the first date of the month and format it
            first_date = month_data['date'].iloc[0]
            month_labels.append(first_date.strftime('%B'))
        else:
            # Handle empty months
            months.append(pd.DataFrame({'date': [], 'activity': []}))
            month_labels.append('')

    # Create figure
    fig = go.Figure()

    y_positions = []
    x_positions = []
    colors = []
    hover_texts = []

    for i, month_data in enumerate(months):
        if not month_data.empty:
            for j, (_, row) in enumerate(month_data.iterrows()):
                y_positions.append(i)
                x_positions.append(j)
                colors.append(get_activity_color(row['activity']))
                hover_texts.append(
                    f"Date: {row['date'].strftime('%Y-%m-%d')}<br>"
                    f"Activity: {row['activity']} contributions"
                )

    if y_positions:  # Only add trace if there's data
        fig.add_trace(go.Scatter(
            x=x_positions,
            y=y_positions,
            mode='markers',
            marker=dict(
                size=15,
                color=colors,
                symbol='square',
            ),
            text=hover_texts,
            hoverinfo='text',
        ))

    # Update layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=20, b=20),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticktext=month_labels,
            tickvals=list(range(12)),
            side='left',
        ),
        height=300,
        showlegend=False,
    )

    return fig