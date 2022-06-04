import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

from dash.exceptions import PreventUpdate

import sys
sys.path.append('.')
sys.path.append('..')

from app import app

navlink_style = {
    'color': '#fff',
    'font-family': 'Avenir'
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#ffcc66",
    'whiteSpace': 'normal',
    'overflow': 'scroll'
}

navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                html.Img(
                    src=app.get_asset_url('companylogo.jpg'), 
                    style={'height':'5%', 'width':'5%', 'padding-Right': '10em'}
                    ),
                    html.A(
                    dbc.NavbarBrand(
                        "Lara's Ark Shelter", 
                        style={'padding':'10px', 'margin-Left':'10em','font-family':'Avenir'}, 
                        className="m1-2"),
                        href="/home",
                        style = {'padding-Left': '5px'}
                        )
            ],
            align='center',
            no_gutters=True,    
        )

    ],
    dark = True,
    color = '#ffaa00'
)

# Remarks for Main Navbar – change the style color of the bootstrap navpill styles

navbar_main = html.Div(
    [
        html.Center(
            html.Img(
                    src=app.get_asset_url('companylogo.jpg'), 
                    style={'height':'13rem', 'width':'13rem'}
                    )
                    ),
        html.Br(),
        html.Center(
            html.H2("Lara's Ark", style={"fontSize": "1.5rem", "font-weight": "600"})
        ),
        html.Center(
            html.H4(id='shelter_br', style={"fontSize": "1.05rem", "font-weight": "300"})
        ),
        html.Hr(),
        html.P(
            """Welcome to the company management system!
            Please select a function.""", style = {'fontSize': '15px', 'font-weight': '300'}
        ),
        dbc.Nav(
            [
                # Create Edit Search
                dbc.NavLink("Homepage", href="/portal", active="exact"), #style={'color':'black'}),

                # Create Edit Search
                dbc.NavLink("Animal Record", href="/pet/menu", active="exact"),

                # Create Edit History
                dbc.DropdownMenu(
                    label = "Animal Adoptions",
                    children = [

                        dbc.DropdownMenuItem("Add an Adopter", href='/adoptions?mode=add'),

                        dbc.DropdownMenuItem("Adopter Database", href="/adoptions/adopter_list"),

                        dbc.DropdownMenuItem("Adoption History", href="/adoptions/history"),

                    ],
                    style = {'marginLeft':'0.25em'},
                    toggle_style = {'background': '#f7b430'}
                ),

                dbc.DropdownMenu(
                    label = "Animal Care",
                    children = [
                        
                        dbc.DropdownMenuItem("Adopt an Animal", href='/schedule/adopt'),

                        dbc.DropdownMenuItem("Schedule Events", href='/schedule/animalcare_event'),
                        
                        # Schedule Edit Search
                        dbc.DropdownMenuItem("Shelter Schedule", href='/schedule')
                    ],
                    style={'marginLeft':'0.25em'},
                    toggle_style={
                        'background': '#f7b430'
                    }
                ),

                # Create Edit Search
                dbc.NavLink("Medical Inventory", href="/medicine", active="exact"),

                # Generate
                dbc.NavLink("Financials and Other Reports", href='/reports', disabled=False, active="exact"),

                # Create Edit Search
                dbc.NavLink("Veterinarian", href='/vet/menu', active="exact"),

                # Log out
                dbc.NavLink("Log Out", href='/home', active="exact")
            ],
            vertical=True,
            pills=True
        ),
        html.Br(),
        html.Br(),
        html.Footer(
            [
                html.H5(
                    "Contact us:", style = {'fontFamily': 'Avenir'}),
                dbc.Row(
                    [
                        dbc.Col(html.Img(
                            src = app.get_asset_url('telephone_icon.png'),
                            style = {'height': '1.25em', 'width':'1.25em', 
                            'marginRight':'0.5em', 'paddingLeft':'0.5px',
                            'top': 0.5, 'left': 0, 'paddingBottom': '2px'} #adjust height
                            ),
                            width = 'auto'),
                        dbc.Col(html.H6(
                            '0917 808 4826 / 0917 896 9668', 
                            style = {'fontFamily':'Avenir', 'wordWrap': 
                            'break-word', 'fontSize': '12px', 'top': 0,
                            'left': 0, 'marginTop': '5px'},
                            ),
                            width = 'auto')
                    ],
                    no_gutters = True
                    ),
                html.P(
                    id = 'shelter_l', 
                    style = {'fontFamily': 'Avenir', 'fontWeight':'100px', 'fontSize': '12px'})
            ]
        )
    ],
    style=SIDEBAR_STYLE,
)