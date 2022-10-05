from dash.dependencies import Input, Output
from dash import html, dcc 
from app import app
from tabs import intro, target, scenes, interface 

style = {'maxWidth' : '1300px', 'margin': 'auto'}

tab_style = {
    'borderBottom'  : '1px solid #d6d6d6',
    'padding'       : '6px',
    'fontWeight'    : 'bold',
    'height'        : '70px',
    'fontSize'      : '2rem'
}

tab_selected_style = {
    'borderTop'         : '1px solid #d6d6d6',
    'borderBottom'      : '1px solid #d6d6d6',
    'backgroundColor'   : '#6699CC',
    'color'             : 'white',
    'padding'           : '6px',
    'fontSize'          : '2rem',
    'fontWeight'        : 'bold',
}

app.layout = html.Div([
    html.H1(
        'Music Streaming Song Recommender',
        style = {'color' : '#6699CC', 'fontSize' : '3rem'}
    ),
    dcc.Tabs(
        id='tabs', value = 'tab-interface', 
        children=[
            dcc.Tab(label = 'User Interface', value = 'tab-interface', style=tab_style, selected_style = tab_selected_style),
            dcc.Tab(label = 'Target Market', value = 'tab-target', style=tab_style, selected_style = tab_selected_style),
            dcc.Tab(label = 'About', value = 'tab-intro', style=tab_style, selected_style = tab_selected_style),
            dcc.Tab(label = 'Behind the Scenes', value = 'tab-scenes', style=tab_style, selected_style = tab_selected_style),
        ]
    ),
    html.Div(id = 'tabs-content'),
], style=style)

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab      ==  'tab-intro': return intro.layout
    elif tab    ==  'tab-target': return target.layout
    elif tab    ==  'tab-scenes': return scenes.layout
    elif tab    ==  'tab-interface': return interface.layout

if __name__     == '__main__':
    app.run_server()