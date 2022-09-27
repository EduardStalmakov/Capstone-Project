use [landodatalakes-group4];
go
drop table if exists dbo.Census;
go 

create table Census(
    
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
