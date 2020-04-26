import news_strings as ns
import random as rd
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import flask
import dash_bootstrap_components as dbc
import base64
import pandas as pd  
import psycopg2
from sqlalchemy import create_engine
import plotly.graph_objs as go
import dash_daq as daq
import plotly.express as px
import time
import math
import urllib
import urllib.request
from datetime import timedelta
import contextlib
import os
import urllib
import urllib.request
from urllib.request import Request, urlopen
from datetime import datetime as dt
import datetime
import json

# Style the button: http://dash-bootstrap-components.opensource.faculty.ai/l/components/button

PAGE_SIZE = 8 # For main data table
PAGE_SIZE_SQL = 3 # for custom sql data table

app = flask.Flask(__name__)
dash_app = dash.Dash(__name__, server = app, url_base_pathname='/') #, external_stylesheets=[external_style]) #dbc.themes.DARKLY


# Images/logos
image_filename_1 = 'chess-logo-2.png' # replace with your own image
encoded_image_1 = base64.b64encode(open(image_filename_1, 'rb').read())


# Serve local css
dash_app.css.config.serve_locally = True
dash_app.scripts.config.serve_locally = True



#####################
####### STYLES ######
#####################

tabs_styles = {
    'height': '60px',
    'width': '1100px',
    'marginLeft': 20
}
tab_style = {
    'borderBottom': '1px solid #333333',
    'padding': '20px',
    'backgroundColor': '#595959',
    'fontColor': 'black',
    'font-family': 'Courier New, monospace',
    'text-align': 'center',
    'text-vertical-align': 'center',
    'font-size': '120%',
    'width': '300px'
}

tab_selected_style = {
    'borderTop': '1px solid #323232',
    'borderBottom': '1px solid #222222',
    'backgroundColor': '#222222',
    'font-family': 'Courier New, monospace',
    'color': 'white',
    'padding': '6px',
    'text-align': 'center',
    'vertical-align': 'center',
    'text-vertical-align': 'center',
    #'fontWeight': 'bold',
    'font-size': '120%',
    'width': '300px'
}



#####################
##### FUNCTIONS #####
#####################

                        ###############################
                        ### Table for error strings ###
                        ###############################



columns = [
    {"id": 0, "name": "time_control"},
    {"id": 1, "name": "end_time"},
    {"id": 2, "name": "rated"},
    {"id": 3, "name": "time_class"},
    {"id": 4, "name": "rules"},
    {"id": 5, "name": "hour"},
    {"id": 6, "name": "user_result"},
    {"id": 7, "name": "user_color"},
    {"id": 8, "name": "user_rating"},
    {"id": 9, "name": "opponent_rating"},
    {"id": 10, "name": "username_opponent"}
    ]

st_date = (dt.today().date() - timedelta(days=600))

def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P("Games Played:"),
                    daq.LEDDisplay(
                        id="led-games-played",
                        value="3000",
                        color="#92e0d3",
                        backgroundColor="#222222",
                        size=50,
                    ),
                ],
            ),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Div(
                id="card-2",
                children=[
                    html.P("Latest ELO:"),
                    daq.LEDDisplay(
                        id="led-elo",
                        value="1400",
                        color="#92e0d3",
                        backgroundColor="#222222",
                        size=50,
                    ),
                ],
            ),
        ],
    )


# Make list of months to get data from api
now = dt(dt.now().year, dt.now().month, 1)
ctr = dt(2020, 3, 1)
list_months = [ctr.strftime('%Y-%m-%d')]

while ctr < now:
    ctr += timedelta(days=32)
    ctr = ctr.replace(day=1)
    list_months.append(dt(ctr.year, ctr.month, 1).strftime('%Y-%m-%d') )

