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
import time
import math
import urllib
import urllib.request
from datetime import datetime
import os

# user = 'YOUR_USER'
# password = 'YOUR_PASS'
# host = 'roitelligence-goeuro.cf3hhc7ijjez.eu-west-1.redshift.amazonaws.com'
# port = '5439'
# database = 'mdwh'
#
# connection_string = 'postgresql://'+user+':'+password+'@'+host+':'+port+'/'+database

# app = dash.Dash(__name__)
# server = app.server

# Style the button: http://dash-bootstrap-components.opensource.faculty.ai/l/components/button

PAGE_SIZE = 8  # For main data table
PAGE_SIZE_SQL = 3  # for custom sql data table

app = flask.Flask(__name__)
dash_app = dash.Dash(__name__, server=app,
                     url_base_pathname='/')  # , external_stylesheets=[external_style]) #dbc.themes.DARKLY

# Images/logos
image_filename_1 = 'chess-logo.png'  # replace with your own image
encoded_image_1 = base64.b64encode(open(image_filename_1, 'rb').read())

# image_filename_2 = 'reconciliator-logo.png' # replace with your own image
# encoded_image_2 = base64.b64encode(open(image_filename_2, 'rb').read())

# Serve local css
dash_app.css.config.serve_locally = True
dash_app.scripts.config.serve_locally = True

# username = "categoriaopuesta" #change
# baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
# stats_url = "https://api.chess.com/pub/player/" + username + "/stats"
# archivesUrl = baseUrl + "archives"
#
# current_year = datetime.today().strftime('%Y')
# current_month = '03' #datetime.today().strftime('%m')
# url = baseUrl + current_year + "/" + current_month
# filename_month = username + current_year + current_month
# urllib.request.urlretrieve(url, os.getcwd() + r"/" + filename_month + ".pgn") #change
# print(filename_month + ".pgn has been downloaded.")
#
# df = pd.read_json (os.getcwd()+ r"/" +filename_month + ".pgn")
#
# df1 = df["games"].apply(pd.Series)
# df2 = pd.concat([df1.drop(['white'], axis=1), df1['white'].apply(pd.Series)], axis=1)
# df3 = pd.concat([df2.drop(['black'], axis=1), df2['black'].apply(pd.Series)], axis=1)
#
# df3.columns = ['url', 'pgn', 'time_control', 'end_time', 'rated', 'fen', 'time_class',
#        'rules', 'rating_white', 'result_white', 'id_white', 'username_white', 'rating_black', 'result_black',
#        'id_black', 'username_black']
#
# df = df3
#
# del df['pgn']
# del df['url']
# del df['id_white']
# del df['id_black']
# del df['fen']
# df['end_time'] = pd.to_datetime(df["end_time"], unit='s').astype('datetime64[ns, Asia/Bangkok]')


# df = pd.read_json(r'/Users/freelance/PycharmProjects/Chesstats/Users/categoriaopuesta/categoriaopuesta202004.pgn')


# # Global dff for empty dataframes to have a reference for columns
# conn = create_engine(connection_string)
# query = "select jira_ticket, error_string, problem_source, summary, explanation from prov_recon.tool_debug_single_string;"
# global_dff = pd.read_sql_query(query, conn)
# conn.dispose()
#
#
# #Global custom sql table
# conn = create_engine(connection_string)
# query = "select jira_ticket, sql_ as sql, problem_source, summary, explanation from prov_recon.tool_debug_sql;"
# global_dff_custom = pd.read_sql_query(query, conn)
# conn.dispose()
#
# #Global pnr table
# conn = create_engine(connection_string)
# query = """ select jira_ticket, summary, count(distinct pnr) as ticket_count, max(pnr) as example_1_pnr, min(pnr) as example_2_pnr
#             from prov_recon.tool_pnr_list
#             group by 1,2
#             order by 3 desc
#             ;"""
# global_pnr = pd.read_sql_query(query, conn)
# conn.dispose()


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
    # 'fontWeight': 'bold',
    'font-size': '120%',
    'width': '300px'
}

#####################
##### FUNCTIONS #####
#####################

###############################
### Table for error strings ###
###############################


username = "categoriaopuesta"  # change
baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
stats_url = "https://api.chess.com/pub/player/" + username + "/stats"
archivesUrl = baseUrl + "archives"


def generate_table():
    # Get inital data for table:
    table = dash_table.DataTable(
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        # data=dff.to_dict('records'),
        # columns=[{"name": i, "id": i} for i in dff.columns],
        editable=False,
        row_deletable=False,
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
        id='table_df',
        page_current=math.floor(len(df) / PAGE_SIZE),
        page_size=PAGE_SIZE
    )
    return table


