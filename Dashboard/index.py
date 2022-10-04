from dash.dependencies import Input, Output
from dash import html, dcc 

from app import app, server
from tabs import intro, target, scenes, interface 
from model import content

style = {'maxWidth': '1400px', 'margin': 'auto'}

app.layout = html.Div([
    dcc.Markdown('# Music Streaming Song Recommender'),
    dcc.Tabs(id='tabs', value='tab-interface', children=[
        dcc.Tab(label='User Interface', value='tab-interface'),
        dcc.Tab(label='Intro', value='tab-intro'),
        dcc.Tab(label='Behind the Scenes', value='tab-scenes'),
        dcc.Tab(label='Target Market', value='tab-target'),
        
    ]),
    html.Div(id='tabs-content'),
], style=style)

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-intro': return intro.layout
    elif tab == 'tab-target': return target.layout
    elif tab == 'tab-scenes': return scenes.layout
    elif tab == 'tab-interface': return interface.layout

if __name__ == '__main__':
    app.run_server(debug=True)
