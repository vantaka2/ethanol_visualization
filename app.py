import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table
import plotly.graph_objs as go


df = pd.read_csv('ethanol_export.csv')
df_4 = df
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
x= df_4.quarter.unique()
x.sort()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div([
                html.Div([
                    html.H2("Ethanol - Exports by quarter", 
                    style={'font-family': 'Dosis'},className='six columns'),
                    html.A(html.Img(src="/assets/6c.png",
                            style={
                                'height': '70px',
                                'float': 'right',
                                #'position': 'relative',
                                'bottom': '145px',
                                'left': '5px'
                            },
                    ),href='https://6csolutions.com/',className='six columns')
                ]),
    ],className='row'),


    html.Div([
        html.Div([
            html.Div([
             dcc.Slider(
                id='date_picker',
                min=1,
                max=len(x)-1,
                marks = {i: '{}'.format(x[i]) for i in range(0,len(x),2) },
                value=18,
                ),],style={"marginBottom": "25"},
                className='row'),

            html.Div([
                html.Div([
                    html.Button('Previous Quarter', id='previous_button',n_clicks_timestamp='0',),
                ],className='four columns button_div'),
                html.P(id='quarter',className='four columns title_small'),
                html.Div([
                    html.Button('Next Quarter', id='next_button',n_clicks_timestamp='0',style={'float':'center'}),
                ],className='four columns button_div'),
               
            ],className='row')

        ],className='eight columns'),
        
        
        html.Div([
        'Click on next and previous quarter to view how exports to countries have changed'   
        ],className='four columns'),
    ],className='row',style={"marginBottom": "10"}),
    html.Div([
    html.Div([
        dcc.Graph(
            id='example-graph',
            style={'height': '500px'},

        ),],className='eight columns'),

    html.Div([
        dash_table.DataTable(id='table',
        columns=[
        {"name": 'Country', "id": 'country'},
        {"name":'Thousand Barrels','id':'Thousand Barrels'}]
            ,
        style_header={
            'fontWeigth':'bold'
        },
        style_cell={'textAlign': 'left',
            'fontSize':'1.2em'},
        style_table={
        'maxHeight': '500',
        'overflowY': 'scroll'
    },    
            )
    ], className='four columns'),

        ],style={"marginBottom": "10"},className='row'),

html.Div([
    dcc.Graph(id='line_chart',className='eight columns',style={'height': '300px'}),

    html.Div([
    html.P("""This visulization is created by 6C Solutions, an industrial analytics startup creating advanced analytics applications for operators and engineers. 
        """),
        html.P("""We apply machine learning and artifical intelligence to industrial data to improve preformance and decrease downtime."""),
        
        html.Div([html.A('Sign up',href='https://6csolutions.com/viz_signup/'),
        """ to be the first to know about the next visulization 6c creates"""] ),

        html.P('All data is from https://www.eia.gov/opendata/ ')
    ]
    ,className='four columns ad')
    

],className='row')


],className='ten columns offset-by-one')


@app.callback(
    Output("line_chart", "figure"), 
    [Input("date_picker", "value"),
    ]
)
def line(value):
    df_5 = df_4.groupby('country',as_index=False).sum().sort_values(by='Thousand Barrels',ascending=False)
    country = df_5[df_5['Thousand Barrels']>5000].country   
    df_5 = df_4.sort_values(['date'])
    data = []
    for i in country:
        df_temp = df_4[df_4['country']== i]
        trace = go.Scatter(
            x = df_temp['date'],
            y = df_temp['Thousand Barrels'],
            mode='lines+markers',
            name= i
        )
        data.append(trace)

    figure={
            'data': data,
            
            'layout': {
               'margin':{'r':25,'b':23,'t':30,'pad':4},
               'title':'Exports by country',
               'hovermode':'closest',
                
            'yaxis':{
                'title':'Thousand Barrels',
                'autorange':'True'
            }
                
            }
        }
    return figure


@app.callback(
    Output('quarter','children'),
    [Input('date_picker','value')
    ]
)
def title(date):
    quarter = x[date]
    year = quarter[0:4]
    q = quarter[-2:]

    return year + ' ' + q



@app.callback(
    Output('table','data'),
    [Input('date_picker','value')
    ]
)
def make_table(date):
    quarter = x[date]
    df_temp = df_4[df_4['quarter']==quarter]
    df_temp= df_temp[['country','Thousand Barrels']]
    df_temp.sort_values('Thousand Barrels',inplace=True,ascending=False)
    return df_temp.to_dict('rows')

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
                showlegend = False,
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
            showland = True,
            landcolor = '#D3D3D3',
            showocean =True,
            oceancolor='#E6F3F7'
        ),
        paper_bgcolor='F4F4F8',
        plot_bgcolor='#323130',
             )
        }
    return figure


@app.callback(
    dash.dependencies.Output('date_picker', 'value'),
    [dash.dependencies.Input('next_button', 'n_clicks_timestamp'),
     dash.dependencies.Input('previous_button','n_clicks_timestamp')],
    [dash.dependencies.State('date_picker', 'value')])
def update_output(next,previous, value):
    print(value)
    if int(next) >= int(previous):
        if int(value) >= 34:
            return 34
        else:
            return value + 1
    elif int(previous) > int(next):
        if int(value) <= 0:
            return 0
        else:
            return value - 1


if __name__ == '__main__':
    app.run_server(debug=True)