#
# def update_db_rows_added(rows_added):
#     unique_rules_added = rows_added[['jira_ticket', 'summary']].drop_duplicates()
#     for index_u, row_u in unique_rules_added.iterrows():
#         k = 0
#         delete_sql = """delete from prov_recon.tool_pnr_list
#                                     where jira_ticket='{jira_ticket}'
#                                         and summary='{summary}';""".format(jira_ticket=row_u['jira_ticket'],
#                                                                            summary=row_u['summary'])
#         conn = create_engine(connection_string)
#         print(delete_sql)
#         conn.execute(delete_sql)
#         conn.dispose()
#         # This loop combines strings that we want in logs and strings that we do NOT want in logs to generate the SQL.
#         for index, row in rows_added.iterrows():
#             if row_u['summary'] == row['summary'] and row_u['jira_ticket'] == row['jira_ticket']:
#                 if k == 0:
#                     k = k + 1
#                     if row['error_string'].startswith('NOT-STRING-'):
#                         not_string = 'not'
#                         error_string = row['error_string'][11:]
#                     else:
#                         not_string = ''
#                         error_string = row['error_string']
#                     reset_sql = """ insert into prov_recon.tool_pnr_list
#                                     select distinct ticket_id, '{jira_ticket}',  '{summary}', '{problem_source}'
#                                     from prov_recon.tool_debug_all_logs
#                                     where ticket_id {not_string} in (select distinct ticket_id
#                                             from  prov_recon.tool_debug_all_logs
#                                             where log_text ilike '%%{error_string}%%')
#                                     """.format(jira_ticket=row['jira_ticket'], not_string=not_string,
#                                                error_string=error_string, summary=row['summary'],
#                                                problem_source=row['problem_source'])
#                 elif k > 0:
#                     if row['error_string'].startswith('NOT-STRING-'):
#                         not_string = 'not'
#                         error_string = row['error_string'][11:]
#                     else:
#                         not_string = ''
#                         error_string = row['error_string']
#                     reset_sql = reset_sql + """and ticket_id {not_string} in (select distinct ticket_id
#                                             from  prov_recon.tool_debug_all_logs
#                                             where log_text ilike '%%{error_string}%%')
#                                             """.format(error_string=error_string, not_string=not_string)
#         conn = create_engine(connection_string)
#         print(reset_sql)
#         conn.execute(reset_sql)
#         conn.dispose()
#
#
# def update_db_rows_removed(rows_removed):
#     unique_rules_removed = rows_removed[['jira_ticket', 'summary']].drop_duplicates()
#     for index_u, row_u in unique_rules_removed.iterrows():
#         reset_sql = """delete from prov_recon.tool_pnr_list
#                     where jira_ticket='{jira_ticket}'
#                     and summary='{summary}';""".format(jira_ticket=row_u['jira_ticket'], summary=row_u['summary'])
#         conn = create_engine(connection_string)
#         print(reset_sql)
#         conn.execute(reset_sql)
#         conn.dispose()


###############################
### Table for custom sql  #####
###############################


# def generate_table_custom():
#     # Get inital data for table:
#     conn = create_engine(connection_string)
#     query_custom = """select jira_ticket, sql_ as sql, problem_source, summary, explanation from
#             prov_recon.tool_debug_sql;"""
#     dff_custom = pd.read_sql_query(query_custom, conn)
#     conn.dispose()
#     table_custom = dash_table.DataTable(
#         style_data={'whiteSpace': 'normal', 'height': 'auto'},
#         data=dff_custom.to_dict('records'),
#         columns=[{"name": n, "id": n} for n in dff_custom.columns],
#         editable=True,
#         row_deletable=True,
#         style_header={'backgroundColor': 'rgb(30, 30, 30)'},
#         style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
#         id='adding-rows-table-custom',
#         page_current=math.floor(len(global_dff_custom) / PAGE_SIZE),
#         page_size=PAGE_SIZE_SQL
#     )
#     return table_custom
#
#
# # Need to update it to do what we want with custom still
#
# def update_db_rows_added_custom(rows_added):
#     unique_rules_added = rows_added[['jira_ticket', 'summary', 'sql', 'problem_source']].drop_duplicates()
#     for index_u, row_u in unique_rules_added.iterrows():
#         delete_sql = """delete from prov_recon.tool_pnr_list
#                                     where jira_ticket='{jira_ticket}'
#                                         and summary='{summary}';""".format(jira_ticket=row_u['jira_ticket'],
#                                                                            summary=row_u['summary'])
#         conn = create_engine(connection_string)
#         print(delete_sql)
#         conn.execute(delete_sql)
#         conn.dispose()
#         reset_sql = """ insert into prov_recon.tool_pnr_list
#                         select distinct ticket_id, '{jira_ticket}',  '{summary}', '{problem_source}'
#                         from prov_recon.tool_debug_all_logs
#                         where ticket_id in ({sql})
#                         """.format(jira_ticket=row_u['jira_ticket'],
#                                    sql=row_u['sql'], summary=row_u['summary'],
#                                    problem_source=row_u['problem_source'])
#         conn = create_engine(connection_string)
#         print(reset_sql)
#         conn.execute(reset_sql)
#         conn.dispose()
#
#
# #idem needs to do sth
# def update_db_rows_removed_custom(rows_removed):
#     unique_rules_removed = rows_removed[['jira_ticket', 'summary']].drop_duplicates()
#     for index_u, row_u in unique_rules_removed.iterrows():
#         reset_sql = """delete from prov_recon.tool_pnr_list
#                     where jira_ticket='{jira_ticket}'
#                     and summary='{summary}';""".format(jira_ticket=row_u['jira_ticket'], summary=row_u['summary'])
#         conn = create_engine(connection_string)
#         print(reset_sql)
#         conn.execute(reset_sql)
#         conn.dispose()


