import dash
import dash_daq as daq
from flask import redirect
import dash_core_components as dcc
import dash_html_components as html
import sqlalchemy as db
import random
import datetime as dt
from . import app_complete, app_main
from .app import app, server

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    app.logger.info("Pathname is {}".format(pathname))
    if pathname == "/":
        return app_main.layout
    elif pathname == "/complete":
        return app_complete.layout
    else:
        return app_main.layout


if __name__ == "__main__":
    app.run_server(debug=True)
