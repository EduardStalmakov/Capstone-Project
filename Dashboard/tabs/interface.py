from ast import Div
from multiprocessing.sharedctypes import Value
import re
from dash.dependencies import Input, Output
from dash import html, dcc 
from app import app
import dash_table
# Importing my content based recommender
from model import content



# Let's Select User 2724 
User = 3216
Playlists = content.Playlist
Playlists = Playlists[Playlists['UserID'] == User].copy()


# Run a dropdown to select the playlist id

layout = html.Div(children=[
    html.H1(children='Welcome LOVES-DESIRE', style={'text-align': 'center'}),


    html.Div([
        html.Label(['Choose a Playlist'],style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': playlist[2], 'value': playlist[0]} for playlist in Playlists.values],
            value='10697',
            style={"width": "40%"}),

    # Create the table with recommended songs
    html.Div(dash_table.DataTable(id='graph',style_table={'width': '100px'}, style_cell={'textAlign': 'center'})),


        ]),

])

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
