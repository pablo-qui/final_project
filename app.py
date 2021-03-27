import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import pandas as pd
import plotly.express as px
import json

crabs_url = 'https://raw.githubusercontent.com/pablo-qui/final_project/master/crabs.csv'
crabs = pd.read_csv(crabs_url)
crabs.drop('index', inplace=True, axis=1)


crabs_cols = [{"name": i, "id": i} for i in crabs.columns]
crabs_sex = crabs['sex'].sort_values().unique()
opt_sex = [{'label': x, 'value': x} for x in crabs_sex]
crabs_sp = crabs['sp'].sort_values().unique()
opt_sp = [{'label': x , 'value': x} for x in crabs_sp]
variables = crabs.columns[2:7]
opt_var = [{'label': x , 'value': x} for x in variables]

#col_vore = {x:px.colors.qualitative.Pastel[i] for i, x in enumerate(df_vore)}


app = dash.Dash(__name__, title="Final Project Dash App")

markdown_text = '''
## Some references
- [Dash HTML Components](dash.plotly.com/dash-html-components)
- [Dash Core Components](dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](dash-bootstrap-components.opensource.faculty.ai/docs/components)  
'''

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
                data = crabs.to_dict("records")
            )
])
graph1_tab = html.Div([
    html.Label(["Select variable for the X axis:",
            dcc.Dropdown('dd-x',
                options= opt_var,
                value= [variables[0]],
                multi= False
            )
        ]),
    html.Label(["Select variable for the Y axis:",
            dcc.Dropdown('dd-y',
                options= opt_var,
                value= [variables[0]],
                multi= False
            )
        ]),
    dcc.Graph(id="sca_crabs",
        figure= px.scatter(crabs,
            x="FL",
            y="RW",
            color="sex")            
    )
])

table2_tab = html.Div([
    dcc.Markdown(variables)
])

graph2_tab = html.Div([
    dcc.Markdown('graph 2')
])

app.layout = html.Div([
     dcc.Markdown(markdown_text),
     html.Div(id="data_crabs",style={'display':'none'}),
     dcc.Tabs(id="tabs", value='tab-t', children=[
            dcc.Tab(label='Table 1', value='tab-t'),
            dcc.Tab(label='Graph 1', value='tab-g'),
            dcc.Tab(label='Table 2', value='tab-t2'),
            dcc.Tab(label='Graph 2', value='tab-g2')
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

# filtering the data
@app.callback(
    Output('data_crabs', 'children'),
    Input('dd-sex','value'),
    Input('dd-sp','value'))
def update_crabs(sex,species):
    filter = crabs['sex'].isin(sex) & crabs['sp'].isin(species)
    return crabs[filter].to_json()

# updating the table
@app.callback(
     Output('my-table', 'data'),
     Input('data_crabs', 'children'),
     State('tabs','value'))
def update_table_tab(data, tab):
    if tab != 'tab-t':
        return None
    crabs = pd.read_json(data)
    return crabs.to_dict("records")

#updating the graph
@app.callback(
     Output('sca_crabs', 'figure'),
     Input('dd-x', 'value'),
     Input('dd-y','value'),
     State('tabs','value'))
def update_figure(varx, vary,tab):
    if tab != 'tab-g':
        return None    
    return px.scatter(crabs, x=varx, y=vary ,color='sex')


if __name__ == '__main__':
    app.server.run(debug=True)
    