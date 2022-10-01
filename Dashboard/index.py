from dash.dependencies import Input, Output
from dash import html, dcc 

from app import app, server
from tabs import intro, investors, demographics, interface 
from model import content

style = {'maxWidth': '1500px', 'margin': 'auto'}

app.layout = html.Div([
    dcc.Markdown('# Music Streaming Song Recommender'),
    dcc.Tabs(id='tabs', value='tab-intro', children=[
        dcc.Tab(label='Intro', value='tab-intro'),
        dcc.Tab(label='Investors', value='tab-investors'),
        dcc.Tab(label='Demographics', value='tab-demographics'),
        dcc.Tab(label='User Interface', value='tab-interface'),
    ]),
    html.Div(id='tabs-content'),
], style=style)

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-intro': return intro.layout
    elif tab == 'tab-investors': return investors.layout
    elif tab == 'tab-demographics': return demographics.layout
    elif tab == 'tab-interface': return interface.layout

if __name__ == '__main__':
    app.run_server(debug=True)