#####################
###### LAYOUT #######
#####################
dash_app.layout = html.Div([

    ###### HIDDEN DIV TO SHARE GLOBAL DATAFRAME
    html.Div(id='hidden-dff', style={'display': 'none'}),
    html.Div(id='filtered-dff', style={'display': 'none'}),
    html.Div(id='games_played', style={'display': 'none'}),
    html.Div(id='intermediate-dff', style={'display': 'none'}),


    ###### TOP TITLE ######
    html.Br(),
    html.Br(),
    html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image_1.decode()))],
                       style={'display': 'inline-block', 'height': '180px', 'align-items': 'center',
                              'justify-content': 'center', 'display': 'flex'}, id='logo'),
    html.Br(),
    html.Br(),
    ###### TABS  ######
    html.Br(),
    dcc.Tabs(id="tabs", children=[

        ###### FIRST TAB: INPUT USER ######

        dcc.Tab(label='Username', children=[
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H5(
                'Input your chess.com username: Hold on 10-20 seconds for data to be fetched'
                , style={'font-family': 'Courier New, monospace', 'marginLeft': 40}),
            html.Div(dcc.Input(id="username", type="text", placeholder="",
                               style={'marginLeft': 40, 'backgroundColor': '#222222', 'color': '#ffffff',
                                      'height': '40px', 'border': '1px solid #c0c0c0', 'borderRadius': '3px',})),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H5(
                'Choose your timezone:'
                , style={'font-family': 'Courier New, monospace', 'marginLeft': 40}),
            dcc.Dropdown(id='timezone-dropdown',
                         options=[
                             {'label': 'Europe/Dublin', 'value': 'Europe/Dublin'},
                             {'label': 'Europe/Berlin', 'value': 'Europe/Berlin'},
                             {'label': 'Europe/Athens', 'value': 'Europe/Athens'},
                             {'label': 'Asia/Istanbul', 'value': 'Asia/Istanbul'},
                             {'label': 'Asia/Dubai', 'value': 'Asia/Dubai'},
                             {'label': 'Asia/Bangkok', 'value': 'Asia/Bangkok'},
                             {'label': 'Asia/Hong_Kong', 'value': 'Asia/Hong_Kong'},
                             {'label': 'Asia/Tokyo', 'value': 'Asia/Tokyo'},
                             {'label': 'Australia/Brisbane', 'value': 'Australia/Brisbane'},
                             {'label': 'Australia/Melbourne', 'value': 'Australia/Melbourne'},
                             {'label': 'Pacific/Fiji', 'value': 'Pacific/Fiji'},
                             {'label': 'America/Buenos_Aires', 'value': 'America/Montevideo'},
                             {'label': 'America/Toronto', 'value': 'America/Toronto'},
                             {'label': 'America/La_Paz', 'value': 'America/La_Paz'},
                             {'label': 'America/Mexico_City', 'value': 'America/Mexico_City'},
                             {'label': 'America/Phoenix', 'value': 'America/Phoenix'},
                             {'label': 'America/Tijuana', 'value': 'America/Tijuana'},
                             {'label': 'America/Vancouver', 'value': 'America/Vancouver'}
                         ],
                         placeholder="Select a Timezone",
                         style={'display': 'inline-block', 'width': '300px', 'marginLeft': 20,
                                'backgroundColor': '#222222'}, ),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H5(
                'Press the button to fetch your data. It can take up to 30-60 seconds to load the data'
                , style={'font-family': 'Courier New, monospace', 'marginLeft': 40}),
             dbc.Button('Fetch data!', id='fetch-data-button', n_clicks=0, className="btn btn-warning",
                        style={'display': 'inline-block', 'marginLeft': 40}),
            dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="default",
                        style={'display': 'inline-block', 'marginLeft': 60}),
            html.Br(),
            html.H5(
                'Once it has finished loading, you can go to the other tabs to see your stats'
                , style={'font-family': 'Courier New, monospace', 'marginLeft': 40}),
            ],style=tab_style,
                selected_style=tab_selected_style),
        dcc.Tab(label='Overview Stats', children=[
            html.Br(),
            html.Br(),
            html.Br(),
             html.Div([
                 html.Div([html.H3('Colour:', style={'font-family': 'Courier New, monospace'})],
                          style={'display': 'inline-block', 'width': '300px', 'marginLeft': 30}),
                 html.Div([html.H3('Dates:', style={'font-family': 'Courier New, monospace'})],
                          style={'display': 'inline-block', 'width': '300px', 'marginLeft': 80,
                                 'font-family': 'Courier New, monospace'}),
                 html.Div([html.H3('Time Class:', style={'font-family': 'Courier New, monospace'})],
                          style={'display': 'inline-block', 'width': '300px', 'marginLeft': 20,
                                 'font-family': 'Courier New, monospace'})
                      ]),
            html.Div(className='row', style={'display': 'flex'},
                     children=[
                dcc.Dropdown(id='color-dropdown',
                             options=[
                                 {'label': 'Black', 'value': 'black'},
                                 {'label': 'White', 'value': 'white'}
                             ],
                             value=['black', 'white'],
                             multi=True,
                             style={'width': '300px', 'height': '40px', 'marginLeft': 20, 'backgroundColor': '#222222'}
                             ),
                html.Div([
                    html.Div(
                                dcc.DatePickerRange(
                                    id='month-range',
                                    min_date_allowed=dt(2017, 1, 1).date(),
                                    max_date_allowed=dt.today().date(),
                                    initial_visible_month= (dt.today().date()),
                                    start_date=st_date,
                                    end_date=dt.today().date(),
                                ), style={'marginLeft': 100}
                            ),
                        ]),
                 dcc.Dropdown(id='time-class-dropdown',
                              options=[
                                  {'label': 'Blitz', 'value': 'blitz'},
                                  {'label': 'Bullet', 'value': 'bullet'},
                                  {'label': 'Rapid', 'value': 'rapid'}
                              ],
                              value=['blitz','bullet'],
                              multi=True,
                              style={'width': '300px', 'height': '40px', 'marginLeft': 20,
                                     'backgroundColor': '#222222'}
                              ),
                        ], id='wrapper'),
            html.Br(),
            html.Br(),

            ######  HOURLY AND DAILY CHARTS ######

            html.Div(className='row', style = {'display' : 'flex', 'justify-content': 'space-between'},
                     children=[
                        html.Div(
                            id="status-container",
                            children=[build_quick_stats_panel()],
                            #style={'marginLeft': 300, 'marginRight': 100, 'marginTop': 50},
                            className='col s12 m6'
                            ),
                         html.Div(
                             dcc.Graph(id='pie-chart'),
                             className='col s12 m6')
                        ]),
            html.Br(),
            html.Div(className='row', style={'display': 'flex', 'justify-content': 'space-between'},
                     children=[
                         html.Div(dcc.Graph(id='hourly-chart'),
                                  className='col s12 m6'),
                         html.Div(dcc.Graph(id='daily-elo-chart'),
                                  className='col s12 m6'),
                                ]
                     ),
                html.Br(),
                html.Br(),
                    ],style=tab_style,
                selected_style=tab_selected_style),


        ###### SECOND TAB: Custom SQL  ######

        dcc.Tab(label='Results table', children=[
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

            # TABLE
            # TABLE
            html.Br(),
            html.Br(),

            dash_table.DataTable(
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                id='table_df',
                page_size=PAGE_SIZE,
                data=[]
            ),
            html.Br(),
            html.Br(),


            html.Br()], style=tab_style, selected_style=tab_selected_style),

    dcc.Tab(label='Your News',
            children=[html.Div([
                        html.Div([],id='your-news')
                                ])
                                               ], style=tab_style,
            selected_style=tab_selected_style),
        # The  &nbsp; are to make empty lines
    dcc.Tab(label='About this site',
            children=[html.Div([
                dcc.Markdown('''
                                Created and maintained by CrowdLee Associates.
                              
                                
                                &nbsp;  
                                &nbsp;
                                &nbsp;  
                                &nbsp;      
                                
                                
                                ''')
                                ]
                                )
                        ],style=tab_style,
                selected_style=tab_selected_style)
        ], style=tabs_styles)
    ])


                                                            #####################
                                                            ###### CALLBACKS ####
                                                            #####################

