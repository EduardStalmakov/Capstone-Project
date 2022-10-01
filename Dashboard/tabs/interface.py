
import re
from dash.dependencies import Input, Output
from dash import html, dcc 
from app import app
import dash_table
import plotly.express as px
# Importing my content based recommender
from model import content

# Getting the top 5 songs and top5 genres
Playlist_Tracks_merged = content.Playlist_Tracks.merge(content.Tracks, how='inner', on='TrackID')
top_5_songs = Playlist_Tracks_merged['TrackName'].value_counts().sort_values(ascending=False)[0:5]
top_5_genre = Playlist_Tracks_merged['Genres'].value_counts().sort_values(ascending=False)[0:5]
top_5_artist = Playlist_Tracks_merged['ArtistName'].value_counts().sort_values(ascending=False)[0:5]


# Page Layout

layout = html.Div(children=[
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
            style={'padding':'0.8rem', 'width':'800px'},
            value= 3216
             ),
    html.H1(id='user-text', style={'text-align': 'center'}),
    html.Div([

    dcc.Graph(id = 'top-5-song', figure= px.bar(x=top_5_songs.index, y=top_5_songs.values, title='Top Trending Songs', labels={'x':'Song','y':'Count on Playlists'}), style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'grey', 'width':'100%'}),
    dcc.Graph(id = 'top-5-genre', figure= px.bar(x=top_5_genre.index, y=top_5_genre.values, title='Top Trending Genres', labels={'x':'Genre','y':'Count on Playlists'}), style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'grey','width':'100%' }),
    dcc.Graph(id = 'top-5-artist', figure= px.bar(x=top_5_artist.index, y=top_5_artist.values, title='Top Trending Artists', labels={'x':'Artist','y':'Count on Playlists'}), style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'grey','width':'100%'}),
    ],style={'display':'inline-flex','width': '100%'}),

    html.H4(['Get recommendations based on a playlist in real time!'],style={'text-align':'left'}),
    html.Div([
        html.Label(['Select Playlist'],style={'font-weight': 'bold', 'padding':'0.8rem'}),
        html.Br(),
        dcc.Dropdown(
            id='dropdown',
            value = 9519,
            style={'padding':'0.8rem', 'width':'300px'}),
    ],style={'display':'inline-flex'}),

    # Create the table with recommended songs
    html.Div([
        dash_table.DataTable(id='recommendations',style_table={'width': '100px'}, style_cell={'textAlign': 'center'})]),

])

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
