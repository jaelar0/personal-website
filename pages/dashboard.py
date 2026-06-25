from dash import dash_table, Input, Output, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from helper_functions import shot_chart, mov_avg_game, game_roster_pm
import dash
import duckdb as duck
import base64
import urllib.parse

dash.register_page(__name__, path='/nba-dash')

steps = [
    {"label": "Scrape from NBA.com and ESPN", "color": "#74c0fc"},
    {"label": "Parse & Clean using bs4 in python", "color": "#ffa94d"},
    {"label": "Save data to Parquet", "color": "#69db7c"},
    {"label": "Upload data assets & connect to Dash", "color": "#b197fc"},
]

def encode_svg(svg):
    svg_url_encoded = urllib.parse.quote(svg)
    return f"data:image/svg+xml;utf8,{svg_url_encoded}"

player_names_sc_df = duck.query("""
    select distinct a1.athlete_display_name
    from './pages/data/SHOT_CHART_UV.parquet' a1
""").df()
player_list = player_names_sc_df['athlete_display_name'].values.tolist()

team_names_df = duck.query("""
    select distinct a1.team_display_name
    from './pages/data/PLAYER_GAME_STATS_UV.parquet' a1
    """).df()
team_list = team_names_df['team_display_name'].values.tolist()

query = f"""
    with q1 as (
        select a1.game_id
        , game_title
        , home_team_id
        , home_team_display_name
        , home_team_score
        , away_team_id
        , away_team_display_name
        , away_team_score
        from './pages/data/GAME_MATCHUP_UV.parquet' a1
    ),
    q2 as (
        select s1.game_id
            , s1.game_title
            , s1.home_team_id
            , s1.home_team_display_name
            , s1.home_team_score
            , s1.away_team_id
            , s1.away_team_display_name
            , s1.away_team_score
            , t1.team_id
            , t1.team_score
            , t1.team_winner
            , t1.assists
            , t1.blocks
            , t1.fast_break_points
            , cast(cast(t1.field_goal_pct as integer) as string) || '%' as field_goal_pct
            , t1.fouls
            , cast(cast(t1.free_throw_pct as integer) as string) || '%' as free_throw_pct
            , t1.points_in_paint
            , t1.steals
            , cast(cast(t1.three_point_field_goal_pct as integer) as string) || '%' as three_point_field_goal_pct
            , t1.total_rebounds
            , t1.team_display_name
            , t1.game_date
        from './pages/data/TEAM_GAME_STATS_UV.parquet' t1
        left join q1 s1 on s1.game_id = t1.game_id
    )

    select team_display_name as "Team Name"
        , case when (team_id = home_team_id and team_winner = True) 
        then game_title || '  W '  || away_team_score || '-' || team_score
        when (team_id = home_team_id and team_winner = False) 
        then game_title || '  L '  || away_team_score || '-' || team_score
        when (team_id = away_team_id and team_winner = True) 
        then game_title || '  W '  || team_score || '-' ||  home_team_score
        when (team_id = away_team_id and team_winner = False) 
        then game_title || '  L '  || team_score || '-' ||  home_team_score
        end as "Game Title"
        , game_date as "Game Date"
        , case when (team_id = home_team_id) 
        then away_team_display_name
        else home_team_display_name
        end as "Opp. Team Name"
        , team_score as Points
        , field_goal_pct as "FG %"
        , three_point_field_goal_pct as "3PT FG %"
        , free_throw_pct as "FT %"
        , fast_break_points as "Fast Break Points"
        , points_in_paint as "Points in Paint"
        , assists as "Assists"
        , total_rebounds as "Rebounds"
        , blocks as "Blocks"
        , fouls as "Fouls"
        , steals as "Steals"
    from q2
    order by game_date asc
"""

# Execute query with DuckDB
team_sched_full = duck.query(query).df()

