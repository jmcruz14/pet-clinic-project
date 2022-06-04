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
}

FONT_STYLE = {
    "font-style": "Avenir"
}

layout = html.Div(
    [

        html.Center(
            dbc.Carousel(
            items = [
                {'key': '1', 'src':'assets/static/images/slide_1.jpg'},
                {'key': '2', 'src':'assets/static/images/slide_2.jpg'},
                {'key': '3', 'src':'assets/static/images/slide_3.jpg'}
            ],
            controls = False,
            indicators = False,
            interval = 2000,
            ride = 'carousel',
            className = 'd-block w-75 h-75' 
            )
        ),
        html.Br(),
        html.Div(
            [
                html.H2(
                    html.P("What is Lara's Ark?", style = FONT_STYLE)
                    ),
                html.P("""Lara's Ark is an Animal Shelter established in June 2020
                whose primary goal is to act as a safe haven for lost dogs and animals
                found across the Philippines. Established months after Taal Volcano erupted
                and left some dogs stranded on the island, it's founder, Susan Lara, settled
                operations in Nasugbu, Batangas in order to house all kinds of stray dogs
                found and retrieved by the shelter's team of handlers.""", style = FONT_STYLE),
                html.Br(),
                html.P("""As of December 2021, the Animal Shelter currently fields
                two sites, one in Nasugbu, Batangas and the other site in Mandaluyong.""", style = FONT_STYLE)
            ]
        )
    ],
    style = CONTENT_STYLE
)