#####################
###### LAYOUT #######
#####################
dash_app.layout = html.Div([

    ###### HIDDEN DIV TO SHARE GLOBAL DATAFRAME
    html.Div(id='hidden-dff', style={'display': 'none'}),
    #    html.Div(id='hidden-dff-custom', style={'display': 'none'}),

    ###### CONFIRM DIALOG FOR DB UPDATE ######

    # dcc.ConfirmDialog(id='confirm', message='Danger zone: Are you sure you want to continue?'),
    # dcc.ConfirmDialog(id='confirm-custom', message='Danger zone: Are you sure you want to continue?'),
    # html.Br(),

    ###### TOP TITLE ######

    html.Div([
        html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image_1.decode()))],
                 style={'display': 'inline-block', 'height': '120px', 'marginLeft': 20}),
        #             html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image_2.decode()))],
        #                      style={'display': 'inline-block', 'height': '50px', 'width': '200px',
        #                             'vertical-align': 'bottom'})
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    ###### TABS  ######

    dcc.Tabs(id="tabs", children=[

        ###### FIRST TAB: ERROR STRING  ######

        dcc.Tab(label='Overview Stats', children=[
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

            # TABLE
            html.Br(),
            html.Br(),
            # html.H5('You can add a new rule in the table below.  This will help you identify PNRs whose logs match a certain string or set of strings.'
            #         ''
            #         'Important: JIRA Ticket + Summary should be unique to each new rule, you will not be able to duplicate this.'
            #         , style={'font-family': 'Courier New, monospace'}),
            generate_table(),
            html.Br(),

            ###### BUTTONS FOR UPDATE ######
            html.H5(
                'In order to make the charts below display the effect of the new rule, you need to Update DB (orange button).  Hold on 10-20 seconds for '
                'the charts to be updated'
                , style={'font-family': 'Courier New, monospace'}),
            html.Div([
                html.Br(),
                # dbc.Button('Add new rule', id='adding-rows-button', n_clicks=0, className="btn btn-primary",
                #            style={'display': 'inline-block', 'marginLeft': 20}),
                # dbc.Button('Update DB', id='update-db', n_clicks=0, className="btn btn-warning",
                #            style={'display': 'inline-block', 'marginLeft': 40}),
                # dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="default",
                #             style={'display': 'inline-block', 'marginLeft': 60}),
            ]),
            html.Br(),
            html.Br(),
            html.H5('Rules to be removed from database:', style={'font-family': 'Courier New, monospace'}),

            # html.Div(id='db-update-placeholder', style={'display': 'none'}),

            ###### ROWS REMOVED: ######

            # dash_table.DataTable(
            #         style_data={
            #                     'whiteSpace': 'normal',
            #                     'height': 'auto'
            #                     },
            #         data=[{}],
            #         columns=[{"name": i, "id": i} for i in df.columns],
            #         editable=False,
            #         row_deletable=False,
            #         style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            #         style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
            #         id='rows-removed'
            #         ),
            # html.Br(),
            # html.H5('Rules to be added to database:', style={'font-family': 'Courier New, monospace'}),
            # dash_table.DataTable(
            #         style_data={
            #                     'whiteSpace': 'normal',
            #                     'height': 'auto'
            #                     },
            #         data=[{}],
            #         columns=[{"name": i, "id": i} for i in df.columns],
            #         editable=False,
            #         row_deletable=False,
            #         style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            #         style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
            #         id='rows-added'
            #         ),
            # html.Br(),
            # html.Br(),
            html.Br()], style=tab_style, selected_style=tab_selected_style),

        ###### SECOND TAB: Custom SQL  ######

        dcc.Tab(label='Explorer', children=[
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

            # TABLE
            html.Br(),
            html.Br(),
            html.H5(
                'You can add a new rule with custom SQL in the table below.'
                , style={'font-family': 'Courier New, monospace'}),
            html.Br(),

            ###### BUTTONS FOR UPDATE ######

            html.Div([
                html.Br(),
                # dbc.Button('Add new rule', id='adding-rows-button-custom', n_clicks=0, className="btn btn-primary",
                #            style={'display': 'inline-block', 'marginLeft': 20}),
                # dbc.Button('Update DB', id='update-db-custom', n_clicks=0, className="btn btn-warning", style={'display':
                #                                                                                         'inline-block',
                #                                                                                         'marginLeft': 40}),
                # dcc.Loading(id="loading-1-custom", children=[html.Div(id="loading-output-1-custom")], type="default",
                #            style={'display': 'inline-block', 'marginLeft': 60}),
            ]),
            html.Br(),
            html.Br(),
            html.H5('Rules to be removed from database:', style={'font-family': 'Courier New, monospace'}),

            # html.Div(id='db-update-placeholder-custom', style={'display': 'none'}),

            ###### ROWS REMOVED: ######
            #
            # dash_table.DataTable(
            #     style_data={'whiteSpace': 'normal', 'height': 'auto'},
            #     data=[{}],
            #     columns=[{"name": i, "id": i} for i in global_dff_custom.columns],
            #     editable=False,
            #     row_deletable=False,
            #     style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            #     style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
            #     id='rows-removed-custom'
            # ),
            html.Br(),
            html.H5('Rules to be added to database:', style={'font-family': 'Courier New, monospace'}),
            # dash_table.DataTable(
            #     style_data={
            #         'whiteSpace': 'normal',
            #         'height': 'auto'
            #     },
            #     data=[{}],
            #     columns=[{"name": i, "id": i} for i in global_dff_custom.columns],
            #     editable=False,
            #     row_deletable=False,
            #     style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            #     style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
            #     id='rows-added-custom'
            # ),
            html.Br(),
            html.Br(),
            html.Br()], style=tab_style, selected_style=tab_selected_style),

        dcc.Tab(label='About this site', children=[html.Div([html.H1(
            'This feature is not implemented yet (search box and display logs for pnr)',
            style={'display': 'inline-block', 'marginLeft': 60, 'marginBottom': 500, 'marginTop': 500}),
                                                             ])
                                                   ], style=tab_style,
                selected_style=tab_selected_style),
        # The  &nbsp; are to make empty lines
        dcc.Tab(label='Documentation', children=[html.Div([
            dcc.Markdown('''
            an example, this SQL will be fine to paste into the table

            &nbsp;    


            ### PNR Search

            &nbsp;
            &nbsp;
            This feature is to be implemented, basically a search box for PNRs and a datatable displaying all logs ordered by timestamp.
            &nbsp;
            &nbsp;  
            &nbsp;
            &nbsp;  
            &nbsp;      


            '''),
            html.H1('', style={'display': 'inline-block', 'marginLeft': 60, 'marginBottom': 500, 'marginTop': 50})

        ])], style=tab_style,
                selected_style=tab_selected_style)
    ], style=tabs_styles),
    ###### PROVIDER AND MONTH DROPDOWNS ######
    html.Div([
        html.Div([html.H3('Providers:', style={'font-family': 'Courier New, monospace'})],
                 style={'display': 'inline-block', 'width': '300px', 'marginLeft': 40}),
        html.Div([html.H3('Months:', style={'font-family': 'Courier New, monospace'})],
                 style={'display': 'inline-block', 'width': '300px', 'marginLeft': 20,
                        'font-family': 'Courier New, monospace'})
    ]),
    html.Div([
        dcc.Dropdown(id='provider-dropdown',
                     options=[
                         {'label': 'Deutschebahn', 'value': 'deutscheBahn'},
                         {'label': 'SNCB', 'value': 'SNCB'},
                         {'label': 'Renfe', 'value': 'renfe'},
                         {'label': 'travelFusion', 'value': 'travelFusion'}
                     ],
                     value=['deutscheBahn', 'SNCB'],
                     multi=True,
                     style={'display': 'inline-block', 'width': '300px', 'marginLeft': 20,
                            'backgroundColor': '#222222'}),
        dcc.Dropdown(id='month-dropdown',
                     options=[
                         {'label': '2019_02', 'value': '2019_02'},
                         {'label': '2019_03', 'value': '2019_03'},
                         {'label': '2019_04', 'value': '2019_04'},
                         {'label': '2019_05', 'value': '2019_05'},
                         {'label': '2019_06', 'value': '2019_06'},
                         {'label': '2019_07', 'value': '2019_07'},
                         {'label': '2019_08', 'value': '2019_08'}
                     ],
                     value=['2019_07', '2019_08'],
                     multi=True,
                     style={'display': 'inline-block', 'width': '300px', 'marginLeft': 20,
                            'backgroundColor': '#222222'}
                     )
    ], id="wrapper"),
    html.Br(),
    html.Br(),
    html.H5(
        'aaaasdölkjsdafölkjasdfölkj'
        'Somthing something'
        , style={'font-family': 'Courier New, monospace'}),
    # dash_table.DataTable(
    #     style_data={'whiteSpace': 'normal', 'height': 'auto'},
    #     data=[{}],
    #     columns=[{"name": i, "id": i} for i in global_pnr.columns],
    #     editable=False,
    #     row_deletable=False,
    #     style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    #     style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
    #     id='pnr-helper'
    # ),
    html.Br(),
    html.Br(),
    html.H5(
        'asdfasdfasdfasdf'
        'asadfasdfaasdfasdf'
        , style={'font-family': 'Courier New, monospace'}),
    ###### JIRA COUNTS CHART ######

    # dcc.Graph(id='jira-ticket-count', style={'display': 'inline-block', 'marginLeft': 10}),
    #
    # ###### JIRA EURO AMOUNTS CHART ######
    #
    # dcc.Graph(id='jira-ticket-amount', style={'display': 'inline-block', 'marginLeft': 20}),
    html.Br(),
    html.Br(),
    html.H5(
        'asdfasdfasdfasdf '
        'asdfasdfasdfasdfasdfsdf'
        , style={'font-family': 'Courier New, monospace'}),

    ###### JIRA EURO AMOUNTS CHART ######

    # dcc.Graph(id='jira-tickets-count', style={'display': 'inline-block', 'marginLeft': 10}),
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


