import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

import sys
sys.path.append('.')
sys.path.append('..')

from app import app
from apps import dbconnect as db

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

FONT_STYLE = {
    "font-style": "Avenir"
}

layout = html.Div(
    [

        html.Br(),

        html.H3("Reports Page"),
        html.P("""The reports page is the section of the website which contains everything you need to know about your company's business data. Costs,
        frequencies, and other statisically relevant data are shown in this section for use by the company to make better decisions regarding future
        company policy going forward."""),

        html.Br(),

        # Dropdown 
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Type of Statistic"),
                        dcc.Dropdown(
                            id = 'stat_type',
                            options = [
                                {'label': 'Total Cost of Adoptions', 'value': 'total_adoptions'},
                                {'label': 'Average Cost of Successful Adoptions', 'value': 'successful_adoptions'},
                                {'label': 'Frequency of Adoptions', 'value':'freq_adoptions'},
                                {'label': 'Number of Rescues', 'value': 'pets_rescued'},
                                {'label': 'Number of Situationers', 'value': 'sit_number'},
                                {'label': 'Number of Vet Appointments', 'value': 'vet_appt_dates'},
                                {'label': 'Number of Adopter Interviews', 'value': 'adopter_int_count'},
                            ],
                            value = 'successful_adoptions',
                            searchable = False,
                            clearable = False,
                            style = {'width': '100%'}
                        )
                    ]
                ),

                dbc.Col(
                    [
                        html.H5("Period Covered"),
                        dcc.Dropdown(
                            id = 'stat_period',
                            options = [
                                {'label': 'per week', 'value': 'per week'},
                                {'label': 'per month', 'value': 'per month'}
                            ],
                            value = 'per month',
                            searchable = False,
                            clearable = False,
                            style = {'width': '100%'}
                    )
                    ]
                )
            ],
            justify = 'center',
            className = 'g-0'
        ),

        html.Br(),

        html.Div(id = 'graph_data'),
    ],
    style = CONTENT_STYLE
)

