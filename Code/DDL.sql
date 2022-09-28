USE [landodatalakes-group4];
GO

DROP TABLE IF EXISTS dbo.Census;
GO 

CREATE TABLE Census(
    
    CensusID int primary key identity (1,1),
    HouseholdMembers int,
    InternetHome nvarchar(3),
    Sex nvarchar(6),
    Age int,
    Race nvarchar (50),
    HouseholdIncome12months nvarchar(50),
    StreamMusic nvarchar (3),
    [State] nvarchar (2),
    EmploymentStatus nvarchar (30)


);

GO

DROP TABLE IF EXISTS LastFmUsers;

-- Creating User Table --
CREATE TABLE LastFmUsers (

    UserID      INT             NOT NULL,        
    UserName    VARCHAR(500)    NULL

    
);

GO

-- Creating Playlist Table --
DROP TABLE IF EXISTS Playlist;

CREATE TABLE Playlist (

    PlaylistID      INT              Not NULL, 
    PlaylistTitle   VARCHAR(600)     NULL,
    UserID          INT              NOT NULL,

    

);

GO

DROP TABLE IF EXISTS Track;

CREATE TABLE Track (
    TrackID VARCHAR,
    TrackName VARCHAR,
    Popularity INT,
    DurationMS INT,
    ArtistID VARCHAR,
    ReleaseYear INT,
    Danceability DECIMAL,
    Energy DECIMAL,
    MusicalKey INT,
    Loudness DECIMAL,
    Mode INT,
    Speechiness DECIMAL,
    Acousticness DECIMAL,
    Instrumentalness DECIMAL,
    Liveness DECIMAL,
    Valence DECIMAL,
    Tempo DECIMAL,
    TimeSignature INT
);

GO

DROP TABLE IF EXISTS PlaylistTrack;

CREATE TABLE PlaylistTrack (
    PlaylistID INT,
    TrackID VARCHAR
);

GO

DROP TABLE IF EXISTS RecommendedSongs;

CREATE TABLE RecommendedSong (
    RecommendedSong INT,
    PlaylistID INT,
    TrackID VARCHAR
);

DROP TABLE IF EXISTS Artist;

CREATE TABLE Artist (
    ArtistID VARCHAR,
    Followers INT,
    Genres VARCHAR,
    ArtistName VARCHAR,
    ArtistPopularity INT
);

GO