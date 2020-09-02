import re
from datetime import datetime as dt, datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

data = pd.read_csv('sleepdata.csv', delimiter=';')
data['Time in bed'] = pd.to_datetime(data['Time in bed']).dt.time
data['Start'] = pd.to_datetime(data['Start'])
print(data['Start'].dt.date)

# fig = go.Figure(data=[go.Scatter(x=data[data.columns[0]], y=data[data.columns[3]])])
fig = px.line(data, x=data['Start'].dt.date, y=data['Time in bed'])

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='My personal Dashboard about my Sleep'),

    html.Div(children='''
        LORUM IPSUM
    '''),

    dcc.Checklist(
        options=[
            {'label': data.columns[2] + '', 'value': 'SQ'},
            {'label': data.columns[3], 'value': 'TIB'},
            {'label': data.columns[4], 'value': 'WU'}
        ],
        value=['SQ', 'TIB', 'WU'],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=(datetime.today()),
        min_date_allowed=data['Start'].min(),
        max_date_allowed=data['Start'].max(),
        end_date_placeholder_text='Select a date!'
    ),
    html.Div(id='output-container-date-picker-range'),
    dcc.Graph(
        figure=fig,
        id='my-graph'
    )
])


# callback for datepicker
@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string
    if end_date is not None:
        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + ' | ' + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


if __name__ == '__main__':
    app.run_server(debug=True)
