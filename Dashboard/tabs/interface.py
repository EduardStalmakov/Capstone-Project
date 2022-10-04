


import re
from dash.dependencies import Input, Output
from dash import html, dcc, State, dash_table
from app import app
import plotly.express as px
# Importing my content based recommender
from model import content
from model import CollaborativeRecommender
from model import collab
import dash_bootstrap_components as dbc
import requests
import json

# Getting the top 5 songs and top5 genres
Playlist_Tracks_merged = content.Playlist_Tracks.merge(content.Tracks, how='inner', on='TrackID')
top_5_songs = Playlist_Tracks_merged['TrackName'].value_counts().sort_values(ascending=False)[0:5]
top_5_genre = Playlist_Tracks_merged['Genres'].value_counts().sort_values(ascending=False)[0:5]
top_5_artist = Playlist_Tracks_merged['ArtistName'].value_counts().sort_values(ascending=False)[0:5]


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Select User", className="display-4"),
        html.Hr(),
        html.P(
            "Pick one user to view your personalized dashboard", className="lead"
        ),
        dcc.Dropdown(
            id = 'user',
            options = [
                {'label': 'LOVES-DESIRE', 'value': 3216 }, 
                {'label': 'theuskid', 'value': 3248}, 
                {'label': 'johnTMcNeill', 'value': 2980},
                {'label': 'demo-crassy', 'value': 3053},
                {'label': 'pogopatterson', 'value': 2352}
                 ],
            style={'backgroundColor': '#F5F5F5', 'width':'13rem','justify-content':'center', 'align-items':'center'},
            value= 3216
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Page Layout

layout = html.Div([
sidebar, 
html.Div(children=[
    

    # Div for drop down and main text
    html.Div([
    # html.Label(['Select User'],style={'font-weight': 'bold','padding':'0.8rem', 'font-size':'20px'}),
        # dcc.Dropdown(
        #     id = 'user',
        #     options = [
        #         {'label': 'LOVES-DESIRE', 'value': 3216 }, 
        #         {'label': 'theuskid', 'value': 3248}, 
        #         {'label': 'johnTMcNeill', 'value': 2980},
        #         {'label': 'demo-crassy', 'value': 3053},
        #         {'label': 'pogopatterson', 'value': 2352}
        #          ],
        #     style={'backgroundColor': '#F5F5F5', 'width':'400px','justify-content':'center', 'align-items':'center'},
        #     value= 3216
        #      ),
    html.H1(id='user-text', style={'text-align': 'center', 'color':'#6699CC', 'font-weight':'bold','font-size':'60px'}),
    ], style={'width': '100%','align-items': 'center', 'justify-content': 'center'}),

    html.Div([
    # Div to hold graphs in a row

    html.Div([
    # Recommendations title
    html.H4(['Choose a playlist to get song recommendations in real time!'],style={'text-align':'left', 'padding':'0.9rem','font-size':'20px'}),


    # Div to hold playlist selection box
    html.Div([
        # html.Label(['Select Playlist'],style={'font-weight': 'bold', 'padding':'0.8rem'}),
        # html.Br(),
        dcc.Dropdown(
            id='dropdown',
            value = 9519,
            style={'backgroundColor': '#F5F5F5', 'width':'500px'}),
    ],style={'display':'inline-flex'}),


    # Div to show the recommendations in a table
    html.Div([
        dash_table.DataTable(id='recommendations',style_table={'width': '100px', 'padding':'0.8rem'}, style_cell={'textAlign': 'left'}),]),

    html.H4(['Get recommendations based on what other users saved to their playlists: Type a Song Name'],style={'text-align':'left','font-size':'20px'}),

    #////////////////// collab recommender section
    html.Div([
        html.Div(dcc.Input(id='input-on-submit', type='text')),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic',
                children='Enter a value and press submit'),
        #if you like statement
        html.Div(id='ifYouLike')
    ]),
        html.Div([
        dash_table.DataTable(id='goodsongs',style_table={'width': '100px'}, style_cell={'textAlign': 'center'})
        # dcc.Graph(id='graph')
    ]),

    html.Br(),
    html.Br(),
    html.H4(['Get a song recommendation from LastFm'],style={'text-align':'left','font-size':'20px', 'padding':'1rem'}),
    html.H4(['Type an artist followed by a track name'],style={'text-align':'left','font-size':'20px'}),
    html.Div([
        dcc.Input(
            id = 'input-on-submit-lastfm-artist',
            type = 'text',
            placeholder="Artist",
            style={'backgroundColor': '#F5F5F5'}
        ),
        dcc.Input(
            id = 'input-on-submit-lastfm-track',
            type = 'text',
            placeholder="Track",
            style={'backgroundColor': '#F5F5F5'}
        ),
        html.Button('Submit', id='submit-lastfm'),
        html.H4(['Below is the Recommendation:'],style={'text-align':'left','font-size':'20px'}),
        html.Label(id='lastfm')
    ])
    ]),
    html.Div([

    dcc.Graph(id = 'top-5-song', figure= px.bar(x=top_5_songs.index, y=top_5_songs.values, title='Top Trending Songs', 
                labels={'x':'Song','y':'Count on Playlists'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White', 'width':'500px'}),


    dcc.Graph(id = 'top-5-genre', figure= px.bar(x=top_5_genre.index, y=top_5_genre.values, title='Top Trending Genres', 
                labels={'x':'Genre','y':'Count on Playlists'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White','width':'500px' }),

    dcc.Graph(id = 'top-5-artist', figure= px.bar(x=top_5_artist.index, y=top_5_artist.values, title='Top Trending Artists', 
                labels={'x':'Artist','y':'Count on Playlists'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White','width':'500px'}),
    ]),
    ], style={'display':'inline-flex'})
])],style={'display':'inline'})


# Callbacks and functions


# Call back for collaborative machine learning
#callback for search box SUCCESS!!
# @app.callback(
#     Output(component_id='container-button-basic', component_property='children'),
#     Input(component_id='submit-val', component_property='n_clicks'),
#     State(component_id='input-on-submit', component_property='value')
# )

# def update_output(n_clicks, value):
#     return 'The input value was "{}" and the button has been clicked {} times'.format(value, n_clicks)

#callback to get "if you like" statement SUCCESS!!
@app.callback(
    Output(component_id='ifYouLike', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='input-on-submit', component_property='value')
)
def ifYouLike(value, n_clicks):
    print('this is n_clicks')
    print(n_clicks)
    print('this is value')
    print(value)
    if n_clicks is not None:
        song = CollaborativeRecommender.songName(str(n_clicks))
        if len(song)<1:
            print(f"hmm... can't find any songs with '{value}.' Try again.")
            
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
    [Input(component_id='user', component_property='value')]
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
    

    # fig = px.bar(t, x='TrackName', y='sim')
    final_data = recommendations_slice.to_dict('records')
    return final_data

@app.callback(
    Output('lastfm', 'children'),
    [Input(component_id='submit-lastfm', component_property='n_clicks')],
    [State('input-on-submit-lastfm-artist','value'), State('input-on-submit-lastfm-track', 'value')])
def get_lastfm_recommendation(n_clicks, artist, track ):
    artist = str(artist)
    track = str(track)
    lastfm_reco = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={artist}&track={track}&api_key=5dcdb3fc11650a31b1a095bb49ccba72&format=json").text
    lastfm_reco_json = json.loads(lastfm_reco)
    reco_song = lastfm_reco_json['similartracks']['track'][0]['name']
    reco_artist = lastfm_reco_json['similartracks']['track'][0]['artist']['name']
    url = lastfm_reco_json['similartracks']['track'][0]['url']
    r = f"""Track Name: {reco_song} 
            Artist: {reco_artist}
            Url: {url}"""
    n = n_clicks
    
    return r