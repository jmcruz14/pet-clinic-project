import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

import plotly.express as px

import sys
sys.path.append('.')
sys.path.append('..')

from app import app
from apps import dbconnect as db

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

FONT_STYLE = {
    "font-style": "Avenir"
}

layout = html.Div(
    [

        html.Br(),

        html.H3("Reports Page"),
        html.P("""The reports page is the section of the website which contains everything you need to know about your company's business data. Costs,
        frequencies, and other statisically relevant data are shown in this section for use by the company to make better decisions regarding future
        company policy going forward."""),

        html.Br(),
        # Dropdown 
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Type of Statistic"),
                        dcc.Dropdown(
                            id = 'stat_type',
                            options = [
                                {'label': 'Average Cost of Successful Adoptions', 'value': 'successful_adoptions'},
                                {'label': 'Frequency of Adoptions', 'value':'freq_adoptions'} 
                            ],
                            style = {'width': '100%'}
                        )
                    ]
                ),

                dbc.Col(
                    [
                        html.H5("Period Covered"),
                        dcc.Dropdown(
                            id = 'stat_period',
                            options = [
                                {'label': 'per week', 'value': 'per week'},
                                {'label': 'per month', 'value': 'per month'}
                            ],
                            style = {'width': '100%'}
                    )
                    ]
                )
            ],
            justify = 'center',
            className = 'g-0'
        ),
        # Appropriate table for showing
        html.H4("hi!")
    ],
    style = CONTENT_STYLE
)