# Callback for reporting to the graph
@app.callback(
    [
        Output('graph_data', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('stat_type', 'value'),
        Input('stat_period', 'value'),
        Input('adminshelter_data', 'data')
    ]
)
def project_graph(pathname, type, timeframe, shelterdata):
    if pathname == '/reports':
        shelter_data_df = pd.DataFrame.from_records(shelterdata)

        shelter_id = int(shelter_data_df.at[0, 'SHELTER ID'])
        if type == 'successful_adoptions':

            # Obtain SQL
            sql = """
                SELECT a.adopt_order_n, ad.adopter_m, ad.adopter_l, ad.adopter_no, 
                p.pet_m, p.pet_b, p.pet_s, a.adopt_order_c, a.adopt_order_trans_date
                from adoption a INNER JOIN pet p ON p.pet_n = a.pet_n
                INNER JOIN adopter ad ON a.adopter_n = ad.adopter_n
                WHERE adopt_order_del_ind = False
                AND pet_delete_ind = True and pet_adpt_stat = True
                AND adopt_order_r = %s
                AND p.shelter_n = %s
                """
            
            values = ['Y', shelter_id]

            cols = ['Adopt Order', 'Adopter Name', 'Adopter Address', 'Adopter Contact', 'Pet Name', 'Pet Breed',
            'Pet Sex', 'Order Cost', 'Transaction Date']

            df = db.querydatafromdatabase(sql, values, cols)

            if df.shape[0]:
                df.drop(["Adopt Order", "Adopter Name", "Adopter Address", "Adopter Contact", "Pet Name", "Pet Breed", "Pet Sex"], axis = 1, inplace=True)
                
                if timeframe == "per month":
                    
                    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
                    df["Order Cost"] = df["Order Cost"].astype("float")
                   
                    new_df = df.groupby(pd.Grouper(key="Transaction Date", freq="M")).mean()
                    new_df.reset_index(inplace=True)
                
                    
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Transaction Date"],
                                    y = new_df["Order Cost"], 
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Average Cost of Adoptions Per Month'
                            }
                        }
                    )

                    return [graph_data]
                
                elif timeframe == "per week":

                    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
                    df["Order Cost"] = df["Order Cost"].astype("float")
                    #df["Order Cost"] = df["Order Cost"].apply(''.format(:.2f))
                   
                    new_df = df.groupby(pd.Grouper(key="Transaction Date", freq="1W")).mean()
                    new_df.reset_index(inplace=True)
                    
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Transaction Date"],
                                    y = new_df["Order Cost"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Average Cost of Adoptions Per Week'
                            }
                        }
                    )

                    return [graph_data]
                
                else:
                    raise PreventUpdate
                
            else:
                return ["Nothing to show here", dash.no_update]
        
        elif type == 'total_adoptions':

            # Obtain SQL
            sql = """
                SELECT a.adopt_order_n, ad.adopter_m, ad.adopter_l, ad.adopter_no, 
                p.pet_m, p.pet_b, p.pet_s, a.adopt_order_c, a.adopt_order_trans_date
                from adoption a INNER JOIN pet p ON p.pet_n = a.pet_n
                INNER JOIN adopter ad ON a.adopter_n = ad.adopter_n
                WHERE adopt_order_del_ind = False
                AND pet_delete_ind = True and pet_adpt_stat = True
                AND adopt_order_r = %s
                AND p.shelter_n = %s
                """
            
            values = ['Y', shelter_id]

            cols = ['Adopt Order', 'Adopter Name', 'Adopter Address', 'Adopter Contact', 'Pet Name', 'Pet Breed',
            'Pet Sex', 'Order Cost', 'Transaction Date']

            df = db.querydatafromdatabase(sql, values, cols)

            if df.shape[0]:
                df.drop(["Adopt Order", "Adopter Name", "Adopter Address", "Adopter Contact", "Pet Name", "Pet Breed", "Pet Sex"], axis = 1, inplace=True)
                
                if timeframe == "per month":
                    
                    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
                    df["Order Cost"] = df["Order Cost"].astype("float")
                   
                    new_df = df.groupby(pd.Grouper(key="Transaction Date", freq="M")).sum()
                    new_df.reset_index(inplace=True)
                   
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Transaction Date"],
                                    y = new_df["Order Cost"], 
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Average Cost of Adoptions Per Month'
                            }
                        }
                    )

                    return [graph_data]
                
                elif timeframe == "per week":

                    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
                    df["Order Cost"] = df["Order Cost"].astype("float")
                    #df["Order Cost"] = df["Order Cost"].apply(''.format(:.2f))
                   
                    new_df = df.groupby(pd.Grouper(key="Transaction Date", freq="1W")).sum()
                    new_df.reset_index(inplace=True)
                   
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Transaction Date"],
                                    y = new_df["Order Cost"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Average Cost of Adoptions Per Week'
                            }
                        }
                    )

                    return [graph_data]
                
                else:
                    raise PreventUpdate
                
            else:
                return ["Nothing to show here", dash.no_update]

        elif type == 'freq_adoptions':

            # Obtain SQL
            sql = """
                SELECT a.adopt_order_n, ad.adopter_m, ad.adopter_l, ad.adopter_no, 
                p.pet_m, p.pet_b, p.pet_s, a.adopt_order_c, a.adopt_order_trans_date
                from adoption a INNER JOIN pet p ON p.pet_n = a.pet_n
                INNER JOIN adopter ad ON a.adopter_n = ad.adopter_n
                WHERE adopt_order_del_ind = False
                AND pet_delete_ind = True and pet_adpt_stat = True
                AND adopt_order_r = %s OR adopt_order_r = %s OR adopt_order_r = %s
                AND p.shelter_n = %s
                """
            
            values = ['Y', 'P', 'F', shelter_id]

            cols = ['Adopt Order', 'Adopter Name', 'Adopter Address', 'Adopter Contact', 'Pet Name', 'Pet Breed',
            'Pet Sex', 'Order Cost', 'Transaction Date']

            df = db.querydatafromdatabase(sql, values, cols)

            if df.shape[0]:
                
                df.drop(["Adopter Name", "Adopter Address", "Adopter Contact", "Pet Name", "Pet Breed", "Pet Sex", "Order Cost"], axis = 1, inplace=True)
                
                if timeframe == "per month":

                    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
                   # df["Adopt Order"] = df["Order Cost"].astype("float")
                    
                    new_df = df.groupby(pd.Grouper(key="Transaction Date", freq="M")).count()
                    new_df.reset_index(inplace=True)
                    
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Transaction Date"],
                                    y = new_df["Adopt Order"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Frequency of Adoptions Per Month'
                            }
                        }
                    )

                    return [graph_data]

                elif timeframe == "per week":

                    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
                   # df["Adopt Order"] = df["Order Cost"].astype("float")
                    
                    new_df = df.groupby(pd.Grouper(key="Transaction Date", freq="W")).count()
                    new_df.reset_index(inplace=True)
                    
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Transaction Date"],
                                    y = new_df["Adopt Order"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Frequency of Adoptions Per Week',
                            },
                            
                        }
                    )

                    return [graph_data]
                
                else:
                    raise PreventUpdate

            else:
                return ["Nothing to show here", dash.no_update]

        elif type == 'pets_rescued':
            sql = """
            SELECT pet_n, pet_rd from pet
            WHERE shelter_n = %s
            """

            values = [shelter_id]

            cols = ["Pet ID", "Rescue Date"]

            df = db.querydatafromdatabase(sql, values, cols)

            if df.shape[0]:                
                if timeframe == "per month":

                    df["Rescue Date"] = pd.to_datetime(df["Rescue Date"])
                   # df["Adopt Order"] = df["Order Cost"].astype("float")
                    
                    new_df = df.groupby(pd.Grouper(key="Rescue Date", freq="M")).count()
                    new_df.reset_index(inplace=True)
                    
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Rescue Date"],
                                    y = new_df["Pet ID"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Pets Rescued Per Month'
                            }
                        }
                    )

                    return [graph_data]

                elif timeframe == "per week":

                    df["Rescue Date"] = pd.to_datetime(df["Rescue Date"])
                   # df["Adopt Order"] = df["Order Cost"].astype("float")
                    
                    new_df = df.groupby(pd.Grouper(key="Rescue Date", freq="W")).count()
                    new_df.reset_index(inplace=True)

                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Rescue Date"],
                                    y = new_df["Pet ID"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Pets Rescued Per Week',
                            },
                            
                        }
                    )

                    return [graph_data]
                
                else:
                    raise PreventUpdate

            else:
                return ["Nothing to show here", dash.no_update]
        
        elif type == "sit_number":
            sql = """
            SELECT e.event_n, e.event_m, s.schedule_d from event e 
            INNER JOIN schedule s ON e.event_n = s.event_n 
            WHERE event_m = %s
            """

            values = ['Situationer']

            cols = ['Event ID', 'Event Name', 'Schedule Date']

            df = db.querydatafromdatabase(sql, values, cols)

            if df.shape[0]:
                df['Schedule Date'] = pd.to_datetime(df['Schedule Date'])
                if timeframe == 'per month':

                    new_df = df.groupby(pd.Grouper(key="Schedule Date", freq="M")).count()
                    new_df.reset_index(inplace=True)

                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Schedule Date"],
                                    y = new_df["Event ID"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Situationers Per Month'
                            }
                        }
                    )

                    return [graph_data]

                elif timeframe == 'per week':

                    new_df = df.groupby(pd.Grouper(key="Schedule Date", freq="1W")).count()
                    new_df.reset_index(inplace=True)
                    
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Schedule Date"],
                                    y = new_df["Event ID"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Situationers Per Week'
                            }
                        }
                    )

                    return [graph_data]
                
                else:
                    raise PreventUpdate
            
            else:
                return ["Nothing to show here", dash.no_update]
        
        elif type == 'vet_appt_dates':
            sql = """
            SELECT e.event_n, e.event_m, s.schedule_d from event e 
            INNER JOIN schedule s ON e.event_n = s.event_n 
            WHERE event_m = %s
            """

            values = ['Veterinary Checkup']

            cols = ['Event ID', 'Event Name', 'Schedule Date']

            df = db.querydatafromdatabase(sql, values, cols)

            if df.shape[0]:
                df['Schedule Date'] = pd.to_datetime(df['Schedule Date'])
                if timeframe == 'per month':

                    new_df = df.groupby(pd.Grouper(key="Schedule Date", freq="M")).count()
                    new_df.reset_index(inplace=True)
                    
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Schedule Date"],
                                    y = new_df["Event ID"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Checkups Per Month'
                            }
                        }
                    )

                    return [graph_data]

                elif timeframe == 'per week':

                    new_df = df.groupby(pd.Grouper(key="Schedule Date", freq="1W")).count()
                    new_df.reset_index(inplace=True)
                    
                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Schedule Date"],
                                    y = new_df["Event ID"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Checkups Per Week'
                            }
                        }
                    )

                    return [graph_data]
                
                else:
                    raise PreventUpdate
            
            else:
                return ["Nothing to show here", dash.no_update]

        elif type == "adopter_int_count":
            sql = """
            SELECT e.event_n, e.event_m, s.schedule_d from event e 
            INNER JOIN schedule s ON e.event_n = s.event_n 
            WHERE event_m = %s
            """

            values = ['Adopter Interview']

            cols = ['Event ID', 'Event Name', 'Schedule Date']

            df = db.querydatafromdatabase(sql, values, cols)

            if df.shape[0]:
                df['Schedule Date'] = pd.to_datetime(df['Schedule Date'])
                if timeframe == 'per month':

                    new_df = df.groupby(pd.Grouper(key="Schedule Date", freq="M")).count()
                    new_df.reset_index(inplace=True)

                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Schedule Date"],
                                    y = new_df["Event ID"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Adopter Interviews Per Month'
                            }
                        }
                    )

                    return [graph_data]

                elif timeframe == 'per week':

                    new_df = df.groupby(pd.Grouper(key="Schedule Date", freq="1W")).count()
                    new_df.reset_index(inplace=True)

                    graph_data = dcc.Graph(
                        figure = {
                            'data': [
                                go.Bar(
                                    x = new_df["Schedule Date"],
                                    y = new_df["Event ID"],
                                    marker = {'color' : '#e19e1e'}
                                )
                            ],
                            'layout': {
                                'title': 'Adopter Interviews Per Week'
                            }
                        }
                    )

                    return [graph_data]
                
                else:
                    raise PreventUpdate
            
            else:
                return ["Nothing to show here", dash.no_update]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate