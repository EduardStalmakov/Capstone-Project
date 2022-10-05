# References external libraries
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_distances
# References files in this repository
from tabs.supp_files import sql_queries

Playlists = sql_queries.Playlist_Tracks
Tracks = sql_queries.Track
Tracks.drop(columns=['Popularity','DurationMS','ReleaseYear','Danceability','Energy','Liveness','MusicalKey','Loudness','Mode','Speechiness','Acousticness','Instrumentalness','Valence','Tempo','TimeSignature'], inplace = True)
Artists = sql_queries.Artists
Artists.drop(columns=['Followers', 'Genres','ArtistPopularity'], inplace = True)

#merge the artists with their tracks
TracksArtists = pd.merge(Tracks, Artists, how = "right", on = "ArtistID")
TracksArtists["Song_Artist"] = TracksArtists["TrackName"] +" (" + TracksArtists["ArtistName"]+ ")"
TracksArtists.drop(columns=['TrackName', 'ArtistID', 'ArtistName'], inplace = True)
# print(TracksArtists)
# 
#merge the tracks to their playlists
PlaylistTracks = pd.merge(TracksArtists, Playlists, how = "left", on = "TrackID")
# print(PlaylistTracks)

#If a song is in a playlist, it will be represented by a 1. If not in a playlist, will be Nan
PlaylistTracks['values'] = 1

#create a pivot table
pivot = PlaylistTracks.pivot_table(index="Song_Artist", #these are the rows
                                columns='PlaylistID', #these are the columns
                                values='values') #bianary if the song is in the playlist or not
# print(pivot)

#sparse matrix only works with 0 as a non value, not Nan
pivot_sparse = sparse.csr_matrix(pivot.fillna(0))

# sparse matrix only shows values that exist 
# doesnt change the data, just represents it in a different way

# print(pivot_sparse)
# says song 0 (the first song) is only on one playlist, #479. Represented by (0, 479)

# Calculate Cosine Similarity
# sklearn has a built-in pairwise_distances function
# that we can use for out recommender. It will return square metric, 
# comparing every song with every other song in the dataset
recommender = cosine_distances(pivot_sparse)

# Create Distances DataFrame
# first turn the numpy array (recommender) into a dataframe
recommender_df = pd.DataFrame(recommender, columns=pivot.index, index=pivot.index)

def finder(n_clicks):
    results=[]
    songfinder = PlaylistTracks[PlaylistTracks['Song_Artist'].str.contains(n_clicks)]['Song_Artist'] #creates a series of all track/artist that include the value entered in search bar
    df = pd.DataFrame(songfinder) #convert series into a dataframe
    df.drop( df.index.to_list()[1:] ,axis = 0, inplace=True)
    
    theSong=df.squeeze() #get the first result from the dataframe (creating a series of just the first matching song)
    results.append(recommender_df[theSong].sort_values()[1:6]) #to get the top 5, not including the search track
    x = pd.DataFrame(results) #make the results into a dataframe

    list = []
    for i in x.columns:
        dict = {}
        dict['Song_Artist'] = i
        dict['Percent_Similar'] = (1-(x[i].values))
        list.append(dict)
    g = pd.DataFrame(list)
    g['Percent_Similar'] = g['Percent_Similar'].apply(lambda x: x[0])
    g.loc[:, "Percent_Similar"] =g["Percent_Similar"].map('{:.0%}'.format)
    return g

def songName(value):
    songfinder = PlaylistTracks[PlaylistTracks['Song_Artist'].str.contains(value)]['Song_Artist'] #creates a series of all track/artist that include the value entered in search bar
    df = pd.DataFrame(songfinder) #convert series into a dataframe
    df.drop( df.index.to_list()[1:] ,axis = 0, inplace=True)
    theSong=df.squeeze() #get the first result from the dataframe (creating a series of just the first matching song)
    return theSong   