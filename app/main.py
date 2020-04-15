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
from datetime import datetime
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

#image_filename_2 = 'reconciliator-logo.png' # replace with your own image
#encoded_image_2 = base64.b64encode(open(image_filename_2, 'rb').read())

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


username = "categoriaopuesta" #change
baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
stats_url = "https://api.chess.com/pub/player/" + username + "/stats"
archivesUrl = baseUrl + "archives"

columns = [
    {"id": 0, "name": "time_control"},
    {"id": 1, "name": "end_time"},
    {"id": 2, "name": "rated"},
    {"id": 3, "name": "time_class"},
    {"id": 4, "name": "hour"},
    {"id": 5, "name": "user_result"},
    {"id": 6, "name": "user_color"},
    {"id": 7, "name": "user_rating"},
    {"id": 8, "name": "opponent_rating"},
    {"id": 9, "name": "username_opponent"}
    ]

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
                    html.P("Current ELO:"),
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



#####################
###### LAYOUT #######
#####################
dash_app.layout = html.Div([

    ###### HIDDEN DIV TO SHARE GLOBAL DATAFRAME
    html.Div(id='hidden-dff', style={'display': 'none'}),

    ###### TOP TITLE ######

    html.Div([
              html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image_1.decode()))],
                       style={'display': 'inline-block', 'height': '200px', 'align-items': 'center', 'justify-content': 'center',
                                'display': 'flex'}, id='logo'),

            ]),
    html.Br(),
    html.Div([
        html.Div([html.H3('Colour:', style={'font-family': 'Courier New, monospace'})],
                 style={'display': 'inline-block', 'width': '300px', 'marginLeft': 40}),
        html.Div([html.H3('Dates:', style={'font-family': 'Courier New, monospace'})],
                 style={'display': 'inline-block', 'width': '300px', 'marginLeft': 20,
                        'font-family': 'Courier New, monospace'})
    ]),
    html.Div([
        dcc.Dropdown(id='color-dropdown',
                     options=[
                         {'label': 'Black', 'value': 'black'},
                         {'label': 'White', 'value': 'white'}
                     ],
                     value=['black', 'white'],
                     multi=True,
                     style={'display': 'inline-block', 'width': '300px', 'marginLeft': 20,
                            'backgroundColor': '#222222'}),
        dcc.Dropdown(id='month-dropdown',
                     options=[
                         {'label': '2019_02', 'value': '2019_02'},
                         {'label': '2019_03', 'value': '2019_03'},
                     ],
                     value=['2019_07', '2019_08'],
                     multi=True,
                     style={'display': 'inline-block', 'width': '300px', 'marginLeft': 20,
                            'backgroundColor': '#222222'}
                     )
    ], id="wrapper"),

    ###### TABS  ######
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Tabs(id="tabs", children=[

        ###### FIRST TAB: ERROR STRING  ######

        dcc.Tab(label='Overview Stats', children=[
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

            ###### BUTTONS FOR UPDATE ######

            # html.H5(
            #     'asdfasdfasdfa'
            #     , style={'font-family': 'Courier New, monospace'}),
            html.Div(className='row', style = {'display' : 'flex', 'justify-content': 'space-between'},
                     children=[
                        html.Div(
                            id="status-container",
                            children=[build_quick_stats_panel()],
                            #style={'marginLeft': 300, 'marginRight': 100, 'marginTop': 50},
                            className='col s12 m6'
                            ),
                         html.Div(
                             dcc.Graph(id='pie-chart' #,style={'marginRight': 10}
                                 ),
                                        className='col s12 m6')
                        ]),
            html.Br(),
            dcc.Graph(id='hourly-chart', style={'display': 'inline-block', 'marginLeft': 10}),
                html.Br(),
                html.Br(),
                html.H5('Rules to be removed from database:', style={'font-family': 'Courier New, monospace'}),


                 html.Br()], style=tab_style, selected_style=tab_selected_style),


        ###### SECOND TAB: Custom SQL  ######

        dcc.Tab(label='All results table', children=[
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
            html.H5(
                'You can add a new rule with custom SQL in the table below.'
                , style={'font-family': 'Courier New, monospace'}),
            html.Br(),

            ###### BUTTONS FOR UPDATE ######

            html.Div([
                html.Br(),
            ]),
            html.Br(),
            html.Br(),
            html.H5('Rules to be removed from database:', style={'font-family': 'Courier New, monospace'}),

            html.Br(),
            html.H5('Rules to be added to database:', style={'font-family': 'Courier New, monospace'}),
            html.Br(),
            html.Br(),
            html.Br()], style=tab_style, selected_style=tab_selected_style),

    dcc.Tab(label='Your News', children=[html.Div([html.H1('Personalized news articles', style={'display': 'inline-block', 'marginLeft': 60,'marginBottom': 500, 'marginTop': 500}),
                                                         ])
                                               ], style=tab_style,
            selected_style=tab_selected_style),
        # The  &nbsp; are to make empty lines
    dcc.Tab(label='About this site', children=[html.Div([
            dcc.Markdown('''
            Created and maintained by CrowdLee Associates.
          
            
            &nbsp;  
            &nbsp;
            &nbsp;  
            &nbsp;      
            
            
            '''),
html.H1('', style={'display': 'inline-block', 'marginLeft': 60,'marginBottom': 500, 'marginTop': 50})

        ])], style=tab_style,
            selected_style=tab_selected_style)
    ], style=tabs_styles),
        ###### PROVIDER AND MONTH DROPDOWNS ######

        html.Br(),
        html.Br(),
        html.H5(
        'aaaasdölkjsdafölkjasdfölkj'
        'Somthing something'
        , style={'font-family': 'Courier New, monospace'}),

        html.Br(),
        html.Br(),
        html.H5(
        'asdfasdfasdfasdf'
        'asadfasdfaasdfasdf'
        , style={'font-family': 'Courier New, monospace'}),

        html.Br(),
        html.Br(),
        html.H5(
        'asdfasdfasdfasdf '
        'asdfasdfasdfasdfasdfsdf'
        , style={'font-family': 'Courier New, monospace'}),

        ###### JIRA EURO AMOUNTS CHART ######


        #
        # ###### JIRA EURO AMOUNTS CHART ######
        #
        # dcc.Graph(id='jira-tickets-amount', style={'display': 'inline-block', 'marginLeft': 20}),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br()
])






                                                            #####################
                                                            ###### CALLBACKS ####
                                                            #####################

