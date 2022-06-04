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
from apps import dbconnect

CONTENT_STYLE = {
    "font-family": 'Avenir',
    'width':'450px', 
    'height':'45px', 
    'padding':'10px',
    'margin-top':'60px', 
    'fontSize':'16px', 
    'border-width':'3px',
    'border-color':'#FFFFFF'
}

CONTENT_STYLE_HEADER = {
    "font-family": 'Avenir',
    'width':'450px', 
    'height':'45px', 
    'padding':'10px',
    'margin-top':'60px',
    'border-width':'3px',
    'border-color':'#FFFFFF'
}

login = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H2("Welcome to the Lara's Ark Management System!")
                                ),

                                dbc.CardImg(
                                    src=app.get_asset_url('dog_collection.png'),
                                    style = {'width': '100%', 'height': 'auto'}
                                ),
                                
                                html.H4(
                                    "What is Lara's Ark?",
                                    style = {'marginLeft': '1em', 'marginTop': '1em'}),

                                dbc.CardBody(
                                    """
                                    Lara's Ark is an Animal Shelter established in June 2020
                                    whose primary goal is to act as a safe haven for lost dogs and animals
                                    found across the Philippines. Established months after Taal Volcano erupted
                                    and left some dogs stranded on the island, it's founder, Susan Lara, settled
                                    operations in Nasugbu, Batangas in order to house all kinds of stray dogs
                                    found and retrieved by the shelter's team of handlers.
                                    """
                                ),

                                dbc.CardBody(
                                    """
                                    As of December 2021, the Animal Shelter currently fields
                                    two sites, one in Nasugbu, Batangas and the other site in Mandaluyong.
                                    """
                                )
                            ]
                        )
                    ],

                    width = {'size': 6, 'offset': 1}
                ),

                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4("Log-in")
                                ),

                                dbc.CardBody(
                                    [

                                        html.H6("Username"),
                                        dbc.InputGroup(
                                            [
                                                dbc.CardImg(
                                                    src=app.get_asset_url("username_asset.png"),
                                                    style = {
                                                        'width':'14%', 
                                                        'height': 'auto',
                                                        'paddingRight': '1em'}
                                                    ),
                                                dbc.Input(id='user', type='text')
                                            ]
                                        ),

                                        html.Br(),

                                        html.H6("Password"),
                                        dbc.InputGroup(
                                            [
                                                dbc.CardImg(
                                                    src=app.get_asset_url("password_asset.png"),
                                                    style = {
                                                        'width':'14%', 
                                                        'height': 'auto',
                                                        'paddingRight': '1em'}
                                                ),
                                                dbc.Input(id='passw', type='password')
                                            ]
                                        )
                                    ]
                                ),

                                dbc.CardFooter(
                                    dbc.Button(
                                        'Log-in', 
                                        id='login', 
                                        n_clicks=0, 
                                        style={
                                            'font-family':'Avenir', 
                                            'border-width':'3px',
                                            'fontSize':'14px'}
                                    )
                                ),

                                html.Div(
                                    id='page_result'
                                )
                            ],
                        style = {
                                'width': '28rem',
                                'marginRight': '5em'
                            },
                        className = 'right'
                        )
                    ]
                )
            ],

        style = {'paddingTop': '2em'}
        ),       

    ]
    
)