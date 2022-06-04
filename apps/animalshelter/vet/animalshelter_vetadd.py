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
        html.H3("Veterinarian Information", style = {'text-align': 'center'}),

        html.Br(),

        dcc.Store(id='vet_add_store', storage_type='memory', data=0),

        dbc.Alert(id='vet_addalert', is_open=False),

        dbc.Row(
            [
                dbc.Col(
                    html.B("Name")
                ),

                dbc.Col(
                    dcc.Input(id='vet_name', type='text', required=True)
                ),

                dbc.Col(
                    html.B("Age")
                ),

                dbc.Col(
                    dcc.Input(id='vet_age', type='number', required=True)
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.B("Address")
                ),

                dbc.Col(
                    dcc.Input(id='vet_l', type='text', required=True)
                ),

                dbc.Col(
                    html.B("Phone Number")
                ),

                dbc.Col(
                    dcc.Input(id='vet_no', type='text', required=True)
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.B("Sex")
                
                ),

                dbc.Col(
                    dcc.Dropdown(
                        id = 'vet_s',
                        options = [
                            {'label': 'Male', 'value': 'M'},
                            {'label': 'Female', 'value': 'F'}
                        ],
                        placeholder = "Sex",
                        searchable=False,
                        clearable=False
                    )
                ),

                dbc.Col(
                    html.B("Specialization")
                ),
                
                dbc.Col(
                    dcc.Input(id='vet_spec', type='text', required=True)
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.B("Cost per Visit")
                ),

                dbc.Col(
                    dcc.Input(id='vet_sal', type='number', required=True)
                ),

                dbc.Col(

                ),

                dbc.Col(

                )
            ],
            justify = 'start'
        ),

        html.Br(),
        dbc.Button("Submit", id='sub_vet', n_clicks = 0),

        # Modal alert – Success for entry of data
        dbc.Modal( #Modal = dialog box; feedback for successful saving
            [
                dbc.ModalHeader(
                    html.H4('Save Success!')
                ),
                dbc.ModalBody(
                    """
                    You have successfully registered a Veterinarian!
                    You may now return to the main portal, or you may
                    continue encoding other veterinarians!"""
                ),
                dbc.ModalFooter(
                    [
                    dbc.Button(
                        'Continue Editing',
                        id='vet_close_button'
                    ),
                    dbc.Button(
                        'Proceed',
                        href='/portal' #Clicking leads to a change of pages
                    )
                    ]
                )
            ],
            centered=True,
            id='vet_addsuccessmodal',
            backdrop=True,
            fade = True

        )
    ],

    style = CONTENT_STYLE
)