###############################
###### Table error strings ####
###############################


@dash_app.callback(Output('hidden-dff', 'children'), [Input('logo','children')])
def user_games(logo):
    # updates both the hidden dff and the global dff
    username = "categoriaopuesta"  # change
    baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
    stats_url = "https://api.chess.com/pub/player/" + username + "/stats"
    archivesUrl = baseUrl + "archives"

    current_year = dt.today().strftime('%Y')
    current_month = '03'  # datetime.today().strftime('%m')
    url = baseUrl + current_year + "/" + current_month
    # filename_month = username + current_year + current_month

    url_request = Request(url)
    data = urlopen(url_request)

    df = pd.read_json(data)

    print(".pgn has been downloaded.")

    df1 = df["games"].apply(pd.Series)
    df2 = pd.concat([df1.drop(['white'], axis=1), df1['white'].apply(pd.Series)], axis=1)
    df = pd.concat([df2.drop(['black'], axis=1), df2['black'].apply(pd.Series)], axis=1)

    df.columns = ['url', 'pgn', 'time_control', 'end_time', 'rated', 'fen', 'time_class',
                   'rules', 'rating_white', 'result_white', 'id_white', 'username_white', 'rating_black',
                   'result_black',
                   'id_black', 'username_black']

    df = df
    print(df.head())
    del df['pgn']
    del df['url']
    del df['id_white']
    del df['id_black']
    del df['fen']
    df['end_time'] = pd.to_datetime(df["end_time"], unit='s').astype('datetime64[ns, Asia/Bangkok]')
    hours = df.end_time.dt.hour
    df = pd.concat([df, pd.DataFrame(hours.rename('hour'), index=df.index)], axis=1)
    df['user_result'] = df['result_white']
    df.loc[df['username_black'] == 'categoriaopuesta', 'user_result'] = \
    df[df['username_black'] == 'categoriaopuesta']['result_black']
    df['user_color'] = 'white'
    df.loc[df['username_black'] == 'categoriaopuesta', 'user_color'] = 'black'
    df['user_rating'] = df['rating_white']
    df.loc[df['username_black'] == 'categoriaopuesta', 'user_rating'] = \
    df[df['username_black'] == 'categoriaopuesta']['rating_black']
    df['opponent_rating'] = df['rating_white']
    df.loc[df['username_black'] != 'categoriaopuesta', 'opponent_rating'] = \
    df[df['username_black'] != 'categoriaopuesta']['rating_black']
    df['username_opponent'] = df['username_white']
    df.loc[df['username_black'] != 'categoriaopuesta', 'username_opponent'] = \
    df[df['username_black'] != 'categoriaopuesta']['username_black']

    del df['rating_white']
    del df['result_white']
    del df['rating_black']
    del df['result_black']
    del df['username_black']
    del df['username_white']
    print(df.columns)
    return df.to_json(orient='split')

@dash_app.callback([Output("table_df", "data"), Output('table_df', 'columns')], [Input('hidden-dff', 'children')])
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')

    return dff.values, columns


@dash_app.callback(
    Output('hourly-chart', 'figure'),
    [Input('hidden-dff', 'children')])
def display_output(hidden_dff):
    dff = pd.read_json(hidden_dff, orient='split')
    def win_games(x):
        return (x == 'win').sum()

    def all_games(x):
        return (x != 'this is to count all').sum()

    print(dff.columns)
    hourly_stats = dff.groupby(['hour'])['user_result'].agg({all_games}).reset_index()
    hourly_ext = dff.groupby(['hour'])['user_result'].agg({win_games}).reset_index()
    hourly_stats = pd.merge(hourly_stats, hourly_ext, on='hour', how='left')
    hourly_stats['perc_win'] = hourly_stats['win_games'] / hourly_stats['all_games']
    h = hourly_stats[hourly_stats['all_games'] > 19]
    h.reset_index(level=0, inplace=True)
    h['win_perc'] = pd.Series(["{0:.0f}%".format(val * 100) for val in h['perc_win']], index=h.index)
    print(dff.columns)

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
    [Input('hidden-dff', 'children')])
def display_output(hidden_dff):
    dff = pd.read_json(hidden_dff, orient='split')
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)