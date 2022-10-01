from ast import Div
from multiprocessing.sharedctypes import Value
import re
from dash.dependencies import Input, Output
from dash import html, dcc 
from app import app
import dash_table
# Importing my content based recommender
from model import content



# Let's Select User 3216 
User = 3216
Playlists = content.Playlist
Playlists = Playlists[Playlists['UserID'] == User].copy()


# Run a dropdown to select the playlist id

layout = html.Div(children=[
    html.H1(children='Welcome LOVES-DESIRE', style={'text-align': 'center'}),


    html.Div([
        html.Label(['Select User'],style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id = 'user',
            options = [
                {'label': 'LOVES-DESIRE', 'value': 3216 }, 
                {'label': 'theuskid', 'value': 3248}, 
                {'label': 'johnTMcNeill', 'value': 2980},
                {'label': 'demo-crassy', 'value': 3053},
                {'label': 'pogopatterson', 'value': 2352}
                 ],
            style={"width": "40%"},
            value= 3216
             ),
        html.Label(['Select Playlist'],style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='dropdown',
            style={"width": "40%"}),


    # Create the table with recommended songs
    html.Div(dash_table.DataTable(id='graph',style_table={'width': '100px'}, style_cell={'textAlign': 'center'})),

    
        ]),

])


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
    Output('graph', 'data'),
    [Input(component_id='dropdown', component_property='value')]
)

#Function to run the cosine similarity model and retun a dictionary from the dataframe as input for the dash_table
def select_graph(value):

    recommendations = content.display_recommendations(int(value))
    recommendations_slice = recommendations[['TrackName','ArtistName']]
    

    # fig = px.bar(t, x='TrackName', y='sim')
    final_data = recommendations_slice.to_dict('records')
    return final_data
