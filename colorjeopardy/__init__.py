import dash
import dash_daq as daq
import dash_html_components as html

external_stylesheets = ['assets/bootstrap.min.css', 'assets/style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div([
            html.Div([
            html.H1('What is this color?', className='display-3'),
            html.P('Help our research by selecting the color on using the color picker.', className='lead'),
            daq.ColorPicker(
                id='color-picker',
                value=dict(hex='#119DFF'),
                theme={'dark': True},
                size=320,
                style={'border':'opx solid', 'border-radius': 0, 'outline': 0, 'box-shadow': None, 'text-align': 'center'}
            ),
             html.Div(id='color-picker-output'),
             html.Div([
                             html.P('Click on next to save and get the next color.', className='lead')
            ],  className='container'),
             html.Button('Next', id='button', className='btn btn-primary btn-lg btn-block')
             ], className='container', id='main',),

    ],className='jumbotron'),
        html.Div([
        html.Div([
            html.H2('About'),
            html.P('We will use this data to turn text descriptions of colors, that we often find in chemistry, into actual numbers.'),
            html.P('If you want to learn more, feel free to contact Kevin.'),
            html.H2('Privacy'),
            html.P('We will store no personal data that can identify you.')
            ],className='container'),
    html.Hr(),
    html.Footer('© Laboratory of Molecular Simulation (LSMO), École polytechnique fédérale de Lausanne (EPFL)')
     ], className='container' ),
    ])


@app.callback(
    dash.dependencies.Output('main', 'style'),
    [dash.dependencies.Input('color-picker', 'value')])
def update_output(value):
    return {'color': value['hex']}


if __name__ == '__main__':
    app.run_server(debug=True)