

import re
from dash.dependencies import Input, Output
from dash import html, dcc, State
from app import app
import dash_table
import plotly.express as px
# Importing my content based recommender
from model import content
from model import CollaborativeRecommender
from model import collab
import dash_bootstrap_components as dbc

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

    html.H4(['Get recommendations based on what other users saved to their palylists: Type a Song Name'],style={'text-align':'left','font-size':'20px'}),

    # creating a search box
    html.Br(),
    html.Div([
        dcc.Input(
            id = 'input-on-submit',
            type = 'text',
            placeholder="Top",
            style={'backgroundColor': '#F5F5F5'}
        ),
        html.Button('Submit', id='submit-val'),
        dash_table.DataTable(id='searchtable',style_table={'width': '800px'}, style_cell={'textAlign': 'left', 'overflow':'hidden','maxWidth':'0'}),
        # dcc.Graph(id='search', style={'padding':'0.8rem'})
    ]),
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

# @app.callback(
#     Output('search', 'figure'),
#     [Input(component_id='submit-val', component_property='n_clicks')],
#     [State('input-on-submit', 'value')])
# def search_recommendations_graph(value, n_clicks):
#     r = CollaborativeRecommender.finder(str(value), n_clicks)
#     fig = px.bar(r,x='Artist', y='Similarity_value')
#     return fig
    
@app.callback(
    Output('searchtable', 'data'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [State('input-on-submit', 'value')])
def search_recommendations(value, n_clicks):
    r = CollaborativeRecommender.finder(str(value), n_clicks)
    p = r.to_dict('records')
    return p
    


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
