import os
import dash
import dash_daq as daq
from flask import redirect, session
import dash_core_components as dcc
import dash_html_components as html
import sqlalchemy as db
import random
import datetime as dt
from . import app_complete, app_main
from .app import app, server
from .colors import COLORS

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    session["COLOR"] = random.choice(COLORS)
    r = lambda: random.randint(0, 255)
    session["RAND_COLOR"] = "#%02X%02X%02X" % (r(), r(), r())
    session["STARTTIME"] = dt.datetime.now()
    session["COUNTER"] = 0

    app.logger.info("Pathname is {}".format(pathname))
    if pathname == "/":
        return app_main.layout
    elif pathname == "/complete":
        return app_complete.layout
    else:
        return app_main.app.layout


if __name__ == "__main__":
    app.server.secret_key = os.urandom(24)
    app.run_server(debug=True)
