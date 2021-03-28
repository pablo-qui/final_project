import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt
import pandas as pd
import plotly.express as px
import json


crabs_url = 'https://raw.githubusercontent.com/pablo-qui/final_project/master/crabs.csv'
air_url='https://raw.githubusercontent.com/pablo-qui/final_project/master/airdata.csv'
air=pd.read_csv(air_url).dropna()
crabs = pd.read_csv(crabs_url).dropna()
crabs.drop('index', inplace=True, axis=1)
navalue1=crabs.isnull().any().sum()
navalue2=air.isnull().any().sum()

crabs_cols = [{"name": i, "id": i} for i in crabs.columns]
crabs_sex = crabs['sex'].sort_values().unique()
opt_sex = [{'label': x, 'value': x} for x in crabs_sex]
crabs_sp = crabs['sp'].sort_values().unique()
opt_sp = [{'label': x , 'value': x} for x in crabs_sp]
variables = crabs.columns[2:7]
opt_var = [{'label': x , 'value': x} for x in variables]


air_cols = [{"name": i, "id": i} for i in air.columns]
air_Month =air['Month'].sort_values().unique()
opt_Month = [{'label': x, 'value': x} for x in air_Month]
variable_air = air.columns[0:4]
opt_var_air = [{'label': x , 'value': x} for x in variable_air]
air_Day = air['Day'].sort_values().unique()
opt_Dayay=[{'label': x, 'value': x} for x in air_Day]


#col_vore = {x:px.colors.qualitative.Pastel[i] for i, x in enumerate(df_vore)}


app = dash.Dash(__name__, title="Final Project Dash App")

markdown_text = '''
## Some references
- [Dash HTML Components](dash.plotly.com/dash-html-components)
- [Dash Core Components](dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](dash-bootstrap-components.opensource.faculty.ai/docs/components) 
- [Dash DataTable](https://dash.plotly.com/datatable)  
-[Introduction](https://raw.githubusercontent.com/pablo-qui/final_project/master/introduction.txt)
'''

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
table1_tab = html.Div([
       html.Label(["Select sex of the crab:",
            dcc.Dropdown('dd-sex',
                options= opt_sex,
                value= [crabs_sex[0]],
                multi= True
            )
        ]),
        html.Label(["Select species of the crab:",
            dcc.Dropdown('dd-sp',
                options= opt_sp,
                value= [crabs_sp[0]],
                multi= True
            )
        ]),
    dt.DataTable(id="my-table",
                columns = crabs_cols,
                data = crabs.to_dict("records"),
                style_as_list_view=True,
                style_cell={'padding': '5px'},
                style_data={ 'border': '1px solid blue' },
    style_header={ 'border': '1px solid pink' },     
            )
])

graph1_tab = html.Div([
    html.Label(["Select variable for the X axis:",
            dcc.Dropdown('dd-x',
                options= opt_var,
                value= variables[0],
                multi= False
            )
        ]),
    html.Label(["Select variable for the Y axis:",
            dcc.Dropdown('dd-y',
                options= opt_var,
                value= variables[1],
                multi= False
            )
        ]),
    html.Label(['Color by sex or species',
        dcc.RadioItems(id='color',
            options=[
                {'label': 'Sex', 'value': 'sex'},
                {'label': 'Species', 'value': 'sp'}
                ],
            value='sex'
            )
        ]),
    dcc.Graph(id="sca_crabs",
        figure= px.scatter(crabs,
            x="FL",
            y="RW",
            color="sex")            
    ),
    dt.DataTable(id="selected_crabs",
        columns = crabs_cols,
        style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white' },
        style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold',
        'color': 'rgb(50, 50, 50)'
    }
    )
])



table2_tab = html.Div([
      html.Label(["Select the month of air :",
            dcc.Dropdown('dd-month',
                options= opt_Month,
                value= [air_Month[0]],
                multi= True
            )
        ]),
        html.Label(["input the day of the this month:",
            dcc.input(id='day'
            )
        ]),
    dt.DataTable(id="my-table_air",
                columns = air_cols,
                data = air.to_dict("records"),
                style_as_list_view=True,
                style_cell={'padding': '5px'},
                style_data={ 'border': '1px solid blue' },
    style_header={ 'border': '1px solid pink' },     
            )
])