###############################
###### Table error strings ####
###############################


@dash_app.callback([Output('hidden-dff', 'children'), Output('loading-output-1', 'children')],
                   [Input('fetch-data-button', 'n_clicks')],
                   [State('username', 'value'), State('timezone-dropdown', 'value')])
def user_games(n_clicks, username_input, timezone_input):
    print(username_input)
    print('that was username_input')
    print(not username_input)
    if not username_input:
        username = 'categoriaopuesta'
    else:
        username = username_input
    print(timezone_input)
    if not timezone_input:
        timezone = ['Asia/Bangkok']
    else:
        timezone = [timezone_input]
    print(timezone)
    # updates both the hidden dff and the global dff
    print('starting hidden-dff')
    baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
    #stats_url = "https://api.chess.com/pub/player/" + username + "/stats"
    #archivesUrl = baseUrl + "archives"

    all_df = None

    if not username_input:
        months_final = ['2020-04-01']
    else:
        months_final = list_months

    for date in months_final:
        print(date)
        current_year = date[0:4]  # '1998' #dt.today().strftime('%Y')
        current_month = date[5:7]  # '03'  # datetime.today().strftime('%m')
        url = baseUrl + current_year + "/" + current_month
        # filename_month = username + current_year + current_month

        tries = 3
        for i in range(tries):
            try:
                print('make url_request var')
                url_request = Request(url)
                print('get api data')
                #data = urlopen(url_request)
                with contextlib.closing(urlopen(url_request)) as data:
                    print('read into df')
                    df = pd.read_json(data)
                print('succesfully read into df')
            except:
                if i < tries - 1:  # i is zero indexed
                    print('api call failed, retrying')
                    print(i)
                    time.sleep(3)
                    continue
                else:
                    Exception('all retries failed for api')
            break
        print(len(df))
        if len(df) > 0:
            # urllib.request.urlretrieve(url, os.getcwd() + r"/" + filename_month + ".pgn")  # change
            print(".pgn has been downloaded.")
            # df = pd.read_json(os.getcwd() + r"/" + filename_month + ".pgn")
            print(df.columns)
            print(len(df))
            df1 = df["games"].apply(pd.Series)
            df2 = pd.concat([df1.drop(['white'], axis=1), df1['white'].apply(pd.Series)], axis=1)
            df3 = pd.concat([df2.drop(['black'], axis=1), df2['black'].apply(pd.Series)], axis=1)
            if 'start_time' in df3.columns:
                del df3['start_time']
            if 'tournament' in df3.columns:
                del df3['tournament']
            print(df3.columns)
            df3.columns = ['url', 'pgn', 'time_control', 'end_time', 'rated', 'fen', 'time_class',
                           'rules', 'rating_white', 'result_white', 'id_white', 'username_white', 'rating_black',
                           'result_black',
                           'id_black', 'username_black']

            df = df3
            #print(df.head())
            del df['pgn']
            del df['url']
            del df['id_white']
            del df['id_black']
            del df['fen']
            print(timezone[0])
            df['end_time'] = pd.to_datetime(df["end_time"], unit='s').astype('datetime64[ns, {0}]'.format(timezone[0]))
            df['end_time'] = df['end_time'].apply(lambda x: x.strftime('%Y-%m-%d  %H:%M:%S')).apply(
                lambda x: dt.strptime(x, '%Y-%m-%d  %H:%M:%S'))
            if all_df is not None:
                all_df = all_df.append(df)
            else:
                all_df = df
    df = all_df
    hours = df.end_time.dt.hour
    df = pd.concat([df, pd.DataFrame(hours.rename('hour'), index=df.index)], axis=1)
    df['hour'] = df['hour'].apply(lambda x: 24 if x == 0 else x)
    df['user_result'] = df['result_white']
    df.loc[df['username_black'] == username, 'user_result'] = \
    df[df['username_black'] == username]['result_black']
    df['user_color'] = 'white'
    df.loc[df['username_black'] == username, 'user_color'] = 'black'
    df['user_rating'] = df['rating_white']
    df.loc[df['username_black'] == username, 'user_rating'] = \
    df[df['username_black'] == username]['rating_black']
    df['opponent_rating'] = df['rating_white']
    df.loc[df['username_black'] != username, 'opponent_rating'] = \
    df[df['username_black'] != username]['rating_black']
    df['username_opponent'] = df['username_white']
    df.loc[df['username_black'] != username, 'username_opponent'] = \
    df[df['username_black'] != username]['username_black']

    del df['rating_white']
    del df['result_white']
    del df['rating_black']
    del df['result_black']
    del df['username_black']
    del df['username_white']
    print('finished making main table')
    print(df.columns)
    print(df.head())
    return df.to_json(orient='split'), '  '

