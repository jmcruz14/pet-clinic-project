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
                                        src=app.get_asset_url('vet_cover.jpg'),
                                        className='img-fluid rounded-start'
                                    ),
                                    className='col-md-4'
                        ),

                        dbc.Col(
                            [
                                html.Br(),
                                html.H4("Veterinarian"),
                                html.Br(),
                                html.P("""
                                    Veterinarians administer medicine on a daily basis when
                                    the pet in question has certain sicknesses or diseases which
                                    they must handle. This section contains the database of existing
                                    veterinarians who are currently paid or retained by the shelter
                                    responsible for taking care of our shelter's strays. 
                                """,
                                className = 'vertical-center')
                            ],
                            width = 6
                        )
                    ]
                )
            ]
        ),

        # Cover Photo
        # html.Img(
        #     src=app.get_asset_url('vet_cover.jpg'), 
        #     style = {'width': '35%', 'height': '35%', 'left':'0px'}
        #     ),
        
        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            #dbc.CardImg(src="create_icon.png"),
                            
                            dbc.CardBody(
                                [
                                    #html.P("Image goes here"),
                                    html.H3("Add Vet", className="card-title"),
                                    html.P(
                                        """Add another veterinary
                                        into the system!""", className="card-text"),
                                    dbc.Button("Add", href="/vet/info?mode=add",
                                    className="p-3 mb-2 bg-warning text-white",
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
                                        Search for vets.
                                        \n
                                        """, className="card-title",
                                        style = {"padding-Bottom": "2px", "margin-Bottom": '2px'}),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Br(),
                                                        dbc.Input(
                                                        id="vet_search", 
                                                        placeholder="", 
                                                        style = {"padding-Top": "2px", "width": "100%"}
                                                        )
                                                    ],

                                                    className = 'row align-items-center'
                                                )
                                            ]
                                        ),
                                    
                                ],
                                
                            )
                        ]
                    )
                )
            ]
        ),

        html.Br(),
        
        dbc.Table(
                            # table must follow sql
                    id = 'vet_table'
        ),

        dbc.Modal(
            [
            dbc.ModalHeader(
                html.H4("Delete Successful!")
            ),

            dbc.ModalBody(
                "You may now refresh the page!"
            )
            ],
            id = 'del_vet_modal',
            centered = True,
            is_open = False,
            backdrop = True,
            scrollable = True
        )


    ],
    style = CONTENT_STYLE
)