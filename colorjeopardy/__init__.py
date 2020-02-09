import dash
import dash_daq as daq
import dash_html_components as html
import sqlalchemy as db
import random
import datetime as dt

# Also track startime and use difference between start and stop to discard entries 

COLORS = ['pink', 'colorless', 'reddish brown', 'purple', 'brown', 'red',
       'blue',  'yellow', 'green', 'black', 'violet', 'rose',
       'deep blue', 'sky blue', 'pale yellow', 'dark green', 'red brown',
       'orange', 'dark red', 'grey', 'white', 'light blue', 'black brown',
       'pale pink', 'slightly pink', 'red-brown', 'light purple',
       'green yellow', 'dark brown', 'primrose yellow', 'cyan',
       'light green', 'faint pink', 'orange brown', 'dark blue',
       'red/purple', 'blue green', 'pale brown', 'pink/purple',
       'light yellow', 'pale green', 'dark turquiose', 'yellowish white',
       'light brown', 'pale blue', 'dark purple', 'yellow-green',
       'black green', 'green-yellow', 'flavescens', 'light pink',
       'intense violet', 'aubergine', 'yellowish yellow', 'orange red',
       'deep-blue', 'lilac', 'pale violet', 'courless', 'dark-violet',
       'gold', 'light red', 'yellow-orange', 'amber', 'pale-yellow',
       'green-black', 'buff', 'deep yellow', 'deep red',
       'whiteish colorless', 'red-violet', 'pale red', 'lavender',
       'straw yellow', 'yellow green', 'brown-red', 'purple black',
       'black purple', 'turquoise', 'brown orange', 'light-purple',
       'greenish blue', 'light violet', 'aquamarine', 'wheat', 'ruby red',
       'navy blue', 'deep purple', 'green blue', 'plate', 'gray',
       'red-orange', 'black-brown', 'red purple', 'dark pink',
       'dark purplish-red', 'purple-red', 'pink-violet',
       'blackish purple', 'reddish purple', 'bright yellow',
       'turquoise blue', 'black red', 'orange-red', 'reddish',
       'greenish-yellow', 'mauve', 'orange-yellow', 'dark violet',
       'red-yellow', 'yellowish', 'translucent', 'magenta', 'beige',
       'greenish cyan', 'dark orange', 'cherry red', 'deep blue-black',
       'light orange', 'deep brown', 'green-blue', 'dark yellow',
       'crimson', 'orange yellow', 'white', 'claybank', 'azure',
       'glaucous', 'greenish green', 'deep green', 'violet red',
       'yellow-red', 'greenish-blue', 'light colorless', 'brown yellow',
       'bluish violet', 'golden yellow', 'red-black', 'intense purple',
       'peach', 'scarlet', 'dull dark black', 'violet-red', 'dark rose',
       'blue violet', 'amaranthine', 'jasmine', 'light-brown',
       'purple-blue', 'dark-blue', 'pink-purple', 'pink-red', 'light',
       'purple red', 'brown-yellow', 'grass green', 'jonquil',
       'yellowish green', 'pale straw', 'pale purple', 'dark-red',
       'green/brown', 'green-brown']

# SQL Engine
disk_engine = db.create_engine(
    "sqlite:///data_entry.db", connect_args={"check_same_thread": False}
)


external_stylesheets = ['assets/bootstrap.min.css', 'assets/style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

connection = disk_engine.connect()
metadata = db.MetaData(connection)
SQL_table = db.Table(
    "data_entry",
    metadata,
    db.Column("color_string", db.String(255)),
    db.Column("hex", db.String(255)),
    db.Column("time_stamp", db.DATETIME, primary_key=True),
)


server = app.server

app.config.suppress_callback_exceptions = False


COLOR = random.choice(COLORS)
r = lambda: random.randint(0,255)
RAND_COLOR = '#%02X%02X%02X' % (r(),r(),r())

def init_color():
    global COLOR
    global RAND_COLOR
    COLOR = random.choice(COLORS)
    r = lambda: random.randint(0,255)
    RAND_COLOR = '#%02X%02X%02X' % (r(),r(),r())


app.layout = html.Div(
    [
        html.Div([
            html.Div([
            html.H1('Please pick this color: {}'.format(COLOR), className='display-3'),
            html.P('Help our research by selecting the color the most resembles the word using the color picker.', className='lead'),
            daq.ColorPicker(
                id='color-picker',
                value=dict(hex=RAND_COLOR),
                theme={'dark': True},
                size=690,
                style={'border':'0px solid', 'border-radius': 0, 'outline': 0, 'box-shadow': None, 'text-align': 'center', 'margin-bottom': 20}
            ),
             html.Div(id='color-picker-output'),
             html.Div([
            html.P('Click on next to save and get the next color.', className='lead')
            ],  className='container'),
             html.Button('Next', id='next', className='btn btn-primary btn-lg btn-block'),
             html.Div(id='button-out')
             ], className='container', id='main'),

    ],className='jumbotron'),
        html.Div([
        html.Div([
            html.H2('About'),
            html.P('We will use this data to turn text descriptions of colors, that we often find in chemistry, into actual numbers. This will help us in building models that can predict the color of chemical compounds.'),
            html.P('If you want to learn more, feel free to contact Kevin.'),
            html.P('We will make this dataset available in curated form under creative commons license.'),
            html.H2('Privacy'),
            html.P('We will store no personal data that can identify you.')
            ],className='container'),
    html.Hr(),
    html.Footer('© Laboratory of Molecular Simulation (LSMO), École polytechnique fédérale de Lausanne (EPFL)')
     ], className='container' ),
    ])


@app.callback(
    dash.dependencies.Output("color-picker", "value"), 
    [dash.dependencies.Input("button-out", "children")]
)
def color_picker(color):
    return dict(hex=RAND_COLOR)


@app.callback(
    dash.dependencies.Output("button-out", 'children'),
    [dash.dependencies.Input("next", "n_clicks")],
    [
        dash.dependencies.State("color-picker", "value"),
    ],
)
def entry_to_db(submit_entry, color):
    hexcolor = color['hex']
    if submit_entry:
        entry = [
            {
                "color_string": COLOR,
                "hex": hexcolor,
                "time_stamp": dt.datetime.now(),
            }
        ]
        insert_entry = connection.execute(db.insert(SQL_table), entry)
        init_color()
        return color
        
    raise dash.exceptions.PreventUpdate

@app.callback(
    dash.dependencies.Output('main', 'style'),
    [dash.dependencies.Input('color-picker', 'value')])
def update_output(value):
    return {'color': value['hex']}


if __name__ == '__main__':
    app.run_server(debug=True)