@dash_app.callback(Output('intermediate-dff', 'children'), [Input('hidden-dff', 'children')])
def update_table(original_df):
    print('making intermediate df')
    if original_df is None:
        raise Exception('the original_df was None, aborting callback chain')
    #print(original_df)
    dff = pd.read_json(original_df, orient='split')
    return dff.to_json(orient='split')

@dash_app.callback(Output('filtered-dff', 'children'), [Input('intermediate-dff', 'children'),
                                                        Input('color-dropdown', 'value'),
                                                        Input('month-range', 'start_date'),
                                                        Input('month-range', 'end_date'),
                                                        Input('time-class-dropdown', 'value')],
                                                        [State('color-dropdown', 'value'),
                                                         State('month-range', 'start_date'),
                                                         State('month-range', 'end_date'),
                                                         State('time-class-dropdown', 'value')
                                                        ]
                   )
def update_table(original_df, colors_i, start_date_i, end_date_i, time_class_i, colors, start_date, end_date, time_class):
    dff = pd.read_json(original_df, orient='split')
    print('getting all states of filters')
    print(dff.head())
    if not colors:
        colors = ['black', 'white']
    if not start_date:
        print('no start_date')
        start_date = (dt.today().date() - timedelta(days=600))
    else:
        print('found start_date')
        print('this is the found start_date:' + start_date)
        start_date = dt.strptime(start_date, '%Y-%m-%d').date()
        print('this is the new date:')
        print(start_date)
    if not end_date:
        end_date = dt.today().date()
    else:
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    print(colors)
    print(start_date)
    print(end_date)
    print(time_class)
    dff = dff[dff['user_color'].isin(colors)]
    dff = dff[dff['time_class'].isin(time_class)]
    dff = dff[dff['rules'].isin(['chess'])]
    dff = dff[dff['end_time'].apply(lambda x: x.date() > start_date)]
    dff = dff[dff['end_time'].apply(lambda x: x.date() < end_date)]
    print(dff.head())
    return dff.to_json(orient='split')

