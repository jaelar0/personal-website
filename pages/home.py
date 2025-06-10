import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go

dash.register_page(__name__, path='/')

layout = html.Div(className="content", children=[
            html.Div(className="podcast-section", children=[
                html.Div(className="podcast", children=[
                    html.Img(src="/assets/profile.png", className="podcast-img"),
                    html.Div([
                        html.H4("A little about me..."),
                        html.H3("My experience and most recent projects"),
                        html.Ul([
                            html.Li(html.P("* I graduated with a Bachelor's in finance but I \
                                       have amassed a passion for programming and data science.")),
                            html.Li(html.P("* This passion has led me to pursue a master's degree \
                                       in data science at the University of Tennessee where I am currently in my last semester.")),
                            html.Li(html.P("* I have over 5 years of experience working at financial \
                                       institutions and have worked on projects ranging from data \
                                       engineering to reporting and data analysis.")),
                            html.Li(html.P("* This site contains a collection of projects that I have \
                                       completed in my master's program. With more to come!"))
                        ])
                    ])
                ])
            ])
        ])
