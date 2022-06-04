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

CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
    "fontFamily": "Avenir"
}

layout = html.Div(
    [
        html.H2("Adoption Form"),
        html.Br(),
        html.H4("Personal Information"),

        dbc.Button(
            "Existing Adopter", 
            href='/schedule/adopt?mode=view', 
            id="adopter_exists", 
            n_clicks = 0),
        html.Br(),
        html.Br(),

        dbc.Alert(id='adoption_addalert', is_open=False),

        dbc.Row(
            [
                dbc.Col(
                    html.B("Name")
                ),

                dbc.Col(
                    dcc.Input(id='adoption_name', type='text')
                ),

                dbc.Col(
                    html.B("Age")
                ),

                dbc.Col(
                    dcc.Input(id='adoption_age', type='number')
                )
            ],

            className = 'row align-items-center'
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.B("Address")
                ),

                dbc.Col(
                    dcc.Input(id='adoption_l', type='text')
                ),

                dbc.Col(
                    html.B("Phone Number")
                ),

                dbc.Col(
                    dcc.Input(id='adoption_no', type='text')
                )
            ],

            className = 'row align-items-center'
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.B("Sex")
                
                ),

                dbc.Col(
                    dcc.Dropdown(
                        id = 'adoption_s',
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
                    dcc.Input(id='adoption_occ', type='text')
                )
            ],

            className='row align-items-center'
        ),

        html.Br(),

        html.H4("Pet to be Adopted"),

        dcc.Dropdown(
            placeholder="Menu",
            id='pet_adoptionlist' # children ?
        ),

        html.Br(),

        html.Div(
            [
                html.H5("Selected Pet"),
                html.P(id = 'pet_adoptselectresult_name'),
                html.P(id = 'pet_adoptselectresult_breed'),
                html.P(id = 'pet_adoptselectresult_sex'),
                html.Br(),
                html.P(id = 'pet_adoptselectresult_rs')
            ],
            id = 'pet_adoptselectdiv',
            hidden = True
        ),

        html.Br(),

        html.H4("Interview Questions"),

        dbc.Row(
            [
                dbc.Col(
                    [
                    html.B("How many people live in your household?")
                    ],
                    width = 2
                ),

                dbc.Col(
                    [
                        dbc.Input(id='aoq_ppl_amt', placeholder='Amount of people', type='number')
                    ]
                )
            ],

            className='row align-items-center'
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.B("What is your ideal pet?")
                    ],

                    width = 2
                ),

                dbc.Col(
                    [
                        dbc.Input(id='aoq_idealpet', placeholder='Ideal pet?', type='text')
                    ]
                )
            ],

            className = 'row align-items-center'
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.B("Are members in your house allergic to animals?")
                    ],

                    width = 2
                ),

                dbc.Col(
                    [
                        dbc.Input(id='aoq_allergycount', placeholder='How many are allergic?', type='text')
                    ]
                )
            ],

            className = 'row align-items-center'
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.B("Have you previously owned and/or adopted a pet?")
                    ],

                    width = 2
                ),

                dbc.Col(
                    [
                        dbc.Input(id='aoq_petownership', type='text')
                    ]
                )
            ],

            className = 'row align-items-center'
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.B(
                            """What steps will you take to familiarize your new 
                            pet with his or her surroundings?""")
                    ],

                    width = 3
                ),

                dbc.Col(
                    [
                        dbc.Input(id='aoq_steps', placeholder='Steps?')
                    ]
                )
            ]
            ,

            className = 'row align-items-center'
        ),

        html.Br(),

        dbc.Button("Submit", id='sub_adoption', n_clicks = 0),

        # Modal alert – Success for entry of data
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
                        id='adoption_close_button'
                    ),
                    dbc.Button(
                        'Proceed',
                        href='/portal' #Clicking leads to a change of pages
                    )
                    ]
                )
            ],
            centered=True,
            id='adoption_addsuccessmodal',
            backdrop=True,
            scrollable=True
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    "Adopter List"
                ),
                dbc.ModalBody(
                    [
                        dbc.Table(
                            id = 'existing_adopter_list'
                        )
                    ]
                )
            ],
            is_open = False,
            centered = True,
            size = 'lg',
            id = 'existing_adopter_modal',
            backdrop = True,
            fade = True
        )
    ],
    style = CONTENT_STYLE
)