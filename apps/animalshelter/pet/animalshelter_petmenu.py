import dash
from dash_html_components.P import P
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

from app import app
from apps import dbconnect as db

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "font-family": "Avenir"
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

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.CardImg(
                                        src=app.get_asset_url("coverphoto_1.jpg"),
                                        className='img-fluid rounded-start'
                                    ),
                                    className='col-md-4' # Check size of this later
                        ),

                        dbc.Col(
                            [
                                html.Br(),
                                html.H4("Pets"),
                                html.Br(),
                                html.P("""
                                Pets are the lifeblood of Lara's Ark. Without
                                them, we would have no animals to be able to
                                put up for adoption.

                                In this section of the website,
                                you may add or modify pet entries found in the
                                shelter as you please.
                                
                                Click on the add button to start adding!""",
                                className = 'vertical-center')
                            ],
                            width = 6
                        )
                    ]
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
                                    html.H3("Add Pet", className="card-title"),
                                    html.P(
                                        """This function enables you to add a rescued pet
                                        into the system.""", className="card-text"),
                                    dbc.Button("Add", href="/pet/add?mode=add",
                                    className="bg-warning text-white",
                                    style = {'width':'100%'})
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
                                    html.H3("Search", className="card-title"),

                                    html.P(
                                        """
                                        Search for pets.
                                        """, 
                                        className="card-text"
                                        ),

                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    dbc.Input(
                                                    id="pet_search", 
                                                    placeholder="", 
                                                    style = {"padding-Top": "2px"},
                                                    type='text')
                                                ]
                                            )
                                        ],
                                        className='row align-items-center'
                                    ),
                                    
                                ],
                                
                            )
                        ]
                    )
                ),
                
            ]
            ),

        html.Br(),

        dbc.Table( 
            # sample table below for testing
            # table must follow sql
            id = 'pet_table'
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
            id = 'delpet_success_modal',
            centered = True,
            is_open = False,
            backdrop = True,
            scrollable = True
        )
    ],
    style = CONTENT_STYLE
)