import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import base64

dash.register_page(__name__, path='/dashboard-info-project')
svg_data = open("./assets/analytics_proj_uml.svg", "rb").read()
encoded = base64.b64encode(svg_data).decode("utf-8")

layout =  html.Div([
            html.H1(['Using web-scraped data to build an mini NBA dashboard'], id="ml-methods-cr"),
            html.Br(),
            html.P(["Go to Dashboard: ", html.A("Dashboard Page", href="/nba-dash", style={"font-family": "lightFont", "color": "white"}),]),
            html.Br(),
            html.H3(['Architecture Overview']),
            html.Div(
              children=[
                     html.Img(src=f"data:image/svg+xml;base64,{encoded}", style={'width': '50%'})
              ],
              style={
                     'display': 'flex',
                     'justifyContent': 'center'
              }
            ),  
            html.Br(),
            html.H3(['Overview']),
            html.P("""
              This project came about during my "Database and Scripting Languages" graduate course and is a full-stack sports analytics pipeline that combines an unconventional data-collection method with a polished visualization layer. Rather than relying on a paid sports data API, the system uses a PiKVM device - normally used for remote server management via KVM-over-IP - to programmatically control a physical machine's browser, navigating to sports statistics websites and downloading the raw HTML pages it renders. This approach sidesteps API rate limits, paywalls, and bot-detection measures that often block conventional scraping, since the requests originate from genuine browser sessions running on real hardware.
            """),
            html.Br(),
            html.P("""
              Once the HTML is captured, a parsing layer (built with BeautifulSoup) extracts structured data from the pages: individual shot locations and outcomes for NBA players, along with box score stats and season averages. This parsed data is cleaned, normalized, and loaded into a PostgreSQL database, which serves as the system's single source of truth and supports efficient querying across players, games, and seasons as the dataset grows over time. The final datasets are then exported to Parquet file formats for speedier queries for frontend visualizations.
            """),
            html.Br(),
            html.P("""
              The final piece is an interactive dashboard built with Dash and Plotly, which queries the exported Parquet files via a DuckDB engine to generate two main types of visualizations: shot charts that break down where on the court a given player took and made or missed shots in a specific game, and time-series plots (with 3, 5, and 7 Game Moving Averages) tracking how a player's season averages (points, rebounds, assists, etc.) trend over the course of the season. The combination of an unusual but reliable data-acquisition method, a robust relational backend, and an interactive analytics frontend makes this project a good demonstration of end-to-end data engineering - from raw HTML to a polished, queryable visual product.     
            """)
        ])

