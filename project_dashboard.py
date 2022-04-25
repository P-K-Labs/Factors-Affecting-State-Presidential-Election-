# data manipulation/regression
import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
import math

import matplotlib.pyplot as plt
# import plotly.tools
# import base64

# plotly 
import plotly.express as px
import plotly.graph_objects as go

# dashboards
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc #for themes
from datetime import date

#DATA LOADING
df = pd.read_csv('dataset_final.csv')
# df = pd.read_csv('final_dataset.csv')
codes = pd.read_csv('statecodes.csv')
#merge codes (for electoral map EDA)
df = df.merge(codes, left_on='STATE', right_on='State', how='left')

#year range and string version for EDA slider
year_range = range(min(df.YEAR), max(df.YEAR)+1, 4)
str_years = [str(x) for x in year_range]

states = sorted(df.STATE.unique())
opts = []
for s in states:
    opts.append({'label': f'{s}', 'value': f'{s}'})

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Br(),
    html.Div([
        html.H1('ELECTION ',
            style={'color': 'red',
                   'fontSize': '40px',
                   'text-align': 'center',
                   'display':'inline'}),
    html.H1('DATA ',
            style={'color': 'blue',
                   'fontSize': '40px',
                   'text-align': 'center',
                   'display':'inline'}),
    html.H1('INVESTI',
            style={'color': 'red',
                   'fontSize': '40px',
                   'text-align': 'center',
                   'display':'inline'}),
    html.H1('GATION',
            style={'color': 'blue',
                   'fontSize': '40px',
                   'text-align': 'center',
                   'display':'inline'}),
    ], style={'textAlign':'center'}),
    html.Br(),
    html.H4('DSO545 Fall 2021 Final Project',
            style={'text-align': 'center',}),
    html.Br(),
    dbc.Tabs(className='custom-tabs', children=[ #DEFINE ALL THE TABS
        dbc.Tab(children=[ 
            html.Br(),
            html.H5("""
            Abstract: The purpose of this project is to investigate which factors may affect 
            presidential election outcomes on a state-by-state basis. The timeframe for
             this study is from 1984 to 2020. The analysis includes descriptive statistics 
             of the dataset as well as regressions to assist with predictions. 
            """, style={'text-align':'center'}),
            html.Br(),
            html.H5('By: Akshay Bhide, Yang Song, Keegan O\'Neill, Sebastian Cahill, Pratik Khadse, Jinyu Chen',
            style={'text-align': 'center',})
        ], label='Introduction'), 
        dbc.Tab([ 
            html.Br(),
            html.H3('Select a Year', 
                style={'text-align':'center'}
            ),
            html.Div(children=
                [html.Div(style={'width':'15%', 'display': 'inline-block', 'text-align':'center'}), 
                html.Div([
                    dcc.Slider(id='slider',
                        min=min(df.YEAR),
                        max=max(df.YEAR),
                        step=4,
                        value=2020,
                        marks=dict(zip(year_range, str_years))
                    )
                    ],
                    style={'width':'70%', 'display': 'inline-block', 'text-align':'center'}
                ),
                html.Div(style={'width':'15%', 'display': 'inline-block', 'text-align':'center'})], 
            ),
            html.Br(),
            html.H2(id='yeartab_title',
                    style={'text-align': 'center'}),
            html.H3(id='winner_title',
                    style={'text-align': 'center'}),
            html.Br(),
            html.H3('Electoral Map',
                    style={'text-align': 'center'}),
            dcc.Graph(
                id='us-map'#,
                # figure=fig
            ),
            # html.H3('Matplotlib',
            #         style={'text-align': 'center'}),
            html.H3('Election Year Metrics',
                    style={'text-align': 'center'}),
            html.Div([
                html.Div(id='popular_vote',
                    children=[html.H3('test'),
                    html.P('test text')], 
                    style={'width': '50%', 'display': 'inline-block', 'text-align':'center', 'vertical-align': 'top',
                    'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#FFFFFF'}
                ),
                html.Div(id='cand_spending',
                    children = [html.H1('test2')], 
                    style={'width': '50%', 'display': 'inline-block', 'text-align':'center', 'vertical-align': 'top',
                    'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#FFFFFF'}
                )
            ]),
            html.Div([
                html.Div(id='voter_turnout',
                    children = [html.H1('test3')], 
                    style={'width': '50%', 'display': 'inline-block', 'text-align':'center', 'vertical-align': 'top',
                    'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#FFFFFF'}
                ),
                html.Div(id='capitol_hill_stats',
                    children=[html.H1('capitol_hill_stats')], 
                    style={'width': '50%', 'display': 'inline-block', 'text-align':'center', 'vertical-align': 'top',
                    'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#FFFFFF'}
                )
            ]),
            html.Br(),
            html.Div(children=
                [html.Div(style={'width':'20%', 'display': 'inline-block', 'text-align':'center'}), 
                html.Div([
                    dcc.Graph(id='yearchange_lollipop')
                    ],
                    style={'width':'60%', 'display': 'inline-block', 'text-align':'center'}
                ),
                html.Div(style={'width':'20%', 'display': 'inline-block', 'text-align':'center'})], 
            ),
            html.Br(),
            html.Div(id = 'sbsmet_title', style={'text-align':'center'}),
            html.Div(children=
                [html.Div(style={'width':'15%', 'display': 'inline-block', 'text-align':'center'}), 
                html.Div([
                    dash_table.DataTable(
                        id='year_table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        page_size=10
                        # style_table={'width': '70%', 'display': 'inline-block', 'text-align':'center'}
                    )],
                    style={'width':'70%', 'display': 'inline-block', 'text-align':'center'}
                ),
                html.Div(style={'width':'15%', 'display': 'inline-block', 'text-align':'center'})], 
            ),
            html.Br(),
            html.Div(id='yearmetric_title'),
            dcc.Dropdown(
                id='yearmetric_dropdown',
                options=[
                    {'label': 'Median Income', 'value': 'Income'},
                    {'label': 'Voter Turnout Percentage', 'value': 'Turnout'},
                    {'label': 'Voting Population', 'value': 'Pop'},
                    {'label': 'Net Votes (Democrat - Republican)', 'value': 'Votes'},
                    {'label': 'Democrat Votes', 'value': 'D_Votes'},
                    {'label': 'Republican Votes', 'value': 'R_Votes'}
                ],
                value='Income'
            ),
            dcc.Graph(
                id='yearmetric_fig'#,
                # figure=fig
            )
        ], label='Year EDA'), 
        dbc.Tab([ 
            html.Br(),
            html.H3('Select a State', 
                style={'text-align':'center'}
            ),
            dcc.Dropdown(
                id='state_dropdown',
                options=opts,
                value='California'
            ),
            html.Br(),
            html.Div([
                html.Div(
                    children=[
                        html.H4('Vote Counts Year-by-Year', style = {'text-align':'center'}),
                        dcc.Graph(
                            id='statevote_fig'#,
                            # figure=fig
                        )
                    ],
                    style = {'width': '50%', 'display': 'inline-block', 'text-align':'center'}
                ),
                html.Div(
                    children=[
                        html.H4('Country-wide Candidate Spending Year-by-Year', style = {'text-align':'center'}),
                        dcc.Graph(
                            id='statespend_fig'#,
                            # figure=fig
                        )
                    ],
                    style = {'width': '50%', 'display': 'inline-block', 'text-align':'center'}
                )
            ]),
            html.Div(id='ybymet_title', style={'text-align':'center'}),
            html.Div(children=
                [html.Div(style={'width':'15%', 'display': 'inline-block', 'text-align':'center'}), 
                html.Div([
                    dash_table.DataTable(
                        id='state_table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records')
                        # style_table={'width': '70%', 'display': 'inline-block', 'text-align':'center'}
                    )],
                    style={'width':'70%', 'display': 'inline-block', 'text-align':'center'}
                ),
                html.Div(style={'width':'15%', 'display': 'inline-block', 'text-align':'center'})], 
            ),
            html.Br(),
            html.Div(id='statemetric_title'),
            dcc.Dropdown(
                id='statemetric_dropdown',
                options=[
                    {'label': 'Median Income', 'value': 'Income'},
                    {'label': 'Voter Turnout Percentage', 'value': 'Turnout'},
                    {'label': 'Voting Population', 'value': 'Pop'},
                    {'label': 'Net Votes (Democrat - Republican)', 'value': 'Votes'},
                    {'label': 'Democrat Votes', 'value': 'D_Votes'},
                    {'label': 'Republican Votes', 'value': 'R_Votes'}
                ],
                value='Income'
            ),
            dcc.Graph(
                id='statemetric_fig'#,
                # figure=fig
            )
        ], label='State EDA'),
        dbc.Tab([
            html.Br(), 
            html.Div([
                html.H4('Select Dependent Variable:', style={'width': '49%', 'display': 'inline-block', 'text-align':'center'}),
                html.H4('Select Independent Variable(s):', style={'width': '49%', 'display': 'inline-block', 'text-align':'center'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='depvar_dropdown',
                    #POSSIBLE DEPENDENTS: 
                    options=[
                        {'label': 'Net Votes', 'value': 'NETVOTES'},
                        {'label': 'Net Votes Percentage', 'value': 'NET_VOTES_PCT'},
                        {'label': 'ln(Net Votes)', 'value': 'ln_NETVOTES'},
                        {'label': 'ln(Net Votes Percentage)', 'value': 'ln_NET_VOTES_PCT'},
                    ],
                    value='NET_VOTES_PCT'
                )
            ], style={'width': '49%', 'display': 'inline-block', 'text-align':'center'}),
            #value (list of strings | numbers; optional): The currently selected value.
            html.Div([
                dcc.Checklist(id='indepvar_checklist',
                    #POSSIBLE INDEPS: 
                    options=[
                        {'label': 'Median Income', 'value': 'MEDIAN_INCOME'},
                        {'label': 'ln(Median Income)', 'value': 'ln_MEDIAN_INCOME'},
                        {'label': 'Democrat Spending', 'value': 'DEM_SPENDING'},
                        {'label': 'ln(Democrat Spending)', 'value': 'ln_DEM_SPENDING'},
                        {'label': 'Republican Spending', 'value': 'REP_SPENDING'},
                        {'label': 'ln(Republican Spending)', 'value': 'ln_REP_SPENDING'},
                        {'label': 'VEP Percent Turnout', 'value': 'VEP_PCT_TURNOUT'},
                        {'label': 'ln(VEP Percent Turnout)', 'value': 'ln_VEP_PCT_TURNOUT'},
                        {'label': 'Total Eligible Population', 'value': 'TOTAL_ELIGIBLE_POPULATION'},
                        {'label': 'ln(Total Eligible Population)', 'value': 'ln_TOTAL_ELIGIBLE_POPULATION'},
                        {'label': 'Third Party Votes', 'value': 'THIRD_PARTY_VOTES'},
                        # {'label': 'ln(Third Party Votes)', 'value': 'ln_THIRD_PARTY_VOTES'},
                        {'label': 'Incumbent Presidency', 'value': 'INCUMBENT'},
                        {'label': 'House of Representatives Control', 'value': 'HOUSE'},
                        {'label': 'Senate Control', 'value': 'SENATE'}
                    ],
                    value=['MEDIAN_INCOME','INCUMBENT','SENATE', 'THIRD_PARTY_VOTES', 'VEP_PCT_TURNOUT', 'ln_TOTAL_ELIGIBLE_POPULATION']
                )
            ], style={'width': '49%', 'display': 'inline-block', 'text-align':'center', 'vertical-align': 'top'}),
            html.Br(),
            html.Br(),
            html.Div([
                html.H4('', style={'width': '49%', 'display': 'inline-block', 'text-align':'center'}),
                html.H4('Select State Control Option:', style={'width': '49%', 'display': 'inline-block', 'text-align':'center'})
            ]),
            html.Div([
            ], style={'width': '49%', 'display': 'inline-block', 'text-align':'center'}),
            #value (list of strings | numbers; optional): The currently selected value.
            html.Div([
                dcc.Dropdown(id='state_checklist',
                    #POSSIBLE INDEPS: 
                    options=[
                        {'label': 'None', 'value': 'nothing'},
                        {'label': 'All 50 States', 'value': 'allstates'},
                        {'label': 'Subset of Significant States', 'value': 'substates'}
                    ],
                    value='nothing'
                )
            ], style={'width': '49%', 'display': 'inline-block', 'text-align':'center', 'vertical-align': 'top'}),

            html.Br(),
            html.Br(),
            html.Div([
                html.Div(style={'width':'20%', 'display': 'inline-block'}),
                html.Div(id='regoutput', style={'width':'60%', 'display': 'inline-block', 'text-align':'center'}),
                # html.Pre(id='regoutput', children=['                            OLS Regression Results                            \n==============================================================================\nDep. Variable:               NETVOTES   R-squared:                       0.196\nModel:                            OLS   Adj. R-squared:                  0.191\nMethod:                 Least Squares   F-statistic:                     40.29\nDate:                Sat, 11 Dec 2021   Prob (F-statistic):           2.58e-23\nTime:                        12:18:40   Log-Likelihood:                -7274.5\nNo. Observations:                 500   AIC:                         1.456e+04\nDf Residuals:                     496   BIC:                         1.457e+04\nDf Model:                           3                                         \nCovariance Type:            nonrobust                                         \n================================================================================\n                   coef    std err          t      P>|t|      [0.025      0.975]\n--------------------------------------------------------------------------------\nIntercept    -2.477e+05   5.45e+04     -4.549      0.000   -3.55e+05   -1.41e+05\nDEM_SPENDING     0.0003      0.000      1.938      0.053   -4.15e-06       0.001\nREP_SPENDING    -0.0002      0.000     -0.891      0.373      -0.001       0.000\nPOPULATION       0.0375      0.004     10.405      0.000       0.030       0.045\n==============================================================================\nOmnibus:                      131.038   Durbin-Watson:                   1.674\nProb(Omnibus):                  0.000   Jarque-Bera (JB):             2867.611\nSkew:                           0.547   Prob(JB):                         0.00\nKurtosis:                      14.681   Cond. No.                     1.74e+09\n==============================================================================\n\nNotes:\n[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.\n[2] The condition number is large, 1.74e+09. This might indicate that there are\nstrong multicollinearity or other numerical problems.'],
                #     style={'width':'40%', 'display': 'inline-block'}
                #     #style={'white-space': 'pre-wrap'}
                # ),
                # html.Pre(children='Model:                            OLS   Adj. R-squared:                  0.191'#,
                #     # style={'width':'70%', 'display': 'inline-block', 'whiteSpace': 'pre-wrap'}
                #     # style={'white-space': 'pre'}
                # )#,
                html.Div(style={'width':'15%', 'display': 'inline-block'})
            ])
        ], label='Regression')#,
        # dbc.Tab([ 
        #     # html.Ul([
        #     #     html.Br(),
        #     #     html.Li('Book title: Interactive Dashboards and Data Apps with Plotly and Dash'),
        #     #     html.Li(['GitHub repo: ',
        #     #              html.A('https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash',
        #     #                     href='https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash')
        #     #              ])
        #     # ])
        # ], label='Prediction')#,
        # dbc.Tab([ #TAB 2
        #     html.Ul([
        #         html.Br(),
        #         html.Li(['State median incomes: ',
        #                  html.A('https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html',
        #                         href='https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html')
        #                  ]),
        #         html.Li([
        #                  html.A('https://electionlab.mit.edu/data',
        #                         href='https://electionlab.mit.edu/data')
        #                  ]),
        #         html.Li(['Election outcomes by state: ',
        #                  html.A('https://dataverse.harvard.edu/file.xhtml?fileId=4299753&version=6.0',
        #                         href='https://dataverse.harvard.edu/file.xhtml?fileId=4299753&version=6.0')
        #                  ]),
        #         html.Li(['Yearly population for each state before 2020: ',
        #                  html.A('Click historical data series for 1969-2009',
        #                         href='https://www.icip.iastate.edu/tables/population/states-estimates')
        #                  ]),
        #         html.Li(['Yearly population for each state for 2020: ',
        #                  html.A('Only used 2020 from here',
        #                         href='https://www.icip.iastate.edu/tables/population/census-states')
        #                  ]),
        #         html.Li(['US Inflation Rate Calculator: ',
        #                  html.A('https://www.usinflationcalculator.com/',
        #                         href='https://www.usinflationcalculator.com/')
        #                  ]),
        #     ])
        # ], label='Sources')   
    ], style={'textAlign':'center'}),
])

