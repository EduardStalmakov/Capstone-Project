import pandas as pd
import numpy as np
import sys #for sparse matrix
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances, cosine_distances, cosine_similarity
import pymssql
import plotly.express as px
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
        # print(df)

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
# print(TracksArtists)
# 
#merge the tracks to their playlists
PlaylistTracks = pd.merge(TracksArtists, Playlists, how="left", on="TrackID")
# print(PlaylistTracks)

#If a song is in a playlist, it will be represented by a 1. If not in a playlist, will be Nan
PlaylistTracks['values']=1

#create a pivot table
pivot = PlaylistTracks.pivot_table(index="Song_Artist", #these are the rows
                                columns='PlaylistID', #these are the columns
                                values='values') #bianary if the song is in the playlist or not
# print(pivot)

#sparse matrix only works with 0 as a non value, not Nan
pivot_sparse = sparse.csr_matrix(pivot.fillna(0))

# sparse matrix only shows values that exist 
#doesnt change the data, just represents it in a different way

# print(pivot_sparse)
#says song 0 (the first song) is only on one playlist, #479. Represented by (0, 479)

# Calculate Cosine Similarity
# sklearn has a built-in pairwise_distances function
# that we can use for out recommender. It will return square metric, 
# comparing every song with every other song in the dataset
recommender = cosine_distances(pivot_sparse)

#Create Distances DataFrame
#first turn the numpy array (recommender) into a dataframe
recommender_df = pd.DataFrame(recommender, columns=pivot.index, index=pivot.index)
# print(recommender_df.head())





def finder(n_clicks):
# def finder():
#     n_clicks = input('\nSearch: ')
    results=[]
    songfinder = PlaylistTracks[PlaylistTracks['Song_Artist'].str.contains(n_clicks)]['Song_Artist'] #creates a series of all track/artist that include the value entered in search bar
    # print('===this is songfinder')
    # print(songfinder)
    # print('===info about songfinder')
    # songfinder.info()
    #====================good to here
    df = pd.DataFrame(songfinder) #convert series into a dataframe
    # print('===this is df')
    # print(df)
    # print('===info about df')
    # df.info()
    #===============this is the new part
    df.drop( df.index.to_list()[1:] ,axis = 0, inplace=True)
    # print('this is the df with only top line')
    # print(df)
    # print('df info - should be a dataframe')
    # df.info()
    
    theSong=df.squeeze() #get the first result from the dataframe (creating a series of just the first matching song)
    # print('===this is theSong')
    # print(theSong)
    # print('===info about theSong')
    # print(theSong)
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

    # print('this is g')
    # print(g)
    # print('this is g info')
    # g.info()
    return g





def songName(value):
# def songName():
#     value = input('\nSearch: ')
    # print('===this is value')
    # print(value)
    songfinder = PlaylistTracks[PlaylistTracks['Song_Artist'].str.contains(value)]['Song_Artist'] #creates a series of all track/artist that include the value entered in search bar
    # print('===this is songfinder')
    # print(songfinder)
    # print('===info about songfinder')
    # songfinder.info()
    #====================good to here
    df = pd.DataFrame(songfinder) #convert series into a dataframe
    # print('===this is df')
    # print(df)
    # print('===info about df')
    # df.info()
    #===============this is the new part
    df.drop( df.index.to_list()[1:] ,axis = 0, inplace=True)
    # print('this is the df with only top line')
    # print(df)
    # print('df info - should be a dataframe')
    # df.info()
    
    theSong=df.squeeze() #get the first result from the dataframe (creating a series of just the first matching song)
    # print('===this is theSong')
    # print('Length of series:',len(theSong))

    # print('Size of the Series:', theSong.size)

    # print('The shape of series:',theSong.shape)

    # print(theSong)

    # songfinder = PlaylistTracks[PlaylistTracks['Song_Artist'].str.contains(value)]['Song_Artist']
    # song = songfinder.iloc[0]
    return theSong


# finder()
#songName()



#grapher()

    