###### ADD ROWS IN TABLE ######
#
# @dash_app.callback(
#     Output('adding-rows-table', 'data'),
#     [Input('adding-rows-button', 'n_clicks'),
#      Input('hidden-dff', 'children')],
#     [State('adding-rows-table', 'data'),
#      State('adding-rows-table', 'columns'),
#      State('adding-rows-button', 'n_clicks_timestamp')])
# def add_row(n_clicks, hidden_dff, rows, columns, n_clicks_timestamp):
#     if n_clicks > 0:
#         if (time.time()*1000 - n_clicks_timestamp)<1000: #Checks if the callback was triggered by adding rule or by db update
#             rows.append({c['id']: '' for c in columns})
#             return rows
#     dff = pd.read_json(hidden_dff, orient='split')
#     return dff.to_dict('records')
#
#
# ###### SHOW REMOVED ROWS ######
#
# @dash_app.callback(
#     Output('rows-removed', 'data'),
#     [Input('adding-rows-table', 'data'), Input('hidden-dff', 'children')],
#     [State('adding-rows-table', 'columns'),
#      State('adding-rows-table', 'data')])
# def show_rows_removed(change, hidden_dff, columns, rows):
#     if hidden_dff:
#         dff = pd.read_json(hidden_dff, orient='split')
#         df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#         #Find rows that have been removed or changed (so we will delete this in the database)
#         df_all = dff.merge(df.drop_duplicates(), on=['jira_ticket', 'error_string', 'summary', 'explanation',
#                                                      'problem_source'],
#                        how='left', indicator=True)
#         rows_removed = dff[df_all['_merge'] == 'left_only']
#         return rows_removed.to_dict('records')
#
# ###### SHOW ADDED ROWS ######
#
# @dash_app.callback(
#     Output('rows-added', 'data'),
#     [Input('adding-rows-table', 'data'), Input('hidden-dff', 'children')],
#     [State('adding-rows-table', 'columns'),
#      State('adding-rows-table', 'data')])
# def show_rows_removed(change, hidden_dff, columns, rows):
#     if hidden_dff:
#         dff = pd.read_json(hidden_dff, orient='split')
#         df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#         #Find rows that have been removed or changed (so we will delete this in the database)
#         df_all = df.merge(dff.drop_duplicates(), on=['jira_ticket', 'error_string', 'summary', 'explanation', 'problem_source'],
#                        how='left', indicator=True)
#         rows_removed = df[df_all['_merge'] == 'left_only']
#         return rows_removed.to_dict('records')
#
#
# ###### CONFIRM BUTTON FOR DB UPDATE ######
#
# @dash_app.callback(Output('confirm', 'displayed'),
#               [Input('update-db', 'n_clicks')])
# def display_confirm(n_clicks):
#     if n_clicks == 0:
#         return False
#     return True
#
# ###### global_dff initial value ######
#

