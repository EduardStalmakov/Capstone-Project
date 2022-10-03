
import re
from dash.dependencies import Input, Output
from dash import html, dcc, State
from app import app
from dash import dash_table
import plotly.express as px
# Importing my content based recommender
from model import content
from model import CollaborativeRecommender

# Getting the top 5 songs and top5 genres
Playlist_Tracks_merged = content.Playlist_Tracks.merge(content.Tracks, how='inner', on='TrackID')
top_5_songs = Playlist_Tracks_merged['TrackName'].value_counts().sort_values(ascending=False)[0:5]
top_5_genre = Playlist_Tracks_merged['Genres'].value_counts().sort_values(ascending=False)[0:5]
top_5_artist = Playlist_Tracks_merged['ArtistName'].value_counts().sort_values(ascending=False)[0:5]


# Page Layout

layout = html.Div(children=[

    # Div for drop down and main text
    html.Div([
    html.Label(['Select User'],style={'font-weight': 'bold','padding':'0.8rem'}),
        dcc.Dropdown(
            id = 'user',
            options = [
                {'label': 'LOVES-DESIRE', 'value': 3216 }, 
                {'label': 'theuskid', 'value': 3248}, 
                {'label': 'johnTMcNeill', 'value': 2980},
                {'label': 'demo-crassy', 'value': 3053},
                {'label': 'pogopatterson', 'value': 2352}
                 ],
            style={'padding':'0.8rem', 'width':'250px'},
            value= 3216
             ),
    html.H1(id='user-text', style={'text-align': 'center'}),
    ], style={'display':'inline','width': '100%'}),


    # Div to hold graphs in a row
    html.Div([

    dcc.Graph(id = 'top-5-song', figure= px.bar(x=top_5_songs.index, y=top_5_songs.values, title='Top Trending Songs', 
                labels={'x':'Song','y':'Count on Playlists'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 
                'border-radius': '10px', 'backgroundColor': 'grey', 'width':'100%'}),


    dcc.Graph(id = 'top-5-genre', figure= px.bar(x=top_5_genre.index, y=top_5_genre.values, title='Top Trending Genres', 
                labels={'x':'Genre','y':'Count on Playlists'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 
                'border-radius': '10px', 'backgroundColor': 'grey','width':'100%' }),

    dcc.Graph(id = 'top-5-artist', figure= px.bar(x=top_5_artist.index, y=top_5_artist.values, title='Top Trending Artists', 
                labels={'x':'Artist','y':'Count on Playlists'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 
                'border-radius': '10px', 'backgroundColor': 'grey','width':'100%'}),
    ],style={'display':'inline-flex','width': '100%'}),


    # Recommendations title
    html.H4(['Get recommendations based on a playlist in real time!'],style={'text-align':'left'}),

    # Div to hold playlist selection box
    html.Div([
        html.Label(['Select Playlist'],style={'font-weight': 'bold', 'padding':'0.8rem'}),
        html.Br(),
        dcc.Dropdown(
            id='dropdown',
            value = 9519,
            style={'padding':'0.8rem', 'width':'500px'}),
    ],style={'display':'inline-flex'}),


    # Div to show the recommendations in a table
    html.Div([
        dash_table.DataTable(id='recommendations',style_table={'width': '100px' }, style_cell={'textAlign': 'center'}),]),

    html.H4(['Get recommendations based on what other users saved to their playlists: Type a Song Name'],style={'text-align':'left'}),

    # creating a search box
    html.Br(),
    html.Div([
        dcc.Input(
            id = 'input-on-submit',
            type = 'text',
            placeholder=" Search a song name"
        ),
        html.Button('Submit', id='submit-val'),
        html.Br(),
        #if you like that try this statement
        html.Div(id='song-output'),
        
        #top ten songs like that
        dash_table.DataTable(id='search',style_table={'width': '100px'}, style_cell={'textAlign': 'center'}),
    ]),
    #make the radar
    html.Div([

        dcc.Graph(id='radar'),
    ])

])


# Callbacks and functions

# Call back for collaborative machine learning
#callback song name
@app.callback(
    Output(component_id='song-output', component_property='children'),
    #[Input(component_id='submit-val', component_property='n_clicks')],
    Input('input-on-submit', 'value'))
def get_song(value):
    song = CollaborativeRecommender.songName(str(value))
    return f'If you like {song}, you should try:'


#callback list of songs:
@app.callback(
    Output(component_id='search', component_property='data'),
    #[Input(component_id='submit-val', component_property='n_clicks')],
    Input(component_id='input-on-submit', component_property='value'))
def search_recommendations(value):
    df = CollaborativeRecommender.finder(str(value))
    p = df.to_dict('records')
    return p

#callback radar figure
@app.callback(
    Output(component_id='radar', component_property='figure'),
    Input(component_id='input-on-submit', component_property='value'))
def radar_maker(value):
    df = CollaborativeRecommender.finder(str(value))
    radar= px.line_polar(df, r='Similarity_Value', theta='Song_Artist', line_close=True, markers=True, title=f'The closer to the center, the more similar the song:', style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'grey', 'width':'100%'}),
    radar.update_traces(fill='toself')
    return radar


#callback for welcome
@app.callback(
    Output('user-text', 'children'),
    [Input(component_id='user', component_property='value')]
)
def change_user_welcome_message(value):
    user = content.Users
    user = user[user['UserID'] == int(value)].copy()

    return f"Welcome {user['UserName'].values[0]}"

#callback for 
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