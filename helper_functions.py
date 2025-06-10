import plotly.graph_objects as go
import duckdb as duck
import urllib.request
from io import BytesIO 
from PIL import Image
import io
import base64
import pandas as pd
import numpy as np
from datetime import datetime

def shot_chart(player, date='all'):
    if date == 'all':
        player_name = player
        query = f"""
        select a1.*
            , ('Quarter ' || a1.period_number || ' - ' || a1.clock_display_value) as quarter_time_clock
            , strftime('%B %d, %Y', game_date) as game_date_frmt
            , case when coordinate_x > 0 then coordinate_x * -1 else coordinate_x end as coordinate_x_frmt
            , case when coordinate_x > 0 then coordinate_y * -1 else coordinate_y end as coordinate_y_frmt
        from './pages/data/SHOT_CHART_UV.parquet' a1
        where a1.athlete_display_name = '{player_name}'
        """
        with duck.connect() as con:
            shot_chart_df = con.execute(query).fetchdf()    

    else: 
        player_name = player
        game_date = date
        query = f"""
        select a1.*
            , ('Quarter ' || a1.period_number || ' - ' || a1.clock_display_value) as quarter_time_clock
            , strftime('%B %d, %Y', game_date) as game_date_frmt
            , case when coordinate_x > 0 then coordinate_x * -1 else coordinate_x end as coordinate_x_frmt
            , case when coordinate_x > 0 then coordinate_y * -1 else coordinate_y end as coordinate_y_frmt
        from './pages/data/SHOT_CHART_UV.parquet' a1
        where a1.athlete_display_name = '{player_name}'
        and a1.game_date = '{game_date}'
        """
        with duck.connect() as con:
            shot_chart_df = con.execute(query).fetchdf()    

    #initializing figure
    fig = go.Figure()
    three_pt_radius = 23.75  # NBA three-point distance (excluding corners)
    hoop_x = -41.75  # Hoop location on left side

    # Generate three-point arc (semi-circle)
    theta = np.linspace(-np.pi / 2.62, np.pi / 2.62, 50)  # Angle range for half-circle
    arc_x = hoop_x + three_pt_radius * np.cos(theta)  # X coordinates
    arc_y = three_pt_radius * np.sin(theta)  # Y coordinates

    # Add the 3PT arc
    fig.add_trace(go.Scatter(
        x=arc_x, 
        y=arc_y,
        mode='lines',
        line=dict(color='#35A29F', width=2),
        showlegend=False,
        zorder=1,
        hoverinfo='skip'
    ))

    # Left end vertical line
    fig.add_shape(
        type="line",
        x0=-47, y0=-25, x1=-47, y1=25, 
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # Top 3PT corner line
    fig.add_shape(
        type="line",
        x0=-47, y0=-22, x1=-33, y1=-22, 
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # Bottom 3PT corner line
    fig.add_shape(
        type="line",
        x0=-47, y0=22, x1=-33, y1=22, 
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # Bottom FT line
    fig.add_shape(
        type="line",
        x0=-47, y0=-8, x1=-28, y1=-8, 
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # Top FT line
    fig.add_shape(
        type="line",
        x0=-47, y0=8, x1=-28, y1=8, 
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # Joined FT line
    fig.add_shape(
        type="line",
        x0=-28, y0=-8, x1=-28, y1=8, 
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # Backboard line
    fig.add_shape(
        type="line",
        x0=-43, y0=-3, x1=-43, y1=3, 
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # Top rest line
    fig.add_shape(
        type="line",
        x0=-47, y0=6, x1=-28, y1=6, 
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # Bottom rest line
    fig.add_shape(
        type="line",
        x0=-47, y0=-6, x1=-28, y1=-6, 
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # key arcs
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-34, y0=-6, x1=-22, y1=6,
        line_color="#35A29F",
        showlegend=False,
        layer="below"
    )

    # basket
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-43, y0=-.75, x1=-41.5, y1=.75,
        line_color="#35A29F",
        showlegend=False,
        layer="below"
    )

    # top court
    fig.add_shape(type="line",
        x0=-47, y0=25, x1=0, y1=25,  
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )

    # bottom court
    fig.add_shape(type="line",
        x0=-47, y0=-25, x1=0, y1=-25,  
        line=dict(color="#35A29F", width=2),
        showlegend=False,
        layer="below"
    )


    fig.add_trace(
        go.Scatter(x=shot_chart_df['coordinate_x_frmt'],
                                y=shot_chart_df['coordinate_y_frmt'],
                                mode='markers',
                                marker=dict(
                                    line=dict(width=2, color='DarkSlateGrey'),
                                    symbol=[ 'circle' if x > 0 else 'x' for x in shot_chart_df['score_value']],
                                    color='#FB4141',
                                    size=10,
                                ),
                                text=shot_chart_df['score_value'],
                                customdata=shot_chart_df[['game_date_frmt', 'game_title', 'quarter_time_clock', 'score_value', 'type_text']],
                                hovertemplate = '<b>Game Date:</b> %{customdata[0]}<br>' + 
                                '<b>Game Title: </b>%{customdata[1]}<br>' 
                                + '<b>Shot Time:</b> %{customdata[2]}<br>'
                                + '<b>Shot Points:</b> %{customdata[3]}<br>'
                                + '<b>Shot Type:</b> %{customdata[4]}<br> <extra></extra>',
                                showlegend=False,
                                zorder=2
                                ))
    if player != '':
        url = shot_chart_df["athlete_headshot_href"].unique()[0]
        # Opening image
        img = Image.open(BytesIO(urllib.request.urlopen(url).read())) 

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        data_uri = f"data:image/png;base64,{encoded_image}"

        # Add player image
        fig.add_layout_image(
            dict(
                source=data_uri,
                xref="paper", yref="paper",
                x=1, y=1.04,
                sizex=0.2, sizey=0.2,
                xanchor="right", yanchor="bottom"
            )
        )

    # Set templates
    fig.update_layout(
        title=dict(
            text="Player Shot Chart",
            xanchor='left',
            yanchor='top'     
        ),
        width=500, height=500,
        plot_bgcolor='#111111',
        template='plotly_dark',
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Courier New, monospace"
        ),
        margin=dict(l=20, r=20, t=80, b=20),
        font=dict(family="Courier New, monospace"),
        xaxis=dict(zeroline=False, showgrid=False, range=[-48, 0], type='linear', showticklabels=False),
        yaxis=dict(zeroline=False, showgrid=False, range=[-26, 26], type='linear', showticklabels=False))
        
    return fig

def game_roster_pm(game_date, team_name):
    # filtered query
    query = f"""
    select a1.*
        , CAST(REPLACE(plus_minus, '+', '') AS INTEGER) AS plus_minus_frmt
        , strftime('%B %d, %Y', game_date) as game_date_frmt
        , case when three_point_field_goals_attempted = 0 then 'NA' else CAST(CAST(((field_goals_made / field_goals_attempted)*100) as INTEGER) AS TEXT) || '%  (' ||
            cast(cast(field_goals_made as integer) as text) || '/' || cast(cast(field_goals_attempted as integer) as text) || ')' end as fg_frmt
        , case when three_point_field_goals_attempted = 0 then 'NA' else CAST(CAST(((three_point_field_goals_made / three_point_field_goals_attempted)*100) as INTEGER) AS TEXT) 
            || '%  (' || cast(cast(three_point_field_goals_made as integer) as text) || '/' || cast(cast(three_point_field_goals_attempted as integer) as text) || ')' 
            end as '3fg_frmt'
        , case when free_throws_attempted = 0 then 'NA' else CAST(CAST(((free_throws_made / free_throws_attempted)*100) as INTEGER) AS TEXT) 
            || '%  (' || cast(cast(free_throws_made as integer) as text) || '/' || cast(cast(free_throws_attempted as integer) as text) || ')' 
            end as 'ft_frmt'
    from './pages/data/PLAYER_GAME_STATS_UV.parquet' a1
    where a1.game_date = '{game_date}'
    and a1.team_display_name = '{team_name}'
    and a1.did_not_play = False
    """

    # Execute query with DuckDB
    with duck.connect() as con:
        roster_df = con.execute(query).fetchdf()

    # Initialize chart figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=roster_df['minutes'],
                                y=roster_df['plus_minus_frmt'],
                                mode='markers',
                                marker=dict(
                                    line=dict(width=2, color='DarkSlateGrey'),
                                    # symbol=[ 'circle' if x > 0 else 'x' for x in roster_df['score_value']],
                                    color='#FB4141',
                                    size=8,
                                    opacity=0
                                ),
                                customdata=roster_df[['athlete_display_name', 'minutes', 'fg_frmt', '3fg_frmt', 'ft_frmt', 
                                                        'rebounds', 'assists',
                                                        'steals', 'blocks', 'turnovers', 'fouls', 'plus_minus', 'points',
                                                        'starter']],
                                hovertemplate = '<b>Player Name: </b>%{customdata[0]}<br>' 
                                + '<b>Minutes Played: </b>%{customdata[1]}<br>' 
                                + '<b>FG %:</b> %{customdata[2]}<br>'
                                + '<b>3-PT FG %:</b> %{customdata[3]}<br>'
                                + '<b>Free-Throw %:</b> %{customdata[4]}<br>'
                                + '<b>Rebounds:</b> %{customdata[5]}<br>'
                                + '<b>Assists:</b> %{customdata[6]}<br>'
                                + '<b>Steals:</b> %{customdata[7]}<br>'
                                + '<b>Blocks:</b> %{customdata[8]}<br>'
                                + '<b>Turnovers:</b> %{customdata[9]}<br>'
                                + '<b>Fouls:</b> %{customdata[10]}<br>'
                                + '<b>Plus-Minus:</b> %{customdata[11]}<br>'
                                + '<b>Total Points:</b> %{customdata[12]}<br>'
                                + '<b>Starter?:</b> %{customdata[13]}<br> <extra></extra>' 
                                ))

    for t in roster_df["athlete_display_name"].unique():
        url = roster_df.loc[roster_df['athlete_display_name']== f"{t}", "athlete_headshot_href"].values[0]
        # Opening image
        img = Image.open(BytesIO(urllib.request.urlopen(url).read())) 

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        data_uri = f"data:image/png;base64,{encoded_image}"

        fig.add_layout_image(
            dict(
            source=data_uri,
            sizex=9,
            sizey=9,
            name=t,
            xref="x",
            yref="y",
            x=int(roster_df.loc[roster_df['athlete_display_name']== f"{t}", "minutes"].values[0]),
            y=int(roster_df.loc[roster_df['athlete_display_name']== f"{t}", "plus_minus_frmt"].values[0]),
            layer="above",
            opacity=.8, 
            xanchor="center",
            yanchor="middle",
            sizing="contain"
        ))

    fig.update_shapes(opacity=0.2)
    if len(roster_df) == 0:
        fig.update_layout(
                    title=dict(
                        text="Plus-Minus Game Team Ranking",
                        xanchor='left',
                        yanchor='top'     
                    ),
                    plot_bgcolor='#111111',
                    template='plotly_dark',
                    hoverlabel=dict(
                        bgcolor="white",
                        font_size=16,
                        font_family="Courier New, monospace"
                    ),
                    margin=dict(l=20, r=20, t=60, b=20),
                    font=dict(family="Courier New, monospace"),
                    xaxis_title='Minutes Played',
                    yaxis_title='Plus-Minus',
                    xaxis=dict(zeroline=True, showgrid=False),
                    yaxis=dict(zeroline=True, showgrid=False),
                    )
    else:
        fig.update_layout(
                    title=dict(
                        text="Plus-Minus Game Team Ranking",
                        xanchor='left',
                        yanchor='top'     
                    ),
                    plot_bgcolor='#111111',
                    template='plotly_dark',
                    hoverlabel=dict(
                        bgcolor="white",
                        font_size=16,
                        font_family="Courier New, monospace"
                    ),
                    margin=dict(l=20, r=20, t=60, b=20),
                    font=dict(family="Courier New, monospace"),
                    xaxis_title='Minutes Played',
                    yaxis_title='Plus-Minus',
                    xaxis=dict(zeroline=True, showgrid=False),
                    yaxis=dict(zeroline=True, showgrid=False),
                    yaxis_range=[int(roster_df['plus_minus_frmt'].min())-10, int(roster_df['plus_minus_frmt'].max())+10],
                    )
    
    return fig

def calculate_moving_average(data, window_size):
    df = pd.DataFrame(data, columns=['Actual'])
    moving_average = df['Actual'].rolling(window=window_size).mean()
    return moving_average

def ma_df(player_name):
    # filtered query
    if player_name == 'PH':
        df = pd.DataFrame({
                'athlete_display_name': ['PH'], 
                'game_date': ['2099-01-01'],
                'points': [100],
                'game_title': ['Placeholder'],
            })
    else:
        query = f"""
        select a1.*
        from './pages/data/PLAYER_GAME_STATS_UV.parquet' a1
        where a1.athlete_display_name = '{player_name}'
        and a1.did_not_play = False
        """
        # Execute query with DuckDB
        with duck.connect() as con:
            df = con.execute(query).fetchdf()

    return df

def mov_avg_game(player_name, attr):
    df = ma_df(player_name)

    init_df = df.sort_values(['athlete_display_name', 'game_date']).reset_index(drop=True)
    fltr_data = init_df[init_df['athlete_display_name']==player_name].reset_index(drop=True)

    data_points = fltr_data[attr].values.tolist()
    moving_avg_3_days = calculate_moving_average(data_points, window_size=3)
    moving_avg_5_days = calculate_moving_average(data_points, window_size=5)
    moving_avg_7_days = calculate_moving_average(data_points, window_size=7)

    fltr_data['mov_avg_3_gms'] = moving_avg_3_days
    fltr_data['mov_avg_5_gms'] = moving_avg_5_days
    fltr_data['mov_avg_7_gms'] = moving_avg_7_days

    actual_dp = fltr_data[attr].values.tolist()
    moving_avg_3= fltr_data["mov_avg_3_gms"].values.tolist()
    moving_avg_5 = fltr_data["mov_avg_5_gms"].values.tolist()
    moving_avg_7 = fltr_data["mov_avg_7_gms"].values.tolist()

    fig = go.Figure()

    # Add trace for actual points
    fig.add_trace(go.Scatter(x=list(range(1, len(actual_dp)+1))
                            , y=actual_dp, mode='lines+markers', name='Actual Points'
                            # , text=text_points
                            , marker=dict(
                                color='#419197',
                                size=5,
                                # angleref="previous"
                            ),
                            customdata=fltr_data[['game_date', 'game_title']],
                            hovertemplate = '<b>Game Date:</b> %{customdata[0]}<br>' + 
                            '<b>Game Matchup: </b>%{customdata[1]}<br>' + '<b>Value:</b> %{y}<br>'
                            ))

    # Add trace for moving average
    fig.add_trace(go.Scatter(x=list(range(1, len(moving_avg_3)+1))
                            , y=moving_avg_3, mode='lines', name='3-Game Moving Average'
                            , marker=dict(
                                color='#FF1E1E'
                            ),
                            hovertemplate = '<b>3-GM MA:</b> %{y}<br>'))

    fig.add_trace(go.Scatter(x=list(range(1, len(moving_avg_5)+1))
                            , y=moving_avg_5, mode='lines', name='5-Game Moving Average'
                            , marker=dict(
                                color='#06D001'
                            ),
                            hovertemplate = '<b>5-GM MA:</b> %{y}<br>'))

    fig.add_trace(go.Scatter(x=list(range(1, len(moving_avg_7)+1))
                            , y=moving_avg_7, mode='lines', name='7-Game Moving Average'
                            , marker=dict(
                                color='#FDFF00'
                            ),
                            hovertemplate = '<b>7-GM MA:</b> %{y}<br>'))

    fig.update_annotations(font_size=9, bordercolor='#419197', font_family="Courier New, monospace", font_color='black', borderwidth=1.5, borderpad=1.5, bgcolor='white')

    # Update layout
    fig.update_layout(
                    title=dict(
                        text="Game Trends",
                        xanchor='left',
                        yanchor='top'     
                    ),
                    showlegend=False,
                    xaxis_title='Game number',
                    yaxis_title=attr,
                    plot_bgcolor='#111111',
                    template='plotly_dark',
                    hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Courier New, monospace"),
                    margin=dict(l=20, r=20, t=60, b=20),
                    font=dict(family="Courier New, monospace"))

    fig.update_yaxes(showline=False, gridcolor='#7D7C7C', griddash='dash', showspikes=True)
    fig.update_xaxes(showline=False, gridcolor='#7D7C7C', griddash='dash')
    # Show the figure
    # fig.show(config={'displayModeBar': False, 'doubleClickDelay': 1000})

    return fig