@app.callback(
        [Output('yeartab_title', 'children'),
        Output('winner_title', 'children'),
        Output('us-map', 'figure'),
        Output('yearchange_lollipop', 'figure'),
        Output('popular_vote', 'children'),
        Output('cand_spending', 'children'),
        Output('voter_turnout', 'children'),
        Output('capitol_hill_stats', 'children'),
        Output('year_table', 'columns'),
        Output('year_table', 'data'),
        Output('yearmetric_title', 'children'),
        Output('yearmetric_fig', 'figure'),
        Output('sbsmet_title', 'children')], #specify where to put output (ie put in children of color_output)
        [Input('slider', 'value'),
        Input('yearmetric_dropdown', 'value')]) #specify what the input is
def update_yeartab(year, metric):
    sdf = df[df.YEAR==year]
    dem_wins = [1992, 1996, 2008, 2012, 2020]
    rep_wins = [1984, 1988, 2000, 2004, 2016]
    winning_party = 'Democrat' if year in dem_wins else 'Republican'
    if winning_party == 'Democrat':
        cand = sdf.DEM_CANDIDATE.values[0]
    else:
        cand = sdf.REP_CANDIDATE.values[0]

    m_title = html.H2('EDA for Election Year ' + str(year))
    w_title = html.H4('Election Winner: ' + cand + ', '  + winning_party)
    
    sdf = sdf[['YEAR', 'DEM_CANDIDATE', 'DEM_VOTES', 'REP_CANDIDATE', 'REP_VOTES', 'STATE', 'Code']]
    sdf = sdf.reset_index(drop=True)
    sdf['Winning Candidate'] = [sdf.loc[x,'DEM_CANDIDATE'] if sdf.loc[x,'DEM_VOTES'] > sdf.loc[x,'REP_VOTES'] else sdf.loc[x,'REP_CANDIDATE'] \
                            for x in range(sdf.shape[0])]

    rep_name = sdf.loc[0,'REP_CANDIDATE']
    dem_name = sdf.loc[0,'DEM_CANDIDATE']
    fig = px.choropleth(sdf, locations="Code", locationmode='USA-states', 
                        color="Winning Candidate", color_discrete_sequence=["red", "blue"],
                        category_orders={"Winning Candidate": [rep_name, dem_name]},
                        hover_data=['DEM_VOTES','REP_VOTES'])

    fig.update_layout(
        # title_text=f'Presidential Electoral Map, {sdf.YEAR.unique()[0]}', title_x=0.5,
        geo = dict(
            scope='usa',
            projection_type='albers usa'
        ),
    )

    sdf = df[df.YEAR==year]
    dem_popvote = int(sdf.DEM_VOTES.sum())
    rep_popvote = int(sdf.REP_VOTES.sum())
    poplist = []
    poplist.append(html.H4('Popular Vote'))
    poplist.append(html.P('Democrat: ' + "{:,}".format(dem_popvote)))
    poplist.append(html.P('Republican: ' + "{:,}".format(rep_popvote)))
    
    dem_spending = sdf.DEM_SPENDING.values[0]
    rep_spending = sdf.REP_SPENDING.values[0]
    spendlist = []
    spendlist.append(html.H4('Candidate Spending'))
    spendlist.append(html.P('Democrat: $' + "{:,}".format(dem_spending)))
    spendlist.append(html.P('Republican: $' + "{:,}".format(rep_spending)))

    voter_turnout = round(((dem_popvote + rep_popvote) / sdf.TOTAL_ELIGIBLE_POPULATION.sum()) * 100, 2)
    vt_list = []
    vt_list.append(html.H4('Country-wide Voter Turnout'))
    vt_list.append(html.P('Total Nationwide Votes: ' +  "{:,}".format(dem_popvote + rep_popvote)))
    vt_list.append(html.P('Total Eligible Voting Population: ' + "{:,}".format(int(sdf.TOTAL_ELIGIBLE_POPULATION.sum()))))
    vt_list.append(html.P('Voter Turnout: ' + str(voter_turnout) + '%'))

    inc = 'Democrat' if sdf.INCUMBENT.values[0]==1 else 'Republican'
    house = 'Democrat' if sdf.HOUSE.values[0]==1 else 'Republican'
    senate = 'Democrat' if sdf.SENATE.values[0]==1 else 'Republican'
    cap_list = []
    cap_list.append(html.H4('Capitol Hill before ' + str(year)))
    cap_list.append(html.P('Incumbent President: ' + inc))
    cap_list.append(html.P('House of Representatives Control: ' + house))
    cap_list.append(html.P('Senate Control: ' + senate))

    stateincome_df = sdf[['STATE','MEDIAN_INCOME','TOTAL_ELIGIBLE_POPULATION','NETVOTES','WINNER']]
    stateincome_df = stateincome_df.sort_values(by='STATE')
    # stateincome_df = sdf.groupby(['STATE'])['MEDIAN_INCOME','TOTAL_ELIGIBLE_POPULATION','NETVOTES','WINNER'].median().reset_index().sort_values(by='MEDIAN_INCOME',ascending=False)
    # stateincome_df=stateincome_df.reset_index(drop = 'TRUE')
    stateincome_df['WINNER']=['Democrat' if i ==1 else 'Republican' for i in stateincome_df['WINNER']]
    cols=[{"name": i, "id": i} for i in stateincome_df.columns]
    data=stateincome_df.to_dict('records')

    ymt = html.H4('Select a Metric to Investigate its Distribution over Every \
                State for ' + str(year), style={'text-align':'center'})
    sbsmt = html.H3('State by State Metrics for ' + str(year))

    figc=go.Figure()
    if metric == 'Income':
        figc.add_trace(go.Box(y = sdf['MEDIAN_INCOME'], name='Median Income'))
    elif metric == 'Turnout':
        figc.add_trace(go.Box(y = sdf['VEP_PCT_TURNOUT']*100, name='Voter Turnout Percentage'))
    elif metric == 'Pop':
        figc.add_trace(go.Box(y = sdf['TOTAL_ELIGIBLE_POPULATION'], name='Voting Population'))
    elif metric == 'Votes':
        figc.add_trace(go.Box(y = sdf['NETVOTES'], name='Net Votes (Democrat - Republican)'))
    elif metric == 'D_Votes':
        figc.add_trace(go.Box(y = sdf['DEM_VOTES'], name='Democrat Votes'))
    elif metric == 'R_Votes':
        figc.add_trace(go.Box(y = sdf['REP_VOTES'], name='Republican Votes'))

    figc.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    if year > 1984:
        pdf = df.loc[((df['YEAR'] == year) |(df['YEAR'] == year-4))]    
        # summary = pdf[['STATE', 'YEAR', 'NETVOTES', 'WINNER' ]]
        summary = pdf[['STATE', 'YEAR', 'NET_VOTES_PCT', 'WINNER' ]]
        summaryPiv = summary.pivot(index = 'STATE', columns = 'YEAR')

        my_colors = ['blue' if i == 1 else 'red' for i in summaryPiv[('WINNER', year)]]
        summaryPiv['colors'] = my_colors

        layout = go.Layout(
            plot_bgcolor="#FFF",  # Sets background color to white
            xaxis=dict(
                title="Rep vs. Dem Differential",
                linecolor="#BCCCDC",  # Sets color of X-axis line
                showgrid=False  # Removes X-axis grid lines
            ),
            yaxis=dict(
                title="State",  
                linecolor="#BCCCDC",  # Sets color of Y-axis line
                showgrid=False,  # Removes Y-axis grid lines    
            )
        )        
        
        
        figp = go.Figure(layout = layout)

        figp.add_vline(x=0)
        
        # figp.add_trace(go.Scatter(x = summaryPiv[('NETVOTES', year-4)], 
        #                           y = summaryPiv.index,
        #                           mode = 'markers',
        #                           marker_color = my_colors,
        #                           marker_size = 10,
        #                           marker_symbol = 'square',
        #                           name = str(year-4)))
        
        # figp.add_trace(go.Scatter(x = summaryPiv[('NETVOTES', year)] , 
        #                          y = summaryPiv.index,
        #                           mode = 'markers',
        #                           marker_color = my_colors,
        #                           marker_size = 10,
        #                           name = str(year)))
        
        # figp.update_layout(legend_title_text='     Years')



        # for i in range(0, len(summaryPiv)):
        #     figp.add_shape(type='line',
        #                         x0 = summaryPiv[('NETVOTES', year-4)][i],
        #                         y0 = i,
        #                         x1 = summaryPiv[('NETVOTES', year)][i],
        #                         y1 = i,
        #                         line=dict(color= summaryPiv['colors'][i], width = 3))

        figp.add_trace(go.Scatter(x = summaryPiv[('NET_VOTES_PCT', year-4)], 
                                  y = summaryPiv.index,
                                  mode = 'markers',
                                  marker_color = my_colors,
                                  marker_size = 10,
                                  marker_symbol = 'square',
                                  name = str(year-4)))
        
        figp.add_trace(go.Scatter(x = summaryPiv[('NET_VOTES_PCT', year)] , 
                                 y = summaryPiv.index,
                                  mode = 'markers',
                                  marker_color = my_colors,
                                  marker_size = 10,
                                  name = str(year)))
        
        figp.update_layout(legend_title_text='     Years')



        for i in range(0, len(summaryPiv)):
            figp.add_shape(type='line',
                                x0 = summaryPiv[('NET_VOTES_PCT', year-4)][i],
                                y0 = i,
                                x1 = summaryPiv[('NET_VOTES_PCT', year)][i],
                                y1 = i,
                                line=dict(color= summaryPiv['colors'][i], width = 3))
            
        
        figp.update_layout(title_text ="Consecutive Election Change in Rep vs. Dem Voter Differential <br><sup>Note: A cross over the 0 line indicates the state flipped in the selected election year.</sup>",
                            title_x=0.5,
                            title_font_size = 25,
                            autosize=False,
                            width=1000,
                            height=1200)
        
        figp.update_layout(showlegend=True)
        
        figp.update_xaxes(range=[-1, 1])
    else:
        layout = go.Layout(
        )        
        
        figp = go.Figure(layout = layout)
        figp.update_layout(title_text =
                            "Please Select a Year After 1984 to View this Chart",
                            title_x=0.5,
                            title_font_size = 25,
                            autosize=False,
                            width=1000,
                            height=1200)

    return m_title, w_title, fig, figp, poplist, spendlist, vt_list, cap_list, cols, data, ymt, figc, sbsmt
    # return m_title, w_title, fig, poplist, spendlist, vt_list, cap_list, cols, data, ymt, figc

