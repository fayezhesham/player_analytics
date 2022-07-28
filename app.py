import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None,
                     plot_bgcolor="rgba(12,25,34, 0)",
                     paper_bgcolor="rgba(12,25,34, 0)",)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    return fig

config = {'displaylogo': False,
         'modeBarButtonsToAdd':['drawline',
                                'drawopenpath',
                                'drawclosedpath',
                                'drawcircle',
                                'drawrect',
                                'eraseshape'
                               ]}

data=pd.read_csv('data_final.csv')
rating=pd.read_csv('rating.csv')

app = dash.Dash(__name__, update_title=None, suppress_callback_exceptions=True, meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'}])
server = app.server
app.title = 'Player analytics'



app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([html.H2('Premier league | Player Analytics', id='titletext')], className='title'),
            dcc.Dropdown(id='dropdown',
                        options=[
                            {'label':x, 'value':x} for x in data.sort_values('full_name')['full_name'].unique()
                        ],
                        multi=False,
                        clearable=False,
                        value='Mohamed Salah'),
            html.Div(id='clubimage'),
            html.Div(id='name'),
            html.Div(id='age'),
        ], className='topsection'),
        html.Div([
            html.Div([
                dcc.Graph(id='rating_graph', figure=blank_fig(), config={'displayModeBar':False}),
            ], id='rating', className='rating'),
            html.Div([
                dcc.Graph(id='goals_graph', figure=blank_fig(), config=config)
            ], id='goals', className='goals'),
            html.Div([
                dcc.Graph(id='homeaway_graph', figure=blank_fig(), config=config)
            ], id='homeaway', className='homeaway'),
            html.Div([
                dcc.Graph(id='radar_graph', figure=blank_fig(), config=config)
            ], id='radar', className='radar'),
            html.Div([
                dcc.Graph(id='tree_graph', figure=blank_fig(), config={'staticPlot':True})
            ], id='tree', className='tree'),
            html.Div(id='grid', className='grid'),
        ],id='bottomsection', className='bottomsection')
    ], className='main')
    
], id='layout')


@app.callback(
    Output('name','children'),
    [Input('dropdown','value')]
)

def update_name(name):
    children=html.P(name, id='playername')
    return children


@app.callback(
    Output('age','children'),
    [Input('dropdown','value')]
)

def update_age(name):
    age= str(list(data['age'][data['full_name'] == name])[0])
    children=[html.P(age, id='agenumber'), html.P('Years', id='years')]
    return children

@app.callback(
    Output('clubimage','children'),
    [Input('dropdown','value')]
)

def update_club(name):
    club= str(list(rating['team'][rating['player'] == name])[0])
    children=[html.Div(html.Img(src=app.get_asset_url(f'{club}.png'), className='clubimage'), className='imagebox')]
    return children


@app.callback(
    Output('goals_graph','figure'),
    [Input('dropdown','value')]
)

def update_goals(name):
    df=rating[rating['player'] == name]
    dff=df.melt(id_vars=['match name', 'match short'], value_vars=['goals', 'shots off target', 'shots on target blocked'])
    dff.columns=['Match', 'match short', 'Shot type', 'Number of shots']
    try:
        fig=px.bar(dff, x='Match', y='Number of shots', color='Shot type', color_discrete_sequence=['#5A9B1A', '#D43830', '#FF8F00'])
        
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=10),
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=-1.3,
                                xanchor="center",
                                x=0.5,
                                title=""
                            ),
                         xaxis = dict(
                                tickmode = 'array',
                                tickvals = list(range(len(dff['match short'].unique()))),
                                ticktext = dff['match short']
                            ),
                         )
        fig.update_xaxes( title='', tickangle=320)
        fig.update_yaxes(title='')
    except ValueError:
        fig=px.bar(dff, x='Match', y='Number of shots', color='Shot type', color_discrete_sequence=['#5A9B1A', '#D43830', '#FF8F00'])
        
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=10),
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=-1.3,
                                xanchor="center",
                                x=0.5,
                                title=""
                            ),
                         xaxis = dict(
                                tickmode = 'array',
                                tickvals = list(range(len(dff['match short'].unique()))),
                                ticktext = dff['match short']
                            ),
                         )
        fig.update_xaxes( title='', tickangle=320)
        fig.update_yaxes(title='')


    return fig




@app.callback(
    Output('rating_graph','figure'),
    [Input('dropdown','value')]
)

def update_rating(name):
    df=rating[rating['player'] == name]
    df['rating'] = df['rating'].round(1)
    df=df.rename(columns={'match name':'Match', 'rating': 'Rating'})
    try:
        fig=px.bar(df, x='Match', y='Rating', color_discrete_sequence=['#5A9B1A'], text='Rating')
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=10),
                          plot_bgcolor="white",
                          paper_bgcolor="white",)
        fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False, title='', visible=False)
        fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False, title='', visible=False)
    except ValueError:
        fig=px.bar(df, x='Match', y='Rating', color_discrete_sequence=['#5A9B1A'], text='Rating')
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=10),
                          plot_bgcolor="white",
                          paper_bgcolor="white",)
        fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False, title='', visible=False)
        fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False, title='', visible=False)

    return fig

