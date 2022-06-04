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
        html.H4("Adopter Database", style = {'text-align': 'center'}),

        html.Br(),
        
        dbc.Table(
            id = 'adopter_table'
        ),

        dbc.Modal(
            [
                dbc.ModalHeader("Delete Successful!")
            ],
            centered=True,
            id='adopter_delsuccessmodal',
            backdrop=True,
            scrollable=True,
            is_open=False
        )
    ],

    style = CONTENT_STYLE
)