@app.callback(
        [Output('state_table', 'columns'),
        Output('state_table', 'data'),
        Output('statevote_fig', 'figure'),
        Output('statespend_fig', 'figure'),
        Output('statemetric_title', 'children'),
        Output('statemetric_fig', 'figure'),
        Output('ybymet_title', 'children')], #specify where to put output (ie put in children of color_output)
        [Input('state_dropdown', 'value'),
        Input('statemetric_dropdown', 'value')]) #specify what the input is
def update_statetab(state, metric):
    state_df = df[df['STATE']== state]
    yearincome_df = state_df[['YEAR','MEDIAN_INCOME','TOTAL_ELIGIBLE_POPULATION','NETVOTES','WINNER']]
    yearincome_df = yearincome_df.sort_values(by='YEAR', ascending=False)
    # yearincome_df = state_df.groupby(['YEAR'])['MEDIAN_INCOME','TOTAL_ELIGIBLE_POPULATION','NETVOTES','WINNER'].median().reset_index().sort_values(by='YEAR',ascending=False)
    # yearincome_df=yearincome_df.reset_index(drop = 'TRUE')
    yearincome_df['WINNER']=['Democrat' if i ==1 else 'Republican' for i in yearincome_df['WINNER']]
    cols=[{"name": i, "id": i} for i in yearincome_df.columns]
    data=yearincome_df.to_dict('records')

    sdf=df[df.STATE==state]
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x = sdf['YEAR'], 
                             y = sdf['DEM_VOTES'],
                             mode = 'lines', name='Dem Votes'
                             ))
    fig1.add_trace(go.Scatter(x = sdf['YEAR'], 
                             y = sdf['REP_VOTES'],
                             mode = 'lines', name='Rep Votes'
                             ))
    fig1.add_trace(go.Scatter(x = sdf['YEAR'], 
                             y = sdf['THIRD_PARTY_VOTES'],
                             mode = 'lines', name='Third Party Votes'
                             ))
    fig1.add_trace(go.Scatter(x = sdf['YEAR'], y = sdf['NETVOTES'],
                             mode = 'lines', name='Net Votes (Dem - Rep)'))
    # fig1.add_trace(go.Scatter(x = sdf['YEAR'], y = [0 for y in sdf.YEAR],
    #                          mode = 'lines', color="black"))
    fig1.add_hline(y=0, line_width=2, line_dash="dash", line_color="black")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x = sdf['YEAR'], 
                             y = sdf['DEM_SPENDING'],
                             mode = 'lines', name='Dem Spending'
                             ))
    fig3.add_trace(go.Scatter(x = sdf['YEAR'], 
                             y = sdf['REP_SPENDING'],
                             mode = 'lines', name='Rep Spending'
                             ))
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    smt = html.H4('Select a Metric to Investigate its Distribution over Every \
                Election Year for ' + state, style={'text-align':'center'})
    ybymt = html.H3('Year by Year Metrics for ' + state)

    figb=go.Figure()
    if metric == 'Income':
        figb.add_trace(go.Box(y = sdf['MEDIAN_INCOME'], name='Median Income'))
    elif metric == 'Turnout':
        figb.add_trace(go.Box(y = sdf['VEP_PCT_TURNOUT']*100, name='Voter Turnout Percentage'))
    elif metric == 'Pop':
        figb.add_trace(go.Box(y = sdf['TOTAL_ELIGIBLE_POPULATION'], name='Voting Population'))
    elif metric == 'Votes':
        figb.add_trace(go.Box(y = sdf['NETVOTES'], name='Net Votes (Democrat - Republican)'))
    elif metric == 'D_Votes':
        figb.add_trace(go.Box(y = sdf['DEM_VOTES'], name='Democrat Votes'))
    elif metric == 'R_Votes':
        figb.add_trace(go.Box(y = sdf['REP_VOTES'], name='Republican Votes'))
    figb.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    return cols, data, fig1, fig3, smt, figb, ybymt

