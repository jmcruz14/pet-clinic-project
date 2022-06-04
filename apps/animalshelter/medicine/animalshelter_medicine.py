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
    
        dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.CardImg(
                                        src="assets/static/images/medicine_supply_img.jpg",
                                        className='img-fluid rounded-start'
                                    ),
                                    className='col-md-4'
                        ),

                        dbc.Col(
                            [
                                html.Br(),
                                html.H4("Medicine"),
                                html.Br(),
                                html.P("""
                                    Medicine is administered on a daily basis when
                                    the pet in question has certain sicknesses or diseases which
                                    they must handle. This section contains the database of existing
                                    medicine products which are currently in circulation within the shelter. 
                                """,
                                className = 'vertical-center')
                            ],
                            width = 6
                        )
                    ]
                )
            ]
        ),

        html.Br(),

        dbc.Card(
            [
                html.Center(
                    dbc.CardHeader("What would you like to do?")
                )
            ]
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H3("Add Medicine", className="card-title"),
                                    
                                    html.Br(),

                                    dbc.Button(
                                        "Add", 
                                        href="/medicine/medinfo?mode=add",
                                        className="bg-secondary text-white",
                                        style = {'width':'100%'}
                                    )
                                ]
                            )
                        ]
                    )
                ),

                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H3(
                                        "Search", 
                                        className="card-title"
                                        ),

                                    html.Br(),

                                    dbc.Input(
                                        id="med_search", 
                                        placeholder=""
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        ),

        html.Br(),

        dbc.Table( # sample table below for testing
                    # table must follow sql
            id = 'med_table'
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Delete Success!')
                ),
                dbc.ModalBody(
                    'You may now return to the main portal!'
                )
            ],
            id = 'delmed_success_modal',
            centered = True,
            is_open = False,
            backdrop = True,
            scrollable = True
        )
        
    ],
    style = CONTENT_STYLE
)