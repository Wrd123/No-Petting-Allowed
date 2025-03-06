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
            options=[{'label': p, 'value': p} for p in df['proto'].unique()] if 'proto' in df.columns else [],
            value=df['proto'].unique()[0] if 'proto' in df.columns else None
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
    def update_charts(selected_proto):
        # 1. Filter data by protocol
        if 'proto' in df.columns and selected_proto:
            filtered_df = df[df['proto'] == selected_proto]
        else:
            filtered_df = df

        # 2. Time Series Chart (example using 'Stime' and 'sbytes')
        #    Convert 'Stime' from integer to a datetime if you want a real date/time axis.
        ts_fig = {}
        if 'Stime' in filtered_df.columns and 'sbytes' in filtered_df.columns:
            # Convert to datetime if needed
            filtered_df['Stime'] = pd.to_datetime(filtered_df['Stime'], unit='s')
            ts_fig = px.line(filtered_df, x='Stime', y='sbytes', title='Traffic Over Time (sbytes)')
        
        # 3. Bar Chart (example counting 'proto' occurrences)
        bar_fig = {}
        if 'proto' in filtered_df.columns:
            bar_data = filtered_df['proto'].value_counts().reset_index()
            bar_data.columns = ['protocol', 'count']
            bar_fig = px.bar(bar_data, x='protocol', y='count', title='Protocol Frequency')
        
        # 4. Pie Chart (example for 'attack_cat')
        pie_fig = {}
        if 'attack_cat' in filtered_df.columns:
            pie_data = filtered_df['attack_cat'].value_counts().reset_index()
            pie_data.columns = ['attack_cat', 'count']
            pie_fig = px.pie(pie_data, names='attack_cat', values='count', title='Attack Category Distribution')

        return ts_fig, bar_fig, pie_fig
    
    return app
