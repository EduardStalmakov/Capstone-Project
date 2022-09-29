import pandas as pd
import numpy as np
import sys #for sparse matrix
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances, cosine_distances, cosine_similarity
import pymssql
#pairwise is the metric we are going to use in our recommender instead of cosine similarity 
#will convert cosine of 1 - -1 to pairwise distance of 0 - 1
# pairwise distance 0 is the best, the most similar. 
# .5 pairwise distance is the same as cosine 0

import warnings
warnings.simplefilter(action='ignore', category=UserWarning) 
 # Ignore the warning message when using pd.read_sql

database = 'landodatalakes-group4'
table1 = 'dbo.PlaylistTrack'
table2 = 'dbo.Track'
table3 = 'dbo.Artist'
user = 'spotify'
password  = 'T35TPA55W0RD!'
server = 'gen10-data-fundamentals-22-07-sql-server.database.windows.net'

def GetData(table):
    try:
        conn = pymssql.connect(server,user,password,database)

        query = f'SELECT * FROM {table}'

        df = pd.read_sql(query, conn)
      
        df.dropna(inplace=True)

        return df
        print(df)

    except Exception as e:
        raise e

Playlists = GetData(table1)
Tracks = GetData(table2)
Tracks.drop(columns=['Popularity','DurationMS','ReleaseYear','Danceability','Energy','Liveness','MusicalKey','Loudness','Mode','Speechiness','Acousticness','Instrumentalness','Valence','Tempo','TimeSignature'], inplace = True)
Artists = GetData(table3)
Artists.drop(columns=['Followers', 'Genres','ArtistPopularity'], inplace = True)

#merge the artists with their tracks
TracksArtists = pd.merge(Tracks, Artists, how="right", on="ArtistID")
TracksArtists["Song_Artist"] = TracksArtists["TrackName"] +" (" + TracksArtists["ArtistName"]+ ")"
TracksArtists.drop(columns=['TrackName', 'ArtistID', 'ArtistName'], inplace = True)
#print(TracksArtists)

#merge the tracks to their playlists
PlaylistTracks = pd.merge(TracksArtists, Playlists, how="left", on="TrackID")
#print(PlaylistTracks)

#If a song is in a playlist, it will be represented by a 1. If not in a playlist, will be Nan
PlaylistTracks['values']=1

#create a pivot table
pivot = PlaylistTracks.pivot_table(index="Song_Artist", #these are the rows
                                columns='PlaylistID', #these are the columns
                                values='values') #bianary if the song is in the playlist or not
#print(pivot)

#sparse matrix only works with 0 as a non value, not Nan
pivot_sparse = sparse.csr_matrix(pivot.fillna(0))

# sparse matrix only shows values that exist 
#doesnt change the data, just represents it in a different way

#print(pivot_sparse)
#says song 0 (the first song) is only on one playlist, #479. Represented by (0, 479)

# Calculate Cosine Similarity
# sklearn has a built-in pairwise_distances function
# that we can use for out recommender. It will return square metric, 
# comparing every song with every other song in the dataset
recommender = cosine_distances(pivot_sparse)

#Create Distances DataFrame
#first turn the numpy array (recommender) into a dataframe
recommender_df = pd.DataFrame(recommender, columns=pivot.index, index=pivot.index)
#print(recommender_df.head())

def finder():
    while True:
        choice = input('\nSearch: ')
        results=[]
        songfinder = PlaylistTracks[PlaylistTracks['Song_Artist'].str.contains(choice)]['Song_Artist']
        print(f'Since you like "{songfinder.iloc[0]}" up next is:' )
        results.append(recommender_df[songfinder.iloc[0]].sort_values()[1:11])
        print(f'Up next: {recommender_df[songfinder.iloc[0]].sort_values()[1:11]}')

        #make the results into a dataframe
        x = pd.DataFrame(results)

        #pivot so rows are song titles
        p = pd.DataFrame(x.columns)
        #x = p[~p['Song_Artist'].str.contains(choice)]
        print(p)


finder()