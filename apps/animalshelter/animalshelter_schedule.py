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
        html.Div(
            html.Img(
                src=app.get_asset_url('animal_daycare.jpg'), 
                style = {'width': '100%', 'height': '250px', 'object-fit':'cover'}
                ),
            style = CONTENT_STYLE_COVER
        ),

        html.Div(
            [
                dbc.Card(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.CardImg(
                                        src="assets/static/images/schedule_shelter_photo.jpg",
                                        className='img-fluid rounded-start'
                                    ),
                                    className='col-md-3'
                                ),

                                dbc.Col(
                                    [
                                        dbc.CardHeader(
                                            html.H4("More Description"),
                                            style = {'background': 'rgba(0,0,0,0.0)', 'border': 'none'},
                                            className = 'border-bottom-0 card-title'
                                        ),
                                        dbc.CardBody(
                                            [
                                                html.P("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                                                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                                                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
                                                """)
                                            ]
                                        )
                                    ]
                                ),

                                dbc.Col(
                                        dbc.CardBody(
                                    [
                                        html.H4("References", className="card-title"),
                                        html.P("Documents and Forms", style={'fontFamily':'Avenir'}),
                                        html.P("Rules and Regulations", style={'fontFamily':'Avenir'}),
                                        html.P("Consent Form", id='consent_form_click', n_clicks=0, style={'fontFamily': 'Avenir'}),
                                        html.P("Animal History", style={'fontFamily':'Avenir'}),
                                    ]
                                    )

                                ),

                                dbc.Col(
                                    html.Br()
                                )

                            ]
                        )

                    ],

                    style = {'border': 'none'} 
                )
            ],
            style = CONTENT_STYLE_CARD,
            className = 'g-0'
        ),

        html.Div(
                [
                    html.Table(
                        [
                            html.Tr(
                                [
                                    html.Td(
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H5("Lara's Ark"),
                                                        html.Br(),
                                                        html.P("Business Hours:"),
                                                        html.P("Monday to Sunday: 8:00 AM – 5:00 PM")
                                                    ]  
                                                )
                                            ],
                                            style = {'border':'None'}
                                        )
                                    ),
                                    html.Td(" ", rowSpan=2)
                                ]
                            ),

                            html.Tr(
                                [
                                    html.Td(" ")
                                ]
                            )
                        ]
                    )
                ],
            style = CONTENT_STYLE_MODIFIED
        ),

        dbc.Modal( #Modal = dialog box; feedback for successful saving
            [
                dbc.ModalHeader(
                    html.H4("""Lara's Ark Consent Form""")
                ),
                dbc.ModalBody(
                    """
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
                    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
                    reprehenderit in voluptate velit esse cillum dolore eu fugiat 
                    nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
                    sunt in culpa qui officia deserunt mollit anim id est laborum."""
                )
            ],
            centered=True,
            id='consent_form',
            backdrop=True,
            fade=True,
        )
    ]
)