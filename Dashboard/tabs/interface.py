# References external libraries
from dash.dependencies import Input, Output
from dash import html, dcc, State, dash_table
from app import app
# References files in this repository
from model import content
from model import CollaborativeRecommender
from tabs.supp_files import db_metrics

SIDEBAR_STYLE = {
    "position"          :   "fixed",
    "top"               :   0,
    "left"              :   0,
    "bottom"            :   0,
    "width"             :   "16rem",
    "padding"           :   "2rem 1rem",
    "background-color"  :   "#BDBDBD",
}

# The styles for the main content position it to the right of the sidebar and add some padding.
CONTENT_STYLE = {
    "margin-left"       : "18rem",
    "margin-right"      : "2rem",
    "padding"           : "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2(
            "Select User", className = "display-4",
            style = {'color' : 'black', 'fontSize' : '5rem', 'fontWeight' : 'bold'}
        ),
        html.Hr(),
        html.P(
            "Pick one user to view your personalized dashboard", className = "lead",
            style = {'color' : 'black', 'fontSize' : '2rem'}
        ),
        dcc.Dropdown(
            id = 'user',
            options = [
                {'label': 'LOVES-DESIRE',   'value': 3216}, 
                {'label': 'theuskid',       'value': 3248}, 
                {'label': 'johnTMcNeill',   'value': 2980},
                {'label': 'demo-crassy',    'value': 3053},
                {'label': 'pogopatterson',  'value': 2352}
            ],
            style = {'fontSize' : '1.5rem', 'backgroundColor' : 'white', 'width' : '13rem', 
                        'justify-content' : 'center', 'align-items' : 'center'},
            value = 3216
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Page Layout
layout = html.Div(
    [
        sidebar, 
        html.Div(children = 
            [
                # Div for drop down and main text
                html.Div(
                    [
                        html.H1(id='user-text', style={'text-align': 'center', 'color':'#6699CC', 'font-weight':'bold','font-size':'60px'}),
                    ], 
                    style={'width': '100%','align-items': 'center', 'justify-content': 'center'}
                ),
                html.Div(
                    [
                        # Div to hold graphs in a row
                        html.Div(
                            [
                                # Recommendations title
                                html.H4(
                                    'Choose a playlist to get song recommendations in real time!',
                                    style = {'text-align' : 'left', 'padding' : '0.9rem', 'fontSize' : 40}
                                ),
                                # Div to hold playlist selection box
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id='dropdown',
                                            value = 9519,
                                            style={'backgroundColor' : '#F5F5F5', 'width' : '500px', 'fontSize' : 12}
                                        ),
                                    ],
                                    style={'display':'inline-flex'}
                                ),
                                # Div to show the recommendations in a table
                                html.Div(
                                    [
                                        dash_table.DataTable(
                                            id='recommendations',
                                            style_table={'width': '50rem', 'padding':'0.8rem'}, 
                                            style_cell={'textAlign': 'left', 'fontSize' : 20},  
                                            style_as_list_view=True,          
                                            style_header={
                                                'backgroundColor': '#003B6D',
                                                'fontWeight': 'bold',
                                                'fontSize' : 20
                                            },
                                        )
                                    ]
                                ),   
                                html.H4([''], style = {'text-align' : 'left'}),
                                html.H4(
                                    'Get recommendations based on what other users saved to their playlists:',
                                    style = {'text-align' : 'left', 'fontSize' : 40}
                                ),
                                html.H4(
                                    'Type a Song Name',
                                    style = {'text-align' : 'left', 'fontSize' : 30}
                                ),                                
                                # Collab recommender section
                                html.Div(
                                    [
                                        html.Div(
                                            dcc.Input(
                                                id='input-on-submit', type='text',
                                                style = {'fontSize' : 30}
                                            )
                                        ),
                                        html.Button(
                                            'Submit', id='submit-val', n_clicks=0,
                                            style = {'fontSize' : 30}
                                        ),
                                        html.Div(
                                            id='container-button-basic',
                                            children='Enter a value and press submit'
                                        ),
                                        html.Div(html.P([html.Br(),''])),
                                         # If you like statement
                                        html.Div(id='ifYouLike')
                                    ]
                                ),
                                html.Div(
                                    [
                                        dash_table.DataTable(
                                            id='goodsongs',
                                            style_table={'max-width': '100%', 'word-wrap' : 'break-word'}, 
                                            style_cell={'textAlign': 'center', 'fontSize' : 20}, 
                                            style_as_list_view=True,
                                            style_header={
                                                'backgroundColor': '#003B6D',
                                                'fontWeight': 'bold',
                                                'fontSize' : 20
                                            },
                                        )
                                    ]
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'top-5-song', 
                                    figure = db_metrics.top_5_track, 
                                    style = {
                                        'padding' : '0.8rem', 'marginTop':'1rem', 'marginLeft' : '1rem', 'boxShadow' : '#e3e3e3 2px 2px 1px', 
                                        'border-radius' : '10px', 'backgroundColor' : '#BDBDBD', 'width' : '500px'
                                    }
                                ),
                                dcc.Graph(
                                    id = 'top-5-genre', 
                                    figure = db_metrics.top_5_genre,
                                    style = {
                                        'padding' : '0.8rem', 'marginTop' : '1rem', 'marginLeft' : '1rem', 'boxShadow' : '#e3e3e3 2px 2px 1px', 
                                        'border-radius' : '10px', 'backgroundColor' : '#BDBDBD', 'width' :'500px'
                                    }
                                ),
                                dcc.Graph(
                                    id = 'top-5-artist', 
                                    figure = db_metrics.top_5_artist,
                                    style = {
                                        'padding' : '0.8rem', 'marginTop' : '1rem', 'marginLeft' : '1rem', 'boxShadow' : '#e3e3e3 2px 2px 1px', 
                                        'border-radius' : '10px', 'backgroundColor' : '#BDBDBD', 'width' : '500px'
                                    }
                                ),
                            ]
                        ),
                    ], 
                    style={'display':'inline-flex'}
                )
            ]
        )
    ],
    style={'display':'inline'}
)


