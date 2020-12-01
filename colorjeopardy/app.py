import dash
from flask import Flask, session
from .colors import COLORS
import random
import datetime as dt


external_stylesheets = ["./assets/bootstrap.min.css", "./assets/style.css"]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"charset": "utf-8"},
        {"http-equiv": "X-UA-Compatible", "content": "IE=edge"},
        # needed for iframe resizer
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

server = app.server

app.config.suppress_callback_exceptions = True
app.title = "colorjeopardy"

app.secret_key = b"456ygrtbffgd4w5ygvd"

