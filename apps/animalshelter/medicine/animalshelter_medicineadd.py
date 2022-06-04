import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

import sys
sys.path.append('.')
sys.path.append('..')
sys.path.append('...')

from app import app
from apps import dbconnect as db

CARD_STYLE = {
    "fontFamily": 'Avenir',
    "marginTop": '1em'
}

CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
    "fontFamily": "Avenir"
}

layout = html.Div(
    [
        dcc.Store(id='med_data_store', storage_type='memory', data=0),

        html.Div(
            html.H2("Input Medicine Details", style = {'fontFamily': 'Avenir'})
        ),
        html.Br(),

        dbc.Alert(id='med_addalert', is_open=False),

        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                                [
                                    html.H4("Medicine Name"),
                                    dcc.Input(id='med_name', placeholder = 'Name')
                                ]
                        ),
                        dbc.Col(
                                [
                                    html.H4("Medicine Count"),
                                    dcc.Slider(
                                    id='med_cn_slider', 
                                    min=0, 
                                    max=99, 
                                    step=1,
                                    value=0,
                                    updatemode='drag'),
                                    html.P(id='med_cn')
                                ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4("Medicine Type"),
                                dcc.Input(id='med_type', placeholder = "Type")
                            ]
                        ),
                        dbc.Col(
                            [
                                html.H4("Cost per item"),
                                dcc.Input(id='med_c', type='number', value='100', placeholder = "100")
                            ]
                        ),
                        dbc.Col(
                            [
                                html.H6("The total cost of Medicine is:", style = {'marginTop': '0.5em'}),
                                html.P(id='med_tc', style = {'marginTop': '0.5em'})
                            ]
                        ),
                        dbc.Col()
                    ]
                ),
                html.Br(),
                dbc.Button("Submit", id = 'sub_md', n_clicks=0)
            ]
        ),
        
        dbc.Modal( #Modal = dialog box; feedback for successful saving
            [
                dbc.ModalHeader(
                    html.H4('Save Success!')
                ),
                dbc.ModalBody(
                    'You may now return to the main portal!'
                ),
                dbc.ModalFooter(
                    [
                    dbc.Button(
                        'Continue Editing',
                        id = 'continue_medaddrecord'
                    ),
                    dbc.Button(
                        'Proceed',
                        href='/medicine' #Clicking leads to a change of pages
                    )
                    ]
                )
            ],
            centered=True,
            id='med_addsuccessmodal',
            backdrop='static' #Dialog box does not go away if you click the background
        )
    ],
    style = CONTENT_STYLE
)