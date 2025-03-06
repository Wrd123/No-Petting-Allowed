import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

def build_dashboard(df):
    """
    Build an interactive dashboard using Plotly Dash.
    
    The dashboard includes:
        - A time series chart for network traffic.
        - A bar chart for event type frequency.
        - A pie chart for attack category distribution.
        - An interactive dropdown to filter data by event type.
    
    Args:
        df (pd.DataFrame): Cleaned dataset.
        
    Returns:
        dash.Dash: The Dash application instance.
    """
    app = dash.Dash(__name__)
    
    # Layout definition for the dashboard
    app.layout = html.Div(children=[
        html.H1("Cybersecurity Analytics Dashboard"),
        html.Div("Interactive dashboard for monitoring network traffic and detecting anomalies."),
        
        # Dropdown for filtering by event type (if available)
        html.Div([
            html.Label("Select Event Type:"),
            dcc.Dropdown(
                id='event-type-dropdown',
                options=[{'label': et, 'value': et} for et in df['event_type'].unique()] if 'event_type' in df.columns else [],
                value=df['event_type'].unique()[0] if 'event_type' in df.columns else None
            )
        ], style={'width': '40%', 'margin': '20px 0'}),
        
        # Graph components for visualizations
        dcc.Graph(id='time-series-chart'),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='pie-chart')
    ])
    
    # Callback to update the charts based on dropdown selection
    @app.callback(
        [Output('time-series-chart', 'figure'),
         Output('bar-chart', 'figure'),
         Output('pie-chart', 'figure')],
        [Input('event-type-dropdown', 'value')]
    )
    def update_charts(selected_event):
        # Filter the data based on the selected event type if applicable
        filtered_df = df[df['event_type'] == selected_event] if 'event_type' in df.columns and selected_event else df
        
        # Build Time Series Chart (if data available)
        if 'timestamp' in filtered_df.columns and 'traffic_volume' in filtered_df.columns:
            filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
            ts_fig = px.line(filtered_df, x='timestamp', y='traffic_volume', title='Network Traffic Over Time')
        else:
            ts_fig = {}
        
        # Build Bar Chart for event type counts
        if 'event_type' in filtered_df.columns:
            bar_data = filtered_df['event_type'].value_counts().reset_index()
            bar_data.columns = ['event_type', 'count']
            bar_fig = px.bar(bar_data, x='event_type', y='count', title='Event Type Frequency')
        else:
            bar_fig = {}
        
        # Build Pie Chart for attack category distribution
        if 'attack_category' in filtered_df.columns:
            pie_data = filtered_df['attack_category'].value_counts().reset_index()
            pie_data.columns = ['attack_category', 'count']
            pie_fig = px.pie(pie_data, names='attack_category', values='count', title='Attack Category Distribution')
        else:
            pie_fig = {}
        
        return ts_fig, bar_fig, pie_fig
    
    return app
