import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import logging

app = dash.Dash(__name__, external_stylesheets=['assets/bootstrap_custom.css'])
server = app.server

app.config.suppress_callback_exceptions = True

app.css.config.serve_locally = True

app.scripts.config.serve_locally = True

app.title = "Lara's Ark Shelter" #Browser Tab Title

log = logging.getLogger('werkezug')
log.setLevel(logging.ERROR)
