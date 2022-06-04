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

from datetime import datetime

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

CONTENT_STYLE_MODIFIED = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "fontFamily": "Avenir"
}

CONTENT_STYLE_COVER = {
    "marginLeft": "15.15rem",
}

CONTENT_STYLE_CARD = {
    "marginLeft": "16rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
    "fontFamily": "Avenir"
}

# Successful Adoptions
# Pending Adoptions
# Failed Adoptions

layout = html.Div(
    [
        html.H3("Adoption Information"),
        html.P("Find out if the adoption status of an animal is a success, failure, or pending."),
        
        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                    "Success", 
                    href="/adoptions/history?mode=success",
                    id = 'adoption_success',
                    className="p-3 mb-2 bg-warning text-white",
                    style = {'width': '100%'},
                    n_clicks = 0),
                    width=4
                ),

                dbc.Col(
                    dbc.Button(
                    "Pending",
                    id = 'adoption_pending', 
                    href="/adoptions/history?mode=pending",
                    className="p-3 mb-2 bg-warning text-white",
                    style = {'width': '100%'},
                    n_clicks = 0),
                    width=4
                ),

                dbc.Col(
                    dbc.Button(
                    "Fail", 
                    id='adoption_fail', 
                    href='/adoptions/history?mode=fail', 
                    className='p-3 mb-2 bg-warning text-white',
                    style = {'width': '100%'},
                    n_clicks = 0
                    ),
                    width = 4
                )
                
            ]
        ),

        html.Br(),

        dbc.Table(
            id='adoptionhistory_table' 
        ),

        dbc.Modal(
            [
                dbc.ModalHeader("Interview Answers"),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H5("Household Count"),
                                    width = 3
                                ),
                                dbc.Col(
                                    html.P(id='interview_q_a', style={'marginBottom': '0px'}),
                                    width = 9
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H5("Ideal Pet"),
                                    width = 3
                                ),

                                dbc.Col(
                                    html.P(id='interview_q_b', style={'marginBottom': '0px'}),
                                    width = 9
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H5("Allergic Household Members?"),
                                    width = 3
                                ),

                                dbc.Col(
                                    html.P(id='interview_q_c', style={'marginBottom': '0px'}),
                                    width = 9
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H5("Previously owned a pet?"),
                                    width = 3
                                ),

                                dbc.Col(
                                    html.P(id='interview_q_d', style={'marginBottom': '0px'}),
                                    width = 9
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H5("Steps to help pet get acclimated?"),
                                    width = 3
                                ),

                                dbc.Col(
                                    html.P(id='interview_q_e', style={'marginBottom': '0px'}),
                                    width = 9
                                )
                            ]
                        )
                    ]
                )
            ],
            id = 'interview_modal_window',
            size = 'lg',
            is_open = False,
            backdrop = True,
            fade = True,
            autoFocus= True
        ),

        dbc.Modal(
            [

                dbc.Alert(id='adoption_history_alert', is_open = False, dismissable=True, duration=1000), # still won't show up

                dbc.ModalHeader(
                    "Update Adoption Order"
                ),
                dbc.ModalBody(
                    [
                        # Adopter Details (Name, Pet of Choice)
                        # If successful adoption, => Adoption Cost
                        # If unsuccessful, ==> remarks

                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H5("Adopter:"),
                                    width = 3
                                ),
                                
                                dbc.Col(
                                    html.P(id="modal_adopter_name", style={'marginBottom': '0px'}),
                                    width = 3
                                ),

                                dbc.Col(
                                    html.H5("Pet of Interest:"),
                                    width = 3
                                ),

                                dbc.Col(
                                    html.P(id='modal_pet_name', style = {'marginBottom': '0px'}),
                                    width = 3
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5("Adoption Status"),
                                        dcc.Dropdown(
                                        id='adoption_order_result_dropdown', 
                                        options = [
                                            {'label': 'Successful', 'value': 'Y'},
                                            {'label': 'Pending', 'value': 'P'},
                                            {'label': 'Failed', 'value': 'F'}
                                            ]
                                        )
                                    ],
                                    width = 5
                                ),

                                dbc.Col(
                                    [
                                        html.H5("Date of Transaction"),
                                        dcc.DatePickerSingle(
                                            id = 'trans_date',
                                            placeholder=' Date',
                                            month_format = 'YYYY-MM-DD',
                                            min_date_allowed = '2020-04-01',
                                            date = datetime.now().strftime("%Y-%m-%d") 
                                        )
                                    ],
                                    width = 7
                                )
                            ]
                        ),

                        html.Br(),
                        html.Br(),

                        # Show if adoption is successful!
                        html.Div(
                            [
                                dbc.Row(
                                    html.P(
                                        "Adoption cost text here.", 
                                        style = {"marginBottom":"10px", "marginLeft": "15px"}
                                        )
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H5("Adoption Cost", style={'marginTop': '5px'}),
                                            width = 3
                                        ),

                                        dbc.Col(
                                            dbc.Input(id='adoption_cost', type='number', maxLength=6, minLength=1),
                                            width = 9
                                        )
                                    ]
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H5()
                                        )
                                    ]
                                )
                            ],
                        ),

                        html.Br(),
                        html.Br(),

                        dbc.Button('Submit', id='submit_adoption_order', n_clicks=0),

                        dbc.Modal(
                            [
                                dbc.ModalHeader("Transaction Registered!"),
                                dbc.ModalBody(
                                    "You may now return to the main adoption screen!"
                                ),
                            ],
                            id = 'register_adopt_order',
                            is_open = False,
                            backdrop = True,
                            fade = True
                        )
                    ]
                )
            ],
            id = 'update_interview_results',
            size = 'lg',
            centered = True,
            is_open = False,
            backdrop = True,
            fade = True,
            autoFocus = True
        ) # Update Window (Reflect Costs, include date of transaction, change adoption status and pet status and pet exit if adopted)
    ],

    style = CONTENT_STYLE
)