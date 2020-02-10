import dash
import dash_daq as daq
from flask import redirect, session
import dash_core_components as dcc
import dash_html_components as html
import sqlalchemy as db
import random
import datetime as dt
from .app import app
from .colors import COLORS

COUNTER_MAX = 5


disk_engine = db.create_engine(
    "postgres://wrjrddoanrkvqp:f7ba4eb5ebb13da9634f32d258bcc06f93a55a8e55d4b01041aea04871c366b8@ec2-54-247-125-38.eu-west-1.compute.amazonaws.com:5432/d2inhdasduajbn")


connection = disk_engine.connect()
metadata = db.MetaData(connection)
SQL_table = db.Table(
    "data_entry",
    metadata,
    db.Column("color_string", db.String(255)),
    db.Column("hex", db.String(255)),
    db.Column("starttime", db.DATETIME),
    db.Column("time_stamp", db.DATETIME, primary_key=True),
)


layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            "Please pick this color: ", className="display-3", id="h1"
                        ),
                        html.P(
                            "Help our research by selecting the color that most resembles the word using the color picker.",
                            className="lead",
                        ),
                        html.P(
                            "Use the slider to select the region in color space and pointer for detailed selection.",
                            className="lead",
                        ),
                        daq.ColorPicker(
                            id="color-picker",
                            # value=dict(hex=session.get(RAND_COLOR)),
                            size=255,
                            theme={"dark": True, "detail": None, "secondary": None},
                            style={
                                "border": "0px solid",
                                "borderRadius": 0,
                                "outline": 0,
                                "boxShadow": None,
                                "textAlign": "Center",
                                "marginBottom": 20,
                                "display": "inline-block",
                            },
                        ),
                        html.Div(id="color-picker-output"),
                        html.Div(
                            [
                                html.P(
                                    "Click on 'Next' to save and get the next color.",
                                    className="lead",
                                )
                            ],
                            className="container",
                        ),
                        html.Button(
                            "Next ({}/{})".format(0, COUNTER_MAX),
                            id="next",
                            className="btn btn-primary btn-lg btn-block",
                        ),
                        html.Div(id="button-out", style={"display": "none"}),
                        html.P(),
                        html.Button(
                            "Skip",
                            id="skip",
                            className="btn btn-secondary btn-lg btn-block",
                        ),
                    ],
                    className="container",
                    id="main",
                ),
                html.Div(id="skip-button-out", style={"display": "none"}),
            ],
            className="jumbotron",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("About"),
                        html.P(
                            "We will use this data to turn text descriptions of colors, that we often find in chemistry, into actual numbers. This will help us in building models that can predict the color of chemical compounds."
                        ),
                        html.P(
                            "To avoid any potential biases, we chose the colors randomly and also initalize the color picker randomly."
                        ),
                        html.P(
                            [
                                "If you want to learn more, feel free to contact ",
                                html.A("Kevin", href="mailto:kevin.jablonka@epfl.ch"),
                                ".",
                            ]
                        ),
                        html.P(
                            [
                                "We commit to relase this dataset in curated form under ",
                                html.A(
                                    "CC BY-SA 4.0 license",
                                    href="https://creativecommons.org/licenses/by-sa/4.0/",
                                ),
                                ".",
                            ]
                        ),
                        html.H3("Technical Details"),
                        html.P(
                            [
                                "This app was implemented using ",
                                html.A("Dash", href="https://plot.ly/dash/"),
                                " and ",
                                html.A(
                                    "Flask",
                                    href="https://flask.palletsprojects.com/en/1.1.x/",
                                ),
                                ". The current progress is saved as ",
                                html.A(
                                    "session cookie.",
                                    href="https://allaboutcookies.org/cookies/session-cookies-used-for.html",
                                ),
                                " If you experience any issues you might try switching the browser or delete cache and cookies.",
                            ]
                        ),
                        html.H2("Privacy"),
                        html.P("We will store no personal data that can identify you."),
                    ],
                    className="container",
                ),
                html.Hr(),
                html.Footer(
                    "© Laboratory of Molecular Simulation (LSMO), École polytechnique fédérale de Lausanne (EPFL)"
                ),
            ],
            className="container",
        ),
    ],
    # tag for iframe resizer
    **{"data-iframe-height": ""},
)


app.layout = layout


@app.callback(
    dash.dependencies.Output("h1", "children"),
    [dash.dependencies.Input("button-out", "children")],
)
def color_picker(color):
    return "Please pick this color: {}".format(session.get("COLOR"))


@app.callback(
    dash.dependencies.Output("color-picker", "value"),
    [dash.dependencies.Input("button-out", "children")],
)
def color_picker(color):
    return dict(hex=session.get("RAND_COLOR"))


@app.callback(
    dash.dependencies.Output("next", "children"),
    [dash.dependencies.Input("button-out", "children")],
)
def color_picker(color):
    return "Next ({}/{})".format(session.get("COUNTER"), COUNTER_MAX)


@app.callback(
    dash.dependencies.Output("button-out", "children"),
    [
        dash.dependencies.Input("next", "n_clicks"),
        dash.dependencies.Input("skip", "n_clicks"),
    ],
    [dash.dependencies.State("color-picker", "value")],
)
def entry_to_db(submit_entry, skip, color):
    hexcolor = color["hex"]
    if submit_entry:
        time_stamp = dt.datetime.now()
        app.logger.info(
            "Logging to db. Color string: {}, hex: {}, starttime: {}. time_stamp: {}".format(
                session.get("COLOR"), hexcolor, session.get("STARTTIME"), time_stamp
            )
        )
        entry = [
            {
                "color_string": session.get("COLOR"),
                "hex": hexcolor,
                "starttime": session.get("STARTTIME"),
                "time_stamp": time_stamp,
            }
        ]
        insert_entry = connection.execute(db.insert(SQL_table), entry)
        # init color start
        session["COLOR"] = random.choice(COLORS)
        r = lambda: random.randint(0, 255)
        session["RAND_COLOR"] = "#%02X%02X%02X" % (r(), r(), r())
        session["STARTTIME"] = dt.datetime.now()
        # init color end
        session["COUNTER"] += 1
        if session.get("COUNTER") >= COUNTER_MAX:
            app.logger.info(
                "Counter equals or exceeds max counter, forwarding to completion page."
            )
            return dcc.Location(
                pathname="/complete", id="forward_complete"
            )  # Forward to thank you when COUNTER == MAX_COUNTER
        return hexcolor
    if skip:
        app.logger.info("Skipping")
        # init color start
        session["COLOR"] = random.choice(COLORS)
        r = lambda: random.randint(0, 255)
        session["RAND_COLOR"] = "#%02X%02X%02X" % (r(), r(), r())
        session["STARTTIME"] = dt.datetime.now()
        # init color end
        hexcolor = color["hex"]
        return hexcolor

    raise dash.exceptions.PreventUpdate


@app.callback(
    dash.dependencies.Output("main", "style"),
    [dash.dependencies.Input("color-picker", "value")],
)
def update_output(value):
    return {"color": value["hex"]}
