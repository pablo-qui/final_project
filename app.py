import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import pandas as pd
import plotly.express as px
import json



app = dash.Dash(__name__, title="Dash App")

markdown_text = '''
## Some references
- [Dash HTML Components](dash.plotly.com/dash-html-components)
- [Dash Core Components](dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](dash-bootstrap-components.opensource.faculty.ai/docs/components)  
'''

table1_tab = html.Div([
    dcc.Markdown('table 1')
])
graph1_tab = html.Div([
    dcc.Markdown('graph 1')
])

table2_tab = html.Div([
    dcc.Markdown('table 2')
])

graph2_tab = html.Div([
    dcc.Markdown('graph 2')
])

app.layout = html.Div([
     dcc.Markdown(markdown_text),
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



if __name__ == '__main__':
    app.server.run(debug=True)
    