graph2_tab = html.Div([
    html.Label(["Select variable for the X axis:",
            dcc.Dropdown('dd-x_air',
                options= opt_var_air,
                value= variable_air[0],
                multi= False
            )
        ]),
    html.Label(["Select variable for the Y axis:",
            dcc.Dropdown('dd-y_air',
                options= opt_var_air,
                value= variable_air[1],
                multi= False
            )
        ]),
    html.Label(['Color by Month',
        dcc.Dropdown('color_air',
                     options=opt_Month,
                     value=air_Month[0],
                multi= False
                )
        ]),
    dcc.Graph(id="sca_air",
        figure= px.scatter(air,
            x="Ozone",
            y="Wind",
            color="Month")            
    ),
    dt.DataTable(id="selected_air",
        columns = air_cols,
        style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white' },
        style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold',
        'color': 'rgb(50, 50, 50)'
    }
    )
])

app.layout = html.Div([
    html.Div([
        html.H1(app.title, className= "app-header--title")
    ], className= "app-header"),

     dcc.Markdown(markdown_text),
     html.Div(id="data_crabs",style={'display':'none'}),
     dcc.Tabs(id="tabs", value='tab-t', children=[
            dcc.Tab(label='Table 1', value='tab-t',style={"width":"100%","text-align":"center","padding-top":"5%"}),
            dcc.Tab(label='Graph 1', value='tab-g',style={"width":"100%","text-align":"center","padding-top":"5%"}),
            dcc.Tab(label='Table 2', value='tab-t2',style={"width":"100%","text-align":"center","padding-top":"5%"}),
            dcc.Tab(label='Graph 2', value='tab-g2',style={"width":"100%","text-align":"center","padding-top":"5%"})
        ]),
        html.Div(id="tabs-content")
        
],className = 'app-body')


@app.callback(
     Output('tabs-content', 'children'),
     Input('tabs', 'value'))
def update_tabs(v):
    if v == 'tab-g':
        return graph1_tab
    elif v == 'tab-t2':
        return table2_tab
    elif v == 'tab-g2':
        return graph2_tab
    return table1_tab



# filtering the data carbs
@app.callback(
    Output('data_crabs', 'children'),
    Input('dd-sex','value'),
    Input('dd-sp','value'))
def update_crabs(sex,species):
    filter = crabs['sex'].isin(sex) & crabs['sp'].isin(species)
    return crabs[filter].to_json()


# filtering the data air
@app.callback(
    Output('data_air', 'children'),
    Input('dd-month','value'),
    Input('day','value'))
def update_air(month,day):
    filter = air['Month'].isin(month) & air['Day'].isin(day)
    return air[filter].to_json()


# updating the table 1
@app.callback(
     Output('my-table', 'data'),
     Input('data_crabs', 'children'),
     State('tabs','value'))
def update_table_tab(data, tab):
    if tab != 'tab-t':
        return None
    crabs = pd.read_json(data)
    return crabs.to_dict("records")


# updating the table 2
@app.callback(
     Output('my-table_air', 'data'),
     Input('data_air', 'children'),
     State('tabs','value'))
def update_table_tab_air(data, tab):
    if tab != 'tab-t':
        return None
    crabs = pd.read_json(data)
    return crabs.to_dict("records")

#updating the graph 1
@app.callback(
     Output('sca_crabs', 'figure'),
     Input('dd-x', 'value'),
     Input('dd-y','value'),
     Input('color','value'),
     State('tabs','value'))
def update_figure(varx, vary, color, tab):
    if tab != 'tab-g':
        return None    
    return px.scatter(crabs, x=varx, y=vary, custom_data=['BD'], color=color)

#updating the graph 2
@app.callback(
     Output('sca_air', 'figure'),
     Input('dd-x_air', 'value'),
     Input('dd-y_air','value'),
     Input('color','value'),
     State('tabs','value'))
def update_figure_air(varx, vary, color, tab):
    if tab != 'tab-g':
        return None    
    return px.scatter(air, x=varx, y=vary, custom_data=['Ozone'], color=color)


#updating the table below the graph with the selected points
@app.callback(
    Output('selected_crabs', 'data'),
    Input('sca_crabs', 'selectedData'))
def display_selected_data(selectedData):
    if selectedData is None:
        return None
    names = [o['customdata'][0] for o in selectedData['points']]
    filter = crabs['BD'].isin(names)
    return crabs[filter].to_dict('records')

@app.callback(
    Output('selected_air', 'data'),
    Input('sca_air', 'selectedData'))
def display_selected_data_air(selectedData):
    if selectedData is None:
        return None
    names = [o['customdata'][0] for o in selectedData['points']]
    filter = crabs['Ozone'].isin(names)
    return air[filter].to_dict('records')


if __name__ == '__main__':
    app.server.run(debug=True)
    