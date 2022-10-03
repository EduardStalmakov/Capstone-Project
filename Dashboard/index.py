from dash.dependencies import Input, Output
from dash import html, dcc 

from app import app, server
from tabs import intro, investors, demographics, interface 


style = {'maxWidth': '1500px', 'margin': 'auto'}

tabs_styles = {
    'height': '60px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#6699CC',
    'color': 'white',
    'padding': '6px'
}


app.layout = html.Div([
    dcc.Markdown('# Music Streaming Song Recommender'),
    dcc.Tabs(id='tabs', value='tab-intro', children=[
        dcc.Tab(label='Intro', value='tab-intro', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Investors', value='tab-investors', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Demographics', value='tab-demographics', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='User Interface', value='tab-interface', style=tab_style, selected_style=tab_selected_style),
    ],style=tabs_styles),
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
    app.run_server()
