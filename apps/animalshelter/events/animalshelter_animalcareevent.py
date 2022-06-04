import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from datetime import datetime

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
        # maglagay ka ng situationer dito gago
        # situationer details
        dbc.Modal(
            [
                dbc.ModalHeader("Select an Event"),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "Situationer", 
                                        id='animal_situationerbtn', 
                                        n_clicks=0,
                                        style = {'width': '100%'}),
                                    width=4
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Veterinary Appointment", 
                                        id='animal_vetappointmentbtn', 
                                        n_clicks=0,
                                        style = {'width': '100%'}),
                                    width = 4
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Adopter Interview", 
                                        id='animal_adptrappointmentbtn', 
                                        n_clicks=0,
                                        style = {'width': '100%'}),
                                    width = 4
                                )
                            ]
                        )
                    ]
                )
            ],
            id = 'animalcare_selectmodal',
            size = 'lg',
            centered = True,
            backdrop = True,
            fade = True,
            is_open = True,
            autoFocus= True
        ),

        # SITUATIONER LAYOUT
        html.Div(
            [
                html.H2("Animal Situationer"),

                html.Br(),

                dbc.Alert(id='situationer_addalert', is_open=False),

                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H4("Date of Rescue"),

                                        dcc.DatePickerSingle(
                                        id = 'sit_d',
                                        placeholder = 'Date',
                                        month_format = 'YYYY-MM-DD',
                                        min_date_allowed = '2020-04-01',
                                        date = datetime.now().strftime("%Y-%m-%d")
                                        )
                                    ]
                                ),

                                dbc.Col(
                                    html.Br()
                                ),

                                dbc.Col(
                                    html.Br()
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H4("Location of Situationer"),
                                        dcc.Input(
                                            placeholder = "Rescue Location",
                                            id = 'sit_location',
                                            type = 'text'
                                        )
                                    ]
                                ),

                                dbc.Col(
                                    [
                                        html.H4("Number of Animals to be Rescued"),
                                        dcc.Input(
                                            id = 'sit_animalcount', # Is this supposed to be here?
                                            type = 'number',
                                            placeholder = 'Number of animals to be rescued'
                                        )
                                    ]
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Button(
                            "Submit",
                            id = 'sub_sit',
                            n_clicks = 0
                        )
                    ]
                ),
                
                    dbc.Modal( #Modal = dialog box; feedback for successful saving
                        [
                            dbc.ModalHeader(
                                html.H4('Situationer Save Success!')
                            ),
                            dbc.ModalBody(
                                'You may now return to the main portal!'
                            ),
                            dbc.ModalFooter(
                                [
                                dbc.Button(
                                    'Continue Encoding',
                                    id='continue_sitaddrecord'
                                ),
                                dbc.Button(
                                    'Proceed',
                                    href='/portal'
                                )
                                ]
                            )
                        ],
                centered=True,
                id='sit_addsuccessmodal',
                backdrop=True #Dialog box does not go away if you click the background
                )

                # Status
            ],
            id = 'animal_situationer',
            hidden = True
        ),


        # VET APPOINTMENT
        html.Div(
            [
                html.H2("Veterinary Appointment"),

                html.Br(),

                dbc.Alert(id='appointment_addalert', is_open=False),

                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H4("Date of Appointment"),

                                        dcc.DatePickerSingle(
                                        id = 'vetappt_d',
                                        placeholder = 'Date',
                                        month_format = 'YYYY-MM-DD',
                                        min_date_allowed = '2020-04-01'
                                        )
                                        ]
                                ),

                                dbc.Col(
                                    html.Br()
                                ),

                                dbc.Col(
                                    html.Br()
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    html.B("Pet Involved"),

                                    width = 2
                                ),

                                dbc.Col(
                                    dcc.Dropdown(
                                    placeholder="Menu",
                                    id='pet_examinationlist',
                                    searchable=False,
                                    clearable=False
                                    )
                                )
                            ],

                            className = 'row align-items-center'
                        ),

                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.B("Medical Records"),

                                        width = 2
                                    ),

                                    dbc.Col(
                                        html.P(id='pet_medicalrecordexam')
                                    )
                                ],
                                className = 'row align-items-center'
                            ),
                        id = 'pet_medicalrecorddiv',
                        hidden = True
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    html.B("Select Vet"),

                                    width = 2
                                ),

                                dbc.Col(
                                    dcc.Dropdown(
                                        placeholder='Menu',
                                        id='vet_examinationlist',
                                        searchable=False,
                                        clearable=False
                                    )
                                )
                            ],

                            className = 'row align-items-center'
                        )
                    ]
                ),

                html.Br(),

                dbc.Modal( #Modal = dialog box; feedback for successful saving
                        [
                            dbc.ModalHeader(
                                html.H4('Check-Up Save Success!')
                            ),
                            dbc.ModalBody(
                                'You may now return to the main portal!'
                            ),
                            dbc.ModalFooter(
                                [
                                dbc.Button(
                                    'Continue Encoding',
                                    id='continue_apptaddrecord',
                                    n_clicks = 0
                                ),
                                dbc.Button(
                                    'Proceed',
                                    href='/portal'
                                )
                                ]
                            )
                        ],
                centered=True,
                id='appt_addsuccessmodal',
                backdrop=True #Dialog box does not go away if you click the background
                ),

                dbc.Button(
                    "Submit",
                    id = 'submit_vetappointment',
                    n_clicks = 0
                )
            ],
            id = 'animal_vetappointment',
            hidden = True
        ),

        # ADOPTER INTERVIEW
        html.Div(
            [
                html.H2("Adopter Interview"),

                html.Br(),

                dbc.Alert(id='interview_addalert', is_open=False),

                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H4("Date of Appointment"),

                                        dcc.DatePickerSingle(
                                        id = 'interview_d',
                                        placeholder = 'Date',
                                        month_format = 'YYYY-MM-DD',
                                        min_date_allowed = '2020-04-01'
                                        )
                                        ]
                                ),

                                dbc.Col(
                                    html.Br()
                                ),

                                dbc.Col(
                                    html.Br()
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    html.B("Adopter Involved"),

                                    width = 2
                                ),

                                dbc.Col(
                                    dcc.Dropdown(
                                    placeholder="Menu",
                                    id='adpt_interviewlist',
                                    searchable=False,
                                    clearable=False
                                    )
                                )
                            ],

                            className = 'row align-items-center'
                        ),

                        html.Br(),
                    ]
                ),

                html.Br(),

                dbc.Modal( #Modal = dialog box; feedback for successful saving
                        [
                            dbc.ModalHeader(
                                html.H4('Interview Save Success!')
                            ),
                            dbc.ModalBody(
                                'You may now return to the main portal!'
                            ),
                            dbc.ModalFooter(
                                [
                                dbc.Button(
                                    'Continue Encoding',
                                    id='continue_interviewaddrecord',
                                    n_clicks = 0
                                ),
                                dbc.Button(
                                    'Proceed',
                                    href='/portal'
                                )
                                ]
                            )
                        ],
                centered=True,
                id='interview_addsuccessmodal',
                backdrop=True #Dialog box does not go away if you click the background
                ),

                dbc.Button(
                    "Submit",
                    id = 'submit_interviewappointment',
                    n_clicks = 0
                )
            ],
            id = 'sched_interviewappointment',
            hidden = True
        )        

    ],
    style = CONTENT_STYLE
)

# SITUATIONER

# VETERINARIAN CARE

# layout 1: SITUATIONER
# layout 2: VETERINARIAN CARE
    # Date of Appointment
    # Pet involved (assume one pet per appointment)
    # Assigned veterinarian