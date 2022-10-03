from dash.dependencies import Input, Output
from dash import html, dcc 
from app import app

layout = [dcc.Markdown("""
#### Talk about stuff from census

race, income, gender, location, age

#### Talk abou tthe data that is not in the census
Emotional ties to music streaming. Self identity, etc.



|           | Validation | Test     |
|-----------|------------|----------|
| MAE       | $71,851    | $68,002  |
| R-Squared | 0.9726     | 0.9839   |


""")]