@dash_app.callback(Output('month-range', 'initial_visible_month'), [Input('month-range', 'start_date')])
def update_visible_month(start_date):
    return start_date

@dash_app.callback([Output("table_df", "data"), Output('table_df', 'columns')], [Input('filtered-dff', 'children')])
def update_table(jsonified_cleaned_data):
    print('making table_df')
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    print(dff.head())
    return dff.values, columns


@dash_app.callback(Output('led-games-played', 'value'), [Input('filtered-dff', 'children')])
def update_style(filtered_df):
    print('getting led games played')
    dff = pd.read_json(filtered_df, orient='split')
    games_played = dff['end_time'].count()
    return games_played


@dash_app.callback(Output('led-elo', 'value'), [Input('filtered-dff', 'children')])
def update_style(filtered_df):
    print('getting led elo')
    dff = pd.read_json(filtered_df, orient='split')
    elo = dff[dff['end_time'] == max(dff['end_time'])]['user_rating'].values[0]
    return elo


####################
# CHARTS CALLBACKS #
####################

@dash_app.callback(
    Output('hourly-chart', 'figure'),
    [Input('filtered-dff', 'children')])
def display_output(filtered_dff):
    print('making hourly chart')
    dff_h = pd.read_json(filtered_dff, orient='split')

    def win_games(x):
        return (x == 'win').sum()

    def all_games(x):
        return (x != 'this is to count all').sum()

    print(dff_h.columns)
    hourly_stats = dff_h.groupby(['hour'])['user_result'].agg({all_games}).reset_index()
    hourly_ext = dff_h.groupby(['hour'])['user_result'].agg({win_games}).reset_index()
    hourly_stats = pd.merge(hourly_stats, hourly_ext, on='hour', how='left')
    hourly_stats['perc_win'] = hourly_stats['win_games'] / hourly_stats['all_games']
    h = hourly_stats[hourly_stats['all_games'] > 19]
    h.reset_index(level=0, inplace=True)
    h['win_perc'] = pd.Series(["{0:.0f}%".format(val * 100) for val in h['perc_win']], index=h.index)
    print(h.columns)
    print('hourly head')
    print(dff_h.head())
    print('hourly head 2')
    print(h.head())
    print('hourly head 3')
    print(hourly_stats.head())

    data = [
    go.Bar(
        x=h['hour'], # assign x as the dataframe column 'x'
        y=h['win_perc']
        )
    ]
    layout = go.Layout(
        hovermode='closest',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title='Hourly win %',
        font={'color': '#ffffff'},
        xaxis=dict(
            title='Hour of day',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#ffffff'
            ),
            color='#ffffff'
        ),
        yaxis=dict(
            title='win %',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#ffffff'
            ),
            color='#ffffff'
        )
    )
    return {'data': data, 'layout': layout}


