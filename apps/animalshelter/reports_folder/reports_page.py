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
                                {'label': 'Average Cost of Successful Adoptions', 'value': 'successful_adoptions'},
                                {'label': 'Frequency of Adoptions', 'value':'freq_adoptions'},
                                {'label': 'Most Adoptions per Adopter', 'value': 'most_adoptions_per_adopter'}
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

        # Table to show that the queries are working as requested – for debugging purposes only
        html.Div(id = 'stat_table'),

        html.Div(id = 'graph_data'),
    ],
    style = CONTENT_STYLE
)

# Callback for reporting to the graph
@app.callback(
    [
        Output('stat_table', 'children'),
        Output('graph_data', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('stat_type', 'value'),
        Input('stat_period', 'value')
    ]
)
def project_graph(pathname, type, timeframe):
    if pathname == '/reports':
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
                """
            
            values = ['Y']

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
                   
                    stat_table = dbc.Table.from_dataframe(
                        new_df, striped=True, bordered=True,
                        hover=True, size='xl')
                    
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

                    return [stat_table, graph_data]
                
                elif timeframe == "per week":

                    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
                    df["Order Cost"] = df["Order Cost"].astype("float")
                    #df["Order Cost"] = df["Order Cost"].apply(''.format(:.2f))
                   
                    new_df = df.groupby(pd.Grouper(key="Transaction Date", freq="1W")).mean()
                    print(new_df)
                    new_df.reset_index(inplace=True)
                   
                    stat_table = dbc.Table.from_dataframe(
                        new_df, striped=True, bordered=True,
                        hover=True, size='xl')
                    
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

                    return [stat_table, graph_data]
                
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
                """
            
            values = ['Y', 'P', 'F']

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

                    stat_table = dbc.Table.from_dataframe(
                        new_df, striped=True, bordered=True,
                        hover=True, size='xl')
                    
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

                    return [stat_table, graph_data]

                elif timeframe == "per week":

                    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
                   # df["Adopt Order"] = df["Order Cost"].astype("float")
                    
                    new_df = df.groupby(pd.Grouper(key="Transaction Date", freq="W")).count()
                    new_df.reset_index(inplace=True)

                    stat_table = dbc.Table.from_dataframe(
                        new_df, striped=True, bordered=True,
                        hover=True, size='xl')
                    
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

                    return [stat_table, graph_data]
                
                else:
                    raise PreventUpdate

            else:
                return ["Nothing to show here", dash.no_update]
        
        # elif type == 'most_adoptions_per_adopter':

        #     # Obtain SQL
        #     sql = """
        #         SELECT a.adopt_order_n, ad.adopter_m, ad.adopter_l, ad.adopter_no, 
        #         p.pet_m, p.pet_b, p.pet_s, a.adopt_order_c, a.adopt_order_trans_date
        #         from adoption a INNER JOIN pet p ON p.pet_n = a.pet_n
        #         INNER JOIN adopter ad ON a.adopter_n = ad.adopter_n
        #         WHERE adopt_order_del_ind = False
        #         AND pet_delete_ind = True and pet_adpt_stat = True
        #         AND adopt_order_r = %s OR adopt_order_r = %s OR adopt_order_r = %s
        #         """
            
        #     values = ['Y', 'P', 'F']

        #     cols = ['Adopt Order', 'Adopter Name', 'Adopter Address', 'Adopter Contact', 'Pet Name', 'Pet Breed',
        #     'Pet Sex', 'Order Cost', 'Transaction Date']

        #     df = db.querydatafromdatabase(sql, values, cols)

        #     if df.shape[0]:
        #         df.drop(["Adopter Name", "Adopter Address", "Adopter Contact", "Pet Name", "Pet Breed", "Pet Sex", "Order Cost"], axis = 1, inplace=True)

        #         if timeframe == 'per month':

        #             df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
        #            # df["Adopt Order"] = df["Order Cost"].astype("float")
                    
        #             new_df = df.groupby(pd.Grouper(key="Transaction Date", freq="M")).count()
        #             new_df.reset_index(inplace=True)

        #             stat_table = dbc.Table.from_dataframe(
        #                 new_df, striped=True, bordered=True,
        #                 hover=True, size='xl')
                    
        #             graph_data = dcc.Graph(
        #                 figure = {
        #                     'data': [
        #                         go.Bar(
        #                             x = new_df["Transaction Date"],
        #                             y = new_df["Adopt Order"],
        #                             marker = {'color' : '#e19e1e'}
        #                         )
        #                     ],
        #                     'layout': {
        #                         'title': 'Freqency of Adoptuions Per Month'
        #                     }
        #                 }
        #             )

        #             return [stat_table, graph_data]

        #             pass
        #         elif timeframe == 'per week':
        #             pass
        #         else:
        #             raise PreventUpdate
        #     else:
        #         return ["Nothing to report here.", dash.no_update]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate