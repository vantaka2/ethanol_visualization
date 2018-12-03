import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd


df = pd.read_csv('ethanol_export.csv')
df_4 = df
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
x= df_4.quarter.unique()
x.sort()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Ethanol Exports'),
    

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        style={'height': '700px'},

    ),
    html.Div([
    dcc.Slider(
        id='date_picker',
        min=1,
        max=len(x)-1,
        marks = {i: '{}'.format(x[i]) for i in range(0,len(x),2) },
        value=1,
)],className='ten columns'),
html.Button('Previous Quarter', id='previous_button',n_clicks_timestamp='0',),
html.Button('Next Quarter', id='next_button',n_clicks_timestamp='0',),
])

@app.callback(
    Output("example-graph", "figure"), 
    [Input("date_picker", "value"),
    ]
)
def make_graph(date):
    quarter = x[date]
    df_temp = df_4[df_4['quarter']==quarter]
    figure={
            'data' : [ dict(
                type = 'scattergeo',
                locationmode='USA-states',#'country names',
                #locations = df_4['alpha_3_code'],
                lon = df_temp['longitude_average'],
                lat = df_temp['latitude_average'],
                #z = df_4['Thousand Barrels'],
                text = df_temp['text'],

                marker = dict(
                    size = df_temp['Thousand Barrels'] / 16.66,
                    opacity = 0.8,
                    reversescale = True,
                    autocolorscale = False,
                    #symbol = 'square',
                    line = dict(
                        width=1,
                        color='rgba(102, 102, 102)'
                    ),
            ))], 
            'layout': dict(margin={'l':25,'r':25,'b':23,'t':10,'pad':4},
        
        geo = dict(
            scope='world',
            projection=dict( type='natural earth' ),
            showcountries= True,
            landcolor = '#A2F22f',
        ),
             )
        }
    return figure


@app.callback(
    dash.dependencies.Output('date_picker', 'value'),
    [dash.dependencies.Input('next_button', 'n_clicks_timestamp'),
     dash.dependencies.Input('previous_button','n_clicks_timestamp')],
    [dash.dependencies.State('date_picker', 'value')])
def update_output(next,previous, value):
    if int(next) >= int(previous):
        return value + 1
    elif int(previous) > int(next):
        return value - 1

# @app.callback(
#     dash.dependencies.Output('date_picker', 'value'),
#     [dash.dependencies.Input('previous_button', 'n_clicks')],
#     [dash.dependencies.State('date_picker', 'value')])
# def update_output(n_clicks, value):
#     value -= 1
#     return value


if __name__ == '__main__':
    app.run_server(debug=True)


