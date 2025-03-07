import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

def build_dashboard(df):
    """
    Build a polished cybersecurity analytics dashboard using Dash and Bootstrap.
    
    The layout includes:
      - A navigation bar (header) for branding.
      - A fixed sidebar for filtering (e.g., protocol selection).
      - A main content area with a time series chart and a row with a bar and pie chart.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the merged dataset.
    
    Returns:
        dash.Dash: The configured Dash application.
    """
    # Use a Bootstrap theme (e.g., SLATE for a dark, modern look)
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
    
    # Create a navigation bar
    navbar = dbc.NavbarSimple(
        brand="Cybersecurity Analytics Dashboard",
        brand_href="#",
        color="primary",
        dark=True,
        sticky="top",
    )

    # Create a sidebar for filters, replacing dbc.FormGroup with an html.Div with className 'form-group'
    sidebar = html.Div(
        [
            html.H5("Filters", className="display-6", style={"color": "#ffffff"}),
            html.Hr(),
            html.Div(
                [
                    dbc.Label("Select Protocol", style={"color": "#ffffff"}),
                    dcc.Dropdown(
                        id="protocol-dropdown",
                        options=[{"label": proto, "value": proto} for proto in sorted(df["proto"].unique())],
                        value=sorted(df["proto"].unique())[0],
                        clearable=False,
                    ),
                ],
                className="form-group"
            ),
        ],
        style={
            "position": "fixed",
            "top": "70px",  # height of the navbar
            "left": 0,
            "bottom": 0,
            "width": "18rem",
            "padding": "2rem 1rem",
            "background-color": "#343a40",
            "overflowY": "auto",
        },
    )

    # Create main content area
    content = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="time-series-chart"), md=12),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="bar-chart"), md=6),
                    dbc.Col(dcc.Graph(id="pie-chart"), md=6),
                ]
            ),
        ],
        style={"margin-left": "20rem", "margin-right": "2rem", "padding": "2rem 1rem"},
    )

    # Define the app layout
    app.layout = html.Div([navbar, sidebar, content])

    # Callback for updating charts based on selected protocol
    @app.callback(
    [Output("time-series-chart", "figure"),
     Output("bar-chart", "figure"),
     Output("pie-chart", "figure")],
    [Input("protocol-dropdown", "value")]
)
    def update_charts(selected_proto):
        # Filter the dataset based on the selected protocol if one is chosen
        filtered_df = df[df["proto"] == selected_proto] if selected_proto else df
        print("Filtered DataFrame shape:", filtered_df.shape)
        
        # --- Time Series Chart ---
        # Since there is no timestamp column, we use the DataFrame index as a proxy.
        ts_fig = {}
        if "sbytes" in filtered_df.columns:
            ts_fig = px.line(filtered_df, x=filtered_df.index, y="sbytes", 
                            title="Traffic Over Rows (sbytes)",
                            labels={"x": "Row Index", "sbytes": "Source Bytes"})
        else:
            ts_fig = px.scatter(title="No source bytes data available")
        
        # --- Bar Chart: Protocol Frequency ---
        bar_fig = {}
        if "proto" in filtered_df.columns:
            bar_data = filtered_df["proto"].value_counts().reset_index()
            bar_data.columns = ["protocol", "count"]
            bar_fig = px.bar(bar_data, x="protocol", y="count", title="Protocol Frequency",
                            labels={"protocol": "Protocol", "count": "Count"})
        else:
            bar_fig = px.scatter(title="No protocol data available")
        
        # --- Pie Chart: Attack Category Distribution ---
        pie_fig = {}
        if "attack_cat" in filtered_df.columns:
            pie_data = filtered_df["attack_cat"].value_counts().reset_index()
            pie_data.columns = ["attack_cat", "count"]
            pie_fig = px.pie(pie_data, names="attack_cat", values="count", title="Attack Category Distribution")
        else:
            pie_fig = px.scatter(title="No attack category data available")
        
        return ts_fig, bar_fig, pie_fig


    return app
