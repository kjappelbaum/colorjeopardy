# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

import dash_table
import pandas as pd

import sqlalchemy as db
from dash.dependencies import Input, Output, State

# SQL Engine
disk_engine = db.create_engine(
    "sqlite:///data_entry.db", connect_args={"check_same_thread": False}
)
connection = disk_engine.connect()
metadata = db.MetaData()
SQL_table = db.Table(
    "data_entries",
    metadata,
    db.Column("color_string", db.String(255)),
    db.Column("color_hex", db.String(255)),
    db.Column("time_stamp", db.DATETIME, primary_key=True),
)

app = dash.Dash(__name__)
server = app.server

app.config.suppress_callback_exceptions = False

app.layout = html.Div([
    html.H1('What Is This Color?'),
    daq.ColorPicker(
        id='my-color-picker',
        label='Color Picker',
        value=dict(hex='#119DFF')
    ),
    html.Div(id='color-picker-output')
])


@app.callback(
    dash.dependencies.Output('color-picker-output', 'children'),
    [dash.dependencies.Input('my-color-picker', 'value')])
def update_output(value):
    return 'The selected color is {}.'.format(value)



if __name__ == "__main__":
    app.run_server(debug=True)
    