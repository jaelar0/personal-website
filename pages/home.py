import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div(
                className="content",
                children=[
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    className="podcast-section",
                                    style={"width": "97%"},
                                    children=[
                                        html.Div(
                                            className="podcast", 
                                            children=[
                                                html.Img(
                                                    src="/assets/profile.png", 
                                                    className="podcast-img"
                                                ),

                                                html.Div(
                                                    [
                                                        html.H4("A little about me..."),
                                                        html.H3("My experience and most recent projects"),
                                                        html.Ul(
                                                            [
                                                                html.Li(html.P("* I graduated with a Bachelor's in finance but I \
                                                                        have amassed a passion for programming and data science.")),
                                                                html.Li(html.P("* This passion led me to complete a master's degree \
                                                                        in data science at the University of Tennessee.")),
                                                                html.Li(html.P("* I have over 6 years of experience working at financial \
                                                                        institutions and have worked on projects ranging from analytics \
                                                                        engineering, BI reporting, and data and modeling analytics.")),
                                                                html.Li(html.P("* This site contains a collection of projects that I have \
                                                                        completed in my master's program. With more to come!"))
                                                            ]
                                                        )
                                                    ]
                                                )                                        
                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.H3("Projects"),
                        )
                    ),
                    
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardImg(
                                            src="/assets/ml_project_bg.png",
                                            top=True,
                                            style={"opacity": 0.3},
                                        ),
                                        dbc.CardImgOverlay(
                                            dbc.CardBody(
                                                [
                                                    html.H4("Machine Learning Methods in Credit Risk", className="card-title"),
                                                    html.P("", className='card-text'),
                                                    dbc.Button("Project Page", color="light", className="me-1", href="/ml-project"),
                                                ],
                                            ),
                                        ),
                                    ],
                                    outline=True,
                                    # style={"width": "22rem"},
                                ),
                                width="auto"
                            ),

                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardImg(
                                            src="/assets/ml_project_bg.png",
                                            top=True,
                                            style={"opacity": 0.3},
                                        ),
                                        dbc.CardImgOverlay(
                                            dbc.CardBody(
                                                [
                                                    html.H4("End-to-End Analytics Engineering using NBA data", className="card-title"),
                                                    html.P("", className='card-text'),
                                                    dbc.Button("More Information", color="light", className="me-1", href="/dashboard-info-project"),
                                                ],
                                            ),
                                        ),
                                    ],
                                    outline=True,
                                    # style={"width": "22rem"},
                                ),
                                width="auto"
                            ),

                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardImg(
                                            src="/assets/ml_project_bg.png",
                                            top=True,
                                            style={"opacity": 0.3},
                                        ),
                                        dbc.CardImgOverlay(
                                            dbc.CardBody(
                                                [
                                                    html.H4("Developing a financial Terminal User Interface (TUI)", className="card-title"),
                                                    html.P("", className='card-text'),
                                                    dbc.Button("Project Page", color="light", className="me-1", href="/tui-project"),
                                                ],
                                            ),
                                        ),
                                    ],
                                    outline=True,
                                    # style={"width": "22rem"},
                                ),
                                width="auto"
                            )
                        ],
                    )
                ]
            )