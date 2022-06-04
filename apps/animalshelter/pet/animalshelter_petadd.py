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

from datetime import datetime

from app import app
from apps import dbconnect as db

CONTENT_STYLE_R = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'font-family': 'Avenir',
    'fontSize': '16px',
    'border-color':'#a0a3a2',
}

layout = html.Div(
    [
        html.Div(
            html.Center(
                html.H2("Enter Pet Details")
            )
        ),

        html.Br(),

        dcc.Store(id='pet_data_store', storage_type='memory', data=0),

        dbc.Alert(id='pet_addalert', is_open=False),

        dbc.Row(
            [
                dbc.Col(
                    [
                    html.H4("Date of Rescue"),
                    dcc.DatePickerSingle(
                    id='pet_rd',
                    placeholder=' Date',
                    month_format = 'YYYY-MM-DD',
                    min_date_allowed = '2020-04-01',
                    date = datetime.now().strftime("%Y-%m-%d") 
                    )
                    ]
                ),
            
            dbc.Col(),
            dbc.Col(),
            dbc.Col(),
            dbc.Col()
            ]
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Pet Name"),
                        dcc.Input(id='pet_name', type='text', required=True, placeholder='Name')
                    ]
                ),
                dbc.Col(
                    [
                        html.H4("Pet Breed"),
                        dcc.Input(id='pet_breed', type='text', placeholder='Breed Type', required=True)
                    ]
                ),
                dbc.Col(
                    [
        
                    ]
                )
            ]
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Sex"),
                dcc.Dropdown(
                id='pet_sex', 
                options=[
                    {'label': 'Male', 'value': 'M'},
                    {'label': 'Female', 'value': 'F'}
                ],
                value='M',
                placeholder=' Pet Sex',
                searchable=False,
                clearable=False,
                style = {'width': '55%'}
                )
                ]
                ),

                dbc.Col(
                    [
                    html.H4("Age"),
                    dcc.Input(
                    id='pet_age',
                    placeholder=' Age',
                    required= True
                    )
                    ]
                ),

                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H4("Adoption Status"),
                                dbc.Row(
                                    [
                                        dbc.Checkbox(
                                            id = 'pet_adpt_stat_box',
                                            name = 'Yes',
                                            checked = False
                                        ),

                                        html.P(" Ready for Adoption", style={'marginBottom': '0px', 'marginLeft': '10px'})
                                    ]
                                ),
                            ],
                            id = 'pet_adpt_stat_div',
                            hidden = True
                        )
                    ]
                )

            ]
        ),

        html.Br(),

        dbc.Row(
            [
            
            dbc.Col(
                [
                    html.H4("Rescue Story"),
                dcc.Textarea(
                        id="pet_story", draggable=False,
                        placeholder = " How was the pet rescued? Where were they found?",
                        style = {'width': '100%', 'height': '100px',
                        'border-color': '#a0a3a2', 'resize': 'None'},
                        required = True
                    )
                    ]
            ),

            dbc.Col(
                [
                    html.H4("Medical Records"),
                dcc.Textarea(id="pet_mr", draggable=False, 
                placeholder = " Medical Records",
                style = {'width': '100%', 'height': '100px',
                        'border-color': '#a0a3a2', 'resize': 'None'}
                        ),
                ]
            )
            ]
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    #PC
                ),
                dbc.Col(
                    
                ),
                dbc.Col(
                    html.Center(dbc.Button
                        ('Submit', id='sub_pd', n_clicks=0,
                        style=
                            {
                            'font-family':'Avenir', 
                            'border-width':'3px',
                            'fontSize':'14px'
                            }
                        ))
                ),
                dbc.Col(

                ),
                dbc.Col(

                )
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
                        'Continue Encoding',
                        id='continue_petaddrecord'
                    ),
                    dbc.Button(
                        'Proceed',
                        href='/pet/menu' #Clicking leads to a change of pages
                    )
                    ]
                )
            ],
            centered=True,
            id='pet_addsuccessmodal',
            backdrop=True #Dialog box does not go away if you click the background
        )
    ],

    style = CONTENT_STYLE_R
)