#callback to get "if you like" statement SUCCESS!!
@app.callback(
    Output(component_id='ifYouLike', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='input-on-submit', component_property='value')
)
def ifYouLike(value, n_clicks):
    if n_clicks is not None:
        song = CollaborativeRecommender.songName(str(n_clicks)) 
        if len(song)<1:
            return f"hmm... can't find any songs with '{n_clicks}.' Try again."    
        else: 
            return f'If you like {song}, you should try:'


#callback collab table SUCCESS!!
@app.callback(
    Output(component_id='goodsongs', component_property='data'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='input-on-submit', component_property='value')
)
def search_recommendations(value, n_clicks):
    if n_clicks is not None:
        r = CollaborativeRecommender.finder(str(n_clicks))
        if len(r)<0:
            print('')
        else:  
            goodsongs = r.to_dict('records')
            return goodsongs


@app.callback(
    Output('user-text', 'children'),
    [Input(component_id = 'user', component_property = 'value')]
)
def change_user_welcome_message(value):
    user = content.Users
    user = user[user['UserID'] == int(value)].copy()

    return f"Welcome {user['UserName'].values[0]}"


@app.callback(
    Output('dropdown', 'options'),
    [Input(component_id='user', component_property='value')]
)
def select_user(value):
    Playlists = content.Playlist
    Playlists = Playlists[Playlists['UserID'] == value].copy()
    options = [{'label': playlist[2], 'value': playlist[0]} for playlist in Playlists.values]
    return options


#callback function to get the selected dropdown value and output the data from the function
@app.callback(
    Output('recommendations', 'data'),
    [Input(component_id='dropdown', component_property='value')]
)
#Function to run the cosine similarity model and retun a dictionary from the dataframe as input for the dash_table
def get_recommendations(value):
    recommendations = content.display_recommendations(int(value))
    recommendations_slice = recommendations[['TrackName','ArtistName']]
    final_data = recommendations_slice.to_dict('records')
    return final_data