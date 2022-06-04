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
        html.H4("Personal Information"),

        dcc.Store(id='adopter_data_store', storage_type='memory', data=0),

        dbc.Alert(id='adopter_addalert', is_open=False),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    html.B("Name")
                ),

                dbc.Col(
                    dcc.Input(id='adopter_name', type='text')
                ),

                dbc.Col(
                    html.B("Age")
                ),

                dbc.Col(
                    dcc.Input(id='adopter_age', type='number')
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.B("Address")
                ),

                dbc.Col(
                    dcc.Input(id='adopter_l', type='text')
                ),

                dbc.Col(
                    html.B("Phone Number")
                ),

                dbc.Col(
                    dcc.Input(id='adopter_no', type='text')
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
                        id = 'adopter_s',
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
                    html.B("Occupation")
                ),
                
                dbc.Col(
                    dcc.Input(id='adopter_occ', type='text')
                )
            ]
        ),

        html.Br(),

        html.Br(),
        dbc.Button("Submit", id='sub_adopter', n_clicks = 0),

        # Modal alert – Success for entry of data
        dbc.Modal( #Modal = dialog box; feedback for successful saving
            [
                dbc.ModalHeader(
                    html.H4('Save Success!', id='adopter_modal_message')
                ),
                dbc.ModalBody(
                    'You may now return to the main portal!'
                ),
                dbc.ModalFooter(
                    [
                    dbc.Button(
                        'Continue Editing',
                        id='adopter_close_button'
                    ),
                    dbc.Button(
                        'Proceed',
                        href='/portal' #Clicking leads to a change of pages
                    )
                    ]
                )
            ],
            centered=True,
            id='adopter_addsuccessmodal',
            backdrop=True   
        )
    ],

    style = CONTENT_STYLE
)