@app.callback(
    Output('homeaway_graph','figure'),
    [Input('dropdown','value')]
)

def update_goalshomeaway(name):
    df=data[data['full_name'] == name]
    names=['Goals Home', 'Goals Away']
    values=[int(list(df['goals_home'])[0]),int(list(df['goals_away'])[0])]
    fig=px.pie(df, names=names, values=values, color_discrete_sequence=['#1D5B2C', '#5A9B1A'], title='Goals Home-Away')
    fig.update_layout(margin=dict(t=25, r=20, b=20, l=20), title={'xanchor': 'center', 'x':0.37})
    return fig

@app.callback(
    Output('radar_graph','figure'),
    [Input('dropdown','value')]
)

def update_radar(name):
    df=data[data['full_name'] == name]
    names=['Wins', 'Losses', 'Tackles', 'Offsides', 'Fouls', 'Interceptions']
    values=[int(list(df['Wins'])[0]),
            int(list(df['Losses'])[0]), 
            int(list(df['Tackles'])[0]),
            int(list(df['Offsides'])[0]),
            int(list(df['Fouls'])[0]),
            int(list(df['Interceptions'])[0])]
    fig = px.line_polar(r=values, theta=names, line_close=True, color_discrete_sequence=['#303F1C'])
    fig.update_traces(fill='toself')
    fig.update_layout(margin=dict(l=23, r=23, t=23, b=23))
    return fig



@app.callback(
    Output('tree_graph','figure'),
    [Input('dropdown','value')]
)

def update_tree(name):
    df=data[data['full_name'] == name]
    names=['Wins', 'Losses', 'Tackles', 'Offsides', 'Fouls', 'Interceptions']
    values=[int(list(df['Wins'])[0]),
            int(list(df['Losses'])[0]), 
            int(list(df['Tackles'])[0]),
            int(list(df['Offsides'])[0]),
            int(list(df['Fouls'])[0]),
            int(list(df['Interceptions'])[0])]
    df=pd.DataFrame()
    df['names'] = names
    df['values'] = values
    df['parents'] = ['']*len(df)
    fig = px.treemap(df,
        names = 'names',
        parents = 'parents',
        values='values',
        color_discrete_sequence=['#1D5B2C', '#5A9B1A', 'green'], 
        custom_data=['names', 'values']
    )
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    fig.update_traces(
        hovertemplate=(
            "Count=%{customdata[1]}")),
    return fig


@app.callback(
    Output('grid','children'),
    [Input('dropdown','value')]
)

def update_grid(name):
    df=data[data['full_name'] == name]
    goals=int(list(df['goals'])[0])
    shots=int(list(df['Shots'])[0])
    shots_on_target=int(list(df['Shots On Target'])[0])
    blocked_shots=int(list(df['Blocked Shots'])[0])
    passes='{:,}'.format(int(list(df['Passes'])[0]))
    tackles=int(list(df['Tackles'])[0])
    offsides=int(list(df['Offsides'])[0])
    fouls=int(list(df['Fouls'])[0])
    interceptions=int(list(df['Interceptions'])[0])
    wins=int(list(df['Wins'])[0])
    red_cards=int(list(df['Red Cards'])[0])
    yellow_cards=int(list(df['Yellow Cards'])[0])
    children=[
        html.Div([html.P(goals, className='bignumber'),html.P('Goals', className='smalltext')], className='topleft'),
        html.Div([html.P(shots, className='bignumber'),html.P('Shots', className='smalltext')], className='topmid'),
        html.Div([html.P(shots_on_target, className='bignumber'),html.P('Shots on target', className='smalltext')], className='topright'),
        html.Div([html.P(blocked_shots, className='bignumber'),html.P('Blocked shots', className='smalltext')], className='midleft'),
        html.Div([html.P(passes, className='bignumber'),html.P('Passes', className='smalltext')], className='midmid'),
        html.Div([html.P(tackles, className='bignumber'),html.P('Tackles', className='smalltext')], className='midright'),
        html.Div([html.P(offsides, className='bignumber'),html.P('Offsides', className='smalltext')], className='midleft2'),
        html.Div([html.P(fouls, className='bignumber'),html.P('Fouls', className='smalltext')], className='midmid2'),
        html.Div([html.P(interceptions, className='bignumber'),html.P('Interceptions', className='smalltext')], className='midright2'),
        html.Div([html.P(wins, className='bignumber'),html.P('Wins', className='smalltext')], className='bottomleft'),
        html.Div([html.P(red_cards, className='bignumber'),html.P('Red cards', className='smalltext')], className='bottommid'),
        html.Div([html.P(yellow_cards, className='bignumber'),html.P('Yellow cards', className='smalltext')], className='bottomright'),
    ]
    return children


if __name__ == "__main__":
    app.run_server(debug=False)
