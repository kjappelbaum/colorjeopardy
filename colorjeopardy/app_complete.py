import dash
import dash_daq as daq
import dash_html_components as html

layout = html.Div(
    [
        html.Div(
            [
                html.H1("Thank you for your participation!"),
                html.P(
                    "You can take this questionaire as often as you want!",
                    className="lead",
                ),
            ],
            className="jumbotron",
        ),
        html.Div(
            [
                html.Hr(),
                html.Footer(
                    "© Laboratory of Molecular Simulation (LSMO), École polytechnique fédérale de Lausanne (EPFL)"
                ),
            ],
            className="container",
        ),
    ],
    className="container",
    # tag for iframe resizer
    **{"data-iframe-height": ""},
)
