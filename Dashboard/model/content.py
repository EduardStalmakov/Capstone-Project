from turtle import Turtle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import pymssql
from sklearn.metrics.pairwise import cosine_similarity
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


# Get the database Tables

database = 'landodatalakes-group4'
Track_table = 'dbo.Track'
Artist_table = 'dbo.Artist'
PlaylistTrack_table = 'dbo.PlaylistTrack'
Playlist_table = 'dbo.Playlist'
Users_table = 'dbo.LastFmUsers'
Census_table = 'dbo.Census' 

user = 'spotify'
password  = 'T35TPA55W0RD!'
server = 'gen10-data-fundamentals-22-07-sql-server.database.windows.net'

conn = pymssql.connect(server,user,password,database)
cursor = conn.cursor()



Census = pd.read_sql(f'SELECT * FROM {Census_table}' ,conn)
#Select the tracks table and join with the artists table to get genres
Tracks = pd.read_sql(f'SELECT Track.TrackID, TrackName, Artist.ArtistName,Popularity,DurationMS, ReleaseYear,\
    Danceability,Energy,MusicalKey,Loudness,Mode, Speechiness,Acousticness,\
        Instrumentalness, Liveness, Valence,Tempo,TimeSignature,Genres FROM {Track_table}\
             INNER JOIN {Artist_table} ON Artist.ArtistID = Track.ArtistID', conn)

# Select all from PlaylistTrack table
Playlist_Tracks = pd.read_sql(f'SELECT * FROM {PlaylistTrack_table}' ,conn)

# Get all of the playlists
Playlist = pd.read_sql(f'SELECT * FROM {Playlist_table}' ,conn)

# Get all of the users
Users = pd.read_sql(f'SELECT * FROM {Users_table}' ,conn)
# Functions to run ml model

#Function to scale down popularity by the number of groups you'd like (popularity ranges from 0-100)
def scale_popularity(df,number_of_buckets):
    df['Popularity-Grouped'] = df['Popularity'].apply(lambda x: int(x/number_of_buckets))

    return df

#Function to create dummies for columns that we want to represent as categorical

def get_dummies_for_column(df, current_column_name, new_name):   
    
    tf_df = pd.get_dummies(df[current_column_name])
    feature_names = tf_df.columns
    tf_df.columns = [new_name + "|" + str(i) for i in feature_names]
    tf_df.reset_index(drop = True, inplace = True)    
    return tf_df

#Function to build the entire feature set for all of the tracks

def create_feature_set(df):

    # Convert the dataframe into a pivot table with only track id and genres
    df_1 = df[['TrackID','Genres']]
    df_1['Values'] = 2
    pivot = df_1.pivot_table(index='TrackID', #these are the rows
                                columns='Genres', #these are the columns
                                values='Values') #bianary if the Genre is a characteristic of that song (0 = no, 1 = yes)
    pivot.fillna(0, inplace=True)
    genre_df = pd.DataFrame(pivot)

    #For each column rename it to genre|genre-name

    genre_df.columns = ['genre' + "|" + i for i in genre_df.columns]
    genre_df.reset_index(drop = True, inplace=True)

    #scale float columns using the minmaxscalar
    float_cols = df.dtypes[(df.dtypes == 'float64')].index.values
    floats = df[float_cols].reset_index(drop = True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(floats), columns = floats.columns) 
    
    # Scale down features because they are not as relevant to recommending a song as other features
    df = scale_popularity(df, 5)

    ReleaseYear_ohe = get_dummies_for_column(df, 'ReleaseYear','ReleaseYear') * 0.5 #Scale to 0.5
    TimeSignature_ohe = get_dummies_for_column(df, 'TimeSignature','TimeSignature') * 0.3 #Scale to 1/3 of its value
    Mode_ohe = get_dummies_for_column(df, 'Mode','Mode') * 0.3 #Scale to 1/3 of its value
    MusicalKey_ohe = get_dummies_for_column(df, 'MusicalKey','MusicalKey') * 0.3 #Scale to 1/3 of its value
    Popularity_ohe = get_dummies_for_column(df, 'Popularity-Grouped', 'Popularity-Grouped') * 0.5 #Scale to 0.5

    #concanenate all features
    final = pd.concat([genre_df, floats_scaled,ReleaseYear_ohe,TimeSignature_ohe, Mode_ohe,MusicalKey_ohe, Popularity_ohe], axis = 1)
     
    #Add the TrackID and fill in any na values with zeros
    final['TrackID']=df['TrackID'].values
    final.fillna(0, inplace=True)
    
    return final


#Function to create an eigenvector for the playlist and also get the vectors for all tracks not on the playlist

def generate_playlist_feature(complete_feature_set, playlist_df):

    
    #Get the track features for the songs that are on the playlist
    complete_feature_set_playlist = complete_feature_set[complete_feature_set['TrackID'].isin(playlist_df['TrackID'].values)]
    complete_feature_set_playlist = complete_feature_set_playlist.merge(playlist_df[['TrackID']], how = 'inner', left_on = 'TrackID', right_on='TrackID')

    #Get the track features that are not on someone's playlist
    complete_feature_set_nonplaylist = complete_feature_set[~complete_feature_set['TrackID'].isin(playlist_df['TrackID'].values)]

    #Drop TrackID 
    complete_feature_set_playlist.drop(columns=['TrackID'],inplace=True)

    #Sum the feature playlist features, since it's technically an eigenvector
    return complete_feature_set_playlist.sum(axis = 0), complete_feature_set_nonplaylist

#Function that uses cosine similarity to generate recommendations

def generate_playlist_recommendations(df, features, nonplaylist_features):

    non_playlist_df = df[df['TrackID'].isin(nonplaylist_features['TrackID'].values)]
    non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('TrackID', axis = 1).values, features.values.reshape(1, -1))[:,0]
    non_playlist_df_top_10 = non_playlist_df.sort_values('sim',ascending = False).head(10)
    return non_playlist_df_top_10


#Function to display recommendations
def display_recommendations(playlist_number):
    playlist_selection= Playlist_Tracks[Playlist_Tracks['PlaylistID']==playlist_number]
    complete_feature_set = create_feature_set(Tracks)
    complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_playlist_feature(complete_feature_set, playlist_selection)
    top_10_recoomendations= generate_playlist_recommendations(Tracks, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)
    return top_10_recoomendations


#Running ML Model Based On selection