# Create a container that arranges the filters next to one another and wraps them if necessary
filters_container = html.Div(style={'backgroundColor': 'black', 'padding': '20px'}, children=[
    # Row 1: First two filters
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'color': 'white'}, children=[
        # html.Div([
        #     html.Label("Team Name"),
        #     dcc.Dropdown(id='team-name-dd', 
        #                  className='team-name-dd', 
        #                  options=team_list, 
        #                  placeholder="Select Team for plus-minus analysis..",
        #                  style={'color': 'black'})
        # ], style={'flex': 1}),

        html.Div([
            html.Label("Player Name"),
            dcc.Dropdown(id='player-name-dd', 
                         className='player-name-dd', 
                         options=player_list, 
                         placeholder="Select player to analyze..",
                         style={'color': 'black'})
        ], style={'flex': 1}),
    ]),

    # Row 2: Second two filters
    html.Div(style={'display': 'flex', 'gap': '20px'}, children=[
        html.Div([
            html.Label("Statistic Type"),
            dcc.Dropdown(
                id='stat-name-dd',
                className='stat-name-dd',
                options=[
                {"label": "FG Made", "value": "field_goals_made"},
                {"label": "FG Att.", "value": "field_goals_attempted"},
                {"label": "3-PT FG Made", "value": "three_point_field_goals_made"},
                {"label": "3-PT FG Att.", "value": "three_point_field_goals_attempted"},
                {"label": "Free Throws Made", "value": "free_throws_made"},
                {"label": "Free Throws Att.", "value": "free_throws_attempted"},
                {"label": "Off. Rebounds", "value": "offensive_rebounds"},
                {"label": "Def. Rebounds", "value": "defensive_rebounds"},
                {"label": "Assists", "value": "assists"},
                {"label": "Points", "value": "points"}
                ], 
                placeholder="Select stat type for Moving Average Analysis...",
                style={'color': 'black'}
            )
        ], style={'flex': 1.2}),

        html.Div([
            html.Label("Game Date"),
            dcc.DatePickerSingle(
                id='game-date-picker',
                className='game-date-picker',
                min_date_allowed=datetime(2023, 10, 1),
                max_date_allowed=datetime(2024, 7, 1),
                initial_visible_month=datetime(2024, 2, 28),
                date=None
            )
        ], style={'flex': 1}),
    ])
])

first_row_charts = html.Div(style={'display': 'flex', 'backgroundColor': 'black', "borderRadius": "10px"}, children=[
                    html.Div([
                        dcc.Loading(
                            id='loading-sc-chart',
                            type='default',
                            children=dcc.Graph(
                                id='shot-chart',
                                figure = shot_chart(''),
                                className='sc-container',
                                config={'displayModeBar': False, 'doubleClickDelay': 1000}
                            )
                        )
                    ], style={'flex': '1', 'padding': '10px'}),
                    html.Div([
                        dcc.Loading(
                            id='loading-ma-chart',
                            type='default',
                            children=dcc.Graph(
                                id='attr-player-gm',
                                figure=mov_avg_game('PH', 'points'),
                                config={'displayModeBar': False, 'doubleClickDelay': 1000}
                            )
                        )
                    ], style={'flex': '1.5', 'padding': '10px'}),
                ])


dashboard_layout = html.Div([
                filters_container,
                html.Br(),
                first_row_charts,
                html.Br(),
                # html.Div([ 
                #     dcc.Loading(
                #         id='loading-pm-chart',
                #         type='default',
                #         children=dcc.Graph(
                #             id='pm-team-rank',
                #             figure=game_roster_pm(datetime(2024, 2, 28), 'All-Stars'),
                #             config={'displayModeBar': False, 'doubleClickDelay': 1000}
                #         )
                #     )
                # ], style={'backgroundColor': 'black', "borderRadius": "10px", 'padding': '10px'}),
    ], className="filter-parent")

layout = html.Div([
            html.Div([
                html.H2("NBA Dashboard", style={"textAlign": "left"}),
            ]),
            html.Br(),
            dashboard_layout
        ])

# SC callback
@dash.callback(
    Output('shot-chart', 'figure'),
    [Input('player-name-dd', 'value'),
     Input('game-date-picker', 'date')],
    prevent_initial_call=True
)
def update_sc(player_name_value, gm_date_value):
    if not player_name_value:
        raise PreventUpdate 
    
    if not gm_date_value:
        sc_player_flt = shot_chart(player_name_value)
    else:
        sc_player_flt = shot_chart(player_name_value, gm_date_value)

    return sc_player_flt

# MA chart callback
@dash.callback(
    Output('attr-player-gm', 'figure'),
    [Input('player-name-dd', 'value'),
    Input('stat-name-dd', 'value')],
    prevent_initial_call=True
)
def update_ma(player_name_value, stat_value):
    if not player_name_value or not stat_value:
        raise PreventUpdate 
    
    ma_attr_gm = mov_avg_game(player_name_value, stat_value)

    return ma_attr_gm

# PM chart callback
@dash.callback(
    Output('pm-team-rank', 'figure'),
    [Input('game-date-picker', 'date'),
    Input('team-name-dd', 'value')],
    prevent_initial_call=True
)

def update_pm(gm_date_value, team_name_value):
    if not gm_date_value or not team_name_value:
        raise PreventUpdate 
    pm_rank = game_roster_pm(gm_date_value, team_name_value)

    return pm_rank