@dash_app.callback(
    Output('pie-chart', 'figure'),
    [Input('filtered-dff', 'children')])
def display_output(filtered_dff):
    print('making pie chart')
    dff = pd.read_json(filtered_dff, orient='split')
    def is_win(val):
        if val in ('win', 'threecheck', 'kingofthehill'):
            return 'win'
        if val in ('insufficient', 'repetition', 'stalemate'):
            return 'draw'
        return 'lose'
    def all_games(x):
        return (x != 'this is to count all').sum()

    pie_overall = dff.groupby('user_result')['rules'].agg(all_games).reset_index()
    pie_overall['short_result'] = pie_overall.apply(lambda row: is_win(row['user_result']), axis=1)
    pie_overall = pie_overall.groupby('short_result')['rules'].agg(sum).reset_index()

    trace1 = go.Pie(
        labels=pie_overall.short_result,
        values=pie_overall["rules"],
        name='games'
    )
    data = [trace1]
    layout = go.Layout(
        hovermode='closest',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title='Overall game results',
        font={'color': '#ffffff'},
    )
    return {'data': data, 'layout': layout}

@dash_app.callback(
    Output('daily-elo-chart', 'figure'),
    [Input('filtered-dff', 'children')])
def display_output(filtered_dff):
    print('making daily elo chart')
    dff = pd.read_json(filtered_dff, orient='split')
    dff['date'] = dff['end_time'].apply(lambda x: x.date())
    daily_elo = dff.groupby(['date'])['user_rating'].agg(max).reset_index()

    trace1 = go.Scatter(
        x=daily_elo.date,
        y=daily_elo.user_rating,
        connectgaps=True
    )
    data = [trace1]
    layout = go.Layout(
        hovermode='closest',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title='Daily max ELO achieved',
        font={'color': '#ffffff'},
    )
    return {'data': data, 'layout': layout}