@app.callback(
        [Output('regoutput', 'children')], #specify where to put output (ie put in children of color_output)
        [Input('depvar_dropdown', 'value'),
        Input('indepvar_checklist', 'value'),
        Input('state_checklist', 'value')]) #specify what the input is
def update_regressiontab(dep_var, indep_vars, statecheck):

    data=df
    data['ln_NETVOTES']=np.log(data['NETVOTES'])
    data['ln_NET_VOTES_PCT']=np.log(data['NET_VOTES_PCT'])
    data['ln_DEM_VOTES']=np.log(data['DEM_VOTES'])
    data['ln_REP_VOTES']=np.log(data['REP_VOTES'])
    data['ln_MEDIAN_INCOME']=np.log(data['MEDIAN_INCOME'])
    data['ln_POPULATION']=np.log(data['POPULATION'])
    data['ln_DEM_SPENDING']=np.log(data['DEM_SPENDING'])
    data['ln_REP_SPENDING']=np.log(data['REP_SPENDING'])
    data['ln_TOTAL_ELIGIBLE_POPULATION']=np.log(data['TOTAL_ELIGIBLE_POPULATION'])
    data['ln_THIRD_PARTY_VOTES']=np.log(data['THIRD_PARTY_VOTES'])
    data['ln_VEP_PCT_TURNOUT']=np.log(data['VEP_PCT_TURNOUT'])

    df_state = pd.get_dummies(data["STATE"])

    # clean column names: case and spaces
    df_state.columns = df_state.columns.str.upper()
    df_state.columns = df_state.columns.str.strip().str.replace(' ', '_')

    # concat
    data_all = pd.concat([data, df_state], axis = 1)
    data_all.drop(["STATE"], axis = 1, inplace = True)
    data_all.drop(["WYOMING"], axis =1, inplace = True) # for avoiding the dummy variable trap: multicollinearity
    
    statesel = False
    states = ''
    if statecheck=='nothing':
        states = ''
    if statecheck=='allstates':
        states = "+".join(list(df_state.drop(["WYOMING"], axis = 1).columns))
        statesel = True
    elif statecheck=='substates':
        states = "+".join(list(df_state.drop(["WYOMING", "ALASKA", "NEBRASKA", "OHIO", "OKLAHOMA", 'TEXAS', 'UTAH', 'OREGON'], axis = 1).columns))
        statesel = True
    
    Z=indep_vars[0]
    for z in indep_vars[1:]:
        Z=str(Z+'+'+z)

    form = ''
    if statesel:
        form = f"{dep_var} ~ {Z} + " + states
    else:
        form = f"{dep_var} ~ {Z}"
    
    result = sm.ols(formula=form, 
                    data=data_all).fit()
    return [html.Pre(children=[result.summary().as_text()])]
    # return [html.P('RETURNED')]



if __name__ == '__main__':
    app.run_server(debug=True)