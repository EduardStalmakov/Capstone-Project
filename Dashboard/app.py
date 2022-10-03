import dash
import dash_bootstrap_components as dbc

external_stylesheets = ['bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.config.suppress_callback_exceptions = True
server = app.server