@dash_app.callback([Output('your-news', 'children')],
                   [Input('filtered-dff', 'children')],
                   [State('username', 'value')])
def make_news(filtered_dff, username_input):
    dff = pd.read_json(filtered_dff, orient='split')
    if not username_input:
        username_input = 'categoriaopuesta'
    max_day = max(dff['end_time']).date()
    if max_day != (dt.today().date()-timedelta(days=1)):
        titles = ns.titles_0
        sen_1 = ns.sen_1_0
        max_day_before = max(
            dff[dff['end_time'].apply(lambda x: x.date()) == max(dff['end_time']).date()]['user_rating'])
    else:
        max_yesterday = max(
            dff[dff['end_time'].apply(lambda x: x.date()) == (dt.today().date() - timedelta(days=1))]['user_rating']
            )
        max_day_before = max(
            dff[dff['end_time'].apply(lambda x: x.date()) == max(
                dff[dff['end_time'].apply(lambda x: x.date()) < (dt.today().date() - timedelta(days=1))]['end_time'])
                .date()]['user_rating']
            )
        diff_rating = max_yesterday - max_day_before
        if diff_rating > 40:
            titles = ns.titles_a
            sen_1 = ns.sen_1_a
        elif diff_rating in range(15, 40):  # intervals in range are semi-open, closed on left side
            titles = ns.titles_b
            sen_1 = ns.sen_1_b
        elif diff_rating in range(-15, 15):
            titles = ns.titles_c
            sen_1 = ns.sen_1_c
        elif diff_rating in range(-40, 15):
            titles = ns.titles_d
            sen_1 = ns.sen_1_d
        elif diff_rating < -40:
            titles = ns.titles_e
            sen_1 = ns.sen_1_e
    print(max_yesterday)
    print(max_day_before)
    abs_diff_rating = abs(diff_rating)
    #if max_yesterday > max_day_before:
    news = [html.Div(children=[
        html.Br(),
        html.Br(),
        html.Br(),
        html.H1(rd.choice(titles).format(username= username_input, pts_diff_day_before=str(abs_diff_rating)),
                style={'justify': 'center', 'align': 'center', 'text-align': 'center'}
                ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H4(
            rd.choice(sen_1).format(username=username_input)
        ),
        html.Br(),
        html.Br(),
        html.H4(
            'These were not bad performances from the opponents but not bad gets you nowhere against the gold '
            'standard in world chess. There were chances for the rival sides, even after {username}’s first '
            'checkmate, and there simply was no player of quality to overcome the cunning skills of our '
            'present era’s chess star. That was the difference in the end. {username}’s sniper vision overwhelmed'
            ' the board once and again, leaving little room to chance.'
            .format(username=username_input)
        ),
        html.Br(),
        html.Br(),
        html.H4(
                'If the second checkmate was not a masterpiece, then the third one was the consequence of a rock '
                'solid opening and then an inaccuracy on the rival’s part in the middle game, just as the match was'
                'starting to open up to complex tactical variants.'
                .format(username=username_input)
        ),
        html.Br(),
        html.Br(),
        html.H4(
                '{username} reached his highest rating of {best_elo} on {date_best}, so he is currently '
                '{diff_with_max} points {above_below} the record.  The universe of chess is eagerly awaiting the '
                'next matches to see if {username} can keep climbing the rating ladder or if the competitive '
                'pressure will make him stumble.'
                .format(username=username_input, date_best='2019-01-01', diff_with_max='200', best_elo='2800',
                        above_below='above')
        ),
        html.Br(),
        html.Br(),
        html.H4(
            '\"Every game yesterday had {username}s signature all over them, making the best out of static '
            'positional matches and pushing forward risky maneuvers. He makes chess seem like a walk in the park\"'
            ', Garry Kasparov pointed out yesterday for ESPN.'.format(username=username_input)
        )], style={'font-family': 'Times New Roman', 'marginLeft': 300, 'marginRight': 300})
            ]
    return news



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)