@dash_app.callback(Output('hidden-dff', 'children'))
def user_games():
    # updates both the hidden dff and the global dff
    username = "categoriaopuesta"  # change
    baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
    stats_url = "https://api.chess.com/pub/player/" + username + "/stats"
    archivesUrl = baseUrl + "archives"

    current_year = datetime.today().strftime('%Y')
    current_month = '03'  # datetime.today().strftime('%m')
    url = baseUrl + current_year + "/" + current_month
    filename_month = username + current_year + current_month
    urllib.request.urlretrieve(url, os.getcwd() + r"/" + filename_month + ".pgn")  # change
    print(filename_month + ".pgn has been downloaded.")

    df = pd.read_json(os.getcwd() + r"/" + filename_month + ".pgn")

    df1 = df["games"].apply(pd.Series)
    df2 = pd.concat([df1.drop(['white'], axis=1), df1['white'].apply(pd.Series)], axis=1)
    df3 = pd.concat([df2.drop(['black'], axis=1), df2['black'].apply(pd.Series)], axis=1)

    df3.columns = ['url', 'pgn', 'time_control', 'end_time', 'rated', 'fen', 'time_class',
                   'rules', 'rating_white', 'result_white', 'id_white', 'username_white', 'rating_black',
                   'result_black',
                   'id_black', 'username_black']

    df = df3

    del df['pgn']
    del df['url']
    del df['id_white']
    del df['id_black']
    del df['fen']
    df['end_time'] = pd.to_datetime(df["end_time"], unit='s').astype('datetime64[ns, Asia/Bangkok]')
    return df.to_json(orient='split')


@dash_app.callback(Output('table_df', 'children'), [Input('hidden-dff', 'children')])
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    return dff


