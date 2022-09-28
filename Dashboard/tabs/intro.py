from dash.dependencies import Input, Output
from dash import html, dcc 

from app import app

layout = [dcc.Markdown("""
#### Intro
This is where the text goes explaining our product and why it is useful.

Maybe also explain our methodology

Talk about what is on the other pages

Probably our names?
""")]
