import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=False)
server = app.server

app.layout = html.Div(
    className="container", children=[
        html.Header(className="header", children=[
            html.Div("Jorge Reyes", className="title"),
            html.Div([
                html.Span("Site about"),
                html.Span(" my", className="highlight"),
                html.Span(" personal "),
                html.Span("projects.", className="highlight")
            ], className="subtitle"),
            html.Nav(className="nav", children=[
                html.A("Home", href="/"),
                html.A("Dashboard Project", href="/nba-dash"),
                html.A("ML Project", href="/ml-project"),
            ]),
            html.Div(className="icons", children=[
                html.A(
                    html.Img(src="https://img.icons8.com/ios-filled/50/ffffff/github.png", className="icon")
                    , href="https://github.com/jaelar0/personal-site"),
                # html.Img(src="https://img.icons8.com/ios-filled/50/ffffff/github.png", className="icon")
            ])
        ]),
       dash.page_container
    ])

if __name__ == '__main__':
    app.run(debug=True)
