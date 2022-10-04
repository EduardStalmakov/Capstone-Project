from dash.dependencies import Input, Output
from dash import html, dcc 
from app import app
from model import content
import plotly.express as px

df2 = content.Census.copy()
df2 = df2[df2['StreamMusic'].str.contains('Yes')]
IS = df2['InternetHome'].value_counts()/len(df2) * 100
AS = df2['Age'].value_counts().sort_index(ascending=True)
HS = df2['HouseholdIncome12months'].value_counts().sort_values(ascending=False).head(10)/len(df2) * 100
SS = df2['State'].value_counts()
SxS = df2['Sex'].value_counts()/len(df2) * 100
RS = df2['Race'].value_counts()/len(df2) * 100
ES = df2['EmploymentStatus'].value_counts()/len(df2) * 100

layout = html.Div(children=[
    dcc.Markdown("""
    ### Target Market

    We created the following visualizations using the US Census Bureau's data on households that stream music from 2019.
    Demographics are based upon the individual in each household that responded to the survey. Our target market was identified by looking
    into each demographic category and searching for the groups with the highest number of respondents. We identified individuals from the ages 23-30,
    households in the middle to upper-middle class, and states with high populations as potential demographics that make up our target market. Individuals who are white, employed, and 
    have access to internet make up a large portion of our target market as well. Finally, males and females were almost equally represented across the streaming market.
    Since they are so similar, sex would not be an important factor in our target market. 
    
    """),
    html.Div([
    dcc.Graph(id='age-streaming', figure= px.line(x=AS.index, y=AS.values, title='Music Streaming by Age',
                labels={'x':'Age','y':'People who Stream Music'}),
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White','width':'100%' }),
    dcc.Graph(id='income-streaming', figure = px.bar(x=HS.values, y=HS.index, orientation='h', title='Music Streaming by Household Income', 
                labels={'y':'Income Last 12 Months','x':'Percentage of Streaming Market'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White','width':'100%' }),
       
                
    ],style={'display':'inline-flex','width': '100%'}),
    
    
    html.Div([
    dcc.Graph(id='state-streaming', figure = px.choropleth(SS, locations=SS.index, locationmode = 'USA-states',
        scope = 'usa', color = SS.values, range_color = [40,400],color_continuous_scale = 'tempo', title = 'Household Music Streaming by State'),style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White','width':'100%' }),
    
        html.Div([
    dcc.Graph(id = 'sex-streaming', figure= px.bar(x=SxS.index, y=SxS.values, title='Music Streaming by Sex', 
                labels={'x':'Sex','y':'Percentage of Streaming Market'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White','width':'100%' }),

    dcc.Graph(id='race-streaming', figure= px.bar(y=RS.index, x=RS.values, title='Music Streaming by Race', orientation = 'h',
                labels={'y':'Race','x':'Percentage of Streaming Market'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White','width':'100%' }),
            ],style={'display':'inline-flex','width': '100%'}),

    html.Div([
    dcc.Graph(id = 'internet-streaming', figure= px.bar(x=IS.index, y=IS.values, title='Music Streaming by Home Internet Connection', 
                labels={'x':'Internet at Home','y':'Percentage of Streaming Market'}), 
                style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White','width':'100%' }),
    dcc.Graph(id='employment-streaming', figure = px.bar(y=ES.values, x=ES.index, title='Music Streaming by Employment Status',
                 labels={'x':'Employment Status','y':'Percentage of Streaming Market'}), 
                 style={'padding':'0.8rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 2px 2px 1px', 
                'border-radius': '10px', 'backgroundColor': 'White','width':'100%' }),
            ],style={'display':'inline-flex','width': '100%'}),
    ])
])