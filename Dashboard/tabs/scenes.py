# References external libraries
from dash.dependencies import Input, Output
from dash import html, dcc
import dash_bootstrap_components as dbc
# References files in the repository
from app import app
from tabs.supp_files import pl_sizes, db_metrics

# Render the page(s) layout
SIDEBAR_STYLE = {
    'position'          :   'fixed',
    'top'               :   0,
    'left'              :   0,
    'bottom'            :   0,
    'width'             :   '16rem',
    'padding'           :   '2rem 1rem',
    'background-color'  :   '#BDBDBD',
}

sidebar = html.Div(
    [
        html.H2(
            'Learn More', className = 'sidebar-title', 
            style = {'color' : 'black', 'fontSize' : '5rem', 'fontWeight' : 'bold'}
        ),
        html.Hr(),
        html.P(
            'A quick glimpse behind the scenes', className = 'lead', 
            style = {'color' : 'black', 'fontSize' : '2rem'}
        ),
        dbc.Nav(
            [
                dbc.NavLink(
                    'Database Metrics', href = '/', active = 'exact',
                    style = {'fontSize' : '1.5rem'}
                ),
                html.P(),
                dbc.NavLink(
                    'Machine Learning Models', href = '/ml_models', active = 'exact',
                    style = {'fontSize' : '1.5rem'}
                ),
            ],
            vertical = True,
            pills = True,
        ),
    ],
    style = SIDEBAR_STYLE
)

content =   html.Div(id = 'page-count')
layout  =   html.Div(
    [
        dcc.Location(id = 'url'),
        sidebar,
        content
    ]
)

@app.callback(Output('page-count', 'children'), [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/':
        return html.Div(
            [
                html.P(),
                html.H1(
                    'Database Metrics', 
                    style = {'color' : '#6699CC', 'fontSize' : '3rem'}
                ),
                html.P(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Row(
                                [
                                    dcc.Markdown(f'''
                                        ###        Number of Tracks:
                                        ###       Number of Artists:
                                        ### Max Tracks to an Artist:
                                        ### Min Tracks to an Artist:
                                    ''', style = {'textAlign' : 'right'})
                                ]
                            )
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dcc.Markdown(f'''
                                        ### **{db_metrics.trk_count}**
                                        ### **{db_metrics.art_count}**
                                        ### **{db_metrics.max_trk}**
                                        ### **{db_metrics.min_trk}**
                                    ''', style = {'color' : '#6699CC'})
                                ]
                            )
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dcc.Markdown(f''' 
                                        ###         Number of Users:
                                        ###     Number of Playlists:
                                        ### Max Playlists to a User:
                                        ### Min Playlists to a User:
                                    ''', style = {'textAlign' : 'right'})
                                ]
                            )
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dcc.Markdown(f'''
                                        ### **{db_metrics.usr_count}**
                                        ### **{db_metrics.pl_count}**
                                        ### **{db_metrics.max_pl}**
                                        ### **{db_metrics.min_pl}**
                                    ''', style = {'color' : '#6699CC'})
                                ]
                            )
                        )
                    ]
                ),
                html.P(),
                dcc.Graph(id = 'pl-size', figure = pl_sizes.pl_sizes)
            ]
        )
    elif pathname   == '/ml_models':
        return html.Div(
            [
                html.P(),
                html.H1(
                    'Machine Learning Models', 
                    style = {'color' : '#6699CC', 'fontSize' : '3rem'}
                ),
                html.P(),
                dcc.Markdown('''
                    ### The Content Recommender Model
                    The content recommender model uses cosine similarity to recommend songs
                    that are most similar to a user's selected playlist. This machine learning
                    algorithm works by first converting each song into a vector with 823 
                    dimensions/features. The features include the song's genre, attributes, 
                    popularity, and Release Year. When a user selects a playlist, a vector is 
                    built based on the sum of the song features to create an eigenvector for 
                    the playlist. This eigenvector and all of the song vectors are normalized 
                    by dividing by their Euclidean magnitudes. Afterwards, a dot product between 
                    the normalized playlist and each song's unit vector is performed to calculate 
                    the cosine similarity. These values range from 0 (no similarity) to 1 (perfectly 
                    similar) and are sorted in descending order. The top 10 songs are selected as 
                    the recommendations.
                ''', style = {'fontSize' : 20}),
                html.P(),
                dcc.Markdown('''
                    ### The Collaborative Recommender Model
                    The collaborative recommender model uses cosine distances of a searched song to 
                    recommend songs that appear most often on other users' playlists that also include 
                    the searched song. For readability to the end user, the cosine of 1 to -1  is 
                    converted to pairwise distance of 0 to 1. 0 being the song most similar to the 
                    searched song, and 1 being the most dissimilar. 
                    This machine learning algorithm works by first joining datasets to have each row 
                    represent a song and a playlist on which it is included. A song can be 
                    listed more than once if it is on more than one playlist. We want to know 
                    on which playlist a song is listed, so we create a pivot table with the index being 
                    the song and the columns being playlists. This creates a huge dataframe where if 
                    a specific song is on a specific playlist, it will return a 1. Everything else is 0.  
                    To make the data more manageable, the pivot table is converted into a sparse matrix. 
                    Sparse matrices only show values that exist; in this case, the 1s. From here, we can 
                    calculate the cosine distance. This returns a distance matrix, comparing every song 
                    with every other song in the dataset.
                    The distance matrix is an array that starts with a 0, meaning that a specific song is 
                    similar to itself. There is a diagonal line of the songs being similar to themselves 
                    across the array. From there, we convert the array into a dataframe. A user enters a 
                    search for a song, that search term is used to find a matching song/artist. The returned 
                    songs are sorted in ascending order, meaning that the most similar songs come first. 
                    This model only works if users have a song saved to their playlist. If new songs get 
                    added to a music streaming platform, it will not be on any playlists, thus will not 
                    get recommended. As users add it to their playlists, a correlation will develop and we 
                    will be able to see what other songs people like that song listen to. 
                ''', style = {'fontSize' : 20})
            ]
        )