# ###### pnr-helper table ######
#
# @dash_app.callback(Output('pnr-helper', 'data'),
#                    [Input('update-db', 'n_clicks'),
#                     Input('db-update-placeholder', 'children'),
#                     Input('db-update-placeholder-custom', 'children'),
#                     Input('provider-dropdown', 'value'), Input('month-dropdown', 'value')])
# def global_data(n_clicks, db_placeholder, db_placeholder_custom, provider, month):
#     #updates both the hidden dff and the global dff
#     global global_pnr
#     conn = create_engine(connection_string)
#     query = """ select jira_ticket, summary, --we want to pick random examples, hence the window functions, could probably have written this simpler
# 				count(distinct pnr) as ticket_count,
# 				coalesce(max(example_1),max(example_1_l)) as example_1_pnr,
# 				coalesce(min(example_2),min(example_2_l)) as example_2_pnr
#                 from (
#                 select case when jira_ticket is null then 'not_yet_debugged' else jira_ticket end as jira_ticket, summary,
# 				coalesce(p.pnr, l.pnr) as pnr,
# 				example_1, example_2,
# 				first_value(p.pnr ignore nulls) over (partition by jira_ticket, summary order by md5(p.pnr||random()::varchar)
# 								rows between unbounded preceding and unbounded following) as example_1_l,
# 				last_value(p.pnr ignore nulls) over (partition by jira_ticket, summary order by md5(p.pnr||random()::varchar)
# 								rows between unbounded preceding and unbounded following) as example_2_l
#                 from (select distinct ticket_id as pnr from prov_recon.tool_debug_all_logs) p
#                 left join (
# 				select jira_ticket, summary, pnr,
# 						first_value(pnr) over (partition by jira_ticket, summary order by md5(pnr||random()::varchar)
# 											rows between unbounded preceding and unbounded following) as example_1,
# 						last_value(pnr) over (partition by jira_ticket, summary order by md5(pnr||random()::varchar)
# 											rows between unbounded preceding and unbounded following) as example_2
# 			    from prov_recon.tool_pnr_list
# 			    ) l on p.pnr=l.pnr
#                 where p.pnr in (select distinct pnr from prov_recon.full_provider_bucket_1_all_time
#                                                         where provider in ('{provider}') and substring(first_month_issue, 1,7) in ('{month}')
#                                                         and pnr is not null
#                                     union select 'string so that we dont have an in-null condition for ticket_id'
#                                                         )
#                 )
#                 group by 1,2 order by 3 desc
#                 ;	""".format(provider="','".join(provider), month="','".join(month))
#     global_pnr = pd.read_sql_query(query, conn)
#     conn.dispose()
#     return global_pnr.to_dict('records')
#
# ###### DB UPDATE ######
#
# @dash_app.callback(
#     [Output('db-update-placeholder', 'children'), Output("loading-output-1", "children")],
#     [Input('confirm', 'submit_n_clicks')],
#     [State('adding-rows-table', 'data'),
#      State('adding-rows-table', 'columns'),
#      State('hidden-dff', 'children')])
# def update_db(submit_n_clicks, rows, columns, hidden_dff):
#     if hidden_dff:
#         dff = pd.read_json(hidden_dff, orient='split')
#         df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#         #Find rows that have been removed or changed (so we will delete this in the database)
#         df_all = dff.merge(df.drop_duplicates(), on=['jira_ticket', 'error_string', 'summary', 'explanation',
#                                                      'problem_source'], how='left', indicator=True)
#         rows_removed = dff[df_all['_merge'] == 'left_only']
#         if len(rows_removed.index) > 0:
#             for index, row in rows_removed.iterrows():
#                 reset_sql = """delete from prov_recon.tool_debug_single_string
#                         where jira_ticket = '{jira_ticket}'
#                         and error_string = '{error_string}'
#                         and summary='{summary}'""".format(jira_ticket=row['jira_ticket'].replace("'", "''"),
#                                                           error_string=row['error_string'].replace("'", "''"),
#                                                           summary=row['summary'].replace("'", "''"))
#                 conn = create_engine(connection_string)
#                 conn.execute(reset_sql)
#                 conn.dispose()
#         #Find rows new rows or changes (so we can add them in the database)
#         df_all = df.merge(dff.drop_duplicates(), on=['jira_ticket', 'error_string', 'summary', 'explanation',
#                                                      'problem_source'], how='left', indicator=True)
#         rows_added = df[df_all['_merge'] == 'left_only']
#         if len(rows_added.index) > 0:
#             check_index = 0  # So that it only checks once for multi string searches.
#             for index, row in rows_added.iterrows():
#                 # First check if ticket-summary already exists
#                 if check_index == 0:
#                     check_sql = """select count(*) from prov_recon.tool_debug_single_string where
#                                 jira_ticket='{jira_ticket}' and summary='{summary}'""" \
#                         .format(jira_ticket=row['jira_ticket'].replace("'", "''"),
#                                 summary=row['summary'].replace("'", "''"))
#                     conn = create_engine(connection_string)
#                     check_results = conn.execute(check_sql).fetchall()
#                     conn.dispose()
#                     if check_results[0][0] != 0:
#                         return ' ', html.Div([html.Br(),
#                                               html.Br(),
#                                               html.Br(),
#                                               html.Div(
#                                                   'Summary-Jira_ticket combination already exists, please choose a new summary',
#                                                   style={'color': 'red', 'fontSize': 30, 'marginLeft': 40}
#                                                   )
#                                               ])
#                 check_index = 1
#                 added_sql = """insert into prov_recon.tool_debug_single_string values
#                             ('{jira_ticket}', '{error_string}','{problem_source}', 0,0 ,
#                             '{summary}', '{explanation}', getdate())"""\
#                     .format(jira_ticket=row['jira_ticket'].replace("'", "''")
#                             , error_string=row['error_string'].replace("'", "''")
#                             , problem_source=row['problem_source'].replace("'", "''")
#                             , summary=row['summary'].replace("'", "''")
#                             , explanation=row['explanation'].replace("'", "''"))
#                 conn = create_engine(connection_string)
#                 conn.execute(added_sql)
#                 conn.dispose()
#
#         if not rows_removed.empty:
#             update_db_rows_removed(rows_removed)
#         if not rows_added.empty:
#             update_db_rows_added(rows_added)
#
#     return 'something', ' '
#
#
# ###############################
# ###### Table custom SQL  ######
# ###############################
#
#
# ###### ADD ROWS IN TABLE ######
#
# @dash_app.callback(
#     Output('adding-rows-table-custom', 'data'),
#     [Input('adding-rows-button-custom', 'n_clicks'),
#      Input('hidden-dff-custom', 'children')],
#     [State('adding-rows-table-custom', 'data'),
#      State('adding-rows-table-custom', 'columns'),
#      State('adding-rows-button-custom', 'n_clicks_timestamp')])
# def add_row_custom(n_clicks, hidden_dff, rows, columns, n_clicks_timestamp):
#     if n_clicks > 0:
#         if (
#                 time.time() * 1000 - n_clicks_timestamp) < 1000:  # Checks if the callback was triggered by adding rule or by db update
#             rows.append({c['id']: '' for c in columns})
#             return rows
#     dff = pd.read_json(hidden_dff, orient='split')
#     return dff.to_dict('records')
#
#
# ###### SHOW REMOVED ROWS ######
#
# @dash_app.callback(
#     Output('rows-removed-custom', 'data'),
#     [Input('adding-rows-table-custom', 'data'), Input('hidden-dff-custom', 'children')],
#     [State('adding-rows-table-custom', 'columns'),
#      State('adding-rows-table-custom', 'data')])
# def show_rows_removed_custom(change, hidden_dff, columns, rows):
#     if hidden_dff:
#         dff = pd.read_json(hidden_dff, orient='split')
#         df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#         # Find rows that have been removed or changed (so we will delete this in the database)
#         df_all = dff.merge(df.drop_duplicates(), on=['jira_ticket', 'sql', 'summary', 'explanation',
#                                                      'problem_source'],
#                            how='left', indicator=True)
#         rows_removed = dff[df_all['_merge'] == 'left_only']
#         return rows_removed.to_dict('records')
#
#
# ###### SHOW ADDED ROWS ######
#
# @dash_app.callback(
#     Output('rows-added-custom', 'data'),
#     [Input('adding-rows-table-custom', 'data'), Input('hidden-dff-custom', 'children')],
#     [State('adding-rows-table-custom', 'columns'),
#      State('adding-rows-table-custom', 'data')])
# def show_rows_removed_custom(change, hidden_dff, columns, rows):
#     if hidden_dff:
#         dff = pd.read_json(hidden_dff, orient='split')
#         df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#         # Find rows that have been removed or changed (so we will delete this in the database)
#         df_all = df.merge(dff.drop_duplicates(),
#                           on=['jira_ticket', 'sql', 'summary', 'explanation', 'problem_source'],
#                           how='left', indicator=True)
#         rows_removed = df[df_all['_merge'] == 'left_only']
#         return rows_removed.to_dict('records')
#
#
# ###### CONFIRM BUTTON FOR DB UPDATE ######
#
# @dash_app.callback(Output('confirm-custom', 'displayed'),
#                    [Input('update-db-custom', 'n_clicks')])
# def display_confirm_custom(n_clicks):
#     if n_clicks == 0:
#         return False
#     return True
#
#
# ###### global_dff initial value ######
#
# @dash_app.callback(Output('hidden-dff-custom', 'children'),
#                    [Input('update-db-custom', 'n_clicks'),
#                     Input('db-update-placeholder-custom', 'children')])
# def global_data_custom(n_clicks, db_placeholder):
#     # updates both the hidden dff and the global dff
#     global global_dff_custom
#     conn = create_engine(connection_string)
#     query = """select jira_ticket, sql_ as sql, problem_source, summary, explanation
#                 from prov_recon.tool_debug_sql;"""
#     global_dff_custom = pd.read_sql_query(query, conn)
#     conn.dispose()
#     return global_dff_custom.to_json(orient='split')
#
#
# ###### DB UPDATE ######
#
# @dash_app.callback(
#     [Output('db-update-placeholder-custom', 'children'), Output("loading-output-1-custom", "children")],
#     [Input('confirm-custom', 'submit_n_clicks')],
#     [State('adding-rows-table-custom', 'data'),
#      State('adding-rows-table-custom', 'columns'),
#      State('hidden-dff-custom', 'children')])
# def update_db_custom(submit_n_clicks, rows, columns, hidden_dff):
#     try:
#         if hidden_dff:
#             dff = pd.read_json(hidden_dff, orient='split')
#
#             df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#             # Find rows that have been removed or changed (so we will delete this in the database)
#             df_all = dff.merge(df.drop_duplicates(),
#                                on=['jira_ticket', 'sql', 'summary', 'explanation', 'problem_source'],
#                                how='left', indicator=True)
#             rows_removed = dff[df_all['_merge'] == 'left_only']
#             if len(rows_removed.index) > 0:
#                 for index, row in rows_removed.iterrows():
#                     reset_sql = """delete from prov_recon.tool_debug_sql
#                             where jira_ticket = '{jira_ticket}'
#                             and summary='{summary}'""".format(jira_ticket=row['jira_ticket'].replace("'", "''")
#                                                               , summary=row['summary'].replace("'", "''"))
#                     conn = create_engine(connection_string)
#                     conn.execute(reset_sql)
#                     conn.dispose()
#                     # Find rows new rows or changes (so we can add them in the database)
#             df_all = df.merge(dff.drop_duplicates(),
#                               on=['jira_ticket', 'sql', 'summary', 'explanation', 'problem_source'],
#                               how='left', indicator=True)
#             rows_added = df[df_all['_merge'] == 'left_only']
#             if not rows_removed.empty:
#                 update_db_rows_removed_custom(rows_removed)
#             if not rows_added.empty:
#                 update_db_rows_added_custom(rows_added)
#             if len(rows_added.index) > 0:
#                 for index, row in rows_added.iterrows():
#                     # First check if ticket-summary already exists
#                     check_sql = """select count(*) from prov_recon.tool_debug_sql where
#                                 jira_ticket='{jira_ticket}' and summary='{summary}'"""\
#                                 .format(jira_ticket=row['jira_ticket'].replace("'", "''"),
#                                         summary=row['summary'].replace("'", "''"))
#                     conn = create_engine(connection_string)
#                     check_results = conn.execute(check_sql).fetchall()
#                     conn.dispose()
#                     if check_results[0][0] != 0:
#                         return ' ', html.Div([html.Br(),
#                                               html.Br(),
#                                               html.Br(),
#                                               html.Div('Summary-Jira_ticket combination already exists, please choose a new summary',
#                                                        style={'color': 'red', 'fontSize': 30, 'marginLeft': 40}
#                                                        )
#                                               ])
#                     added_sql = """insert into prov_recon.tool_debug_sql values
#                                 ('{jira_ticket}', '{sql}','{problem_source}', 0,0 ,
#                                 '{summary}', '{explanation}', getdate())""" \
#                         .format(jira_ticket=row['jira_ticket'].replace("'", "''")
#                                 , sql=row['sql'].replace("'", "''")
#                                 , problem_source=row['problem_source'].replace("'", "''")
#                                 , summary=row['summary'].replace("'", "''")
#                                 , explanation=row['explanation'].replace("'", "''"))
#                     conn = create_engine(connection_string)
#                     conn.execute(added_sql)
#                     conn.dispose()
#
#         return 'something', ' '
#     except:
#         return ' ', html.Div([html.Br(),
#                               html.Br(),
#                               html.Br(),
#                               html.Div('SQL could not be run, please check documentation',
#                                        style={'color': 'red', 'fontSize': 30, 'marginLeft': 40}
#                                        )
#                               ])
#
#
#
# ### DISPLAY JIRA TICKET COUNT
# @dash_app.callback(
#     Output('jira-ticket-count', 'figure'),
#     [Input('db-update-placeholder', 'children'),
#      Input('db-update-placeholder-custom', 'children'),
#      Input('provider-dropdown', 'value'), Input('month-dropdown', 'value')])
# def display_output(db_placeholder, dbc, provider, month):
#     conn = create_engine(connection_string)
#
#     query = """select case when jira_ticket is null then 'not_yet_debugged' else jira_ticket end, count(distinct p.pnr) as ticket_count
#                 from (select distinct ticket_id as pnr from prov_recon.tool_debug_all_logs) p
#                 left join prov_recon.tool_pnr_list l on p.pnr=l.pnr
#                 where p.pnr in (select distinct pnr from prov_recon.full_provider_bucket_1_all_time
#                                                         where provider in ('{provider}') and substring(first_month_issue, 1,7) in ('{month}')
#                                                         and pnr is not null
#                                     union select 'string so that we dont have an in-null condition for ticket_id'
#                                                         )
#                 group by 1 order by 2 desc;""".format(provider="','".join(provider), month="','".join(month))
#     print(query)
#     dff = pd.read_sql_query(query, conn)
#     conn.dispose()
#     data = [
#     go.Bar(
#         x=dff['jira_ticket'], # assign x as the dataframe column 'x'
#         y=dff['ticket_count']
#         )
#     ]
#     layout = go.Layout(
#         hovermode='closest',
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         title='JIRA Issue counts',
#         font={'color': '#ffffff'},
#         xaxis=dict(
#             title='JIRA Ticket',
#             titlefont=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#ffffff'
#             ),
#             color='#ffffff'
#         ),
#         yaxis=dict(
#             title='Ticket Count',
#             titlefont=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#ffffff'
#             ),
#             color='#ffffff'
#         )
#     )
#
#     return {'data': data, 'layout': layout}
#
#
# ### DISPLAY JIRA TICKET  AMOUNT
# @dash_app.callback(
#     Output('jira-ticket-amount', 'figure'),
#     [Input('db-update-placeholder', 'children'),
#      Input('db-update-placeholder-custom', 'children'),
#      Input('provider-dropdown', 'value'), Input('month-dropdown', 'value')])
# def display_output(db_placeholder, dbc, provider, month):
#     conn = create_engine(connection_string)
#
#     query = """select case when jira_ticket is null then 'not_yet_debugged' else jira_ticket end, sum(provider_amount) as euro_amount
#                 from (select distinct ticket_id as pnr from prov_recon.tool_debug_all_logs) p
#                 left join (select pnr, sum(provider_amount) as provider_amount from prov_recon.full_provider_bucket_1_all_time group by 1) a on p.pnr=a.pnr
#                 left join prov_recon.tool_pnr_list l on a.pnr=l.pnr --duplication is ok here, we want amounts in each jira bucket
#                 where p.pnr in (select distinct pnr from prov_recon.full_provider_bucket_1_all_time
#                                                         where provider in ('{provider}') and substring(first_month_issue, 1, 7) in ('{month}')
#                                                         and pnr is not null
#                                     union select 'string so that we dont have an in-null condition for ticket_id' -- wait is this really needed? todo: check
#                                                         )
#                 group by 1 order by 2 desc;""".format(provider="','".join(provider), month="','".join(month))
#     print(query)
#     dff = pd.read_sql_query(query, conn)
#     conn.dispose()
#     data = [
#         go.Bar(
#             x=dff['jira_ticket'],  # assign x as the dataframe column 'x'
#             y=dff['euro_amount']
#         )
#     ]
#     layout = go.Layout(
#         hovermode='closest',
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         title='JIRA Euro Amounts',
#         font={'color': '#ffffff'},
#         xaxis=dict(
#             title='JIRA Ticket',
#             titlefont=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#ffffff'
#             ),
#             color='#ffffff'
#         ),
#         yaxis=dict(
#             title='Euro amount',
#             titlefont=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#ffffff'
#             ),
#             color='#ffffff'
#         )
#     )
#
#     return {'data': data, 'layout': layout}
#
# ### DISPLAY JIRA MULTIPLE TICKET COUNT
# @dash_app.callback(
#     Output('jira-tickets-count', 'figure'),
#      [Input('db-update-placeholder', 'children'),
#        Input('db-update-placeholder-custom', 'children'),
#      Input('provider-dropdown', 'value'), Input('month-dropdown', 'value')])
# def display_output(db_placeholder, dbc, provider, month):
#     conn = create_engine(connection_string)
#
#     query = """select jira_tickets, count(distinct pnr) as ticket_count
#                 from (
#                 select pnr, listagg(distinct jira_ticket, '; ') within group (order by jira_ticket) as jira_tickets
#                 from prov_recon.tool_pnr_list
#                 group by pnr
#                 )
#                 where pnr in (select distinct pnr from prov_recon.full_provider_bucket_1_all_time
#                                                         where provider in ('{provider}') and substring(first_month_issue, 1, 7) in ('{month}')
#                                                         and pnr is not null
#                                     union select 'string so that we dont have an in-null condition for ticket_id' -- wait is this really needed? todo: check
#                                                         )
#                 group by jira_tickets order by ticket_count desc;""".format(provider="','".join(provider), month="','".join(month))
#     print(query)
#     dff = pd.read_sql_query(query, conn)
#     conn.dispose()
#     data = [
#         go.Bar(
#             x=dff['jira_tickets'],  # assign x as the dataframe column 'x'
#             y=dff['ticket_count']
#         )
#     ]
#     layout = go.Layout(
#         hovermode='closest',
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         title='JIRA Tickets combination',
#         font={'color': '#ffffff'},
#         xaxis=dict(
#             title='JIRA Ticket',
#             titlefont=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#ffffff'
#             ),
#             color='#ffffff'
#         ),
#         yaxis=dict(
#             title='Ticket count',
#             titlefont=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#ffffff'
#             ),
#             color='#ffffff'
#         )
#     )
#
#     return {'data': data, 'layout': layout}
#
# ### DISPLAY JIRA MULTIPLE TICKET AMOUNT
# @dash_app.callback(
#     Output('jira-tickets-amount', 'figure'),
#      [Input('db-update-placeholder', 'children'),
#        Input('db-update-placeholder-custom', 'children'),
#      Input('provider-dropdown', 'value'), Input('month-dropdown', 'value')])
# def display_output(db_placeholder, dbc, provider, month):
#     conn = create_engine(connection_string)
#
#     query = """select jira_tickets, sum(provider_amount) as euro_amount
#                 from (
#                 select pnr, listagg(distinct jira_ticket, '; ') within group (order by jira_ticket) as jira_tickets
#                 from prov_recon.tool_pnr_list
#                 group by pnr
#                 ) p
#                 join (select pnr, sum(provider_amount) as provider_amount from prov_recon.full_provider_bucket_1_all_time group by 1) f
#                 on p.pnr=f.pnr
#                 where p.pnr in (select distinct pnr from prov_recon.full_provider_bucket_1_all_time
#                                                         where provider in ('{provider}') and substring(first_month_issue, 1, 7) in ('{month}')
#                                                         and pnr is not null
#                                     union select 'string so that we dont have an in-null condition for ticket_id' -- wait is this really needed? todo: check
#                                                         )
#                 group by jira_tickets order by euro_amount desc;""".format(provider="','".join(provider), month="','".join(month))
#     print(query)
#     dff = pd.read_sql_query(query, conn)
#     conn.dispose()
#     data = [
#         go.Bar(
#             x=dff['jira_tickets'],  # assign x as the dataframe column 'x'
#             y=dff['euro_amount']
#         )
#     ]
#     layout = go.Layout(
#         hovermode='closest',
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         title='JIRA Tickets combination Euro Amount',
#         font={'color': '#ffffff'},
#         xaxis=dict(
#             title='JIRA Ticket',
#             titlefont=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#ffffff'
#             ),
#             color='#ffffff'
#         ),
#         yaxis=dict(
#             title='Euro amount',
#             titlefont=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#ffffff'
#             ),
#             color='#ffffff'
#         )
#     )

#    return {'data': data, 'layout': layout}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)