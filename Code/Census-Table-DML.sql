insert into dbo.Census (
    HouseholdMembers, InternetHome, Sex, Age, Race, HouseholdIncome12months, StreamMusic, [State], EmploymentStatus 
)
select Number_of_household_members,
Does_anyone_use_the_Internet_at_home,
Sex,
Age,
Race,
Household_total_income_last_12_months,
Stream_or_Download_Music,
[State],
Employment_Status
from dbo.CensusPop

select * from dbo.Census

drop table dbo.CensusPop