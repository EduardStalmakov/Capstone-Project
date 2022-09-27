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

