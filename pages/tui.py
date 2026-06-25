import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import base64

dash.register_page(__name__, path='/tui-project')

svg_data = open("./assets/terminal_app_uml.svg", "rb").read()
encoded = base64.b64encode(svg_data).decode("utf-8")

layout =  html.Div([
            html.H1(['Developing a free alternative to Bloomberg Terminal'], id="ml-methods-cr"),
            html.Br(),
            html.P(["Link to Github for Code:", html.A("Github Page", href="https://github.com/jaelar0/financial-terminal", style={"font-family": "lightFont", "color": "white"}),]),
            html.Br(),
            html.H3(['Application Infrastructure']),
            html.P("This idea came about during my Software Engineering course as a final and semester-long project.\
                   A team of 3 members were tasked to deliver a terminal user interface (TUI) application that would \
                   allow users to conduct fundamental and some technical analysis for any stock traded on the major US markets. \
                   The link to github contains the code our team produced cloned into a public repository. Any user that clones the repo \
                   should receive a functional application when executing the codebase."),
            html.Br(),
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
            html.H3(['Application Overview']),
            html.P("""
              This project is a terminal-based financial data dashboard built with Python's Textual framework, designed as a free, open-source alternative to expensive platforms like the Bloomberg Terminal. 
              The application runs entirely in the terminal but delivers a modern, responsive, multi-pane interface—complete with live-updating widgets, keyboard-driven navigation, and mouse support—all rendered in the terminal emulator rather than a browser or desktop GUI. 
              The goal was to recreate the feel of a professional trading desk tool: dense information layouts, fast context-switching between tickers, and real-time visual feedback, but without licensing costs or the overhead of a full web stack.
              Data is sourced from two main libraries: yfinance for real-time and historical market data (quotes, price history, fundamentals, options chains), and edgartools for pulling SEC filings directly from EDGAR, including 10-Ks, 10-Qs, and 8-Ks, so users can cross-reference market activity with primary-source regulatory disclosures.          
              """
            ),
            html.Br(),
            html.P("""
              To make the experience feel personalized rather than static, the app uses a local SQLite database to persist user preferences—things like saved watchlists, layout configurations, color themes, and recently viewed tickers—so the dashboard remembers how each user likes to work between sessions.
              Architecturally, the project leans heavily into Textual's reactive programming model, using async workers to fetch data in the background without blocking the UI, and custom widgets to display candlestick-style price charts, scrolling filing summaries, and sortable data tables directly in the terminal. The result is a snappy, keyboard-first tool that's especially appealing to developers and power users who live in the terminal anyway and want quick access to market data and SEC filings without tabbing over to a browser.
              Currently, I am working on re-writing the frontend in C++ but eventually the entire app will be re-written. This will open doors for more functionality and a more stable and snappier application.             
              """
            ),
            html.Br(),
            html.H3(['Video Demo']),
            html.Video(
              src="/assets/financial_terminal_demo.mp4",
              controls=True,
              autoPlay=False,
              style={"width": "100%", "maxWidth": "800px", 'justifyContent': 'center'}
            )
        ])

