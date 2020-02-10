import dash

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

app.config.suppress_callback_exceptions = False
app.title = "colorjeopardy"
