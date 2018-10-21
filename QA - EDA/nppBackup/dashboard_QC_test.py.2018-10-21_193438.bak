
# import packages
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

#=================================================
# Pick Dashboard CSS Style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#=================================================
# Select working Directory - get data
os.chdir("../Data")

# Read in Dataset to do QC on 
catalogue_name = "sc_hot_and_top.csv"

current_catalogue = pd.read_csv(catalogue_name, index_col = 0)

#=================================================

# Unique observations of each column to display
genre_per_run = pd.DataFrame(current_catalogue\
                             .groupby(['runID'])\
                             .genre\
                             .nunique())

countries_per_run = pd.DataFrame(current_catalogue\
                                 .groupby(['runID'])\
                                 .country\
                                 .nunique())

artists_per_run = pd.DataFrame(current_catalogue\
                               .groupby(['runID'])\
                               .artist_name\
                               .nunique())

songs_per_run = pd.DataFrame(current_catalogue\
                             .groupby(['runID'])\
                             .song_name\
                             .nunique())

#=================================================
# Generate Dashboard


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
        style={'width': '100%', 
              'display': 'inline-block'},
        
        children=[
        html.H1(children='Catalogue QC Dashboard',
                style={'textAlign': 'center'}),
        
        html.Div(
        children='''
                 Dashboard to monitor data quality of scraped artist catalogue         
        ''',
        style={'textAlign': 'center'}),
        
        html.Div([
            dcc.Graph(
                id = 'genre_per_run',
                figure = {
                    'data':[
                        {'x': genre_per_run.index.values,
                         'y': genre_per_run['genre'].values,
                         'type': 'line',
                         'name': 'Genre Per Run'},
                         {'x': countries_per_run.index.values,
                         'y': countries_per_run['country'].values,
                         'type': 'line',
                         'name': 'Countries Per Run'},
                        ],
                    'layout': go.Layout(
                            legend=dict(orientation="h",
                                        xanchor="center",
                                        y= 1.2,
                                        x= 0.5),
                            xaxis = {'title':'Run Number'},
                            title = 'Parameter Check')
                    })
        ], style={'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
                id= 'artists_songs',
                figure = {
                    'data':[
                        {'x': artists_per_run.index.values,
                         'y': artists_per_run['artist_name'].values,
                         'type': 'line',
                         'name': 'Artists Per Run'},
                         {'x': songs_per_run.index.values,
                         'y': songs_per_run['song_name'].values,
                         'type': 'line',
                         'name': 'Songs Per Run'},
                        ],
                    'layout': go.Layout(
                            legend=dict(orientation="h",
                                        xanchor="center",
                                        y= 1.2,
                                        x= 0.5),
                            xaxis = {'title':'Run Number'},
                            title = 'Volume Check')
                    })
        ],style={'display': 'inline-block'})
    
])



if __name__ == '__main__':
    app.run_server(debug=True)




